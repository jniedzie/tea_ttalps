import os
import ROOT
from ttalps_cross_sections import get_cross_sections
from TTAlpsABCDConfigHelper import TTAlpsABCDConfigHelper
from Histogram import Histogram2D
from HistogramNormalizer import NormalizationType

luminosity = 59830.  # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2
year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)

# ------------------------------------------
# ABCD calculation and optimization settings
# ------------------------------------------

# do_region = "SR"
# do_region = "SRnewMatching"
# do_region = "SRnoIso"
# do_region = "JPsiCR"
do_region = "JPsiCRnewMatching"
# do_region = "JPsiCRwithIso"
# do_region = "ttZCR"
# do_region = "VVCR"
# do_region = "QCDCR"
# do_region = "WjetsCR"
# do_region = "bbCR"

do_data = False
do_nonresonant_signal_as_background = False

if do_region == "SR" or do_region == "SRnoIso":
  do_data = False

if do_region == "SR" or do_region == "bbCR" or do_region == "QCDCR" or do_region == "JPsiCRwithIso":
  background_collection = "BestPFIsoDimuonVertex"
  signal_collection = "BestPFIsoDimuonVertex"
elif do_region == "SRnewMatching":
  background_collection = "BestPFIsoDimuonVertex"
  signal_collection = "BestPFIsoDimuonVertex"
elif "JPsiCR" in do_region:
  background_collection = "BestDimuonVertex"
  signal_collection = "BestPFIsoDimuonVertex"
elif do_region == "SRnoIso":
  background_collection = "BestDimuonVertex"
  signal_collection = "BestDimuonVertex"

if do_nonresonant_signal_as_background:
  background_collection = background_collection + "NonResonant"
  signal_collection = signal_collection+ "FromALP"

# category = ""
# category = "_Pat"
# category = "_PatDSA"
category = "_DSA"

# exclude_backgrounds_with_less_than = 10  # entries
exclude_backgrounds_with_less_than = 3  # entries

