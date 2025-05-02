from ttalps_samples_list import dasSamples2018, dasData2018, dasBackgrounds2018, dasSignals2018, dasData2018_standard
import os

max_files = -1

# input_username = "lrygaard"
input_username = "jniedzie"

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v2", "")

# SR, J/Psi CR, ttZ CR (no isolation requirement on the loose muons)
skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuonsNoIso", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuonsWithIso", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons")

# other CRs
# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "")
# skim = ("skimmed_looseSemielectronic_v1_ttbarCR", "", "")
# skim = ("skimmed_looseNonTT_v1_VVCR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseNoBjets_lt4jets_v1_merged", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")  # QCD CR
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons", "_LooseNonLeadingMuonsVertexSegmentMatch")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonic_v2_LLPtrigger_SR", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_notrigger_SR", "_SRDimuons")

# samples = dasSamples2018.keys()
# samples = dasData2018.keys()
samples = dasBackgrounds2018.keys()
# samples = dasSignals2018.keys()
# samples = dasData2018_standard.keys()

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

output_hists_dir += f"{skim[1]}{skim[2]}/"
