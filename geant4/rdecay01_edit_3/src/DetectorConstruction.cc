#include "DetectorConstruction.hh"

DetectorConstruction::DetectorConstruction()
 : G4VUserDetectorConstruction()
{
    fWorldSize = 16*m;  // World size containing the KamLAND and Xenon liquid scintillators and PMTs

    // booleans to edit the construction of the detector
    checkOverlaps = true;
    constructScintillators = true;
    constructSensitiveDetectors = true;  // PMTs
}

DetectorConstruction::~DetectorConstruction()
{}

void DetectorConstruction::DefineMaterials()
{
    // Define elements for decane, pseudocumene, dodecane and PPO
    C = new G4Element("Carbon", "C", 6, 12.01 * g/mole);
    H = new G4Element("Hydrogen", "H", 1, 1.01 * g/mole);
    O = new G4Element("Oxygen", "O", 8, 16.00 * g/mole);
    N = new G4Element("Nitrogen", "N", 7, 14.01 * g/mole);

    // Define these materials
    Decane = new G4Material("Decane", 0.731 * g/cm3, 2);
    Decane->AddElement(C, 10);
    Decane->AddElement(H, 22);

    Pseudocumene = new G4Material("pseudocumene", 0.875 * g/cm3, 2);
    Pseudocumene->AddElement(C, 9);
    Pseudocumene->AddElement(H, 12);

    Dodecane = new G4Material("Dodecane", 0.753 * g/cm3, 2);
    Dodecane->AddElement(C, 12);
    Dodecane->AddElement(H, 26);

    PPO = new G4Material("PPO", 1.094 * g/cm3, 4);
    PPO->AddElement(C, 15);
    PPO->AddElement(H, 11);
    PPO->AddElement(O, 1);
    PPO->AddElement(N, 1);

    // Define xenon isotopes in the Xe liquid scintillator
    G4Isotope* Xe136 = new G4Isotope("Xe136", 54, 136, 135.90722 * g/mole);
    G4Isotope* Xe134 = new G4Isotope("Xe134", 54, 134, 133.80539 * g/mole);
    // Set the Xe ratio
    G4double enrich_fraction = 0.9077;  // 90% enriched
    Xe = new G4Element("enriched Xenon", "Xe", 2);
    Xe->AddIsotope(Xe136, enrich_fraction);
    Xe->AddIsotope(Xe134, 1.0 - enrich_fraction);

    // Define Xe liquid scintillator, first without the xenon
    XeLS_noXe = new G4Material("XenonLiquidScintillator_noXe", 0.780 * g/cm3, 3);
    PPO_fraction_Xe = 2.38*g/(1e3*cm3*0.780*g/cm3);  // 2.38 g/l
    XeLS_noXe->AddMaterial(Decane, 0.824/(1.0+PPO_fraction_Xe));
    XeLS_noXe->AddMaterial(Pseudocumene, 0.176/(1.0+PPO_fraction_Xe));
    XeLS_noXe->AddMaterial(PPO, PPO_fraction_Xe/(1.0+PPO_fraction_Xe));

    XeLS = new G4Material("XenonLiquidScintillator", 0.78013 * g/cm3, 2);
    XeLS->AddMaterial(XeLS_noXe, 0.9687);
    XeLS->AddElement(Xe, 0.0313);  // 3.13% by weight

    // Now define KamLAND liquid scintillator
    KamLS = new G4Material("KamLandLiquidScintillator", 0.7772 * g/cm3, 3);
    PPO_fraction_Kam = 1.36*g/(1e3*cm3*0.7772*g/cm3);  // 1.36 g/l
    KamLS->AddMaterial(Dodecane, 0.802/(1.0+PPO_fraction_Kam));
    KamLS->AddMaterial(Pseudocumene, 0.198/(1.0+PPO_fraction_Kam));
    KamLS->AddMaterial(PPO, PPO_fraction_Kam/(1.0+PPO_fraction_Kam));

    // Define the Optical Surface between the scintillators
    OpticalSurface = new G4OpticalSurface("ScintillatorBorderSurface");
    OpticalSurface->SetType(dielectric_dielectric);
    OpticalSurface->SetFinish(polished);
    OpticalSurface->SetModel(unified);

    // Define the detector material
    detectorMat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Si");

    // Define the photocathode surface for sensitive detector
    photocathodeSurface = new G4OpticalSurface("PhotocathodeSurface");
    photocathodeSurface->SetType(dielectric_metal);
    photocathodeSurface->SetFinish(polished);
    photocathodeSurface->SetModel(unified);

    // Define the world material as air
    worldMat = G4NistManager::Instance()->FindOrBuildMaterial("G4_AIR");
}

