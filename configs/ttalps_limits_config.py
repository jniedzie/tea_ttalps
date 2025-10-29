from Sample import Sample, SampleType
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType
from ttalps_cross_sections import get_cross_sections, get_theory_cross_section
from ttalps_luminosities import get_luminosity_uncertainty_default
from TTAlpsABCDConfigHelper import TTAlpsABCDConfigHelper
import ttalps_abcd_config as abcd_config
import os

# years = ["2017","2018","2022preEE","2022postEE"]
years = abcd_config.years
year = years[0]
year_str = ""
for year_ in years:
  year_str += year_
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)
category = abcd_config.category
lumi_uncertainty = get_luminosity_uncertainty_default(year)

username = os.getenv("USER")
base_path = f"/data/dust/user/jniedzie/ttalps_cms/"
combine_path = "/afs/desy.de/user/j/jniedzie/combine/CMSSW_14_1_0_pre4/src/"
base_output_path = "/afs/desy.de/user/j/jniedzie/tea_ttalps"
if username == "lrygaard":
  base_path = f"/data/dust/user/lrygaard/ttalps_cms/"
  combine_path = "/afs/desy.de/user/l/lrygaard/Combine/CMSSW_14_1_0_pre4/src/"
  base_output_path = "/afs/desy.de/user/l/lrygaard/TTALP/tea_ttalps"

# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_jecSFs"
# hist_path = f"histograms_muonSFs_dsamuonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_jecSFs"
# hist_path = f"histograms_muonSFs_dsamuonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_dimuonEffSFs_jecSFs"

# SR dimuon cuts applied
signal_hist_path = (
    f"{hist_path}"
    f"{abcd_config.signal_skim[1]}{abcd_config.signal_skim[2]}"
)

background_hist_path = (
    f"{hist_path}"
    f"{abcd_config.background_skim[1]}{abcd_config.background_skim[2]}"
)

# to print rates and uncertainty:
use_combined_limits = True

# extra_str = "_newSelection"
extra_str = "_newSelection_dsaSFs"
# extra_str = "_newSelection_dsaSFs_dimuonEffSFs"
datacards_output_path = f"{base_output_path}/limits/limits_{year_str}/datacards{extra_str}_{abcd_config.do_region}/"
plots_output_path = f"{base_output_path}/limits/limits_{year_str}/plots{extra_str}/"

results_output_path = f"{base_output_path}/limits/limits_{year_str}/results{extra_str}/"

# If True, poisson error on empty bins (1.84) will be added to data histograms
add_uncertainties_on_zero = False

luminosity = abcd_config.luminosity_sum

do_abcd = True
use_abcd_prediction = True  # if False, it will use the actual number of events in the signal bin
include_shapes = True

if do_abcd:
  include_shapes = False  # currently not supported for ABCD

skip_combine = False

# Sample(
  #     name="data_obs",
  #     file_path=f"{base_path}/histograms/data.root",
  #     type=SampleType.data,
  # ),


config_helper = TTAlpsABCDConfigHelper(
    years,
    abcd_config.background_skim,
    abcd_config.category,
    base_path,
    background_hist_path,
)

background_samples, backgrounds = config_helper.get_background_samples()
signal_samples, signals = config_helper.get_signal_samples()
samples = signal_samples + background_samples

if not do_abcd:
  # Use this 1D hisogram to calculate limits using shapes and MC backgrounds
  variable = "LxySignificance"
  # variable = "Lxy"

  histogram = Histogram(
      name=f"{abcd_config.collection}{abcd_config.category}_{variable}",
      norm_type=NormalizationType.to_lumi,
      x_max=140,
      rebin=5
  )
else:
  # Use this 2D histogram to calculate limits with cut-and-count and optionally ABCD background prediction
  abcd_point = abcd_config.abcd_point
  rebin_2D = abcd_config.rebin_2D
  histogram = abcd_config.histogram
  signal_bin = abcd_config.signal_bin
  exclude_backgrounds_for_years = abcd_config.exclude_backgrounds_for_years


# List nuisance parameters (they will only be added for processes for which they were listed)
nuisances = {
    "bTaggingMedium_down_correlated": "variation",
    "bTaggingMedium_down_uncorrelated": "variation",
    "bTaggingMedium_up_correlated": "variation",
    "bTaggingMedium_up_uncorrelated": "variation",

    # "dimuonEff_down": "variation",
    # "dimuonEff_up": "variation",
    # "DSAEff_down": "variation",
    # "DSAEff_up": "variation",

    # "abcd_nonClosure": "closure",
    "abcd_unc": "abcd",
    "lumi": {
        "signal": lumi_uncertainty,
        "bkg": lumi_uncertainty,
    }
}

if abcd_config.category != "_DSA":
  nuisances["muonIDLoose_systdown"] = "variation"
  nuisances["muonIDLoose_systup"] = "variation"

if abcd_config.category != "_Pat":
  nuisances["dsamuonID_down_syst"] = "variation"
  nuisances["dsamuonID_up_syst"] = "variation"
  nuisances["dsamuonReco_cosmic_down"] = "variation"
  nuisances["dsamuonReco_cosmic_up"] = "variation"

