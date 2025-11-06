import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

input_path_noVeto = "../jetMapNoVeto.root"
input_path_withVeto = "../jetMapWithVeto.root"

file_noVeto = ROOT.TFile.Open(input_path_noVeto)
file_withVeto = ROOT.TFile.Open(input_path_withVeto)

hist_noVeto = file_noVeto.Get("jetMapNoVeto")
hist_withVeto = file_withVeto.Get("jetMapWithVeto")

canvas = ROOT.TCanvas("canvas", "Jet Veto Map Comparison", 800, 600)
canvas.Divide(2, 1)


def prepare_hist(hist):
  hist.GetXaxis().SetTitle("#eta_{j}")
  hist.GetYaxis().SetTitle("#phi_{j}")

  hist.GetXaxis().SetTitleSize(0.05)
  hist.GetYaxis().SetTitleSize(0.05)
  hist.GetXaxis().SetLabelSize(0.04)
  hist.GetYaxis().SetLabelSize(0.04)
  hist.GetXaxis().SetTitleOffset(1.2)
  hist.GetYaxis().SetTitleOffset(1.2)


canvas.cd(1)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.15)
hist_noVeto.SetTitle("No veto applied")
prepare_hist(hist_noVeto)
hist_noVeto.Draw("COLZ")

canvas.cd(2)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.15)
hist_withVeto.SetTitle("With veto applied")
prepare_hist(hist_withVeto)
hist_withVeto.Draw("COLZ")

canvas.Update()
canvas.SaveAs("../plots/jetVetoMapComparison.pdf")
