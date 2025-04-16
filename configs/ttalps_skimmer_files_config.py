from ttalps_samples_list import dasSamples2018, dasBackgrounds2018, dasData2018, dasSignals2018
import os

max_files = -1

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

### Input skims ###

# Loose semimuonic skim (merged means each 10 files were merged into one)
# input_skim = "skimmed_looseSemimuonic_v2"
input_skim = "skimmed_looseSemimuonic_v2_merged"

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# input_skim = "skimmed_looseSemimuonicv1_LLPtrigger"

# Loose non-ttbar skims (vetoing events with b-jets)
# input_skim = "skimmed_looseNonTT_v1_merged"
# input_skim = "skimmed_looseNoBjets_lt4jets_v1_merged"
# input_skim = "skimmed_loose_lt3bjets_lt4jets_v1_merged"

### Output skims ###

# Signal like skim: SR, J/Psi CR and Z CR with no isolation requirement on the loose muons
output_skim = "skimmed_looseSemimuonic_v2_SR"
# output_skim = "skimmed_looseSemimuonic_v2_SR_muEtaLt1p2"
# output_skim = "skimmed_looseSemimuonic_v2_SR_muEtaLt1p2_muPtGt10"
# output_skim = "skimmed_looseSemimuonic_v2_SR_muEtaLt1p2_muPtGt7"

# Signal like skim with Dimuon triggers for LLP trigger study
# output_skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger"

# tt̄ CR skim
# output_skim = "skimmed_looseSemimuonic_v2_ttbarCR"

# Loose non-ttbar skims, vetoing events with too many (b-)jets
# output_skim = "skimmed_looseNonTT_v1_QCDCR"  # this is in fact VV CR
# output_skim = "skimmed_looseNoBjets_lt4jets_v1_QCDCR"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1_bbCR"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt10"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt20"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1_bbCR_muPtGt20"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

# For local inputs:
sample_path = ""

input_directory = f"{base_path}/{sample_path}/{input_skim}"
output_trees_dir = f"{base_path}/{sample_path}/{output_skim}/"

samples = dasSamples2018.keys()
# samples = dasBackgrounds2018.keys()
# samples = dasSignals2018.keys()
# samples = dasData2018.keys()
