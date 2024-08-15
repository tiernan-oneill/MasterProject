# rdecay01_edit_1 README page
 	
### IMPORTANT

  You must create an output_files folder into your build folder,
  this is where all of the macros will create and/or save the output ROOT files.

### My Edits to this example

 Not many edits have been made in this example, the main differences are
 in the RunAction.cc and TrackingAction.cc files. Also I created a lot of macros
 for the execution of each isotope simulation.

### Geometry construction

 It is a simple box which represente an 'infinite' homogeneous medium.
  
### Physics list

 PhysicsList.cc defines only G4RadioactiveDecay, G4Transportation processes,
 and relevant particle definitions. It does this with 'G4Radioactivation'.
         	
### Primary generator
 
 Default kinematic is an ion (Ne24), at rest, at coordinate origin.
 Can be changed with particleGun commands that we make use of in
 the macros.
         	
### Physics

 Single decay chain: only the beta decays.
 EM and atomic de-excitation processes turned off.
  	
### Histograms
 
  This example produces several 1D histograms in the ROOT files.
  These are:
    - 1 : energy spectrum: e+ e-
    - 2 : energy spectrum: nu_e anti_nu_ev
    - 3 : energy spectrum: gamma
    - 4 : energy spectrum: alpha
    - 5 : energy spectrum: ions
    - 6 : total kinetic energy (Q)
    - 7 : momentum balance
    - 8 : total time of life of decay chain
    - 9 : total visible energy

  We ignore these and remove the code that fills them.
  The information that we want is stored separately in the ROOT files.
