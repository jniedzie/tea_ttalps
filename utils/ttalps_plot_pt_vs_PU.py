from Logger import error, fatal, logger_print

import os
import ROOT

base_path = "/data/dust/user/jniedzie/ttalps_cms"
hist_base_name = "histograms"
skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_fakes")

# year = "2016preVFP"
# year = "2016postVFP"
# year = "2017"
# year = "2018"
# year = "2022preEE"
year = "2022postEE"
# year = "2023preBPix"
# year = "2023postBPix"

ttsemi_name = "TTToSemiLeptonic" if "22" not in year and "23" not in year else "TTtoLNu2Q"

# for signal
signal_process = f"signals{year}/tta_mAlp-12GeV_ctau-1e3mm"
input_path_signal = f"{base_path}/{signal_process}/{skim[0]}/{hist_base_name}{skim[1]}{skim[2]}/histograms.root"

# for background
background_process = f"backgrounds{year}/{ttsemi_name}"
input_path_background = f"{base_path}/{background_process}/{skim[0]}/{hist_base_name}{skim[1]}{skim[2]}/histograms.root"

canvas_divide = (2, 2)
collection_name = "LoosePATMuonsSegmentMatch"


def prepare_pad():
  ROOT.gPad.SetLeftMargin(0.1)
  ROOT.gPad.SetRightMargin(0.05)
  ROOT.gPad.SetTopMargin(0.1)
  ROOT.gPad.SetBottomMargin(0.12)


def prepare_hist(hist, color, rebin):
  hist.GetXaxis().SetLabelSize(0.04)
  hist.GetYaxis().SetLabelSize(0.04)
  hist.GetXaxis().SetTitleSize(0.05)
  hist.GetYaxis().SetTitleSize(0.05)
  hist.GetXaxis().SetTitleOffset(1.0)
  hist.GetYaxis().SetTitleOffset(1.2)

  hist.SetLineColor(color)
  hist.SetFillColorAlpha(color, 0.35)

  hist.Rebin(rebin)


def main():
  ROOT.gROOT.SetBatch(True)
  ROOT.gStyle.SetLineScalePS(1.0)
  ROOT.gStyle.SetOptStat(0)

  file = ROOT.TFile(input_path_background)

  if file is None or file.IsZombie():
    fatal(f"File {input_path_background} not found or corrupted.")
    return

  canvas = ROOT.TCanvas("canvas", "canvas", 2500, 2500)

  legend = ROOT.TLegend(0.6, 0.7, 0.95, 0.9)

  (rebin, x_min, x_max, y_min, y_max) = (2, 0, 50, 1e-3, 1.0)

  hist_nonFakes_name = f"{collection_name}_nonFakes_pt"
  hist_nonFakes = file.Get(hist_nonFakes_name)

  if hist_nonFakes is None or not isinstance(hist_nonFakes, ROOT.TH1):
    error(f"{hist_nonFakes_name} not found in file: {input_path_background}")
    return

  hist_fakes_name = f"{collection_name}_fakes_pt"
  hist_fakes = file.Get(hist_fakes_name)
  if hist_fakes is None or not isinstance(hist_fakes, ROOT.TH1):
    error(f"{hist_fakes_name} not found in file: {input_path_background}")
    return

  prepare_pad()
  prepare_hist(hist_nonFakes, ROOT.kBlue, rebin)
  prepare_hist(hist_fakes, ROOT.kRed, rebin)

  hist_nonFakes.Scale(1 / hist_nonFakes.Integral())
  hist_fakes.Scale(1 / hist_fakes.Integral())
  
  hist_nonFakes.SetTitle(year)
  hist_nonFakes.GetXaxis().SetTitle("p_{T}^{#mu} [GeV]")

  hist_nonFakes.GetXaxis().SetRangeUser(x_min, x_max)
  hist_nonFakes.GetYaxis().SetRangeUser(y_min, y_max)
  
  legend.AddEntry(hist_nonFakes, "gen-matched", "l")
  legend.AddEntry(hist_fakes, "non-gen-matched", "l")

  ROOT.gPad.SetLogy()

  hist_nonFakes.Draw("histe")
  hist_fakes.Draw("samehiste")
  legend.Draw()

  os.makedirs("../plots/pt_vs_PU/", exist_ok=True)

  canvas.Update()
  canvas.SaveAs(f"../plots/pt_vs_PU/pt_vs_PU_{year}.pdf")

  logger_print()


if __name__ == "__main__":
  main()
