import numpy as np

from ttalps_luminosities import get_luminosity
from ttalps_cross_sections import get_cross_sections
from ttalps_samples_list import dasBackgrounds2018,dasBackgrounds2017,dasBackgrounds2016preVFP,dasBackgrounds2016postVFP
from ttalps_samples_list import dasBackgrounds2022postEE,dasBackgrounds2022preEE,dasBackgrounds2023preBPix,dasBackgrounds2023postBPix

from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType
from Sample import Sample, SampleType

# years = ["2022postEE",]
years = ["2016preVFP", "2016postVFP", "2017", "2018", "2022preEE", "2022postEE", "2023preBPix", "2023postBPix",]
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
extrapolate_in_x = False
extrapolate_in_y = False

base_path = "/data/dust/user/lrygaard/ttalps_cms"

skim = ("skimmed_looseSemimuonic_v3_SR", "_JPsiDimuons", "")

hist_path = f"histograms{skim[1]}{skim[2]}" # all SFs 2018

samples = []
year_string = ""
for year in years:
    year_string += year
    cross_sections = get_cross_sections(year)
    luminosity = get_luminosity(year)

    backgrounds = globals()[f"dasBackgrounds{year}"]
    for background in backgrounds.keys():
        samples.append(
            Sample(
                name=background.split("/")[-1],
                file_path=f"{base_path}/{background}/{skim[0]}/{hist_path}/histograms.root",
                type=SampleType.background,
                cross_sections=cross_sections,
                luminosity=luminosity,
                line_alpha=0,
                line_style=1,
                fill_alpha=0.7,
                marker_size=0,
                marker_style=0,
                year=year,
            )
        )
    data = f"collision_data{year}/SingleMuon{year}"
    if "2022" in year or "2023" in year:
        data = f"collision_data{year}/Muon{year}"
    samples.append(
        Sample(
            name=f"data_{year}",
            file_path=f"{base_path}/{data}_{skim[0]}_{hist_path}.root",
            type=SampleType.data,
            line_style=1,
            line_alpha=1,
            fill_alpha=0,
            marker_size=0.7,
            marker_style=20,
            year=year,
        )
    )
year = year_string

histogram1D = None
histograms1D = {}
histogram2D = None
histograms2D = {}

# TODO: figure out how to handle different SFs 
# - with another config or have one config for multiple corrections

####################    JPsi CR Dimuon Efficiency SFs  (multiple 1D histograms)  ####################
exclude_backgrounds_with_less_than = 0  # entries
# exclude_backgrounds_with_less_than = 3  # entries
# if year == "2022postEE":
#     exclude_backgrounds_with_less_than = 4

collection = "BestDimuonVertex"
variable = "invMassJPsiBin"
output_name = f"../data/dimuonEffSFs{year_string}_{variable}_DSAChi2DCA1p5.json"

for category in ("Pat", "PatDSA", "DSA"):
# for category in ("DSA",):
    hist_name = f"{collection}_{category}_{variable}"
    # hist_name = f"Event_n{collection}_{category}"
    histograms1D[category] = Histogram(
        name=hist_name,
        title=hist_name,
        norm_type=NormalizationType.to_lumi,
    )

# CorrectioWriter input
correction_name =  "dimuonEff"
correction_description = "Scale factors for dimuon efficiency given from J/Psi invariant mass distribution"
correction_version = 1
correction_inputs = [
    {"name": "dimuon_category", "type": "string", "description": "Dimuon categories Pat, PatDSA or DSA"},
    {"name": "scale_factors", "type": "string", "description": "Choose nominal scale factor or one of the uncertainties"}
]
correction_output = {"name": "weight", "type": "real", "description": "Output scale factor (nominal) or uncertainty"}
correction_edges = [
    ["Pat", "PatDSA", "DSA"],
    ["nominal", "up", "down"]
]
correction_flow = "error"

####################    tt+1DSA Muon Efficiency SFs (one 1D histogram)  ####################
# output_name = f"../data/DSAEffSFs{year}_ttbarLike1DSA_segmentMatchedDSA_pt.json"
# exclude_backgrounds_with_less_than = 0  # entries

# collection = "LooseDSAMuonsSegmentMatch"
# variable_bins = []
# variable = "pt_irr2"
# hist_name = f"{collection}_{variable}"
# histogram1D = Histogram(
#     name=hist_name,
#     title=hist_name,
#     norm_type=NormalizationType.to_lumi,
# )

