#include "TotalHitCounter.hh"

TotalHitCounterOpPhoton* TotalHitCounterOpPhoton::fInstanceOpPhoton = nullptr;

TotalHitCounterOpPhoton::TotalHitCounterOpPhoton() : fTotalHitsOpPhoton(0) {}

TotalHitCounterOpPhoton::~TotalHitCounterOpPhoton() {}

TotalHitCounterOpPhoton* TotalHitCounterOpPhoton::Instance() {
    if (!fInstanceOpPhoton) {
        fInstanceOpPhoton = new TotalHitCounterOpPhoton();
    }
    return fInstanceOpPhoton;
}

void TotalHitCounterOpPhoton::AddHitOpPhoton() {
    fTotalHitsOpPhoton++;
}

int TotalHitCounterOpPhoton::GetTotalHitsOpPhoton() const {
    return fTotalHitsOpPhoton;
}

void TotalHitCounterOpPhoton::ResetOpPhoton() {
    fTotalHitsOpPhoton = 0;
}
