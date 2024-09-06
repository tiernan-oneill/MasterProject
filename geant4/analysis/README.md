# Analysis    

### beta_spectra

 Plots beta spectra of the isotopes along with ENSDF beta_data. Two isotopes have their own
 scripts as they are plotted differently from the rest in the thesis.
  
### real_spectra

 Plots the real (or total) decay spectra of the isotopes. Also combines all of the isotopes into one
 total histogram which is plotted and also saved in a ROOT file. The gamma spectrum of 122I is studied
 separately for use in the thesis.
         	
### hit_counts
 
 Contains the optical photon hit count information from the rdecay01_edit_3 build. Histograms of these hit
 counts are plotted and the mean values are stored. From this the calibration factors are stored for use
 in getting our visible energy spectra.

### visible_spectra

 A python script creates new ROOT files for each isotope and applies a smearing and calibration to the real 
 energy spectra. Plots the smeared + calibrated (or visible) spectra of the isotopes. Also plots just the 
 smeared spectra of the isotopes. Combines all of the isotopes into one total histogram which is plotted and 
 also saved in a ROOT file. This is done for both the smeared and visible cases.

### final_spectra

 Plots the spectra used in the thesis results section. Plots a total visible spectrum with some specific 
 isotopes as an example. A comparison plot is also used for studying the individual visible spectra with 
 that of the KLG4 build. The python script creates the final results in the thesis.
         	
### other

 Included are two data sets, both taken from https://arxiv.org/abs/2301.09307. A data set of isotope yields from FLUKA is used for normalizing our isotope 
 energy spectra. A data file contains rough y-values of the total visible energy spectrum of the KLG4 build, 
 to be used in the final graph.
