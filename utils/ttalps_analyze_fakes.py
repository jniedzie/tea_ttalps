from Logger import info, warn, error, fatal, logger_print

import ROOT
import os
from math import pi

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"


hist_base_name = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"

# for signal
# mass = "0p35"
# mass = "2"
# mass = "12"
# mass = "30"
mass = "60"

# ctau = "1e-5"
# ctau = "1e0"
# ctau = "1e1"
# ctau = "1e2"
ctau = "1e3"

# process = f"signals/tta_mAlp-{mass}GeV_ctau-{ctau}mm"

# input_path = f"{base_path}/signals/tta_mAlp-{mass}GeV_ctau-{ctau}mm/{skim[0]}/{hist_base_name}{skim[1]}/histograms.root"
# output_path = f"../plots/fakes_{mass}GeV_{ctau}mm.pdf"


# for background
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt10", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt20", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_muPtGt20", "_SRDimuons")

# skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons")
skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2_muPtGt10", "_SRDimuons")

hist_base_name = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs"


process = "backgrounds2018/TTTo2L2Nu"
# process = "backgrounds2018/TTToSemiLeptonic"
# process = "backgrounds2018/ST_tW_antitop"
# process = "backgrounds2018/ST_t-channel_antitop"
# process = "backgrounds2018/ST_tW_top"
# process = "backgrounds2018/ST_t-channel_top"


input_path = f"{base_path}/{process}/{skim[0]}/{hist_base_name}{skim[1]}{skim[2]}/histograms.root"
# input_path = "../test.root"

output_path = f"../plots/fakes_{process.split('/')[-1]}.pdf"

# canvas_divide = (4, 4)
# collection_name = "BestPFIsoDimuonVertex_PatDSA"
# # collection_name = "BestPFIsoDimuonVertex_Pat"
# hist_params = {
#     "dEta": (10, 0, 5, 1e-4, 2e0, True),  # interesting
#     "dPhi": (10, 0, 2*pi, 1e-4, 2e0, True),  # interesting
#     "dR": (10, 0, 5, 1e-4, 2e0, True),  # interesting
#     "outerDR": (10, 0, 5, 1e-4, 2e0, True),  # interesting

#     "absPtLxyDPhi1": (10, 0, pi, 1e-4, 2e0, True),  # interesting
#     "absPtLxyDPhi2": (10, 0, pi, 1e-4, 2e0, True),  # interesting
#     "logLxy": (20, -5, 2, 1e-4, 2e0, True),  # interesting
#     "eta": (5, -3, 3, 0, 0.2, False),

#     "vxyzSigma": (100, 0, 20, 1e-4, 1e0, True),  # check
#     "displacedTrackIso04Muon2": (40, 0, 20, 1e-4, 1e0, True),
#     "displacedTrackIso03Muon2": (20, 0, 20, 1e-4, 1e0, True),
#     "hitsInFrontOfVert1": (1, 0, 10, 1e-2, 1e0, True),

#     "invMass": (200, 0, 80, 1e-4, 1e-1, True),  # check
#     "logInvMass": (20, 0, 3, 1e-4, 1e0, True),
#     "vxy": (10, 0, 30, 1e-3, 1e0, True),
#     "vz": (10, -100, 100, 1e-4, 1e0, True),

#     # "vzErr": (5, 0, 100, 1e-4, 1e0, True),
#     # "dRprox": (10, 0, 4, 1e-4, 1e0, True),
#     # "dcaz": (10, -100, 100, 1e-4, 1e0, True),
#     # "3Dangle": (20, 0, 5, 1e-4, 2e0, True),

#     # "cos3Dangle": (10, -1, 1, 1e-4, 2e-1, True),
#     # "absCollinearityAngle": (20, -3, 3, 1e-4, 1e0, True),
#     # "Lxy": (200, 0, 500, 1e-7, 2e0, True),
#     # "LxySigma": (400, 0, 100, 1e-7, 2e0, True),

#     # "LxySignificance": (1, 0, 30, 1e-4, 2e0, True),
#     # "dca": (5, 0, 3, 1e-3, 1e-1, True),
#     # "displacedTrackIso03Dimuon1": (20, 0, 10, 1e-6, 2e0, True),
#     # "displacedTrackIso03Dimuon2": (10, 0, 10, 1e-6, 2e0, True),

#     # "displacedTrackIso04Dimuon1": (40, 0, 15, 1e-6, 2e0, True),
#     # "displacedTrackIso04Dimuon2": (20, 0, 15, 1e-6, 2e0, True),
#     # "dxyPVTraj1": (5, 0, 100, 1e-6, 2e0, True),
#     # "dxyPVTraj2": (5, 0, 100, 1e-6, 1e0, True),

#     # "dxyPVTrajSig1": (10, 0, 500, 1e-5, 2e0, True),
#     # "dxyPVTrajSig2": (10, 0, 500, 1e-5, 2e0, True),
#     # "normChi2": (100, 0, 5, 1e-4, 2e0, True),
#     # "maxHitsInFrontOfVert": (1, 0, 10, 1e-4, 2e0, True),

#     # "pt": (20, 0, 400, 1e-4, 2e0, True),
#     # "leadingPt": (20, 0, 400, 1e-4, 2e0, True),
#     # "pfRelIso04all1": (1, 0, 5, 1e-6, 2e0, True),
#     # "pfRelIso04all2": (1, 0, 5, 1e-6, 2e0, True),

#     # "nSegments": (1, 0, 20, 1e-4, 2e0, True),
#     # "nSegments1": (1, 0, 20, 1e-4, 2e0, True),
#     # "nSegments2": (1, 0, 20, 1e-4, 2e0, True),
#     # "isValid": (1, 0, 2, 1e-7, 2e0, True),

#     # "vxyz": (20, 0, 50, 1e-4, 2e0, True),
#     # "chi2": (2, 0, 5, 1e-5, 2e0, True),
#     # "ndof": (1, 0, 20, 1e-4, 2e0, True),
#     # "vx": (10, -100, 100, 1e-4, 2e0, True),

#     # "vy": (10, -100, 100, 1e-4, 1e0, True),
#     # "t": (1, -100, 100, 1e-4, 1e0, True),
#     # "vxErr": (10, 0, 100, 1e-4, 1e0, True),
#     # "vyErr": (10, 0, 100, 1e-4, 1e0, True),

#     # "tErr": (20, 0, 100, 1e-4, 1e0, True),
#     # "displacedTrackIso03Muon1": (50, 0, 20, 1e-4, 1e0, True),
#     # "displacedTrackIso04Muon1": (50, 0, 20, 1e-4, 1e0, True),
#     # "dcaStatus": (2, 0, 2, 1e-4, 1e0, True),

#     # "dcax": (10, -100, 100, 1e-4, 1e0, True),
#     # "dcay": (10, -100, 100, 1e-4, 1e0, True),
#     # "missHitsAfterVert1": (1, 0, 20, 1e-10, 2e0, True),
#     # "missHitsAfterVert2": (1, 0, 20, 1e-10, 2e0, True),
# }


