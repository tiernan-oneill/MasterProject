import ROOT
import os
import numpy as np

'''
Script plots the beta spectra for 100Rh specifically.
Separate from the other script to allow for more customization.
'''

Isotope = "100Rh"

x_min = 0
n_bins = 100

height_upper = 0.22e-3

# Open the root file and get the tree for the electron/positron kinetic energy and neutrino kinetic energy
root_file = ROOT.TFile.Open(f"/data/xenon/toneill/rdecay01_edit_1_output/output_{Isotope}.root")
e_tree = root_file.Get("eEkin")
v_tree = root_file.Get("vEkin")

# Open the .dat file for reading ENSDF data
dat_file = open(f"beta_data/{Isotope}.dat", 'r')

# Initialize lists to store data
x_values = []
y_values = []

# Read and parse the data from the file
for line in dat_file:
    # Assuming the data is space-separated
    data = line.strip().split()

    # Convert the strings to floats, first column is Energy (keV), second is dN/dE
    x_values.append(float(data[0]))
    y_values.append(float(data[1]))

# Close the data file
dat_file.close()

x_values = np.array(x_values, dtype='float64')
y_values = np.array(y_values, dtype='float64')

n_points = len(x_values)
graph = ROOT.TGraph(n_points, x_values, y_values)
graph.SetLineColor(ROOT.kBlue)

# Loop over all entries in the tree to get maximum value
max_value = 0.0
for entry in e_tree:
    # Access the value of the branch you're interested in
    value = entry.eEkin
    # Update the maximum value if the current value is larger
    if value > max_value:
        max_value = value
x_max = max_value*1.05

# Create a histogram of the beta spectrum and draw it to a canvas
histogram = ROOT.TH1F("histogram", f"{Isotope} Beta Spectrum; Energy (keV); dN/dE", n_bins, x_min, x_max)
canvas = ROOT.TCanvas("canvas", f"{Isotope} beta spectrum", 1000, 600)
e_tree.Draw("eEkin>>histogram")

# Set the histogram's line color to red and disable the statistics box
histogram.SetLineColor(ROOT.kRed)
histogram.SetStats(0)

# Change the histogram's line width
histogram.SetLineWidth(2)

# Normalize the histogram with the specified factor (branching ratio)
#beta_particle_factor = 1
beta_particle_factor = e_tree.GetEntries()/v_tree.GetEntries()

histogram.Scale(beta_particle_factor/histogram.Integral(), "width")

# Draw the histogram
histogram.Draw("hist")

# Draw the TGraph
graph.Draw("same l")

# Create a TMultiGraph to store the horizontal lines to be drawn
multi_graph = ROOT.TMultiGraph()

# Create an array of y-values to draw 10 horizontal lines
yValues = np.linspace(0, height_upper, 10)

# Loop over the y-values
for yValue in yValues:
    line = ROOT.TGraph(2)
    line.SetPoint(0, x_min, yValue)
    line.SetPoint(1, x_max, yValue)

    line.SetLineColor(ROOT.kGray)

    # Set line style to dashed
    line.SetLineStyle(2)

    # Add the line to the TMultiGraph
    multi_graph.Add(line)

# Now draw the TMultiGraph
multi_graph.Draw()

# Create a legend, add entries, and draw it
legend = ROOT.TLegend(0.7, 0.7, 0.95, 0.91)  # These are the coordinates of the legend
legend.AddEntry(histogram, "Geant4", "l")
legend.AddEntry(graph, "ENSDF data", "l")
legend.SetTextSize(0.04)
legend.Draw()

histogram.GetXaxis().SetTitleSize(0.04)
histogram.GetYaxis().SetTitleSize(0.04)
histogram.GetYaxis().SetRangeUser(0, height_upper)

# Optionally, set the margins if you want more control over the space around the graph
canvas.SetLeftMargin(0.13)
canvas.SetRightMargin(0.05)
canvas.SetTopMargin(0.09)
canvas.SetBottomMargin(0.13)

# Set output file name and folder path for the PNG file to be saved
output_file_name = f"{Isotope}_beta_spectrum.png"
folder_path = "figures"

file_path = os.path.join(folder_path, output_file_name)
canvas.SaveAs(file_path)

# Clean up
del histogram
del canvas
root_file.Close()