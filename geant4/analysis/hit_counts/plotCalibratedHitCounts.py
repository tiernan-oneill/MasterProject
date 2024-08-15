import matplotlib.pyplot as plt
import numpy as np

'''
Script to plot the mean number of optical photon hits against the calibrated energy of the particle.
To show the effects of hit count calibration on the energies.
The plot is saved as a PNG file.
'''

ParticleList = [
    "gamma",
    "electron",
    "positron"
]

for particle in ParticleList:
    exec(f"{particle}_mean_array = []")
    with open(f"/data/xenon/toneill/rdecay01_edit_3_output/hit_info_data/{particle}_hit_info.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            # Skip first three lines
            if line.startswith("##") or line.startswith("Energy") or line == "\n":
                continue
            else:
                Energy, mean, std_dev = line.split()
                exec(f"{particle}_mean_array.append({mean})")

energies = [0.0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.225, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5]  # MeV
calibration_hit_count = gamma_mean_array[energies.index(2.225)]

# Create new arrays with calibrated energies
for particle in ParticleList:
    exec(f"{particle}_calibration_factors = np.divide({particle}_mean_array, calibration_hit_count)")
    exec(f"{particle}_calibrated_energies = np.multiply(energies, {particle}_calibration_factors)")

# Plot the mean values against the calibrated energies
plt.figure(figsize=(14, 8))
plt.plot(gamma_calibrated_energies, gamma_mean_array, label="Gamma",  color="green")
plt.plot(electron_calibrated_energies, electron_mean_array, label="Electron", color="red")
plt.plot(positron_calibrated_energies, positron_mean_array, label="Positron", color="blue")

# Plot vertical line at calibration energy
plt.axvline(x=2.225, color="black", linestyle="--", label=f"Calibration Energy.\nHit Count = {int(round(calibration_hit_count))}")

plt.xlabel("Calibrated Energy (MeV)", fontsize=20, loc="right")
plt.ylabel("OP HC", fontsize=20, loc="top")
plt.title("Mean OP HC (1e4 events) vs Calibrated Energy", fontsize=25)
plt.legend(fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()

plt.savefig("figures/hitCountCalibrated.png")