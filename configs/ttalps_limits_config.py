from Sample import Sample, SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType
from ttalps_cross_sections import get_cross_sections
from ttalps_samples_list import dasSignals2018, dasBackgrounds2018

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)

base_path = "/data/dust/user/jniedzie/ttalps_cms/"

combine_path = "/afs/desy.de/user/j/jniedzie/combine/CMSSW_14_1_0_pre4/src/"

# For signal like skim: SR and J/Psi CR with no isolation requirement on the loose muons
skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons")

# SR dimuon cuts applied
hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}"

output_path = "/afs/desy.de/user/j/jniedzie/tea_ttalps/datacards/"

# If True, poisson error on empty bins (1.84) will be added to data histograms
add_uncertainties_on_zero = False

luminosity = 59830.  # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2
include_shapes = True

skip_combine = False

signal_samples = []
background_samples = []
background_names = []

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


for name in dasBackgrounds2018:
  background_names.append(name.split("/")[-1])

  background_samples.append(
      Sample(
          name=name.split("/")[-1],
          file_path=f"{base_path}/{name}/{skim[0]}/{hist_path}/histograms.root",
          type=SampleType.background,
          cross_sections=cross_sections,
      )
  )

samples = signal_samples + background_samples

# List histograms for which to create datacards
histogram = Histogram(name="BestPFIsoDimuonVertex_Pat_LxySignificance", norm_type=NormalizationType.to_lumi, x_max=140, rebin=5)
# Histogram(name="BestPFIsoDimuonVertex_Pat_Lxy"               , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),
# Histogram(name="BestPFIsoDimuonVertex_PatDSA_Lxy"            , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),
# Histogram(name="BestPFIsoDimuonVertex_DSA_Lxy"               , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),

# Histogram(name="BestPFIsoDimuonVertex_PatDSA_LxySignificance"  , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),
# Histogram(name="BestPFIsoDimuonVertex_DSA_LxySignificance"     , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),

# List nuisance parameters (they will only be added for processes for which they were listed)
nuisances = {
    "bck_syst": {name: 1.1 for name in background_names},
    "signal_unc": {
        "signal_"+signal_name: 1.05,
    }
}

# combineCards.py datacard_BestPFIsoDimuonVertex_Pat_LxySignificance_tta_mAlp-2GeV_ctau-1e-5mm_PFIso.txt datacard_BestPFIsoDimuonVertex_PatDSA_LxySignificance_tta_mAlp-2GeV_ctau-1e-5mm_PFIso.txt datacard_BestPFIsoDimuonVertex_DSA_LxySignificance_tta_mAlp-2GeV_ctau-1e-5mm_PFIso.txt > datacard_BestPFIsoDimuonVertex_combined_LxySignificance_tta_mAlp-2GeV_ctau-1e-5mm_PFIso.txt
