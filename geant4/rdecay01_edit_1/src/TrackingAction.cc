#include "TrackingAction.hh"

#include "HistoManager.hh"
#include "Run.hh"
#include "EventAction.hh"
#include "TrackingMessenger.hh"

#include "G4Track.hh"
#include "G4ParticleTypes.hh"
#include "G4IonTable.hh"
#include "G4RunManager.hh"

#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

TrackingAction::TrackingAction(EventAction* EA)
:G4UserTrackingAction(),
 fEvent(EA),fTrackMessenger(0),
 fFullChain(true)
 
{
  fTrackMessenger = new TrackingMessenger(this);   
  
  fTimeWindow1 = fTimeWindow2 = 0.;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

TrackingAction::~TrackingAction()
{
  delete fTrackMessenger;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void TrackingAction::SetTimeWindow(G4double t1, G4double dt)
{
  fTimeWindow1 = t1;
  fTimeWindow2 = fTimeWindow1 + dt;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void TrackingAction::PreUserTrackingAction(const G4Track* track)
{
  Run* run 
   = static_cast<Run*>(G4RunManager::GetRunManager()->GetNonConstCurrentRun());
         
  G4ParticleDefinition* particle = track->GetDefinition();
  G4String name   = particle->GetParticleName();
  fCharge = particle->GetPDGCharge();
  fMass   = particle->GetPDGMass();  
    
  G4double Ekin = track->GetKineticEnergy();
  G4int ID      = track->GetTrackID();
  
  G4bool condition = false;
  
  // check LifeTime
  //
  G4double meanLife = particle->GetPDGLifeTime();
  
  //count particles
  //
  run->ParticleCount(name, Ekin, meanLife);
  
  // store the kinetic energies of electrons/positrons and neutrinos/antineutrinos once they are created
  //
  G4int ih = 0;
  if (particle == G4Electron::Electron()||
      particle == G4Positron::Positron()){  
      G4AnalysisManager::Instance()->FillNtupleDColumn(0, 0, 1000*Ekin);
      G4AnalysisManager::Instance()->AddNtupleRow(0); }
  
  else if (particle == G4NeutrinoE::NeutrinoE()||
           particle == G4AntiNeutrinoE::AntiNeutrinoE()){
      G4AnalysisManager::Instance()->FillNtupleDColumn(1, 0, 1000*Ekin);
      G4AnalysisManager::Instance()->AddNtupleRow(1); }
  
  //Ion
  //
  if (fCharge > 2.) {
    //build decay chain
    if (ID == 1) fEvent->AddDecayChain(name);
      else       fEvent->AddDecayChain(" ---> " + name);
    // 
    //full chain: put at rest; if not: kill secondary      
    G4Track* tr = (G4Track*) track;
    if (fFullChain) { tr->SetKineticEnergy(0.);
                      tr->SetTrackStatus(fStopButAlive);}
      else if (ID>1) tr->SetTrackStatus(fStopAndKill);
    //
    fTime_birth = track->GetGlobalTime();
  }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void TrackingAction::PostUserTrackingAction(const G4Track* track)
{
  //keep only ions
  //
  if (fCharge < 3. ) return;
  
  Run* run 
   = static_cast<Run*>(G4RunManager::GetRunManager()->GetNonConstCurrentRun());

  G4AnalysisManager* analysis = G4AnalysisManager::Instance();
   
  //get time
  //   
  G4double time = track->GetGlobalTime();
  G4int ID = track->GetTrackID();
  if (ID == 1) run->PrimaryTiming(time);        //time of life of primary ion
  fTime_end = time;
      
  //energy and momentum balance (from secondaries)
  //
  const std::vector<const G4Track*>* secondaries 
                              = track->GetStep()->GetSecondaryInCurrentStep();
  size_t nbtrk = (*secondaries).size();
  if (nbtrk) {
    //there are secondaries --> it is a decay
    //
    //balance    
    G4double EkinTot = 0., EkinVis = 0.;
    G4ThreeVector Pbalance = - track->GetMomentum();
    for (size_t itr=0; itr<nbtrk; itr++) {
       const G4Track* trk = (*secondaries)[itr];
       G4ParticleDefinition* particle = trk->GetDefinition();
       G4double Ekin = trk->GetKineticEnergy();
       EkinTot += Ekin;
       G4bool visible = !((particle == G4NeutrinoE::NeutrinoE())||
                          (particle == G4AntiNeutrinoE::AntiNeutrinoE()));
       if (visible) EkinVis += Ekin; 
       //exclude gamma desexcitation from momentum balance
       if (particle != G4Gamma::Gamma()) Pbalance += trk->GetMomentum();
    }
    G4double Pbal = Pbalance.mag();  
    run->Balance(EkinTot,Pbal);
    fEvent->AddEvisible(EkinVis);
  }
  
  //no secondaries --> end of chain    
  //  
  if (!nbtrk) {
    run->EventTiming(time);                     //total time of life
    G4double weight = track->GetWeight();
    fTime_end = DBL_MAX;
  }
  
  //count activity in time window
  //
  run->SetTimeWindow(fTimeWindow1, fTimeWindow2);
  
  G4String name   = track->GetDefinition()->GetParticleName();
  G4bool life1(false), life2(false), decay(false);
  if ((fTime_birth <= fTimeWindow1)&&(fTime_end > fTimeWindow1)) life1 = true;
  if ((fTime_birth <= fTimeWindow2)&&(fTime_end > fTimeWindow2)) life2 = true;
  if ((fTime_end   >  fTimeWindow1)&&(fTime_end < fTimeWindow2)) decay = true;
  if (life1||life2||decay) run->CountInTimeWindow(name,life1,life2,decay);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