# binning always expressed in bin numbers, not values
optimal_parameters = {
    # optimized on MC, pT > 3 GeV:
    # ("_Pat", "SR"): ("logAbsCollinearityAngle", "logPt", (12, 10), "D"),  # best
    # ("_Pat", "SR"): ("logAbsCollinearityAngle", "leadingPt", (24, 11), "D"),
    # ("_Pat", "SR"): ("logAbsCollinearityAngle", "logLeadingPt", (12, 11), "D"),
    # ("_Pat", "SR"): ("invMass", "logDeltaIso03", (10, 2), "A"),
    # ("_Pat", "SR"): ("invMass", "logDeltaSquaredIso03", (9, 7), "A"),
    # ("_Pat", "SR"): ("logAbsCollinearityAngle", "logInvMass", (11, 10), "D"),
    # ("_Pat", "SRnoIso"): ("logAbsCollinearityAngle", "logPt", (11, 10), "D"),
    # ("_Pat", "SRnoIso"): ("logAbsCollinearityAngle", "logInvMass", (11, 10), "D"),
    # ("_Pat", "SRnoIso"): ("logAbsPtLxyDPhi1", "logDxyPVTraj1", (16, 4), "D"),
    # ("_Pat", "JPsiCR"): ("logAbsCollinearityAngle", "logPt", (11, 10), "D"),
    # ("_Pat", "JPsiCR"): ("invMass", "logDeltaIso03", (10, 2), "A"),
    # ("_Pat", "JPsiCR"): ("invMass", "logDeltaSquaredIso03", (9, 7), "A"),
    # ("_Pat", "JPsiCR"): ("logAbsCollinearityAngle", "leadingPt", (24, 11), "D"),
    # ("_Pat", "JPsiCR"): ("logAbsCollinearityAngle", "logLeadingPt", (12, 11), "D"),
    # ("_Pat", "JPsiCR"): ("logAbsPtLxyDPhi1", "logDxyPVTraj1", (16, 4), "
    # ("_Pat", "JPsiCR"): ("logAbsPtLxyDPhi2", "logDisplacedTrackIso03Dimuon1", (21, 19), "A"),
    # ("_Pat", "JPsiCR"): ("logAbsPtLxyDPhi2", "logDisplacedTrackIso03Dimuon1", (19, 16), "A"),
    # ("_Pat", "QCDCR"): ("logAbsCollinearityAngle", "logLeadingPt", (14, 17), "D"),

    # ("_PatDSA", "JPsiCR"): ("logAbsPtLxyDPhi2", "logDisplacedTrackIso03Dimuon1", (19, 16), "A"),

    # new matching with JPsi SFs and min 3 bkg entries
    # ("_Pat", "SRnewMatching"): ("logAbsCollinearityAngle", "logPt", (11, 10), "D"), # 12 points
    # ("_PatDSA", "SRnewMatching"): ("absPtLxyDPhi2", "logDxyPVTraj1", (13, 16), "D"), # 13 points
    # ("_DSA", "SRnewMatching"): ("logLxy", "outerDR", (7, 12), "A"), # 11 points
    # ("_Pat", "SRnewMatching"): ("logAbsCollinearityAngle", "pt", (23, 10), "D"), # 10 points
    # ("_PatDSA", "SRnewMatching"): ("log3Dangle", "logDxyPVTraj1", (13, 5), "D"), # 12 points
    # ("_DSA", "SRnewMatching"): ("logLxy", "outerDR", (10, 8), "A"),  # 11 points
    
    # new matching DSAChi2DCADPhi (with new dimuonEff SFs)
    ("_Pat", "SRnewMatching"): ("logAbsCollinearityAngle", "pt", (23, 10), "D"), # 10 points
    ("_PatDSA", "SRnewMatching"): ("log3Dangle", "logDxyPVTraj1", (13, 5), "D"), # 12 points
    # ("_DSA", "SRnewMatching"): ("logLxy", "log3Dangle", (19, 10), "A"),  # 15 points
    ("_DSA", "SRnewMatching"): ("logLxy", "log3Dangle", (21, 16), "A"),  # 12 points 2022postEE
    # ("_DSA", "SRnewMatching"): ("logDxyPVTrajSig2", "logInvMass", (22, 9), "A"),  # 14 points
    # ("_DSA", "SRnewMatching"): ("logLxySignificance", "logInvMass", (10, 8), "A"),  # 12 points
    ("_Pat", "JPsiCRnewMatching"): ("logAbsPtLxyDPhi1", "logDeltaIso03", (11, 14), "A"), 
    ("_PatDSA", "JPsiCRnewMatching"): ("logLxy", "logLeadingPt", (10, 11), "D"),    
    ("_DSA", "JPsiCRnewMatching"): ("logLxy", "logPt", (9, 7), "D"),
    # ("_DSA", "JPsiCRnewMatching"): ("logLxy", "leadingPt", (22, 7), "D"),

    ("_DSA", "tt1DSACR"): ("logDxyPVTraj", "pt", (22, 7), "D"),

    # optimized on MC (rebin 4, μ pt > 8 GeV):
    # ("_Pat", "SR"): ("invMass", "logDeltaSquaredIso03", (23, 2), "C"),
    # ("_Pat", "SR"): ("logAbsCollinearityAngle", "logLeadingPt", (11, 13), "D"),
    # ("_Pat", "SR"): ("logAbsCollinearityAngle", "logPt", (10, 12), "D"),
    # ("_Pat", "JPsiCR"): ("log3Dangle", "logDeltaIso03", (13, 15), "A"),
    # ("_Pat", "JPsiCR"): ("logAbsPtLxyDPhi1", "logDeltaIso03", (11, 13), "A"),
    # ("_Pat", "JPsiCR"): ("outerDR", "logDeltaIso03", (14, 2), "A"),
    # ("_PatDSA", "SR"): ("logLxy", "outerDR", (7, 14), "A"),
    # ("_PatDSA", "SR"): ("outerDR", "logAbsPtLxyDPhi1", (17, 12), "D"),
    # ("_PatDSA", "SR"): ("dPhi", "logDxyPVTraj1", (15, 15), "D"),
    # ("_DSA", "SR"): ("absPtLxyDPhi2", "leadingPt", (24, 21), "D"),
    # ("_DSA", "SR"): ("leadingPt", "dEta", (4, 3), "A"),
    # ("_DSA", "SR"): ("leadingPt", "dPhi", (3, 3), "A"),
    # ("_DSA", "SR"): ("logLeadingPt", "dEta", (4, 15), "A"),
    # ("_DSA", "SR"): ("logLeadingPt", "dPhi", (3, 15), "A"),
    # ("_DSA", "SR"): ("logLxySignificance", "outerDR", (6, 14), "A"),
    # ("_DSA", "JPsiCR"): ("logLeadingPt", "dPhi", (10, 13), "A"),

}
if (category, do_region) in optimal_parameters:
  variable_1 = optimal_parameters[(category, do_region)][0]
  variable_2 = optimal_parameters[(category, do_region)][1]
  abcd_point = optimal_parameters[(category, do_region)][2]
  signal_bin = optimal_parameters[(category, do_region)][3]
else:
  variable_1 = optimal_parameters[(category, "SR")][0]
  variable_2 = optimal_parameters[(category, "SR")][1]
  abcd_point = optimal_parameters[(category, "SR")][2]
  signal_bin = optimal_parameters[(category, "SR")][3]

# optimization_param = None
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

histogram = Histogram2D(
    name=f"{background_collection}_{variable_1}_vs_{variable_2}{category}",
    norm_type=NormalizationType.to_lumi,
    x_rebin=rebin_2D,
    y_rebin=rebin_2D,
)

# ------------------------------------------
# Plotting settings
# ------------------------------------------

canvas_size = 200

# axes limits for the 1D projection
if "JPsiCR" in do_region:
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
if do_nonresonant_signal_as_background:
  background_color = ROOT.kBlue
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

# base_path = "/data/dust/user/jniedzie/ttalps_cms"
base_path = "/data/dust/user/lrygaard/ttalps_cms"

skims = {
    "SR": (
        "skimmed_looseSemimuonic_v2_SR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"
        # "skimmed_looseSemimuonic_v2_SR_looseMuonPtGt8GeV", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"
    ),
    "SRnewMatching": (
        "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuonsDSAChi2DCADPhi", "_LooseNonLeadingMuonsVertexSegmentMatch" #new dimuonEff SFs
        # "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"
        # "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuonsDSAIso", "_LooseNonLeadingMuonsVertexSegmentMatch"
    ),
    "SRnoIso": ("skimmed_looseSemimuonic_v2_SR", "_SRDimuonsNoIso", "_LooseNonLeadingMuonsVertexSegmentMatch"),
    "JPsiCR": (
        ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        # ("skimmed_looseSemimuonic_v2_SR_looseMuonPtGt8GeV", "_JPsiDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        # ("skimmed_looseSemimuonic_v2_SR_looseMuonPtGt8GeV", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
    ),
    "JPsiCRnewMatching": (
        # ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_JPsiDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        # ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_JPsiDimuonsDSAChi2DCADPhi", "_LooseNonLeadingMuonsVertexSegmentMatch"), #new dimuonEff SFs
        ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuonsDSAChi2DCADPhi", "_LooseNonLeadingMuonsVertexSegmentMatch"), #new dimuonEff SFs
    ),
    "JPsiCRwithIso": (
        ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuonsWithIso", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
    ),
    "ttZCR": ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons"),
    "VVCR": ("skimmed_looseNonTT_v1_QCDCR", "_SRDimuons"),
    "QCDCR": (
        ("skimmed_looseNoBjets_lt4jets_v1_merged", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        # ("skimmed_looseNoBjets_lt4jets_v1_looseMuonPtGt8GeV", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        # ("skimmed_looseSemimuonic_v2_SR_looseMuonPtGt8GeV", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
    ),
    "WjetsCR": ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "_SRDimuons"),
    "bbCR": (
        ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
    )
}

