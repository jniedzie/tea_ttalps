extraEventCollections = {
  "TightMuons": {
    "inputCollections": ("Muon",),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
    "pfRelIso04_all": (0., 0.15),
    "tightId": True,
  },
  "LooseIsoPATMuons": {
    "inputCollections": ("Muon",),
    "pt": (3., 9999999.),
    "eta": (-2.5, 2.5),
    "pfRelIso04_all": (0., 0.25),
    "looseId": True,
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
  
  "LooseElectrons": {
    "inputCollections": ("Electron",),
    "pt": (15., 9999999.),
    "eta": (-2.5, 2.5),
    "mvaFall17V2Iso_WPL": True,
  },
  
  "GoodJets": {
    "inputCollections": ("Jet", ),
    "pt": (30., 9999999.),
    "eta": (-2.4, 2.4),
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
}
