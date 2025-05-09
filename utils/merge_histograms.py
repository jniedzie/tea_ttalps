from ttalps_samples_list import dasSamples2018, dasData2018, dasBackgrounds2018, dasSignals2018, dasData2018_standard
import os
import re
import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("--single_thread", action="store_true", default=False, help="Use single thread.")
parser.add_argument("--condor", action="store_true", default=False, help="Run on condor.")
parser.add_argument("--dry", action="store_true", default=False, help="Dry run.")
args = parser.parse_args()

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v2", "")

# SR, J/Psi CR, ttZ CR (no isolation requirement on the loose muons)
skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR_looseMuonPtGt8GeV", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuonsNoIso", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR_looseMuonPtGt8GeV", "_JPsiDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")

# skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuonsWithIso", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons")

# other CRs
# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "", "")
# skim = ("skimmed_looseSemielectronic_v1_ttbarCR", "", "")
# skim = ("skimmed_looseNonTT_v1_VVCR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseNoBjets_lt4jets_v1_merged", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")  # QCD CR
# skim = ("skimmed_looseNoBjets_lt4jets_looseMuonPtGt5GeV_v1_merged", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")  # QCD CR
# skim = ("skimmed_looseNoBjets_lt4jets_v1_looseMuonPtGt8GeV", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")  # QCD CR
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonicv1_LLPtrigger", "SRDimuons_TriggerStudy")
# skim = ("skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger", "SRDimuons_TriggerStudy")

hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs"
if skim[1] != "":
  hist_path += f"_{skim[1]}"
if skim[2] != "":
  hist_path += f"_{skim[2]}"

# ------------------------------------------------------------------------------
# Samples
# ------------------------------------------------------------------------------

# sample_paths = dasSamples2018.keys()
sample_paths = dasData2018.keys()
# sample_paths = dasBackgrounds2018.keys()
# sample_paths = list(dasBackgrounds2018.keys()) + list(dasData2018_standard.keys())
# sample_paths = dasSignals2018.keys()
# sample_paths = dasData2018_standard.keys()
# sample_paths = list(dasBackgrounds2018.keys()) + list(dasData2018.keys())


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
    if not args.dry:
      subprocess.run(["condor_submit", submit_file], check=True)
  else:
    for command in commands:
      if args.dry:
        print(command)
      else:
        os.system(command)


if __name__ == "__main__":
  main()
