import ROOT
import numpy as np
import os
import math
from array import array

topMargin = 0.06
bottomMargin = 0.3
leftMargin = 0.16
rightMargin = 0.15

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

# Open the ROOT file (assuming all histograms are stored in the same file)
# signal = ("tta_mAlp-2GeV_ctau-1e0mm", "m_{a} = 2 GeV, c#tau_{a} = 1 mm")
signal = ("tta_mAlp-2GeV_ctau-1e1mm", "m_{a} = 2 GeV, c#tau_{a} = 1 cm")
# signal = ("tta_mAlp-2GeV_ctau-1e2mm", "m_{a} = 2 GeV, c#tau_{a} = 10 cm")

skim = "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5"
hist_path = "histograms_dimuonEffSFs_SRDimuons_ABCD"

filename=f"/data/dust/user/lrygaard/ttalps_cms/signals2018/{signal[0]}/{skim}/{hist_path}/histograms.root"
file = ROOT.TFile.Open(filename)

# Retrieve histograms from the file
dimuonCollection = "BestPFIsoDimuonVertex"
Lxy_DSA = file.Get(dimuonCollection+"_DSA_Lxy")
Lxy_Pat = file.Get(dimuonCollection+"_Pat_Lxy")
Lxy_PatDSA = file.Get(dimuonCollection+"_PatDSA_Lxy")
Lxy_tot = file.Get(dimuonCollection+"_Lxy")

include_overflow = False

x_max = 300
bin_edges = np.concatenate([
    np.arange(0, 50, 10), 
    np.arange(51, 130, 20),     
    np.arange(131, 180, 25),
    np.arange(181, 300, 40),
    [300], 
])
bin_edges = np.array(bin_edges, dtype=np.float64)
n_bins = len(bin_edges) - 1

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

def get_overflow(hist, x_max_):
    overflow = 0
    bin_max = hist.GetXaxis().FindBin(x_max_)
    for i in range(bin_max, hist.GetNbinsX() + 1):
        overflow += hist.GetBinContent(i)
    return overflow

def set_overflow(hist, overflow):
    total_events = hist.GetBinContent(hist.GetNbinsX()) + overflow
    hist.SetBinContent(hist.GetNbinsX(), total_events)
    return hist

overflow_DSA = get_overflow(Lxy_DSA, x_max)
overflow_Pat = get_overflow(Lxy_Pat, x_max)
overflow_PatDSA = get_overflow(Lxy_PatDSA, x_max)
overflow_tot = get_overflow(Lxy_tot, x_max)

Lxy_DSA_rebinned = Lxy_DSA.Rebin(n_bins, "Lxy_DSA_rebinned", bin_edges)
Lxy_Pat_rebinned = Lxy_Pat.Rebin(n_bins, "Lxy_Pat_rebinned", bin_edges)
Lxy_PatDSA_rebinned = Lxy_PatDSA.Rebin(n_bins, "Lxy_PatDSA_rebinned", bin_edges)
Lxy_tot_rebinned = Lxy_tot.Rebin(n_bins, "Lxy_tot_rebinned", bin_edges)

if include_overflow:
    Lxy_DSA_rebinned = set_overflow(Lxy_DSA_rebinned, overflow_DSA)
    Lxy_Pat_rebinned = set_overflow(Lxy_Pat_rebinned, overflow_Pat)
    Lxy_PatDSA_rebinned = set_overflow(Lxy_PatDSA_rebinned, overflow_PatDSA)
    Lxy_tot_rebinned = set_overflow(Lxy_tot_rebinned, overflow_tot)

eff_DSA = weighted_efficiency(Lxy_DSA_rebinned, Lxy_tot_rebinned)
eff_Pat = weighted_efficiency(Lxy_Pat_rebinned, Lxy_tot_rebinned)
eff_PatDSA = weighted_efficiency(Lxy_PatDSA_rebinned, Lxy_tot_rebinned)

eff_DSA.SetLineColor(ROOT.kBlue+1)
eff_DSA.SetMarkerColor(ROOT.kBlue+1)
# eff_DSA.SetLineColor(ROOT.kRed)
# eff_DSA.SetMarkerColor(ROOT.kRed)
eff_DSA.SetMarkerStyle(20)

eff_Pat.SetLineColor(ROOT.kGreen+1)
eff_Pat.SetMarkerColor(ROOT.kGreen+1)
eff_Pat.SetMarkerStyle(20)

# eff_PatDSA.SetLineColor(ROOT.kBlue)
# eff_PatDSA.SetMarkerColor(ROOT.kBlue)
eff_PatDSA.SetLineColor(ROOT.kOrange+1)
eff_PatDSA.SetMarkerColor(ROOT.kOrange+1)
eff_PatDSA.SetMarkerStyle(20)

hist0 = ROOT.TH1F("hist0", "hist0", n_bins, bin_edges)
hist0.GetXaxis().SetTitle("L_{xy} [cm]")
hist0.GetYaxis().SetTitle("Fraction of dimuons")
hist0.SetMaximum(1.5)
hist0.GetXaxis().SetLimits(0, 300)

# Set up a canvas to draw the plots
canvas = ROOT.TCanvas("canvas", "Efficiency Ratios", 800, 600)
canvas.SetLeftMargin(leftMargin)
canvas.SetBottomMargin(bottomMargin)
canvas.SetRightMargin(rightMargin)
canvas.SetTopMargin(topMargin)
canvas.SetTickx(0)
canvas.SetTicky(0)
canvas.SetBottomMargin(0.2)
canvas.SetTopMargin(topMargin + 0.03)

# Draw the TEfficiency objects on the same canvas
hist0.Draw("hist")  # Draw the first hist0 with axis
eff_PatDSA.Draw("P SAME") # Draw others on the same canvas
eff_Pat.Draw("P SAME")  
eff_DSA.Draw("P SAME")

canvas.Update()

legend = ROOT.TLegend(0.42, 0.76, 0.8, 0.9)
legend.AddEntry(eff_Pat, "Fraction of PAT-PAT dimuons", "lep")
legend.AddEntry(eff_PatDSA, "Fraction of PAT-DSA dimuons", "lep")
legend.AddEntry(eff_DSA, "Fraction of DSA-DSA dimuons", "lep")
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
posX_ = left + 0.045*(1-left-right) + 12
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
latex.DrawLatex(135, 1.15, "m_{a} = 2 GeV, c#tau_{a} = 1 cm")

# Update and save the canvas
canvas.Update()
canvas.Update()
if not os.path.exists("../plots/dimuon_Lxy_ratio"):
    os.makedirs("../plots/dimuon_Lxy_ratio")
overflow_str = ""
if include_overflow:
    overflow_str = "_overflow"
canvas.SaveAs(f"../plots/dimuon_Lxy_ratio/dimuon_ratios_2018_{signal[0]}{overflow_str}.pdf")

# Keep the canvas open in interactive mode
canvas.Draw()
