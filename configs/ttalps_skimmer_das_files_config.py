from ttalps_samples_list import dasData2016preVFP, dasBackgrounds2016preVFP, dasSignals2016preVFP
from ttalps_samples_list import dasData2016postVFP, dasBackgrounds2016postVFP, dasSignals2016postVFP
from ttalps_samples_list import dasData2017, dasBackgrounds2017, dasSignals2017
from ttalps_samples_list import dasData2018, dasBackgrounds2018, dasSignals2018

from ttalps_samples_list import dasData2022preEE, dasBackgrounds2022preEE, dasSignals2022preEE
from ttalps_samples_list import dasData2022postEE, dasBackgrounds2022postEE, dasSignals2022postEE

from ttalps_samples_list import dasData2023preBPix, dasBackgrounds2023preBPix, dasSignals2023preBPix
from ttalps_samples_list import dasData2023postBPix, dasBackgrounds2023postBPix, dasSignals2023postBPix

import teaHelpers as tea

import os
import subprocess
from Logger import info, error

max_files = -1

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# Loose semimuonic
output_skim = "skimmed_looseSemimuonic_v3"

dbs_instance = "prod/phys03"
# dbs_instance = "prod/global"

dasSamples = dasData2018
year = tea.get_year_from_samples(dasSamples.keys())

# For DAS datasets:


def get_input_output_file_lists():
  input_output_file_lists = []

  for path, das_dataset in dasSamples.items():
    command = f"dasgoclient --query='file dataset={das_dataset} instance={dbs_instance}'"
    info(f"Running command: {command}")
    das_files = subprocess.check_output(command, shell=True, text=True).strip().split('\n')

    if das_files == ['']:
      error(f"No files found for dataset {das_dataset}, skipping...")
      continue

    input_output_file_list = []

    for input_path in das_files:
      input_file_name = input_path.split('/')[-1].split('.')[0]
      input_part = input_path.split('/')[-2]
      input_date_tag = input_path.split('/')[-3]

      output_file = (
          f"{base_path}/{path}/{output_skim}/"
          f"{input_file_name}_{input_date_tag}_{input_part}.root"
      )
      input_output_file_list.append((input_path, output_file, "/dev/null"))

    input_output_file_lists.append(input_output_file_list)

  return input_output_file_lists

# # For local path to DAS files:
# output_trees_dir = ""
# output_hists_dir = ""
# input_directory = ""
# input_dasfiles = ""
# input_dasfiles_and_output_trees_dirs = [(v, f"{base_path}/{k}/{output_skim}/") for k, v in dasSamples.items()]
