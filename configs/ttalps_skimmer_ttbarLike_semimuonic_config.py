from ttalps_extra_collections import get_extra_event_collections
from scale_factors_config import get_scale_factors
from ttalps_skimmer_files_config import year

extraEventCollections = get_extra_event_collections(year)
scaleFactors = get_scale_factors(year)

nEvents = -1

applyLooseSkimming = False
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

muonMatchingParams = {"Segment": 2.0/3.0}

eventCuts = {
    "MET_pt": (50, 9999999),
    "nTightMuons": (1, 1),  # This is against TOP recommendation, but we do it to keep it the same as SR
    "nLoosePATMuons": (1, 1),
    # "nLooseDSAMuons": (0, 0),
    "nLooseDSAMuonsSegmentMatch": (0, 0),
    "nLooseElectrons": (0, 0),
}

specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}
