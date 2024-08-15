#include "RunAction.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

RunAction::RunAction(PrimaryGeneratorAction* kin)
:G4UserRunAction(),
 fPrimary(kin), fRun(0), fFileName("rdecay01")
{   // this function is related to the filename and type information
    Book();

    // Create arrays to store energy information of all secondaries as well as a combined array
    G4AnalysisManager::Instance()->CreateNtuple("electron","electron");
    G4AnalysisManager::Instance()->CreateNtupleDColumn("electronEkin");
    G4AnalysisManager::Instance()->FinishNtuple(0);
    G4AnalysisManager::Instance()->CreateNtuple("positron","positron");
    G4AnalysisManager::Instance()->CreateNtupleDColumn("positronEkin");
    G4AnalysisManager::Instance()->FinishNtuple(1);
    G4AnalysisManager::Instance()->CreateNtuple("gamma","gamma");
    G4AnalysisManager::Instance()->CreateNtupleDColumn("gammaEkin");
    G4AnalysisManager::Instance()->FinishNtuple(2);
    G4AnalysisManager::Instance()->CreateNtuple("neutrino","neutrino");
    G4AnalysisManager::Instance()->CreateNtupleDColumn("neutrinoEkin");
    G4AnalysisManager::Instance()->FinishNtuple(3);
    G4AnalysisManager::Instance()->CreateNtuple("totalEkin","totalEkin");
    G4AnalysisManager::Instance()->CreateNtupleDColumn("totalEkin");
    G4AnalysisManager::Instance()->FinishNtuple(4);

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
  // keep run condition
  if (fPrimary) { 
    G4ParticleDefinition* particle 
      = fPrimary->GetParticleGun()->GetParticleDefinition();
    G4double energy = fPrimary->GetParticleGun()->GetParticleEnergy();
    fRun->SetPrimary(particle, energy);
  }    
      
  //histograms
  //
  G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
  if ( analysisManager->IsActive() ) {
    analysisManager->OpenFile();
  }

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void RunAction::EndOfRunAction(const G4Run*)
{
 if (isMaster) fRun->EndOfRun();
            
 //save histograms
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
