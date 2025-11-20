import ROOT
from Logger import info, error, logger_print

years = [
    ["2016preVFP", "2016preVFP"],
    ["2016postVFP", "2016postVFP"],
    ["2017", "2017"],
    ["2018", "2018"],
    ["2022preEE", "2022preEE"],
    ["2022postEE", "2022postEE"],
    ["2023preBPix", "2023preBPix"],
    ["2023postBPix", "2023postBPix"],
]

hist_path_JPsi = "histograms_JPsiDimuons_ABCD"
hist_path_SR = "histograms_SRDimuons_ABCD"
# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "JPsiDimuons", "ABCD")
skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

collection_CR = "BestDimuonVertex"
collection_SR = "BestPFIsoDimuonVertex"

# collection_CR = "GoodDimuonVertex"
# collection_SR = "GoodPFIsoDimuonVertex"


def get_paths_for_year(year):
  muon_name = "SingleMuon"
  semi_name = "TTToSemiLeptonic"
  lept_name = "TTTo2L2Nu"
  if "22" in year[0] or "23" in year[0]:
    muon_name = "Muon"
    semi_name = "TTtoLNu2Q"
    lept_name = "TTto2L2Nu"

  paths = {
      # data
      "J/#Psi CR, data": (
          f"/data/dust/user/lrygaard/ttalps_cms/collision_data{year[0]}/{muon_name}{year[0]}_{skim[0]}_{hist_path_JPsi}.root",
          collection_CR,
      ),
      # "tt CR, data": (
      #     f"/data/dust/user/lrygaard/ttalps_cms/backgrounds{year[1]}/{semi_name}/{skim[0]}/{hist_path}/histograms.root",
      #     collection_CR,
      # ),
      # backgrounds CR
      "J/#Psi CR, tt (semi.)": (
          f"/data/dust/user/lrygaard/ttalps_cms/backgrounds{year[1]}/{semi_name}/{skim[0]}/{hist_path_JPsi}/histograms.root",
          collection_CR,
      ),
      # "J/#Psi CR, tt (lept.)": (
      #   f"/data/dust/user/lrygaard/ttalps_cms/backgrounds{year[1]}/{lept_name}/{skim[0]}/{hist_path}/histograms.root",
      #   collection_CR,
      # ),
      # backgrounds SR
      "SR, tt (semi.)": (
          f"/data/dust/user/lrygaard/ttalps_cms/backgrounds{year[1]}/{semi_name}/{skim[0]}/{hist_path_SR}/histograms.root",
          collection_SR,
      ),

  }
  return paths


rebin2D = 1

categories = ["_Pat", "_PatDSA", "_DSA"]


# suffix = ""
suffix = "_trackerOnly"


def prepare_hist(hist):
  hist.Rebin2D(rebin2D, rebin2D)
  hist.SetMarkerStyle(20)
  hist.SetMarkerSize(1.0)
  hist.SetMarkerColor(ROOT.kBlack)
  hist.SetLineColor(ROOT.kViolet)
  hist.SetFillColorAlpha(ROOT.kViolet, 1.0)

  hist.GetXaxis().SetTitle("x [cm]")
  hist.GetYaxis().SetTitle("y [cm]")
  hist.GetXaxis().SetTitleSize(0.05)
  hist.GetYaxis().SetTitleSize(0.05)
  hist.GetXaxis().SetTitleOffset(1.2)
  hist.GetYaxis().SetTitleOffset(1.5)
  hist.GetXaxis().SetLabelSize(0.05)
  hist.GetYaxis().SetLabelSize(0.05)
  hist.GetXaxis().SetLabelOffset(0.015)
  hist.GetYaxis().SetLabelOffset(0.015)


def main():
  ROOT.gROOT.SetBatch(True)
  ROOT.gStyle.SetOptStat(0)

  files = {}
  hists = {}

  n_rows = 3
  n_columns = len(categories)

  for year in years:
    canvas = ROOT.TCanvas("canvas", "canvas", 2000, 2000)
    canvas.Divide(n_columns, n_rows)

    for i_category, category in enumerate(categories):
      info("=================================")
      info(f"\nProcessing category: {category}")
      info("=================================")

      for i_sample, (name, (path, collection)) in enumerate(get_paths_for_year(year).items()):

        hist_name = f"{collection}{category}_vy_vs_vx{suffix}"
        info(f"\nProcessing sample {name}: {path}")

        try:
          files[name] = ROOT.TFile.Open(path)
        except OSError:
          error(f"Could not open file: {path}")
          continue

        hists[name] = files[name].Get(hist_name)

        if hists[name] is None or type(hists[name]) == ROOT.TObject:
          error(f"Histogram {hist_name} not found in file {path}")
          continue

        if hists[name].GetSumOfWeights() == 0:
          error(f"Histogram {hist_name} in file {path} has sum of weights = 0")
          continue

        prepare_hist(hists[name])

        i = i_category * n_rows + i_sample
        canvas.cd(i + 1)
        ROOT.gPad.SetLeftMargin(0.15)
        ROOT.gPad.SetRightMargin(0.15)
        ROOT.gPad.SetBottomMargin(0.15)
        ROOT.gPad.SetLogz()

        hists[name].SetTitle(f"{category.replace('_', '')}, {name}")
        hists[name].DrawNormalized("BOX")

    canvas.Update()
    canvas.SaveAs(f"../plots/material_maps{suffix}_{year[0]}.pdf")

  logger_print()


if __name__ == "__main__":
  main()
