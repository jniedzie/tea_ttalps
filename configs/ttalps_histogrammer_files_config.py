from ttalps_samples_list import dasSamples2018, dasData2018, dasBackgrounds2018, dasSignals2018
import os

max_files = -1

# input_username = "lrygaard"
input_username = "jniedzie"

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

# skim = ("skimmed_looseNonTT_v1_QCDCR", "_SRDimuons")  # this is in fact VV CR
# skim = ("skimmed_looseNoBjets_lt4jets_v1_QCDCR", "_SRDimuons")

# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt10", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt20", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_muPtGt20", "_SRDimuons")


# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonic_v2_LLPtrigger_SR", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_notrigger_SR", "_SRDimuons")

samples = dasSamples2018.keys()
# samples = dasData2018.keys()
# samples = dasBackgrounds2018.keys()
# samples = dasSignals2018.keys()

base_path = "/data/dust/user/{}/ttalps_cms"

applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
  "PUjetID": True,
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
