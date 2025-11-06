import os
import ROOT
from ttalps_luminosities import get_luminosity
from TTAlpsABCDConfigHelper import TTAlpsABCDConfigHelper
from Histogram import Histogram2D
from HistogramNormalizer import NormalizationType

years = ["2016preVFP","2016postVFP","2017","2018","2022preEE","2022postEE","2023preBPix","2023postBPix"]
# years = ["2016preVFP","2016postVFP","2017","2018","2022preEE","2022postEE","2023preBPix",]
# years = ["2016preVFP","2016postVFP","2017","2018",]
# years = ["2022preEE","2022postEE","2023preBPix","2023postBPix"]
# years = ["2016postVFP",]
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
luminosity_sum = 0
year = ""
for year_ in years:
  luminosity_sum += get_luminosity(year_)
  year += year_

# ------------------------------------------
# ABCD calculation and optimization settings
# ------------------------------------------

do_region = "SR"
# do_region = "SR_noChi2DCACut"
# do_region = "SR_DSAChi2DCA2"
# do_region = "SR_dimuonEffSFs" # temprary tests with generated dimuon eff. SFs
# do_region = "JPsiCR"
# do_region = "ttZCR"
# do_region = "VVCR"
# do_region = "QCDCR"
# do_region = "WjetsCR"
# do_region = "bbCR"

do_data = False
do_nonresonant_signal_as_background = False
do_binning_uncertainty = True

if"SR" in do_region:
  do_data = False
  background_collection = "BestPFIsoDimuonVertex"
  signal_collection = "BestPFIsoDimuonVertex"
elif do_region == "bbCR" or do_region == "QCDCR":
  background_collection = "BestPFIsoDimuonVertex"
  signal_collection = "BestPFIsoDimuonVertex"
elif "JPsiCR" in do_region:
  background_collection = "BestDimuonVertex"
  signal_collection = "BestPFIsoDimuonVertex"

if do_nonresonant_signal_as_background:
  background_collection = background_collection + "NonResonant"
  signal_collection = signal_collection+ "FromALP"

# category = ""
category = "_Pat"
# category = "_PatDSA"
# category = "_DSA"

exclude_backgrounds_for_years = {
  "2016preVFP": 3,
  "2016postVFP": 3,
  "2017": 3,
  "2018": 3,
  "2022preEE": 3,
  "2022postEE": 4,
  "2023preBPix": 3,
  "2023postBPix": 3,
}

