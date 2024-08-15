#include "PhysicsList.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

PhysicsList::PhysicsList()
: G4VModularPhysicsList()
{   
    G4int verbosity = 0;
    RegisterPhysics(new G4RadioactiveDecayPhysics(verbosity));
    RegisterPhysics(new G4DecayPhysics(verbosity));
    RegisterPhysics(new G4EmLivermorePhysics(verbosity));
    RegisterPhysics(new G4OpticalPhysics(verbosity));

    /*
    // Hadronic processes
    RegisterPhysics(new G4HadronPhysicsQGSP_BIC_HP(2));
    RegisterPhysics(new G4HadronElasticPhysicsHP(verbosity));
    RegisterPhysics(new G4StoppingPhysics(verbosity));
    RegisterPhysics(new G4IonPhysics(verbosity));
    RegisterPhysics(new G4EmExtraPhysics(verbosity));
    */

    //add new units for radioActive decays
    // 
    const G4double minute = 60*second;
    const G4double hour   = 60*minute;
    const G4double day    = 24*hour;
    const G4double year   = 365*day;
    new G4UnitDefinition("minute", "min", "Time", minute);
    new G4UnitDefinition("hour",   "h",   "Time", hour);
    new G4UnitDefinition("day",    "d",   "Time", day);
    new G4UnitDefinition("year",   "y",   "Time", year);

    // mandatory for G4NuclideTable
    // Half-life threshold must be set small or many short-lived isomers 
    // will not be assigned life times (default to 0) 
    G4NuclideTable::GetInstance()->SetThresholdOfHalfLife(0.1*picosecond);
    G4NuclideTable::GetInstance()->SetLevelTolerance(1.0*eV);

    //read new PhotonEvaporation data set 
    //
    G4DeexPrecoParameters* deex = 
        G4NuclearLevelData::GetInstance()->GetParameters();
    deex->SetCorrelatedGamma(false);
    deex->SetStoreAllLevels(true);
    deex->SetIsomerProduction(true);  
    deex->SetMaxLifeTime(G4NuclideTable::GetInstance()->GetThresholdOfHalfLife()
                    /std::log(2.));
}

PhysicsList::~PhysicsList()
{}

void PhysicsList::SetCuts()
{
  SetCutsWithDefault();
  
  // Set cut for proton
  //SetCutValue(0.0001*mm, "proton");
}