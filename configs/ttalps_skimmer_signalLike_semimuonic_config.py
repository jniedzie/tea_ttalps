from ttalps_extra_collections import *
from ttalps_object_cuts import *

year = "2018"
extraEventCollections = get_extra_event_collections(year)

nEvents = -1
printEveryNevents = 1000

applyLooseSkimming = False
applyTTbarLikeSkimming = False
applyTTZLikeSkimming = False
applySignalLikeSkimming = True

weightsBranchName = ""
# weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

# For the signal like skimming all given muonMatchingParams are applied together
# If only one matching method should be used ONLY include that one method
# We might want to update the logic of this in the future
# Matching methods implemented are:
# "Segment" : max matching ratio (eg. 2.0/3.0)
# "DR" : max Delta R (eg. 0.1)
# "OuterDR" : max Delta R (eg. 0.1)
# "ProxDR" : max Delta R (eg. 0.1)
muonMatchingParams = {
    "Segment" : 2.0/3.0,
    # "DR" : 0.1,
    # "OuterDR" : 0.1,
    # "ProxDR" : 0.1,
}

eventCuts = {
    "MET_pt": (50, 9999999),
    "nTightMuons": (1, 9999999),
    "nLooseElectrons": (0, 0),
    # "nGoodBtaggedJets": (2, 9999999),
    # "nGoodMediumBtaggedJets": (1, 9999999),
}

branchesToKeep = ["*"]
branchesToRemove = []

specialBranchSizes = {
  "Proton_multiRP": "nProton_multiRP",
  "Proton_singleRP": "nProton_singleRP",
}
