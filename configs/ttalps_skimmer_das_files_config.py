from ttalps_samples_list import *
import os

max_files = -1

# base_path = "/data/dust/user/jniedzie/ttalps_cms"
base_path = "/data/dust/user/lrygaard/ttalps_cms"

# Loose semimuonic skims - unmerged directories to later merge files
# output_skim = "skimmed_looseSemimuonicv1_unmerged"
output_skim = "skimmed_looseSemimuonic_v2"

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# output_skim = "skimmed_looseSemimuonicv1_LLPtrigger_unmerged"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

# # For DAS datasets:
# dataset = ""
# # For local path to DAS files:
input_dasfiles = ""

dbs_instance = "prod/phys03"
dasSamples = TT_dasBackgrounds2022preEE

# create list datasets_and_output_trees_dirs with tuples (dasSamples value, f"{base_path}/{k}/{output_skim}/") for k is dasSamples key
# datasets_and_output_trees_dirs = [(v, f"{base_path}/{k}/{output_skim}/") for k, v in dasSamples.items()]

# create list input_dasfiles_and_output_trees_dirs with tuples (dasSamples value, f"{base_path}/{k}/{output_skim}/") for k is dasSamples key
input_dasfiles_and_output_trees_dirs = [(v, f"{base_path}/{k}/{output_skim}/") for k, v in dasSamples.items()]
