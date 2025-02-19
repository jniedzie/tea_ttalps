import ROOT
from ttalps_cross_sections import cross_sections

base_path = "/data/dust/user/jniedzie/ttalps_cms"
output_path = "../abcd_results"

lumi = 137190  # pb^-1


# ------------------------------------------
# ABCD calculation and optimization settings
# ------------------------------------------

# variables to use for the two ABCD axes
variable_1 = "LogLxySignificance"
variable_2 = "Log3Dangle"

# your chosen ABCD crossing point that will be used to make 1D projections
abcd_point = (-0.9, 0.0)

# optimization parameters
max_error = 1.0
max_closure = 10
min_n_events = 10


# ------------------------------------------
# Rebinning and projection settings
# ------------------------------------------

# you can specify custom binning for the 1D projection
custom_rebin = True
custom_projections_binning = [0, 0.5, 0.9, 1.5, 2.0]
# custom_projections_binning = [0, 0.6, 1.5, 2.0]

# you can also use smart rebinning for the 1D projection, which will keep the relative error below a certain threshold
smart_rebin = False
smart_rebin_max_error = 0.30  # max allowed ralative error for smaert rebinning

# or you can use standard rebinning for the 1D projection (the number is the rebin factor)
standard_rebin = 1

rebin_grid = 10  # rebinning factor for the 2D histograms of signals and backgrounds
# rebinning factor for the 2D optimization histograms (closure, error, min_n_events, significance)
rebin_optimization = 2


# ------------------------------------------
# Plotting settings
# ------------------------------------------

# axes limits for the 1D projection
y_max = 30
y_max_ratio = 10

# you can specify colors for the signals in the projection (otherwise they will default to red)
signal_colors = {
    ("1", "1e1"): ROOT.kGreen+1,
    ("1", "1e2"): ROOT.kCyan+1,
    ("12", "1e1"): ROOT.kBlue,
    ("12", "1e2"): ROOT.kViolet,
}

signal_label_position = (0.1, 0.1)
projections_legend_position = (0.6, 0.6, 0.9, 0.9)

variable_1_min = -3.0
variable_1_max = 1.0
variable_2_min = -2.0
variable_2_max = 2.0

background_color = ROOT.kBlack
signal_color = ROOT.kRed

abcd_line_color = ROOT.kCyan+1
abcd_line_width = 2

true_background_color = ROOT.kRed
true_background_description = "Background in A"

predicted_background_color = ROOT.kBlack
predicted_background_description = "ABCD prediction"

projection_y_title = "Events (2018, 137 fb^{-1})"
ratio_y_title = "True / Pred  "

# you can specify custom names for the variables to be displayed in the plots
nice_names = {
    "Lxy": "L_{xy} (cm)",
    "LxySignificance": "L_{xy} significance",
    "absCollinearityAngle": "|#theta_{coll}|",
    "3Dangle": "#alpha_{3D}",
    "LogLxy": "log_{10}[L_{xy} (cm)]",
    "LogLxySignificance": "log_{10}[L_{xy} significance]",
    "LogAbsCollinearityAngle": "log_{10}[|#theta_{coll}|]",
    "Log3Dangle": "log_{10}[#alpha_{3D}]",
}

# ------------------------------------------
# Samples settings
# ------------------------------------------

skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"
hist_dir = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons"
signal_path_pattern = "signals/tta_mAlp-{}GeV_ctau-{}mm/{}/{}/histograms.root"

background_path_pattern = "backgrounds2018/{}/{}/{}/histograms.root"

# signal points for which to run ABCD analysis
masses = ["0p35", "1", "2", "12", "60"]
ctaus = ["1e-5", "1e0", "1e1", "1e2", "1e3", "1e5"]

# masses = ["1", "12"]
# ctaus = ["1e1", "1e2"]

# select which region to use (obsolete, but needed if you already have histograms with region names)
# region = "_JPsiCR"
region = "_SR"

backgrounds = (
    "TTToSemiLeptonic",
    "TTToHadronic",
    "TTTo2L2Nu",

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

    "QCD_Pt-15To20",
    "QCD_Pt-20To30",
    "QCD_Pt-30To50",
    "QCD_Pt-50To80",
    "QCD_Pt-80To120",
    "QCD_Pt-120To170",
    "QCD_Pt-170To300",
    "QCD_Pt-300To470",
    "QCD_Pt-470To600",
    "QCD_Pt-600To800",
    "QCD_Pt-800To1000",
    "QCD_Pt-1000",
)

background_params = []
for b in backgrounds:
    for k, v in cross_sections.items():
        if b in k:
            background_params.append((b, v))
            break

z_params = {
    "closure": ("|True - Pred|/True x 100 %", 0, 100, False),
    "error": ("|True - Pred|/#sqrt{#Delta Pred^{2} + #Delta True^{2}}", 0, 5, False),
    "min_n_events": ("min(A, B, C, D)", 0, 100, True)
}

