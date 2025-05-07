from itertools import product
from math import pi


class TTAlpsHistogrammerConfigHelper:
  def __init__(self, muonMatchingParams, muonVertexCollection, muonVertexCollectionInput):
    self.muonMatchingParams = muonMatchingParams

    self.looseMuonCollections = []
    self.tightMuonCollections = []

    for category, matching in product(("", "DSA", "PAT"), muonMatchingParams):
      self.tightMuonCollections.append(f"Tight{category}Muons{matching}Match")
      self.looseMuonCollections.append(f"Loose{category}Muons{matching}Match")

    self.bestMuonVertexCollections = []
    self.goodMuonVertexCollections = []
    self.fakeStudyBestMuonVertexCollections = []

    self.bestMuonVertexCollectionCuts = []

    if muonVertexCollection is not None:
      for category in ("", "_PatDSA", "_DSA", "_Pat"):
        self.bestMuonVertexCollections.append(f"{muonVertexCollection[0]}{category}")
        self.goodMuonVertexCollections.append(f"{muonVertexCollection[0].replace('Best', 'Good')}{category}")
      self.bestMuonVertexCollectionCuts = muonVertexCollection[1]

    self.looseMuonVertexCollections = []
    for category, matching in product(("", "_PatDSA", "_DSA", "_Pat"), muonMatchingParams):
      self.looseMuonVertexCollections.append(f"LooseMuonsVertex{matching}Match{category}")
      self.looseMuonVertexCollections.append(f"{muonVertexCollectionInput}{category}")

    self.ABCD_variables = {

        "absCollinearityAngle": (100, 0, 2),
        "3Dangle": (100, 0, pi),

        "logLxy": (100, -2, 3),
        "logLxySignificance": (100, -2, 2),
        "logAbsCollinearityAngle": (100, -5, 1),
        "log3Dangle": (100, -3, 1),

        "outerDR": (100, 0, 5),
        "maxHitsInFrontOfVert": (10, 0, 10),
        "absPtLxyDPhi1": (100, 0, pi),
        "absPtLxyDPhi2": (100, 0, pi),

        "logAbsPtLxyDPhi1": (100, -5, 1),
        "logAbsPtLxyDPhi2": (100, -5, 1),

        "invMass": (100, 0, 100),
        "logInvMass": (100, -1, 2),

        "pt": (100, 0, 200),
        "leadingPt": (100, 0, 200),

        "logPt": (100, -1, 3),
        "logLeadingPt": (100, -1, 3),

        "eta": (100, -3, 3),
        "dEta": (100, 0, 3),
        "dPhi": (100, 0, 2*pi),
        "nSegments": (10, 0, 10),
        "logDisplacedTrackIso03Dimuon1": (100, -3, 0),
        "logDisplacedTrackIso04Dimuon1": (100, -3, 0),
        "logDisplacedTrackIso03Dimuon2": (100, -3, 0),
        "logDisplacedTrackIso04Dimuon2": (100, -3, 0),


        "logDxyPVTraj1": (100, -5, 1),
        "logDxyPVTraj2": (100, -5, 1),
        "logDxyPVTrajSig1": (100, -3, 1),
        "logDxyPVTrajSig2": (100, -3, 1),

        "deltaIso03": (100, 0, 10),
        "deltaIso04": (100, 0, 10),
        "logDeltaIso03": (100, -5, 5),
        "logDeltaIso04": (100, -5, 5),
        "deltaSquaredIso03": (100, 0, 10),
        "deltaSquaredIso04": (100, 0, 10),
        "logDeltaSquaredIso03": (100, -5, 5),
        "logDeltaSquaredIso04": (100, -5, 5),
    }

  def get_default_params(self):
    return (
        #  collection             variable               bins    xmin    xmax    dir
        ("Event", "MET_pt", 1000, 0, 1000, ""),
        ("Event", "PV_npvs", 300, 0, 300, ""),
        ("Event", "PV_npvsGood", 300, 0, 300, ""),
        ("Event", "PV_x", 2000, -100, 100, ""),
        ("Event", "PV_y", 2000, -100, 100, ""),
        ("Event", "PV_z", 2000, -100, 100, ""),
        ("Event", "PV_chi2", 2000, -100, 100, ""),

        ("Event", "nGoodJets", 20, 0, 20, ""),
        ("GoodJets", "pt", 1000, 0, 1000, ""),
        ("GoodJets", "leadingPt", 1000, 0, 1000, ""),
        ("GoodJets", "subleadingPt", 1000, 0, 1000, ""),
        ("GoodJets", "eta", 300, -3, 3, ""),
        ("GoodJets", "phi", 300, -3, 3, ""),
        ("GoodJets", "mass", 1000, 0, 1000, ""),

        ("Event", "nGoodMediumBtaggedJets", 20, 0, 20, ""),
        ("GoodMediumBtaggedJets", "pt", 1000, 0, 1000, ""),
        ("GoodMediumBtaggedJets", "leadingPt", 1000, 0, 1000, ""),
        ("GoodMediumBtaggedJets", "subleadingPt", 1000, 0, 1000, ""),
        ("GoodMediumBtaggedJets", "eta", 300, -3, 3, ""),
        ("GoodMediumBtaggedJets", "phi", 300, -3, 3, ""),
        ("GoodMediumBtaggedJets", "mass", 1000, 0, 1000, ""),
        ("GoodMediumBtaggedJets", "btagDeepFlavB", 1000, 0, 1, ""),

        ("Event", "nTightMuons", 50, 0, 50, ""),
        ("TightMuons", "pt", 2000, 0, 1000, ""),
        ("TightMuons", "leadingPt", 2000, 0, 1000, ""),
        ("TightMuons", "subleadingPt", 2000, 0, 1000, ""),
        ("TightMuons", "eta", 300, -3, 3, ""),
        ("TightMuons", "phi", 300, -3, 3, ""),
        
        ("Event", "nLooseElectrons", 50, 0, 50, ""),
        ("LooseElectrons", "pt", 2000, 0, 1000, ""),
        ("LooseElectrons", "leadingPt", 2000, 0, 1000, ""),
        ("LooseElectrons", "eta", 300, -3, 3, ""),
        ("LooseElectrons", "phi", 300, -3, 3, ""),
    )

  def get_basic_params(self):
    return (
        #  collection         variable                      bins   xmin   xmax    dir
        ("Event", "normCheck", 1, 0, 1, ""),
        ("Event", "isData",    2, 0, 2, ""),
    )

  def get_llp_params(self):
    params = []

    for collection in self.looseMuonCollections:
      self.__insert_MuonHistograms(params, collection)

    for collection in self.looseMuonVertexCollections + self.bestMuonVertexCollections:
      self.__insert_MuonVertexHistograms(params, collection)

    for collection in self.bestMuonVertexCollections + self.goodMuonVertexCollections:
      for cut in self.bestMuonVertexCollectionCuts:
        name = self.__insert_into_name(collection, "Nminus1")
        self.__insert_Nminus1Histograms(params, name)

    return tuple(params)

  def get_gen_vertex_params(self):
    params = []

    for collection in self.bestMuonVertexCollections + self.goodMuonVertexCollections:

      for cut in self.bestMuonVertexCollectionCuts:
        name = self.__insert_into_name(collection, "FromALPNminus1")
        self.__insert_Nminus1Histograms(params, name)

    for collection in self.looseMuonVertexCollections + self.bestMuonVertexCollections:

      names = (
          self.__insert_into_name(collection, "FromALP"),
          self.__insert_into_name(collection, "ResonancesNotFromALP"),
          self.__insert_into_name(collection, "NonresonancesNotFromALP"),
      )
      for name in names:
        self.__insert_MuonVertexHistograms(params, name)

    return tuple(params)

  def get_gen_matched_params(self):
    params = []

    for collection in self.looseMuonVertexCollections:
      names = (
          self.__insert_into_name(collection, "FromALP"),
          self.__insert_into_name(collection, "ResonancesNotFromALP"),
          self.__insert_into_name(collection, "NonresonancesNotFromALP"),
      )
      for name in names:
        self.__insert_MuonVertexHistograms(params, name)

    for collection in self.looseMuonCollections + self.tightMuonCollections:
      names = (
          self.__insert_into_name(collection, "FromALP"),
          self.__insert_into_name(collection, "FromW"),
      )
      for name in names:
        self.__insert_MuonHistograms(params, name)
        params += (
            ("Event", "n"+name, 50, 0, 50, ""),
            ("Event", "n"+name+"_hmu", 50, 0, 50, ""),
            (name, "hasLeadingMuon", 10, 0, 10, ""),
            (name, "hmu_hasLeadingMuon", 10, 0, 10, ""),
            (name, "index", 10, 0, 10, ""),
            (name, "pt", 4000, 0, 1000, ""),
            (name, "hmu_index", 10, 0, 10, ""),
            (name, "hmu_pt", 4000, 0, 1000, ""),
        )

    return tuple(params)

  def get_gen_params(self):
    params = []

    params += (
        ("Event", "nGenALP", 50, 0, 50, ""),
        ("GenALP", "pdgId", 200, -100, 100, ""),
        ("GenALP", "pt", 4000, 0, 1000, ""),
        ("GenALP", "mass", 10000, 0, 100, ""),
        ("GenALP", "eta", 300, -3, 3, ""),
        ("GenALP", "phi", 300, -3, 3, ""),
    )

    for name in ["GenDimuonFromALP", "GenDimuonResonancesNotFromALP", "GenDimuonsNonresonancesNotFromALP", "GenMuonFromW"]:
      self.__insert_GenDimuonHistograms(params, name)

    for matchingMethod in self.muonMatchingParams:
      for name in ["GenDimuonFromALP", "GenMuonFromW"]:
        params += (
            (name+"1", "LooseMuons"+matchingMethod+"MatchMinDR", 1000, 0, 10, ""),
            (name+"1", "LooseMuons"+matchingMethod+"MatchMinDPhi", 1000, 0, 10, ""),
            (name+"1", "LooseMuons"+matchingMethod+"MatchMinDEta", 1000, 0, 10, ""),
            (name+"2", "LooseMuons"+matchingMethod+"MatchMinDR", 1000, 0, 10, ""),
            (name+"2", "LooseMuons"+matchingMethod+"MatchMinDPhi", 1000, 0, 10, ""),
            (name+"2", "LooseMuons"+matchingMethod+"MatchMinDEta", 1000, 0, 10, ""),
            (name+"1", "LooseMuons"+matchingMethod+"MatchFinalMinDR", 1000, 0, 10, ""),
            (name+"1", "LooseMuons"+matchingMethod+"MatchFinalMinDPhi", 1000, 0, 10, ""),
            (name+"1", "LooseMuons"+matchingMethod+"MatchFinalMinDEta", 1000, 0, 10, ""),
            (name+"2", "LooseMuons"+matchingMethod+"MatchFinalMinDR", 1000, 0, 10, ""),
            (name+"2", "LooseMuons"+matchingMethod+"MatchFinalMinDPhi", 1000, 0, 10, ""),
            (name+"2", "LooseMuons"+matchingMethod+"MatchFinalMinDEta", 1000, 0, 10, ""),
        )

    return tuple(params)

  def get_trigger_params(self):
    params = []

    for name in ["NoExtra", "SingleMuon", "DoubleMuon", "SingleorDoubleMuon"]:
      params += (
          ("Event", "n"+name+"TriggerGenMuonFromALP", 50, 0, 50, ""),
          (name+"TriggerGenMuonFromALP", "pt1", 2000, 0, 1000, ""),
          (name+"TriggerGenMuonFromALP", "pt2", 2000, 0, 1000, ""),
          (name+"TriggerGenMuonFromALP", "leadingPt", 2000, 0, 1000, ""),
          (name+"TriggerGenMuonFromALP", "subleadingPt", 2000, 0, 1000, ""),
      )

    return tuple(params)

  def get_abcd_2Dparams(self):
    params = []

    for collection in self.bestMuonVertexCollections:

      for variable_1, (nBins_1, xMin_1, xMax_1) in self.ABCD_variables.items():
        for variable_2, (nBins_2, xMin_2, xMax_2) in self.ABCD_variables.items():
          if variable_1 == variable_2:
            continue

          name = self.__insert_into_name(collection, f"_{variable_2}_vs_{variable_1}")

          params.append((name, nBins_1, xMin_1, xMax_1, nBins_2, xMin_2, xMax_2, ""))

    return tuple(params)

  def get_abcd_mothers_2Dparams(self):
    params = []

    for collection in self.bestMuonVertexCollections:
      for blob in ["", "_lowBlob", "_rightBlob", "_centralBlob", "_lowLine", "_rightLine", "_mysteriousBlob"]:
        params.append((collection+"_motherPid1_vs_motherPid2"+blob, 2000, -1000, 1000, 2000, -1000, 1000, ""))

    return tuple(params)

  def get_abcd_1Dparams(self):
    params = []

    for collection in self.bestMuonVertexCollections:
      params += (
          (collection, "deltaR_WW", 500, 0, 10, ""),
          (collection, "deltaR_Wtau", 500, 0, 10, ""),
          (collection, "deltaR_OS", 500, 0, 10, ""),
          (collection, "logDeltaR_WW", 100, -5, 5, ""),
          (collection, "logDeltaR_Wtau", 100, -5, 5, ""),
          (collection, "logDeltaR_OS", 100, -5, -5, ""),
      )

    return tuple(params)

  def get_fakes_params(self):
    params = []

    for collection in self.bestMuonVertexCollections:
      for type in ["_fakes", "_nonFakes"]:
        self.__insert_MuonVertexHistograms(params, collection + type)

    for collection in self.looseMuonCollections:
      for type in ["_fakes", "_nonFakes"]:
        self.__insert_MuonHistograms(params, collection + type)

    return tuple(params)

  def get_matching_params(self):
    params = []

    for name in ["MatchLoose", "MatchLooseDSA", "DRMatchLoose", "OuterDRMatchLoose"]:
      params += (
          ("Event", "nSegment"+name+"Muons", 50, 0, 50, ""),
          ("Segment"+name+"Muons", "genMinDR", 1000, 0, 10, ""),
          ("Segment"+name+"Muons", "genMinDRidx", 100, 0, 100, ""),
          ("Segment"+name+"Muons", "nSegments", 50, 0, 50, ""),
          ("Segment"+name+"Muons", "matchingRatio", 600, 0, 2, ""),
          ("Segment"+name+"Muons", "maxMatches", 50, 0, 50, ""),
          ("Segment"+name+"Muons", "muonMatchIdx", 50, 0, 50, ""),
          ("Segment"+name+"Muons", "pt", 2000, 0, 1000, ""),
          ("Segment"+name+"Muons", "eta", 300, -3, 3, ""),
          ("Segment"+name+"Muons", "phi", 300, -3, 3, ""),
          ("Segment"+name+"Muons", "dxyPVTraj", 20000, -2000, 2000, ""),
          ("Segment"+name+"Muons", "dxyPVTrajSig", 10000, 0, 2000, ""),
          ("Segment"+name+"Muons", "ip3DPVSigned", 20000, -2000, 2000, ""),
          ("Segment"+name+"Muons", "ip3DPVSignedSig", 10000, 0, 2000, ""),
      )

    params += (
        ("LooseDSAMuons", "nSegments", 50, 0, 50, ""),
        ("LooseDSAMuons", "muonMatch1", 50, 0, 50, ""),
        ("LooseDSAMuons", "muonMatch2", 50, 0, 50, ""),
        ("LooseDSAMuons", "matchRatio1", 600, 0, 2, ""),
        ("LooseDSAMuons", "matchRatio2", 600, 0, 2, ""),
        ("LooseDSAMuons", "PATOuterDR", 1000, 0, 10, ""),
        ("LooseDSAMuons", "PATProxDR", 1000, 0, 10, ""),
        ("LooseDSAMuons", "PATDR", 1000, 0, 10, ""),
    )

    return tuple(params)

  def get_2D_matching_params(self):
    params = (
        ("LooseDSAMuons_muonMatch1_nSegments",               50, 0, 50, 50, 0, 50, ""),
        ("LooseDSAMuons_muonMatch2_nSegments",               50, 0, 50, 50, 0, 50, ""),

        ("SegmentMatchLooseMuons_LooseDSAMuons_genMinDR",    1000, 0, 10, 1000, 0, 10, ""),
        ("SegmentMatchLooseMuons_LooseDSAMuons_genMinDRidx", 100, 0, 100, 100, 0, 100, ""),
        ("SegmentMatchLooseMuons_LooseDSAMuons_eta",         60, -3, 3, 60, -3, 3, ""),
        ("SegmentMatchLooseMuons_LooseDSAMuons_phi",         60, -3, 3, 60, -3, 3, ""),
        ("SegmentMatchLooseMuons_LooseDSAMuons_outerEta",    60, -3, 3, 60, -3, 3, ""),
        ("SegmentMatchLooseMuons_LooseDSAMuons_outerPhi",    60, -3, 3, 60, -3, 3, ""),

        ("SegmentMatchLooseMuons_eta_outerEta",              60, -3, 3, 60, -3, 3, ""),
        ("SegmentMatchLooseMuons_phi_outerPhi",              60, -3, 3, 60, -3, 3, ""),
        ("SegmentMatchLooseDSAMuons_eta_outerEta",           60, -3, 3, 60, -3, 3, ""),
        ("SegmentMatchLooseDSAMuons_phi_outerPhi",           60, -3, 3, 60, -3, 3, ""),
    )

    return tuple(params)

  def get_SF_variation_variables(self):
    collection = "BestPFIsoDimuonVertex"

    variables = (
        "logLxySignificance_vs_log3Dangle",
        "dPhi_vs_logDxyPVTraj1",
        "logLxy_vs_log3Dangle",
        "logAbsCollinearityAngle_vs_logPt",
        "logPt_vs_logDxyPVTraj1",
        "logLxy_vs_log3Dangle",
        "logLeadingPt_vs_dPhi"
    )

    SF_variables = []

    for variable in variables:
      for category in ("", "_PatDSA", "_DSA", "_Pat"):
        name = self.__insert_into_name(collection, f"_{variable}{category}")
        SF_variables.append(name)

    return SF_variables

  def get_muon_trigger_objects_params(self):
    params = []
    for collection in ("MuonTrigObj", "MuonTriggerObjects", "LeadingMuonTriggerObject"):
      params += (
          ("Event", "n"+collection, 50, 0, 50, ""),
          (collection, "pt", 2000, 0, 1000, ""),
          (collection, "eta", 300, -3, 3, ""),
          (collection, "phi", 300, -3, 3, ""),
          (collection, "filterBits", 5000, 0, 5000, ""),
          (collection, "hasFilterBits2", 10, 0, 10, ""),
          (collection, "l1iso", 800, 0, 20, ""),
          (collection, "l1pt", 2000, 0, 1000, ""),
          (collection, "l1pt_2", 2000, 0, 1000, ""),
          (collection, "minDRTightLooseMuon", 500, 0, 10, ""),
          (collection, "tightLooseMuonMatch0p3", 10, 0, 10, ""),
          (collection, "tightLooseMuonMatch0p1", 10, 0, 10, ""),
          (collection, "triggerMuonMatchDR", 500, 0, 10, ""),
      )
    return tuple(params)

  def __insert_into_name(self, collection, to_insert):
    if "_" in collection:
      return collection.rsplit("_", 1)[0] + to_insert + "_" + collection.rsplit("_", 1)[1]

    return collection + to_insert

  def __insert_MuonHistograms(self, params, name):
    params += (
        ("Event", "n"+name, 50, 0, 50, ""),
        (name, "pt", 2000, 0, 1000, ""),
        (name, "eta", 300, -3, 3, ""),
        (name, "phi", 300, -3, 3, ""),
        (name, "dxy", 20000, -2000, 2000, ""),
        (name, "pfRelIso04all", 800, 0, 20, ""),
        (name, "isPAT", 10, 0, 10, ""),
        (name, "IsTight", 10, 0, 10, ""),
        (name, "ptErr", 2000, 0, 1000, ""),
        (name, "etaErr", 300, -3, 3, ""),
        (name, "phiErr", 300, -3, 3, ""),
        (name, "dz", 20000, -2000, 2000, ""),
        (name, "absDzFromLeadingTight", 10000, 0, 100, ""),
        (name, "logAbsDzFromLeadingTight", 10000, -5, 3, ""),
        (name, "vx", 200, -100, 100, ""),
        (name, "vy", 200, -100, 100, ""),
        (name, "vz", 200, -100, 100, ""),
        (name, "chi2", 1000, 0, 100, ""),
        (name, "ndof", 100, 0, 100, ""),
        (name, "trkNumPlanes", 20, 0, 20, ""),
        (name, "trkNumHits", 50, 0, 50, ""),
        (name, "trkNumDTHits", 50, 0, 50, ""),
        (name, "trkNumCSCHits", 50, 0, 50, ""),
        (name, "normChi2", 50000, 0, 50, ""),
        (name, "outerEta", 300, -3, 3, ""),
        (name, "outerPhi", 300, -3, 3, ""),
        (name, "dzPV", 20000, -2000, 2000, ""),
        (name, "dzPVErr", 20000, -2000, 2000, ""),
        (name, "dxyPVTraj", 20000, -2000, 2000, ""),
        (name, "dxyPVTrajErr", 20000, -2000, 2000, ""),
        (name, "dxyPVSigned", 20000, -2000, 2000, ""),
        (name, "dxyPVSignedErr", 20000, -2000, 2000, ""),
        (name, "ip3DPVSigned", 20000, -2000, 2000, ""),
        (name, "ip3DPVSignedErr", 20000, -2000, 2000, ""),
        (name, "dxyBS", 20000, -2000, 2000, ""),
        (name, "dxyBSErr", 20000, -2000, 2000, ""),
        (name, "dzBS", 20000, -2000, 2000, ""),
        (name, "dzBSErr", 20000, -2000, 2000, ""),
        (name, "dxyBSTraj", 20000, -2000, 2000, ""),
        (name, "dxyBSTrajErr", 20000, -2000, 2000, ""),
        (name, "dxyBSSigned", 20000, -2000, 2000, ""),
        (name, "dxyBSSignedErr", 20000, -2000, 2000, ""),
        (name, "ip3DBSSigned", 20000, -2000, 2000, ""),
        (name, "ip3DBSSignedErr", 20000, -2000, 2000, ""),
        (name, "displacedID", 10, 0, 10, ""),
        (name, "nSegments", 50, 0, 50, ""),
        (name, "nDTSegments", 50, 0, 50, ""),
        (name, "nCSCSegments", 50, 0, 50, ""),
    )

  # FillMuonVertexHistograms function
  def __insert_MuonVertexHistograms(self, params, name):
    params += (
        ("Event", "n"+name, 50, 0, 50, ""),
        (name, "normChi2", 50000, 0, 50, ""),
        (name, "Lxy", 10000, 0, 1000, ""),
        (name, "logLxy", 2000, -10, 10, ""),
        (name, "LxySigma", 10000, 0, 100, ""),
        (name, "LxySignificance", 1000, 0, 1000, ""),
        (name, "dR", 500, 0, 10, ""),
        (name, "proxDR", 500, 0, 10, ""),
        (name, "outerDR", 500, 0, 10, ""),
        (name, "dEta", 500, 0, 10, ""),
        (name, "dPhi", 500, 0, 10, ""),
        (name, "maxHitsInFrontOfVert", 100, 0, 100, ""),
        (name, "hitsInFrontOfVert1", 100, 0, 100, ""),
        (name, "hitsInFrontOfVert2", 100, 0, 100, ""),
        (name, "dca", 1000, 0, 20, ""),
        (name, "absCollinearityAngle", 500, 0, 5, ""),
        (name, "absPtLxyDPhi1", 500, 0, 5, ""),
        (name, "absPtLxyDPhi2", 500, 0, 5, ""),
        (name, "invMass", 20000, 0, 200, ""),
        (name, "logInvMass", 1000, -1, 2, ""),
        (name, "pt", 2000, 0, 1000, ""),
        (name, "eta", 500, -10, 10, ""),
        (name, "chargeProduct", 4, -2, 2, ""),
        (name, "leadingPt", 2000, 0, 1000, ""),
        (name, "subleadingPt", 2000, 0, 1000, ""),
        (name, "leadingEta", 500, -10, 10, ""),
        (name, "subleadingEta", 500, -10, 10, ""),
        (name, "dxyPVTraj1", 1000, 0, 1000, ""),
        (name, "dxyPVTraj2", 1000, 0, 1000, ""),
        (name, "dxyPVTrajSig1", 1000, 0, 1000, ""),
        (name, "dxyPVTrajSig2", 1000, 0, 1000, ""),
        (name, "displacedTrackIso03Dimuon1", 800, 0, 20, ""),
        (name, "displacedTrackIso04Dimuon1", 800, 0, 20, ""),
        (name, "displacedTrackIso03Dimuon2", 800, 0, 20, ""),
        (name, "displacedTrackIso04Dimuon2", 800, 0, 20, ""),
        (name, "pfRelIso04all1", 800, 0, 20, ""),
        (name, "pfRelIso04all2", 800, 0, 20, ""),
        (name, "3Dangle", 2000, -10, 10, ""),
        (name, "cos3Dangle", 400, -2, 2, ""),
        (name, "nSegments", 50, 0, 50, ""),
        (name, "nSegments1", 50, 0, 50, ""),
        (name, "nSegments2", 50, 0, 50, ""),
        (name, "isValid", 10, 0, 10, ""),
        (name, "vxy", 10000, 0, 1000, ""),
        (name, "vxySigma", 10000, 0, 100, ""),
        (name, "vxyz", 10000, 0, 1000, ""),
        (name, "vxyzSigma", 10000, 0, 100, ""),
        (name, "chi2", 1000, 0, 100, ""),
        (name, "ndof", 100, 0, 100, ""),
        (name, "vx", 200, -100, 100, ""),
        (name, "vy", 200, -100, 100, ""),
        (name, "vz", 200, -100, 100, ""),
        (name, "t", 200, -100, 100, ""),
        (name, "vxErr", 1000, -50, 50, ""),
        (name, "vyErr", 1000, -50, 50, ""),
        (name, "vzErr", 1000, -50, 50, ""),
        (name, "tErr", 200, -100, 100, ""),
        (name, "displacedTrackIso03Muon1", 800, 0, 20, ""),
        (name, "displacedTrackIso04Muon1", 800, 0, 20, ""),
        (name, "displacedTrackIso03Muon2", 800, 0, 20, ""),
        (name, "displacedTrackIso04Muon2", 800, 0, 20, ""),
        (name, "dRprox", 500, 0, 10, ""),
        (name, "dcaStatus", 10, 0, 10, ""),
        (name, "dcax", 200, -100, 100, ""),
        (name, "dcay", 200, -100, 100, ""),
        (name, "dcaz", 200, -100, 100, ""),
        (name, "missHitsAfterVert1", 100, 0, 100, ""),
        (name, "missHitsAfterVert2", 100, 0, 100, ""),
        (name, "deltaIso03", 1000, 0, 10, ""),
        (name, "deltaIso04", 1000, 0, 10, ""),
        (name, "logDeltaIso03", 1000, -5, 5, ""),
        (name, "logDeltaIso04", 1000, -5, 5, ""),
        (name, "deltaSquaredIso03", 1000, 0, 10, ""),
        (name, "deltaSquaredIso04", 1000, 0, 10, ""),
        (name, "logDeltaSquaredIso03", 1000, -5, 5, ""),
        (name, "logDeltaSquaredIso04", 1000, -5, 5, ""),
    )

  def __insert_Nminus1Histograms(self, params, name):
    params += (
        (name, "invMass", 20000, 0, 200, ""),
        (name, "logInvMass", 1000, -1, 2, ""),
        (name, "chargeProduct", 4, -2, 2, ""),
        (name, "maxHitsInFrontOfVert", 100, 0, 100, ""),
        (name, "absPtLxyDPhi1", 500, 0, 5, ""),
        (name, "dca", 1000, 0, 20, ""),
        (name, "absCollinearityAngle", 500, 0, 5, ""),
        (name, "normChi2", 50000, 0, 50, ""),
        (name, "displacedTrackIso03Dimuon1", 800, 0, 20, ""),
        (name, "displacedTrackIso03Dimuon2", 800, 0, 20, ""),
        (name, "pfRelIso1", 800, 0, 20, ""),
        (name, "pfRelIso2", 800, 0, 20, ""),
    )

  # For FillGenDimuonHistograms function
  def __insert_GenDimuonHistograms(self, params, name):
    for i in range(1, 6):
      params += (
          (name, "motherID1"+str(i), 10010, -10, 10000, ""),
          (name, "motherID2"+str(i), 10010, -10, 10000, ""),
      )
    params += (
        ("Event", "n"+name, 50, 0, 50, ""),
        (name, "index1", 100, 0, 100, ""),
        (name, "index2", 100, 0, 100, ""),
        (name, "index3", 100, 0, 100, ""),
        (name, "Lxy", 50000, 0, 5000, ""),
        (name, "Lxyz", 50000, 0, 5000, ""),
        (name, "properLxy", 50000, 0, 5000, ""),
        (name, "invMass", 20000, 0, 200, ""),
        (name, "logInvMass", 1000, -1, 2, ""),
        (name, "deltaR", 1000, 0, 10, ""),
        (name, "absCollinearityAngle", 500, 0, 5, ""),
        (name, "absPtLxyDPhi1", 500, 0, 5, ""),
        (name, "absPtLxyDPhi2", 500, 0, 5, ""),
        (name, "logLxy", 2000, -10, 10, ""),
    )
