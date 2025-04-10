import os
import ROOT
from ttalps_cross_sections import get_cross_sections


lumi = 137190  # pb^-1
year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)


# ------------------------------------------
# ABCD calculation and optimization settings
# ------------------------------------------

do_region = "SR"
# do_region = "JPsiCR"
# do_region = "ttZCR"
# do_region = "VVCR"
# do_region = "QCDCR"
# do_region = "WjetsCR"
# do_region = "bbCR"

do_data = False

if do_region == "SR":
  do_data = False


# collection = "GoodPFIsoDimuonVertex"
collection = "BestPFIsoDimuonVertex"
# collection = "BestDimuonVertex"

# Pat-Pat:
variable_1 = "logLxySignificance"
variable_2 = "log3Dangle"

# DSA-DSA:
# variable_1 = "logLxySignificance"
# variable_2 = "logAbsPtLxyDPhi1"

# category = ""
# category = "_Pat"
# category = "_PatDSA"
category = "_DSA"

# this is obsolete, and also has to move to bin-based rather than value-based
optimal_points = {
    # optimizing on significance
    "JPsi_noIso_mc": (-0.9, 0.86),
    "JPsi_noIso_data": (-0.54, 0.42),  # all identical

    "JPsi_iso_mc": (-1.06, 0.22),  # outdated
    "JPsi_iso_data": (-1.18, 0.46),

    "SR_noIso_mc": (0.46, -1.94),  # all identical
    "SR_iso_mc": (-0.78, 0.34),

    "SR_iso_PATDSA_muEtaLt1p2_muPtGt10_mc": (0.1, -0.54),  # middle ground

    "QCD_iso_mc": (0.02, 0.82),
    "QCD_iso_data": (0.46, 1.14),

    # optimizing on error (same results on closure)
    "JPsi_noIso_mc_optimalError": (-1.22, 0.06),  # outdated
    "JPsi_noIso_data_optimalError": (-1.38, -1.26),  # outdated
}

# binning always expressed in bin numbers, not values
abcd_point = (999, 999)
# abcd_point = (18, 2)
# abcd_point = (3, 2)

# abcd_point = optimal_points["QCD_iso_data"]

optimization_param = "significance"
# optimization_param = "error"
# optimization_param = "closure"

common_signals_optimization = True

# ------------------------------------------
# Rebinning and projection settings
# ------------------------------------------

# you can specify custom binning for the 1D projection
custom_rebin = True
custom_projections_binning = [0, 0.5, 0.9, 1.5, 2.0]
# custom_projections_binning = [0, 0.6, 1.5, 2.0]

# you can also use smart rebinning for the 1D projection, which will keep the relative error below a certain threshold
smart_rebin = False
smart_rebin_max_error = 0.30  # max allowed ralative error for smart rebinning

# or you can use standard rebinning for the 1D projection (the number is the rebin factor)
standard_rebin = 1

# rebinning factor for the 2D histograms of signals and backgrounds and optimization histograms
# (closure, error, min_n_events, significance, contamination)
rebin_2D = 4


# ------------------------------------------
# Plotting settings
# ------------------------------------------

canvas_size = 200

# axes limits for the 1D projection
if do_region == "JPsiCR":
  y_max = 50
  y_max_ratio = 3
elif do_region == "SR":
  y_max = 30
  y_max_ratio = 10
elif do_region == "ttZCR":
  y_max = 10
  y_max_ratio = 10
elif do_region == "VVCR":
  y_max = 10
  y_max_ratio = 10
elif do_region == "QCDCR":
  y_max = 10
  y_max_ratio = 10
elif do_region == "WjetsCR":
  y_max = 10
  y_max_ratio = 10
elif do_region == "bbCR":
  y_max = 10
  y_max_ratio = 10


# you can specify colors for the signals in the projection (otherwise they will default to red)
signal_colors = {
    ("1", "1e1"): ROOT.kGreen+1,
    ("1", "1e2"): ROOT.kCyan+1,
    ("12", "1e1"): ROOT.kBlue,
    ("12", "1e2"): ROOT.kViolet,
}

signal_label_position = (0.11, 0.12)
projections_legend_position = (0.6, 0.6, 0.9, 0.9)

background_color = ROOT.kBlack
signal_color = ROOT.kRed

abcd_line_color = ROOT.kCyan+1
abcd_line_width = 1

true_background_color = ROOT.kRed
true_background_description = "Background in A"

predicted_background_color = ROOT.kBlack
predicted_background_description = "ABCD prediction"

projection_y_title = "Events (2018, 137 fb^{-1})"
ratio_y_title = " Pred / True   "

# you can specify custom names for the variables to be displayed in the plots
nice_names = {
    "Lxy": "L_{xy} (cm)",
    "LxySignificance": "L_{xy} significance",
    "absCollinearityAngle": "|#theta_{coll}|",
    "3Dangle": "#alpha_{3D}",
    "logLxy": "log_{10}[L_{xy} (cm)]",
    "logLxySignificance": "log_{10}[L_{xy} significance]",
    "logAbsCollinearityAngle": "log_{10}[|#theta_{coll}|]",
    "log3Dangle": "log_{10}[#alpha_{3D}]",
    "LogLxy": "log_{10}[L_{xy} (cm)]",
    "LogLxySignificance": "log_{10}[L_{xy} significance]",
    "LogAbsCollinearityAngle": "log_{10}[|#theta_{coll}|]",
    "Log3Dangle": "log_{10}[#alpha_{3D}]",
}

# ------------------------------------------
# Samples settings
# ------------------------------------------

base_path = "/data/dust/user/jniedzie/ttalps_cms"

username = os.getenv("USER")
output_path = f"/afs/desy.de/user/{username[0]}/{username}/tea_ttalps/abcd/results_{do_region}_{collection}"

if do_data:
  output_path += "_data"
else:
  output_path += "_mc"


output_path += category

if do_region == "JPsiCR":
  skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons")
elif do_region == "ttZCR":
  skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons")
elif do_region == "SR":
  skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons")
  # skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2", "_SRDimuons")
  # skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2_muPtGt10", "_SRDimuons")
  # skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2_muPtGt7", "_SRDimuons")
elif do_region == "VVCR":
  skim = ("skimmed_looseNonTT_v1_QCDCR", "_SRDimuons")
elif do_region == "QCDCR":
  skim = ("skimmed_looseNoBjets_lt4jets_v1_QCDCR", "_SRDimuons")
elif do_region == "WjetsCR":
  skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "_SRDimuons")
elif do_region == "bbCR":
  skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons")
  # skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt10", "_SRDimuons")
  # skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt20", "_SRDimuons")
  # skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_muPtGt20", "_SRDimuons")

hist_dir = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}"

signal_path_pattern = "signals/tta_mAlp-{}GeV_ctau-{}mm/{}/{}/histograms.root"
background_path_pattern = "backgrounds2018/{}/{}/{}/histograms.root"

data_path = f"collision_data2018/SingleMuon2018_{skim[0]}_{hist_dir}.root"

# signal points for which to run ABCD analysis
masses = ["0p35", "1", "2", "12", "30", "60"]
ctaus = ["1e-5", "1e0", "1e1", "1e2", "1e3"]

# masses = ["1", "2"]
# ctaus = ["1e0", "1e1", "1e2", "1e3"]

# masses = ["1", "12"]
# ctaus = ["1e1", "1e2"]

# masses = ["1"]
# ctaus = ["1e0"]

backgrounds = [
    "TTToSemiLeptonic",
    "TTToHadronic",
    # "TTTo2L2Nu",  # fluctuates in SR DSA-DSA

    "TTZToLLNuNu_M-10",
    "TTZToLL_M-1to10",
    "TTZZ",
    "TTZH",
    "TTTT",

    "TTWJetsToLNu",

    "ttHTobb",
    "ttHToNonbb",

    "ST_tW_antitop",
    "ST_t-channel_antitop",
    "ST_tW_top",
    "ST_t-channel_top",

    "DYJetsToMuMu_M-50",
    "DYJetsToMuMu_M-10to50",
    # "WJetsToLNu",

    # "QCD_Pt-15To20",
    # "QCD_Pt-20To30",
    # "QCD_Pt-30To50",
    # "QCD_Pt-50To80",
    # "QCD_Pt-80To120",
    # "QCD_Pt-120To170",
    # "QCD_Pt-170To300",
    "QCD_Pt-300To470",
    "QCD_Pt-470To600",
    "QCD_Pt-600To800",
    "QCD_Pt-800To1000",
    "QCD_Pt-1000",
]

if category != "_DSA" or do_region != "SR":
  backgrounds.append("TTTo2L2Nu")  # fluctuates in SR DSA-DSA

background_params = []
for b in backgrounds:
  for k, v in cross_sections.items():
    if b in k:
      background_params.append((b, v))
      break

z_params = {
    "closure": ("|True - Pred|/True", 0, 1.0, False),
    "error": ("|True - Pred|/#sqrt{#Delta Pred^{2} + #Delta True^{2}}", 0, 5, False),
    "min_n_events": ("min(A, B, C, D)", 0, 100, True)
}
