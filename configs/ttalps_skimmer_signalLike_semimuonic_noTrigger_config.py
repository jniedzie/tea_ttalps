from ttalps_extra_collections import get_extra_event_collections
from golden_json_config import goldenJsons
from ttalps_met_filters import get_met_filters
from ttalps_skimmer_files_config import year

goldenJson = goldenJsons[year]
extraEventCollections = get_extra_event_collections(year)

nEvents = -1

applyLooseSkimming = True
applyTTbarLikeSkimming = False
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)


eventCuts = {
    "MET_pt": (30, 9999999),
    "nTightMuons": (1, 9999999),
    "nLoosePATMuons": (1, 9999999),
    "nLooseMuons": (3, 9999999),
    "nLooseElectrons": (0, 0),
    "nGoodJets": (4, 9999999),
    "nGoodMediumBtaggedJets": (1, 9999999),
}

requiredFlags = get_met_filters(year)

branchesToKeep = ["*"]
branchesToRemove = []
specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}

redirector = "xrootd-cms.infn.it"
