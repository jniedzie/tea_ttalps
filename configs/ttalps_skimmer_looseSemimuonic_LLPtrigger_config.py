from ttalps_extra_collections import *
from golden_json_config import goldenJsons

year = "2018"
goldenJson = goldenJsons[year]
extraEventCollections = get_extra_event_collections(year)

nEvents = -1
printEveryNevents = 10000

applyLooseSkimming = True
applyTTbarLikeSkimming = False
applyTTZLikeSkimming = False
applySignalLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

triggerSelection = (
    "HLT_DoubleL2Mu23NoVtx_2Cha",
    "HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed",
)

eventCuts = {
    "MET_pt": (30, 9999999),
    "nLoosePATMuons": (1, 9999999),
    "nGoodJets": (4, 9999999),
    "nGoodMediumBtaggedJets": (1, 9999999),
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
