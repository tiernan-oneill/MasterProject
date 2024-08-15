#include "PMT.hh"
#include "TotalHitCounter.hh"

MySensitiveDetector::MySensitiveDetector(const G4String& name): 
G4VSensitiveDetector(name), fHitCountPerEvent(0)
{}

MySensitiveDetector::~MySensitiveDetector()
{}

void MySensitiveDetector::Initialize(G4HCofThisEvent* hce) 
{
    fHitCountPerEvent = 0;  // Reset hit count at the beginning of each event
}

G4bool MySensitiveDetector::ProcessHits(G4Step *step, G4TouchableHistory *history)
{   
    // Get particle name
    G4String particleName = step->GetTrack()->GetDefinition()->GetParticleName();

    if(particleName == "opticalphoton"){
        //G4double photocoverage = 0.34;  // Default photocoverage
        G4double photocoverage = 1.0;  // Assume 100% photocoverage
        //G4double quEff = 0.35;  // Default quantum efficiency
        G4double quEff = 1.0;  // Assume 100% quantum efficiency

        G4double rand1 = G4UniformRand();
        G4double rand2 = G4UniformRand();
        //G4cout << "Random number: " << rand1 << " to compare to Quantum Efficiency: " << quEff << G4endl;
        //G4cout << "Random number: " << rand2 << " to compare to Photocoverage: " << photocoverage << G4endl;

        if(rand1 < quEff && rand2 < photocoverage){
            //G4cout << "Photon detected and absorbed by PMT!" << G4endl;

            fHitCountPerEvent++;  // Increment hit count for this event
            TotalHitCounterOpPhoton::Instance()->AddHitOpPhoton();  // Increment hit count for the whole run

            // Get the hit position and energy
            G4ThreeVector hitPosition = step->GetPostStepPoint()->GetPosition();
            G4double hitEnergy = step->GetPostStepPoint()->GetTotalEnergy();
            //G4cout << "Hit Position: " << hitPosition/m << " m, Hit Energy: " << hitEnergy/eV << " eV" << G4endl;
        }
    }
    
    // Kill all tracks once PMT is hit
    step->GetTrack()->SetTrackStatus(fStopAndKill);
    return true;  // Return true if the hit was processed
}

void MySensitiveDetector::EndOfEvent(G4HCofThisEvent* hce) 
{
    //G4cout << "Number of hits in this event: " << fHitCountPerEvent << G4endl;
    G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
    analysisManager->FillNtupleIColumn(0, fHitCountPerEvent);
    analysisManager->AddNtupleRow(0);
}