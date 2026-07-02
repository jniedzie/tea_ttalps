import ROOT
import numpy as np
import os
import math
from array import array

from ttalps_luminosities import get_luminosity

topMargin = 0.06
bottomMargin = 0.3
leftMargin = 0.16
rightMargin = 0.15

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

# Open the ROOT file (assuming all histograms are stored in the same file)
# signal = ("tta_mAlp-2GeV_ctau-1e0mm", "m_{a} = 2 GeV, c#tau_{a} = 1 mm")
# signal = ("tta_mAlp-2GeV_ctau-1e1mm", "m_{a} = 2 GeV, c#tau_{a} = 1 cm")
signal = ("tta_mAlp-2GeV_ctau-1e2mm", "m_{a} = 2 GeV, c#tau_{a} = 10 cm")

# signal = ("tta_mAlp-12GeV_ctau-1e0mm", "m_{a} = 12 GeV, c#tau_{a} = 1 mm")
# signal = ("tta_mAlp-12GeV_ctau-1e1mm", "m_{a} = 12 GeV, c#tau_{a} = 1 cm")
# signal = ("tta_mAlp-12GeV_ctau-1e2mm", "m_{a} = 12 GeV, c#tau_{a} = 10 cm")

# skim = "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5"
skim = "skimmed_looseSemimuonic_v3_SR"
# hist_path = "histograms_dimuonEffSFs_SRDimuons_ABCD"
# hist_path = "histograms_SRDimuons_ABCD_ANv2"
hist_path = "histograms_SRDimuons_ABCD_ANv5"

years = ["2016preVFP","2016postVFP","2017","2018",]
# years = ["2016preVFP","2016postVFP","2017","2018","2022preEE","2022postEE","2023preBPix","2023postBPix",]
year_str = ""
Lxy_DSA = None
Lxy_Pat = None
Lxy_PatDSA = None
Lxy_tot = None
dimuonCollection = "BestPFIsoDimuonVertex"
include_run3 = False

for year in years:
    year_str += year
    if "2022" in year or "2023" in year:
        include_run3 = True
    filename=f"/data/dust/user/lrygaard/ttalps_cms/signals{year}/{signal[0]}/{skim}/{hist_path}/histograms.root"
    file = ROOT.TFile.Open(filename)

    h_DSA = file.Get(dimuonCollection+"_DSA_Lxy")
    h_Pat = file.Get(dimuonCollection+"_Pat_Lxy")
    h_PatDSA = file.Get(dimuonCollection+"_PatDSA_Lxy")
    h_tot = file.Get(dimuonCollection+"_Lxy")

    luminosity = get_luminosity(year)
    h_cutflow = file.Get("cutFlow")
    initial_weight = h_cutflow.GetBinContent(1)
    h_DSA.Scale(luminosity / initial_weight)
    h_Pat.Scale(luminosity / initial_weight)
    h_PatDSA.Scale(luminosity / initial_weight)
    h_tot.Scale(luminosity / initial_weight)
    
    if Lxy_tot is None:
        Lxy_DSA = h_DSA.Clone(f"Lxy_DSA_{year}")
        Lxy_DSA.SetDirectory(0)
        Lxy_Pat = h_Pat.Clone(f"Lxy_Pat_{year}")
        Lxy_Pat.SetDirectory(0)
        Lxy_PatDSA = h_PatDSA.Clone(f"Lxy_PatDSA_{year}")
        Lxy_PatDSA.SetDirectory(0)
        Lxy_tot = h_tot.Clone(f"Lxy_tot_{year}")
        Lxy_tot.SetDirectory(0)
    else:
        Lxy_DSA.Add(h_DSA)
        Lxy_Pat.Add(h_Pat)
        Lxy_PatDSA.Add(h_PatDSA)
        Lxy_tot.Add(h_tot)
    
    file.Close()

include_overflow = True
paper = True
thesis = False
if thesis:
    paper = True

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

cms_red = ROOT.TColor.GetColor("#bd1f01")
cms_green = ROOT.TColor.GetColor("#b9ac70")
cms_yellow = ROOT.TColor.GetColor("#ffa90e")
cms_blue = ROOT.TColor.GetColor("#3f90da")

# eff_DSA.SetLineColor(ROOT.kBlue+1)
# eff_DSA.SetMarkerColor(ROOT.kBlue+1)
# eff_DSA.SetLineColor(ROOT.kGreen+2)
# eff_DSA.SetMarkerColor(ROOT.kGreen+2)
# eff_DSA.SetLineColor(cms_red)
# eff_DSA.SetMarkerColor(cms_red)
# eff_DSA.SetMarkerStyle(20)

eff_DSA.SetLineColor(cms_blue)
eff_DSA.SetMarkerColor(cms_blue)
eff_DSA.SetMarkerStyle(22)

