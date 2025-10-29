from ttalps_extra_collections import get_extra_event_collections

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
extraEventCollections = get_extra_event_collections(year)

nEvents = -1
printEveryNevents = 10000

applyLooseSkimming = False
applyTTZLikeSkimming = False

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

eventCuts = {
    "MET_pt": (50, 9999999),
    "nTightMuons": (1, 1),  # This is against TOP recommendation, but we do it to keep it the same as SR
    "nLooseDSAMuons": (0, 0),
    "nLoosePATMuons": (1, 1),
    "nLooseElectrons": (0, 0),

    # TODO: make it possible to have event-level flags instead of always ranges
    "applyHEMveto": (True, 0),  # only the first value matters, set it to True or False
}

specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}
