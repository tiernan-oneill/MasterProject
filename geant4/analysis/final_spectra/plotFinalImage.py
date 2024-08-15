import ROOT
import os
import numpy as np

'''
Script to create a plot comparing the KLG4 visible energy spectrum with three
of my G4 energy spectra: the original, the smeared, and the calibrated (visible).
The KLG4 data is loaded in from a text file. The G4 data is loaded in from the 
respective total histogram ROOT files.
The script creates a main plot showing the three G4 histograms and the KLG4 data,
with a subplot showing the percentage difference between the KLG4 data and the G4
visible energy data.
This is saved as a PNG file.
'''

# Define Y limits of plot
height_upper = 1e2
height_lower = 1e-2

# Define histogram parameters
bin_width = 0.05  # in MeV units
x_min = 0.5
x_max = 4.8
n_bins = int((x_max - x_min)/bin_width)

# Create a ROOT histogram
root_file_combined_new = ROOT.TFile("../visible_spectra/total_visible_energy_hist.root", "READ")
hist_combined_new = root_file_combined_new.Get("hist_combined")
root_file_combined_mid = ROOT.TFile("../visible_spectra/total_smeared_energy_hist.root", "READ")
hist_combined_mid = root_file_combined_mid.Get("hist_combined")
root_file_combined_old = ROOT.TFile("../real_spectra/total_real_energy_hist.root", "READ")
hist_combined_old = root_file_combined_old.Get("hist_combined")

canvas = ROOT.TCanvas("canvas", "Isotope Energy Spectrum", 800, 600)

hist_combined_new.SetLineColor(ROOT.kRed)
hist_combined_old.SetLineColor(ROOT.kBlue)
hist_combined_mid.SetLineColor(ROOT.kOrange)

# Scale the histograms to compare with the KLG4 data 
# Our histograms contain about 90pc of the LL isotope contribution
hist_combined_new.Scale(10./9)
hist_combined_mid.Scale(10./9)
hist_combined_old.Scale(10./9)

# Load in the KLG4 spectrum data
y_values = np.loadtxt('../klg4_y_values.txt')
x_values = np.arange(x_min, x_max, bin_width)

# Create a TGraph to plot the KLG4 data
graph = ROOT.TGraph(len(x_values), x_values, y_values)
graph.SetLineColor(ROOT.kBlack)
graph.SetLineWidth(2)

# Calculate the difference between TGraph and Histogram
diff_hist = ROOT.TH1F("diff_hist", "Difference Between KLG4 and G4 Visible Energies", n_bins, x_min, x_max)
for i in range(len(y_values)):
    bin_content = hist_combined_new.GetBinContent(i + 1)
    diff_value = y_values[i] - bin_content
    diff_percent = (diff_value / bin_content) * 100
    diff_hist.SetBinContent(i + 1, diff_percent)

# Create a pad for the main plot
pad1 = ROOT.TPad("pad1", "Pad for Main Plot", 0, 0.3, 1, 1.0)
pad1.Draw()
pad1.cd()

hist_combined_old.Draw('HIST')
hist_combined_mid.Draw('HIST SAME')
hist_combined_new.Draw('HIST SAME')

legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
legend.AddEntry(hist_combined_old, 'G4 Real Energy', 'l')
legend.AddEntry(hist_combined_mid, 'G4 Smeared Energy', 'l')
legend.AddEntry(hist_combined_new, 'G4 Visible Energy', 'l')

# Draw vertical lines to show the region of interest for 0vbb
vertical_line1 = ROOT.TLine(2.35, height_lower, 2.35, height_upper)
vertical_line2 = ROOT.TLine(2.7, height_lower, 2.7, height_upper)
vertical_line1.SetLineStyle(ROOT.kDashed)
vertical_line1.SetLineColor(ROOT.kBlack)
vertical_line1.Draw()
vertical_line2.SetLineStyle(ROOT.kDashed)
vertical_line2.SetLineColor(ROOT.kBlack)
vertical_line2.Draw()

graph.Draw('SAME')
legend.AddEntry(graph, 'KLG4 Visible Energy', 'l')

# Make a logarithmic y axis
ROOT.gPad.SetLogy()

# Draw the legend
legend.SetTextSize(0.05)
legend.Draw()

# Disable the stats box 
hist_combined_old.SetStats(0)
hist_combined_old.SetTitle("")

hist_combined_old.GetYaxis().SetTitle("Events /(MeV kton day)")
hist_combined_old.GetYaxis().SetTitleSize(0.05)
hist_combined_old.GetYaxis().SetRangeUser(height_lower, height_upper)

# remove x axis labels for the main plot
hist_combined_old.GetXaxis().SetLabelSize(0)

# Go back to the main canvas and create a pad for the subplot
canvas.cd()
pad2 = ROOT.TPad("pad2", "Pad for Subplot", 0, 0.05, 1, 0.35)
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad2.Draw()
pad2.cd()

# Draw the difference plot in the subplot
diff_hist.SetLineColor(ROOT.kGreen)
diff_hist.Draw()
diff_hist.SetStats(0)

# Adjust axis labels for the subplot
diff_hist.GetXaxis().SetTitle("Energy (MeV)")
diff_hist.GetYaxis().SetTitle("Percentage")
diff_hist.GetXaxis().SetTitleSize(0.12)
diff_hist.GetXaxis().SetLabelSize(0.1)

diff_hist.GetYaxis().SetTitleSize(0.1)
diff_hist.GetYaxis().SetTitleOffset(0.5)
diff_hist.GetYaxis().SetLabelSize(0.07)

ROOT.gStyle.SetTitleW(0.5) # title width
ROOT.gStyle.SetTitleH(0.1) # title height

canvas.Update()

# Set output file name and folder path for the PNG file to be saved
output_file_name = "final_image.png"
folder_path = "figures"

file_path = os.path.join(folder_path, output_file_name)
canvas.SaveAs(file_path)

# Clean up
del canvas
del hist_combined_new
del hist_combined_mid
del hist_combined_old
del diff_hist
root_file_combined_new.Close()
root_file_combined_mid.Close()
root_file_combined_old.Close()