if isinstance(skims[do_region][0], str):
  background_skim = skims[do_region]
  signal_skim = skims[do_region]
else:
  background_skim = skims[do_region][0]
  signal_skim = skims[do_region][1]

username = os.getenv("USER")
output_path = (
    f"/afs/desy.de/user/{username[0]}/{username}/tea_ttalps/abcd/results_"
    f"{do_region}_{background_collection}{background_skim[2]}"
)
if username == "lrygaard":
    output_path = (
        f"/afs/desy.de/user/{username[0]}/{username}/TTALP/tea_ttalps/abcd/wipPlots/results_{year}_"
        f"{do_region}_{background_collection}{background_skim[1]}{background_skim[2]}"
    )
    if not do_nonresonant_signal_as_background:
      output_path = (
        f"/afs/desy.de/user/{username[0]}/{username}/TTALP/tea_ttalps/abcd/results_{year}_"
        f"{do_region}_{background_collection}{background_skim[1]}{background_skim[2]}"
      )
output_path += "_data" if do_data else "_mc"
output_path += category

# hist_base_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs"
# hist_base_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_jecSFs"
# hist_base_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_DSAEffSFs_jecSFs"
hist_base_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_dimuonEffSFs_jecSFs"
if year == "2022postEE":
    hist_base_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_dimuonEffSFs_jecSFs"

background_hist_path = (
    f"{hist_base_path}"
    f"{background_skim[1]}{background_skim[2]}"
)
signal_hist_path = f"{hist_base_path}{signal_skim[1]}{signal_skim[2]}"

signal_path_pattern = "signals/tta_mAlp-{}GeV_ctau-{}mm/{}/{}/histograms.root"
background_path_pattern = "backgrounds2018/{}/{}/{}/histograms.root"
if year == "2022postEE":
  signal_path_pattern = "signals2022postEE/tta_mAlp-{}GeV_ctau-{}mm/{}/{}/histograms.root"
  background_path_pattern = "backgrounds2022postEE/{}/{}/{}/histograms.root"

data_path = f"collision_data2018/SingleMuon2018_{background_skim[0]}_{background_hist_path}.root"

# signal points for which to run ABCD analysis
masses = ["0p35", "2", "12", "30", "60"]
ctaus = ["1e-5", "1e0", "1e1", "1e2", "1e3"]

# masses = ["0p35", "1", "2"]
# ctaus = ["1e-5", "1e0", "1e1", "1e2", "1e3"]

# masses = ["1", "2"]
# ctaus = ["1e0", "1e1", "1e2", "1e3"]

# masses = ["1", "12"]
# ctaus = ["1e1", "1e2"]

# masses = ["1"]
# ctaus = ["1e0"]

config_helper = TTAlpsABCDConfigHelper(
    year,
    background_skim,
    category,
    base_path,
    background_hist_path,
)

if do_nonresonant_signal_as_background:
  background_samples, backgrounds = config_helper.get_signal_as_background_samples(year)
else:
  background_samples, backgrounds = config_helper.get_background_samples(year)
samples = background_samples
background_params = config_helper.get_background_params(backgrounds)

z_params = {
    "closure": ("|True - Pred|/True", 0, 1.0, False),
    "error": ("|True - Pred|/#sqrt{#Delta Pred^{2} + #Delta True^{2}}", 0, 5, False),
    "min_n_events": ("min(A, B, C, D)", 0, 100, True)
}
