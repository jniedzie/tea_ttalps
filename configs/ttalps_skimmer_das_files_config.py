from ttalps_samples_list import *

max_files = -1

base_path = "/data/dust/user/jniedzie/ttalps_cms"
# base_path = "/data/dust/user/lrygaard/ttalps_cms"

# Loose semimuonic skims - unmerged directories to later merge files
# output_skim = "skimmed_looseSemimuonicv1_unmerged"
# output_skim = "skimmed_looseSemimuonic_v2"

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# output_skim = "skimmed_looseSemimuonicv1_LLPtrigger_unmerged"

# Loose non-ttbar skims (vetoing events with b-jets)
# output_skim = "skimmed_looseNonTT_v1"
output_skim = "skimmed_looseNoBjets_lt4jets_v1"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

dbs_instance = "prod/phys03"
dasSamples = dasSamples2018
# dasSamples = dasData2018
# dasSamples = dasSignals2018

dirs = [(v, f"{base_path}/{k}/{output_skim}/") for k, v in dasSamples.items()]

# # For DAS datasets:
dataset = ""
datasets_and_output_trees_dirs = dirs

# # For local path to DAS files:
# input_dasfiles = ""
# input_dasfiles_and_output_trees_dirs = dirs