# # CorrectioWriter input
# correction_name =  "DSAEff"
# correction_description = "Scale factors for DSA muon efficiency given from ttbar + 1 DSA muon CR pt distribution"
# correction_version = 1
# correction_inputs = [
#     {"name": variable, "type": "real", "description": "pt of the DSA muon candidate"},
#     {"name": "scale_factors", "type": "string", "description": "Choose nominal scale factor or one of the uncertainties"}
# ]
# correction_output = {"name": "weight", "type": "real", "description": "Output scale factor (nominal) or uncertainty"}
# correction_edges = [
#     variable_bins,
#     ["nominal", "up", "down"]
# ]
# correction_flow = "error"

####################    tt+1DSA Muon Efficiency SFs (one 2D histogram)   ####################
# # output_name = f"../data/DSAEffSFs{year}_ttbarLike1DSA_pt_absdxy.json"
# output_name = f"../data/DSAEffSFs{year}_ttbarLike1DSA_segmentMatchedDSA_pt_absdxy.json"
# # output_name = "../data/DSAEffSFs2018_ttbarLike1DSA_pt_dxy.json"
# exclude_backgrounds_with_less_than = 0  # entries
# collection = "LooseDSAMuonsSegmentMatch"

# variable1 = "pt_irr"
# variable2 = "absDxyPVTraj_irr"
# # variable2 = "dxyPVTraj_irr"
# variable1_bins = []
# variable2_bins = []

# # extrapolating missing SF values:
# extrapolate_in_x = False # dxy in x
# extrapolate_in_y = True # extrapolate over pt in y
# # options: const, lin, 2Dpoly
# extrapolation_function = "const" 
# if extrapolate_in_x or extrapolate_in_y:
#     # output_name = f"../data/DSAEffSFs{year}_ttbarLike1DSA_pt_absdxy_{extrapolation_function}.json"
#     output_name = f"../data/DSAEffSFs{year}_ttbarLike1DSA_segmentMatchedDSA_pt_absdxy_{extrapolation_function}.json"

# hist_name = f"{collection}_{variable2}_vs_{variable1}"
# histogram2D = Histogram2D(
#     name=hist_name,
#     title=hist_name,
#     norm_type=NormalizationType.to_lumi,
#     x_rebin = 1,
#     y_rebin = 1,
# )

# # CorrectioWriter input
# correction_name =  "DSAEff"
# correction_description = "Scale factors for DSA muon efficiency given from ttbar + 1 DSA muon CR pt and |dxy| distribution"
# correction_version = 1
# correction_inputs = [
#     {"name": variable1, "type": "real", "description": "pt of the DSA muon candidate"},
#     {"name": variable2, "type": "real", "description": "absolute value of dxy from the PV of the DSA muon candidate"},
#     {"name": "scale_factors", "type": "string", "description": "Choose nominal scale factor or one of the uncertainties"}
# ]
# correction_output = {"name": "weight", "type": "real", "description": "Output scale factor (nominal) or uncertainty"}
# correction_edges = [
#     variable1_bins,
#     variable2_bins,
#     ["nominal", "up", "down"]
# ]
# correction_flow = "error"

####################    1D hist SFs    ####################
# output_name = "../data/DSAEffSFs2018_ttbarLike1DSA.json"
# collection = "LooseDSAMuons"
# variable_bins = []

# variable = "eta"
# for i in np.arange(-2.5, 2.55, 0.05):
#     i_rounded = round(i, 2)
#     variable_bins.append(i_rounded)
# print("variable_bins:")
# print(variable_bins)

# # variable = "pt"
# # for i in range(0,300,10):
# #   variable_bins.append(i)
# # for i in range(300,600,20):
# #   variable_bins.append(i)
# # for i in range(600,2000,100):
# #   variable_bins.append(i)

# hist_name = f"{collection}_{variable}"

# histograms = {}
# for variable_i in range(len(variable_bins) - 1):
#     if variable_i == len(variable_bins) - 1:
#         continue
#     minVariable = variable_bins[variable_i]
#     maxVariable = variable_bins[variable_i + 1]
#     x_bin = minVariable
#     hist_title = f"{variable}-{minVariable}-{maxVariable}"
#     histograms[x_bin] = Histogram(
#         name=hist_name,
#         title=hist_title,
#         norm_type=NormalizationType.to_lumi,
#         x_min=minVariable,
#         x_max=maxVariable
#     )

# # CorrectioWriter input
# correction_name =  "DSAEff"
# correction_description = "Scale factors for DSA muon efficiency given from ttbar + 1 DSA muon CR eta distribution"
# correction_version = 1
# correction_inputs = [
#     {"name": variable, "type": "real", "description": "eta of the DSA muon candidate"},
#     {"name": "scale_factors", "type": "string", "description": "Choose nominal scale factor or one of the uncertainties"}
# ]
# correction_output = {"name": "weight", "type": "real", "description": "Output scale factor (nominal) or uncertainty"}
# correction_edges = [
#     variable_bins,
#     ["nominal", "up", "down"]
# ]
# correction_flow = "error"