import numpy as np

from ttalps_luminosities import get_luminosity
from ttalps_cross_sections import get_cross_sections
from ttalps_samples_list import dasBackgrounds2018, dasBackgrounds2022postEE, dasBackgrounds2018Devel

from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType
from Sample import Sample, SampleType

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)

base_path = "/data/dust/user/lrygaard/ttalps_cms"

# backgrounds = dasBackgrounds2018
# data = "collision_data2018/SingleMuon2018"
backgrounds = dasBackgrounds2018Devel
data = "collision_data2018/SingleMuon2018Devel"
# backgrounds = dasBackgrounds2022postEE
# data = "collision_data2022postEE/Muon2022postEE"

# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_JPsiDimuonsDSAChi2DCADPhi", "_LooseNonLeadingMuonsVertexSegmentMatch")
skim = ("skimmed_looseSemimuonic_v2_ttbarLike1DSA", "", "")
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_jecSFs{skim[1]}{skim[2]}" # all SFs 2018
hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_DSAEffSFs_jecSFs{skim[1]}{skim[2]}" # all SFs 2018
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_dimuonEffSFs_jecSFs{skim[1]}{skim[2]}" # all SFs 2018

exclude_backgrounds_with_less_than = 3  # entries

samples = []
for background in backgrounds.keys():
    samples.append(
        Sample(
            name=background.split("/")[-1],
            file_path=f"{base_path}/{background}/{skim[0]}/{hist_path}/histograms.root",
            type=SampleType.background,
            cross_sections=cross_sections,
        )
    )
samples.append(
    Sample(
        name="data",
        file_path=f"{base_path}/{data}_{skim[0]}_{hist_path}.root",
        type=SampleType.data,
    )
)

# histograms = {}
# histograms2D = {}
# histograms3D = {} # hists with 3 variable binnings, eg. pt, eta, category

# TODO: figure out how to handle different SFs 
# - with another config or have one config for multiple corrections

####################    JPsi CR SFs    ####################
# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_JPsiDimuonsDSAChi2DCADPhi", "_LooseNonLeadingMuonsVertexSegmentMatch")
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_jecSFs{skim[1]}{skim[2]}" # all SFs 2018
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_jecSFs{skim[1]}{skim[2]}" # all SFs 2022postEE
# output_name = "../data/JPsiCRsf2018.json"
# output_name = "../data/dimuonEffSFs2022postEE_newMatching_JPsiDimuonsDSAChi2DCADPhi.json"
# collection = "BestDimuonVertex"
# variable = "invMass"
# for category in ("Pat", "PatDSA", "DSA"):
#     hist_name = f"{collection}_{category}_{variable}"
#     histograms[category] = Histogram(
#         name=hist_name,
#         title=hist_name,
#         norm_type=NormalizationType.to_lumi,
#         x_min=3.0,
#         x_max=3.2
#     )

# CorrectioWriter input
# correction_name =  "dimuonEff"
# correction_description = "Scale factors for dimuon efficiency given from J/Psi invariant mass distribution"
# correction_version = 1
# correction_inputs = [
#     {"name": "dimuon_category", "type": "string", "description": "Dimuon categories Pat, PatDSA or DSA"},
#     {"name": "scale_factors", "type": "string", "description": "Choose nominal scale factor or one of the uncertainties"}
# ]
# correction_output = {"name": "weight", "type": "real", "description": "Output scale factor (nominal) or uncertainty"}
# correction_edges = [
#     ["Pat", "PatDSA", "DSA"],
#     ["nominal", "up", "down"]
# ]
# correction_flow = "error"

####################    2D hist SFs    ####################

# output_name = "../data/DSAEffSFs2018_ttbarLike1DSA_pt_dxy.json"
output_name = "../data/DSAEffSFs2018_ttbarLike1DSA_pt_dxy_devel.json"
collection = "LooseDSAMuons"

