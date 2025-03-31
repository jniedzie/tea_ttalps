from ttalps_extra_collections import *
from golden_json_config import goldenJsons
from ttalps_met_filters import *

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
goldenJson = goldenJsons[year]
extraEventCollections = get_extra_event_collections(year)
met_filters = get_met_filters(year)

nEvents = -1
printEveryNevents = 10000

applyLooseSkimming = True
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

triggerSelection = (
    "HLT_IsoMu24",
)

eventCuts = {
    "MET_pt": (30, 9999999),
    "nLoosePATMuons": (1, 9999999),
    "nGoodJets": (4, 9999999),
    "nGoodMediumBtaggedJets": (1, 9999999),
}

requiredFlags = met_filters

branchesToKeep = ["*"]
branchesToRemove = []
specialBranchSizes = {
  "Proton_multiRP": "nProton_multiRP",
  "Proton_singleRP": "nProton_singleRP",
}

redirector = "xrootd-cms.infn.it"
