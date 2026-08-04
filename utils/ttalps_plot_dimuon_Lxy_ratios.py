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

x_max = 400
bin_edges = np.concatenate([
    np.arange(0, 50, 10), 
    np.arange(51, 130, 20),     
    np.arange(131, 180, 25),
    np.arange(181, 300, 40),
    np.arange(301, 400, 50),
    [400], 
])
bin_edges = np.array(bin_edges, dtype=np.float64)
n_bins = len(bin_edges) - 1

if thesis:
    eff_DSA.SetLineColor(cms_red)
    eff_DSA.SetMarkerColor(cms_red)
    eff_DSA.SetMarkerStyle(20)
else:
    eff_DSA.SetLineColor(cms_blue)
    eff_DSA.SetMarkerColor(cms_blue)
    eff_DSA.SetMarkerStyle(22)

eff_Pat.SetLineColor(cms_yellow)
eff_Pat.SetMarkerColor(cms_yellow)
eff_Pat.SetMarkerStyle(21)

eff_PatDSA.SetLineColor(cms_blue)
eff_PatDSA.SetMarkerColor(cms_blue)
eff_PatDSA.SetMarkerStyle(22)

hist0 = ROOT.TH1F("hist0", "hist0", n_bins, bin_edges)
hist0.GetXaxis().SetTitle("L_{xy} [cm]")
hist0.GetYaxis().SetTitle("Fraction of dimuons")
hist0.GetYaxis().SetTitleSize(0.05)
hist0.GetYaxis().SetLabelSize(0.05)
hist0.SetMaximum(1.5)
hist0.GetXaxis().SetLimits(0, 300)
hist0.GetXaxis().SetTitleSize(0.05)
hist0.GetXaxis().SetLabelSize(0.05)
hist0.GetXaxis().SetTitleOffset(1.2)


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
    legend.AddEntry(eff_PatDSA, "Fraction of TMS-STA dimuons", "lep")
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
latex.SetTextSize(0.76*0.55*top)
lumi = f"{59830. / 1000.0:.1f} fb^{{-1}}"
lumiText = "(13 TeV)"
if include_run3:
    lumiText = "(13 TeV), (13.6 TeV)"
latex.DrawLatex(1-right, 1-top+0.02, lumiText)


left = canvas.GetLeftMargin()
bottom = canvas.GetBottomMargin()
posX_ = left + 0.045*(1-left-right) + 17
posY_ = 1-top - 0.070*(1-bottom) + 0.57
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
latex.DrawLatex(posX_, posY_ - 0.115 , "Simulation")
latex.DrawLatex(posX_, posY_ - 0.2 , "Preliminary")

latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextAlign(13)
extraTextSize = 0.76 * 0.55*top
latex.SetTextSize(0.76*0.55*top)
latex.DrawLatex(195, 1.12, signal[1])

# Update and save the canvas
canvas.Update()
canvas.Update()
if not os.path.exists("../plots/dimuon_Lxy_ratio"):
    os.makedirs("../plots/dimuon_Lxy_ratio")
overflow_str = ""
if include_overflow:
    overflow_str = "_overflow"

if thesis:
    canvas.SaveAs(f"../plots/dimuon_Lxy_ratio/dimuon_ratios_thesis_{year_str}_{signal[0]}{overflow_str}_petroff_defense.pdf")
elif paper:
    canvas.SaveAs(f"../plots/dimuon_Lxy_ratio/dimuon_ratios_paper_noPatDSA_{year_str}_{signal[0]}{overflow_str}_petroff.pdf")
else:
    canvas.SaveAs(f"../plots/dimuon_Lxy_ratio/dimuon_ratios_AN_noPatDSA_{year_str}_{signal[0]}{overflow_str}.pdf")

# Keep the canvas open in interactive mode
canvas.Draw()
