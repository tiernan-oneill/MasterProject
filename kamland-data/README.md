# Data analysis with the KamLAND-Zen 800 data
 	
### veto python script

 The vetoes_spectrum.py studies the effects of different vetoes on the energy spectrum.
  
### compare_datasets

 Studies the difference in energy spectra before and after the 2023 paper (https://arxiv.org/abs/2203.02139), both in individual bins 
 and in total. Useful for spotting the need for a 'hotspot' veto.
         	
### LL_vetoes
 
 Studying the effects of the current Long-Lived veto on the data. Functions to read the unixtime were created 
 and information on this veto was obtained per month intervals over the duration of the 800 run.
 This information is stored in the data files, and visualised in the images.
         	
### data files

 This folder also contains two ROOT files; the data used in the 2023 article and all of the ROOT data from the 800 run.
 Used in the compare_datasets subfolder. Not included publicly. 
