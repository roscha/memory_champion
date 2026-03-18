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
import pickle

pathfiles=''
#################### exemple script testing average values from a set of regions/network template in original map versus moran randomized 1000-map set

subname=['CIFTI_STRUCTURE_ACCUMBENS', 'CIFTI_STRUCTURE_AMYGDALA', 'CIFTI_STRUCTURE_CAUDATE', 'CIFTI_STRUCTURE_CEREBELLUM', 'CIFTI_STRUCTURE_HIPPOCAMPUS', 'CIFTI_STRUCTURE_PALLIDUM', 'CIFTI_STRUCTURE_PUTAMEN', 'CIFTI_STRUCTURE_THALAMUS']
netval=np.array([0,1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
mapname=['???','DMN','Parieto-Occipital','VisLat','VisDor-ventralstream','VisV5','VisV1','FPN','DorsAtt','Premotor','Language','Salience','CON','MedialParietal','MotorHand','MotorMouth','MotorFoot','Auditory','SCAN']
s='MA01'


#now the nice picture
#here2401
netval=np.array([0,1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
mapname=['???','DMN','Parieto-Occipital','VisLat','VisDor-ventralstream','VisV5','VisV1','FPN','DorsAtt','Premotor','Language','Salience','CON','MedialParietal','MotorHand','MotorMouth','MotorFoot','Auditory','SCAN']

subjects=['MA01']
e=0
s=subjects[e]
    

boot=1000    
    #get the map

######################################################################
e=0
s='MA01'




pathmoran=pathfiles+'/Tools/Moran/MA01/Moran_distance_moran1000rand'
msrL=pickle.load(open(pathmoran+'_L.npy', 'rb'))
msrR=pickle.load(open(pathmoran+'_R.npy', 'rb'))
msrV=pickle.load(open(pathmoran+'_vol.npy', 'rb'))
print('loaded')


contval2=netval[1:]#[4,15,1,9,13]
contval2ref=np.arange(18)#[1,15-3,0,9-3,13-3]
#cardview>fake
raw=nibabel.load(pathfiles+'/TaskProcessing/16FDfilter/concatenate/MA01/MA01_MACtasks_all_ZstatsMotorContrasts_smooth6.0.dscalar.nii')
data=raw.get_fdata()
ad=''
speRS=nibabel.load(pathfiles+'/TaskProcessing/16FDfilter'+ad+'/readingspan-ME/'+s+'/second_level_cifti_all_readingspan_210525/cifti_cope43/zstat1_smooth6.0.dtseries.nii').get_fdata()[0]

axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
time_axis, brain_model_axis = axes
time_axis2=nibabel.cifti2.cifti2_axes.SeriesAxis(1,1,1)

#cardview>fake
masklist=[126,128]
contrastsign=[-1,1]
contrastlist=[-1,1]#it's a special contrast not concatenated no this is random
namelist=['_rs_encodeOVERStore','_rs_storeOVERencode']

moranmatuniqueNET2021=np.zeros((boot,len(contrastlist),16))

matuniqueNET2021=np.zeros((len(contrastlist),16))


for l in range(len(masklist)):
    dataprov=contrastsign[l]*copy.deepcopy(speRS)
    #hit positive
    mask=data[masklist[l]]
    dataprov[np.where(mask<=0)]=0
    dataprov[np.where(dataprov<0)]=0
    structure='CIFTI_STRUCTURE_DIENCEPHALON_VENTRAL'
    locvox=np.where((brain_model_axis.name=='CIFTI_STRUCTURE_BRAIN_STEM')|(brain_model_axis.name==structure+'_RIGHT')|(brain_model_axis.name==structure+'_LEFT'))[0]
    dataprov[locvox]=0
    mask=pathfiles+'/RestProcessing/MA/'+s+'_SNRavgmap_mask.dtseries.nii'
    maskdata=nibabel.load(mask).get_fdata()[0]
    dataprov[np.where(maskdata[:29696+29716]==1)[0]]=np.nan


    template=nibabel.load(pathfiles+'/RestProcessing/HCP/commonMA0120212015_percentbeyondHCP_overlapALL_split4d_MA01subcortmask.dtseries.nii').get_fdata()
    
    for c2,c in enumerate(range(len(template))):
        matuniqueNET2021[l][c2]=np.nanmean(dataprov[np.where(template[c]==1)[0]])
    




    dataX=copy.deepcopy(dataprov)
    dataX[np.where(np.isnan(dataX))]=0## left right hemisphere and volume are done independantly as it's based on distance weight
    Lmoran=msrL.randomize(np.array(dataX)[:29696])
    Rmoran=msrR.randomize(np.array(dataX)[29696:29696+29716])
    Vmoran=msrV.randomize(np.array(dataX)[29696+29716:])
    #normalization
    valprov=[np.nanmean(np.array(dataX)[:29696][np.where(np.array(dataX)[:29696]>0)]),np.nanstd(np.array(dataX)[:29696][np.where(np.array(dataX)[:29696]>0)])]
    N=len(np.where(np.array(dataX)[:29696]>0)[0])
    for l2 in range(boot):
        prov2=Lmoran[l2]
        prov=np.argsort(prov2)[::-1]
        prov2[prov[N:]]=0
        prov2[prov[:N]]=(prov2[prov[:N]]-np.nanmean(prov2[prov[:N]]))/np.nanstd(prov2[prov[:N]])*valprov[1]+valprov[0]
        Lmoran[l2]=prov2

    valprov=[np.nanmean(np.array(dataX)[29696:29696+29716][np.where(np.array(dataX)[29696:29696+29716]>0)]),np.nanstd(np.array(dataX)[29696:29696+29716][np.where(np.array(dataX)[29696:29696+29716]>0)])]
    N=len(np.where(np.array(dataX)[29696:29696+29716]>0)[0])
    for l2 in range(boot):
        prov2=Rmoran[l2]
        prov=np.argsort(prov2)[::-1]
        prov2[prov[N:]]=0
        prov2[prov[:N]]=(prov2[prov[:N]]-np.nanmean(prov2[prov[:N]]))/np.nanstd(prov2[prov[:N]])*valprov[1]+valprov[0]
        Rmoran[l2]=prov2

    valprov=[np.nanmean(np.array(dataX)[29696+29716:][np.where(np.array(dataX)[29696+29716:]>0)]),np.nanstd(np.array(dataX)[29696+29716:][np.where(np.array(dataX)[29696+29716:]>0)])]
    N=len(np.where(np.array(dataX)[29696+29716:]>0)[0])
    for l2 in range(boot):
        prov2=Vmoran[l2]
        prov=np.argsort(prov2)[::-1]
        prov2[prov[N:]]=0
        prov2[prov[:N]]=(prov2[prov[:N]]-np.nanmean(prov2[prov[:N]]))/np.nanstd(prov2[prov[:N]])*valprov[1]+valprov[0]
        Vmoran[l2]=prov2

    axes = [raw.header.get_axis(i) for i in range(raw.ndim)]
    time_axis, brain_model_axis = axes
    time_axis2=nibabel.cifti2.cifti2_axes.SeriesAxis(1,1,1)
    
    contval2=netval[1:]#[4,15,1,9,13]
    contval2ref=np.arange(18)#[1,15-3,0,9-3,13-3]
    #hit>miss
    
    structure='CIFTI_STRUCTURE_DIENCEPHALON_VENTRAL'
    locvox=np.where((brain_model_axis.name=='CIFTI_STRUCTURE_BRAIN_STEM')|(brain_model_axis.name==structure+'_RIGHT')|(brain_model_axis.name==structure+'_LEFT'))[0]
    dataX[locvox]=0
    mask=pathfiles+'/RestProcessing/MA/'+s+'_SNRavgmap_mask.dtseries.nii'
    maskdata=nibabel.load(mask).get_fdata()[0]
    dataX[np.where(maskdata[:29696+29716]==1)[0]]=np.nan
    #barplot
    template=nibabel.load(pathfiles+'/RestProcessing/HCP/commonMA0120212015_percentbeyondHCP_overlapALL_split4d_MA01subcortmask.dtseries.nii').get_fdata()
    
    #recombine
    datacombineprov=np.concatenate([Lmoran,Rmoran,Vmoran],1)
    for b in range(boot):
        dataprov=datacombineprov[b]
        
        mask=pathfiles+'/RestProcessing/MA/'+s+'_SNRavgmap_mask.dtseries.nii'
        maskdata=nibabel.load(mask).get_fdata()[0]
        dataprov[np.where(maskdata[:29696+29716]==1)[0]]=np.nan
        #barplot
        
        keepPROV=[]
        for c2,c in enumerate(range(len(template))):
            keepPROV+=[np.nanmean(dataprov[np.where(template[c]==1)[0]])]
        moranmatuniqueNET2021[b][l]=keepPROV

        
moranmatuniqueNET2021=moranmatuniqueNET2021.T

pval95matuniqueNET2021=np.zeros((len(template),len(contrastlist)))
for n3,n in enumerate(masklist):
    for n2,n4 in enumerate(range(len(template))):
        pval95matuniqueNET2021[n2][n3]=len(np.where(moranmatuniqueNET2021[n2][n3]>matuniqueNET2021[n3][n2])[0])/1000.
                                    
    


np.save(pathfiles+'/RestProcessing/MA/rspvalunique.npy', pval95matuniqueNET2021, allow_pickle=True)


