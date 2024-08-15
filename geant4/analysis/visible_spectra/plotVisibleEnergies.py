import ROOT
import os

'''
This script is used to plot the real, smeared and calibrated energy spectra for a given isotope. 
Can loop through all isotopes in the list Isotope_list, or just plot a single isotope. 
The script will save the plots as PNG files in the figures/visible folder.
'''

simulated_events_factor = 1e-7  # need to account for the number of simulated events in scaling the histograms

# Condition to draw all isotopes
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
    "134I"
    ]
else:
    Isotope_list = ["122I"]

bin_width = 0.05  # in MeV units
x_min = 0.5
x_max = 5 
n_bins = int((x_max - x_min)/bin_width)

 # Define y axis range
height_upper = 1e2
height_lower = 1e-5

# Loop over the list to study each isotope
for Isotope in Isotope_list:
    print(f"Plotting spectra for {Isotope}")

    # Here when we refer to old we mean the original real energies

    # Open the root file and get the tree for the different energies
    old_root_file = ROOT.TFile.Open(f"/data/xenon/toneill/rdecay01_edit_2_output/output_{Isotope}.root")
    old_total_tree = old_root_file.Get("totalEkin")
    new_root_file = ROOT.TFile.Open(f"/data/xenon/toneill/final_output/{Isotope}.root")
    new_total_tree = new_root_file.Get("totalEkin")

    # Create histograms of the energy spectrum, connect to tree data and draw it to a canvas
    old_hist = ROOT.TH1F("old_hist", f"{Isotope} Energy Spectrum", n_bins, x_min, x_max)
    smeared_hist = ROOT.TH1F("smeared_hist", "", n_bins, x_min, x_max)
    calibrated_hist = ROOT.TH1F("calibrated_hist", "", n_bins, x_min, x_max)

    old_total_tree.Draw("totalEkin>>old_hist")
    new_total_tree.Draw("smeared_energy>>smeared_hist")
    new_total_tree.Draw("smeared_calibrated_energy>>calibrated_hist")

    canvas = ROOT.TCanvas("canvas", f"{Isotope} energy spectrum", 1000, 600)

    # Scale the histograms
    old_hist.Scale(simulated_events_factor/bin_width)
    smeared_hist.Scale(simulated_events_factor/bin_width)
    calibrated_hist.Scale(simulated_events_factor/bin_width)

    # Set the histogram's line colors
    old_hist.SetLineColor(ROOT.kRed)
    smeared_hist.SetLineColor(ROOT.kBlue)
    calibrated_hist.SetLineColor(8)

    # Draw the histograms
    old_hist.Draw("HIST")
    smeared_hist.Draw("HIST SAME")
    calibrated_hist.Draw("HIST SAME")

    # Draw vertical line to show the calibration point
    vertical_line = ROOT.TLine(2.225, height_lower, 2.225, height_upper)
    vertical_line.SetLineStyle(ROOT.kDashed)
    vertical_line.SetLineColor(ROOT.kBlack)
    vertical_line.Draw()

    # Make a logarithmic y axis
    ROOT.gPad.SetLogy()

    # Create a legend, add entries, and draw it
    legend = ROOT.TLegend(0.7, 0.7, 0.95, 0.91)  # These are the coordinates of the legend
    legend.AddEntry(old_hist, f"Real Energy", "l")
    legend.AddEntry(smeared_hist, f" + Smearing", "l")
    legend.AddEntry(calibrated_hist, f" + Calibration", "l")
    legend.SetTextSize(0.04)
    legend.Draw()

    # Disable the stats box 
    old_hist.SetStats(0)

    # Set axis titles and y axis range
    old_hist.GetXaxis().SetTitle("Energy (MeV)")
    old_hist.GetYaxis().SetTitle("Events/MeV")
    old_hist.GetXaxis().SetTitleSize(0.04)
    old_hist.GetYaxis().SetTitleSize(0.04)
    old_hist.GetYaxis().SetRangeUser(height_lower, height_upper)

    # Optionally, set the margins if you want more control over the space around the graph
    canvas.SetLeftMargin(0.13)
    canvas.SetRightMargin(0.05)
    canvas.SetTopMargin(0.09)
    canvas.SetBottomMargin(0.13)

    canvas.Update()

    # Set output file name and folder path for the PNG file to be saved
    output_file_name = f"{Isotope}_visible_energy_spectrum.png"
    folder_path = "figures/visible"

    file_path = os.path.join(folder_path, output_file_name)
    canvas.SaveAs(file_path)

    # Clean up
    del old_hist
    del smeared_hist
    del calibrated_hist
    del canvas
    old_root_file.Close()
    new_root_file.Close()