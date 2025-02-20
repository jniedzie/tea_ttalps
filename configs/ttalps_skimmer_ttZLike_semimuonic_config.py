from ttalps_extra_collections import *

year = "2018"
extraEventCollections = get_extra_event_collections(year)

nEvents = -1
printEveryNevents = 10000

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
