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

input_username = "lrygaard"
# input_username = "jalimena"
# input_username = "jniedzie"

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v2_merged", "", "")
# skim = ("skimmed_looseSemimuonic_v2", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# SR, J/Psi CR skim without segment match ratio
skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# other CRs
# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "", "")
# skim = ("skimmed_looseSemielectronic_v1_ttbarCR", "", "")
# skim = ("skimmed_looseSemimuonic_v2_ttbarCR_withJetVeto", "", "")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonic_v2_SR_noTrigger", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# For leading tight muon study: do not use NonLeadingMuons:
# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "SRDimuons", "LooseMuonsVertexSegmentMatch")

# samples = dasSamples2018.keys()
# samples = dasData2017.keys()
samples = dasData2016preVFP.keys()

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
    # "DSAEff": (False, False),
    "jec": (False, True),
    "L1PreFiringWeight": (True, True),
}

# this has to be here, otherwise the script will not work:
sample_path = ""
output_username = os.environ["USER"]
input_directory = f"{base_path.format(input_username)}/{sample_path}/{skim[0]}/"
output_hists_dir = f"{base_path.format(output_username)}/{sample_path}/{skim[0]}/histograms"

if "dimuonEff" in applyScaleFactors:
  if applyScaleFactors["dimuonEff"][0] or applyScaleFactors["dimuonEff"][1]:
    output_hists_dir += "_dimuonEffSFs"

if skim[1] != "":
  output_hists_dir += f"_{skim[1]}"

output_hists_dir += "/"
# output_hists_dir += "_ABCD/"
# output_hists_dir += "_nminus1/"
# output_hists_dir += "_genInfo/"
# output_hists_dir += "_withLeadingTightMuon_genInfo/"
# output_hists_dir += "_revertedMatching/"
