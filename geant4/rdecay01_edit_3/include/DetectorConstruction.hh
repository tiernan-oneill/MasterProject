#ifndef DetectorConstruction_h
#define DetectorConstruction_h 1

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"

#include "PMT.hh"
#include "G4OpticalSurface.hh"
#include "G4LogicalBorderSurface.hh"

#include "G4Material.hh"
#include "G4Sphere.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4SDManager.hh"
#include "G4RotationMatrix.hh"
#include "G4RandomDirection.hh"

#include "G4MaterialPropertiesTable.hh"
#include "G4MaterialPropertyVector.hh"

#include <fstream>
#include <vector>
#include <iostream>

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

class DetectorConstruction : public G4VUserDetectorConstruction
{
  public:
  
    DetectorConstruction();
    virtual ~DetectorConstruction();

    virtual G4VPhysicalVolume* Construct();
                        
    G4double GetWorldSize() {return fWorldSize;}; 

  private:
    void DefineMaterials();
    void SetMaterialProperties();
  
    G4double fWorldSize, KamLSRadius, XeLSRadius, detectorSize, detectorDistance, PPO_fraction_Xe, PPO_fraction_Kam;

    G4bool checkOverlaps, constructScintillators, constructSensitiveDetectors;

    G4Element *C, *H, *O, *N, *Xe;
    G4Material *Decane, *Pseudocumene, *Dodecane, *PPO;
    G4Material *KamLS, *XeLS, *XeLS_noXe, *detectorMat, *worldMat; 
    G4MaterialPropertiesTable *mptKamLS, *mptXeLS, *mptPhotocathode, *mptOpticalSurface;
    G4OpticalSurface *photocathodeSurface, *OpticalSurface;

    G4Box *solidWorld, *solidDetectorBox;
    G4Sphere *solidKamLS, *solidXeLS, *solidDetectorShell;

    G4LogicalVolume *logicDetector, *logicWorld, *logicKamLS, *logicXeLS;
    G4VPhysicalVolume *physWorld, *physKamLS, *physXeLS, *physDetector;
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif

