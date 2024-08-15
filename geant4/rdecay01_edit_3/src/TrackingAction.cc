#include "TrackingAction.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

TrackingAction::TrackingAction(EventAction* EA)
: G4UserTrackingAction(), fEvent(EA), fTrackMessenger(0), fFullChain(true)
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
  G4String particleName   = particle->GetParticleName();
  fCharge = particle->GetPDGCharge();
  fMass   = particle->GetPDGMass();  
  G4int trackID = track->GetTrackID();
  G4double Ekin = track->GetKineticEnergy();
  
  // check LifeTime
  //
  G4double meanLife = particle->GetPDGLifeTime();
  
  //count particles
  //
  run->ParticleCount(particleName, Ekin, meanLife);
  
  //Ion
  //
  if (fCharge > 2.) {
    //build decay chain
    if (trackID == 1) fEvent->AddDecayChain(particleName);
      else       fEvent->AddDecayChain(" ---> " + particleName);
    //full chain: put at rest; if not: kill secondary      
    G4Track* tr = (G4Track*) track;
    if (fFullChain) { tr->SetKineticEnergy(0.);
                      tr->SetTrackStatus(fStopButAlive);}
    //
    fTime_birth = track->GetGlobalTime();
  }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void TrackingAction::PostUserTrackingAction(const G4Track* track)
{ 
  // Get track ID
  G4int trackID = track->GetTrackID();

  // Get final position of the particle
  G4ThreeVector position = track->GetStep()->GetPostStepPoint()->GetPosition();
  //G4cout << "Position of end of track " << track->GetTrackID() << " at " << position.mag()/1000 << " m" << G4endl;

  //keep only ions
  //
  if (fCharge < 3. ) return;
  
  Run* run 
   = static_cast<Run*>(G4RunManager::GetRunManager()->GetNonConstCurrentRun());
   
  //get time
  //   
  G4double time = track->GetGlobalTime();
  if (trackID == 1) run->PrimaryTiming(time);        //time of life of primary ion
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
    fTime_end = DBL_MAX;
  }
  
  //count activity in time window
  //
  run->SetTimeWindow(fTimeWindow1, fTimeWindow2);
  
  G4String particleName   = track->GetDefinition()->GetParticleName();
  G4bool life1(false), life2(false), decay(false);
  if ((fTime_birth <= fTimeWindow1)&&(fTime_end > fTimeWindow1)) life1 = true;
  if ((fTime_birth <= fTimeWindow2)&&(fTime_end > fTimeWindow2)) life2 = true;
  if ((fTime_end   >  fTimeWindow1)&&(fTime_end < fTimeWindow2)) decay = true;
  if (life1||life2||decay) run->CountInTimeWindow(particleName,life1,life2,decay);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

