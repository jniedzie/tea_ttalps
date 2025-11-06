from ttalps_extra_collections import get_extra_event_collections
from golden_json_config import goldenJsons
from ttalps_met_filters import get_met_filters
from ttalps_triggers import get_Ele_Tight_trigger
from ttalps_skimmer_files_config import year

goldenJson = goldenJsons[year]
extraEventCollections = get_extra_event_collections(year)

nEvents = -1

applyLooseSkimming = True
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

triggerSelection = get_Ele_Tight_trigger(year)

eventCuts = {
    "MET_pt": (30, 9999999),
    "nLooseElectrons": (1, 9999999),
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
