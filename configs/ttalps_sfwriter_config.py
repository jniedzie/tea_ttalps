from ttalps_luminosities import get_luminosity
from ttalps_cross_sections import get_cross_sections
from ttalps_samples_list import dasBackgrounds2018

from Histogram import Histogram
from HistogramNormalizer import NormalizationType
from Sample import Sample, SampleType

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)

# TODO: figure out how to handle different SFs 
# - with another config or have one config for multiple corrections
# JPsi CR SFs
skim = "skimmed_looseSemimuonic_v2_SR"
hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_JPsiDimuons_LooseNonLeadingMuonsVertexSegmentMatch" # all SFs
base_path = "/data/dust/user/lrygaard/ttalps_cms"
output_name = "../data/JPsiCRsf2018.json"

collection = "BestDimuonVertex"
variable = "invMass"
backgrounds = dasBackgrounds2018
data = "collision_data2018/SingleMuon2018"
histograms = {}
for category in ("Pat", "PatDSA", "DSA"):
    hist_name = f"{collection}_{category}_{variable}"
    histograms[category] = Histogram(
        name=hist_name,
        title=hist_name,
        norm_type=NormalizationType.to_lumi,
        x_min=3.0,
        x_max=3.2
    )

samples = []
for background in backgrounds.keys():
    samples.append(
        Sample(
            name=background.split("/")[-1],
            file_path=f"{base_path}/{background}/{skim}/{hist_path}/histograms.root",
            type=SampleType.background,
            cross_sections=cross_sections,
        )
    )
samples.append(
    Sample(
        name="data",
        file_path=f"{base_path}/{data}_{skim}_{hist_path}.root",
        type=SampleType.data,
    )
)

# CorrectioWriter input
correction_name =  "JpsiInvMass"
correction_description = "Scale factors for J/Psi invariant mass"
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
