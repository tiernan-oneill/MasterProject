#ifndef Run_h
#define Run_h 1

#include "G4Run.hh"
#include "G4VProcess.hh"
#include "globals.hh"
#include <map>

#include "PrimaryGeneratorAction.hh"
#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"
#include "G4PhysicalConstants.hh"

class G4ParticleDefinition;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

class Run : public G4Run
{
  public:
    Run();
   ~Run();

  public:
    void ParticleCount(G4String, G4double, G4double);
    void Balance(G4double,G4double);
    void EventTiming(G4double);
    void PrimaryTiming(G4double);
    void EvisEvent(G4double);

    void SetTimeWindow(G4double , G4double);
    void CountInTimeWindow(G4String, G4bool,G4bool,G4bool);
        
    void SetPrimary(G4ParticleDefinition* particle, G4double energy);
    void EndOfRun(); 

    virtual void Merge(const G4Run*);

  private:    
    struct ParticleData {
     ParticleData()
       : fCount(0), fEmean(0.), fEmin(0.), fEmax(0.), fTmean(-1.) {}
     ParticleData(G4int count, G4double ekin, G4double emin, G4double emax,
                  G4double meanLife)
       : fCount(count), fEmean(ekin), fEmin(emin), fEmax(emax),
         fTmean(meanLife) {}
     G4int     fCount;
     G4double  fEmean;
     G4double  fEmin;
     G4double  fEmax;
     G4double  fTmean;
    };
     
  private: 
    G4ParticleDefinition*  fParticle;
    G4double  fEkin;
             
    std::map<G4String,ParticleData>  fParticleDataMap;    
    G4int    fDecayCount, fTimeCount;
    G4double fEkinTot[3];
    G4double fPbalance[3];
    G4double fEventTime[3];
    G4double fPrimaryTime;
    G4double fEvisEvent[3];

private:    
  struct ActivityData {
   ActivityData()
     : fNlife_t1(0), fNlife_t2(0), fNdecay_t1t2(0) {}
   ActivityData(G4int n1, G4int n2, G4int nd)
     : fNlife_t1(n1), fNlife_t2(n2), fNdecay_t1t2(nd) {}
   G4int  fNlife_t1;
   G4int  fNlife_t2;
   G4int  fNdecay_t1t2;
  };
  
  std::map<G4String,ActivityData>  fActivityMap;
  G4double fTimeWindow1, fTimeWindow2;
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif

