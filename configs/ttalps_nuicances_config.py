from ttalps_luminosities import get_luminosity_uncertainty_for_years, get_luminosity_uncertainty

# List nuisance parameters (they will only be added for processes for which they were listed)
correlated_nuisances = {
    "bTaggingMedium_down_correlated": ("variation", "CMS_btag"),
    "bTaggingMedium_up_correlated": ("variation", "CMS_btag"),

    "muonIDTight_systdown": ("variation", f"CMS_eff_m_id_syst_tight"),
    "muonIDTight_systup": ("variation", f"CMS_eff_m_id_syst_tight"),

    "muonIsoTight_systup": ("variation", f"CMS_eff_m_iso_syst_tight"),
    "muonIsoTight_systdown": ("variation", f"CMS_eff_m_iso_syst_tight"),
    "muonTrigger_systdown": ("variation", f"CMS_eff_m_trigger_syst"),
    "muonTrigger_systup": ("variation", f"CMS_eff_m_trigger_syst"),

    "jecMC_Regrouped_Absolute_down": ("variation", "CMS_scale_j_Absolute"),
    "jecMC_Regrouped_Absolute_up": ("variation", "CMS_scale_j_Absolute"),
    "jecMC_Regrouped_FlavorQCD_down": ("variation", "CMS_scale_j_FlavorQCD"),
    "jecMC_Regrouped_FlavorQCD_up": ("variation", "CMS_scale_j_FlavorQCD"),
    "jecMC_Regrouped_BBEC1_down": ("variation", "CMS_scale_j_BBEC1"),
    "jecMC_Regrouped_BBEC1_up": ("variation", "CMS_scale_j_BBEC1"),
    "jecMC_Regrouped_EC2_down": ("variation", "CMS_scale_j_EC2"),
    "jecMC_Regrouped_EC2_up": ("variation", "CMS_scale_j_EC2"),
    "jecMC_Regrouped_HF_down": ("variation", "CMS_scale_j_HF"),
    "jecMC_Regrouped_HF_up": ("variation", "CMS_scale_j_HF"),
    "jecMC_Regrouped_RelativeBal_down": ("variation", "CMS_scale_j_RelativeBal"),
    "jecMC_Regrouped_RelativeBal_up": ("variation", "CMS_scale_j_RelativeBal"),

    "metMC_Regrouped_Absolute_down": ("variation", "CMS_scale_met_Absolute"),
    "metMC_Regrouped_Absolute_up": ("variation", "CMS_scale_met_Absolute"),
    "metMC_Regrouped_FlavorQCD_down": ("variation", "CMS_scale_met_FlavorQCD"),
    "metMC_Regrouped_FlavorQCD_up": ("variation", "CMS_scale_met_FlavorQCD"),
    "metMC_Regrouped_BBEC1_down": ("variation", "CMS_scale_met_BBEC1"),
    "metMC_Regrouped_BBEC1_up": ("variation", "CMS_scale_met_BBEC1"),
    "metMC_Regrouped_EC2_down": ("variation", "CMS_scale_met_EC2"),
    "metMC_Regrouped_EC2_up": ("variation", "CMS_scale_met_EC2"),
    "metMC_Regrouped_HF_down": ("variation", "CMS_scale_met_HF"),
    "metMC_Regrouped_HF_up": ("variation", "CMS_scale_met_HF"),
    "metMC_Regrouped_RelativeBal_down": ("variation", "CMS_scale_met_RelativeBal"),
    "metMC_Regrouped_RelativeBal_up": ("variation", "CMS_scale_met_RelativeBal"),

    f"abcd_unc": ("abcd", f"CMS_EXO25022_abcd"),

    f"lxy_unc": ("lxy", f"CMS_EXO25022_lxy"),
}

correlated_nuisances_Run2 = {
    "muonReco_systdown": ("variation", f"CMS_eff_m_reco_syst"),
    "muonReco_systup": ("variation", f"CMS_eff_m_reco_syst"),
}

