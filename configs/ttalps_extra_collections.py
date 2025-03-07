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
  
  # To build PAT+DSA collection
  "LooseDSAMuons": {
    "inputCollections": ("DSAMuon",),
    "displacedID": (1, 9999999.),
    "pt": (3., 9999999.),
    "eta": (-2.5, 2.5),
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
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
    "btagDeepFlavB": (0.7100, 9999999.),
    # bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto*
    "jetId": 6,
  },
  
  # Used in all skims
  "GoodMediumBtaggedJets": {
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
    "btagDeepFlavB": (0.2783, 9999999.),
    # bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto*
    "jetId": 6,
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
    "mvaIso_WP90": True,  #  TODO: check if this is the correct WP
  },
}

def get_extra_event_collections(year):
  if year == "2016" or year == "2017" or year == "2018":
    return {**commonExtraEventCollections, **run2extraEventCollections}
  elif year == "2022" or year == "2023":
    return {**commonExtraEventCollections, **run3extraEventCollections}
  else:
    raise ValueError(f"Year {year} not supported.")
