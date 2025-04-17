from Sample import Sample, SampleType
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType
from ttalps_cross_sections import get_cross_sections
from ttalps_samples_list import dasSignals2018
from TTAlpsABCDConfigHelper import TTAlpsABCDConfigHelper

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)


base_path = "/data/dust/user/jniedzie/ttalps_cms/"

combine_path = "/afs/desy.de/user/j/jniedzie/combine/CMSSW_14_1_0_pre4/src/"

# For signal like skim: SR and J/Psi CR with no isolation requirement on the loose muons
skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons")

# SR dimuon cuts applied
hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}"

datacards_output_path = "/afs/desy.de/user/j/jniedzie/tea_ttalps/limits/datacards/"
plots_output_path = "/afs/desy.de/user/j/jniedzie/tea_ttalps/limits/plots/"
results_output_path = "/afs/desy.de/user/j/jniedzie/tea_ttalps/limits/results/"

# If True, poisson error on empty bins (1.84) will be added to data histograms
add_uncertainties_on_zero = False

luminosity = 59830.  # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

do_abcd = True
use_abcd_prediction = True  # if False, it will use the actual number of events in the signal bin
include_shapes = True

if do_abcd:
  include_shapes = False  # currently not supported for ABCD

config_helper = TTAlpsABCDConfigHelper(
    year,
    skim,
    base_path,
    hist_path,
)

skip_combine = False

# category = ""
category = "_Pat"
# category = "_PatDSA"
# category = "_DSA"

collection = "BestPFIsoDimuonVertex"

signal_samples = []


for name in dasSignals2018:
  signal_name = name.split("/")[-1]

  signal_samples.append(
      Sample(
          name="signal_"+signal_name,
          file_path=f"{base_path}/signals/{signal_name}/{skim[0]}/{hist_path}/histograms.root",
          type=SampleType.signal,
          cross_sections=cross_sections,
      )
  )


# Sample(
  #     name="data_obs",
  #     file_path=f"{base_path}/histograms/data.root",
  #     type=SampleType.data,
  # ),


backgrounds_to_exclude = [
    "QCD_Pt-15To20",
    "QCD_Pt-20To30",
    "QCD_Pt-30To50",
    "QCD_Pt-50To80",
    "QCD_Pt-80To120",
    "QCD_Pt-120To170",
    "QCD_Pt-170To300",
]

if category == "_DSA":
  backgrounds_to_exclude.append("TTTo2L2Nu")  # fluctuates in SR DSA-DSA

background_samples, backgrounds = config_helper.get_background_samples(backgrounds_to_exclude)
samples = signal_samples + background_samples
background_params = config_helper.get_background_params(backgrounds)


if not do_abcd:
  # Use this 1D hisogram to calculate limits using shapes and MC backgrounds
  variable = "LxySignificance"
  # variable = "Lxy"

  histogram = Histogram(
      name=f"{collection}{category}_{variable}",
      norm_type=NormalizationType.to_lumi,
      x_max=140,
      rebin=5
  )
else:
  # Use this 2D histogram to calculate limits with cut-and-count and optionally ABCD background prediction
  # Binning is always expressed in bin numbers, not values. The abcd_points it's the first bin to the top-right
  # of the ABCD division lines.
  if category == "_Pat":
    variable_1 = "logLxySignificance"
    variable_2 = "log3Dangle"
    abcd_point = (22, 2)
  elif category == "_PatDSA":
    variable_1 = "dPhi"
    variable_2 = "logDxyPVTraj1"
    abcd_point = (21, 7)
  elif category == "_DSA":
    variable_1 = "logLxy"
    variable_2 = "log3Dangle"
    abcd_point = (19, 16)

  rebin_2D = 4

  histogram = Histogram2D(
      name=f"{collection}_{variable_1}_vs_{variable_2}{category}",
      norm_type=NormalizationType.to_lumi,
      x_rebin=rebin_2D,
      y_rebin=rebin_2D,
  )


# List nuisance parameters (they will only be added for processes for which they were listed)
nuisances = {
    "PUjetIDtight_down": "variation",
    "PUjetIDtight_up": "variation",
    "bTaggingMedium_down_correlated": "variation",
    "bTaggingMedium_down_uncorrelated": "variation",
    "bTaggingMedium_up_correlated": "variation",
    "bTaggingMedium_up_uncorrelated": "variation",
    "muonIDLoose_systdown": "variation",
    "muonIDLoose_systup": "variation",
    # "muonReco_systdown": "variation",
    # "muonReco_systup": "variation",
    "muonTriggerIsoMu24_systdown": "variation",
    "muonTriggerIsoMu24_systup": "variation",

    "abcd_nonClosure": "closure",
}

# combineCards.py datacard_BestPFIsoDimuonVertex_Pat_LxySignificance_tta_mAlp-2GeV_ctau-1e-5mm_PFIso.txt datacard_BestPFIsoDimuonVertex_PatDSA_LxySignificance_tta_mAlp-2GeV_ctau-1e-5mm_PFIso.txt datacard_BestPFIsoDimuonVertex_DSA_LxySignificance_tta_mAlp-2GeV_ctau-1e-5mm_PFIso.txt > datacard_BestPFIsoDimuonVertex_combined_LxySignificance_tta_mAlp-2GeV_ctau-1e-5mm_PFIso.txt