correlated_nuisances_Pat = {
    "muonIDLoose_systdown": ("variation", f"CMS_eff_m_id_syst_loose"),
    "muonIDLoose_systup": ("variation", f"CMS_eff_m_id_syst_loose"),
    "muonIsoLoose_systdown": ("variation", f"CMS_eff_m_iso_syst_loose"),
    "muonIsoLoose_systup": ("variation", f"CMS_eff_m_iso_syst_loose"),

    f"dxydzIso_unc": ("dxydzIso", f"CMS_EXO25022_dxydzIso"),
}

correlated_nuisances_DSA = {
    "dsamuonID_down_syst": ("variation", f"CMS_eff_m_id_dsa"),
    "dsamuonID_up_syst": ("variation", f"CMS_eff_m_id_dsa"),
    "dsamuonReco_cosmic_down": ("variation", f"CMS_eff_m_reco_dsa"),
    "dsamuonReco_cosmic_up": ("variation", f"CMS_eff_m_reco_dsa"),
}

jec_years = {
  "2016preVFP": "2016", 
  "2016postVFP": "2016", 
  "2017": "2017",
  "2018": "2018",
  "2022preEE": "2022",
  "2022postEE": "2022EE",
  "2023preBPix": "2023",
  "2023postBPix": "2023BPix",
}

systematic_years = {
  "2016preVFP": "2016preVFP", 
  "2016postVFP": "2016postVFP", 
  "2017": "2017",
  "2018": "2018",
  "2022preEE": "2022",
  "2022postEE": "2022EE",
  "2023preBPix": "2023",
  "2023postBPix": "2023BPix",
}

lumi_years = {
  "2016preVFP": "2016",
  "2016postVFP": "2016",
  "2017": "2017",
  "2018": "2018",
  "2022preEE": "13p6TeV_2022",
  "2022postEE": "13p6TeV_2022",
  "2023preBPix": "13p6TeV_2023",
  "2023postBPix": "13p6TeV_2023",
}

# variations where we take the maximum of up/down variation as symmetrized uncertainty
symmetric_nuisances = [
  "CMS_scale_j", 
  "CMS_scale_met", 
  "CMS_res_j", 
  "CMS_res_met", 
  "CMS_scale_met_unclustered_energy",
  "CMS_eff_m_id_stat",
  "CMS_eff_m_iso_stat",
  "CMS_eff_m_reco_stat",
  "CMS_eff_m_trigger_stat",
]

def get_correlated_nuisances(year_str, category):
  nuisances = correlated_nuisances
  if category != "_DSA":
    nuisances.update(correlated_nuisances_Pat)
  if category != "_Pat":
    nuisances.update(correlated_nuisances_DSA)
  if "2016" in year_str or "2017" in year_str or "2018" in year_str:
    nuisances.update(correlated_nuisances_Run2)
  return nuisances

