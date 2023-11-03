max_files = -1

# skim = "skimmed_ttbarLike"
# skim = "skimmed_ttZLike"
skim = "skimmed_ttbarSemimuonicCR_tightMuon"

base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"

doScaleFactors = True
excludeTriggerSFs = True

# Backgrounds
sample_path = f"backgrounds2018/ttZJets"
# sample_path = f"backgrounds2018/ttWJets"
# sample_path = f"backgrounds2018/TTToSemiLeptonic"
# sample_path = f"backgrounds2018/ST_tW_antitop"
# sample_path = f"backgrounds2018/ST_tW_top"
# sample_path = f"backgrounds2018/ttHToMuMu"
# sample_path = f"backgrounds2018/ttHTobb"
# sample_path = f"backgrounds2018/DYJetsToMuMu_M-50"

# sample_path = f"backgrounds2018/ST_t-channel_antitop"
# sample_path = f"backgrounds2018/ST_t-channel_top"
# sample_path = f"backgrounds2018/TTZToLLNuNu"
# sample_path = f"backgrounds2018/TTWJetsToLNu"
# sample_path = f"backgrounds2018/WJetsToLNu"

# QCD
# sample_path = f"backgrounds2018/QCD_Pt_15to30"
# sample_path = f"backgrounds2018/QCD_Pt_30to50"
# sample_path = f"backgrounds2018/QCD_Pt_50to80"
# sample_path = f"backgrounds2018/QCD_Pt_80to120"
# sample_path = f"backgrounds2018/QCD_Pt_120to170"
# sample_path = f"backgrounds2018/QCD_Pt_170to300"
# sample_path = f"backgrounds2018/QCD_Pt_300to470"
# sample_path = f"backgrounds2018/QCD_Pt_470to600"
# sample_path = f"backgrounds2018/QCD_Pt_600to800"
# sample_path = f"backgrounds2018/QCD_Pt_800to1000"
# sample_path = f"backgrounds2018/QCD_Pt_1000to1400"
# sample_path = f"backgrounds2018/QCD_Pt_1400to1800"
# sample_path = f"backgrounds2018/QCD_Pt_1800to2400"
# sample_path = f"backgrounds2018/QCD_Pt_2400to3200"
# sample_path = f"backgrounds2018/QCD_Pt_3200toInf"

# QCD mu enhanced
# sample_path = f"backgrounds2018/QCD_Pt_15to20_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_20to30_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_30to50_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_50to80_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_80to120_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_120to170_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_170to300_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_300to470_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_470to600_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_600to800_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_800to1000_MuEnriched"
# sample_path = f"backgrounds2018/QCD_Pt_1000_MuEnriched"

# Data
# sample_path = f"collision_data2018/SingleMuon2018A"
# sample_path = f"collision_data2018/SingleMuon2018B"
# sample_path = f"collision_data2018/SingleMuon2018C"
# sample_path = f"collision_data2018/SingleMuon2018D"


input_directory = f"{base_path}/{sample_path}/{skim}/"

if doScaleFactors:
  output_dir = f"{input_directory}/histograms/"
  applyMuonScaleFactors = "collision_data" not in sample_path
  applyMuonTriggerScaleFactors = "collision_data" not in sample_path
elif not excludeTriggerSFs:
  output_dir = f"{input_directory}/histograms_noSFs/"
  applyMuonScaleFactors = False
  applyMuonTriggerScaleFactors = False
else:
  output_dir = f"{input_directory}/histograms_noTriggerSFs/"
  applyMuonScaleFactors = True
  applyMuonTriggerScaleFactors = False





