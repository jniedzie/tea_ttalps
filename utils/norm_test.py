import ROOT
from Logger import info

mc_file_path = "../mc.root"
data_file_path = "../SingleMuon2017_skimmed_looseSemimuonic_v3_ttbarCR_histograms_noDimuonEffSFs_noSFs.root"

lumi = 41475  # pb^-1
cross_section = 365.34  # pb


def main():
  file_mc = ROOT.TFile(mc_file_path)
  file_data = ROOT.TFile(data_file_path)

  hist_mc = file_mc.Get("cutFlow")
  hist_data = file_data.Get("cutFlow")

  mc_initial = hist_mc.GetBinContent(1)
  mc_scale = (lumi * cross_section) / mc_initial

  hist_mc.Scale(mc_scale)

  canvas = ROOT.TCanvas("canvas", "Cut Flow", 800, 600)

  ROOT.gPad.SetLogy()

  hist_mc.SetLineColor(ROOT.kRed)
  hist_mc.SetLineWidth(2)

  hist_data.SetLineColor(ROOT.kBlue)
  hist_data.SetLineWidth(2)

  hist_mc.Draw("HIST")
  hist_data.Draw("HIST SAME")

  # set y range
  max_y = max(hist_mc.GetMaximum(), hist_data.GetMaximum())
  hist_mc.SetMaximum(max_y * 1.2)
  min_y = min(hist_mc.GetMinimum(), hist_data.GetMinimum())
  hist_mc.SetMinimum(min_y * 0.8)

  legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
  legend.AddEntry(hist_mc, "MC", "l")
  legend.AddEntry(hist_data, "Data", "l")
  legend.Draw()

  canvas.SaveAs("../plots/cut_flow_comparison.pdf")

  data_last = hist_data.GetBinContent(hist_data.GetNbinsX())
  mc_last = hist_mc.GetBinContent(hist_mc.GetNbinsX())

  info(f"Data/MC in last bin: {data_last:.0f}/{mc_last:.0f} = {data_last/mc_last:.3f}")


if __name__ == "__main__":
  main()