def get_base_uncorrelated_nuisances_for_year(year):
    jec_year = jec_years[year]
    syst_year = systematic_years[year]
    nuisances = {
        f"bTaggingMedium_down_uncorrelated_{year}": ("variation", f"CMS_eff_b_{syst_year}"),
        f"bTaggingMedium_up_uncorrelated_{year}": ("variation", f"CMS_eff_b_{syst_year}"),

        f"muonIDTight_stat_down_{year}": ("variation", f"CMS_eff_m_id_stat_tight_{syst_year}"),
        f"muonIDTight_stat_up_{year}": ("variation", f"CMS_eff_m_id_stat_tight_{syst_year}"),

        f"muonIsoTight_stat_up_{year}": ("variation", f"CMS_eff_m_iso_stat_tight_{syst_year}"),
        f"muonIsoTight_stat_down_{year}": ("variation", f"CMS_eff_m_iso_stat_tight_{syst_year}"),
        f"muonTrigger_stat_down_{year}": ("variation", f"CMS_eff_m_trigger_stat_{syst_year}"),
        f"muonTrigger_stat_up_{year}": ("variation", f"CMS_eff_m_trigger_stat_{syst_year}"),

        f"pileup_up_{year}": ("variation", f"CMS_pileup_{syst_year}"),
        f"pileup_down_{year}": ("variation", f"CMS_pileup_{syst_year}"),

        f"jecMC_Regrouped_Absolute_{jec_year}_down_{year}": ("variation", f"CMS_scale_j_Absolute_{syst_year}"),
        f"jecMC_Regrouped_Absolute_{jec_year}_up_{year}": ("variation", f"CMS_scale_j_Absolute_{syst_year}"),
        f"jecMC_Regrouped_BBEC1_{jec_year}_down_{year}": ("variation", f"CMS_scale_j_BBEC1_{syst_year}"),
        f"jecMC_Regrouped_BBEC1_{jec_year}_up_{year}": ("variation", f"CMS_scale_j_BBEC1_{syst_year}"),
        f"jecMC_Regrouped_EC2_{jec_year}_down_{year}": ("variation", f"CMS_scale_j_EC2_{syst_year}"),
        f"jecMC_Regrouped_EC2_{jec_year}_up_{year}": ("variation", f"CMS_scale_j_EC2_{syst_year}"),
        f"jecMC_Regrouped_HF_{jec_year}_down_{year}": ("variation", f"CMS_scale_j_HF_{syst_year}"),
        f"jecMC_Regrouped_HF_{jec_year}_up_{year}": ("variation", f"CMS_scale_j_HF_{syst_year}"),
        f"jecMC_Regrouped_RelativeSample_{jec_year}_down_{year}": ("variation", f"CMS_scale_j_RelativeSample_{syst_year}"),
        f"jecMC_Regrouped_RelativeSample_{jec_year}_up_{year}": ("variation", f"CMS_scale_j_RelativeSample_{syst_year}"),

        f"metMC_Regrouped_Absolute_{jec_year}_down_{year}": ("variation", f"CMS_scale_met_Absolute_{syst_year}"),
        f"metMC_Regrouped_Absolute_{jec_year}_up_{year}": ("variation", f"CMS_scale_met_Absolute_{syst_year}"),
        f"metMC_Regrouped_BBEC1_{jec_year}_down_{year}": ("variation", f"CMS_scale_met_BBEC1_{syst_year}"),
        f"metMC_Regrouped_BBEC1_{jec_year}_up_{year}": ("variation", f"CMS_scale_met_BBEC1_{syst_year}"),
        f"metMC_Regrouped_EC2_{jec_year}_down_{year}": ("variation", f"CMS_scale_met_EC2_{syst_year}"),
        f"metMC_Regrouped_EC2_{jec_year}_up_{year}": ("variation", f"CMS_scale_met_EC2_{syst_year}"),
        f"metMC_Regrouped_HF_{jec_year}_down_{year}": ("variation", f"CMS_scale_met_HF_{syst_year}"),
        f"metMC_Regrouped_HF_{jec_year}_up_{year}": ("variation", f"CMS_scale_met_HF_{syst_year}"),
        f"metMC_Regrouped_RelativeSample_{jec_year}_down_{year}": ("variation", f"CMS_scale_met_RelativeSample_{syst_year}"),
        f"metMC_Regrouped_RelativeSample_{jec_year}_up_{year}": ("variation", f"CMS_scale_met_RelativeSample_{syst_year}"),

        f"jer_up_{year}": ("variation", f"CMS_res_j_{syst_year}"),
        f"jer_down_{year}": ("variation", f"CMS_res_j_{syst_year}"),
        f"met_jer_up_{year}": ("variation", f"CMS_res_met_{syst_year}"),
        f"met_jer_down_{year}": ("variation", f"CMS_res_met_{syst_year}"),

        f"MET_unclusteredEnergy_up_{year}": ("variation", f"CMS_scale_met_unclustered_energy_{syst_year}"),
        f"MET_unclusteredEnergy_down_{year}": ("variation", f"CMS_scale_met_unclustered_energy_{syst_year}"),
    }
    return nuisances