# eff_Pat.SetLineColor(ROOT.kGreen+1)
# eff_Pat.SetMarkerColor(ROOT.kGreen+1)
# eff_Pat.SetLineColor(ROOT.kRed+1)
# eff_Pat.SetMarkerColor(ROOT.kRed+1)
eff_Pat.SetLineColor(cms_yellow)
eff_Pat.SetMarkerColor(cms_yellow)
eff_Pat.SetMarkerStyle(21)

# eff_PatDSA.SetLineColor(ROOT.kOrange+1)
# eff_PatDSA.SetMarkerColor(ROOT.kOrange+1)
# eff_PatDSA.SetLineColor(ROOT.kAzure+7)
# eff_PatDSA.SetMarkerColor(ROOT.kAzure+7)
eff_PatDSA.SetLineColor(cms_blue)
eff_PatDSA.SetMarkerColor(cms_blue)
eff_PatDSA.SetMarkerStyle(22)

hist0 = ROOT.TH1F("hist0", "hist0", n_bins, bin_edges)
hist0.GetXaxis().SetTitle("L_{xy} [cm]")
hist0.GetYaxis().SetTitle("Fraction of dimuons")
hist0.GetYaxis().SetTitleSize(0.04)
hist0.SetMaximum(1.5)
hist0.GetXaxis().SetLimits(0, 300)
hist0.GetXaxis().SetTitleSize(0.04)

# Set up a canvas to draw the plots
canvas = ROOT.TCanvas("canvas", "Efficiency Ratios", 800, 600)
canvas.SetLeftMargin(leftMargin)
canvas.SetBottomMargin(bottomMargin)
canvas.SetRightMargin(rightMargin)
canvas.SetTopMargin(topMargin)
canvas.SetTickx(1)
canvas.SetTicky(1)
canvas.SetBottomMargin(0.2)
canvas.SetTopMargin(topMargin + 0.03)

# Draw the TEfficiency objects on the same canvas
hist0.Draw("hist")  # Draw the first hist0 with axis
# eff_PatDSA.Draw("P SAME") # Draw others on the same canvas
eff_Pat.Draw("P SAME")  
eff_DSA.Draw("P SAME")

canvas.Update()

legend = ROOT.TLegend(0.4, 0.74, 0.78, 0.88)
if not paper or thesis:
    legend.AddEntry(eff_Pat, "Fraction of PAT-PAT dimuons", "lep")
    # legend.AddEntry(eff_PatDSA, "Fraction of PAT-DSA dimuons", "lep")
    legend.AddEntry(eff_DSA, "Fraction of DSA-DSA dimuons", "lep")
else:
    legend.AddEntry(eff_Pat, "Fraction of TMS-TMS dimuons", "lep")
    # legend.AddEntry(eff_PatDSA, "Fraction of TMS-STA dimuons", "lep")
    legend.AddEntry(eff_DSA, "Fraction of STA-STA dimuons", "lep")
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
# lumiText = lumi + " (13 TeV)"
lumiText = "(13 TeV)"
if include_run3:
    lumiText = "(13 TeV), (13.6 TeV)"
latex.DrawLatex(1-right, 1-top+0.02, lumiText)


left = canvas.GetLeftMargin()
bottom = canvas.GetBottomMargin()
posX_ = left + 0.045*(1-left-right) + 13
posY_ = 1-top - 0.070*(1-bottom) + 0.59
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
# latex.DrawLatex(posX_, posY_ - 0.1 , "Simulation Preliminary")
latex.DrawLatex(posX_, posY_ - 0.115 , "Simulation")
latex.DrawLatex(posX_, posY_ - 0.2 , "Preliminary")
# latex.DrawLatex(posX_, posY_ - 0.1 , "Internal")

latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextAlign(13)
extraTextSize = 0.76 * 0.55*top
latex.SetTextSize(0.76*0.55*top)
latex.DrawLatex(146, 1.12, signal[1])

# Update and save the canvas
canvas.Update()
canvas.Update()
if not os.path.exists("../plots/dimuon_Lxy_ratio"):
    os.makedirs("../plots/dimuon_Lxy_ratio")
overflow_str = ""
if include_overflow:
    overflow_str = "_overflow"

if thesis:
    canvas.SaveAs(f"../plots/dimuon_Lxy_ratio/dimuon_ratios_thesis_noPatDSA_{year_str}_{signal[0]}{overflow_str}_petroff.pdf")
elif paper:
    # canvas.SaveAs(f"../plots/dimuon_Lxy_ratio/dimuon_ratios_paper_2018_{signal[0]}{overflow_str}.pdf")
    canvas.SaveAs(f"../plots/dimuon_Lxy_ratio/dimuon_ratios_paper_noPatDSA_{year_str}_{signal[0]}{overflow_str}_petroff.pdf")
else:
    canvas.SaveAs(f"../plots/dimuon_Lxy_ratio/dimuon_ratios_AN_noPatDSA_{year_str}_{signal[0]}{overflow_str}.pdf")

# Keep the canvas open in interactive mode
canvas.Draw()
