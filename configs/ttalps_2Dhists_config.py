import os
import ROOT
from ttalps_luminosities import get_luminosity
from TTAlpsABCDConfigHelper import TTAlpsABCDConfigHelper
from Histogram import Histogram2D
from HistogramNormalizer import NormalizationType

# years = ["2016preVFP","2016postVFP","2017","2018","2022preEE","2022postEE","2023preBPix","2023postBPix"]
years = ["2018",]
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
luminosity_sum = 0
year = ""
for year_ in years:
  luminosity_sum += get_luminosity(year_)
  year += year_

# ------------------------------------------
# 2D plotting settings
# ------------------------------------------

do_region = "SR_collinearityAngle_plot"
# do_region = "SR_chi2vsDCA_plot"
# do_region = "JPsiCR_chi2vsDCA_plot"

do_data = False
do_nonresonant_signal_as_background = False
do_binning_uncertainty = True

if "SR" in do_region:
  do_data = False
  background_collection = "BestPFIsoDimuonVertex"
  signal_collection = "BestPFIsoDimuonVertex"
  if do_region == "SR_collinearityAngle_plot":
    background_collection = "BestPFIsoDimuonVertexNminus1CollinearityAngleCut"
    signal_collection = "BestPFIsoDimuonVertexNminus1CollinearityAngleCut"
elif "JPsiCR" in do_region:
  background_collection = "BestDimuonVertex"
  signal_collection = "BestPFIsoDimuonVertex"
  if do_region == "JPsiCR_chi2vsDCA_plot":
    # I accidentaly names the J/Psi dimuons BestPFIso..
    background_collection = "BestPFIsoDimuonVertex" 


if do_nonresonant_signal_as_background:
  background_collection = background_collection + "NonResonant"
  signal_collection = signal_collection+ "FromALP"

# category = ""
# category = "_Pat"
# category = "_PatDSA"
category = "_DSA"

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
    # To produce N-1 plots of collinearity angle vs. dPhi between muon1 and Lxy vector
    ("_Pat", "SR_collinearityAngle_plot"): ("absPtLxyDPhi1", "absCollinearityAngle", (30, 30), "A"),
    ("_PatDSA", "SR_collinearityAngle_plot"): ("absPtLxyDPhi1", "absCollinearityAngle", (30, 30), "A"),
    ("_DSA", "SR_collinearityAngle_plot"): ("absPtLxyDPhi1", "absCollinearityAngle", (30, 30), "A"),

    ("_Pat", "SR_chi2vsDCA_plot"): ("logNormChi2", "logDca", (50, 50), "A"),
    ("_PatDSA", "SR_chi2vsDCA_plot"): ("logNormChi2", "logDca", (50, 50), "A"),
    ("_DSA", "SR_chi2vsDCA_plot"): ("logNormChi2", "logDca", (50, 50), "A"),
    ("_Pat", "JPsiCR_chi2vsDCA_plot"): ("logNormChi2", "logDca", (50, 50), "A"),
    ("_PatDSA", "JPsiCR_chi2vsDCA_plot"): ("logNormChi2", "logDca", (50, 50), "A"),
    ("_DSA", "JPsiCR_chi2vsDCA_plot"): ("logNormChi2", "logDca", (50, 50), "A"),
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

optimization_param = None
common_signals_optimization = False

# ------------------------------------------
# Rebinning and projection settings
# ------------------------------------------

# you can specify custom binning for the 1D projection
custom_rebin = True
custom_projections_binning = [0, 0.5, 0.9, 1.5, 2.0]

# you can also use smart rebinning for the 1D projection, which will keep the relative error below a certain threshold
smart_rebin = False
smart_rebin_max_error = 0.30  # max allowed ralative error for smart rebinning

# or you can use standard rebinning for the 1D projection (the number is the rebin factor)
standard_rebin = 1

# rebinning factor for the 2D histograms of signals and backgrounds and optimization histograms
# (closure, error, min_n_events, significance, contamination)
rebin_2D = 4

background_hist_name=f"{background_collection}_{variable_1}_vs_{variable_2}{category}"
signal_hist_name=f"{signal_collection}_{variable_1}_vs_{variable_2}{category}"
if do_region == "SR_collinearityAngle_plot":
  background_hist_name=f"{background_collection}{category}_{variable_1}_vs_{variable_2}"
  signal_hist_name=f"{background_collection}{category}_{variable_1}_vs_{variable_2}"
histogram = Histogram2D(
    name=background_hist_name,
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
    "absCollinearityAngle": "|#Delta#Phi_{coll}|",
    "absPtLxyDPhi1": "|#Delta#phi(p_{T}^{#mu1}, L_{xy})|",
    "logNormChi2": "log_{10} #chi^{2} / ndof",
    "logDca": "log_{10}[DCA [cm]]",
}

# ------------------------------------------
# Samples settings
# ------------------------------------------

# base_path = "/data/dust/user/jniedzie/ttalps_cms"
base_path = "/data/dust/user/lrygaard/ttalps_cms"

skims = {
    "SR_collinearityAngle_plot": (
        "skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_nminus1"
    ),
    "SR_chi2vsDCA_plot": (
        "skimmed_looseSemimuonic_v3_SR", "_SRDimuonsNoChi2", "_genInfo"
    ),
    "JPsiCR_chi2vsDCA_plot": (
      ("skimmed_looseSemimuonic_v3_SR", "_JPsiDimuonsNoChi2", "_ABCD"),
      ("skimmed_looseSemimuonic_v3_SR", "_SRDimuonsNoChi2", "_genInfo"),
    ),
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
base_afs_path = f"/afs/desy.de/user/{username[0]}/{username}/{tea_ttalps_path}"
if not os.path.exists(f"{base_afs_path}/plots/2Dhists"):
  os.makedirs(f"{base_afs_path}/plots/2Dhists")
output_path = (
  f"{base_afs_path}/plots/2Dhists/results_{year}/results_"
  f"{do_region}_{background_collection}{background_skim[1]}"
)
if do_nonresonant_signal_as_background:
  output_path = (
    f"{base_afs_path}/plots/2Dhists/results_{year}/signal_resonances/results_{year}_"
    f"{do_region}{background_skim[1]}"
  )
  
output_path += "_data" if do_data else "_mc"
output_path += category

if optimization_param:
  output_path += "_"+optimization_param

hist_base_path = f"histograms"

background_hist_path = (
    f"{hist_base_path}"
    f"{background_skim[1]}{background_skim[2]}"
)
signal_hist_path = f"{hist_base_path}{signal_skim[1]}{signal_skim[2]}"

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

# used by ttalps_get_signal_events
signal_cross_section = 0.01

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