void DetectorConstruction::SetMaterialProperties()
{   
    // Define optical properties for the XeLS
    mptXeLS = new G4MaterialPropertiesTable();
    G4double energyXeLS[2] = {1.375 * eV, 6.2 * eV};  // range of energies for optical photons
    G4double rindexXeLS[2] = {1.45, 1.45};
    G4double absorptionLengthXeLS[2] = {15.8*m, 15.8*m};
    G4double scatteringLengthXeLS[2] = {1*m, 1*m};  // unsure about this value
    G4double reEmissionXeLS[2] = {0.158, 0.158};
    G4double fastScintYieldXeLS[2] = {0.75, 0.75};
    G4double midScintYieldXeLS[2] = {0.21, 0.21};
    G4double slowScintYieldXeLS[2] = {0.04, 0.04};
    G4double fastTimeConstantXeLS = 3.7*ns;
    G4double midTimeConstantXeLS = 10.8*ns;
    G4double slowTimeConstantXeLS = 195*ns;
    G4double scintillationYieldXeLS = 6592./MeV;
    G4double birksConstantXeLS = 0.31 * mm/MeV;
    // Unsure about these values
    G4double resolutionScaleXeLS = 1.0;
    G4double fastYieldRatioXeLS = 0.6;
    G4double midYieldRatioXeLS = 0.3;
    G4double slowYieldRatioXeLS = 0.1;
    
    mptXeLS->AddProperty("RINDEX", energyXeLS, rindexXeLS, 2);
    mptXeLS->AddProperty("ABSLENGTH", energyXeLS, absorptionLengthXeLS, 2);
    mptXeLS->AddProperty("RAYLEIGH", energyXeLS, scatteringLengthXeLS, 2);
    mptXeLS->AddProperty("REEMISSIONPROB", energyXeLS, reEmissionXeLS, 2);
    mptXeLS->AddProperty("SCINTILLATIONCOMPONENT1", energyXeLS, fastScintYieldXeLS, 2);
    mptXeLS->AddProperty("SCINTILLATIONCOMPONENT2", energyXeLS, midScintYieldXeLS, 2);
    mptXeLS->AddProperty("SCINTILLATIONCOMPONENT3", energyXeLS, slowScintYieldXeLS, 2);
    mptXeLS->AddConstProperty("SCINTILLATIONTIMECONSTANT1", fastTimeConstantXeLS);
    mptXeLS->AddConstProperty("SCINTILLATIONTIMECONSTANT2", midTimeConstantXeLS);
    mptXeLS->AddConstProperty("SCINTILLATIONTIMECONSTANT3", slowTimeConstantXeLS);
    mptXeLS->AddConstProperty("SCINTILLATIONYIELD", scintillationYieldXeLS);
    mptXeLS->AddConstProperty("BIRKS_CONSTANT", birksConstantXeLS);
    mptXeLS->AddConstProperty("RESOLUTIONSCALE", resolutionScaleXeLS);
    mptXeLS->AddConstProperty("SCINTILLATIONYIELD1", fastYieldRatioXeLS);
    mptXeLS->AddConstProperty("SCINTILLATIONYIELD2", midYieldRatioXeLS);
    mptXeLS->AddConstProperty("SCINTILLATIONYIELD3", slowYieldRatioXeLS);
    //mptXeLS->DumpTable();

    XeLS->SetMaterialPropertiesTable(mptXeLS);

    // Define optical properties for the KamLS
    mptKamLS = new G4MaterialPropertiesTable();
    G4double energyKamLS[2] = {1.375 * eV, 6.2 * eV};  // range of energies for optical photons
    G4double rindexKamLS[2] = {1.5, 1.5};  // unsure about this value
    G4double absorptionLengthKamLS[2] = {12.0*m, 12.0*m};
    G4double scatteringLengthKamLS[2] = {1*m, 1*m};  // unsure about this value
    G4double reEmissionKamLS[2] = {0.069, 0.069};
    G4double fastScintYieldKamLS[2] = {0.79, 0.79};
    G4double midScintYieldKamLS[2] = {0.17, 0.17};
    G4double slowScintYieldKamLS[2] = {0.04, 0.04};
    G4double fastTimeConstantKamLS = 7.2*ns;
    G4double midTimeConstantKamLS = 8.09*ns;
    G4double slowTimeConstantKamLS = 196*ns;
    G4double scintillationYieldKamLS = 7909./MeV;
    G4double birksConstantKamLS = 0.23 * mm/MeV;
    // Unsure about these values
    G4double resolutionScaleKamLS = 1.0;
    G4double fastYieldRatioKamLS = 0.6;
    G4double midYieldRatioKamLS = 0.3;
    G4double slowYieldRatioKamLS = 0.1;

    mptKamLS->AddProperty("RINDEX", energyKamLS, rindexKamLS, 2);
    mptKamLS->AddProperty("ABSLENGTH", energyKamLS, absorptionLengthKamLS, 2);
    mptKamLS->AddProperty("RAYLEIGH", energyKamLS, scatteringLengthKamLS, 2);
    mptKamLS->AddProperty("REEMISSIONPROB", energyKamLS, reEmissionKamLS, 2);
    mptKamLS->AddProperty("SCINTILLATIONCOMPONENT1", energyKamLS, fastScintYieldKamLS, 2);
    mptKamLS->AddProperty("SCINTILLATIONCOMPONENT2", energyKamLS, midScintYieldKamLS, 2);
    mptKamLS->AddProperty("SCINTILLATIONCOMPONENT3", energyKamLS, slowScintYieldKamLS, 2);
    mptKamLS->AddConstProperty("SCINTILLATIONTIMECONSTANT1", fastTimeConstantKamLS);
    mptKamLS->AddConstProperty("SCINTILLATIONTIMECONSTANT2", midTimeConstantKamLS);
    mptKamLS->AddConstProperty("SCINTILLATIONTIMECONSTANT3", slowTimeConstantKamLS);
    mptKamLS->AddConstProperty("SCINTILLATIONYIELD", scintillationYieldKamLS);
    mptKamLS->AddConstProperty("BIRKS_CONSTANT", birksConstantKamLS);
    mptKamLS->AddConstProperty("RESOLUTIONSCALE", resolutionScaleKamLS);
    mptKamLS->AddConstProperty("SCINTILLATIONYIELD1", fastYieldRatioKamLS);
    mptKamLS->AddConstProperty("SCINTILLATIONYIELD2", midYieldRatioKamLS);
    mptKamLS->AddConstProperty("SCINTILLATIONYIELD3", slowYieldRatioKamLS);
    //mptKamLS->DumpTable();

    KamLS->SetMaterialPropertiesTable(mptKamLS);

    // Create the material properties table for the optical surface between the scintillators
    mptOpticalSurface = new G4MaterialPropertiesTable();
    // Example:
    G4double energyOpticalSurface[2] = {1.375 * eV, 6.2 * eV};  // range of energies for optical photons
    G4double reflectivity[2] = {1.0, 1.0}; // Assume 100% reflectivity

    mptOpticalSurface->AddProperty("REFLECTIVITY", energyOpticalSurface, reflectivity, 2);
    OpticalSurface->SetMaterialPropertiesTable(mptOpticalSurface);

    mptPhotocathode = new G4MaterialPropertiesTable();
    G4double energiesPhotocathode[2] = {1.375 * eV, 6.2 * eV};  // range of energies for optical photons
    G4double reflectivityPhotocathode[2] = {1.0, 1.0};  // Assume 100% reflectivity
    
    mptPhotocathode->AddProperty("REFLECTIVITY", energiesPhotocathode, reflectivityPhotocathode, 2);
    photocathodeSurface->SetMaterialPropertiesTable(mptPhotocathode);
}

