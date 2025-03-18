from ttalps_samples_list import *
import os

max_files = -1

# input_username = "lrygaard"
input_username = "jniedzie"

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v2", "")

# SR (+J/Psi CR) and tt̄ CR with no isolation requirement on the loose muons
# skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons")
skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons")
# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonicv1_LLPtrigger", "_SRDimuons_TriggerStudy")
# skim = ("skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger", "_SRDimuons_TriggerStudy")

samples = dasSamples2018.keys()
# samples = dasData2018.keys()
# samples = dasBackgrounds2018.keys()
# samples = QCD_dasBackgrounds2018.keys()
# samples = TT_dasBackgrounds2018.keys()
# samples = dasSignals2018.keys()
# samples = dasSignals2018_2GeV.keys()

base_path = "/data/dust/user/{}/ttalps_cms"

applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
  "jetID": False,  # no need to apply jet ID SFs in UL
}

# this has to be here, otherwise the script will not work:
sample_path = ""
output_username = os.environ["USER"]
input_directory = f"{base_path.format(input_username)}/{sample_path}/{skim[0]}/"
output_hists_dir = f"{base_path.format(output_username)}/{sample_path}/{skim[0]}/histograms"

for name, apply in applyScaleFactors.items():
  if not apply:
    continue
  
  output_hists_dir += f"_{name}SFs"

output_hists_dir += f"{skim[1]}/"