if "2016" in year_str or "2017" in year_str or "2018" in year_str:
  jec_year = year
  if "2016" in year:
    jec_year = "2016"
  nuisances["muonReco_systdown"] = "variation"
  nuisances["muonReco_systup"] = "variation"
  nuisances["muonTrigger_systdown"] = "variation"
  nuisances["muonTrigger_systup"] = "variation"
  nuisances["PUjetIDtight_down"] = "variation"
  nuisances["PUjetIDtight_up"] = "variation"
  nuisances["jecMC_Regrouped_Absolute_down"] = "variation"
  nuisances["jecMC_Regrouped_Absolute_up"] = "variation"
  nuisances[f"jecMC_Regrouped_Absolute_{jec_year}_down"] = "variation"
  nuisances[f"jecMC_Regrouped_Absolute_{jec_year}_up"] = "variation"
  nuisances["jecMC_Regrouped_FlavorQCD_down"] = "variation"
  nuisances["jecMC_Regrouped_FlavorQCD_up"] = "variation"
  nuisances["jecMC_Regrouped_BBEC1_down"] = "variation"
  nuisances["jecMC_Regrouped_BBEC1_up"] = "variation"
  nuisances[f"jecMC_Regrouped_BBEC1_{jec_year}_down"] = "variation"
  nuisances[f"jecMC_Regrouped_BBEC1_{jec_year}_up"] = "variation"
  nuisances["jecMC_Regrouped_EC2_down"] = "variation"
  nuisances["jecMC_Regrouped_EC2_up"] = "variation"
  nuisances[f"jecMC_Regrouped_EC2_{jec_year}_down"] = "variation"
  nuisances[f"jecMC_Regrouped_EC2_{jec_year}_up"] = "variation"
  nuisances["jecMC_Regrouped_HF_down"] = "variation"
  nuisances["jecMC_Regrouped_HF_up"] = "variation"
  nuisances[f"jecMC_Regrouped_HF_{jec_year}_down"] = "variation"
  nuisances[f"jecMC_Regrouped_HF_{jec_year}_up"] = "variation"
  nuisances["jecMC_Regrouped_RelativeBal_down"] = "variation"
  nuisances["jecMC_Regrouped_RelativeBal_up"] = "variation"
  nuisances[f"jecMC_Regrouped_RelativeSample_{jec_year}_down"] = "variation"
  nuisances[f"jecMC_Regrouped_RelativeSample_{jec_year}_up"] = "variation"

if "2022" in year_str or "2023" in year_str:
  nuisances["jecMC_AbsoluteMPFBias_up"] = "variation"
  nuisances["jecMC_AbsoluteMPFBias_down"] = "variation"
  nuisances["jecMC_AbsoluteScale_up"] = "variation"
  nuisances["jecMC_AbsoluteScale_down"] = "variation"
  nuisances["jecMC_AbsoluteStat_up"] = "variation"
  nuisances["jecMC_AbsoluteStat_down"] = "variation"
  nuisances["jecMC_FlavorQCD_up"] = "variation"
  nuisances["jecMC_FlavorQCD_down"] = "variation"
  nuisances["jecMC_Fragmentation_up"] = "variation"
  nuisances["jecMC_Fragmentation_down"] = "variation"
  nuisances["jecMC_PileUpDataMC_up"] = "variation"
  nuisances["jecMC_PileUpDataMC_down"] = "variation"
  nuisances["jecMC_PileUpPtBB_up"] = "variation"
  nuisances["jecMC_PileUpPtBB_down"] = "variation"
  nuisances["jecMC_PileUpPtEC1_up"] = "variation"
  nuisances["jecMC_PileUpPtEC1_down"] = "variation"
  nuisances["jecMC_PileUpPtEC2_up"] = "variation"
  nuisances["jecMC_PileUpPtEC2_down"] = "variation"
  nuisances["jecMC_PileUpPtHF_up"] = "variation"
  nuisances["jecMC_PileUpPtHF_down"] = "variation"
  nuisances["jecMC_PileUpPtRef_up"] = "variation"
  nuisances["jecMC_PileUpPtRef_down"] = "variation"
  nuisances["jecMC_RelativeFSR_up"] = "variation"
  nuisances["jecMC_RelativeFSR_down"] = "variation"
  nuisances["jecMC_RelativeJEREC1_up"] = "variation"
  nuisances["jecMC_RelativeJEREC1_down"] = "variation"
  nuisances["jecMC_RelativeJEREC2_up"] = "variation"
  nuisances["jecMC_RelativeJEREC2_down"] = "variation"
  nuisances["jecMC_RelativeJERHF_up"] = "variation"
  nuisances["jecMC_RelativeJERHF_down"] = "variation"
  nuisances["jecMC_RelativePtBB_up"] = "variation"
  nuisances["jecMC_RelativePtBB_down"] = "variation"
  nuisances["jecMC_RelativePtEC1_up"] = "variation"
  nuisances["jecMC_RelativePtEC1_down"] = "variation"
  nuisances["jecMC_RelativePtEC2_up"] = "variation"
  nuisances["jecMC_RelativePtEC2_down"] = "variation"
  nuisances["jecMC_RelativePtHF_up"] = "variation"
  nuisances["jecMC_RelativePtHF_down"] = "variation"
  nuisances["jecMC_RelativeBal_up"] = "variation"
  nuisances["jecMC_RelativeBal_down"] = "variation"
  nuisances["jecMC_RelativeSample_up"] = "variation"
  nuisances["jecMC_RelativeSample_down"] = "variation"
  nuisances["jecMC_RelativeStatEC_up"] = "variation"
  nuisances["jecMC_RelativeStatEC_down"] = "variation"
  nuisances["jecMC_RelativeStatFSR_up"] = "variation"
  nuisances["jecMC_RelativeStatFSR_down"] = "variation"
  nuisances["jecMC_RelativeStatHF_up"] = "variation"
  nuisances["jecMC_RelativeStatHF_down"] = "variation"
  nuisances["jecMC_SinglePionECAL_up"] = "variation"
  nuisances["jecMC_SinglePionECAL_down"] = "variation"
  nuisances["jecMC_SinglePionHCAL_up"] = "variation"
  nuisances["jecMC_SinglePionHCAL_down"] = "variation"
  nuisances["jecMC_TimePtEta_up"] = "variation"
  nuisances["jecMC_TimePtEta_down"] = "variation"
