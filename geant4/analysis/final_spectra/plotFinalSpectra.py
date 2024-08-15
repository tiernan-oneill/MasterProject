import ROOT
import os
import numpy as np
from array import array

'''
This script is used to make one plot: the total visible energy spectra of all of the isotopes (in black). 
The IsotopeDict dictionary is used to define the set of individual isotopes to plot, 
and the line colour for each. The script will save the plot as PNG files in the figures folder.
Using the 'comparison' boolean below with klg4 slightly changes the canvas dimensions and 
x range of the graph, to be better compared with the plot given by the KLG4 build.
'''

simulated_events_factor = 1e-7  # need to account for the number of simulated events in scaling the histograms

comparison_with_klg4 = True

# Set a dictionary of isotopes to plot together, and the line colour for each
# Also include total yield of each isotope for comparison (events per kton day in total)
IsotopeDict = {
    "88Y": ['kRed', 0.136],
    "118Sb": ['kBlue', 1.288],
    "122I": ['kOrange', 1.965],
    "124I": ['kMagenta', 1.654],
    "130I": ['kCyan', 1.188],
    "132I": ['kGreen', 0.427]}

# Define Y limits
height_upper = 1e2
height_lower = 1e-2

# Define histogram parameters
bin_width = 0.05  # in MeV units
x_min = 0.5
x_max = 4.75
n_bins = int((x_max - x_min)/bin_width)

# Create a legend
if comparison_with_klg4:
    legend = ROOT.TLegend(0.74, 0.53, 0.95, 0.91)  # These are the coordinates of the legend
else:
    legend = ROOT.TLegend(0.6, 0.55, 0.95, 0.91)
    legend.SetHeader("Isotope : Total Yield (/kton-day)")

for Isotope in IsotopeDict:
    print(f"Plotting {Isotope}")

    # Open the root files and get the tree for the total energies
    exec(f"root_file_{Isotope} = ROOT.TFile.Open(f'/data/xenon/toneill/final_output/{Isotope}.root')")
    exec(f"total_tree_{Isotope} = root_file_{Isotope}.Get('totalEkin')")

    # Create histograms of the energy spectrum, connect to tree data and draw it to a canvas
    if comparison_with_klg4:
        exec(f"hist_{Isotope} = ROOT.TH1F('hist_{Isotope}', '', n_bins, x_min, x_max)")
    else:
        exec(f"hist_{Isotope} = ROOT.TH1F('hist_{Isotope}', 'LL Isotope Visible Energy Spectra', n_bins, x_min, x_max)")
    exec(f"total_tree_{Isotope}.Draw('smeared_calibrated_energy>>hist_{Isotope}', '', 'goff')")

    # Set the histogram line color
    exec(f"hist_{Isotope}.SetLineColor(ROOT.{IsotopeDict[Isotope][0]})")

    # Add entries to legend
    if comparison_with_klg4:
        exec(f"legend.AddEntry(hist_{Isotope}, '{Isotope}'), 'l'")
    else:
        exec(f"legend.AddEntry(hist_{Isotope}, '{Isotope}: {IsotopeDict[Isotope][1]}'), 'l'")

print("Finalising plot...")

if comparison_with_klg4:
    canvas = ROOT.TCanvas("canvas", "Visible energy spectrum", 800, 600)
else:
    canvas = ROOT.TCanvas("canvas", "Visible energy spectrum", 1000, 600)

# Scale the histograms
for Isotope in IsotopeDict:
    yield_factor = IsotopeDict[Isotope][1]
    exec(f"hist_{Isotope}.Scale(yield_factor * simulated_events_factor/bin_width)")
root_file_combined = ROOT.TFile("../visible_spectra/total_visible_energy_hist.root", "READ")
hist_combined = root_file_combined.Get("hist_combined")

hist_combined.SetLineColor(ROOT.kBlack)
hist_combined.SetLineWidth(2)
hist_combined.Scale(10./9)  # our 32 isotopes only account for 90pc of the LL contribution

# Draw the histograms
hist_88Y.Draw('HIST')
for Isotope in IsotopeDict:
    if Isotope != "88Y":
        exec(f"hist_{Isotope}.Draw('HIST SAME')")
if comparison_with_klg4 == False:
    hist_combined.Draw('HIST SAME')
    legend.AddEntry(hist_combined, 'Total')

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
hist_88Y.GetXaxis().SetTitle("Visible Energy (MeV)")
hist_88Y.GetYaxis().SetTitle("Events /(MeV kton day)")
hist_88Y.GetXaxis().SetTitleSize(0.04)
hist_88Y.GetYaxis().SetTitleSize(0.04)
hist_88Y.GetYaxis().SetRangeUser(height_lower, height_upper)

canvas.SetLeftMargin(0.13)
canvas.SetRightMargin(0.05)
canvas.SetTopMargin(0.09)
canvas.SetBottomMargin(0.13)

canvas.Update()

# Set output file name and folder path for the PNG file to be saved
if comparison_with_klg4:
    output_file_name = "visible_E_tot_compare.png"
else:    
    output_file_name = "visible_E_tot_example.png"
folder_path = "figures"

file_path = os.path.join(folder_path, output_file_name)
canvas.SaveAs(file_path)

# Clean up
del canvas
del hist_combined
root_file_combined.Close()
for Isotope in IsotopeDict:
    exec(f"del hist_{Isotope}")
    exec(f"root_file_{Isotope}.Close()")