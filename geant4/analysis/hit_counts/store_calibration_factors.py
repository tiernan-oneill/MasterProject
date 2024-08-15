import numpy as np

'''
Script applies calibration factors to the hit counts of the particles.
The script will save the calibration factors for each particle type and energy in a text file.
'''

ParticleList = [
    "gamma",
    "electron",
    "positron"
]

# First load in the mean hit counts for each particle type 
for particle in ParticleList:
    exec(f"{particle}_mean_array = []")
    with open(f"/data/xenon/toneill/rdecay01_edit_3_output/hit_info_data/{particle}_hit_info.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            # Skip first three lines
            if line.startswith("##") or line.startswith("Energy") or line == "\n":
                continue
            else:
                Particle, mean, std_dev = line.split()
                exec(f"{particle}_mean_array.append({mean})")

# List of energies to loop through, from 0 to 5 MeV in 0.25 MeV increments
# along with the inclusion of the gamma calibration energy 2.225 MeV
energies = [0.0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.225, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5]
calibration_hit_count = gamma_mean_array[energies.index(2.225)]

# Create new arrays with calibrated energies using the calibration hit count
for particle in ParticleList:
    exec(f"{particle}_calibration_factors = np.divide({particle}_mean_array, calibration_hit_count)")


# Create text file to save the calibration factors and true energies for Gammas
with open("/data/xenon/toneill/rdecay01_edit_3_output/hit_info_data/gamma_calibration_factors.txt", "w") as file:
    file.write("## Calibration factors of Gammas for different energies ##\n\n")
    file.write("True energy (MeV) , Calibration factor\n")
    for i in range(len(energies)):
        file.write(f"{energies[i]} {gamma_calibration_factors[i]}\n")

# Create text file to save the calibration factors and true energies for Electrons
with open("/data/xenon/toneill/rdecay01_edit_3_output/hit_info_data/electron_calibration_factors.txt", "w") as file:
    file.write("## Calibration factors of Electrons for different energies ##\n\n")
    file.write("True energy (MeV) , Calibration factor\n")
    for i in range(len(energies)):
        file.write(f"{energies[i]} {electron_calibration_factors[i]}\n")

# Create text file to save the calibration factors and true energies for Positrons
with open("/data/xenon/toneill/rdecay01_edit_3_output/hit_info_data/positron_calibration_factors.txt", "w") as file:
    file.write("## Calibration factors of Positrons for different energies ##\n\n")
    file.write("True energy (MeV) , Calibration factor\n")
    for i in range(len(energies)):
        file.write(f"{energies[i]} {positron_calibration_factors[i]}\n")