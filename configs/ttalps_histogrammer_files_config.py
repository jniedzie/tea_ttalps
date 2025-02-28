from ttalps_samples_list import dasSamples2018, dasData2018, QCD_dasBackgrounds2018, TT_dasBackgrounds2018
import os

max_files = -1

# Loose semimuonic skim
# skim = "skimmed_looseSemimuonicv1"
# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = "skimmed_looseSemimuonicv1_LLPtrigger"

# SR (+J/Psi CR) and tt̄ CR with no isolation requirement on the loose muons
# skim = "skimmed_looseSemimuonic_v2_SR"
skim = "skimmed_looseSemimuonic_v2_ttbarCR"

# For signal like skim with Dimuon triggers for LLP trigger study
# skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger"

base_path = "/data/dust/user/{}/ttalps_cms"
# input_username = "lrygaard"
input_username = "jniedzie"
output_username = os.environ["USER"]

applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
  "jetID": False,  # no need to apply jet ID SFs in UL
}

samples = dasSamples2018.keys()
# samples = dasData2018.keys()
# samples = QCD_dasBackgrounds2018.keys()
# samples = TT_dasBackgrounds2018.keys()

# this has to be here, otherwise the script will not work:
sample_path = ""
input_directory = f"{base_path.format(input_username)}/{sample_path}/{skim}/"
output_hists_dir = f"{base_path.format(output_username)}/{sample_path}/{skim}/histograms"

for name, apply in applyScaleFactors.items():
  if not apply:
    continue
  
  output_hists_dir += f"_{name}SFs"
  
output_hists_dir += "_JPsiDimuons"
# output_hists_dir += "_SRDimuons"
# output_hists_dir += "_SRDimuons_TriggerStudy"

output_hists_dir += "/"
