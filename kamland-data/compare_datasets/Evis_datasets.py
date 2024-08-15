import ROOT

'''
This script studies the energy spectra of these different data sets,
and creates a PNG image of this.
'''

# Load in root file
root_file_all =  ROOT.TFile.Open("../AllDataZen800Single-DoubleBeta.root")
root_file_old =  ROOT.TFile.Open("../FileFromArticleSingle-DoubleBeta.root")

# Get tree data
tree_all = root_file_all.Get("nt")
tree_old = root_file_old.Get("nt")

# Create histogram parameters
bin_width = 0.05  # in MeV units
x_min = 0.5
x_max = 5
num_of_bins = int((x_max - x_min)/bin_width)

# Define Y limits
height_lower = 1e2
height_upper = 1e8

# Create histograms
hist1 = ROOT.TH1F("hist1", "KamLAND-Zen 800 Energy Spectrum", num_of_bins, x_min, x_max)
hist2 = ROOT.TH1F("hist2", "", num_of_bins, x_min, x_max)
hist3 = ROOT.TH1F("hist3", "", num_of_bins, x_min, x_max)

# Define veto criterion
unixtime_data = "unixtime > 1626910271"  # only include events after the original set of data

# Select the relevant branch data for each histogram
tree_old.Draw("Evis >> hist1", "", "goff")   # goff means no graphics output
tree_all.Draw("Evis >> hist2", unixtime_data, "goff")
tree_all.Draw("Evis >> hist3", "", "goff")

# Scale histograms
hist1.Scale(1./bin_width)
hist2.Scale(1./bin_width)
hist3.Scale(1./bin_width)

# Create canvas for plotting and draw histograms to it
canvas = ROOT.TCanvas('c1', 'canvas title', 0, 0, 1000, 700)  # last two parameters are graph width and height respectively
hist1.Draw('HIST')
hist2.Draw('HIST SAME')
hist3.Draw('HIST SAME')

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
hist1.SetLineColor(ROOT.kRed)
hist2.SetLineColor(ROOT.kBlue)
hist3.SetLineColor(ROOT.kBlack)

# Create a legend
legend = ROOT.TLegend(0.66, 0.7, 0.95, 0.91)
legend.AddEntry(hist1, "Data from Article", "L")
legend.AddEntry(hist2, "Data after Article", "L")
legend.AddEntry(hist3, "All Data", "L")
legend.SetTextSize(0.04)
legend.Draw()

# Disable the stats box 
hist1.SetStats(0)

# Set axis titles and y axis range
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

canvas.Update()

# Save the image
canvas.SaveAs("figures/Evis_datasets_image.png")

# Clean up
del hist1
del hist2
del hist3
del canvas
root_file_all.Close()
root_file_old.Close()