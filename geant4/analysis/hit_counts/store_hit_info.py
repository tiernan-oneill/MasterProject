import ROOT
import os

'''
Script creates histograms of the hit count for each particle type and energy.
The script will save the histograms as PNG files to the figures/{Particle} folder 
and also save the mean and standard deviation values for each energy in a text file.
'''

Particle_list= ["electron", "positron", "gamma"]

# List of energies to loop through, from 0 to 5 MeV in 0.25 MeV increments
# along with the inclusion of the calibration energy 2.225 MeV
Energy_list= [
    "0",
    "025",
    "05",
    "075",
    "1",
    "125",
    "15",
    "175",
    "2",
    "2225",
    "225",
    "25",
    "275",
    "3",
    "325",
    "35",
    "375",
    "4",
    "425",
    "45",
    "475",
    "5"
    ]

for Particle in Particle_list:
    # Create arrays to save data
    mean_array = []
    std_dev_array = []
    for Energy in Energy_list:
        root_file = ROOT.TFile.Open(f"/data/xenon/toneill/rdecay01_edit_3_output/output_{Particle}{Energy}.root")
        tree = root_file.Get("OpPhotonHits")
        # Get the maximum number of hits in an event to determine the range of the histogram
        max_hits = tree.GetMaximum("hitNumber")

        # Create the histogram
        hist = ROOT.TH1F("hist", f"OpPhoton Hit count for {Particle}; Hit Count; frequency (from 1e4 events)", 100, 0, max_hits)
        canvas = ROOT.TCanvas("canvas", f"{Particle} Hit count", 1000, 600)
        tree.Draw("hitNumber>>hist")

        hist.SetLineColor(ROOT.kRed)

        # Get the statistics of the histogram
        mean = hist.GetMean()
        mean_array.append(mean)
        std_dev = hist.GetStdDev()
        std_dev_array.append(std_dev)

        # Create a vertical dashed line at the mean value
        line = ROOT.TLine(mean, 0, mean, hist.GetMaximum())
        line.SetLineWidth(2)
        line.SetLineStyle(2)

        hist.Draw()
        line.Draw()
        canvas.Update()

        # Set output file name and folder path for the PNG file to be saved
        output_file_name = f"{Particle}{Energy}_hitCount.png"
        folder_path = f"figures/{Particle}s"

        file_path = os.path.join(folder_path, output_file_name)
        canvas.SaveAs(file_path)

        # Clean up
        del hist
        del canvas
        root_file.Close()

    # Create text file to save the mean and standard deviation values
    with open(f"/data/xenon/toneill/rdecay01_edit_3_output/hit_info_data/{Particle}_hit_info.txt", "w") as file:
        file.write(f"## Optical Photon Hit Count Information for {Particle}s of Different Energies ##\n\n")
        file.write("Energy Mean StandardDev\n")
        for i in range(len(Energy_list)):
            file.write(f"{Energy_list[i]} {mean_array[i]} {std_dev_array[i]}\n")