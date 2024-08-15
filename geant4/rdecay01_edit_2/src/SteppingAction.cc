#include "SteppingAction.hh"

MySteppingAction::MySteppingAction()
: G4UserSteppingAction(), fTimeThreshold(0)
{   
    istimethreshold = false;

    // Set the time threshold (eg. 1 day)
    fTimeThreshold = 24*3600*second;

    if (istimethreshold) {
        G4cout << "Time threshold is enabled and set to: " << fTimeThreshold/second << " s" << G4endl;
    }
}

MySteppingAction::~MySteppingAction() {}

void MySteppingAction::UserSteppingAction(const G4Step* step) {

    if (istimethreshold) {
        G4double globalTime = step->GetPostStepPoint()->GetGlobalTime();
        if (globalTime > fTimeThreshold) {
        G4RunManager::GetRunManager()->AbortEvent();
        /*G4cout << "Event aborted because global time exceeded the threshold of "
               << fTimeThreshold / second << " seconds. Global time: "
               << globalTime / second << " seconds." << G4endl;*/
        }
    }
}