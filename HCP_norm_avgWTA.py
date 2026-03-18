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
#so for the whole subcortical, I have the network maps normalized
#so I can do the average across the population
#then do a winner takes all

##############exemple script of winner take all script for the subcortex and network territories calculation
import sklearn
import sklearn.covariance

pathfiles=''

#redo WTA my way 
def WTAsubcortex(avgFCseriesNorm,netindex,netval):
    #1) vox x net correlation (as mean TS) = Cvec
    
    
    raw=nibabel.load(avgFCseriesNorm)
    
    data=raw.get_fdata()
    axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
    # You'll want the brain model axis
    time_axis, brain_model_axis = axes
    
    voxnotcor=np.where((brain_model_axis.name != 'CIFTI_STRUCTURE_CORTEX_RIGHT')&(brain_model_axis.name != 'CIFTI_STRUCTURE_CORTEX_LEFT'))[0]
    corrstruct=data[netindex].T[voxnotcor]
    corrstruct[np.isnan(corrstruct)]=0
    
    
    corrstructcorrected=copy.deepcopy(corrstruct)
    corrstructcorrected[np.where(corrstructcorrected<=0)]=0
    #3) DST https://c4i.gmu.edu/~pcosta/F15/data/fileserver/file/472284/filename/Paper_1570113983.pdf to define P focal point 
    # to see how many competitor (if 1 or more than 1) 
    #Pdst=np.zeros(len(voxID),len(netval))
    corrstructcorrectedclean=copy.deepcopy(corrstructcorrected)
    
    for e in range(len(voxnotcor)):
        #do the delta v x V
        deltaW=np.array([(corrstructcorrected[e][e2]-corrstructcorrected[e])*corrstructcorrected[e][e2] for e2 in range(len(netval))])
        colW=np.sum(deltaW,1)#column sum
        colW[np.where(colW<0)]=0 #remove neg =h
        corrstructcorrectedclean[e][np.where(colW==0)[0]]=0
    
    #4) produce a map for each network of direct strength on voxel where they are competitor
    #5) do a wta map from direct and alone competitor + filler unsure how to represent for not alone competitor
    
    strongestID=[np.argsort(corrstructcorrected[e])[::-1][0] for e in range(len(voxnotcor))]#descending
    
    netwta=netval[strongestID]
    netwta[np.where(np.array([corrstructcorrectedclean[e][strongestID[e]] for e in range(len(voxnotcor))])<=0)]=0
    
    netwta2=np.zeros(len(data[0]))
    netwta2[voxnotcor]=netwta
    corrstruct2=np.zeros((len(data[0]),len(netval)))
    corrstruct2[voxnotcor]=corrstruct
    corrstructcorrectedclean2=np.zeros((len(data[0]),len(netval)))
    corrstructcorrectedclean2[voxnotcor]=corrstructcorrectedclean
    return netwta2,corrstruct2,corrstructcorrectedclean2

if __name__ == "__main__":

    #read list of subject
    savedir = ""
    
    
    listsub=[i for i in open(pathfiles+'/data_HCP/Subject_IDs.txt','r').read().split('\n') if i!='']
    #read the HCP subject FC norm file and average
    avgFCseriesNorm=[]
    for e, s in enumerate(listsub):
        #
        if os.path.exists(pathfiles+'/RestProcessing/HCP/'+s+'_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM.dscalar.nii'):
            
            raw=nibabel.load(pathfiles+'/RestProcessing/HCP/'+s+'_basetemplate_18MSHBMnet_MAsnrmask_netstrength_normperstructureMM.dscalar.nii')
            avgFCseriesNorm+=[raw.get_fdata()]
    
##create the average FC network maps to perform a mean winner take all
avgFCseriesNorm=np.mean(avgFCseriesNorm,0)
#average
netval=np.array([0,1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
mapname=['???','DMN','Parieto-Occipital','VisLat','VisDor-ventralstream','VisV5','VisV1','FPN','DorsAtt','Premotor','Language','Salience','CON','MedialParietal','MotorHand','MotorMouth','MotorFoot','Auditory','SCAN']

netval=(netval[1:])
netindex=range(len(netval))

avgFCseriesNormpath=pathfiles+'/RestProcessing/HCP/HCPavg_basetemplate_18MSHBMnet_MAsnrmaskNHCPsubcortmask_netstrength_normperstructureMM.dscalar.nii'
img=ci.Cifti2Image(np.array(avgFCseriesNorm), header=raw.header)
ci.save(img,avgFCseriesNormpath)

##core of the script
netwta2,corrstruct2,corrstructcorrectedclean2=WTAsubcortex(avgFCseriesNormpath,netindex,netval)

##then saving
s='MSC01'#get the structure to save the output
raw=nibabel.load(pathfiles+'/RestProcessing/HCP/'+s+'_zscoresHCP_basetemplate_18MSHBMnet_MAsnrmaskNHCPsubcortmask_netstrength_normperstructureMM_HCPsubcortmask.dtseries.nii')
axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
# You'll want the brain model axis
corrstruct2path=pathfiles+'/RestProcessing/HCP/HCPavg_netstrength_basetemplate_18MSHBMnet_MAsnrmaskNHCPsubcortmask_netstrength_normperstructureMM.dtseries.nii'
time_axis, brain_model_axis = axes
time_axis2=nibabel.cifti2.cifti2_axes.SeriesAxis(1,1,len(corrstruct2.T))
img=ci.Cifti2Image(np.array(corrstruct2.T), header=(time_axis2, brain_model_axis),
            nifti_header=raw.nifti_header)
ci.save(img,corrstruct2path)
corrstruct2path=pathfiles+'/RestProcessing/HCP/HCPavg_netcompetitor_basetemplate_18MSHBMnet_MAsnrmaskNHCPsubcortmask_netstrength_normperstructureMM.dtseries.nii'
time_axis, brain_model_axis = axes
time_axis2=nibabel.cifti2.cifti2_axes.SeriesAxis(1,1,len(corrstructcorrectedclean2.T))
img=ci.Cifti2Image(np.array(corrstructcorrectedclean2.T), header=(time_axis2, brain_model_axis),
            nifti_header=raw.nifti_header)
ci.save(img,corrstruct2path)


raw2=nibabel.load(pathfiles+'/RestProcessing/MSC/MSHBM/ind_parcellation/sub1/MS-HBM_FunctionalNetworks_VertexWiseThresh0.01_w20_c20-18net.dlabel.nii')
    
axes = [raw2.header.get_axis(i) for i in range(raw2.ndim)]
# You'll want the brain model axis
label_axis, brain_model_axis2 = axes
label_axis2=nibabel.cifti2.cifti2_axes.LabelAxis([label_axis.name[0]],[label_axis.label[0]])
img=ci.Cifti2Image(np.array([netwta2]), header=(label_axis2, brain_model_axis),
                nifti_header=raw.nifti_header)
ci.save(img,pathfiles+'/RestProcessing/HCP/HCPavg_winnerlabel_basetemplate_18MSHBMnet_MAsnrmaskNHCPsubcortmask_netstrength_normperstructureMM.dlabel.nii')





