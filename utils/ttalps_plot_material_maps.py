import ROOT
from Logger import info, error, logger_print

years = [
    "2016preVFP",
    "2016postVFP",
    "2017",
    "2018",
    "2022preEE",
    "2022postEE",
    "2023preBPix",
    "2023postBPix",
]


skim = "skimmed_looseSemimuonic_v3_SR"

dimuon_type = "Best"
# dimuon_type = "Good"


hist_paths = {
    "_Pat": "ABCD",
    "_PatDSA": "noMatching",
    "_DSA": "noMatching",

    # this has a bit more entries for J/Ψ CR, but less for SR and requires running more histograms
    # It's also going to be less consistent. We decided to stick to noMatching for now.
    # "_PatDSA": "revertedMatching",
    # "_DSA": "revertedMatching",
}

user_per_category = {
    "_Pat": "lrygaard",
    "_PatDSA": "jniedzie",
    "_DSA": "jniedzie",
}

r_max = {
    "_Pat": 5,
    "_PatDSA": 180,
    "_DSA": 180,
}

rebin1D = {
    "_Pat": 2,
    "_PatDSA": 60,
    "_DSA": 100,
}

rebin2D = 1


tracker_layers = [
    # BPIX (Phase-1)
    2.9,   # BPIX Layer 1
    6.8,   # BPIX Layer 2
    10.9,  # BPIX Layer 3
    16.0,  # BPIX Layer 4

    # TIB
    25.0,  # TIB Layer 1
    34.0,  # TIB Layer 2
    43.0,  # TIB Layer 3
    52.0,  # TIB Layer 4

    # TOB
    61.0,   # TOB Layer 1
    69.6,   # TOB Layer 2
    78.2,   # TOB Layer 3
    86.8,   # TOB Layer 4
    96.5,   # TOB Layer 5
    108.0,  # TOB Layer 6
]

# suffix = ""
suffix = "_trackerOnly"


def get_paths(year, category):
  user = user_per_category[category]

  muon_name = "Muon" if "22" in year or "23" in year else "SingleMuon"
  semi_name = "TTtoLNu2Q" if "22" in year or "23" in year else "TTToSemiLeptonic"

  if muon_name == "Muon" and "23" in year and user == "jniedzie":
    muon_name = "Muon1"

  merged_year = ''.join(filter(str.isdigit, year)) if user == "jniedzie" else year

  dimuon_type_suffix = "_revertedMatching" if hist_paths[category] == "revertedMatching" else ""
  # dimuon_type_suffix = ""

  paths = {
      # data
      "J/#Psi CR, data": (
          (
              f"/data/dust/user/{user}/ttalps_cms/collision_data{year}/"
              f"{muon_name}{merged_year}_{skim}_histograms_JPsiDimuons_{hist_paths[category]}.root"
          ),
          f"{dimuon_type}DimuonVertex{dimuon_type_suffix}",
      ),
      # backgrounds CR
      "J/#Psi CR, tt (semi.)": (
          (
              f"/data/dust/user/{user}/ttalps_cms/backgrounds{year}/"
              f"{semi_name}/{skim}/histograms_JPsiDimuons_{hist_paths[category]}/histograms.root"
          ),
          f"{dimuon_type}DimuonVertex{dimuon_type_suffix}",
      ),
      # backgrounds SR
      "SR, tt (semi.)": (
          (
              f"/data/dust/user/{user}/ttalps_cms/backgrounds{year}/"
              f"{semi_name}/{skim}/histograms_SRDimuons_{hist_paths[category]}/histograms.root"
          ),
          f"{dimuon_type}PFIsoDimuonVertex{dimuon_type_suffix}",
      ),

  }
  return paths


def prepare_2d_hist(hist):
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


def prepare_1d_hist(hist):
  hist.SetLineColor(ROOT.kViolet)

  hist.GetXaxis().SetTitle("r [cm]")
  hist.GetYaxis().SetTitle("dN/dr")
  hist.GetXaxis().SetTitleSize(0.05)
  hist.GetYaxis().SetTitleSize(0.05)
  hist.GetXaxis().SetTitleOffset(1.2)
  hist.GetYaxis().SetTitleOffset(1.5)
  hist.GetXaxis().SetLabelSize(0.05)
  hist.GetYaxis().SetLabelSize(0.05)
  hist.GetXaxis().SetLabelOffset(0.015)
  hist.GetYaxis().SetLabelOffset(0.015)
  hist.GetXaxis().SetNdivisions(505)


