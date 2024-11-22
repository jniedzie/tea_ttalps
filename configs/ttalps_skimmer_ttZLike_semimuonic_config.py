from ttalps_extra_collections import extraEventCollections

nEvents = -1
printEveryNevents = 10000

applyLooseSkimming = False
applyTTbarLikeSkimming = False
applyTTZLikeSkimming = True
applySignalLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeName = "Events"

eventSelections = {
    "MET_pt": (50, 9999999),
    "nTightMuons": (1, 9999999),
    "nLooseIsoPATMuons": (3, 9999999),
    "nLooseElectrons": (0, 0),
    "nGoodBtaggedJets": (2, 9999999),
}

branchesToKeep = ["*"]
branchesToRemove = []
specialBranchSizes = {}
