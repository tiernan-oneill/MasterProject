#include "RunAction.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

RunAction::RunAction(PrimaryGeneratorAction* kin)
:G4UserRunAction(),
 fPrimary(kin), fRun(0), fFileName("rdecay01")
{ 
    Book();

    // Only study the hit count number per event
    G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
    analysisManager->CreateNtuple("OpPhotonHits","OpPhotonHits");
    analysisManager->CreateNtupleIColumn("hitNumber");
    analysisManager->FinishNtuple(0);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

RunAction::~RunAction()
{ 
  delete G4AnalysisManager::Instance();
}
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4Run* RunAction::GenerateRun()
{ 
  fRun = new Run();
  return fRun;
}
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void RunAction::BeginOfRunAction(const G4Run*)
{ 
  // Reset the total hit counter at the beginning of the run
  TotalHitCounterOpPhoton::Instance()->ResetOpPhoton();

  // keep run condition
  if (fPrimary) { 
    G4ParticleDefinition* particle 
      = fPrimary->GetParticleGun()->GetParticleDefinition();
    G4double energy = fPrimary->GetParticleGun()->GetParticleEnergy();
    fRun->SetPrimary(particle, energy);
  }    
      
  // root file
  //
  G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
  if ( analysisManager->IsActive() ) {
    analysisManager->OpenFile();
  }

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void RunAction::EndOfRunAction(const G4Run*)
{
    // Print out the total number of hits at the end of the run
    int totalHitsOpPhoton = TotalHitCounterOpPhoton::Instance()->GetTotalHitsOpPhoton();
    G4cout << "\nTotal number of OpPhoton hits on the PMTs over the entire run: " << totalHitsOpPhoton << G4endl;

 if (isMaster) fRun->EndOfRun();
            
 //save root file
 //
 G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
 if ( analysisManager->IsActive() ) {
  analysisManager->Write();
  analysisManager->CloseFile();
 } 
}

void RunAction::Book()
{
  // Create or get analysis manager
  G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
  analysisManager->SetFileName(fFileName);
  analysisManager->SetVerboseLevel(1);
  analysisManager->SetActivation(true);     //enable inactivation of histograms

  // Define histogram values
  const G4int kMaxHisto = 1;
  const G4String id[] = {"0"};
  const G4String title[] = { "dummy"};

  // Create histogram
  for (G4int k=0; k<kMaxHisto; k++) {
    G4int ih = analysisManager->CreateH1(id[k], title[k], 100, 0., 100.);
    analysisManager->SetH1Activation(ih, true);
  }

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
