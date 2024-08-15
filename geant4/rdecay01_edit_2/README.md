# rdecay01_edit_2 README page
 	
### IMPORTANT

  You must create an output_files folder into your build folder,
  this is where all of the macros will create and/or save the output ROOT files.

### My Edits to this example

 In going from the first build to this one, the main differences are:
 - More information stored with the RunAction.cc and TrackingAction.cc files.
 - Physics slightly altered in PhysicsList.cc.
 - New .hh and .cc files 'SteppingAction' (described below).
 - Removed unused histogram information throughout the build.

### Geometry construction

 It is a simple box which represente an 'infinite' homogeneous medium.
  
### Physics list

 Still uses G4Radioactivation. ARMflag is set to True,
 so Atomic de-excitation processes are turned on.
 Full decay chain: simulation only stops once a stable ground state nuclide is reached,
 this is turned on in the macro files.
         	
### Primary generator
 
 Default kinematic is an ion (Ne24), at rest, at coordinate origin.
 Can be changed with particleGun commands that we make use of in
 the macros.

### SteppingAction
 
 Added a SteppingAction to allow step information to be studied.
 Its only function here is to end the simulation after a pre-set in-run time
 has been reached (eg. 1 day). Switched off by a boolean by default.
 This class is used more in the next build.
  	
### Histograms
 
  We remove alot of this information since we don't use it.
  Macro files no longer need to set this information.
  HistoManager .cc and .hh files removed.
  Any necessary ROOT file related stuff is handled in RunAction files.