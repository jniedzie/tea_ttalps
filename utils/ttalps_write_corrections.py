import os
import glob
from copy import deepcopy
import ROOT
from array import array
import random

from ttalps_samples_list import dasBackgrounds2018
from Sample import Sample, SampleType

from CorrectionWriter import CorrectionWriter
from ttalps_luminosities import get_luminosity
from ttalps_cross_sections import get_cross_sections
from get_dataMC_ratio_plots import get_background_stack, get_data_hist, get_asymmetric_uncertainties, get_dataMC_ratio

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)


def write_Jspi_invariant_mass_corrections(correctionWriter):
    skim = "skimmed_looseSemimuonic_v2_SR"
    hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_JPsiDimuons_LooseNonLeadingMuonsVertexSegmentMatch" # all SFs
    base_path = "/data/dust/user/lrygaard/ttalps_cms"
    collection = "BestDimuonVertex"
    variable = "invMass"
    backgrounds = dasBackgrounds2018
    data = "collision_data2018/SingleMuon2018"

    scale_factors = {}
    for category in ("Pat", "PatDSA", "DSA"):
        hist_name = f"{collection}_{category}_{variable}"

        background_samples = []
        for background in backgrounds.keys():
            background_samples.append(
                Sample(
                    name=background.split("/")[-1],
                    file_path=f"{base_path}/{background}/{skim}/{hist_path}/histograms.root",
                    type=SampleType.background,
                    cross_sections=cross_sections,
                )
            )
        background_stack = get_background_stack("", hist_name, background_samples)
        data_sample = Sample(
            name="data",
            file_path=f"{base_path}/{data}_{skim}_{hist_path}.root",
            type=SampleType.data,
        )
        data_hist = get_data_hist("", hist_name, data_sample)

        data_yield, data_uncertainty_down, data_uncertainty_up = get_asymmetric_uncertainties(data_hist)
        background_yield, background_uncertainty_down, background_uncertainty_up = get_asymmetric_uncertainties(background_stack.GetStack().Last())
        
        ratio,ratio_uncertainty_down,ratio_uncertainty_up = get_dataMC_ratio(data_yield, data_uncertainty_down, data_uncertainty_up, background_yield, background_uncertainty_down, background_uncertainty_up)
        
        scale_factors[category] = [ratio, ratio_uncertainty_up, ratio_uncertainty_down]

    category_input = {"name": "dimuon_category", "type": "string", "description": "Dimuon categories Pat, PatDSA or DSA"}
    scale_factors_input = {"name": "scale_factors", "type": "string", "description": "Choose nominal scale factor or one of the uncertainties"}
    category_edges = ["Pat", "PatDSA", "DSA"]
    scale_factors_edges = ["nominal", "up", "down"]

    correctionWriter.add_multibinned_correction(
        name= "JpsiInvMassSFs",
        description="Scale factors for J/Psi invariant mass",
        version=1,
        inputs=[category_input, scale_factors_input],
        output={"name": "weight", "type": "real", "description": "Output scale factor (nominal) or uncertainty"},
        edges=[ category_edges, scale_factors_edges ],
        data=[scale_factors["Pat"], scale_factors["PatDSA"], scale_factors["DSA"]],
        flow="error"
    )

def write_example_pt_eta_corrections(correctionWriter):
    pt_input = {"name": "pt", "type": "real", "description": "Probe pt"}
    pt_edges = [0, 10, 20, 30] # 3 bins
    eta_input = {"name": "eta", "type": "real", "description": "Probe eta"}
    eta_edges = [-2.4, 0.0, 2.4] # 2 bins
    scale_factors_input = {"name": "scale_factors", "type": "string", "description": "Choose nominal scale factor or one of the uncertainties"}
    scale_factors_edges = ["nominal", "up", "down"]
    values_pt1 = [[0.1, 0.2, 0.3],[0.4, 0.5, 0.6]]  # [nominal, up, down] for each eta bin
    values_pt2 = [[0.7, 0.8, 0.9],[1.0, 1.1, 1.2]]
    values_pt3 = [[1.3, 1.4, 1.5],[1.6, 1.7, 1.8]]
    correctionWriter.add_multibinned_correction(
        name= "testSF",
        description="Example test SF",
        version=1,
        inputs=[pt_input, eta_input, scale_factors_input],
        output={"name": "weight", "type": "real", "description": "Output scale factor (nominal) or uncertainty"},
        edges=[ pt_edges, eta_edges, scale_factors_edges ],
        data=[values_pt1, values_pt2, values_pt3],
        flow="error"
    )

def main():

    correctionWriter = CorrectionWriter()

    write_Jspi_invariant_mass_corrections(correctionWriter)

    write_example_pt_eta_corrections(correctionWriter)

    correctionWriter.save_json(f"{os.getcwd()}/../data/sf2018.json")


if __name__ == '__main__':
  main()
