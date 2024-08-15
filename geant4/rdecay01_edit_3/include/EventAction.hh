#ifndef EventAction_h
#define EventAction_h 1

#include "G4UserEventAction.hh"
#include "globals.hh"
#include "RunAction.hh"
#include <vector>

#include "Run.hh"

#include "G4Event.hh"
#include "G4RunManager.hh"

#include "G4TrajectoryContainer.hh"
#include "G4Trajectory.hh"

#include <iomanip>

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

class G4Event;

class EventAction : public G4UserEventAction
{
  public:
    EventAction();
   ~EventAction();

  public:
    virtual void BeginOfEventAction(const G4Event*);
    virtual void   EndOfEventAction(const G4Event*);
    
    void AddDecayChain(G4String val) {fDecayChain += val;};
    void AddEvisible(G4double val)   {fEvisTot    += val;};
    
  private:
    G4String        fDecayChain;                   
    G4double        fEvisTot;
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif

    
