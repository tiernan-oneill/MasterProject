# rdecay01_edit_3 README page

### IMPORTANT

  You must create an output_files folder into your build folder,
  this is where all of the macros will create and/or save the output ROOT files.

### My Edits to this example

 In going from the second build to this one, several changes were made:
 - New .cc and .hh files for 'PMT' and 'TotalHitCounter'.
 - Major Detector Construction changes.
 - Store photon hit information in output ROOT files.
 - Isotropic particle directions upon creation at origin.

### Geometry construction

 World volume is a cube of dimensions 16m.
 Concurrent spheres of XeLS and KamLS of radius 1.9 and 6.5m respectively.
 Sensitive detector volume ('PMTs') is a 1m thick shell around these.
 Optical properties and borders defined.
  
### Physics list

 G4RadioactiveDecayPhysics, G4DecayPhysics, G4OpticalPhysics, G4EmLivermorePhysics.
 Changed to a ModularPhysicsList for a more simple implementation.
         	
### Primary generator
 
 We slightly changed the default input information. The generated particle now has an
 random isotropic momentum once created at origin.

### PMTs

 Sensitive detector class used to process hits in the PMTs and keep track of this.
 Can implement quantum efficiency and photocoverage effects here if required.
 This is done on a per-event basis.

### TotalHitCounter
 
 A hit counter to keep track of the hit number in the PMTs over the entire run.
 Only outputs this value in the readout of the simulation (not stored in ROOT file).
 Useful for comparing the hit count with the total number of produced photons over the entire run.

### SteppingAction
 
 Once again not actively used, but you can study, for example, the energy deposit
 of secondaries here for further understanding of what is happening in the simulation.