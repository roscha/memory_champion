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

pathfiles=''
###script to calculate the network mean FC per resting state runs
netval=np.array([1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
if __name__ == "__main__":

    sessions=[['vc...'],['vc...'],['vc...']]
    bold=[['...'],['...'],['...']]


    cor2021cerebnet=dict()
    subjects=['MA01','MAC01','MAC02']
    for e,s in enumerate(subjects):
        cor2021cerebnet[s]=dict()



    
        #network individual label
        img_contour=pathfiles+'/RestProcessing/MA/NeighborCleaned_smooth255/MSHBM/ind_parcellation/sub'+str(e+1)+'/MS-HBM_FunctionalNetworks_VertexWiseThresh0.01_w20_c20-18net.dlabel.nii'
        atlas=nibabel.load(img_contour).get_fdata()[0]

        for e2,ses in enumerate(sessions[e]):
            cor2021cerebnet[s][ses]=dict()
            #read bold time series
            fileloc=pathfiles+'/DataProcessing/MemoryAthlete/'+s+'/'+ses+'/Functionals/cifti_timeseries_normalwall_atlas_freesurf/'+ses+'_b'+bold[e][e2]+'_MNI152_T1_2mm_Swgt_norm_bpss_resid_LR_surf_subcort_32k_fsLR_brainstem_smooth255_scrubbed_neighborclean.dtseries.nii'
            
            



            
            #read SNR mask
            raw=nibabel.load(pathfiles+'/RestProcessing/MA/'+s+'_SNRavgmap.dtseries.nii')
            snrdata=raw.get_fdata()[0]
            
            ##first the distribution per structure
            axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
            # You'll want the brain model axis
            time_axis, brain_model_axis = axes
            #scalarname=[]
            datasave=[]
            
            raw=nibabel.load(fileloc)
            data=raw.get_fdata()


            data=data.T
            ts=[]
            for c2,c in enumerate(netval):
                ts+=[np.mean(data[np.where(snrdata>=20)[0]][np.where(atlas[np.where(snrdata>=20)[0]]==c)[0]],0)]
            
            for val2,val in enumerate(netval):
                for c2,c in enumerate(netval):
                
                    cor2021cerebnet[s][ses][val]=[[np.corrcoef([ts[c2],ts[val2]])[0][1]] for c2 in range(len(ts))]#[np.corrcoef([tsprov,ts[c2]])[0][1] for c2 in range(len(ts))]

                
            
            
    
    
    np.save(pathfiles+'/RestProcessing/MA/snrselec_NeighborCleaned_smooth255/cor2021netXnet.npy', cor2021cerebnet, allow_pickle=True)
    #####2015 mamory champion data, same
    s='MA01'
    cor2015cerebnet=dict()
    cor2015cerebnet[s]=dict()
    
    img_contour=pathfiles+'/RestProcessing/MAold/MSHBM/ind_parcellation/sub1/MS-HBM_FunctionalNetworks_VertexWiseThresh0.01_w20_c20-18net.dlabel.nii'
    atlas=nibabel.load(img_contour).get_fdata()[0]



    basedir2=pathfiles+'/MemAthlete/MA01/Functionals/'
    M = np.array([i.split('\t') for i in open(basedir2+'COHORTSELECT/NEW_TMASKLIST.txt','r').read().split('\n') if i!=''])
    sessionsOLDMA =  M.T[0]

    for sess2,vc in enumerate(sessionsOLDMA):
        cor2015cerebnet[s][vc]=dict()
        fileloc=pathfiles+'/RestProcessing/MAold/MA01/'+vc+'/RSFC_LR_surf_subcort_333_32k_fsLR_smooth2.55.dtseries.nii'
        raw=nibabel.load(fileloc)
        data=raw.get_fdata()
        snrdata2=nibabel.load(pathfiles+'/MSC/SNR/MSCmean_badverts_cort.dtseries.nii').get_fdata()[0]
        snrdata=np.zeros(len(data[0]))
        snrdata[:len(snrdata2)]=snrdata2
        
        ##first the distribution per structure
        axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
        # You'll want the brain model axis
        time_axis, brain_model_axis = axes
        #scalarname=[]
        datasave=[]
        
        raw=nibabel.load(fileloc)
        data=raw.get_fdata()


        data=data.T
        ts=[]
        for c2,c in enumerate(netval):
            ts+=[np.mean(data[np.where(snrdata!=1)[0]][np.where(atlas[np.where(snrdata!=1)[0]]==c)[0]],0)]
        
        for val2,val in enumerate(netval):
            for c2,c in enumerate(netval):
            
                cor2015cerebnet[s][vc][val]=[[np.corrcoef([ts[c2],ts[val2]])[0][1]] for c2 in range(len(ts))]#[np.corrcoef([tsprov,ts[c2]])[0][1] for c2 in range(len(ts))]

                
            
            
    ##and the MSC
    subjects=['MSC'+"{0:02}".format(i) for i in range(1,11)]
    for e,s in enumerate(subjects):
        cor2015cerebnet[s]=dict()




        tag3='dscalar'
        
        img_contour=pathfiles+'/RestProcessing/MSC/MSHBM/ind_parcellation/sub'+str(e+1)+'/MS-HBM_FunctionalNetworks_VertexWiseThresh0.01_w20_c20-18net.dlabel.nii'
        atlas=nibabel.load(img_contour).get_fdata()[0]






        
        #read the tmasks
        tmask=[i.split('\t') for i in open(pathfiles+'/MSC/subjects/'+s+'_TMASKLIST.txt','r').read().split('\n') if i!='']
        
        for vc2,vcall in enumerate(tmask):

            [vc,tmaskvc]=vcall
            
            fileloc=pathfiles+'/RestProcessing/MSC/'+s+'/'+vc+'/RSFC_LR_surf_subcort_333_32k_fsLR_smooth2.55.dtseries.nii'
            cor2015cerebnet[s][vc]=dict()



            
            raw=nibabel.load(fileloc)
            data=raw.get_fdata()
            snrdata2=nibabel.load(pathfiles+'/MSC/SNR/MSCmean_badverts_cort.dtseries.nii').get_fdata()[0]
            snrdata=np.zeros(len(data[0]))
            snrdata[:len(snrdata2)]=snrdata2
            
            ##first the distribution per structure
            axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
            # You'll want the brain model axis
            time_axis, brain_model_axis = axes
            #scalarname=[]
            datasave=[]
            
            raw=nibabel.load(fileloc)
            data=raw.get_fdata()


            data=data.T
            
            ts=[]
            for c2,c in enumerate(netval):
                ts+=[np.mean(data[np.where(snrdata!=1)[0]][np.where(atlas[np.where(snrdata!=1)[0]]==c)[0]],0)]
            
            for val2,val in enumerate(netval):
                for c2,c in enumerate(netval):
                
                    cor2015cerebnet[s][vc][val]=[[np.corrcoef([ts[c2],ts[val2]])[0][1]] for c2 in range(len(ts))]#[np.corrcoef([tsprov,ts[c2]])[0][1] for c2 in range(len(ts))]

                
            
            
    
    
    np.save(pathfiles+'/RestProcessing/MA/snrselec_NeighborCleaned_smooth255/cor2015netXnet.npy', cor2015cerebnet, allow_pickle=True)
    