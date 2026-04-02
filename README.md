# Brain organization of a memory champion

## Scripts instruction
analysis scripts related to the manuscript "Brain organization of a memory champion"

This repository contains scripts that illustrate the set of analyses from the manuscript:

- FCavg_perrun_netXnet: Script to calculate the network to network FC per resting state run.

- HCP_norm_avg_WTA: Example script of winner-take-all for the subcortex and network territories calculation.

- HCP_seedcorrelation: Script to calculate all seed network correlations across all datasets.

- HCP_seedcorrelation_norm: This script takes all concatenated FC network seed maps (full set), performs mixture modeling for each participant, with mixture modeling done at the brain structure level.

- Alb_MM_functions: Functions to perform mixture modeling.

- prepMoranHCP: Script to create the base randomized weight set files that are used to create a random representation of a given map and get the null matching 1000-set of maps.

- TaskPI_moran_testing_unique: Example script testing average values from a set of regions (here high centrality regions but could be a network template) in the original map versus Moran randomized 1000-map set.


The ipython notebooks files provide the code for replication of the main figures. For file size reason and enabling a direct webbrowser opening, this notebook is cut into different section, so that you can open and visualise the code associated to the creation of each of the figures 
Particularly:
     
- part 1 : pi retrieval contrasts and quantification per network and high centrality regions
     
- part 2 : deck of cards task, card imagery contrasts and encode & recall contrasts + reading span task encode & recall contrasts 
     
- part 3 : reading span continue + localizer contrasts / retrosplenial segmentation / SNR mask definition / resting state FC winner take all for controls / subcortical network territories and overlap
     
- part 4 : FC testing at the resting state run level between PFM participants / seed and module FC maps / high centrality segmentation map and network labeling / subcortical FC network strength compared to controls / High centrality analyses for controls 
     
- part 5 : seed FC memory champion and controls 
     
- part 6 : more seed FC memory champion and controls / memory champion US record / high centrality regions FC maps similarity / Neurosynth analysis / subcortical volume


## Task fMRI
Please find script and instruction for the fMRI task in the fMRI_task folder
JS psych task can be viewed and tested from web links available in the instruction file

## dependencies
Scripts were run using python 3.9 via anaconda install
python packages used are : 
### Name                    Version    
fontconfig                2.14.1     
fonttools                 4.43.0     
ipython                   8.12.0             
jupyter                   1.0.0              
mat73                     0.62       
matplotlib                3.7.3      
neurodesign               0.2.2      
nibabel                   4.0.2      
nilearn                   0.10.2     
numpy                     1.24.4     
pandas                    2.0.3      
param                     1.11.1     
scikit-learn              1.3.1      
scipy                     1.10.1     
seaborn                   0.12.2             
matplotlib                3.7.3 


Javascript task fMRI are standalone and do not require specific software installation from a "normal" desktop computer with an existing webbrowser 


