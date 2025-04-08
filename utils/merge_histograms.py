from ttalps_samples_list import *
import os
import re
import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("--single_thread", action="store_true", default=False, help="Use single thread.")
parser.add_argument("--condor", action="store_true", default=False, help="Run on condor.")
args = parser.parse_args()

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v2", "")

# SR (+J/Psi CR), tt̄ CR, and QCD CR, with no isolation requirement on the loose muons
skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2_muPtGt10", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2_muPtGt7", "_SRDimuons")

# skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons")
# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "")
# skim = ("skimmed_looseNonTT_v1_QCDCR", "_SRDimuons")
# skim = ("skimmed_looseNoBjets_lt4jets_v1_QCDCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt10", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt20", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_muPtGt20", "_SRDimuons")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonicv1_LLPtrigger", "_SRDimuons_TriggerStudy")
# skim = ("skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger", "_SRDimuons_TriggerStudy")

# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs{skim[1]}"
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}"
hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}_newSFs" # all SFs
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs{skim[1]}_newSFs" # no PUjetIDSFs
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_PUjetIDSFs{skim[1]}_newSFs" # no bTaggingSFs
# hist_path = f"histograms_muonSFs_muonTriggerSFs_bTaggingSFs_PUjetIDSFs{skim[1]}_newSFs" # no pilup
# hist_path = f"histograms_muonSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}_newSFs" # no muonTriggerSFs
# hist_path = f"histograms_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}_newSFs" # no muonSF

# ------------------------------------------------------------------------------
# Samples
# ------------------------------------------------------------------------------

# sample_paths = dasSamples2018.keys()
# sample_paths = dasData2018.keys()
sample_paths = dasBackgrounds2018.keys()
# sample_paths = TT_dasBackgrounds2018.keys()
# sample_paths = dasSignals2018.keys()
# sample_paths = dasSignals2018_12GeV.keys()


def extract_year(s):
  match = re.search(r'(20\d{2})(?!\d)', s)
  return int(match.group(1)) if match else None


def clean_path_after_year(s, year):
  parts = s.split(str(year))
  clean_path = str(year).join(parts[:-1]) + str(year)
  return clean_path


def main():
  input_data_paths = {}
  output_data_path = {}

  commands = []

  for sample_path in sample_paths:
    print(f"{sample_path=}")
    input_path = f"{sample_path}/{skim[0]}/{hist_path}/*.root"

    if "collision_data" in input_path:
      year = extract_year(sample_path)

      if year not in input_data_paths:
        input_data_paths[year] = ""

      clean_path = clean_path_after_year(sample_path, year)

      output_data_path[year] = f"{clean_path}_{skim[0]}_{hist_path}.root"
      input_data_paths[year] += f"{base_path}/{input_path} "
    else:
      output_path = input_path.replace("*.root", "histograms.root")
      command = f"rm {base_path}/{output_path}; "
      command += f"{'hadd -f -k ' if args.single_thread else 'hadd -f -j -k '}"
      command += f"{base_path}/{output_path} "
      command += f"{base_path}/{input_path}"
      commands.append(command)

  for year, input_data_path in input_data_paths.items():
    output_data_path = output_data_path[year]
    command = f"rm {base_path}/{output_data_path}; "
    command += f"{'hadd -f -k ' if args.single_thread else 'hadd -f -j -k '}"
    command += f"{base_path}/{output_data_path} "
    command += f"{input_data_path}"

    commands.append(command)

  if args.condor:
    
    os.makedirs("scripts", exist_ok=True)
    with open("merge_cmds.txt", "w") as f:
      for i, cmd in enumerate(commands):
        script_name = f"scripts/job_{i}.sh"
        with open(script_name, "w") as sf:
          sf.write("#!/bin/bash\n")
          sf.write(cmd + "\n")
        os.chmod(script_name, 0o755)
        f.write(script_name + "\n")

    # Create the submit file
    submit_file = "submit_merge_jobs.sub"
    with open(submit_file, "w") as f:
      f.write('''\
    universe   = vanilla
    executable = $(cmd)
    # output     = /dev/null
    # error      = /dev/null
    # log        = /dev/null
    output     = ./output/$(ClusterId).$(ProcId).out
    error      = ./error/$(ClusterId).$(ProcId).err
    log        = ./log/$(ClusterId).log
    request_cpus = 16
    request_memory = 16000MB
    initialdir = .
    getenv = True
    queue cmd from merge_cmds.txt
    ''')

    # Submit the jobs
    subprocess.run(["condor_submit", submit_file], check=True)
  else:
    for command in commands:
      os.system(command)


if __name__ == "__main__":
  main()
