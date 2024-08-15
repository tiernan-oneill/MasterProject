import ROOT
import os

'''
Script to plot the gamma energy spectrum of 122I used in thesis.
It will save the plot as a PNG file in the figures folder.
'''

simulated_events_factor = 1e-7

bin_width = 0.05  # in MeV units
x_min = 0.5
x_max = 5 
n_bins = int((x_max - x_min)/bin_width)

# Define Y limits of plots
height_upper = 1e2
height_lower = 1e-5

Isotope = "122I"

# Open the root file and get the tree for the different energies
root_file = ROOT.TFile.Open(f"/data/xenon/toneill/rdecay01_edit_2_output/output_{Isotope}.root")
gamma_tree = root_file.Get("gamma")

# Create histograms of the energy spectrum, connect to tree data and draw it to a canvas
hist1 = ROOT.TH1F("hist1", f"{Isotope} Gamma Energy Spectrum", n_bins, x_min, x_max)

gamma_tree.Draw("gammaEkin>>hist1")

canvas = ROOT.TCanvas("canvas", f"{Isotope} gamma energy spectrum", 1000, 600)

# Scale the histograms
hist1.Scale(simulated_events_factor/bin_width)

# Set the histogram's line colors
hist1.SetLineColor(ROOT.kBlue)

# Draw the histogram
hist1.Draw('HIST')

# Make a logarithmic y axis
ROOT.gPad.SetLogy()

# Create a legend, add entries, and draw it
legend = ROOT.TLegend(0.7, 0.7, 0.95, 0.91)  # These are the coordinates of the legend
legend.AddEntry(hist1, "Gammas", "l")
legend.SetTextSize(0.04)
legend.Draw()

# Disable the stats box 
hist1.SetStats(0)

# Set axis titles and y axis range
hist1.GetXaxis().SetTitle("Real Energy (MeV)")
hist1.GetYaxis().SetTitle("Events/MeV")
hist1.GetXaxis().SetTitleSize(0.04)
hist1.GetYaxis().SetTitleSize(0.04)
hist1.GetYaxis().SetRangeUser(height_lower, height_upper)

# Optionally, set the margins if you want more control over the space around the graph
canvas.SetLeftMargin(0.13)
canvas.SetRightMargin(0.05)
canvas.SetTopMargin(0.09)
canvas.SetBottomMargin(0.13)

canvas.Update()

# Set output file name and folder path for the PNG file to be saved
output_file_name = f"122I_gamma.png"
folder_path = "figures"

file_path = os.path.join(folder_path, output_file_name)
canvas.SaveAs(file_path)

# Clean up
del hist1
del canvas
root_file.Close()