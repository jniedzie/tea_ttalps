import ttalps_samples_list.py

max_files = -1

# base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"
base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms"

# Loose skims
# output_skim = "skimmed_looseSemimuonicv1"

# CRs
# output_skim = "skimmed_ttbarLike"
# output_skim = "skimmed_ttbarSemimuonicCR_tightMuon"
# output_skim = "skimmed_ttbarSemimuonicCR_tightMuon_newBtag"
# output_skim = "skimmed_ttbarSemimuonicCR"
# output_skim = "skimmed_ttbarSemimuonicCR_Met30GeV"
# output_skim = "skimmed_ttbarSemimuonicCR_Met50GeV_2mediumBjets"
# output_skim = "skimmed_ttbarSemimuonicCR_Met50GeV_2tightBjets"
# output_skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso"
# output_skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso_goldenJson"

# output_skim = "skimmed_ttZSemimuonicCR_tightMuon_noLooseMuonIso"
# output_skim = "skimmed_ttZSemimuonicCR_Met50GeV"

# SRs
# output_skim = "skimmed_looseSemimuonic_SRmuonic_DR"
# output_skim = "skimmed_looseSemimuonic_SRmuonic_OuterDR"
output_skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""


# # For DAS inputs:
# dataset = ""
# dbs_instance = "prod/phys03"
# # create dict datasets_and_output_trees_dirs with the key as the values in the dasbackgrounds2018 and dasSignals2018 dicts and the value as f"{base_path}/key/{skim}/") with key in dasbackgrounds2018 and dasSignals2018
# datasets_and_output_trees_dirs = {v: f"{base_path}/{k}/{output_skim}/" for k, v in dasbackgrounds2018.items()}
# datasets_and_output_trees_dirs.update({v: f"{base_path}/{k}/{output_skim}/" for k, v in dasSignals2018.items()})
# datasets_and_output_trees_dirs.update({v: f"{base_path}/{k}/{output_skim}/" for k, v in dasData2018.items()})


# # For local inputs:
sample_path = ""
# Loose skims
# input_skim = "skimmed_looseSemileptonic"
# input_skim = "skimmed_looseSemimuonic_tightMuon"
# input_skim = "skimmed_looseSemimuonic_tightMuon_newBtag"
input_skim = "skimmed_looseSemimuonicv1"
# input_skim = "skimmed_looseSemimuonic_looseMuon_looseBjet"
# input_skim = "skimmed_looseSemimuonic_looseMuon_looseBjet_goldenJson"
input_directory = f"{base_path}/{sample_path}/{input_skim}"
output_trees_dir = f"{base_path}/{sample_path}/{output_skim}/"

samples = backgrounds2018 + signals2018 + data2018
