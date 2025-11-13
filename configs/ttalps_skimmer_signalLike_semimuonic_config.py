from ttalps_extra_collections import get_extra_event_collections
from ttalps_object_cuts import *
from scale_factors_config import get_scale_factors
from ttalps_skimmer_files_config import year

extraEventCollections = get_extra_event_collections(year)
scaleFactors = get_scale_factors(year)

nEvents = -1

applyLooseSkimming = False
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

eventCuts = {
    "MET_pt": (50, 9999999),
    "nTightMuons": (1, 9999999),
    "nLooseMuons": (3, 9999999),
    "nLooseElectrons": (0, 0),
    # "nGoodTightBtaggedJets": (2, 9999999),  # TODO: consider tight WP and/or 2 b-tags
}

branchesToKeep = ["*"]
branchesToRemove = []

specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}