# binning always expressed in bin numbers, not values
optimal_parameters = {
    # SRDimuons 2018 updated October 2025, matching before dimuon selection, collinearity angle < 0.5
    # ("_Pat", "SR"): ("logAbsCollinearityAngle", "logLeadingPt", (11, 14), "D"),
    # ("_PatDSA", "SR"): ("logDxyPVTraj1", "logLeadingPt", (12, 9), "C"),
    # ("_DSA", "SR"): ("logPt", "logInvMass", (15, 15), "C"), # displaced ctaus = 1e0-1e3

    # SRDimuons all years updated October 2025, matching before dimuon selection, collinearity angle < 0.5
    # with log Chi2 < 2 log DCA - 1.5
    ("_Pat", "SR"): ("logAbsCollinearityAngle", "logLeadingPt", (11, 14), "D"),
    ("_PatDSA", "SR"): ("logDxyPVTraj1", "logLeadingPt", (13, 8), "C"),
    ("_DSA", "SR"): ("logPt", "logInvMass", (15, 15), "C"), # displaced ctaus = 1e0-1e3

    # SRDimuons 2018 updated October 2025, with log Chi2 < 2 log DCA - 2
    ("_Pat", "SR_DSAChi2DCA2"): ("logAbsCollinearityAngle", "logPt", (11, 11), "D"),
    ("_PatDSA", "SR_DSAChi2DCA2"): ("logDxyPVTraj1", "logLeadingPt", (13, 8), "C"),
    ("_DSA", "SR_DSAChi2DCA2"): ("logOuterDR", "logLeadingPt", (14, 12), "D"),

    # JPsiDimuons 2018 updated October 2025, matching before dimuon selection, collinearity angle < 0.5
    ("_Pat", "JPsiCR"): ("logLeadingPt", "logDisplacedTrackIso03Dimuon2", (15, 14), "A"),
    ("_PatDSA", "JPsiCR"): ("logDxyPVTraj1", "logPt", (10, 11), "C"), 
    # ("_DSA", "JPsiCR"): ("logLeadingPt", "logNormChi2", (13, 15), "C"),
    ("_DSA", "JPsiCR"): ("logNormChi2", "logDca", (50, 50), "A"),

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

projection_y_title = f"Events ({year}, {luminosity_sum/1000:.1f} fb^{-1})"
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
        "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"
    ),
    "SR_noChi2DCACut": (
        "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuonsNoChi2DCA", "_LooseNonLeadingMuonsVertexSegmentMatch"
    ),
    "SR_DSAChi2DCA2": (
        "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuonsDSAChi2DCA2", "_LooseNonLeadingMuonsVertexSegmentMatch"
    ),
    "SR_dimuonEffSFs": (
        "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"
    ),
    "JPsiCR": (
        ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_JPsiDimuonsNoChi2DCA", "_LooseNonLeadingMuonsVertexSegmentMatch"),
        ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch"),
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
tea_ttalps_path = "tea_ttalps"
if username == "lrygaard":
  tea_ttalps_path = "TTALP/tea_ttalps"
output_path = (
  f"/afs/desy.de/user/{username[0]}/{username}/{tea_ttalps_path}/abcd/results_{year}/results_"
  f"{do_region}_{background_collection}{background_skim[1]}"
)
if do_nonresonant_signal_as_background:
  output_path = (
    f"/afs/desy.de/user/{username[0]}/{username}/{tea_ttalps_path}/abcd/results_{year}/signal_resonances/results_{year}_"
    f"{do_region}{background_skim[1]}"
  )
  
output_path += "_data" if do_data else "_mc"
output_path += category

if optimization_param:
  output_path += "_"+optimization_param

# hist_base_path = f"histograms_muonSFs_dsamuonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_jecSFs"
# hist_base_path = f"histograms_muonSFs_dsamuonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_dimuonEffSFs_jecSFs"
hist_base_path = f"histograms_muonSFs_dsamuonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_dimuonEffSFs_jecSFs_L1PreFiringWeightSFs"

background_hist_path = (
    f"{hist_base_path}"
    f"{background_skim[1]}{background_skim[2]}"
)
signal_hist_path = f"{hist_base_path}{signal_skim[1]}{signal_skim[2]}"

if do_nonresonant_signal_as_background:
  background_hist_path += "_genInfo_nminus1"
  signal_hist_path += "_genInfo_nminus1"

signal_path_pattern = "signals{}/tta_mAlp-{}GeV_ctau-{}mm/{}/{}/histograms.root"

data_paths = {
  "2016preVFP": f"collision_data2016preVFP/SingleMuon2016preVFP_{background_skim[0]}_{background_hist_path}.root",
  "2016postVFP": f"collision_data2016postVFP/SingleMuon2016postVFP_{background_skim[0]}_{background_hist_path}.root",
  "2017": f"collision_data2017/SingleMuon2017_{background_skim[0]}_{background_hist_path}.root",
  "2018": f"collision_data2018/SingleMuon2018_{background_skim[0]}_{background_hist_path}.root",
  "2022preEE": f"collision_data2022preEE/Muon2022preEE_{background_skim[0]}_{background_hist_path}.root",
  "2022postEE": f"collision_data2022postEE/Muon2022postEE_{background_skim[0]}_{background_hist_path}.root",
  "2023preBPix": f"collision_data2023preBPix/Muon2023preBPix_{background_skim[0]}_{background_hist_path}.root",
  "2023postBPix": f"collision_data2023postBPix/Muon2023postBPix_{background_skim[0]}_{background_hist_path}.root",
}

# signal points for which to run ABCD analysis
masses = ["0p35", "2", "12", "30", "60"]
ctaus = ["1e-5", "1e0", "1e1", "1e2", "1e3"]

# DSA-DSA displaced muons
# ctaus = ["1e0", "1e1", "1e2", "1e3"]
# PAT-PAT prompt muons
# ctaus = ["1e-5", "1e0", "1e1"]

config_helper = TTAlpsABCDConfigHelper(
    years,
    background_skim,
    category,
    base_path,
    background_hist_path,
)

if do_nonresonant_signal_as_background:
  background_samples, backgrounds = config_helper.get_signal_as_background_samples()
else:
  background_samples, backgrounds = config_helper.get_background_samples()
samples = background_samples

z_params = {
    "closure": ("|True - Pred|/True", 0, 1.0, False),
    "error": ("|True - Pred|/#sqrt{#Delta Pred^{2} + #Delta True^{2}}", 0, 5, False),
    "min_n_events": ("min(A, B, C, D)", 0, 100, True)
}
