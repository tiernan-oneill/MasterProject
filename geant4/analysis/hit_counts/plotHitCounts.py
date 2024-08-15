import matplotlib.pyplot as plt

'''
Script to plot the mean number of optical photon hits against the energy of the particle.
The calibration point and hit count number is also plotted.
The plot is saved as a PNG file.
'''

ParticleList = [
    "gamma",
    "electron",
    "positron"
]

# Load in all the mean hit counts for each particle type
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

# Plot the mean values against the energies
energies = [0.0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.225, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5]  # MeV
calibration_hit_count = gamma_mean_array[energies.index(2.225)]

plt.figure(figsize=(14, 8))
plt.plot(energies, gamma_mean_array, color="green", label="Gamma")
plt.plot(energies, electron_mean_array, color="red", label="Electron")
plt.plot(energies, positron_mean_array, color="blue", label="Positron")

# Plot vertical line at calibration energy
plt.axvline(x=2.225, color="black", linestyle="--", label=f"Calibration Energy.\nHit Count = {int(round(calibration_hit_count))}")

plt.xlabel("Energy (MeV)", fontsize=20, loc="right")
plt.ylabel("OP HC", fontsize=20, loc="top")
plt.title("Mean OP HC (1e4 events) vs Energy", fontsize=25)
plt.legend(fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()

plt.savefig("figures/hitCount.png")