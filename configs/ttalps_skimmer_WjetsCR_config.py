from ttalps_extra_collections import get_extra_event_collections
from ttalps_object_cuts import *
from ttalps_skimmer_files_config import year

extraEventCollections = get_extra_event_collections(year)

nEvents = -1

applyLooseSkimming = False
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
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
    "Segment": 2.0/3.0,
    # "DR" : 0.1,
    # "OuterDR" : 0.1,
    # "ProxDR" : 0.1,
}

eventCuts = {
    "MET_pt": (50, 9999999),
    "nTightMuons": (1, 9999999),
    "nLooseMuonsSegmentMatch": (3, 9999999),
    "nLooseElectrons": (0, 0),
    "nGoodJets": (2, 2),
    "nGoodMediumBtaggedJets": (1, 1),
    # "nGoodTightBtaggedJets": (2, 9999999),  # TODO: consider tight WP and/or 2 b-tags
}

branchesToKeep = ["*"]
branchesToRemove = []

specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}