canvas_divide = (2, 2)
# collection_name = "LooseDSAMuonsSegmentMatch"
collection_name = "LoosePATMuonsSegmentMatch"
hist_params = {
    "pt": (5, 0, 100, 1e-5, 2e0, True),  # check
    # "dxy": (5, -20, 20, 1e-6, 2e0, True),
    # "dxyPVTrajErr": (5, 0, 50, 1e-6, 2e0, True),
    "eta": (20, -3, 3, 1e-4, 2e0, True),  # check
    "dz": (20, -50, 50, 1e-6, 2e0, True),  # check
    # "dzPVErr": (5, 0, 50, 1e-6, 2e0, True),
    "normChi2": (100, 0, 4, 1e-5, 1e0, True),  # check
    # "phi": (20, -3.5, 3.5, 1e-4, 2e0, True),
    # "ptErr": (10, 0, 50, 1e-5, 2e0, True),

    # "etaErr": (2, 0, 1, 1e-5, 2e0, True),
    # "phiErr": (2, 0, 1, 1e-5, 2e0, True),
    # "vx": (10, -200, 200, 1e-6, 2e0, True),
    # "vy": (10, -200, 200, 1e-6, 2e0, True),
    # "vz": (10, -200, 200, 1e-6, 2e0, True),
    # "chi2": (20, 0, 50, 1e-5, 2e0, True),
    # "ndof": (2, 0, 50, 1e-4, 2e0, True),
    # "trkNumPlanes": (1, 0, 10, 1e-4, 2e0, True),
    # "trkNumHits": (1, 0, 50, 1e-4, 2e0, True),

    # "trkNumDTHits": (1, 0, 20, 1e-4, 2e0, True),
    # "trkNumCSCHits": (1, 0, 20, 1e-4, 2e0, True),
    # "outerEta": (20, -3, 3, 1e-4, 2e0, True),
    # "outerPhi": (20, -3.5, 3.5, 1e-4, 2e0, True),
    # "dzPV": (40, -200, 200, 1e-6, 2e0, True),
    # "dxyPVTraj": (40, -200, 200, 1e-6, 2e0, True),
    # "dxyPVSigned": (40, -200, 200, 1e-6, 2e0, True),
    # "dxyPVSignedErr": (40, 0, 200, 1e-6, 2e0, True),
    # "ip3DPVSigned": (40, -200, 200, 1e-6, 2e0, True),

    # "ip3DPVSignedErr": (40, 0, 200, 1e-6, 2e0, True),
    # "dxyBS": (40, -200, 200, 1e-6, 2e0, True),
    # "dxyBSErr": (40, 0, 200, 1e-6, 2e0, True),
    # "dzBS": (40, -200, 200, 1e-6, 2e0, True),
    # "dzBSErr": (40, 0, 200, 1e-6, 2e0, True),
    # "dxyBSTraj": (40, 0, 200, 1e-6, 2e0, True),
    # "dxyBSTrajErr": (40, 0, 200, 1e-6, 2e0, True),
    # "dxyBSSigned": (40, -200, 200, 1e-6, 2e0, True),
    # "dxyBSSignedErr": (40, 0, 200, 1e-6, 2e0, True),

    # "ip3DBSSigned": (40, -200, 200, 1e-6, 2e0, True),
    # "ip3DBSSignedErr": (40, 0, 200, 1e-6, 2e0, True),
    # "displacedID": (1, -100, 100, 1e-6, 2e0, True),
    # "nSegments": (1, 0, 10, 1e-6, 1e0, True),
    # "nDTSegments": (1, 0, 10, 1e-2, 1e0, True),
    # "nCSCSegments": (1, 0, 15, 1e-4, 1e0, True),
}


def main():
  ROOT.gROOT.SetBatch(True)

  ROOT.gStyle.SetLineScalePS(1.0)
  ROOT.gStyle.SetOptStat(0)
  file = ROOT.TFile(input_path)

  if file is None or file.IsZombie():
    fatal(f"File {input_path} not found or corrupted.")
    return

  canvas = ROOT.TCanvas("canvas", "canvas", 2500, 2500)
  canvas.Divide(*canvas_divide)

  legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)

  for i, (hist_name, (rebin, x_min, x_max, y_min, y_max, log_y)) in enumerate(hist_params.items()):
    hist_nonFakes_name = f"{collection_name}_nonFakes_{hist_name}"
    hist_nonFakes = file.Get(hist_nonFakes_name)

    if hist_nonFakes is None or not isinstance(hist_nonFakes, ROOT.TH1):
      error(f"{hist_nonFakes_name} not found in file: {input_path}")
      continue

    hist_fakes_name = f"{collection_name}_fakes_{hist_name}"
    hist_fakes = file.Get(hist_fakes_name)
    if hist_fakes is None or not isinstance(hist_fakes, ROOT.TH1):
      error(f"{hist_fakes_name} not found in file: {input_path}")
      continue

    canvas.cd(i + 1)
    ROOT.gPad.SetLeftMargin(0.05)
    ROOT.gPad.SetRightMargin(0.01)
    hist_nonFakes.SetLineColor(ROOT.kBlue)
    hist_fakes.SetLineColor(ROOT.kRed)

    hist_nonFakes.Rebin(rebin)
    hist_fakes.Rebin(rebin)

    if hist_nonFakes.Integral() > 0 and hist_fakes.Integral() > 0:
      hist_nonFakes.Scale(1 / hist_nonFakes.Integral())
      hist_fakes.Scale(1 / hist_fakes.Integral())

    hist_nonFakes.Draw("")
    hist_fakes.Draw("same")

    hist_nonFakes.GetXaxis().SetRangeUser(x_min, x_max)
    hist_nonFakes.GetYaxis().SetRangeUser(y_min, y_max)
    hist_nonFakes.GetXaxis().SetTitle(hist_name)

    if i == 0:
      legend.AddEntry(hist_nonFakes, "non-fakes", "l")
      legend.AddEntry(hist_fakes, "fakes", "l") 

    ROOT.gPad.SetLogy(log_y)

  legend.Draw()

  canvas.Update()
  canvas.SaveAs(output_path)

  logger_print()


if __name__ == "__main__":
  main()
