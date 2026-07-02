from Sample import Sample, SampleType
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType
from ttalps_cross_sections import get_cross_sections, get_theory_cross_section
# from ttalps_luminosities import get_luminosity_uncertainty_default, get_luminosity_uncertainty
from ttalps_nuicances_config import get_correlated_nuisances, get_uncorrelated_nuisances, symmetric_nuisances
from TTAlpsABCDConfigHelper import TTAlpsABCDConfigHelper
import ttalps_abcd_config as abcd_config
import os

years = abcd_config.years
year = years[0]
year_str = ""
for year_ in years:
  year_str += year_
cross_sections = get_cross_sections(year)
category = abcd_config.category
# lumi_uncertainty = get_luminosity_uncertainty_default(year)
# lumi_uncertainty_dict = get_luminosity_uncertainty(year)

username = os.getenv("USER")
base_path = f"/data/dust/user/jniedzie/ttalps_cms/"
combine_path = "/afs/desy.de/user/j/jniedzie/combine/CMSSW_14_1_0_pre4/src/"
base_output_path = "/afs/desy.de/user/j/jniedzie/tea_ttalps"
if username == "lrygaard":
  base_path = f"/data/dust/user/lrygaard/ttalps_cms/"
  combine_path = "/afs/desy.de/user/l/lrygaard/Combine/CMSSW_14_1_0_pre4/src/"
  base_output_path = "/afs/desy.de/user/l/lrygaard/TTALP/tea_ttalps"

hist_path = "histograms"

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

run_signal_injection = abcd_config.run_signal_injection

theory_cross_section = False

extra_str = ""
# extra_str = "_testingObs"
# extra_str = "_ctau-1e-13mm"
# extra_str = "_ctau-1e-09mm"
# extra_str = "_years_combined"
# extra_str = "_preapproval"
# extra_str = "_years_combined_noDimuonSFs"
# extra_str = "_years_combined_dxydzIso"
# extra_str = "_years_combined_noUnc"
# extra_str = "_noUnc"
if theory_cross_section:
  extra_str += "_theoryCrossSection"
datacards_output_path = f"{base_output_path}/limits/limits_{year_str}/datacards{extra_str}_{abcd_config.do_region}/"
plots_output_path = f"{base_output_path}/limits/limits_{year_str}/plots{extra_str}/"

results_output_path = f"{base_output_path}/limits/limits_{year_str}/results{extra_str}_{abcd_config.do_region}/"

# If True, poisson error on empty bins (1.84) will be added to data histograms
add_uncertainties_on_zero = False

luminosity = abcd_config.luminosity_sum

do_data = abcd_config.do_data
blinded_region_A = abcd_config.blinded_region_A
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
    abcd_config.signal_skim,
    signal_hist_path,
)

signal_samples, signals = config_helper.get_signal_samples(theory_cross_section)

if not abcd_config.do_data:
  background_samples, backgrounds = config_helper.get_background_samples()
else:
  background_samples, backgrounds = config_helper.get_data_samples(abcd_config.data_paths)
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

nuisances_correlated = get_correlated_nuisances(year_str, abcd_config.category)
dimuonSFs = True if not "noDimuonEff" in abcd_config.signal_skim[2] else False
nuisances_uncorrelated = get_uncorrelated_nuisances(years, category, dimuonSFs)
nuisances = {**nuisances_correlated, **nuisances_uncorrelated}

# nuisances_correlated = {}
# nuisances_uncorrelated = {}
# nuisances = {}

# jec_years = {
#   "2016preVFP": "2016", 
#   "2016postVFP": "2016", 
#   "2017": "2017",
#   "2018": "2018",
#   "2022preEE": "2022",
#   "2022postEE": "2022EE",
#   "2023preBPix": "2023",
#   "2023postBPix": "2023BPix",
# }
# jec_year = jec_years[year]

# systematic_years = {
#   "2016preVFP": "2016preVFP", 
#   "2016postVFP": "2016postVFP", 
#   "2017": "2017",
#   "2018": "2018",
#   "2022preEE": "2022",
#   "2022postEE": "2022EE",
#   "2023preBPix": "2023",
#   "2023postBPix": "2023BPix",
# }
# syst_year = systematic_years[year]

