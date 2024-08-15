#ifndef RunAction_h
#define RunAction_h 1

#include "G4UserRunAction.hh"

#include "g4root.hh"

#include "Run.hh"
#include "PrimaryGeneratorAction.hh"
#include "TotalHitCounter.hh"

#include "G4Run.hh"
#include "G4RunManager.hh"
#include "G4UnitsTable.hh"
#include "G4PhysicalConstants.hh"
#include "G4SystemOfUnits.hh"
#include <iomanip>

class Run;
class PrimaryGeneratorAction;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

class RunAction : public G4UserRunAction
{
  public:
    RunAction(PrimaryGeneratorAction*);
   ~RunAction();

    virtual G4Run* GenerateRun();   
    virtual void BeginOfRunAction(const G4Run*);
    virtual void   EndOfRunAction(const G4Run*);
    
  private:
    PrimaryGeneratorAction* fPrimary;
    Run*                    fRun;  

    // analysis manager and root file stuff
    void Book();
    G4String fFileName;
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif

