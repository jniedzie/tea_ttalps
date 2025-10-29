import ROOT
from Logger import info

skim_SR = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5",
           "SRDimuonsDSAChi2DCADPhi", "LooseNonLeadingMuonsVertexSegmentMatch")

skim_CR = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5",
           "JPsiDimuonsDSAChi2DCADPhi", "LooseNonLeadingMuonsVertexSegmentMatch")

hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_dimuonEffSFs_jecSFs"

base_path = "/data/dust/user/jniedzie/ttalps_cms"

paths = {
    "J/#Psi CR, tt (semi.)": f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim_CR[0]}/{hist_path}_{skim_CR[1]}_{skim_CR[2]}/histograms.root",
    "J/#Psi CR, tt (lept.)": f"{base_path}/backgrounds2018/TTTo2L2Nu/{skim_CR[0]}/{hist_path}_{skim_CR[1]}_{skim_CR[2]}/histograms.root",
    "J/#Psi CR, data": f"{base_path}/collision_data2018/SingleMuon2018_{skim_CR[0]}_{hist_path}_{skim_CR[1]}_{skim_CR[2]}.root",
    "SR, tt (semi.)": f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim_SR[0]}/{hist_path}_{skim_SR[1]}_{skim_SR[2]}/histograms.root",
}

rebin2D = 5

# category = ""
# category = "_Pat"
# category = "_PatDSA"
category = "_DSA"


# suffix = ""
suffix = "_trackerOnly"

hist_name = {
    "J/#Psi CR, tt (semi.)": f"BestDimuonVertex{category}_vy_vs_vx{suffix}",
    "J/#Psi CR, tt (lept.)": f"BestDimuonVertex{category}_vy_vs_vx{suffix}",
    "J/#Psi CR, data": f"BestDimuonVertex{category}_vy_vs_vx{suffix}",
    "SR, tt (semi.)": f"BestPFIsoDimuonVertex{category}_vy_vs_vx{suffix}",
}


def main():
  ROOT.gROOT.SetBatch(True)
  ROOT.gStyle.SetOptStat(0)

  files = {}
  hists = {}

  canvas = ROOT.TCanvas("canvas", "canvas", 2000, 500)
  canvas.Divide(4, 1)

  for i, (name, path) in enumerate(paths.items()):
    info(f"Opening file: {path}")

    files[name] = ROOT.TFile.Open(path)
    hists[name] = files[name].Get(hist_name[name])

    hists[name].Rebin2D(rebin2D, rebin2D)
    hists[name].GetXaxis().SetTitle("x [cm]")
    hists[name].GetYaxis().SetTitle("y [cm]")

    canvas.cd(i + 1)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)
    ROOT.gPad.SetLogz()

    hists[name].SetTitle(name)
    hists[name].DrawNormalized("COLZ")

  canvas.Update()
  canvas.SaveAs(f"../plots/material_maps{category}{suffix}.pdf")


if __name__ == "__main__":
  main()
