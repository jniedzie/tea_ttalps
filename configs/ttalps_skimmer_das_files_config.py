from ttalps_samples_list import dasSamples2018, dasData2018

max_files = -1

base_path = "/data/dust/user/jniedzie/ttalps_cms"
# base_path = "/data/dust/user/lrygaard/ttalps_cms"

# Loose semimuonic skims - unmerged directories to later merge files
# output_skim = "skimmed_looseSemimuonicv1_unmerged"
# output_skim = "skimmed_looseSemimuonic_v2"
output_skim = "skimmed_looseSemimuonic_v2_reproduce"

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# output_skim = "skimmed_looseSemimuonicv1_LLPtrigger_unmerged"

output_dir = ""
input_directory = ""

# # For DAS inputs:
dataset = ""
dbs_instance = "prod/phys03"

# dasSamples = dasSamples2018
dasSamples = dasData2018

# create list datasets_and_output_trees_dirs with tuples (dasSamples value, f"{base_path}/{k}/{output_skim}/") for k is dasSamples key
datasets_and_output_dirs = [(v, f"{base_path}/{k}/{output_skim}/") for k, v in dasSamples.items()]

