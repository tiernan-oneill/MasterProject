#ifndef TOTAL_HIT_COUNTER_H
#define TOTAL_HIT_COUNTER_H

class TotalHitCounterOpPhoton {
public:
    static TotalHitCounterOpPhoton* Instance();
    void AddHitOpPhoton();
    int GetTotalHitsOpPhoton() const;
    void ResetOpPhoton();

private:
    TotalHitCounterOpPhoton();
    ~TotalHitCounterOpPhoton();
    static TotalHitCounterOpPhoton* fInstanceOpPhoton;
    int fTotalHitsOpPhoton;
};

#endif