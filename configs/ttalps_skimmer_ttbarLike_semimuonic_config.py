from ttalps_extra_collections import get_extra_event_collections
from scale_factors_config import get_scale_factors

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
extraEventCollections = get_extra_event_collections(year)
scaleFactors = get_scale_factors(year)

nEvents = -1

applyLooseSkimming = False
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

eventCuts = {
    "MET_pt": (50, 9999999),
    "nTightMuons": (1, 1),  # This is against TOP recommendation, but we do it to keep it the same as SR
    "nLooseMuons": (1, 1),
    "nLooseElectrons": (0, 0),

    # The first value is whether to apply the cut, the second is the fraction of events in data with run>=319077.
    # To measure the second number, you can use the `utils/count_hem_events.py` script.
    "nano_applyHEMveto": (False, 0.6294),

    # First argument: should the veto be applied? Second argument: should histograms be saved?
    "nano_applyJetVetoMaps": (True, False),
}

specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}
