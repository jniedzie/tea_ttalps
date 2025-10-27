from ttalps_samples_list import dasBackgrounds2016PreVFP, dasData2016PreVFP
from ttalps_samples_list import dasBackgrounds2016PostVFP, dasData2016PostVFP
import os
import subprocess
from Logger import info

max_files = -1

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# Loose semimuonic skims - unmerged directories to later merge files
output_skim = "skimmed_looseSemimuonic_v2"

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

dbs_instance = "prod/phys03"
# dbs_instance = "prod/global"

dasSamples = dasBackgrounds2018

# # For DAS datasets:
input_output_file_list = []

for path, das_dataset in dasSamples.items():
  command = f"dasgoclient --query='file dataset={das_dataset} instance={dbs_instance}'"
  info(f"Running command: {command}")
  das_files = subprocess.check_output(command, shell=True, text=True).strip().split('\n')

  for input_path in das_files:

    input_file_name = input_path.split('/')[-1].split('.')[0]
    input_part = input_path.split('/')[-2]
    input_date_tag = input_path.split('/')[-3]

    input_output_file_list.append((input_path, f"{base_path}/{path}/{output_skim}/{input_file_name}_{input_date_tag}_{input_part}.root", "/dev/null"))


# # For local path to DAS files:
# input_dasfiles = ""
# input_dasfiles_and_output_trees_dirs = dirs
