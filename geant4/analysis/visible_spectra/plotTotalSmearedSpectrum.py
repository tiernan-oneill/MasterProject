import ROOT
import os

'''
This script is used to make one plot: the total smeared energy spectrum of all of the isotopes. 
All 32 isotopes are also plotted, with respective production yields taken into account.
The script will save the plot as PNG files in the figures folder. It will also save a ROOT
file containing the combined histogram of all the individual histograms.
'''

simulated_events_factor = 1e-7  # need to account for the number of simulated events in scaling the histograms

def read_data_file(filename):
    '''Function reads in the yields data for each of the 32 isotopes
    and returns a dictionary with the isotope as the key and the yield as the value.'''
    data_dict = {}
    
    with open(filename, 'r') as file:
        # Skip the header line of file
        next(file)
        
        for line in file:
            key, value = line.split()
            data_dict[key] = float(value)
    
    return data_dict
    
IsotopeDict = read_data_file('../isotope_yields.dat')

# Define Y limits of plot
height_upper = 1e2
height_lower = 1e-4

# Define histogram parameters
bin_width = 0.05  # in MeV units
x_min = 0.5
x_max = 4.8
n_bins = int((x_max - x_min)/bin_width)

# Create a legend
legend = ROOT.TLegend(0.77, 0.8, 0.95, 0.91)  # These are the coordinates of the legend

for Isotope in IsotopeDict:
    print(f"Plotting {Isotope}")

    # Open the root files and get the tree for the total energies
    exec(f"root_file_{Isotope} = ROOT.TFile.Open(f'/data/xenon/toneill/final_output/{Isotope}.root')")
    exec(f"total_tree_{Isotope} = root_file_{Isotope}.Get('totalEkin')")

    # Create histograms of the energy spectrum, connect to tree data and draw it to a canvas
    exec(f"hist_{Isotope} = ROOT.TH1F('hist_{Isotope}', 'Isotope Smeared Energy Spectrum', n_bins, x_min, x_max)")
    exec(f"total_tree_{Isotope}.Draw('smeared_energy>>hist_{Isotope}')")

print("Finalising plot...")

canvas = ROOT.TCanvas("canvas", "Isotope Smeared Energy Spectrum", 1000, 600)

# Scale the histograms
for Isotope in IsotopeDict:
    yield_factor = IsotopeDict[Isotope]
    exec(f"hist_{Isotope}.Scale(yield_factor * simulated_events_factor/0.05)")

# Create a histogram for the sum of all isotopes
hist_combined = hist_88Y.Clone("hist_combined")
for Isotope in IsotopeDict:
    if Isotope != "88Y":
        exec(f"hist_combined.Add(hist_{Isotope})")
hist_combined.SetLineColor(ROOT.kBlack)
hist_combined.SetLineWidth(2)

# Draw the histograms
hist_88Y.Draw('HIST')
for Isotope in IsotopeDict:
    if Isotope != "88Y":
        exec(f"hist_{Isotope}.Draw('HIST SAME')")
hist_combined.Draw('HIST SAME')
legend.AddEntry(hist_combined, 'Total', 'l')

# Draw vertical lines to show the region of interest for 0vbb
vertical_line1 = ROOT.TLine(2.35, height_lower, 2.35, height_upper)
vertical_line2 = ROOT.TLine(2.7, height_lower, 2.7, height_upper)
vertical_line1.SetLineStyle(ROOT.kDashed)
vertical_line1.SetLineColor(ROOT.kBlack)
vertical_line1.Draw()
vertical_line2.SetLineStyle(ROOT.kDashed)
vertical_line2.SetLineColor(ROOT.kBlack)
vertical_line2.Draw()

# Make a logarithmic y axis
ROOT.gPad.SetLogy()

# Draw the legend
legend.SetTextSize(0.04)
legend.Draw()

# Disable the stats box 
hist_88Y.SetStats(0)

# Set axis titles and y axis range
hist_88Y.GetXaxis().SetTitle("Energy (MeV)")
hist_88Y.GetYaxis().SetTitle("Events /(MeV kton day)")
hist_88Y.GetYaxis().SetTitleSize(0.04)
hist_88Y.GetXaxis().SetTitleSize(0.04)
hist_88Y.GetYaxis().SetRangeUser(height_lower, height_upper)

canvas.SetLeftMargin(0.13)
canvas.SetRightMargin(0.05)
canvas.SetTopMargin(0.09)
canvas.SetBottomMargin(0.13)

canvas.Update()

# Set output file name and folder path for the PNG file to be saved
output_file_name = "total_smeared_spectrum.png"
folder_path = "figures"

file_path = os.path.join(folder_path, output_file_name)
canvas.SaveAs(file_path)


output_root_file = ROOT.TFile("total_smeared_energy_hist.root", "RECREATE")
hist_combined.Write()
output_root_file.Close()

# Clean up
del canvas
del hist_combined
for Isotope in IsotopeDict:
    exec(f"del hist_{Isotope}")
    exec(f"root_file_{Isotope}.Close()")