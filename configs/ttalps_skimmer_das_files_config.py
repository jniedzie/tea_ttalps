from ttalps_samples_list import dasBackgrounds2016
from ttalps_samples_list import dasSamples2018, dasData2018, dasSignals2018, TT_dasBackgrounds2018, dasData2018_standard
from ttalps_samples_list import dasBackgrounds2022preEE
import os

max_files = 1

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# Loose semimuonic skims - unmerged directories to later merge files
# output_skim = "skimmed_looseSemimuonicv1_unmerged"
# output_skim = "skimmed_looseSemimuonic_v2"
output_skim = "skimmed_looseSemimuonic_v3_jec"

# Loose semielectronic skims
# output_skim = "skimmed_looseSemielectronic_v1"

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# output_skim = "skimmed_looseSemimuonicv1_LLPtrigger_unmerged"

# Loose non-ttbar skims, vetoing events with too many (b-)jets
# output_skim = "skimmed_looseNonTT_v1"  
# output_skim = "skimmed_looseNoBjets_lt4jets_v1"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1"

# output_skim = "skimmed_looseNoBjets_lt4jets_looseMuonPtGt8GeV_v1"

# Inverted/no MET skims
# output_skim = "skimmed_looseInvertedMet_v1"
# output_skim = "skimmed_looseNoMet_v1"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

applyScaleFactors = {
    "jec" : (False, False),
    "pileup" : (False, False)
}

dbs_instance = "prod/phys03"
# dbs_instance = "prod/global"

# dasSamples = dasBackgrounds2016

# dasSamples = dasSamples2018
# dasSamples = dasData2018
# dasSamples = dasSignals2018
dasSamples = TT_dasBackgrounds2018
# dasSamples = dasData2018_standard

# dasSamples = dasBackgrounds2022preEE

dirs = [(v, f"{base_path}/{k}/{output_skim}/") for k, v in dasSamples.items()]

sampleNames = {v: k for k, v in dasSamples.items()}
sample = ""

# # For DAS datasets:
dataset = ""
datasets_and_output_trees_dirs = dirs

# # For local path to DAS files:
# input_dasfiles = ""
# input_dasfiles_and_output_trees_dirs = dirs
