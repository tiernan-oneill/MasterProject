import ROOT
import os

'''
This script is used to plot the real energy spectra of electrons, positrons, gammas, and (optionally) 
the total energy for a given isotope. Can loop through all isotopes in the list Isotope_list, or
just plot a single isotope. The script will save the plots as PNG files in the figures/real folder.
'''

simulated_events_factor = 1e-7  # need to account for the number of simulated events in scaling the histograms

# Condition to also draw combined (total) energy spectrum
draw_total_energy_spectrum = False

# Condition to draw all isotopes or just a subset given below
draw_all_isotopes = True

# Set a list of isotope names
if(draw_all_isotopes):
    Isotope_list = [
    "88Y",
    "90m1Zr",
    "90Nb",
    "96Tc",
    "98Rh",
    "100Rh",
    "104Ag",
    "104m1Ag",
    "107In",
    "108In",
    "109Sn",
    "110In",
    "110m1In",
    "113Sb",
    "114Sb",
    "115Sb",
    "115Te",
    "116Sb",
    "117Te",
    "118Sb",
    "119I",
    "120I",
    "121Xe",
    "122I",
    "124I",
    "124Sb",
    "125Cs",
    "126Cs",
    "128Cs",
    "130I",
    "132I", 
    "134I"]
else:
    Isotope_list = [ "114Sb", "128Cs"]

bin_width = 0.05  # in MeV units
x_min = 0.5
x_max = 5 
n_bins = int((x_max - x_min)/bin_width)

# Define Y limits of plots
height_upper = 1e2
height_lower = 1e-6

# Loop over the list to study each isotope
for Isotope in Isotope_list:
    print(f"Plotting {Isotope} energy spectrum")

    # Open the root file and get the tree for the different energies
    root_file = ROOT.TFile.Open(f"/data/xenon/toneill/rdecay01_edit_2_output/output_{Isotope}.root")
    electron_tree = root_file.Get("electron")
    positron_tree = root_file.Get("positron")
    gamma_tree = root_file.Get("gamma")
    total_tree = root_file.Get("totalEkin")

    # Create histograms of each particle energy spectrum, connect to tree data and draw it to a canvas
    hist1 = ROOT.TH1F("hist1", f"{Isotope} Real Energy Spectrum", n_bins, x_min, x_max)
    hist2 = ROOT.TH1F("hist2", "", n_bins, x_min, x_max)
    hist3 = ROOT.TH1F("hist3", "", n_bins, x_min, x_max)
    hist4 = ROOT.TH1F("hist4", "", n_bins, x_min, x_max)

    electron_tree.Draw("electronEkin>>hist1")
    positron_tree.Draw("positronEkin>>hist2")
    gamma_tree.Draw("gammaEkin>>hist3")
    total_tree.Draw("totalEkin>>hist4")

    canvas = ROOT.TCanvas("canvas", f"{Isotope} energy spectrum", 1000, 600)

    # Scale the histograms
    hist1.Scale(simulated_events_factor/bin_width)
    hist2.Scale(simulated_events_factor/bin_width)
    hist3.Scale(simulated_events_factor/bin_width)
    hist4.Scale(simulated_events_factor/bin_width)

    # Set the histogram's line colors
    hist1.SetLineColor(ROOT.kRed)
    hist2.SetLineColor(ROOT.kBlue)
    hist3.SetLineColor(8)  # Dark green
    hist4.SetLineColor(ROOT.kBlack)

    # Draw the histograms
    hist1.Draw('HIST')
    hist2.Draw("HIST SAME")
    hist3.Draw("HIST SAME")
    if(draw_total_energy_spectrum):
        hist4.Draw("HIST SAME")

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

    # Create a legend, add entries, and draw it
    legend = ROOT.TLegend(0.7, 0.7, 0.95, 0.91)  # These are the coordinates of the legend
    legend.AddEntry(hist1, "Electrons", "l")
    legend.AddEntry(hist2, "Positrons", "l")
    legend.AddEntry(hist3, "Gammas", "l")
    if(draw_total_energy_spectrum):
        legend.AddEntry(hist4, "Total", "l")
    legend.SetTextSize(0.04)
    legend.Draw()

    # Disable the stats box 
    hist1.SetStats(0)

    # Set axis titles and sizes and y axis range
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
    output_file_name = f"{Isotope}_energy_spectrum.png"
    folder_path = "figures/real"

    file_path = os.path.join(folder_path, output_file_name)
    canvas.SaveAs(file_path)

    # Clean up
    del hist1
    del hist2
    del hist3
    del hist4
    del canvas
    root_file.Close()