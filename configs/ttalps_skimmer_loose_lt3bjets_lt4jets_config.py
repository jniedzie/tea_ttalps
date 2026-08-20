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
metBranchName = "MET"
rhoBranchName = "fixedGridRhoFastjetAll"  # for jec unc.
if "2022" in year or "2023" in year or "2024" in year or "2025" in year:
  metBranchName = "PuppiMET"
  rhoBranchName = "Rho_fixedGridRhoFastjetAll"  # for jec unc. in 2022 and 2023

triggerSelection = get_IsoMu_trigger(year)

eventCuts = {
    "nano_MET_pt": (30, 9999999),
    "nLoosePATMuons": (1, 9999999),
    "nGoodJets": (1, 3),
    "nGoodMediumBtaggedJets": (1, 2),
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
