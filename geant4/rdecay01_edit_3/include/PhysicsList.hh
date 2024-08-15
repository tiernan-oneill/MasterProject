#ifndef PhysicsList_h
#define PhysicsList_h 1

#include "G4VModularPhysicsList.hh"
#include "globals.hh"

#include "G4UnitsTable.hh"
#include "G4ParticleTypes.hh"
#include "G4PhysicsListHelper.hh"
#include "G4IonConstructor.hh"

#include "G4RadioactiveDecayPhysics.hh"
#include "G4DecayPhysics.hh"

// Hadronic processes (if used)
#include "G4HadronPhysicsQGSP_BIC_HP.hh"
#include "G4HadronElasticPhysicsHP.hh"
#include "G4StoppingPhysics.hh"
#include "G4IonPhysics.hh"

#include "G4SystemOfUnits.hh"
#include "G4NuclideTable.hh"
#include "G4LossTableManager.hh"
#include "G4UAtomicDeexcitation.hh"
#include "G4NuclearLevelData.hh"
#include "G4DeexPrecoParameters.hh"

// Electromagnetic processes
#include "G4EmLivermorePhysics.hh"
#include "G4EmExtraPhysics.hh"

// Optical processes
#include "G4OpticalPhysics.hh"

#include "G4Scintillation.hh"
#include "G4EmSaturation.hh"
#include "G4ProcessManager.hh"

#include "G4ProductionCutsTable.hh"

class G4VPhysicsConstructor;

class PhysicsList: public G4VModularPhysicsList
{
  public:
    PhysicsList();
   ~PhysicsList();

  protected:
    virtual void SetCuts();
};

#endif




