from ttalps_samples_list import backgrounds2018, signals2018, data2018

max_files = -1

# base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"
base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms"


### Input skims ###

# input_skim = "skimmed_looseSemileptonic"
# input_skim = "skimmed_looseSemimuonic_tightMuon"
# input_skim = "skimmed_looseSemimuonic_tightMuon_newBtag"
input_skim = "skimmed_looseSemimuonicv1"
# input_skim = "skimmed_looseSemimuonic_looseMuon_looseBjet"
# input_skim = "skimmed_looseSemimuonic_looseMuon_looseBjet_goldenJson"

### Output skims ###

# CRs
# output_skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso_goldenJson"
# output_skim = "skimmed_ttZSemimuonicCR_Met50GeV"

# SRs
# output_skim = "skimmed_looseSemimuonic_SRmuonic_OuterDR"
# output_skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

# For local inputs:
sample_path = ""

input_directory = f"{base_path}/{sample_path}/{input_skim}"
output_trees_dir = f"{base_path}/{sample_path}/{output_skim}/"

samples = backgrounds2018 + signals2018 + data2018
