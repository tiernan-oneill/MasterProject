#include "SteppingAction.hh"

MySteppingAction::MySteppingAction()
: G4UserSteppingAction(), fTimeThreshold(0)
{   
    istimethreshold = false;

    // Set the time threshold (eg. 1 day)
    fTimeThreshold = 24*3600*second;

    if (istimethreshold) {
        G4cout << "Time threshold is enabled and set to: " << fTimeThreshold/second << " s\n" << G4endl;
    }
}

MySteppingAction::~MySteppingAction() {}

void MySteppingAction::UserSteppingAction(const G4Step* step) {

    if (istimethreshold) {
        G4double globalTime = step->GetPostStepPoint()->GetGlobalTime();
        if (globalTime > fTimeThreshold) {
        G4RunManager::GetRunManager()->AbortEvent();
        }
    }

    /*
    // Get step information
    G4Track* track = step->GetTrack();
    G4StepPoint* preStepPoint = step->GetPreStepPoint();
    G4StepPoint* postStepPoint = step->GetPostStepPoint();
    G4ThreeVector prePosition = preStepPoint->GetPosition();
    G4ThreeVector postPosition = postStepPoint->GetPosition();
    G4double energyDeposit = step->GetTotalEnergyDeposit();
    G4double stepLength = step->GetStepLength();

    G4cout << "Energy deposit: " << energyDeposit/keV << " keV, at position: " << postPosition/mm << " mm" << G4endl;
    */
}