# lumi_years = {
#   "2016preVFP": "2016",
#   "2016postVFP": "2016",
#   "2017": "2017",
#   "2018": "2018",
#   "2022preEE": "13p6TeV_2022",
#   "2022postEE": "13p6TeV_2022",
#   "2023preBPix": "13p6TeV_2023",
#   "2023postBPix": "13p6TeV_2023",
# }
# lumi_year = lumi_years[year]

# # List nuisance parameters (they will only be added for processes for which they were listed)
# nuisances = {
#     "bTaggingMedium_down_correlated": ("variation", "CMS_btag"),
#     "bTaggingMedium_down_uncorrelated": ("variation", f"CMS_eff_b_{syst_year}"),
#     "bTaggingMedium_up_correlated": ("variation", "CMS_btag"),
#     "bTaggingMedium_up_uncorrelated": ("variation", f"CMS_eff_b_{syst_year}"),

#     "muonIDTight_systdown": ("variation", f"CMS_eff_m_id_syst_tight"),
#     "muonIDTight_systup": ("variation", f"CMS_eff_m_id_syst_tight"),
#     "muonIDTight_stat_down": ("variation", f"CMS_eff_m_id_stat_tight_{syst_year}"),
#     "muonIDTight_stat_up": ("variation", f"CMS_eff_m_id_stat_tight_{syst_year}"),

#     "muonIsoTight_systup": ("variation", f"CMS_eff_m_iso_syst_tight"),
#     "muonIsoTight_systdown": ("variation", f"CMS_eff_m_iso_syst_tight"),
#     "muonIsoTight_stat_up": ("variation", f"CMS_eff_m_iso_stat_tight_{syst_year}"),
#     "muonIsoTight_stat_down": ("variation", f"CMS_eff_m_iso_stat_tight_{syst_year}"),
#     "muonTrigger_systdown": ("variation", f"CMS_eff_m_trigger_syst"),
#     "muonTrigger_systup": ("variation", f"CMS_eff_m_trigger_syst"),
#     "muonTrigger_stat_down": ("variation", f"CMS_eff_m_trigger_stat_{syst_year}"),
#     "muonTrigger_stat_up": ("variation", f"CMS_eff_m_trigger_stat_{syst_year}"),

#     "pileup_up": ("variation", f"CMS_pileup_{syst_year}"),
#     "pileup_down": ("variation", f"CMS_pileup_{syst_year}"),

#     "abcd_unc": ("abcd", f"CMS_EXO25022_abcd_{syst_year}"),

#     "lxy_unc": ("lxy", f"CMS_EXO25022_lxy_{syst_year}"),

#     "jecMC_Regrouped_Absolute_down": ("variation", "CMS_scale_j_Absolute"),
#     "jecMC_Regrouped_Absolute_up": ("variation", "CMS_scale_j_Absolute"),
#     f"jecMC_Regrouped_Absolute_{jec_year}_down": ("variation", f"CMS_scale_j_Absolute_{syst_year}"),
#     f"jecMC_Regrouped_Absolute_{jec_year}_up": ("variation", f"CMS_scale_j_Absolute_{syst_year}"),
#     "jecMC_Regrouped_FlavorQCD_down": ("variation", "CMS_scale_j_FlavorQCD"),
#     "jecMC_Regrouped_FlavorQCD_up": ("variation", "CMS_scale_j_FlavorQCD"),
#     "jecMC_Regrouped_BBEC1_down": ("variation", "CMS_scale_j_BBEC1"),
#     "jecMC_Regrouped_BBEC1_up": ("variation", "CMS_scale_j_BBEC1"),
#     f"jecMC_Regrouped_BBEC1_{jec_year}_down": ("variation", f"CMS_scale_j_BBEC1_{syst_year}"),
#     f"jecMC_Regrouped_BBEC1_{jec_year}_up": ("variation", f"CMS_scale_j_BBEC1_{syst_year}"),
#     "jecMC_Regrouped_EC2_down": ("variation", "CMS_scale_j_EC2"),
#     "jecMC_Regrouped_EC2_up": ("variation", "CMS_scale_j_EC2"),
#     f"jecMC_Regrouped_EC2_{jec_year}_down": ("variation", f"CMS_scale_j_EC2_{syst_year}"),
#     f"jecMC_Regrouped_EC2_{jec_year}_up": ("variation", f"CMS_scale_j_EC2_{syst_year}"),
#     "jecMC_Regrouped_HF_down": ("variation", "CMS_scale_j_HF"),
#     "jecMC_Regrouped_HF_up": ("variation", "CMS_scale_j_HF"),
#     f"jecMC_Regrouped_HF_{jec_year}_down": ("variation", f"CMS_scale_j_HF_{syst_year}"),
#     f"jecMC_Regrouped_HF_{jec_year}_up": ("variation", f"CMS_scale_j_HF_{syst_year}"),
#     "jecMC_Regrouped_RelativeBal_down": ("variation", "CMS_scale_j_RelativeBal"),
#     "jecMC_Regrouped_RelativeBal_up": ("variation", "CMS_scale_j_RelativeBal"),
#     f"jecMC_Regrouped_RelativeSample_{jec_year}_down": ("variation", f"CMS_scale_j_RelativeSample_{syst_year}"),
#     f"jecMC_Regrouped_RelativeSample_{jec_year}_up": ("variation", f"CMS_scale_j_RelativeSample_{syst_year}"),

