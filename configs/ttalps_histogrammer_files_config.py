from ttalps_samples_list import dasSamples2018, dasData2018, dasBackgrounds2018, dasSignals2018, dasData2018_standard
import os

max_files = -1

# input_username = "lrygaard"
input_username = "jniedzie"

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v2", "")
# skim = ("skimmed_looseSemimuonic_v2", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# SR, J/Psi CR, ttZ CR (no isolation requirement on the loose muons)
skim = ("skimmed_looseSemimuonic_v2_SR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "SRDimuonsNoIso", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "JPsiDimuonsWithIso", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR", "JPsiDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR", "ZDimuons")

# other CRs
# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "", "")
# skim = ("skimmed_looseSemielectronic_v1_ttbarCR", "", "")
# skim = ("skimmed_looseNonTT_v1_VVCR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseNoBjets_lt4jets_v1_merged", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")  # QCD CR
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonic_v2_LLPtrigger_SR", "SRDimuons", "")
# skim = ("skimmed_looseSemimuonic_v2_notrigger_SR", "SRDimuons", "")
# skim = ("skimmed_looseSemimuonic_v2_notrigger_SR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# samples = dasSamples2018.keys()
# samples = dasData2018.keys()
samples = dasBackgrounds2018.keys()
# samples = dasSignals2018.keys()
# samples = dasData2018_standard.keys()

base_path = "/data/dust/user/{}/ttalps_cms"

applyScaleFactors = {
  # name : (apply nominal, apply variation)
  "muon": (True, True),
  "muonTrigger": (True, True),
  "pileup": (True, True),
  "bTagging": (True, True),
  "PUjetID": (True, True),
  # "JpsiInvMassSFs": (True, True),
  # "jetEnergy" : (False, True),
  # "met" : (False, True),
  # "QCDscale" : (False, True),
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

if skim[1] != "":
  output_hists_dir += f"_{skim[1]}"
if skim[2] != "":
  output_hists_dir += f"_{skim[2]}"
output_hists_dir += "/"
