from ttalps_extra_collections import get_extra_event_collections
from ttalps_skimmer_files_config import year

extraEventCollections = get_extra_event_collections(year)

nEvents = -1

applyLooseSkimming = False
applyTTZLikeSkimming = True

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)
metBranchName = "MET"
rhoBranchName = "fixedGridRhoFastjetAll"  # for jec unc.
if "2022" in year or "2023" in year or "2024" in year or "2025" in year:
  metBranchName = "PuppiMET"
  rhoBranchName = "Rho_fixedGridRhoFastjetAll"  # for jec unc. in 2022 and 2023

eventCuts = {
    "nano_MET_pt": (50, 9999999),
    "nTightMuons": (1, 9999999),
    "nLoosePATMuons": (3, 9999999),
    "nLooseElectrons": (0, 0),
    "nGoodBtaggedJets": (2, 9999999),
}

branchesToKeep = ["*"]
branchesToRemove = []
specialBranchSizes = {}