def get_uncorrelated_nuisances(years, category, dimuonSFs):
    nuisances = {}
    lumi_uncertainty_dict = get_luminosity_uncertainty_for_years(years)
    for name, unc in lumi_uncertainty_dict.items():
        nuisances[f"{name}"] = {
            "signal": [unc],
            # "bkg": [unc],
        }
    for year in years:
        jec_year = jec_years[year]
        syst_year = systematic_years[year]
        lumi_year = lumi_years[year]

        nuisances.update(get_base_uncorrelated_nuisances_for_year(year))
        #     f"bTaggingMedium_down_uncorrelated_{year}": ("variation", f"CMS_eff_b_{syst_year}"),
        #     f"bTaggingMedium_up_uncorrelated_{year}": ("variation", f"CMS_eff_b_{syst_year}"),

        #     f"muonIDTight_stat_down_{year}": ("variation", f"CMS_eff_m_id_stat_tight_{syst_year}"),
        #     f"muonIDTight_stat_up_{year}": ("variation", f"CMS_eff_m_id_stat_tight_{syst_year}"),

        #     f"muonIsoTight_stat_up_{year}": ("variation", f"CMS_eff_m_iso_stat_tight_{syst_year}"),
        #     f"muonIsoTight_stat_down_{year}": ("variation", f"CMS_eff_m_iso_stat_tight_{syst_year}"),
        #     f"muonTrigger_stat_down_{year}": ("variation", f"CMS_eff_m_trigger_stat_{syst_year}"),
        #     f"muonTrigger_stat_up_{year}": ("variation", f"CMS_eff_m_trigger_stat_{syst_year}"),

        #     f"pileup_up_{year}": ("variation", f"CMS_pileup_{syst_year}"),
        #     f"pileup_down_{year}": ("variation", f"CMS_pileup_{syst_year}"),

        #     f"abcd_unc_{year}": ("abcd", f"CMS_EXO25022_abcd_{syst_year}"),

        #     f"lxy_unc_{year}": ("lxy", f"CMS_EXO25022_lxy_{syst_year}"),

        #     f"jecMC_Regrouped_Absolute_{jec_year}_down": ("variation", f"CMS_scale_j_Absolute_{syst_year}"),
        #     f"jecMC_Regrouped_Absolute_{jec_year}_up": ("variation", f"CMS_scale_j_Absolute_{syst_year}"),
        #     f"jecMC_Regrouped_BBEC1_{jec_year}_down": ("variation", f"CMS_scale_j_BBEC1_{syst_year}"),
        #     f"jecMC_Regrouped_BBEC1_{jec_year}_up": ("variation", f"CMS_scale_j_BBEC1_{syst_year}"),
        #     f"jecMC_Regrouped_EC2_{jec_year}_down": ("variation", f"CMS_scale_j_EC2_{syst_year}"),
        #     f"jecMC_Regrouped_EC2_{jec_year}_up": ("variation", f"CMS_scale_j_EC2_{syst_year}"),
        #     f"jecMC_Regrouped_HF_{jec_year}_down": ("variation", f"CMS_scale_j_HF_{syst_year}"),
        #     f"jecMC_Regrouped_HF_{jec_year}_up": ("variation", f"CMS_scale_j_HF_{syst_year}"),
        #     f"jecMC_Regrouped_RelativeSample_{jec_year}_down": ("variation", f"CMS_scale_j_RelativeSample_{syst_year}"),
        #     f"jecMC_Regrouped_RelativeSample_{jec_year}_up": ("variation", f"CMS_scale_j_RelativeSample_{syst_year}"),

        #     f"metMC_Regrouped_Absolute_{jec_year}_down": ("variation", f"CMS_scale_met_Absolute_{syst_year}"),
        #     f"metMC_Regrouped_Absolute_{jec_year}_up": ("variation", f"CMS_scale_met_Absolute_{syst_year}"),
        #     f"metMC_Regrouped_BBEC1_{jec_year}_down": ("variation", f"CMS_scale_met_BBEC1_{syst_year}"),
        #     f"metMC_Regrouped_BBEC1_{jec_year}_up": ("variation", f"CMS_scale_met_BBEC1_{syst_year}"),
        #     f"metMC_Regrouped_EC2_{jec_year}_down": ("variation", f"CMS_scale_met_EC2_{syst_year}"),
        #     f"metMC_Regrouped_EC2_{jec_year}_up": ("variation", f"CMS_scale_met_EC2_{syst_year}"),
        #     f"metMC_Regrouped_HF_{jec_year}_down": ("variation", f"CMS_scale_met_HF_{syst_year}"),
        #     f"metMC_Regrouped_HF_{jec_year}_up": ("variation", f"CMS_scale_met_HF_{syst_year}"),
        #     f"metMC_Regrouped_RelativeSample_{jec_year}_down": ("variation", f"CMS_scale_met_RelativeSample_{syst_year}"),
        #     f"metMC_Regrouped_RelativeSample_{jec_year}_up": ("variation", f"CMS_scale_met_RelativeSample_{syst_year}"),

        #     f"jer_up_{year}": ("variation", f"CMS_res_j_{syst_year}"),
        #     f"jer_down_{year}": ("variation", f"CMS_res_j_{syst_year}"),
        #     f"met_jer_up_{year}": ("variation", f"CMS_res_met_{syst_year}"),
        #     f"met_jer_down_{year}": ("variation", f"CMS_res_met_{syst_year}"),

        #     f"MET_unclusteredEnergy_up_{year}": ("variation", f"CMS_scale_met_unclustered_energy_{syst_year}"),
        #     f"MET_unclusteredEnergy_down_{year}": ("variation", f"CMS_scale_met_unclustered_energy_{syst_year}"),
        # )

        if dimuonSFs:
            nuisances[f"dimuonEff{category}down_{year}"] = ("variation", f"CMS_EXO25022_dimuonSFs{category}_{syst_year}")
            nuisances[f"dimuonEff{category}up_{year}"] = ("variation", f"CMS_EXO25022_dimuonSFs{category}_{syst_year}")
        if category != "_DSA":
            nuisances[f"muonIDLoose_stat_down_{year}"] = ("variation", f"CMS_eff_m_id_stat_loose_{syst_year}")
            nuisances[f"muonIDLoose_stat_up_{year}"] = ("variation", f"CMS_eff_m_id_stat_loose_{syst_year}")
            nuisances[f"muonIsoLoose_stat_down_{year}"] = ("variation", f"CMS_eff_m_iso_stat_loose_{syst_year}")
            nuisances[f"muonIsoLoose_stat_up_{year}"] = ("variation", f"CMS_eff_m_iso_stat_loose_{syst_year}")
        # muon reco and PU jet ID only available for run 2 as of now
        if "2016" in year or "2017" in year or "2018" in year:
            nuisances[f"muonReco_stat_down_{year}"] = ("variation", f"CMS_eff_m_reco_stat_{syst_year}")
            nuisances[f"muonReco_stat_up_{year}"] = ("variation", f"CMS_eff_m_reco_stat_{syst_year}")
            nuisances[f"PUjetIDtight_down_{year}"] = ("variation", f"CMS_eff_j_PUJetID_eff_{syst_year}")
            nuisances[f"PUjetIDtight_up_{year}"] = ("variation", f"CMS_eff_j_PUJetID_eff_{syst_year}")
            nuisances[f"L1PreFiringWeight_Dn_{year}"] = ("variation", f"CMS_l1_prefiring_{syst_year}")
            nuisances[f"L1PreFiringWeight_Up_{year}"] = ("variation", f"CMS_l1_prefiring_{syst_year}")
    return nuisances
    
