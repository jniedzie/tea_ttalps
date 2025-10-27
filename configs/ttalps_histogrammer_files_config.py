from ttalps_samples_list import dasSamples2018, dasData2018, dasBackgrounds2018, dasSignalsPrivate2018, dasData2018_standard, dasSignals2018
from ttalps_samples_list import dasBackgrounds2018Devel, dasData2018Devel
from ttalps_samples_list import dasBackgrounds2022preEE, dasSignals2022preEE, dasData2022preEE
from ttalps_samples_list import dasBackgrounds2022postEE, dasSignals2022postEE, dasData2022postEE
from ttalps_samples_list import dasBackgrounds2017, dasData2017, dasSignals2017
from ttalps_samples_list import dasBackgrounds2016PreVFP, dasData2016PreVFP, dasSignals2016PreVFP
from ttalps_samples_list import dasBackgrounds2016PostVFP, dasData2016PostVFP, dasSignals2016PostVFP
from ttalps_samples_list import dasBackgrounds2023preBPix, dasSignals2023preBPix, dasData2023preBPix
from ttalps_samples_list import dasBackgrounds2023postBPix, dasSignals2023postBPix, dasData2023postBPix
import os

max_files = -1

input_username = "lrygaard"
# input_username = "jalimena"
# input_username = "jniedzie"

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v2", "")
# skim = ("skimmed_looseSemimuonic_v2", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# SR, J/Psi CR skim without segment match ratio
# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "SRDimuonsNoChi2", "LooseNonLeadingMuonsVertexSegmentMatch")
skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "JPsiDimuonsNoChi2DCA", "LooseNonLeadingMuonsVertexSegmentMatch")

# other CRs
# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "", "")
# skim = ("skimmed_looseSemielectronic_v1_ttbarCR", "", "")
# skim = ("skimmed_looseNonTT_v1_VVCR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseNoBjets_lt4jets_v1_merged", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")  # QCD CR
# skim = ("skimmed_looseNoBjets_lt4jets_looseMuonPtGt5GeV_v1_merged", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")  # QCD CR
# skim = ("skimmed_looseNoBjets_lt4jets_v1_looseMuonPtGt8GeV", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")  # QCD CR
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# skim = ("skimmed_looseSemimuonic_v2_ttbarLike1DSA", "", "")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonic_v2_notrigger_SR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# Inverted MET skim
# skim = ("skimmed_looseInvertedMet_v1_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseNoMet_v1_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# samples = dasSamples2018.keys()
# samples = dasData2018.keys()
samples = dasBackgrounds2018.keys()
# samples = dasSignals2018.keys()
# samples = list(dasBackgrounds2018.keys()) + list(dasData2018_standard.keys())

base_path = "/data/dust/user/{}/ttalps_cms"

applyScaleFactors = {
  # name : (apply nominal, apply variation)
  "muon": (True, True),
  "dsamuon": (True, True),
  "muonTrigger": (True, True),
  "pileup": (True, True),
  "bTagging": (True, True),
  "PUjetID": (True, True),
  "dimuonEff": (False, False),
  # "DSAEff": (False, False),
  "jec" : (False, True), 
}

# this has to be here, otherwise the script will not work:
sample_path = ""
output_username = os.environ["USER"]
input_directory = f"{base_path.format(input_username)}/{sample_path}/{skim[0]}/"
output_hists_dir = f"{base_path.format(output_username)}/{sample_path}/{skim[0]}/histograms"

for name, apply in applyScaleFactors.items():
  if not apply[0] and not apply[1]:
    continue

  output_hists_dir += f"_{name}SFs"

if skim[1] != "":
  output_hists_dir += f"_{skim[1]}"
if skim[2] != "":
  output_hists_dir += f"_{skim[2]}"
output_hists_dir += "/"
# output_hists_dir += "_genInfo_nminus1/"
# output_hists_dir += "_revertedMatching/"
