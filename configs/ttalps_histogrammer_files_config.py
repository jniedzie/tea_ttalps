from ttalps_samples_list import backgrounds2018, signals2018, data2018, signals2018_1GeV, test_backgrounds2018
import os

max_files = -1

# skim = "skimmed_looseSemimuonic"
# skim = "LLPnanoAODv1merged"

# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso_goldenJson"
# skim = "skimmed_ttZSemimuonicCR_Met50GeV"

# skim = "skimmed_looseSemimuonic_SRmuonic_OuterDR"
skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1"


base_path = "/nfs/dust/cms/user/{}/ttalps_cms"
input_username = "lrygaard"
output_username = os.environ["USER"]


applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
}

samples = backgrounds2018 + signals2018_1GeV + data2018
# samples = test_backgrounds2018

# this has to be here, otherwise the script will not work:
sample_path = ""
input_directory = f"{base_path.format(input_username)}/{sample_path}/{skim}/"
output_hists_dir = f"{input_directory}/histograms"

for name, apply in applyScaleFactors.items():
  if not apply:
    continue
  
  output_hists_dir += f"_{name}SFs"
  
output_hists_dir += "/"
