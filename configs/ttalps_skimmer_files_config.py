from ttalps_samples_list import *
import os

max_files = -1

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

### Input skims ###

# Loose semimuonic skim (merged means each 10 files were merged into one)
# input_skim = "skimmed_looseSemimuonic_v2"
# input_skim = "skimmed_looseSemimuonic_v2_merged"

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# input_skim = "skimmed_looseSemimuonicv1_LLPtrigger"

# Loose non-ttbar skims (vetoing events with b-jets)
input_skim = "skimmed_looseNonTT_v1_merged"

### Output skims ###

# Signal like skim: SR, J/Psi CR and Z CR with no isolation requirement on the loose muons
# output_skim = "skimmed_looseSemimuonic_v2_SR"

# Signal like skim with Dimuon triggers for LLP trigger study
# output_skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger"

# tt̄ CR skim
# output_skim = "skimmed_looseSemimuonic_v2_ttbarCR"

# QCD CR (vetoing events with b-jets, but identical to SR otherwise)
output_skim = "skimmed_looseNonTT_v1_QCDCR"

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
