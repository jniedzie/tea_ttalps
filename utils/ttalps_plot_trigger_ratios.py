import ROOT
import numpy as np
import math
from array import array
import os

topMargin = 0.06
bottomMargin = 0.3
leftMargin = 0.16
rightMargin = 0.15

ROOT.gStyle.SetOptTitle(0)

variable_singleMu = "SingleMuonTriggerGenMuonFromALP_leadingPt"
variable_doubleMu = "DoubleMuonTriggerGenMuonFromALP_leadingPt"
variable_singleOrDoubleMu = "SingleorDoubleMuonTriggerGenMuonFromALP_leadingPt"
variable_notrigger = "NoExtraTriggerGenMuonFromALP_leadingPt"

skim = "skimmed_looseSemimuonic_v2_SR_noTrigger"
hist_path = "histograms_muonSFs_dsamuonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_dimuonEffSFs_jecSFs_SRDimuons_LooseNonLeadingMuonsVertexSegmentMatch"

# Open the ROOT file (assuming all histograms are stored in the same file)
# signal = ("tta_mAlp-2GeV_ctau-1e-5mm", "m_{a} = 2 GeV, c#tau_{a} = 10 nm")
signal = ("tta_mAlp-2GeV_ctau-1e0mm", "m_{a} = 2 GeV, c#tau_{a} = 1 m")
# signal = ("tta_mAlp-2GeV_ctau-1e1mm", "m_{a} = 2 GeV, c#tau_{a} = 1 cm")
# signal = ("tta_mAlp-2GeV_ctau-1e2mm", "m_{a} = 2 GeV, c#tau_{a} = 10 cm")
# signal = ("tta_mAlp-2GeV_ctau-1e3mm", "m_{a} = 2 GeV, c#tau_{a} = 1 m")
filename=f"/data/dust/user/lrygaard/ttalps_cms/signals2018/{signal[0]}/{skim}/{hist_path}/histograms.root"
file = ROOT.TFile.Open(filename)

x_max = 100

def weighted_efficiency(num_hist, den_hist):
    """
    Create a TGraphAsymmErrors representing efficiency for weighted histograms.
    """
    nbins = num_hist.GetNbinsX()
    x = []
    y = []
    ex_low = []
    ex_high = []
    ey_low = []
    ey_high = []

    for i in range(1, nbins+1):
        # Weighted numerator and denominator sums
        w_num = num_hist.GetBinContent(i)
        w_den = den_hist.GetBinContent(i)
        # Sum of squared weights for error propagation
        w_num2 = num_hist.GetBinError(i)**2
        w_den2 = den_hist.GetBinError(i)**2

        # Efficiency
        eff = w_num / w_den if w_den != 0 else 0

        # Weighted error (propagation)
        if w_den != 0:
            sigma_eff = math.sqrt(w_num2 / (w_den**2) + (w_num**2 * w_den2) / (w_den**4))
        else:
            sigma_eff = 0

        # Clip errors to [0,1] boundaries
        err_up = min(sigma_eff, 1 - eff)
        err_down = min(sigma_eff, eff)

        # Bin info
        bin_center = num_hist.GetBinCenter(i)
        bin_width = num_hist.GetBinWidth(i)

        # Fill arrays
        x.append(bin_center)
        y.append(eff)
        ex_low.append(bin_width/2)
        ex_high.append(bin_width/2)
        ey_low.append(err_down)
        ey_high.append(err_up)

    # Create the graph
    g = getattr(ROOT, "TGraphAsymmErrors")(len(x), array('d', x), array('d', y),
                                           array('d', ex_low), array('d', ex_high),
                                           array('d', ey_low), array('d', ey_high))
    return g

def get_overflow(hist):
    overflow = 0
    bin_max = hist.GetXaxis().FindBin(x_max)
    for i in range(bin_max, hist.GetNbinsX() + 1):
        overflow += hist.GetBinContent(i)
    return overflow

def set_overflow(hist, overflow):
    total_events = hist.GetBinContent(variable_singleMu.GetNbinsX()) + overflow
    hist.SetBinContent(variable_singleMu.GetNbinsX(), total_events)
    return hist


# Retrieve histograms from the file
variable_singleMu = file.Get(variable_singleMu)
variable_doubleMu = file.Get(variable_doubleMu)
variable_singleOrDoubleMu = file.Get(variable_singleOrDoubleMu)
variable_notrigger = file.Get(variable_notrigger)

if x_max == 100:
    bin_edges = np.concatenate([
        np.arange(3, 9, 6),  # Bins from 0 to 50 with bin width of 1
        np.arange(10, 50, 5),  # Bins from 0 to 50 with bin width of 1
        np.arange(50, 100, 10),  # Bins from 50 to 160 with bin width of 2
        [100]
    ])
elif x_max == 200:
    bin_edges = np.concatenate([
        np.arange(3, 9, 6),  # Bins from 0 to 50 with bin width of 1
        np.arange(10, 50, 5),  # Bins from 0 to 50 with bin width of 1
        np.arange(50, 100, 10),  # Bins from 50 to 160 with bin width of 2
        np.arange(101, 200, 20),  # Bins from 50 to 160 with bin width of 2
        [200]
    ])
else:
    print(f"Error: bin_edges not setup for {x_max}")
# Convert the numpy array to a ROOT array format
bin_edges = np.array(bin_edges, dtype=np.float64)
n_bins = len(bin_edges) - 1

# # Get overflow bin content
overflow_singleMu = get_overflow(variable_singleMu)
overflow_doubleMu = get_overflow(variable_doubleMu)
overflow_singleOrDoubleMu = get_overflow(variable_singleOrDoubleMu)
overflow_notrigger = get_overflow(variable_notrigger)

