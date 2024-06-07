from ttalps_samples_list import *
import os

max_files = 1

# skim = "skimmed_looseSemimuonic_looseMuon_looseBjet_goldenJson"
# skim = "skimmed_looseSemimuonic"
# skim = "LLPnanoAODv1merged"

# skim = "skimmed_ttbarLike"
# skim = "skimmed_ttZLike"
# skim = "skimmed_ttbarSemimuonicCR_tightMuon"
# skim = "skimmed_ttbarSemimuonicCR_tightMuon_newBtag"
# skim = "skimmed_ttbarSemimuonicCR"
# skim = "skimmed_ttbarSemimuonicCR_Met30GeV"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_2mediumBjets"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_2tightBjets"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso_goldenJson"

# skim = "skimmed_ttZSemimuonicCR_tightMuon_noLooseMuonIso"
# skim = "skimmed_ttZSemimuonicCR_Met50GeV"

# skim = "skimmed_looseSemimuonic_SRmuonic_DR"
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

# samples = backgrounds2018 + signals2018 + data2018
# samples = backgrounds2018 + signals2018
samples = signals2018

# this has to be here, otherwise the script will not work:
sample_path = ""
input_directory = f"{base_path.format(input_username)}/{sample_path}/{skim}/"
output_hists_dir = f"{input_directory}/histograms"

for name, apply in applyScaleFactors.items():
  if not apply:
    continue
  
  output_hists_dir += f"_{name}SFs"
  
output_hists_dir += "/"
