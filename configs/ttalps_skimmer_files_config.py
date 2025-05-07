from ttalps_samples_list import dasSamples2018, dasBackgrounds2018, dasData2018, dasSignals2018, dasData2018_standard
import os

max_files = -1

input_user = "jniedzie"
# input_user = "lrygaard"
input_base_path = f"/data/dust/user/{input_user}/ttalps_cms"
output_base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"


# Signal like skim: SR, J/Psi CR and Z CR with no isolation requirement on the loose muons
input_skim = "skimmed_looseSemimuonic_v2_merged"
output_skim = "skimmed_looseSemimuonic_v2_SR"

# tt̄ (μ+jets) CR
# input_skim = "skimmed_looseSemimuonic_v2_merged"
# output_skim = "skimmed_looseSemimuonic_v2_ttbarCR"

# tt̄ (e+jets) CR
# input_skim = "skimmed_looseSemielectronic_v1_merged"
# output_skim = "skimmed_looseSemielectronic_v1_ttbarCR"

# VV CR
# input_skim = "skimmed_looseNonTT_v1_merged"
# output_skim = "skimmed_looseNonTT_v1_VVCR"

# QCD CR
# input_skim = "skimmed_looseNoBjets_lt4jets_v1_merged"
# output_skim = "skimmed_looseNoBjets_lt4jets_v1_QCDCR"

# W+jets CR
# input_skim = "skimmed_loose_lt3bjets_lt4jets_v1_merged"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR"

# bb CR
# input_skim = "skimmed_loose_lt3bjets_lt4jets_v1_merged"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1_bbCR"

# Skims with no triggers for LLP trigger study
# input_skim = "skimmed_looseSemimuonic_v2_notrigger_merged"
# output_skim = "skimmed_looseSemimuonic_v2_notrigger_SR"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

# For local inputs:
sample_path = ""

input_directory = f"{input_base_path}/{sample_path}/{input_skim}"
output_trees_dir = f"{output_base_path}/{sample_path}/{output_skim}/"

samples = dasSamples2018.keys()
# samples = dasBackgrounds2018.keys()
# samples = dasSignals2018.keys()
# samples = dasData2018.keys()
# samples = dasData2018_standard.keys()