variable_singleMu = variable_singleMu.Rebin(n_bins, "variable_singleMu_rebinned", bin_edges)
variable_doubleMu = variable_doubleMu.Rebin(n_bins, "variable_doubleMu_rebinned", bin_edges)
variable_singleOrDoubleMu = variable_singleOrDoubleMu.Rebin(n_bins, "variable_singleOrDoubleMu_rebinned", bin_edges)
variable_notrigger = variable_notrigger.Rebin(n_bins, "variable_notrigger_rebinned", bin_edges)

variable_singleMu = set_overflow(variable_singleMu, overflow_singleMu)
variable_doubleMu = set_overflow(variable_doubleMu, overflow_doubleMu)
variable_singleOrDoubleMu = set_overflow(variable_singleOrDoubleMu, overflow_singleOrDoubleMu)
variable_notrigger = set_overflow(variable_notrigger, overflow_notrigger)

ratio_hist_singleMu = weighted_efficiency(variable_singleMu, variable_notrigger)
ratio_hist_doubleMu = weighted_efficiency(variable_doubleMu, variable_notrigger)
ratio_hist_singleOrDoubleMu = weighted_efficiency(variable_singleOrDoubleMu, variable_notrigger)

# Set marker style and color for each plot
ratio_hist_singleMu.SetMaximum(1.5)
ratio_hist_singleMu.SetMinimum(0)
ratio_hist_singleMu.GetXaxis().SetLimits(0, 100)
ratio_hist_singleMu.GetXaxis().SetTitle("p_{T} of leading gen muon from ALP [GeV]")
ratio_hist_singleMu.GetYaxis().SetTitle("#epsilon_{trigger}")
ratio_hist_singleMu.GetXaxis().SetTitleSize(0.04)
ratio_hist_singleMu.GetXaxis().SetLabelSize(0.04)
ratio_hist_singleMu.GetXaxis().SetTitleOffset(1.7)
ratio_hist_singleMu.GetYaxis().SetTitleSize(0.03)
ratio_hist_singleMu.GetYaxis().SetLabelSize(0.06)
ratio_hist_singleMu.GetYaxis().SetTitleOffset(2.0)
ratio_hist_singleMu.SetLineColor(ROOT.kMagenta-7)
ratio_hist_singleMu.SetMarkerColor(ROOT.kMagenta-7)
ratio_hist_singleMu.SetMarkerStyle(20)
ratio_hist_doubleMu.SetLineColor(ROOT.kOrange+1)
ratio_hist_doubleMu.SetMarkerColor(ROOT.kOrange+1)
ratio_hist_doubleMu.SetMarkerStyle(21)
ratio_hist_singleOrDoubleMu.SetLineColor(ROOT.kGreen+1)
ratio_hist_singleOrDoubleMu.SetMarkerColor(ROOT.kGreen+1)
ratio_hist_singleOrDoubleMu.SetMarkerStyle(22)

# Set up a canvas to draw the plots
canvas = ROOT.TCanvas("canvas", "Ratio histogram", 800, 600)
canvas.SetLeftMargin(leftMargin)
canvas.SetBottomMargin(bottomMargin)
canvas.SetRightMargin(rightMargin)
canvas.SetTopMargin(topMargin)
canvas.SetTickx(0)
canvas.SetTicky(0)
canvas.SetBottomMargin(0.2)
canvas.SetTopMargin(topMargin + 0.03)

# Draw the TEfficiency objects on the same canvas
ratio_hist_singleMu.Draw("AP")
ratio_hist_doubleMu.Draw("P same")
ratio_hist_singleOrDoubleMu.Draw("P same")

canvas.Update()

# Add a legend to describe the plots
legend = ROOT.TLegend(0.4, 0.76, 0.82, 0.85)
legend.AddEntry(ratio_hist_singleMu, "SingleMuon")
legend.AddEntry(ratio_hist_doubleMu, "DoubleMuon")
legend.AddEntry(ratio_hist_singleOrDoubleMu, "SingleORDoubleMuon")
legend.SetBorderSize(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.Draw()

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)
latex.SetTextFont(42)
latex.SetTextAlign(31)
top = canvas.GetTopMargin()
right = canvas.GetRightMargin()
latex.SetTextSize(0.4*top)
lumi = f"{59830. / 1000.0:.1f} fb^{{-1}}"
lumiText = lumi + " (13 TeV)"
latex.DrawLatex(1-right, 1-top+0.02, lumiText)

left = canvas.GetLeftMargin()
bottom = canvas.GetBottomMargin()
posX_ = left + 0.045*(1-left-right) + 5
posY_ = 1-top - 0.070*(1-bottom) + 0.61
latex = ROOT.TLatex()
latex.SetTextFont(61)
latex.SetTextSize(0.55*top)
latex.SetTextAlign(13)
latex.DrawLatex(posX_, posY_, "CMS")

latex = ROOT.TLatex()
latex.SetTextFont(52)
latex.SetTextAlign(13)
extraTextSize = 0.76 * 0.55*top
latex.SetTextSize(0.76*0.55*top)
latex.DrawLatex(posX_, posY_ - 0.1 , "Preliminary")

latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextAlign(13)
extraTextSize = 0.76 * 0.55*top
latex.SetTextSize(0.76*0.55*top)
posX_ = 50
latex.DrawLatex(posX_, posY_, signal[1])

# Update and save the canvas
canvas.Update()
if not os.path.exists("../plots/trigger_ratios"):
    os.makedirs("../plots/trigger_ratios")
canvas.SaveAs(f"../plots/trigger_ratios/ratio_hist_trigger_{signal[0]}.pdf")

# Keep the canvas open in interactive mode
canvas.Draw()
