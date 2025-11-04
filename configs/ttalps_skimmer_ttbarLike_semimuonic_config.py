from ttalps_extra_collections import get_extra_event_collections

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
extraEventCollections = get_extra_event_collections(year)

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
    "applyHEMveto": (False, 0.6294),

    # Only the first argument matters
    "applyJetVetoMaps": (True, None),
}

specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}
