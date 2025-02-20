from ttalps_extra_collections import *

year = "2018"
extraEventCollections = get_extra_event_collections(year)

nEvents = -1
printEveryNevents = 10000

applyLooseSkimming = False
applyTTbarLikeSkimming = True
applyTTZLikeSkimming = False
applySignalLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

eventCuts = {
    "MET_pt": (50, 9999999),
    # "nTightMuons": (1, 1), # This is already handled in PassesSingleLeptonCuts
    "nLooseElectrons": (0, 0),
    # "nGoodTightBtaggedJets": (2, 9999999),
    "nGoodMediumBtaggedJets": (1, 9999999),
}

branchesToKeep = ["*"]
branchesToRemove = []

specialBranchSizes = {
  "Proton_multiRP": "nProton_multiRP",
  "Proton_singleRP": "nProton_singleRP",
}