ROOT.gInterpreter.Declare(r"""
TH1D* RadialProjection(const TH2& h, int nbins, double rmax) {
  // Create a standalone histogram (not owned by any file) to avoid double free crashes
  auto out = new TH1D(Form("r_hist_%p", &h), "r_hist", nbins, 0., rmax);
  out->SetDirectory(nullptr);
  out->Sumw2(); // keep correct uncertainties when summing many bins
  const auto xax = h.GetXaxis();
  const auto yax = h.GetYaxis();
  const int nx = xax->GetNbins();
  const int ny = yax->GetNbins();
  for (int ix = 1; ix <= nx; ++ix) {
    const double x = xax->GetBinCenter(ix);
    for (int iy = 1; iy <= ny; ++iy) {
      const double r = std::hypot(x, yax->GetBinCenter(iy));
      const double content = h.GetBinContent(ix, iy);
      const double err = h.GetBinError(ix, iy);
      const int bin = out->FindBin(r);
      out->AddBinContent(bin, content);
      const double prev_err = out->GetBinError(bin);
      out->SetBinError(bin, std::hypot(prev_err, err)); // propagate errors in quadrature
    }
  }
  return out;
}
""")


def get_r_histogram(hist2d):
  nbins = int((hist2d.GetXaxis().GetXmax() - hist2d.GetXaxis().GetXmin()) * 10)
  rmax = (hist2d.GetXaxis().GetXmax()**2 + hist2d.GetYaxis().GetXmax()**2) ** 0.5
  return ROOT.RadialProjection(hist2d, nbins, rmax)


def prepare_pad():
  ROOT.gPad.SetLeftMargin(0.15)
  ROOT.gPad.SetRightMargin(0.15)
  ROOT.gPad.SetBottomMargin(0.15)


def main():
  ROOT.gROOT.SetBatch(True)
  ROOT.gStyle.SetOptStat(0)

  files = {}
  hists = {}
  hists_r = {}

  categories = ["_Pat", "_PatDSA", "_DSA"]

  n_rows = 3
  n_columns = len(categories)

  for year in years:
    canvas = ROOT.TCanvas("canvas", "canvas", 2000, 2000)
    canvas.Divide(n_columns, n_rows)

    canvas_r = ROOT.TCanvas("canvas_r", "canvas_r", 2000, 2000)
    canvas_r.Divide(n_columns, n_rows)

    for i_category, category in enumerate(categories):
      info("=================================")
      info(f"\nProcessing category: {category}")
      info("=================================")

      for i_sample, (name, (path, collection)) in enumerate(get_paths(year, category).items()):

        unique_name = f"{year}_{category}_{name.replace(' ', '_')}"

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

        prepare_2d_hist(hists[name])

        i = i_category * n_columns + i_sample
        canvas.cd(i + 1)
        prepare_pad()
        ROOT.gPad.SetLogz()

        hists[name].SetTitle(f"{category.replace('_', '')}, {name}")
        hists[name].DrawNormalized("BOX")
        # hists[name].DrawNormalized("COLZ")

        canvas_r.cd(i + 1)
        prepare_pad()
        ROOT.gPad.SetLogy()

        hists_r[unique_name] = get_r_histogram(hists[name])
        prepare_1d_hist(hists_r[unique_name])
        hists_r[unique_name].SetTitle(f"{category.replace('_', '')}, {name}")
        hists_r[unique_name].Rebin(rebin1D[category])

        hists_r[unique_name].Draw()
        hists_r[unique_name].GetXaxis().SetRangeUser(0, r_max[category])

        for layer in tracker_layers:
          line = ROOT.TLine(layer, 0, layer, hists_r[unique_name].GetMaximum()*1.1)
          line.SetLineColor(ROOT.kBlue)
          line.SetLineStyle(ROOT.kDashed)
          line.DrawClone("same")

        pipe_radius = 2.23

        pipe_line = ROOT.TLine(pipe_radius, 0, pipe_radius, hists_r[unique_name].GetMaximum()*1.1)
        pipe_line.SetLineColor(ROOT.kGreen+2)
        pipe_line.SetLineStyle(ROOT.kDotted)
        pipe_line.DrawClone("same")

    legend = ROOT.TLegend(0.5, 0.7, 0.85, 0.9)
    line_tracker = ROOT.TLine(0, 0, 0, 0)
    line_tracker.SetLineColor(ROOT.kBlue)
    line_tracker.SetLineStyle(ROOT.kDashed)
    line_pipe = ROOT.TLine(0, 0, 0, 0)
    line_pipe.SetLineColor(ROOT.kGreen+2)
    line_pipe.SetLineStyle(ROOT.kDotted)
    legend.AddEntry(line_tracker, "Tracker layers", "l")
    legend.AddEntry(line_pipe, "Beam pipe", "l")
    canvas_r.cd(1)
    legend.Draw()

    canvas.Update()
    canvas.SaveAs(f"../plots/material_maps{suffix}_{year}.pdf")

    canvas_r.Update()
    canvas_r.SaveAs(f"../plots/material_maps_r{suffix}_{year}.pdf")

  logger_print()


if __name__ == "__main__":
  main()
