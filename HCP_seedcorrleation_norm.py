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
import sys
pathfiles=''
sys.path.append(pathfiles+'/Scripts/')
import alb_MM_functions as alb

#####################this script take all FC concatenate network seed maps (full set), perform a mixture modelling for each participant for each, mixture modelling is done at the brain structure level 
if __name__ == "__main__":
    maxiters=100
    tol=0.000001 #relative tolerance for convergence
    MM=2 #2 is'GGM', 3 is 'GIM'

    #get and load template
    #let's load the SNR mask of the MA01 and save output with MA01snrmask
    #snrmask
    sub=['MA01','MAC01','MAC02']
    snrdataall=[nibabel.load(pathfiles+'/RestProcessing/MA/'+s+'_SNRavgmap.dtseries.nii').get_fdata()[0] for s in sub]
    keepdata=[]
    #extract network name as well so I can save dscalar
    netval=np.array([0,1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    mapname=['???','DMN','Parieto-Occipital','VisLat','VisDor-ventralstream','VisV5','VisV1','FPN','DorsAtt','Premotor','Language','Salience','CON','MedialParietal','MotorHand','MotorMouth','MotorFoot','Auditory','SCAN']
    val=netval[1:]
    
    namelist=mapname[1:]
    
    
    for e,s in enumerate(sub):
        snrdata=snrdataall[e]

        
        
        #
        fileloc=pathfiles+'/RestProcessing/MA/snrselec_NeighborCleaned_smooth255/'+s+'/FC/'+s+'_basetemplate_18MSHBMnet_'+s+'snrmask_netstrength.dscalar.nii'
        raw=nibabel.load(fileloc)
        data=raw.get_fdata()
        axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
        # You'll want the brain model axis
        label_axis, brain_model_axis = axes
        #extract all the structures (left and right)
        liststructure=np.unique(brain_model_axis.name)
        liststructure=np.unique([l.replace('_LEFT','').replace('_RIGHT','') for l in liststructure])
        data=data.T
        for i,structure in enumerate(liststructure):
            if structure!='CIFTI_STRUCTURE_BRAIN_STEM':
                locvox=np.array(np.where(snrdata>=20)[0])[np.where((np.array(brain_model_axis.name)[np.where(snrdata>=20)[0]]==structure+'_RIGHT')|(np.array(brain_model_axis.name)[np.where(snrdata>=20)[0]]==structure+'_LEFT'))[0]]
                locvoxall=np.where((np.array(brain_model_axis.name)==structure+'_RIGHT')|(np.array(brain_model_axis.name)==structure+'_LEFT'))[0]
            else:
                locvox=np.array(np.where(snrdata>=20)[0])[np.where(np.array(brain_model_axis.name)[np.where(snrdata>=20)[0]]==structure)[0]]
                locvoxall=np.where(np.array(brain_model_axis.name)==structure)[0]
            
            #for each structure, get all voxels within mask of interest across all network and normalize, put back (if not mask voxels selection, enhance FC by noise)
            prov=np.concatenate(data[locvox],0)
            output=alb.mmfit3(prov, maxiters,tol,MM)
            #data[locvoxall]=(data[locvoxall]-np.nanmean(data[locvox]))/np.nanstd(data[locvox])
            data[locvoxall]=(data[locvoxall]-output[0])/np.sqrt(output[1])
        #save
        time_axis2=nibabel.cifti2.cifti2_axes.ScalarAxis(namelist)
        img=ci.Cifti2Image(data.T, header=(time_axis2, brain_model_axis),
                    nifti_header=raw.nifti_header)
        ci.save(img,pathfiles+'/RestProcessing/MA/snrselec_NeighborCleaned_smooth255/'+s+'/FC/'+s+'_basetemplate_18MSHBMnet_'+s+'snrmask_netstrength_normperstructureMM.dscalar.nii')
        


        
        #			
        data=data.T    
        keepdata+=[copy.deepcopy(data)]
    
    ##now HCP
    savedir = pathfiles+"/RestProcessing/HCP/"
    
    
    listsub=[i for i in open(pathfiles+'/data_HCP/Subject_IDs.txt','r').read().split('\n') if i!='']
    j=0
    for e, s in enumerate(listsub):
        if e / 50.0 - int(e / 50.0) == 0:
            print(e)
        

        #they are 4 runs normally 1 and 2, RL and LR
        dataloc=savedir+'/'+s+'_basetemplate_18MSHBMnet_MAsnrmask_netstrength.dscalar.nii'

        #if anyfile exists
        if os.path.exists(dataloc):
            j+=1
            fileloc=savedir+'/'+s+'_basetemplate_18MSHBMnet_MAsnrmask_netstrength.dscalar.nii'
            raw=nibabel.load(fileloc)
            data=raw.get_fdata()
            axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
            # You'll want the brain model axis
            label_axis, brain_model_axis = axes
            #extract all the structures (left and right)
            liststructure=np.unique(brain_model_axis.name)
            liststructure=np.unique([l.replace('_LEFT','').replace('_RIGHT','') for l in liststructure])
            data=data.T
            for i,structure in enumerate(liststructure):
                if structure!='CIFTI_STRUCTURE_BRAIN_STEM':
                    locvoxall=np.where((np.array(brain_model_axis.name)==structure+'_RIGHT')|(np.array(brain_model_axis.name)==structure+'_LEFT'))[0]
                else:
                    locvoxall=np.where(np.array(brain_model_axis.name)==structure)[0]
                
                #for each structure, get all voxels within mask of interest across all network and normalize, put back (if not mask voxels selection, enhance FC by noise)
                prov=np.concatenate(data[locvoxall],0)
                output=alb.mmfit3(prov, maxiters,tol,MM)
                prov=prov[~np.isnan(prov)]
                data[locvoxall]=(data[locvoxall]-output[0])/np.sqrt(output[1])
                #data[locvoxall]=(data[locvoxall]-np.nanmean(data[locvoxall]))/np.nanstd(data[locvoxall])

            #save
            time_axis2=nibabel.cifti2.cifti2_axes.ScalarAxis(namelist)
            img=ci.Cifti2Image(data.T, header=(time_axis2, brain_model_axis),
                        nifti_header=raw.nifti_header)
            ci.save(img,savedir+'/'+s+'_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM.dscalar.nii')

            data=data.T
            
            
            #calculate running mean and std
            if j==1:
                tcstruct2mean=copy.deepcopy(data)
                tcstruct2sd=np.zeros(data.shape)
            
            else:
                #rollingmean
                tcstruct2meanprov=((j-1)/j)*tcstruct2mean+(data)/j
                #rollingstd
                tcstruct2sd=((j-1)/j)*tcstruct2sd+((j-1)/j)*(tcstruct2mean-tcstruct2meanprov)**2+(1/j)*(data-tcstruct2meanprov)**2
                tcstruct2mean=copy.deepcopy(tcstruct2meanprov)
        


        else:
            print('no '+s)
    
    #save running mean and std 
    img=ci.Cifti2Image(tcstruct2mean, header=(time_axis2, brain_model_axis),
                nifti_header=raw.nifti_header)
    ci.save(img,savedir+'/allMEAN_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM.dscalar.nii')
    img=ci.Cifti2Image(tcstruct2sd, header=(time_axis2, brain_model_axis),
                nifti_header=raw.nifti_header)
    ci.save(img,savedir+'/allSTD_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM.dscalar.nii')

    ###calc zstats and save
    #need to deal with the size of the subcortex

    
    
    #normative modelling quickly
    raw=nibabel.load(savedir+'/allMEAN_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructure.dscalar.nii')
    data=raw.get_fdata()
    raw=nibabel.load(savedir+'/allSTD_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructure.dscalar.nii')
    data2=raw.get_fdata()
    axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
    # You'll want the brain model axis
    label_axis, brain_model_axis = axes
    #extract all the structures (left and right)
    liststructure=np.unique(brain_model_axis.name)
    liststructure=np.unique([l.replace('_LEFT','').replace('_RIGHT','') for l in liststructure])
    data=data.T
    data2=data2.T
    for i,structure in enumerate(liststructure):
        if structure!='CIFTI_STRUCTURE_BRAIN_STEM':
            locvoxall=np.where((np.array(brain_model_axis.name)==structure+'_RIGHT')|(np.array(brain_model_axis.name)==structure+'_LEFT'))[0]
        else:
            locvoxall=np.where(np.array(brain_model_axis.name)==structure)[0]
        
        #for each structure, get all voxels within mask of interest across all network and normalize, put back (if not mask voxels selection, enhance FC by noise)
        prov=np.concatenate(data[locvoxall],0)
        output=alb.mmfit3(prov, maxiters,tol,MM)
        #data[locvoxall]=(data[locvoxall]-np.nanmean(data[locvoxall]))/np.nanstd(data[locvoxall])
        data[locvoxall]=(data[locvoxall]-output[0])/np.sqrt(output[1])
        data2[locvoxall]=(data2[locvoxall])/(output[1])
        
    #save
    time_axis2=nibabel.cifti2.cifti2_axes.ScalarAxis(namelist)
    

    

    #save running mean and std 
    img=ci.Cifti2Image(data.T, header=(time_axis2, brain_model_axis),
                nifti_header=raw.nifti_header)
    ci.save(img,savedir+'/allMEAN_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM.dscalar.nii')
    img=ci.Cifti2Image(data2.T, header=(time_axis2, brain_model_axis),
                nifti_header=raw.nifti_header)
    ci.save(img,savedir+'/allSTD_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM.dscalar.nii')
    
    ###calc zstats and save
    #need to deal with the size of the subcortex

    
    

    #split the HCP cifti 
    
    
    for net in [savedir+'/allMEAN_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM.dscalar.nii',savedir+'/allSTD_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM.dscalar.nii',savedir+'/HCPbinary.dscalar.nii']:
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
            

    

    
    
    for s2,s in enumerate(sub):
        #read mean std and mask HCP and mask MA
        tcstruct2mean=nibabel.load(savedir+'/allMEAN_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM_'+s+'subcortmask.dtseries.nii').get_fdata()
        tcstruct2sd=nibabel.load(savedir+'/allSTD_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM_'+s+'subcortmask.dtseries.nii').get_fdata()
        raw=nibabel.load(savedir+'/HCPbinary_'+s+'subcortmask.dtseries.nii')
        hcpmask=raw.get_fdata()[0]
        
        keepdataprov=(keepdata[s2]-tcstruct2mean)/tcstruct2sd
        keepdataprov=keepdataprov.T
        keepdataprov[np.where(snrdata[s2]<20)[0]]=np.nan
        keepdataprov[np.where(hcpmask==0)[0]]=np.nan

        
        axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
        # You'll want the brain model axis
        time_axis, brain_model_axis = axes
        time_axis2=nibabel.cifti2.cifti2_axes.ScalarAxis(namelist)
        img=ci.Cifti2Image(keepdataprov.T, header=(time_axis2, brain_model_axis),
                    nifti_header=raw.nifti_header)
        ci.save(img,savedir+'/'+s+'_zscoresHCP_basetemplate_18MSHBMnet_MAsnrmaskNHCPsubcortmask_netstrength_normperstructureMM.dscalar.nii')




        