#     "metMC_Regrouped_Absolute_down": ("variation", "CMS_scale_met_Absolute"),
#     "metMC_Regrouped_Absolute_up": ("variation", "CMS_scale_met_Absolute"),
#     f"metMC_Regrouped_Absolute_{jec_year}_down": ("variation", f"CMS_scale_met_Absolute_{syst_year}"),
#     f"metMC_Regrouped_Absolute_{jec_year}_up": ("variation", f"CMS_scale_met_Absolute_{syst_year}"),
#     "metMC_Regrouped_FlavorQCD_down": ("variation", "CMS_scale_met_FlavorQCD"),
#     "metMC_Regrouped_FlavorQCD_up": ("variation", "CMS_scale_met_FlavorQCD"),
#     "metMC_Regrouped_BBEC1_down": ("variation", "CMS_scale_met_BBEC1"),
#     "metMC_Regrouped_BBEC1_up": ("variation", "CMS_scale_met_BBEC1"),
#     f"metMC_Regrouped_BBEC1_{jec_year}_down": ("variation", f"CMS_scale_met_BBEC1_{syst_year}"),
#     f"metMC_Regrouped_BBEC1_{jec_year}_up": ("variation", f"CMS_scale_met_BBEC1_{syst_year}"),
#     "metMC_Regrouped_EC2_down": ("variation", "CMS_scale_met_EC2"),
#     "metMC_Regrouped_EC2_up": ("variation", "CMS_scale_met_EC2"),
#     f"metMC_Regrouped_EC2_{jec_year}_down": ("variation", f"CMS_scale_met_EC2_{syst_year}"),
#     f"metMC_Regrouped_EC2_{jec_year}_up": ("variation", f"CMS_scale_met_EC2_{syst_year}"),
#     "metMC_Regrouped_HF_down": ("variation", "CMS_scale_met_HF"),
#     "metMC_Regrouped_HF_up": ("variation", "CMS_scale_met_HF"),
#     f"metMC_Regrouped_HF_{jec_year}_down": ("variation", f"CMS_scale_met_HF_{syst_year}"),
#     f"metMC_Regrouped_HF_{jec_year}_up": ("variation", f"CMS_scale_met_HF_{syst_year}"),
#     "metMC_Regrouped_RelativeBal_down": ("variation", "CMS_scale_met_RelativeBal"),
#     "metMC_Regrouped_RelativeBal_up": ("variation", "CMS_scale_met_RelativeBal"),
#     f"metMC_Regrouped_RelativeSample_{jec_year}_down": ("variation", f"CMS_scale_met_RelativeSample_{syst_year}"),
#     f"metMC_Regrouped_RelativeSample_{jec_year}_up": ("variation", f"CMS_scale_met_RelativeSample_{syst_year}"),

#     "jer_up": ("variation", f"CMS_res_j_{syst_year}"),
#     "jer_down": ("variation", f"CMS_res_j_{syst_year}"),
#     "met_jer_up": ("variation", f"CMS_res_met_{syst_year}"),
#     "met_jer_down": ("variation", f"CMS_res_met_{syst_year}"),

#     "MET_unclusteredEnergy_up": ("variation", f"CMS_scale_met_unclustered_energy_{syst_year}"),
#     "MET_unclusteredEnergy_down": ("variation", f"CMS_scale_met_unclustered_energy_{syst_year}"),
# }

