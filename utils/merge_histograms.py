from ttalps_samples_list import dasSamples2018, dasData2018, QCD_dasBackgrounds2018
import os
import re

base_path = "/data/dust/user/{}/ttalps_cms"
output_username = os.environ["USER"]

# ------------------------------------------------------------------------------
# Skims
# ------------------------------------------------------------------------------

# SR, J/Psi CR, and tt̄ CR with no isolation requirement on the loose muons
# skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"
skim = "skimmed_looseSemimuonic_v2_ttbarCR"

# For signal like skim with Dimuon triggers for LLP trigger study
# skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger"

# Loose semimuonic skim
# skim = "skimmed_looseSemimuonicv1"

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = "skimmed_looseSemimuonicv1_LLPtrigger"

# ------------------------------------------------------------------------------
# Histograms
# ------------------------------------------------------------------------------

# Default settings (e.g. for tt̄ CR)
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_jetIDSFs"

# SR dimuon cuts applied
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons"

# JPsi dimuon cuts applied
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_JPsiDimuons"

# ------------------------------------------------------------------------------
# Samples
# ------------------------------------------------------------------------------

sample_paths = dasSamples2018.keys()
# sample_paths = dasData2018.keys()
# sample_paths = QCD_dasBackgrounds2018.keys()


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
        input_path = f"{sample_path}/{skim}/{hist_path}/*.root"

        if "collision_data" in input_path:
            year = extract_year(sample_path)

            if year not in input_data_paths:
                input_data_paths[year] = ""

            clean_path = clean_path_after_year(sample_path, year)

            output_data_path[year] = f"{clean_path}_{skim}_{hist_path}.root"
            input_data_paths[year] += f"{base_path.format(output_username)}/{input_path} "
        else:

            output_path = input_path.replace("*.root", "histograms.root")
            os.system(f"rm {base_path.format(output_username)}/{output_path}")
            os.system(
                f"hadd -f -j -k {base_path.format(output_username)}/{output_path} {base_path.format(output_username)}/{input_path}")
            print(f"{output_path=}")

    for year, input_data_path in input_data_paths.items():
        output_data_path = output_data_path[year]
        os.system(f"rm {base_path.format(output_username)}/{output_data_path}")
        os.system(f"hadd -f -j -k {base_path.format(output_username)}/{output_data_path} {input_data_path}")


if __name__ == "__main__":
    main()
