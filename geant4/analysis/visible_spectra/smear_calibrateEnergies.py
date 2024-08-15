import ROOT
import numpy as np
from tqdm import tqdm

'''
Script applies a smearing and calibration to the real energies of the particles.
The script will save the smeared energies and then the smeared+calibrated energies 
in a new ROOT file. The hits_info_data folder contains the calibration factor information
for each particle type that we apply below.
'''

smear_calibrate_all_isotopes = False

if(smear_calibrate_all_isotopes):
    Isotope_list = [
    "88Y",
    "90m1Zr"
    "90Nb",
    "96Tc",
    "98Rh",
    "100Rh",
    "104Ag",
    "104m1Ag",
    "107In",
    "108In",
    "109Sn",
    "110In",
    "110m1In",
    "113Sb",
    "114Sb",
    "115Sb",
    "115Te",
    "116Sb",
    "117Te",
    "118Sb",
    "119I",
    "120I",
    "121Xe",
    "122I",
    "124I",
    "124Sb",
    "125Cs",
    "126Cs",
    "128Cs",
    "130I",
    "132I", 
    "134I"
    ]
else:
    Isotope_list = ["124Sb"]

ParticleList = ["positron", "electron", "gamma"]

for particle in ParticleList:
    exec(f"{particle}_calibration_factors = []")
    with open(f"/data/xenon/toneill/rdecay01_edit_3_output/hit_info_data/{particle}_calibration_factors.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            # Skip first three lines
            if line.startswith("##") or line.startswith("True") or line == "\n":
                continue
            else:
                energy, calibration_factor = line.split()
                exec(f"{particle}_calibration_factors.append({calibration_factor})")
Energy_list = [0.0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.225, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5]  # MeV

def apply_energy_resolution(energy, resolution_percent=6.7):
    sigma = (resolution_percent / 100) * np.sqrt(energy)
    smeared_energy = np.random.normal(energy, sigma)
    return smeared_energy

for Isotope in Isotope_list:

    # Open the ROOT file
    root_file = ROOT.TFile.Open(f'/data/xenon/toneill/rdecay01_edit_2_output/output_{Isotope}.root')

    # Create a new ROOT file to store new energies
    output_file = ROOT.TFile.Open(f"/data/xenon/toneill/final_output/{Isotope}.root", "RECREATE")
    new_tree = ROOT.TTree("totalEkin", "New energies")

    # Create branches for smeared and calibrated energies
    smeared_energy = np.zeros(1, dtype=float)
    smeared_calibrated_energy = np.zeros(1, dtype=float)

    new_tree.Branch("total_smeared", smeared_energy, "smeared_energy/D")
    new_tree.Branch("total_smeared_calibrated", smeared_calibrated_energy, "smeared_calibrated_energy/D")

    # Loop through each particle and apply the smearing and calibrating, and store both
    for particle in ParticleList:
        tree = root_file.Get(particle)
        n_entries = tree.GetEntries()
        print(f"Smearing and calibrating {n_entries} {particle} energies for {Isotope}")
        for event in tqdm(tree):
            energy = getattr(event, f"{particle}Ekin")
            # Smear the energies
            smeared_energy[0] = apply_energy_resolution(energy)

            # Then calibrate the energies
            if particle == "positron":
                energy_calibration_factor = np.interp(energy, Energy_list, positron_calibration_factors)
            if particle == "gamma":
                energy_calibration_factor = np.interp(energy, Energy_list, gamma_calibration_factors)
            else:
                energy_calibration_factor = np.interp(energy, Energy_list, electron_calibration_factors)

            smeared_calibrated_energy[0] = energy_calibration_factor*smeared_energy[0]

            new_tree.Fill()

    # Write the new tree to the output file and clean up
    new_tree.Write()
    output_file.Close()
    root_file.Close()