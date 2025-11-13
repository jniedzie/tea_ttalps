from ttalps_extra_collections import get_extra_event_collections
from golden_json_config import goldenJsons
from ttalps_met_filters import get_met_filters
from ttalps_triggers import get_IsoMu_trigger
from scale_factors_config import get_scale_factors
from ttalps_skimmer_das_files_config import year

goldenJson = goldenJsons[year]
extraEventCollections = get_extra_event_collections(year)
scaleFactors = get_scale_factors(year)

nEvents = -1

applyLooseSkimming = True
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

triggerSelection = get_IsoMu_trigger(year)

eventCuts = {
    "MET_pt": (30, 9999999),
    "nLoosePATMuons": (1, 9999999),
    "nGoodJets": (4, 9999999),
    "nGoodMediumBtaggedJets": (1, 9999999),

    # The first value is whether to apply the cut, the second is the fraction of events in data with run>=319077.
    # To measure the second number, you can use the `utils/count_hem_events.py` script.
    "nano_applyHEMveto": (True, 0.6294),

    # Only the first argument matters
    "nano_applyJetVetoMaps": (True, False),
}

requiredFlags = get_met_filters(year)

branchesToKeep = ["*"]
branchesToRemove = []
specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}

redirector = "xrootd-cms.infn.it"