G4VPhysicalVolume* DetectorConstruction::Construct()
{   
    // Define the materials
    DefineMaterials();

    // Define the material properties
    SetMaterialProperties();

    // Define the box world volume
    solidWorld = new G4Box("solidWorld", fWorldSize/2, fWorldSize/2, fWorldSize/2);
    
    // Define the logical world volume
    logicWorld = new G4LogicalVolume(solidWorld, worldMat, "logicWorld");

    // Define the physical world volume
    physWorld = new G4PVPlacement(0, G4ThreeVector(), logicWorld, "physiWorld", 0, false, 0);

    // Define size of the spheres
    KamLSRadius = 6.5 * m;
    XeLSRadius = 1.9 * m;

    // Construct and place XeLS sphere
    solidXeLS = new G4Sphere("solidXeLS", 0, XeLSRadius, 0, 2 * CLHEP::pi, 0, CLHEP::pi);
    logicXeLS = new G4LogicalVolume(solidXeLS, XeLS, "logicXeLS");
    if (constructScintillators){
        physXeLS = new G4PVPlacement(0, G4ThreeVector(), logicXeLS, "physXeLS", logicWorld, false, 1, checkOverlaps);
    }

    // Construct and place outer sphere (actually a shell starting at the XeLS radius and ending at the KamLS radius)
    solidKamLS = new G4Sphere("solidKamLS", XeLSRadius, KamLSRadius, 0, 2 * CLHEP::pi, 0, CLHEP::pi);
    logicKamLS = new G4LogicalVolume(solidKamLS, KamLS, "logicKamLS");
    if (constructScintillators){
        physKamLS = new G4PVPlacement(0, G4ThreeVector(), logicKamLS, "physKamLS", logicWorld, false, 2, checkOverlaps);
    }

    // Create the logical border surface between the scintillators
    if (constructScintillators){
        new G4LogicalBorderSurface("ScintillatorBorder", physXeLS, physKamLS, OpticalSurface);
    }

    // Construct the sensitive detector shell around the KamLS
    if (constructSensitiveDetectors){
        solidDetectorShell = new G4Sphere("solidDetector", KamLSRadius, KamLSRadius + 1*m, 0, 2 * CLHEP::pi, 0, CLHEP::pi);
        logicDetector = new G4LogicalVolume(solidDetectorShell, detectorMat, "logicDetector");

        // Create and register sensitive detector
        G4SDManager* sdManager = G4SDManager::GetSDMpointer();
        MySensitiveDetector* sensDet = new MySensitiveDetector("MySensitiveDetector");
        sdManager->AddNewDetector(sensDet);
        logicDetector->SetSensitiveDetector(sensDet);

        physDetector = new G4PVPlacement(0, G4ThreeVector(), logicDetector, "physDetector", logicWorld, false, 3, checkOverlaps);
    }

    // Attach the optical surface to the PMT
    if (constructSensitiveDetectors && constructScintillators){
        new G4LogicalBorderSurface("PhotocathodeSurface", physKamLS, physDetector, photocathodeSurface);
    }

    //
    //always return the physical World
    //  
    return physWorld;
}