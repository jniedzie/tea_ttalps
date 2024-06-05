import ttalps_samples_list.py

max_files = -1

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
skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso_goldenJson"

# skim = "skimmed_ttZSemimuonicCR_tightMuon_noLooseMuonIso"
# skim = "skimmed_ttZSemimuonicCR_Met50GeV"

# skim = "skimmed_looseSemimuonic_SRmuonic_DR"
# skim = "skimmed_looseSemimuonic_SRmuonic_OuterDR"
# skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1"

base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"
# base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms"

applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
}

samples = backgrounds2018 + signals2018 + data2018

# this has to be here, otherwise the script will not work:
sample_path = ""
input_directory = f"{base_path}/{sample_path}/{skim}/"

output_dir = f"{input_directory}/histograms"

for name, apply in applyScaleFactors.items():
  if not apply:
    continue
  
  output_dir += f"_{name}SFs"
  
output_dir += "/"
