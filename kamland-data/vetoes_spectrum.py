import ROOT
import numpy as np

'''
This script studies the energy spectrum of double beta decay candidates from the 800 run.
It plots the entire spectrum along with some vetoes applied to the data.
The image is saved as a PNG
'''

# Load in root file
root_file =  ROOT.TFile("AllDataZen800Single-DoubleBeta.root")

# Get tree data
tree = root_file.Get("nt")

# Create histogram parameters
bin_width = 0.05  # in MeV units
x_min = 0.5
x_max = 5
num_of_bins = int((x_max - x_min)/bin_width)

# Define Y limits
height_lower = 1e0
height_upper = 1e7

# Create histograms
hist1 = ROOT.TH1F("hist1", "KamLAND-Zen 800 Energy Spectrum", num_of_bins, x_min, x_max)
hist2 = ROOT.TH1F("hist2", "All vetoes", num_of_bins, x_min, x_max)
hist3 = ROOT.TH1F("hist3", "r < 160cm", num_of_bins, x_min, x_max)
hist4 = ROOT.TH1F("hist4", "All except LL and r veto", num_of_bins, x_min, x_max)
hist5 = ROOT.TH1F("hist5", "All except PMT and LL and r veto", num_of_bins, x_min, x_max)
gauss_hist = ROOT.TH1F("gauss_hist", "0vbb signal", 10, 2.35, 2.7)

# Fill the 0vbb histogram with Gaussian-distributed data
for _ in range(10000):
    gauss_hist.Fill(ROOT.gRandom.Gaus(2.525, 0.09))
gauss_hist.Scale(2./gauss_hist.Integral())

# Obtain relevant energy data with certain veto/energy or radius conditions
energy_criterion = "Evis > 0.5 && Evis < 5"  # in MeV
radius_criterion = "r < 160"  # in cm
total_veto_criterion = "Dveto==0 && Mveto==0 && MFveto==0 && MoGveto==0 && C10veto==0 && Xe137veto==0 && \
                LLveto_3D==0 && Showerveto==0 && Rveto==0 && Rnveto==0 && Pileupveto==0"
spallation_veto_criterion = "Dveto==0 && MFveto==0 && MoGveto==0 && \
                Rveto==0 && Rnveto==0 && Pileupveto==0"
radon_spallation_veto_criterion = "Dveto==0 && MFveto==0 && MoGveto==0 && \
                Rveto==0 && Pileupveto==0"
total_criterion = energy_criterion + "&&" + radius_criterion + "&&" + total_veto_criterion

# Select the relevant branch data for each histogram
tree.Draw("Evis >> hist1", "", "goff")  # goff means no graphical output
tree.Draw("Evis >> hist2", total_criterion, "goff")
tree.Draw("Evis >> hist3", energy_criterion + "&&" + radon_spallation_veto_criterion, "goff")
tree.Draw("Evis >> hist4", energy_criterion + "&&" + radius_criterion + "&&" + spallation_veto_criterion, "goff")
tree.Draw("Evis >> hist5", energy_criterion + "&&" + radius_criterion + "&&" + radon_spallation_veto_criterion, "goff")

# Scale histograms to the bin width
hist1.Scale(1./bin_width)
hist2.Scale(1./bin_width)
hist3.Scale(1./bin_width)
hist4.Scale(1./bin_width)
hist5.Scale(1./bin_width)
gauss_hist.Scale(1./bin_width)

# Create canvas for plotting and draw histograms to it
canvas = ROOT.TCanvas('c1', 'canvas title', 0, 0, 1000, 600)  # last two parameters are graph width and height respectively
hist1.Draw('HIST')
hist2.Draw('HIST SAME')
hist3.Draw('HIST SAME')
hist4.Draw('HIST SAME')
hist5.Draw('HIST SAME')
gauss_hist.Draw('HIST SAME')

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

# Edit the histogram colours
hist1.SetLineColor(ROOT.kBlack)
hist2.SetLineColor(ROOT.kRed)
hist3.SetLineColor(8)  # Dark green
hist4.SetLineColor(ROOT.kBlue)
hist5.SetLineColor(ROOT.kMagenta)
gauss_hist.SetLineColor(ROOT.kCyan)
gauss_hist.SetLineWidth(3)

# Create a legend
legend = ROOT.TLegend(0.65, 0.6, 0.95, 0.91)  # these are the legend coordinates
legend.AddEntry(gauss_hist, "0vbb", "L")
legend.AddEntry(hist1, "Original Data", "L")
legend.AddEntry(hist2, "All vetoes", "L")
legend.AddEntry(hist4, "+ Spallation Events", "L")
legend.AddEntry(hist5, "+ Radon Events", "L")
legend.AddEntry(hist3, "+ Fiducial Events", "L")
legend.SetTextSize(0.04)
legend.Draw()

# Disable the stats box 
hist1.SetStats(0)

# Set axis titles and font size, and the y axis range
hist1.GetXaxis().SetTitle("Visible Energy (MeV)")
hist1.GetYaxis().SetTitle("Events/MeV")
hist1.GetXaxis().SetTitleSize(0.04)
hist1.GetYaxis().SetTitleSize(0.04)
hist1.GetYaxis().SetRangeUser(height_lower, height_upper)

# Optionally, set the margins if you want more control over the space around the graph
canvas.SetLeftMargin(0.13)
canvas.SetRightMargin(0.05)
canvas.SetTopMargin(0.09)
canvas.SetBottomMargin(0.13)

# Set title width and height
ROOT.gStyle.SetTitleW(0.5)
ROOT.gStyle.SetTitleH(0.1)

canvas.Update()

# Save the image
canvas.SaveAs("vetoes_spectrum_image.png")

# Clean up
del hist1
del hist2
del hist3
del hist4
del hist5
del gauss_hist
del canvas
root_file.Close()