# variable1 = "logPt"
# variable2 = "logDxyPVTraj"
# variable1 = "pt"
# variable2 = "dxyPVTraj"
variable1 = "pt_irr"
variable2 = "dxyPVTraj_irr"
variable1_bins = []
variable2_bins = []
# for i in range(0,300,10):
#   variable1_bins.append(i)
# for i in range(300,600,50):
#   variable1_bins.append(i)
# for i in range(600,2000,100):
#   variable1_bins.append(i)
# for i in np.arange(-2.5, 2.55, 0.1):
#     i_rounded = round(i, 2)
#     variable2_bins.append(i_rounded)
# pt-eta bins
# for i in range(0,150,10):
#   variable1_bins.append(i)
# for i in range(150,400,50):
#   variable1_bins.append(i)
# for i in range(400,800,200):
#   variable1_bins.append(i)
# for i in range(800,2400,400):
#   variable1_bins.append(i)
# for i in np.arange(-2.5, -2.0, 0.25):
#     i_rounded = round(i, 2)
#     variable2_bins.append(i_rounded)
# for i in np.arange(-2.0, 2.0, 0.5):
#     i_rounded = round(i, 2)
#     variable2_bins.append(i_rounded)
# for i in np.arange(2.0, 2.75, 0.25):
#     i_rounded = round(i, 2)
#     variable2_bins.append(i_rounded)

# pt-dxy bins
# for i in range(0,150,5):
#     variable1_bins.append(i)
# for i in range(150,450,100):
#     variable1_bins.append(i)
# for i in range(450,2000,150):
#     variable1_bins.append(i)
# variable1_bins.append(2000)
# for i in np.arange(-500, -203, 29):
#     i_rounded = round(i, 2)
#     variable2_bins.append(i_rounded)
# for i in np.arange(-203, 203, 7):
#     i_rounded = round(i, 2)
#     variable2_bins.append(i_rounded)
# for i in np.arange(203, 500, 29):
#     i_rounded = round(i, 2)
#     variable2_bins.append(i_rounded)
# variable2_bins.append(500)

# log pt - log dxy bins
# for i in np.arange(-1.,3.,0.16):
#     i_rounded = round(i, 2)
#     variable1_bins.append(i_rounded)
# for i in np.arange(-5.,3.,0.32):
#     i_rounded = round(i, 2)
#     variable2_bins.append(i_rounded)

# print(f"variable1_bins: {variable1_bins}")
# print(f"variable2_bins: {variable2_bins}")

hist_name = f"{collection}_{variable2}_vs_{variable1}"
histogram2D = Histogram2D(
    name=hist_name,
    title=hist_name,
    norm_type=NormalizationType.to_lumi,
    x_rebin = 1,
    y_rebin = 1,
)

# for variable1_i in range(len(variable1_bins) - 1):
#     if variable1_i == len(variable1_bins) - 1:
#         continue
#     minVariable1 = variable1_bins[variable1_i]
#     maxVariable1 = variable1_bins[variable1_i + 1]
#     x_bin = minVariable1
#     histograms2D[x_bin] = {}
#     for variable2_i in range(len(variable2_bins) - 1):
#         if variable2_i == len(variable2_bins) - 1:
#             continue
#         minVariable2 = variable2_bins[variable2_i]
#         maxVariable2 = variable2_bins[variable2_i + 1]
#         y_bin = minVariable2
#         histograms2D[x_bin][y_bin] = {}
#         hist_title = f"{variable1}-{minVariable1}-{maxVariable1}_{variable2}-{minVariable2}-{maxVariable2}"
#         histograms2D[x_bin][y_bin] = Histogram2D(
#             name=hist_name,
#             title=hist_title,
#             norm_type=NormalizationType.to_lumi,
#             x_min=minVariable2,
#             x_max=maxVariable2,
#             y_min=minVariable1,
#             y_max=maxVariable1,
#         )

# CorrectioWriter input
correction_name =  "DSAEff"
correction_description = "Scale factors for DSA muon efficiency given from ttbar + 1 DSA muon CR pt and eta distribution"
correction_version = 1
correction_inputs = [
    {"name": variable1, "type": "real", "description": "pt of the DSA muon candidate"},
    {"name": variable2, "type": "real", "description": "dxy of the DSA muon candidate"},
    {"name": "scale_factors", "type": "string", "description": "Choose nominal scale factor or one of the uncertainties"}
]
correction_output = {"name": "weight", "type": "real", "description": "Output scale factor (nominal) or uncertainty"}
correction_edges = [
    variable1_bins,
    variable2_bins,
    ["nominal", "up", "down"]
]
correction_flow = "error"

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