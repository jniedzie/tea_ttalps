from ttalps_samples_list import dasSamples2018, dasSignalsPrivate2018, dasData2018, dasData2018_standard, dasBackgrounds2018, dasSignals2018
from ttalps_samples_list import dasBackgrounds2022preEE, dasSignals2022preEE, dasBackgrounds2023preBPix, dasSignals2023postBPix, dasData2023postBPix
from ttalps_samples_list import dasBackgrounds2017, dasData2017, dasSignals2017, dasSignals2016PreVFP, dasSignals2016PostVFP, dasBackgrounds2016PostVFP, dasData2016PostVFP
from ttalps_samples_list import dasBackgrounds2018Devel, dasData2018Devel
from Logger import warn, logger_print

import argparse
import glob
import os
import ROOT

user = "lrygaard"
# user = "jalimena"
input_base_path = f"/data/dust/user/{user}/ttalps_cms"
output_base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# Loose ttbar semimuonic skim
# skim = "skimmed_looseSemimuonic_v2"

# Loose ttbar semielectronic skim
# skim = "skimmed_looseSemielectronic_v1"

skim = "skimmed_looseSemimuonic_v2_SR_noTrigger"


# Loose non-ttbar skims, vetoing events with too many (b-)jets
# skim = "skimmed_looseNonTT_v1"
# skim = "skimmed_looseNoBjets_lt4jets_v1"
# skim = "skimmed_loose_lt3bjets_lt4jets_v1"
# skim = "skimmed_looseNoBjets_lt4jets_looseMuonPtGt8GeV_v1"

# Inverted/no MET skims
# skim = "skimmed_looseInvertedMet_v1"
# skim = "skimmed_looseNoMet_v1"

# sample_paths = dasSignals2018.keys()
sample_paths = dasBackgrounds2018.keys()

input_pattern = "*.root"
output_pattern = "output_{}.root"

python_path = "python3"

condor_commands = []


def get_args():
  parser = argparse.ArgumentParser(description="merger")
  parser.add_argument("--dry", action="store_true", default=False, help="dry run")
  parser.add_argument("--n", type=int, default=10, help="Number of files to merge into one")
  parser.add_argument("--condor", action="store_true", default=False, help="run on condor")
  parser.add_argument("--fix_broken", action="store_true", default=False, help="only fix broken files")
  args = parser.parse_args()
  return args


def get_file_paths(input_path):
  path_pattern = os.path.join(input_path, input_pattern)
  file_paths = glob.glob(path_pattern)
  print(f"Found {len(file_paths)} files matching pattern {path_pattern}")
  return file_paths


def get_file_name(index, output_path):
  output_filename = output_pattern.format(index)
  output_filename = os.path.join(output_path, output_filename)
  return output_filename


def run_on_condor(commands, dry_run=False):
  submit_file = "condor_submit_file.sub"

  # Create wrapper scripts for each job
  for idx, command in enumerate(commands):
    script_file = f"tmp/condor_command_{idx}.sh"
    with open(script_file, "w") as f:
      f.write("#!/bin/bash\n")
      f.write(command + "\n")
    os.chmod(script_file, 0o755)  # Make it executable

  # Create the Condor submit file
  with open(submit_file, "w") as f:
    f.write("universe = vanilla\n")
    f.write("getenv = True\n")  # Ensure environment variables are inherited
    f.write("request_memory = 4 GB\n")
    f.write("+JobFlavour = \"espresso\"\n")

    # Logging (separate files per job)
    if not dry_run:
      f.write("output = /dev/null\n")
      f.write("error = /dev/null\n")
      f.write("log = /dev/null\n")
    else:
      f.write("output = output/condor_output_$(Process).txt\n")
      f.write("error = error/condor_error_$(Process).txt\n")
      f.write("log = log/condor_log_$(Process).txt\n")

    f.write("\n")

    f.write("max_materialize = 5000\n")

    # Use a single queue submission for all jobs
    f.write("executable = tmp/condor_command_$(Process).sh\n")
    f.write(f"queue {len(commands)}\n")  # Submit all jobs in one go

  # Submit the jobs
  if not dry_run:
    os.system(f"condor_submit {submit_file}")
    os.system(f"rm {submit_file}")


def is_broken_file(file_path):
  # check for ROOT errors
  try:
    print(f"Checking file {file_path}")
    file = ROOT.TFile.Open(file_path)
  except OSError:
    return True

  # check for other errors
  if not file:
    return True
  if file is None:
    return True
  if file.IsZombie():
    return True
  if file.TestBit(ROOT.TFile.kRecovered):
    return True

  return False


def merge_batch_of_files(files_to_merge, output_ntuple_counter, output_path, dry_run, condor, fix_broken):
  output_filename = get_file_name(output_ntuple_counter, output_path)

  if fix_broken:
    if not is_broken_file(output_filename):
      return
    else:
      warn("Found broken file")

  command = f"{python_path} hadd_safe.py -f -j -k {output_filename} {' '.join(files_to_merge)}"

  if condor:
    condor_commands.append(command)
  elif dry_run:
    print(command)
  else:
    os.system(command)


def merge_n_files(input_path, output_path, args):
  file_paths = get_file_paths(input_path)
  files_to_merge = []
  output_ntuple_counter = 0

  if not os.path.exists(output_path):
    os.makedirs(output_path)

  # merge files in batches of n_files_to_merge:
  for filename in file_paths:

    # if full, merge and move to the next batch:
    if len(files_to_merge) == args.n:
      merge_batch_of_files(files_to_merge, output_ntuple_counter, output_path, args.dry, args.condor, args.fix_broken)
      files_to_merge = []
      output_ntuple_counter += 1

    files_to_merge.append(filename)

  # merge any remaining files:
  if len(files_to_merge) != 0:
    merge_batch_of_files(files_to_merge, output_ntuple_counter, output_path, args.dry, args.condor, args.fix_broken)


def main():
  # suppress all ROOT errors, warnings and info messages
  ROOT.gErrorIgnoreLevel = ROOT.kFatal

  args = get_args()

  for path in sample_paths:
    input_path = f"{input_base_path}/{path}/{skim}/"
    output_path = f"{output_base_path}/{path}/{skim}_merged/"
    merge_n_files(input_path, output_path, args)

  if args.condor:
    run_on_condor(condor_commands, args.dry)

  logger_print()


if __name__ == "__main__":
  main()
