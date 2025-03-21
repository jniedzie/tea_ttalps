from ttalps_samples_list import *
import os

max_files = -1

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# Loose semimuonic skims - unmerged directories to later merge files
# output_skim = "skimmed_looseSemimuonicv1_unmerged"
output_skim = "skimmed_looseSemimuonic_v2"

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# output_skim = "skimmed_looseSemimuonicv1_LLPtrigger_unmerged"

# Loose non-ttbar skims (vetoing events with b-jets)
# output_skim = "skimmed_looseNonTT_v1"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

# # For DAS datasets:
# dataset = ""
# # For local path to DAS files:
input_dasfiles = ""

dbs_instance = "prod/phys03"
dasSamples = dasSamples2018
# dasSamples = dasData2018
# dasSamples = dasSignals2018

# create list datasets_and_output_trees_dirs with tuples (dasSamples value, f"{base_path}/{k}/{output_skim}/") for k is dasSamples key
# datasets_and_output_trees_dirs = [(v, f"{base_path}/{k}/{output_skim}/") for k, v in dasSamples.items()]

# create list input_dasfiles_and_output_trees_dirs with tuples (dasSamples value, f"{base_path}/{k}/{output_skim}/") for k is dasSamples key
input_dasfiles_and_output_trees_dirs = [(v, f"{base_path}/{k}/{output_skim}/") for k, v in dasSamples.items()]
