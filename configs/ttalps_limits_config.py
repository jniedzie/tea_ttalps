from Sample import Sample, SampleType
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType
from ttalps_cross_sections import get_cross_sections, get_theory_cross_section
from ttalps_samples_list import dasSignals2018
from TTAlpsABCDConfigHelper import TTAlpsABCDConfigHelper
import ttalps_abcd_config as abcd_config
import os

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)

username = os.getenv("USER")
base_path = f"/data/dust/user/jniedzie/ttalps_cms/"
combine_path = "/afs/desy.de/user/j/jniedzie/combine/CMSSW_14_1_0_pre4/src/"
base_output_path = "/afs/desy.de/user/j/jniedzie/tea_ttalps"
if username == "lrygaard":
  base_path = f"/data/dust/user/lrygaard/ttalps_cms/"
  combine_path = "/afs/desy.de/user/l/lrygaard/Combine/CMSSW_14_1_0_pre4/src/"
  base_output_path = "/afs/desy.de/user/l/lrygaard/TTALP/tea_ttalps"

# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs"
hist_path = f"histograms_muonSFs_muonTriggerIsoMu24SFs_pileupSFs_bTaggingSFs_PUjetIDSFs_JpsiInvMassSFs"
# SR dimuon cuts applied
signal_hist_path = (
    f"{hist_path}"
    f"{abcd_config.signal_skim[1]}{abcd_config.signal_skim[2]}"
)

background_hist_path = (
    f"{hist_path}"
    f"{abcd_config.background_skim[1]}{abcd_config.background_skim[2]}"
)


datacards_output_path = f"{base_output_path}/limits/datacards_{abcd_config.do_region}/"
plots_output_path = f"{base_output_path}/limits/plots/"
results_output_path = f"{base_output_path}/limits/results/"

# If True, poisson error on empty bins (1.84) will be added to data histograms
add_uncertainties_on_zero = False

luminosity = abcd_config.luminosity

do_abcd = True
use_abcd_prediction = True  # if False, it will use the actual number of events in the signal bin
include_shapes = True

if do_abcd:
  include_shapes = False  # currently not supported for ABCD

skip_combine = False

signal_samples = []


for name in dasSignals2018:
  signal_name = name.split("/")[-1]

  signal_samples.append(
      Sample(
          name="signal_"+signal_name,
          file_path=f"{base_path}/signals/{signal_name}/{abcd_config.signal_skim[0]}/{signal_hist_path}/histograms.root",
          type=SampleType.signal,
          cross_sections=cross_sections,
      )
  )


# Sample(
  #     name="data_obs",
  #     file_path=f"{base_path}/histograms/data.root",
  #     type=SampleType.data,
  # ),


config_helper = TTAlpsABCDConfigHelper(
    year,
    abcd_config.background_skim,
    abcd_config.category,
    base_path,
    background_hist_path,
)

background_samples, backgrounds = config_helper.get_background_samples()
samples = signal_samples + background_samples
background_params = config_helper.get_background_params(backgrounds)


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


# List nuisance parameters (they will only be added for processes for which they were listed)
nuisances = {
    "PUjetIDtight_down": "variation",
    "PUjetIDtight_up": "variation",
    "bTaggingMedium_down_correlated": "variation",
    "bTaggingMedium_down_uncorrelated": "variation",
    "bTaggingMedium_up_correlated": "variation",
    "bTaggingMedium_up_uncorrelated": "variation",
    "muonReco_systdown": "variation",
    "muonReco_systup": "variation",
    "muonTrigger_systdown": "variation",
    "muonTrigger_systup": "variation",

    "JpsiInvMass_down": "variation",
    "JpsiInvMass_up": "variation",

    "abcd_nonClosure": "closure",
    "lumi": {
        "signal": 1.017,  # arxiv.org/abs/2503.03946
        "bkg": 1.017,
    }
}

if abcd_config.category != "_DSA":
  nuisances["muonIDLoose_systdown"] = "variation"
  nuisances["muonIDLoose_systup"] = "variation"
