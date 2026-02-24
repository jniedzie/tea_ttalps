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
samples = dasSignals2018.keys()

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v3_merged", "", "")
# skim = ("skimmed_looseSemimuonic_v2", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# SR, J/Psi CR skim
skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuonsHitsInFrontOfVertex", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuonsDPhiBetweenMuonpTAndLxy", "LooseNonLeadingMuonsVertexSegmentMatch")

# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SSDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# J/Psi CR PAT-DSA no association
# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuonsPatDSA", "LooseNonLeadingMuonsVertex")

# J/Psi CR DSA-DSA reverted association after PAT-PAT Dimuon selection
# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "LooseNonLeadingPATMuonsVertex")

# J/Psi CR DSA-DSA reverted association with DSA-DSA Dimuon selection
# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "RevertedSegmentMatchedDSAMuonsVertex")


# other CRs
# skim = ("skimmed_3muCR_merged", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_ttbarCR", "", "")
# skim = ("skimmed_looseSemimuonic_v2_ttbarLike1DSA", "", "")

# Loose semimuonic skim with Dimuon triggers for LLP trigger study
# skim = ("skimmed_looseSemimuonic_v2_SR_noTrigger", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# For leading tight muon study: do not use NonLeadingMuons:
# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "SRDimuons", "LooseMuonsVertexSegmentMatch")

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
    "dimuonEff_Pat": (True, True),
    "dimuonEff_PatDSA": (True, True),
    "dimuonEff_DSA": (True, True),
    "jec": (False, True),
    "L1PreFiringWeight": (True, True),
}

# We don't need the SF variations for uncertainties in CRs
if "SRDimuons" not in skim[1]:
  for name in applyScaleFactors: 
    sfs = applyScaleFactors[name]
    applyScaleFactors[name][1] = False

hist_path = "histograms"

if skim[1] != "":
  hist_path += f"_{skim[1]}"

if "dimuonEff" in applyScaleFactors and "ttbarCR" not in skim[0]:
  if applyScaleFactors["dimuonEff_Pat"][0] is False and \
    applyScaleFactors["dimuonEff_PatDSA"][0] is False and \
    applyScaleFactors["dimuonEff_DSA"][0] is False:
    hist_path += "_noDimuonEffSFs"

hist_path += "_ABCD_ANv2"
# hist_path += "_nminus1/"
# hist_path += "_noMatching_ABCD_ANv2"
# hist_path += "_revertedMatching_ABCD_ANv2"
# hist_path += "_fakes/"
# hist_path += "_noMatching/"

# this has to be here, otherwise the script will not work:
sample_path = ""
output_username = os.environ["USER"]
input_directory = f"/data/dust/group/cms/ttALPs-desy/{sample_path}/{skim[0]}/"

output_hists_dir = f"{base_path.format(output_username)}/{sample_path}/{skim[0]}/{hist_path}/"
