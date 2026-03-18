# memory_champion
analysis scripts related to the manuscript "Brain organization of a memory champion"

This repository contains scripts that illustrate the set of analyses from the manuscript:

FCavg_perrun_netXnet: Script to calculate the network mean FC per resting state run.
HCP_norm_avg_WTA: Example script of winner-take-all for the subcortex and network territories calculation.
HCP_seedcorrelation: Script to calculate all seed network correlations across all datasets.
HCP_seedcorrelation_norm: This script takes all concatenated FC network seed maps (full set), performs mixture modeling for each participant, with mixture modeling done at the brain structure level.
Alb_MM_functions: Functions to perform mixture modeling.
prepMoranHCP: Script to create the base randomized weight set files to then feed a given map and get the null matching set of maps.
TaskPI_moran_testing_unique: Example script testing average values from a set of region/network templates in the original map versus Moran randomized 1000-map set.


the ipython notebooks files provide the code for replication of the main figures.