# for name, unc in lumi_uncertainty_dict.items():
#   nuisances[name] = {
#     "signal": [unc],
#     # "bkg": [unc],
#   }

# if not "noDimuonEff" in hist_path:
#   nuisances["dimuonEff_Patdown"] = ("variation", f"CMS_EXO25022_dimuonSFs_Pat_{syst_year}")
#   nuisances["dimuonEff_Patup"] = ("variation", f"CMS_EXO25022_dimuonSFs_Pat_{syst_year}")
#   nuisances["dimuonEff_PatDSAdown"] = ("variation", f"CMS_EXO25022_dimuonSFs_PatDSA_{syst_year}")
#   nuisances["dimuonEff_PatDSAup"] = ("variation", f"CMS_EXO25022_dimuonSFs_PatDSA_{syst_year}")
#   nuisances["dimuonEff_DSAdown"] = ("variation", f"CMS_EXO25022_dimuonSFs_DSA_{syst_year}")
#   nuisances["dimuonEff_DSAup"] = ("variation", f"CMS_EXO25022_dimuonSFs_DSA_{syst_year}")

# if abcd_config.category != "_DSA":
#   nuisances["muonIDLoose_systdown"] = ("variation", f"CMS_eff_m_id_syst_loose")
#   nuisances["muonIDLoose_systup"] = ("variation", f"CMS_eff_m_id_syst_loose")
#   nuisances["muonIDLoose_stat_down"] = ("variation", f"CMS_eff_m_id_stat_loose_{syst_year}")
#   nuisances["muonIDLoose_stat_up"] = ("variation", f"CMS_eff_m_id_stat_loose_{syst_year}")
#   nuisances["muonIsoLoose_systdown"] = ("variation", f"CMS_eff_m_iso_syst_loose")
#   nuisances["muonIsoLoose_systup"] = ("variation", f"CMS_eff_m_iso_syst_loose")
#   nuisances["muonIsoLoose_stat_down"] = ("variation", f"CMS_eff_m_iso_stat_loose_{syst_year}")
#   nuisances["muonIsoLoose_stat_up"] = ("variation", f"CMS_eff_m_iso_stat_loose_{syst_year}")

# if abcd_config.category != "_Pat":
#   nuisances["dsamuonID_down_syst"] = ("variation", f"CMS_eff_m_id_dsa")
#   nuisances["dsamuonID_up_syst"] = ("variation", f"CMS_eff_m_id_dsa")
#   nuisances["dsamuonReco_cosmic_down"] = ("variation", f"CMS_eff_m_reco_dsa")
#   nuisances["dsamuonReco_cosmic_up"] = ("variation", f"CMS_eff_m_reco_dsa")

# # muon reco and PU jet ID only available for run 2 as of now
# if "2016" in year_str or "2017" in year_str or "2018" in year_str:
#   nuisances["muonReco_systdown"] = ("variation", f"CMS_eff_m_reco_syst")
#   nuisances["muonReco_systup"] = ("variation", f"CMS_eff_m_reco_syst")
#   nuisances["muonReco_stat_down"] = ("variation", f"CMS_eff_m_reco_stat_{syst_year}")
#   nuisances["muonReco_stat_up"] = ("variation", f"CMS_eff_m_reco_stat_{syst_year}")
#   nuisances["PUjetIDtight_down"] = ("variation", f"CMS_eff_j_PUJetID_eff_{syst_year}")
#   nuisances["PUjetIDtight_up"] = ("variation", f"CMS_eff_j_PUJetID_eff_{syst_year}")
#   nuisances["L1PreFiringWeight_Dn"] = ("variation", f"CMS_l1_prefiring_{syst_year}")
#   nuisances["L1PreFiringWeight_Up"] = ("variation", f"CMS_l1_prefiring_{syst_year}")

# # variations where we take the maximum of up/down variation as symmetrized uncertainty
# symmetric_nuisances = [
#   "CMS_scale_j", 
#   "CMS_scale_met", 
#   "CMS_res_j", 
#   "CMS_res_met", 
#   "CMS_scale_met_unclustered_energy",
#   "CMS_eff_m_id_stat",
#   "CMS_eff_m_iso_stat",
#   "CMS_eff_m_reco_stat",
#   "CMS_eff_m_trigger_stat",
# ]
