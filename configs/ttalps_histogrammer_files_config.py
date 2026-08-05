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
samples = dasBackgrounds2018.keys()

# Loose semimuonic skim
# skim = ("skimmed_looseSemimuonic_v3_merged", "", "")
# skim = ("skimmed_looseSemimuonic_v2", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# SR, J/Psi CR skim
skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuonsHitsInFrontOfVertex", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuonsDPhiBetweenMuonpTAndLxy", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuonsMaxDxyDz", "LooseNonLeadingMuonsVertexSegmentMatch")

# skim = ("skimmed_looseSemimuonic_v3_SR_noBTag", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR_noBTag_merged", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SSDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")
# skim = ("skimmed_looseSemimuonic_v3_SR", "Chi2Dimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

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
# skim = ("skimmed_looseSemimuonic_v2_SR_noTrigger_merged", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch")

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
    "jec": (True, True),
    "jer": (True, True),
    "metUnclEnergy": (False, True),
    "metXYcorrection": (True, False),
    "L1PreFiringWeight": (True, True),
}

# We only need to update the JEC for Run 3 Puppi Jets
if year == "2016preVFP" or year == "2016postVFP" or year == "2017" or year == "2018":
  _, variation = applyScaleFactors["jec"]
  applyScaleFactors["jec"] = (False, variation)

# We don't need the SF variations for uncertainties in CRs
if "SRDimuons" not in skim[1]:
  for name in applyScaleFactors: 
    nominal, _ = applyScaleFactors[name]
    applyScaleFactors[name] = (nominal, False)

hist_path = "histograms"

if skim[1] != "":
  hist_path += f"_{skim[1]}"

if "ttbarCR" not in skim[0]:
  if applyScaleFactors["dimuonEff_Pat"][0] is False and \
    applyScaleFactors["dimuonEff_PatDSA"][0] is False and \
    applyScaleFactors["dimuonEff_DSA"][0] is False:
    hist_path += "_noDimuonEffSFs"

hist_path += "_ABCD_ANv10_regionABCD"

# this has to be here, otherwise the script will not work:
sample_path = ""
output_username = os.environ["USER"]
input_directory = f"/data/dust/group/cms/ttALPs-desy/{sample_path}/{skim[0]}/"

output_hists_dir = f"{base_path.format(output_username)}/{sample_path}/{skim[0]}/{hist_path}/"
