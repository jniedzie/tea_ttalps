from ttalps_samples_list import backgrounds2018, signals2018, data2018

max_files = -1

# base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"
base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms"


### Input skims ###

# Loose semimuonic skim
input_skim = "skimmed_looseSemimuonicv1"
# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# input_skim = "skimmed_looseSemimuonicv1_LLPtrigger"

### Output skims ###

# For signal like skim: SR and J/Psi CR with no isolation requirement on the loose muons
output_skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"

# For signal like skim with Dimuon triggers for LLP trigger study
# output_skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

# For local inputs:
sample_path = ""

input_directory = f"{base_path}/{sample_path}/{input_skim}"
output_trees_dir = f"{base_path}/{sample_path}/{output_skim}/"

samples = backgrounds2018 + signals2018 + data2018
