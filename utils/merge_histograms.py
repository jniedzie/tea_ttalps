from ttalps_samples_list import *
import os
import re
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--single_thread", action="store_true", default=False, help="Use single thread.")
args = parser.parse_args()

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v2", "")

# SR (+J/Psi CR), tt̄ CR, and QCD CR, with no isolation requirement on the loose muons
# skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons")
# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "")
# skim = ("skimmed_looseNonTT_v1_QCDCR", "_SRDimuons")
# skim = ("skimmed_looseNoBjets_lt4jets_v1_QCDCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "_SRDimuons")
skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonicv1_LLPtrigger", "_SRDimuons_TriggerStudy")
# skim = ("skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger", "_SRDimuons_TriggerStudy")

hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs{skim[1]}"

# ------------------------------------------------------------------------------
# Samples
# ------------------------------------------------------------------------------

sample_paths = dasSamples2018.keys()
# sample_paths = dasData2018.keys()
# sample_paths = QCD_dasBackgrounds2018.keys()
# sample_paths = TT_dasBackgrounds2018.keys()
# sample_paths = dasSignals2018_2GeV.keys()


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
      os.system(f"rm {base_path}/{output_path}")
      os.system(
          f"{'hadd -f -k ' if args.single_thread else 'hadd -f -j -k '}"
          f"{base_path}/{output_path} "
          f"{base_path}/{input_path}")
      print(f"{output_path=}")

  for year, input_data_path in input_data_paths.items():
    output_data_path = output_data_path[year]
    os.system(f"rm {base_path}/{output_data_path}")
    os.system(f"hadd -f -j -k {base_path}/{output_data_path} {input_data_path}")


if __name__ == "__main__":
  main()
