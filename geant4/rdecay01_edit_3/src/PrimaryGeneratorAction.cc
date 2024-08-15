#include "PrimaryGeneratorAction.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

PrimaryGeneratorAction::PrimaryGeneratorAction()
 : G4VUserPrimaryGeneratorAction(),
   fParticleGun(0)
{
  G4int n_particle = 1;
  fParticleGun  = new G4ParticleGun(n_particle);

  fParticleGun->SetParticleEnergy(0*eV);
  fParticleGun->SetParticlePosition(G4ThreeVector(0.,0.,0.));         
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

PrimaryGeneratorAction::~PrimaryGeneratorAction()
{
  delete fParticleGun;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
{
  if (fParticleGun->GetParticleDefinition() == G4Geantino::Geantino()) {  
    G4int Z = 10, A = 24;
    G4double ionCharge   = 0.*eplus;
    G4double excitEnergy = 0.*keV;
    
    G4ParticleDefinition* ion
       = G4IonTable::GetIonTable()->GetIon(Z,A,excitEnergy);
    fParticleGun->SetParticleDefinition(ion);
    fParticleGun->SetParticleCharge(ionCharge);
  }

    G4double energy = fParticleGun->GetParticleEnergy();
    if (energy == 0) {
      // no energy means no momentum
       fParticleGun->SetParticleMomentumDirection(G4ThreeVector(0.,0.,0.));
    }
    else{
    // Generate isotropic direction of particle
    costheta = 2 * G4UniformRand() - 1.0;
    sintheta = sqrt(1.0 - costheta * costheta);
    phi = 2 * CLHEP::pi * G4UniformRand();
    px = sintheta * cos(phi);
    py = sintheta * sin(phi);
    pz = costheta;
    fParticleGun->SetParticleMomentumDirection(G4ThreeVector(px, py, pz));
    }    

    //create vertex
    //   
    fParticleGun->GeneratePrimaryVertex(anEvent);
}
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
