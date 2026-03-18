# import
import glob
import numpy as np
import os
import nibabel
import subprocess
# function
# LnR
from nibabel import cifti2 as ci
import copy
##############scrpt to calculate all seed network correlation across all datasets

# do regression
def regression(data, design, mask='', demean=True, desnorm=False, resids=False):
    
    import numpy as np
        
    # Y = Xb + e
    # process Y
    
    Y = data[mask==1,:]
    
    # process X
    if design.shape[0] == Y.shape[1]:
        X = design
        
    else:
        X = design[mask==1,:]
        
    
    if demean == True:
        #demean Y
        if Y.shape[0] == X.shape[0]:
            Y = Y - np.average(Y,axis=0)
        else:
            # demean the data, subtract mean over time from each voxel
            Y = Y - np.tile(np.average(Y, axis=1), (Y.shape[1],1)).T
    
        # demean the design
        X = X - np.average(X,axis=0)#np.repeat(np.mean(X,0),len(X[0]))#.mean(axis=0)
    
    if desnorm == True:
        # variance normalize the design
        X = X/X.std(axis=0, ddof=1)

    # add constant to X
    constant = np.ones(X.shape[0])
    X = np.column_stack((constant,X))
    
    if Y.shape[1] == X.shape[0]:
        # put time in rows for regression against time course
        Y = Y.T
    
    # obtain betas
    B = np.linalg.pinv(X).dot(Y)
    # obtain residuals
    #print Y.shape, X.shape, B.shape
    eta = Y - X.dot(B)
    #print eta.shape
    
    # put betas back into image if needed
    if max(B.shape) == max(Y.shape):
        bi = np.zeros((B.shape[0],max(data.shape)))
        bi[:,mask==1] = B
        B = bi
    
    # put residuals back into image
    if resids == True:
        ei = np.zeros_like(data)
        ei[mask==1,:] = eta.T
        eta = ei
        
    # return betas and design
    # discard first beta, this is the constant
    if resids == True:
        return B[1:,:], eta
    else:
        return B[1:,:]



