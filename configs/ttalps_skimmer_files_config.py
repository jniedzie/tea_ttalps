from ttalps_samples_list import dasSamples2018, dasData2018, QCD_dasBackgrounds2018, TT_dasBackgrounds2018

max_files = -1

base_path = "/data/dust/user/jniedzie/ttalps_cms"
# base_path = "/data/dust/user/lrygaard/ttalps_cms"


### Input skims ###

# Loose semimuonic skim (merged means each 10 files were merged into one)
# input_skim = "skimmed_looseSemimuonicv1"
# input_skim = "skimmed_looseSemimuonic_v2"
input_skim = "skimmed_looseSemimuonic_v2_merged"

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# input_skim = "skimmed_looseSemimuonicv1_LLPtrigger"

### Output skims ###

# For signal like skim: SR and J/Psi CR with no isolation requirement on the loose muons
# output_skim = "skimmed_looseSemimuonic_v2_SR"

# For signal like skim with Dimuon triggers for LLP trigger study
# output_skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger"

# For ttbar CR skim
output_skim = "skimmed_looseSemimuonic_v2_ttbarCR"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

# For local inputs:
sample_path = ""

input_directory = f"{base_path}/{sample_path}/{input_skim}"
output_trees_dir = f"{base_path}/{sample_path}/{output_skim}/"

samples = dasSamples2018.keys()
# samples = dasData2018.keys()
# samples = QCD_dasBackgrounds2018.keys()
# samples = TT_dasBackgrounds2018.keys()
