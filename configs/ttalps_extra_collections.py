commonExtraEventCollections = {
  "TightMuons": {
    "inputCollections": ("Muon",),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
    "pfRelIso04_all": (0., 0.15),
    "tightId": True,
  },
  "LoosePATMuons": {
    "inputCollections": ("Muon",),
    "pt": (3., 9999999.),
    "eta": (-2.5, 2.5),
    "looseId": True,
  },
  "LooseDSAMuons": {
    "inputCollections": ("DSAMuon",),
    "displacedID": (1, 9999999.),
    "pt": (3., 9999999.),
    "eta": (-2.5, 2.5),
  },
  
  "GoodJets": {
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
    # bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto*
    "jetId": 6,
  },
  "GoodForwardJetsPlus": {
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (2.4, 4.7),
    # bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto*
    "jetId": 6,
  },
  "GoodForwardJetsMinus": {
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (-4.7, -2.4),
    # bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto*
    "jetId": 6,
  },
  "GoodTightBtaggedJets": {
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
    "btagDeepFlavB": (0.7100, 9999999.),
    # bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto*
    "jetId": 6,
  },
  "GoodMediumBtaggedJets": {
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
    "btagDeepFlavB": (0.2783, 9999999.),
    # bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto*
    "jetId": 6,
  },
  
  "GoodNonTightBtaggedJets": {
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
    "btagDeepFlavB": (0.0, 0.7100),
    # bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto*
    "jetId": 6,
  },
  
  "GoodCentralNonBtaggedJets": {
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
    "btagDeepFlavB": (0.0, 0.2783),
    "jetId": 6,
  },
}

run2extraEventCollections = {
  "LooseElectrons": {
    "inputCollections": ("Electron",),
    "pt": (15., 9999999.),
    "eta": (-2.5, 2.5),
    "mvaFall17V2Iso_WPL": True,
  },
}

run3extraEventCollections = {
  "LooseElectrons": {
    "inputCollections": ("Electron",),
    "pt": (15., 9999999.),
    "eta": (-2.5, 2.5),
    "mvaIso_WP80": True, 
  },
}

def get_extra_event_collections(year):
  if year == "2016" or year == "2017" or year == "2018":
    return {**commonExtraEventCollections, **run2extraEventCollections}
  elif year == "2022" or year == "2023":
    return {**commonExtraEventCollections, **run3extraEventCollections}
  else:
    raise ValueError(f"Year {year} not supported.")
