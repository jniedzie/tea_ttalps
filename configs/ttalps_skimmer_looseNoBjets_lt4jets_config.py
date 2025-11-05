from ttalps_extra_collections import get_extra_event_collections
from golden_json_config import goldenJsons
from ttalps_triggers import get_IsoMu_trigger
from ttalps_skimmer_files_config import year

goldenJson = goldenJsons[year]
extraEventCollections = get_extra_event_collections(year)

nEvents = -1

applyLooseSkimming = True
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

triggerSelection = get_IsoMu_trigger(year)

eventCuts = {
    "MET_pt": (30, 9999999),
    "nLoosePATMuons": (1, 9999999),
    "nGoodJets": (0, 3),
    "nGoodMediumBtaggedJets": (0, 0),
}

requiredFlags = (
    "Flag_goodVertices",
    "Flag_globalSuperTightHalo2016Filter",
    "Flag_HBHENoiseFilter",
    "Flag_HBHENoiseIsoFilter",
    "Flag_EcalDeadCellTriggerPrimitiveFilter",
    "Flag_BadPFMuonFilter",
    "Flag_BadPFMuonDzFilter",
    "Flag_hfNoisyHitsFilter",
    "Flag_eeBadScFilter",
    "Flag_ecalBadCalibFilter",
)

branchesToKeep = ["*"]
branchesToRemove = []
specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}

redirector = "xrootd-cms.infn.it"
