#ifndef PMT_HH
#define PMT_HH

#include "G4VSensitiveDetector.hh"

#include "G4RunManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4Step.hh"
#include "G4Track.hh"
#include "G4VPhysicalVolume.hh"
#include "G4HCofThisEvent.hh"
#include "G4TouchableHistory.hh"
#include "G4ParticleDefinition.hh"
#include "G4ParticleTypes.hh"

#include "g4root.hh"
#include "globals.hh"

class MySensitiveDetector : public G4VSensitiveDetector
{
  public:
    MySensitiveDetector(const G4String&);
    ~MySensitiveDetector();

    virtual void Initialize(G4HCofThisEvent*);
    virtual G4bool ProcessHits(G4Step*, G4TouchableHistory*);
    virtual void EndOfEvent(G4HCofThisEvent*);

  private:
    G4int fHitCountPerEvent;
};

#endif