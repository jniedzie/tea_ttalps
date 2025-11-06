import ROOT

rebin = 20

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

base_path = "/data/dust/user/jniedzie/ttalps_cms/backgrounds2017/TTToSemiLeptonic/skimmed_looseSemimuonic_v2_ttbarCR"
base_hist_name = "histograms_muonSFs_dsamuonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_jecSFs_L1PreFiringWeightSFs"

input_path_noL1 = f"{base_path}/{base_hist_name}_noL1weights/histograms.root"
input_path_withL1 = f"{base_path}/{base_hist_name}/histograms.root"

file_noL1 = ROOT.TFile.Open(input_path_noL1)
file_withL1 = ROOT.TFile.Open(input_path_withL1)

hist_noL1 = file_noL1.Get("Event_MET_pt")
hist_withL1 = file_withL1.Get("Event_MET_pt")

hist_noL1.Rebin(rebin)
hist_withL1.Rebin(rebin)

canvas = ROOT.TCanvas("canvas", "L1 Prefiring Comparison", 800, 600)
canvas.cd()

pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1)
pad1.SetBottomMargin(0)
pad1.SetLogy()
pad1.Draw()

pad2 = ROOT.TPad("pad2", "pad2", 0, 0, 1, 0.3)
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad2.Draw()

pad1.cd()
hist_noL1.SetLineColor(ROOT.kBlue)
hist_noL1.SetMarkerStyle(20)
hist_noL1.SetMarkerSize(0.8)
hist_noL1.SetMarkerColor(ROOT.kBlue)

hist_withL1.SetLineColor(ROOT.kRed)
hist_withL1.SetMarkerStyle(21)
hist_withL1.SetMarkerSize(0.8)
hist_withL1.SetMarkerColor(ROOT.kRed)

hist_noL1.SetTitle("")
hist_noL1.GetXaxis().SetTitle("MET_pt (GeV)")
hist_noL1.GetYaxis().SetTitle("Events")

hist_noL1.Draw("PE")
hist_withL1.Draw("PE same")

legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
legend.AddEntry(hist_noL1, "Without L1 Prefiring", "l")
legend.AddEntry(hist_withL1, "With L1 Prefiring", "l")
legend.Draw()
pad1.Update()


pad2.cd()

ratio_hist = hist_withL1.Clone("ratio_hist")
ratio_hist.Divide(ratio_hist, hist_noL1, 1.0, 1.0, "B")
ratio_hist.SetTitle("")

ratio_hist.SetMarkerStyle(20)
ratio_hist.SetMarkerSize(0.8)
ratio_hist.SetMarkerColor(ROOT.kBlack)
ratio_hist.SetLineColor(ROOT.kBlack)

ratio_hist.GetXaxis().SetTitle("MET_pt (GeV)")
ratio_hist.GetXaxis().SetLabelSize(0.1)
ratio_hist.GetXaxis().SetTitleSize(0.12)

ratio_hist.GetYaxis().SetTitle("With/Without")
ratio_hist.GetYaxis().SetLabelSize(0.1)
ratio_hist.GetYaxis().SetTitleSize(0.09)
ratio_hist.GetYaxis().SetTitleOffset(0.5)

ratio_hist.GetYaxis().SetRangeUser(0.8, 1.2)

ratio_hist.Draw("PE")

line = ROOT.TLine(hist_noL1.GetXaxis().GetXmin(), 1.0, hist_noL1.GetXaxis().GetXmax(), 1.0)
line.SetLineStyle(ROOT.kDashed)
line.SetLineColor(ROOT.kBlack)
line.Draw()

pad2.Update()

canvas.SaveAs("../plots/L1_prefiring_comparison.pdf")
