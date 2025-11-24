from Logger import info, warn, error, fatal, logger_print

import os
from array import array
import ROOT

base_path = "/data/dust/user/jniedzie/ttalps_cms"
hist_base_name = "histograms"
skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_fakes")

# year = "2016preVFP"
# year = "2016postVFP"
# year = "2017"
# year = "2018"
# year = "2022preEE"
# year = "2022postEE"
# year = "2023preBPix"
year = "2023postBPix"

ttsemi_name = "TTToSemiLeptonic" if "22" not in year and "23" not in year else "TTtoLNu2Q"

# for signal
signal_process = f"signals{year}/tta_mAlp-12GeV_ctau-1e3mm"
input_path_signal = f"{base_path}/{signal_process}/{skim[0]}/{hist_base_name}{skim[1]}{skim[2]}/histograms.root"

# for background
background_process = f"backgrounds{year}/{ttsemi_name}"
input_path_background = f"{base_path}/{background_process}/{skim[0]}/{hist_base_name}{skim[1]}{skim[2]}/histograms.root"

canvas_divide = (2, 2)
collection_name = "LoosePATMuonsSegmentMatch"
hist_params = {
    "logAbsDzFromLeadingTightPUlt30": (500, -5, 3, 1e-2, 0.2, False),
    "logAbsDzFromLeadingTightPUge30": (500, -5, 3, 1e-2, 0.2, False),

    "logAbsDzFromLeadingTightPUlt15": (1000, -5, 3, 1e-2, 0.5, False),
    "logAbsDzFromLeadingTightPUgt45": (1000, -5, 3, 1e-2, 0.5, False),
}

beam_spot_sigma_z = 3.9  # in cm


