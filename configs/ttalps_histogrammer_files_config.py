import teaHelpers as tea

from ttalps_samples_list import dasData2016preVFP, dasBackgrounds2016preVFP, dasSignals2016preVFP
from ttalps_samples_list import dasData2016postVFP, dasBackgrounds2016postVFP, dasSignals2016postVFP
from ttalps_samples_list import dasData2017, dasBackgrounds2017, dasSignals2017
from ttalps_samples_list import dasData2018, dasBackgrounds2018, dasSignals2018

from ttalps_samples_list import dasData2022preEE, dasBackgrounds2022preEE, dasSignals2022preEE
from ttalps_samples_list import dasData2022postEE, dasBackgrounds2022postEE, dasSignals2022postEE

from ttalps_samples_list import dasData2023preBPix, dasBackgrounds2023preBPix, dasSignals2023preBPix
from ttalps_samples_list import dasData2023postBPix, dasBackgrounds2023postBPix, dasSignals2023postBPix
import os

max_files = -1
samples = dasSignals2017.keys()

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v2_merged", "", "")
# skim = ("skimmed_looseSemimuonic_v2", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# SR, J/Psi CR skim
skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuonsNoChi2", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "LooseNonLeadingPATMuonsVertex")

# other CRs
# skim = ("skimmed_looseSemimuonic_v3_ttbarCR", "", "")
# skim = ("skimmed_looseSemimuonic_v2_ttbarLike1DSA", "", "")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonic_v2_SR_noTrigger", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# For leading tight muon study: do not use NonLeadingMuons:
# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "SRDimuons", "LooseMuonsVertexSegmentMatch")

if "ttbarCR" in skim[0]:
  input_username = "jniedzie"
elif "merged" in skim[0]:
  input_username = "jalimena"
else:
  input_username = "lrygaard"

year = tea.get_year_from_samples(samples)
base_path = "/data/dust/user/{}/ttalps_cms"

applyScaleFactors = {
    # name : (apply nominal, apply variation)
    "muon": (True, True),
    "dsamuon": (True, True),
    "muonTrigger": (True, True),
    "pileup": (True, True),
    "bTagging": (True, True),
    "PUjetID": (True, True),
    "dimuonEff": (True, True),
    "jec": (False, True),
    "L1PreFiringWeight": (True, True),
}

hist_path = "histograms"

if skim[1] != "":
  hist_path += f"_{skim[1]}"

if "dimuonEff" in applyScaleFactors and "ttbarCR" not in skim[0]:
  if applyScaleFactors["dimuonEff"][0] is False:
    hist_path += "_noDimuonEffSFs"

# hist_path += "_ABCD/"
# hist_path += "_nminus1/"
# hist_path += "_withLeadingTightMuon_genInfo/"
# hist_path += "_genInfo/"
# hist_path += "_revertedMatching_nminus1/"
# hist_path += "_fakes/"

# this has to be here, otherwise the script will not work:
sample_path = ""
output_username = os.environ["USER"]
input_directory = f"{base_path.format(input_username)}/{sample_path}/{skim[0]}/"

output_hists_dir = f"{base_path.format(output_username)}/{sample_path}/{skim[0]}/{hist_path}/"