if __name__ == "__main__":

    #get and load template (adjust = DMN piece together, actually alreadu done)
    templateloc=pathfiles+'/infomap/MSHBM/FunctionalNetworks-18.dlabel.nii'
    raw=nibabel.load(templateloc)
    
    axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
    # You'll want the brain model axis
    label_axis, brain_model_axis = axes
    template=raw.get_fdata()[0]
    val=np.array([i for i in np.unique(template) if i!=0])
    #let's load the SNR mask of the MA01 and save output with MA01snrmask
    #snrmask
    sub=['MA01','MAC01','MAC02']
    snrdata=[nibabel.load(pathfiles+'/RestProcessing/MA/'+s+'_SNRavgmap.dtseries.nii').get_fdata()[0] for s in sub]
    snrmask=np.unique(np.where(np.array([snr[:29696+29716] for snr in snrdata])<20)[0][1]) #this is ust cortex as for the template we only care about the cortex
    template[snrmask]=-10
    keepdata=[]
    valloc=[np.where(template==v)[0] for v in val]
    #extract network name as well so I can save dscalar
    netval=np.array([0,1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    mapname=['???','DMN','Parieto-Occipital','VisLat','VisDor-ventralstream','VisV5','VisV1','FPN','DorsAtt','Premotor','Language','Salience','CON','MedialParietal','MotorHand','MotorMouth','MotorFoot','Auditory','SCAN']
    
    diclabel={netval[i]:(mapname[i],label_axis.label[0][netval[i]][1]) for i in range(len(netval))}
    namelist=[diclabel[v][0] for v in val]
    
    
    for s in sub:
        
        

        
        
        #let's also calculate it for MA01 (from template and not it's own infomap) so it's less biaised
        #load the MA concateanted file,
        fileloc=pathfiles+'/RestProcessing/MA/snrselec_NeighborCleaned_smooth255/'+s+'/'+s+'_222/'+s+'_concatenatedTC_LR_surf_subcort_222_32k_fsLR_smooth2.55_novolsmooth_newrest.dtseries.nii'
        raw=nibabel.load(fileloc)
        data=raw.get_fdata()

        				

        data=data.T
        ts=np.array([np.mean(data[v],0) for v in valloc])

        #calculate seed of each net
        data=np.array([[np.corrcoef([data[v],ts[i]])[0][1] for v in range(len(data))] for i in range(len(ts))])

        #save in GMT3/MA 
        axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
        # You'll want the brain model axis
        time_axis, brain_model_axis = axes
        time_axis2=nibabel.cifti2.cifti2_axes.ScalarAxis(namelist)
        img=ci.Cifti2Image(data, header=(time_axis2, brain_model_axis),
                    nifti_header=raw.nifti_header)
        ci.save(img,pathfiles+'/RestProcessing/MA/snrselec_NeighborCleaned_smooth255/'+s+'/FC/'+s+'_basetemplate_18MSHBMnet_'+s+'snrmask_netstrength.dscalar.nii')

        keepdata+=[copy.deepcopy(data)]
    
    ##now HCP
    savedir = ""
    

    listsub=[i for i in open(pathfiles+'/data_HCP/Subject_IDs.txt','r').read().split('\n') if i!='']
    keepsub=[]
    keepsubI=[]
    for e, s in enumerate(listsub):
        if e / 50.0 - int(e / 50.0) == 0:
            print(e)
        

        #they are 4 runs normally 1 and 2, RL and LR
        dataloc=glob.glob(pathfiles+"/HCP/Resting_State/"+s+"/MNINonLinear/Results/rfMRI_REST*/rfMRI_REST*_Atlas_hp2000_clean.dtseries.nii")

        #if anyfile exists
        if len(dataloc)!=0:
            #save subject id
            keepsub+=[s]
            keepsubI+=[e]
            #read all 4 and concatenate (see if anything else need tobe done like scrubbing but i don't have accessto any mvt file)
            for d2,d in enumerate(dataloc):
                if d2==0:
                    raw=nibabel.load(d)
                    data=raw.get_fdata()
                    #GSR
                    gs1=data.mean(axis=tuple(range(1, data.ndim)))
                    gs2=np.concatenate([[0],np.diff(gs1)],0)
                    [reg, newprov]=regression(data.T,np.array([gs1,gs2]).T,np.ones(data.T.shape[:data.ndim-1]), resids=True,desnorm=False,demean=False)
                    data=newprov.T
                    
                else:
                    prov=nibabel.load(d).get_fdata()
                    
            #then extract average timeseries fr each 18 cortical network of the template 
            
                    #GSR
                    gs1=prov.mean(axis=tuple(range(1, prov.ndim)))
                    gs2=np.concatenate([[0],np.diff(gs1)],0)
                    [reg, newprov]=regression(prov.T,np.array([gs1,gs2]).T,np.ones(prov.T.shape[:prov.ndim-1]), resids=True,desnorm=False,demean=False)
                                
                    data=np.concatenate([data,newprov.T],0)
                    
            data=data.T#newprov
            
            ts=np.array([np.mean(data[v],0) for v in valloc])

            #calculate seed of each net
            #make correaltion maps of each whole brain
            data=np.array([[np.corrcoef([data[v],ts[i]])[0][1] for v in range(len(data))] for i in range(len(ts))])

            #save in HCP GMt3 with 18MSHBMnet_MA01snrmask
            #save in GMT3/HCP
            axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
            # You'll want the brain model axis
            time_axis, brain_model_axis = axes
            time_axis2=nibabel.cifti2.cifti2_axes.ScalarAxis(namelist)
            img=ci.Cifti2Image((data), header=(time_axis2, brain_model_axis),
                        nifti_header=raw.nifti_header)
            ci.save(img,savedir+'/'+s+'_basetemplate_18MSHBMnet_MAsnrmask_netstrength.dscalar.nii')

            
            
            
            #calculate running mean and std
            if len(keepsub)==1:
                tcstruct2mean=copy.deepcopy(data)
                tcstruct2sd=np.zeros(data.shape)
            
            else:
                j=len(keepsub)
                #rollingmean
                tcstruct2meanprov=((j-1)/j)*tcstruct2mean+(data)/j
                #rollingstd
                tcstruct2sd=((j-1)/j)*tcstruct2sd+((j-1)/j)*(tcstruct2mean-tcstruct2meanprov)**2+(1/j)*(data-tcstruct2meanprov)**2
                tcstruct2mean=copy.deepcopy(tcstruct2meanprov)
        


        else:
            print('no '+s)
    #save list ID
    with open(savedir+"hcp_subID.txt",'w') as f:
        f.write('\n'.join(keepsub))

    with open(savedir+"hcp_subIDindex.txt",'w') as f:
        f.write('\n'.join([str(i) for i in keepsubI]))
    #save running mean and std 
    img=ci.Cifti2Image(tcstruct2mean, header=(time_axis2, brain_model_axis),
                nifti_header=raw.nifti_header)
    ci.save(img,savedir+'/allMEAN_basetemplate_18MSHBMnet_MAsnrmask_netstrength.dscalar.nii')
    img=ci.Cifti2Image(tcstruct2sd, header=(time_axis2, brain_model_axis),
                nifti_header=raw.nifti_header)
    ci.save(img,savedir+'/allSTD_basetemplate_18MSHBMnet_MAsnrmask_netstrength.dscalar.nii')

    ###calc zstats and save
    #need to deal with the size of the subcortex

    # binarize to use it as subcortical mask and inverse to make a subcortical mask
    raw=nibabel.load(savedir+'/allSTD_basetemplate_18MSHBMnet_MAsnrmask_netstrength.dscalar.nii')
    axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
    label_axis, brain_model_axis = axes
    data=np.sign(np.sum(raw.get_fdata(),0))
    time_axis2=nibabel.cifti2.cifti2_axes.ScalarAxis(['mask'])
    img=ci.Cifti2Image(np.array([data]), header=(time_axis2, brain_model_axis),nifti_header=raw.nifti_header)
    ci.save(img,savedir+'/HCPbinary.dscalar.nii')
    
    #split the HCP cifti 
    
    
    for net in [savedir+'/allMEAN_basetemplate_18MSHBMnet_MAsnrmask_netstrength.dscalar.nii',savedir+'/allSTD_basetemplate_18MSHBMnet_MAsnrmask_netstrength.dscalar.nii',savedir+'/HCPbinary.dscalar.nii']:
        tag3='dscalar'

        subprocess.call(['wb_command','-cifti-separate-all',net,'-volume',net.replace('.'+tag3+'.nii','_vol.nii.gz'),'-left',net.replace('.'+tag3+'.nii','_L.func.gii'),'-right',net.replace('.'+tag3+'.nii','_R.func.gii')])

        netV=net.replace('.'+tag3+'.nii','_vol.nii.gz')
        for s2,s in enumerate(sub):
            subcorticaldir=pathfiles+'/DataProcessing/MemoryAthlete/'+s+'/subcortical_mask'
            if s == 'MAC01':
                subcorticaldir=subcorticaldir+'7.2'
            #if s==0:
            subcorticalmask=subcorticaldir+'/subcortical_mask_LR_MNI152_T1_2mm.nii'
            #save-flirt-load
            # bring it to MA cifti 
            # check if same resolution as MA
            if s2==0:
                #reshape
                subprocess.call(['flirt','-in',netV,'-ref',subcorticalmask,'-applyxfm','-usesqform','-out',netV.replace('.nii.gz','_MAshape.nii.gz')])
            rightfile=net.replace('.'+tag3+'.nii','_R.func.gii')
            leftfile=net.replace('.'+tag3+'.nii','_L.func.gii')
            Subcortical=netV.replace('.nii.gz','_MAshape.nii.gz')
            

            #put hcp result in MA cifti mask
            subprocess.call(['wb_command','-cifti-create-dense-timeseries',net.replace('.'+tag3+'.nii','_'+s+'subcortmask.dtseries.nii'),'-volume',Subcortical,subcorticalmask,'-left-metric',leftfile,'-roi-left',subcorticaldir+'/L.atlasroi.32k_fs_LR.shape.gii','-right-metric',rightfile,'-roi-right',subcorticaldir+'/R.atlasroi.32k_fs_LR.shape.gii'])
            

    

    
    
    #probably need to redo with smoothing of HCP
    for s2,s in enumerate(sub):
        #read mean std and mask HCP and mask MA
        tcstruct2mean=nibabel.load(savedir+'/allMEAN_basetemplate_18MSHBMnet_MAsnrmask_netstrength_'+s+'subcortmask.dtseries.nii').get_fdata()
        tcstruct2sd=nibabel.load(savedir+'/allSTD_basetemplate_18MSHBMnet_MAsnrmask_netstrength_'+s+'subcortmask.dtseries.nii').get_fdata()
        raw=nibabel.load(savedir+'/HCPbinary_'+s+'subcortmask.dtseries.nii')
        hcpmask=raw.get_fdata()[0]
        
        keepdataprov=(keepdata[s2]-tcstruct2mean)/tcstruct2sd
        keepdataprov=keepdataprov.T
        keepdataprov[np.where(snrdata[s2]<20)[0]]=-10
        keepdataprov[np.where(hcpmask==0)[0]]=-10

        
        axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
        # You'll want the brain model axis
        time_axis, brain_model_axis = axes
        time_axis2=nibabel.cifti2.cifti2_axes.ScalarAxis(namelist)
        img=ci.Cifti2Image(keepdataprov.T, header=(time_axis2, brain_model_axis),
                    nifti_header=raw.nifti_header)
        ci.save(img,savedir+'/'+s+'_zscoresHCP_basetemplate_18MSHBMnet_MAsnrmaskNHCPsubcortmask_netstrength.dscalar.nii')




        