def get_n_events_in_n_PV_range(nPVsHist, nPV_min, nPV_max):
  nPVsHist.GetXaxis().SetRangeUser(nPV_min, nPV_max)
  nPVsHist.SetDirectory(0)
  nPVsHist.SetName("nPVsHist")
  nPVsHist.SetTitle("")

  n_events = nPVsHist.Integral()
  return n_events


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
  canvas.Divide(*canvas_divide)

  canvas_reproduce = ROOT.TCanvas("canvas_reproduce", "canvas_reproduce", 2500, 2500)
  canvas_reproduce.Divide(2, 2)

  canvas_reproduce.cd(3)
  prepare_pad()
  gauss = ROOT.TF1("gauss", "gaus", -20, 20)
  gauss.SetParameters(1, 0, beam_spot_sigma_z)  # amplitude, mean, sigma
  gauss.SetTitle(f"Gaussian Distribution (sigma={beam_spot_sigma_z:.1f} cm);z (cm);Density")
  gauss.Draw()

  # Right panel
  canvas_reproduce.cd(4)
  prepare_pad()
  ROOT.gPad.SetLogx()

  nBins = 20
  log_bins = []
  for i in range(nBins + 1):
    log_bins.append(10 ** (-5 + i * (8 / nBins)))

  deltaZHist = ROOT.TH1F("deltaZ", "|z| distribution;#left|#Delta z#right| (cm);Entries", nBins, array('d', log_bins))
  deltaZHist.SetLineColor(ROOT.kRed)
  deltaZHist.SetFillColorAlpha(ROOT.kRed, 0.3)

  nEntries = 1000
  for _ in range(nEntries):
    x1 = gauss.GetRandom()
    x2 = gauss.GetRandom()
    deltaZ = abs(x1 - x2)
    deltaZHist.Fill(deltaZ)

  deltaZHist.Scale(1 / deltaZHist.Integral())

  deltaZHist.Draw("hist")
  deltaZHist.GetYaxis().SetRangeUser(0, 1.0)

  legend = ROOT.TLegend(0.6, 0.7, 0.95, 0.9)

  nPVsHist = file.Get("Event_PV_npvsGood")

  for i, (hist_name, (rebin, x_min, x_max, y_min, y_max, log_y)) in enumerate(hist_params.items()):
    hist_nonFakes_name = f"{collection_name}_nonFakes_{hist_name}"
    hist_nonFakes = file.Get(hist_nonFakes_name)

    if hist_nonFakes is None or not isinstance(hist_nonFakes, ROOT.TH1):
      error(f"{hist_nonFakes_name} not found in file: {input_path_background}")
      continue

    hist_fakes_name = f"{collection_name}_fakes_{hist_name}"
    hist_fakes = file.Get(hist_fakes_name)
    if hist_fakes is None or not isinstance(hist_fakes, ROOT.TH1):
      error(f"{hist_fakes_name} not found in file: {input_path_background}")
      continue

    canvas.cd(i + 1)
    prepare_pad()
    prepare_hist(hist_nonFakes, ROOT.kBlue, rebin)
    prepare_hist(hist_fakes, ROOT.kRed, rebin)

    n_events = None

    if hist_name == "logAbsDzFromLeadingTightPUlt30":
      n_events = get_n_events_in_n_PV_range(nPVsHist, 0, 30)
    elif hist_name == "logAbsDzFromLeadingTightPUge30":
      n_events = get_n_events_in_n_PV_range(nPVsHist, 30, 999999)
    elif hist_name == "logAbsDzFromLeadingTightPUlt15":
      n_events = get_n_events_in_n_PV_range(nPVsHist, 0, 15)
    elif hist_name == "logAbsDzFromLeadingTightPUgt45":
      n_events = get_n_events_in_n_PV_range(nPVsHist, 45, 999999)

    if n_events is None:
      if hist_nonFakes.Integral() > 0 and hist_fakes.Integral() > 0:
        hist_nonFakes.Scale(1 / hist_nonFakes.Integral())
        hist_fakes.Scale(1 / hist_fakes.Integral())
    elif n_events > 0:
      hist_nonFakes.Scale(1 / n_events)
      hist_fakes.Scale(1 / n_events)

    hist_nonFakes.SetTitle(f"PU {hist_name.split('PU')[-1].replace('lt', '<').replace('gt', '>').replace('ge', '>=')}")
    hist_nonFakes.GetXaxis().SetTitle("log #left|#Delta z_{muon, leading tight muon}#right| [cm]")

    hist_nonFakes.GetXaxis().SetRangeUser(x_min, x_max)
    hist_nonFakes.GetYaxis().SetRangeUser(y_min, y_max)

    if i == 0:
      legend.AddEntry(hist_nonFakes, "gen-matched", "l")
      legend.AddEntry(hist_fakes, "non-gen-matched", "l")

    ROOT.gPad.SetLogy(log_y)

    hist_nonFakes.Draw("histe")
    hist_fakes.Draw("samehiste")
    legend.Draw()

    if "lt30" in hist_name:
      canvas_reproduce.cd(2)
      prepare_pad()
      hist_nonFakes.Draw("histe")
      hist_fakes.Draw("samehiste")
      legend.Draw()

  try:
    file_signal = ROOT.TFile(input_path_signal)
    hist_signal_nonFakes = file_signal.Get(f"{collection_name}_nonFakes_logAbsDzFromLeadingTight")
    hist_signal_fakes = file_signal.Get(f"{collection_name}_fakes_logAbsDzFromLeadingTight")

    canvas_reproduce.cd(1)
    prepare_pad()
    prepare_hist(hist_signal_nonFakes, ROOT.kBlue, 600)
    prepare_hist(hist_signal_fakes, ROOT.kRed, 600)

    hist_signal_nonFakes.SetTitle("Signal: 12 GeV, 1 m")
    hist_signal_nonFakes.GetXaxis().SetTitle("log #left|#Delta z_{muon, leading tight muon}#right| [cm]")
    hist_signal_nonFakes.Scale(1 / hist_signal_nonFakes.Integral())
    hist_signal_fakes.Scale(1 / hist_signal_fakes.Integral())

    hist_signal_nonFakes.Draw("histe")
    hist_signal_fakes.Draw("samehiste")

    hist_signal_nonFakes.GetXaxis().SetRangeUser(-5, 3)
    hist_signal_nonFakes.GetYaxis().SetRangeUser(0, 0.9)

    legend.Draw()
  except OSError:
    error(f"File {input_path_signal} not found or corrupted.")

  os.makedirs("../plots/delta_z/", exist_ok=True)

  canvas.Update()
  canvas.SaveAs(f"../plots/delta_z/delta_z_vs_PU_{year}.pdf")

  canvas_reproduce.Update()
  canvas_reproduce.SaveAs(f"../plots/delta_z/delta_z_vs_PU_reproduce_{year}.pdf")

  logger_print()


if __name__ == "__main__":
  main()
