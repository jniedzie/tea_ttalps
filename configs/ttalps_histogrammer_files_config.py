from ttalps_samples_list import backgrounds2018, signals2018, data2018, signals2018_1GeV, test_backgrounds2018, test_signals2018
import os

max_files = -1

# Loose semimuonic skim
skim = "skimmed_looseSemimuonicv1"
# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = "skimmed_looseSemimuonicv1_LLPtrigger"

# For signal like skim: SR and J/Psi CR with no isolation requirement on the loose muons
# skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"

# For signal like skim with Dimuon triggers for LLP trigger study
# skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger"

base_path = "/data/dust/user/{}/ttalps_cms"
input_username = "lrygaard"
output_username = os.environ["USER"]


applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
}

# samples = data2018
# samples = backgrounds2018 + signals2018_1GeV
# samples = backgrounds2018
# samples = signals2018_1GeV
samples = test_signals2018

# this has to be here, otherwise the script will not work:
sample_path = ""
input_directory = f"{base_path.format(input_username)}/{sample_path}/{skim}/"
output_hists_dir = f"{input_directory}/histograms"

for name, apply in applyScaleFactors.items():
  if not apply:
    continue
  
  output_hists_dir += f"_{name}SFs"
  
# output_hists_dir += "_JPsiDimuons"
output_hists_dir += "_SRDimuons"
# output_hists_dir += "_SRDimuons_TriggerStudy"
output_hists_dir += "/"
