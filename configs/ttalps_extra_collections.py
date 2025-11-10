commonExtraEventCollections = {

    # We use this mainly to find tops
    "TightMuons": {
        "inputCollections": ("Muon",),
        "pt": (30., 9999999.),
        "eta": (-2.4, 2.4),
        "pfRelIso04_all": (0., 0.15),
        "tightId": True,
    },

    # For loose skim and to build PAT+DSA collection
    "LoosePATMuons": {
        "inputCollections": ("Muon",),
        "pt": (3., 9999999.),
        "eta": (-2.5, 2.5),
        "looseId": True,
    },

    "LooseDisplacedPATMuons": {
        "inputCollections": ("LoosePATMuons",),
        "dxyPVTraj": (0.02, 9999999.)
    },

    # Slightly displaced Loose PAT muoons, dxy based on displaced dimuon search
    "LooseDSAMuons": {
        "inputCollections": ("DSAMuon",),
        "displacedID": (1, 9999999.),
        "pt": (3., 9999999.),
        "eta": (-2.5, 2.5),
    },

    "LooseMuons": {
        "inputCollections": ("LoosePATMuons", "LooseDSAMuons",),
    },

    # To get IsoMu24 trigger object
    "MuonTrigObj": {
        "inputCollections": ("TrigObj",),
        "pt": (24., 9999999.),
        "id": 13,
    },

    # Used for the loose skim
    "GoodJets": {
        "inputCollections": ("Jet", ),
        "pt": (30., 9999999.),
        "eta": (-2.4, 2.4),
        # bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto*
        "jetId": 6,
    },

    # To consider in CRs and SR
    "GoodTightBtaggedJets": {
        "inputCollections": ("GoodJets", ),
        "btagDeepFlavB": (None, None),  # will be set per year in get_extra_event_collections
    },

    # Used in all skims
    "GoodMediumBtaggedJets": {
        "inputCollections": ("GoodJets", ),
        "btagDeepFlavB": (None, None),  # will be set per year in get_extra_event_collections
    },
}

run2extraEventCollections = {
    # Used in CRs and SR to reject t->e+jets
    "LooseElectrons": {
        "inputCollections": ("Electron",),
        "pt": (15., 9999999.),
        "eta": (-2.5, 2.5),
        "mvaFall17V2Iso_WPL": True,
    },
}

run3extraEventCollections = {
    # Used in CRs and SR to reject t->e+jets
    "LooseElectrons": {
        "inputCollections": ("Electron",),
        "pt": (15., 9999999.),
        "eta": (-2.5, 2.5),
        "mvaIso_WP90": True,  # TODO: check if this is the correct WP
    },
}

# medium WPs based on https://btv-wiki.docs.cern.ch/ScaleFactors
b_tag_medium_WPs = {
    "2016preVFP": 0.2598,
    "2016postVFP": 0.2489,
    "2017": 0.3040,
    "2018": 0.2783,
    "2022preEE": 0.3086,
    "2022postEE": 0.3196,
    "2023preBPix": 0.2431,
    "2023postBPix": 0.2435,
}

b_tag_tight_WPs = {
    "2016preVFP": 0.6502,
    "2016postVFP": 0.6377,
    "2017": 0.7476,
    "2018": 0.7100,
    "2022preEE": 0.7183,
    "2022postEE": 0.7300,
    "2023preBPix": 0.6553,
    "2023postBPix": 0.6563,
}


def get_extra_event_collections(year):
  collections = None

  if year == "2016preVFP" or year == "2016postVFP" or year == "2017" or year == "2018":
    collections = {**commonExtraEventCollections, **run2extraEventCollections}
  elif year == "2022preEE" or year == "2022postEE" or year == "2023preBPix" or year == "2023postBPix":
    collections = {**commonExtraEventCollections, **run3extraEventCollections}
  else:
    raise ValueError(f"Year {year} not supported.")

  collections["GoodMediumBtaggedJets"]["btagDeepFlavB"] = (b_tag_medium_WPs[year], 9999999.)
  collections["GoodTightBtaggedJets"]["btagDeepFlavB"] = (b_tag_tight_WPs[year], 9999999.)

  return collections
