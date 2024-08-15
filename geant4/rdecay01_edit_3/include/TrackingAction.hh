#ifndef TrackingAction_h
#define TrackingAction_h 1

#include "G4UserTrackingAction.hh"
#include "globals.hh"
#include "g4root.hh"
#include <vector>

#include "Run.hh"
#include "EventAction.hh"
#include "TrackingMessenger.hh"

#include "G4Track.hh"
#include "G4Trajectory.hh"
#include "G4TrackingManager.hh"
#include "G4ParticleTypes.hh"
#include "G4IonTable.hh"
#include "G4RunManager.hh"

#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"

#include "G4Exception.hh"
#include "G4VProcess.hh"
#include "G4ios.hh"

class EventAction;
class TrackingMessenger;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

class TrackingAction : public G4UserTrackingAction {

  public:  
    TrackingAction(EventAction*);
   ~TrackingAction();
   
    virtual void  PreUserTrackingAction(const G4Track*);
    virtual void PostUserTrackingAction(const G4Track*);
    
    void SetFullChain(G4bool flag) { fFullChain = flag;};
    void SetTimeWindow(G4double , G4double);
    
  private:
    EventAction*        fEvent;
    TrackingMessenger*  fTrackMessenger;
    
    G4double fCharge, fMass;        
    G4bool   fFullChain;

    G4double fTime_birth,  fTime_end;
    G4double fTimeWindow1, fTimeWindow2;
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif
