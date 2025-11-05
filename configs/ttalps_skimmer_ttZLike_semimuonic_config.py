from ttalps_extra_collections import get_extra_event_collections
from ttalps_skimmer_files_config import year

extraEventCollections = get_extra_event_collections(year)

nEvents = -1

applyLooseSkimming = False
applyTTZLikeSkimming = True

weightsBranchName = "genWeight"
eventsTreeName = "Events"

eventCuts = {
    "MET_pt": (50, 9999999),
    "nTightMuons": (1, 9999999),
    "nLoosePATMuons": (3, 9999999),
    "nLooseElectrons": (0, 0),
    "nGoodBtaggedJets": (2, 9999999),
}

branchesToKeep = ["*"]
branchesToRemove = []
specialBranchSizes = {}
