from itertools import product
from math import pi
import numpy as np


class TTAlpsHistogrammerConfigHelper:
  def __init__(self, muonMatchingParams, muonVertexCollection, muonVertexCollectionInput, runRevertedMatching):
    self.muonMatchingParams = muonMatchingParams

    self.looseMuonCollections = []
    self.tightMuonCollections = []

    for category, matching in product(("", "DSA", "PAT"), muonMatchingParams):
      if runRevertedMatching:
        self.looseMuonCollections.append(f"Reverted{matching}Matched{category}Muons")
        self.looseMuonCollections.append(f"Reverted{matching}MatchedDisplaced{category}Muons")
      self.tightMuonCollections.append(f"Tight{category}Muons{matching}Match")
      self.looseMuonCollections.append(f"Loose{category}Muons{matching}Match")

    if muonMatchingParams.__len__() == 0:
      self.looseMuonCollections.append(f"LooseDSAMuons")
      self.looseMuonCollections.append(f"LoosePATMuons")

    self.bestMuonVertexCollections = []
    self.goodMuonVertexCollections = []
    self.fakeStudyBestMuonVertexCollections = []

    self.bestMuonVertexCollectionCuts = []

    if muonVertexCollection is not None:
      for category in ("", "_PatDSA", "_DSA", "_Pat"):
        self.bestMuonVertexCollections.append(f"{muonVertexCollection[0]}{category}")
        self.goodMuonVertexCollections.append(f"{muonVertexCollection[0].replace('Best', 'Good')}{category}")
        if runRevertedMatching:
          self.bestMuonVertexCollections.append(f"{muonVertexCollection[0]}_revertedMatching{category}")
          self.bestMuonVertexCollections.append(f"{muonVertexCollection[0]}_matchedToPatDSA{category}")
          self.bestMuonVertexCollections.append(f"{muonVertexCollection[0]}_matchedToDSA{category}")
      self.bestMuonVertexCollectionCuts = muonVertexCollection[1]

    self.looseMuonVertexCollections = []
    for category, matching in product(("", "_PatDSA", "_DSA", "_Pat"), muonMatchingParams):
      self.looseMuonVertexCollections.append(f"LooseMuonsVertex{matching}Match{category}")
      self.looseMuonVertexCollections.append(f"{muonVertexCollectionInput}{category}")

    self.ABCD_variables = {

        "absCollinearityAngle": (100, 0, 4),
        "3Dangle": (100, 0, pi),
        "cos3Dangle": (100, 0, 1),

        "Lxy": (100, 0, 700),
        "logLxy": (100, -2, 3),
        "logLxySignificance": (100, -2, 2),
        "logAbsCollinearityAngle": (160, -7, 1),
        "log3Dangle": (100, -3, 1),
        "logCos3Dangle": (100, -3, 1),

        "outerDR": (100, 0, 5),
        "logOuterDR": (100, -3, 3),
        "maxHitsInFrontOfVert": (10, 0, 10),
        "absPtLxyDPhi1": (100, 0, pi),
        "absPtLxyDPhi2": (100, 0, pi),

        "logAbsPtLxyDPhi1": (100, -5, 1),
        "logAbsPtLxyDPhi2": (100, -5, 1),

        "invMass": (100, 0, 100),
        "logInvMass": (100, -1, 2),

        "pt": (100, 0, 200),
        "leadingPt": (100, 0, 400),

        "logPt": (100, -1, 3),
        "logLeadingPt": (100, -1, 3),

        "eta": (100, -3, 3),
        "logEta": (100, -3, 1),
        "dEta": (100, 0, 3),
        "logDEta": (100, -3, 1),
        "dPhi": (100, 0, 2*pi),
        "logDPhi": (100, -3, 1),
        "nSegments": (10, 0, 10),
        "displacedTrackIso03Dimuon1": (100, 0, 0.01),
        "displacedTrackIso04Dimuon1": (100, 0, 0.01),
        "displacedTrackIso03Dimuon2": (100, 0, 0.01),
        "displacedTrackIso04Dimuon2": (100, 0, 0.01),
        "logDisplacedTrackIso03Dimuon1": (100, -4, 2),
        "logDisplacedTrackIso04Dimuon1": (100, -4, 2),
        "logDisplacedTrackIso03Dimuon2": (100, -4, 2),
        "logDisplacedTrackIso04Dimuon2": (100, -4, 2),

        "logDxyPVTraj1": (100, -5, 3),
        "logDxyPVTraj2": (100, -5, 3),
        "logDxyPVTrajSig1": (100, -3, 4),
        "logDxyPVTrajSig2": (100, -3, 4),

        "deltaIso03": (100, 0, 10),
        "deltaIso04": (100, 0, 10),
        "logDeltaIso03": (100, -9, 5),
        "logDeltaIso04": (100, -9, 5),
        "deltaSquaredIso03": (100, 0, 10),
        "deltaSquaredIso04": (100, 0, 10),
        "logDeltaSquaredIso03": (100, -7, 5),
        "logDeltaSquaredIso04": (100, -7, 5),

        # some extra:
        "normChi2": (100, 0, 1),
        "logNormChi2": (100, -7, 2),
        "dca": (100, 0, 2),
        "logDca": (100, -4, 1),
    }

    self.ABCD_variables_subset = {
        "logAbsCollinearityAngle": (100, -7, 1),
        "logLeadingPt": (100, -1, 3),
        "logDxyPVTraj1": (100, -5, 3),
        "logPt": (100, -1, 3),
        "logInvMass": (100, -1, 2),
        "logOuterDR": (100, -3, 3),
        "logDxyPVTrajSig1": (100, -3, 4),
        "logDxyPVTrajSig2": (100, -3, 4),
        "absPtLxyDPhi1": (100, 0, pi),
        "absCollinearityAngle": (100, 0, 4),
        "logNormChi2": (100, -7, 2),
        "logDca": (100, -4, 1),
    }

    self.singleMuon_ABCD_variables = {

        "pt": (400, 0, 2000),
        "logPt": (100, -1, 3),

        "eta": (120, -3, 3),
        "phi": (100, -3, 3),

        "dxyPVTraj": (200, -700, 700),
        "absDxyPVTraj": (100, 0, 700),
        "logDxyPVTraj": (100, -5, 3),
        "dxyPVTrajSig": (200, -700, 700),
        "absDxyPVTrajSig": (100, 0, 700),
        "logDxyPVTrajSig": (100, -3, 3),

        "normChi2": (100, 0, 1),
        "logNormChi2": (100, -7, 1),
    }

    self.pt_irr_bins = [3, 20, 40, 100, 200, 600]
    self.absDxy_irr_bins = [0, 10, 120, 700]
    self.singleMuon_ABCD_irregular_variables = {
        "absDxyPVTraj_irr": self.absDxy_irr_bins,
        "pt_irr": self.pt_irr_bins,
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
    for collection in self.goodMuonVertexCollections:
      params += (
          ("Event", "n"+collection, 50, 0, 50, ""),
      )

    return tuple(params)

  def get_llp_irregular_params(self):
    params = []
    for collection in self.looseMuonCollections:
      self.__insert_irregular_MuonHistograms(params, collection)

    return tuple(params)

  def get_nminus1_params(self):
    params = []

    for collection in self.bestMuonVertexCollections + self.goodMuonVertexCollections:
      for cut in self.bestMuonVertexCollectionCuts:
        name = self.__insert_into_name(collection, "Nminus1"+cut)
        self.__insert_Nminus1Histograms(params, name)
        names = (
            self.__insert_into_name(name, "FromALP"),
            self.__insert_into_name(name, "Resonant"),
            self.__insert_into_name(name, "FalseResonant"),
            self.__insert_into_name(name, "NonResonant"),
        )
        for name_ in names:
          self.__insert_Nminus1Histograms(params, name_)

    return tuple(params)

  def get_nminus1_params2D(self):
    params = []

    for collection in self.bestMuonVertexCollections + self.goodMuonVertexCollections:
      for cut in self.bestMuonVertexCollectionCuts:
        name = self.__insert_into_name(collection, "Nminus1"+cut)
        self.__insert_Nminus1Histograms2D(params, name)
        names = (
            self.__insert_into_name(name, "FromALP"),
            self.__insert_into_name(name, "Resonant"),
            self.__insert_into_name(name, "FalseResonant"),
            self.__insert_into_name(name, "NonResonant"),
        )
        for name_ in names:
          self.__insert_Nminus1Histograms2D(params, name_)

    return tuple(params)

  def get_llp_2d_params(self):
    params = []

    for collection in self.bestMuonVertexCollections + self.goodMuonVertexCollections:
      self.__insert_MuonVertex2DHistograms(params, collection)

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

    # FillRecoGenSingleMuonHistograms
    for collection in self.bestMuonVertexCollections:
      for flag in ("PU", "fake", "real"):
        name = collection + "_" + flag
        self.__insert_SingleMuonQualityHistograms(params, name)

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

  def get_gen_matched_irregular_params(self):
    params = []
    for collection in self.looseMuonCollections + self.tightMuonCollections:
      names = (
          self.__insert_into_name(collection, "FromALP"),
          self.__insert_into_name(collection, "FromW"),
      )
      for name in names:
        self.__insert_irregular_MuonHistograms(params, name)

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

  def get_abcd_2Dparams(self, runGenLevelResonancesABCD, runGenLevelMothersABCD):
    params = []

    all_mother_categories = []
    if runGenLevelMothersABCD:
      mother_categories = ["other", "X", "Y", "ALP", "D", "B", "d", "u", "s", "c", "b", "t", "e",
                           "mu", "tau", "g", "gamma", "Z", "W", "rho", "pi0", "omega", "K0", "phi", "upsilon", "JPsi"]
      mother_categories = ["other", "X", "Y", "ALP", "D", "B", "q", "l", "tau", "g", "gamma", "Z", 
                            "W", "lightMeson", "JPsi"]
      for category1 in mother_categories:
        for category2 in mother_categories:
          category_name = "".join(sorted([category1, category2]))
          all_mother_categories.append(category_name)

    for collection in self.bestMuonVertexCollections:
      for variable_1, (nBins_1, xMin_1, xMax_1) in self.ABCD_variables.items():
        for variable_2, (nBins_2, xMin_2, xMax_2) in self.ABCD_variables.items():
          if variable_1 == variable_2:
            continue

          name = self.__insert_into_name(collection, f"_{variable_2}_vs_{variable_1}")

          params.append((name, nBins_1, xMin_1, xMax_1, nBins_2, xMin_2, xMax_2, ""))

      for variable_1, (nBins_1, xMin_1, xMax_1) in self.ABCD_variables_subset.items():
        for variable_2, (nBins_2, xMin_2, xMax_2) in self.ABCD_variables_subset.items():
          for category in all_mother_categories:
            name = self.__insert_into_name(collection, f"_{variable_2}_vs_{variable_1}_{category}")
            params.append((name, nBins_1, xMin_1, xMax_1, nBins_2, xMin_2, xMax_2, ""))

          if runGenLevelResonancesABCD:
            names = (
                self.__insert_into_name(collection, "FromALP"),
                self.__insert_into_name(collection, "Resonant"),
                self.__insert_into_name(collection, "FalseResonant"),
                self.__insert_into_name(collection, "NonResonant"),
            )
            for collectionName in names:
              name = self.__insert_into_name(collectionName, f"_{variable_2}_vs_{variable_1}")
              params.append((name, nBins_1, xMin_1, xMax_1, nBins_2, xMin_2, xMax_2, ""))

    return tuple(params)

  def get_singleMuon_abcd_2Dparams(self):
    params = []

    for collection in self.looseMuonCollections:
      for variable_1, (nBins_1, xMin_1, xMax_1) in self.singleMuon_ABCD_variables.items():
        for variable_2, (nBins_2, xMin_2, xMax_2) in self.singleMuon_ABCD_variables.items():
          if variable_1 == variable_2:
            continue

          name = self.__insert_into_name(collection, f"_{variable_2}_vs_{variable_1}")
          params.append((name, nBins_1, xMin_1, xMax_1, nBins_2, xMin_2, xMax_2, ""))

    return tuple(params)

  def get_singleMuon_abcd_irregular_2Dparams(self):
    params = []

    for collection in self.looseMuonCollections:
      for variable_1, binEdges1 in self.singleMuon_ABCD_irregular_variables.items():
        for variable_2, binEdges2 in self.singleMuon_ABCD_irregular_variables.items():
          if variable_1 == variable_2:
            continue

          name = self.__insert_into_name(collection, f"_{variable_2}_vs_{variable_1}")
          params.append((name, binEdges1, binEdges2, ""))

    return tuple(params)

  def get_abcd_mothers_2Dparams(self):
    params = []

    for collection in self.bestMuonVertexCollections:
      for blob in ["", "_lowBlob", "_rightBlob", "_centralBlob", "_lowLine", "_rightLine", "_mysteriousBlob"]:
        params.append((collection+"_motherPid1_vs_motherPid2"+blob, 2000, -1000, 1000, 2000, -1000, 1000, ""))

    return tuple(params)

  def get_abcd_1Dparams(self, runGenLevelResonancesABCD, runABCDMothersHistograms):
    params = []

    for collection in self.bestMuonVertexCollections:
      if runABCDMothersHistograms:
        params += (
            (collection, "deltaR_WW", 500, 0, 10, ""),
            (collection, "deltaR_Wtau", 500, 0, 10, ""),
            (collection, "deltaR_OS", 500, 0, 10, ""),
            (collection, "logDeltaR_WW", 100, -5, 5, ""),
            (collection, "logDeltaR_Wtau", 100, -5, 5, ""),
            (collection, "logDeltaR_OS", 100, -5, -5, ""),
        )
      if runGenLevelResonancesABCD:
        names = (
            self.__insert_into_name(collection, "FromALP"),
            self.__insert_into_name(collection, "Resonant"),
            self.__insert_into_name(collection, "FalseResonant"),
            self.__insert_into_name(collection, "NonResonant"),
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
    collections = ("BestDimuonVertex", "BestPFIsoDimuonVertex")

    variables = (

        # SR 2018:
        ("logLxy", "logLeadingPt"),  # SR 2018
        ("logDxyPVTraj1", "logLeadingPt"),
        ("logDxyPVTraj1", "logPt"),
        ("logDxyPVTraj2", "logPt"),
        ("logPt", "logInvMass"),
        ("logPt", "logDEta"),

        ("logAbsCollinearityAngle", "logLeadingPt"), # SR combined
        ("logAbsCollinearityAngle", "logPt"), # SR combined

        ("log3Dangle", "logLeadingPt"), # 2018 DSA-DSA looser chi2 vs DCA cut
        ("logOuterDR", "logLeadingPt"), # 2018 DSA-DSA looser chi2 vs DCA cut
        
        ("logLxy", "log3Dangle"), # SR combined, 2018
        ("logPt", "logDisplacedTrackIso03Dimuon2"), # Jpsi CR 2018
        ("logLxy", "logPt"), # Jpsi CR 2018
    )

    SF_variables = []
    for collection in collections:
      for variable_pair in variables:
        variable1 = f"{variable_pair[0]}_vs_{variable_pair[1]}"
        variable2 = f"{variable_pair[1]}_vs_{variable_pair[0]}"
        for category in ("", "_PatDSA", "_DSA", "_Pat"):
          name1 = self.__insert_into_name(collection, f"_{variable1}{category}")
          name2 = self.__insert_into_name(collection, f"_{variable2}{category}")
          SF_variables.append(name1)
          SF_variables.append(name2)

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
        (name, "pt", 10000, 0, 5000, ""),
        (name, "logPt", 1000, -1, 3, ""),
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
        (name, "logAbsDzFromLeadingTightPUlt30", 10000, -5, 3, ""),
        (name, "logAbsDzFromLeadingTightPUge30", 10000, -5, 3, ""),
        (name, "logAbsDzFromLeadingTightPUlt15", 10000, -5, 3, ""),
        (name, "logAbsDzFromLeadingTightPUgt45", 10000, -5, 3, ""),
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
        (name, "absDxyPVTraj", 50000, 0, 1000, ""),
        (name, "logDxyPVTraj", 1000, -5, 3, ""),
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

  def __insert_irregular_MuonHistograms(self, params, name):
    params += (
        (name, "absDxyPVTraj_irr", self.absDxy_irr_bins, ""),
        (name, "pt_irr", self.pt_irr_bins, ""),
    )

  # FillMuonVertexHistograms function
  def __insert_MuonVertexHistograms(self, params, name):
    params += (
        ("Event", "n"+name, 50, 0, 50, ""),
        (name, "normChi2", 50000, 0, 50, ""),
        (name, "logNormChi2", 1000, -8, 2, ""),
        (name, "Lxy", 40000, 0, 1000, ""),
        (name, "logLxy", 2000, -10, 10, ""),
        (name, "LxySigma", 5000, 0, 500, ""),
        (name, "LxySignificance", 4000, 0, 1000, ""),
        (name, "dR", 500, 0, 10, ""),
        (name, "proxDR", 500, 0, 10, ""),
        (name, "outerDR", 500, 0, 10, ""),
        (name, "logOuterDR", 600, -3, 3, ""),
        (name, "dEta", 500, 0, 10, ""),
        (name, "dPhi", 500, 0, 10, ""),
        (name, "maxHitsInFrontOfVert", 100, 0, 100, ""),
        (name, "sumHitsInFrontOfVert", 100, 0, 100, ""),
        (name, "hitsInFrontOfVert1", 100, 0, 100, ""),
        (name, "hitsInFrontOfVert2", 100, 0, 100, ""),
        (name, "dca", 1000, 0, 20, ""),
        (name, "logDca", 500, -4, 1, ""),
        (name, "absCollinearityAngle", 500, 0, 5, ""),
        (name, "absPtLxyDPhi1", 500, 0, 5, ""),
        (name, "absPtLxyDPhi2", 500, 0, 5, ""),
        (name, "logAbsPtLxyDPhi1", 600, -5, 1, ""),
        (name, "logAbsPtLxyDPhi2", 600, -5, 1, ""),
        (name, "invMass", 20000, 0, 200, ""),
        (name, "invMassJPsiBin", 1, 2.4, 3.9, ""),
        (name, "logInvMass", 1000, -1, 3, ""),
        (name, "pt", 2000, 0, 1000, ""),
        (name, "logPt", 1000, -1, 3, ""),
        (name, "eta", 500, -10, 10, ""),
        (name, "chargeProduct", 4, -2, 2, ""),
        (name, "muonPt", 2000, 0, 1000, ""),
        (name, "muonPtErr", 2000, 0, 1000, ""),
        (name, "muonPt1", 2000, 0, 1000, ""),
        (name, "muonPt2", 2000, 0, 1000, ""),
        (name, "muonPtErr1", 2000, 0, 1000, ""),
        (name, "muonPtErr2", 2000, 0, 1000, ""),
        (name, "leadingPt", 2000, 0, 1000, ""),
        (name, "subleadingPt", 2000, 0, 1000, ""),
        (name, "leadingEta", 500, -10, 10, ""),
        (name, "subleadingEta", 500, -10, 10, ""),
        (name, "muonEta1", 500, -10, 10, ""),
        (name, "muonEta2", 500, -10, 10, ""),
        (name, "dxyPVTraj1", 50000, -500, 500, ""),
        (name, "dxyPVTraj2", 50000, -500, 500, ""),
        (name, "absDxyPVTraj1", 50000, 0, 1000, ""),
        (name, "absDxyPVTraj2", 50000, 0, 1000, ""),
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
        (name, "vxySigma", 5000, 0, 500, ""),
        (name, "vxyz", 10000, 0, 1000, ""),
        (name, "vxyzSigma", 5000, 0, 500, ""),
        (name, "chi2", 1000, 0, 100, ""),
        (name, "ndof", 100, 0, 100, ""),
        (name, "vx", 200, -100, 100, ""),
        (name, "vy", 200, -100, 100, ""),
        (name, "vz", 200, -100, 100, ""),
        (name, "t", 200, -100, 100, ""),
        (name, "vxErr", 2000, -100, 100, ""),
        (name, "vyErr", 2000, -100, 100, ""),
        (name, "vzErr", 2000, -100, 100, ""),
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
        (name, "absDzFromLeadingTight1", 10000, 0, 100, ""),
        (name, "absDzFromLeadingTight2", 10000, 0, 100, ""),
    )

  def __insert_MuonVertex2DHistograms(self, params, name):
    params += (
        (f"{name}_vy_vs_vx", 1000, -1000, 1000, 1000, -1000, 1000, ""),
        (f"{name}_vy_vs_vx_trackerOnly", 1000, -130, 130, 1000, -130, 130, ""),
    )

  def __insert_Nminus1Histograms(self, params, name):
    params += (
        (name, "invMass", 20000, 0, 200, ""),
        (name, "logInvMass", 1000, -1, 3, ""),
        (name, "invMassJPsiBin", 1, 2.4, 3.9, ""),
        (name, "chargeProduct", 4, -2, 2, ""),
        (name, "maxHitsInFrontOfVert", 100, 0, 100, ""),
        (name, "sumHitsInFrontOfVert", 100, 0, 100, ""),
        (name, "hitsInFrontOfVert1", 100, 0, 100, ""),
        (name, "hitsInFrontOfVert2", 100, 0, 100, ""),
        (name, "absPtLxyDPhi1", 500, 0, 5, ""),
        (name, "absPtLxyDPhi2", 500, 0, 5, ""),
        (name, "dca", 1000, 0, 20, ""),
        (name, "absCollinearityAngle", 500, 0, 5, ""),
        (name, "normChi2", 50000, 0, 50, ""),
        (name, "displacedTrackIso03Dimuon1", 800, 0, 20, ""),
        (name, "displacedTrackIso03Dimuon2", 800, 0, 20, ""),
        (name, "pfRelIso1", 800, 0, 20, ""),
        (name, "pfRelIso2", 800, 0, 20, ""),
        (name, "dR", 500, 0, 10, ""),
        (name, "outerDR", 500, 0, 10, ""),
        (name, "Lxy", 10000, 0, 1000, ""),
        (name, "LxySigma", 5000, 0, 500, ""),
        (name, "vxy", 10000, 0, 1000, ""),
        (name, "vxySigma", 5000, 0, 500, ""),
        (name, "vxErr", 2000, -100, 100, ""),
        (name, "vyErr", 2000, -100, 100, ""),
        (name, "vzErr", 2000, -100, 100, ""),
        (name, "logLxy", 2000, -10, 10, ""),
        (name, "OS_chargeProduct", 4, -2, 2, ""),
        (name, "SS_chargeProduct", 4, -2, 2, ""),
        (name, "OS_leadingPt", 2000, 0, 1000, ""),
        (name, "SS_leadingPt", 2000, 0, 1000, ""),
        (name, "OS_Lxy", 10000, 0, 1000, ""),
        (name, "SS_Lxy", 10000, 0, 1000, ""),
        (name, "absCollinearityAngle_lt2", 500, 0, 5, ""),
        (name, "absCollinearityAngle_gt2", 500, 0, 5, ""),
    )

  def __insert_Nminus1Histograms2D(self, params, name):
    params += (
        (name + "_logNormChi2_vs_logDCA", 100, -4, 1, 100, -7, 1, ""),
        (name + "_absPtLxyDPhi1_vs_absCollinearityAngle", 100, 0, 4, 100, 0, pi, ""),
        (name + "_absPtLxyDPhi2_vs_absCollinearityAngle", 100, 0, 4, 100, 0, pi, ""),
        (name + "_logPtLxyDPhi1_vs_logCollinearityAngle", 160, -7, 1, 100, -5, 1, ""),
        (name + "_logPtLxyDPhi2_vs_logCollinearityAngle", 160, -7, 1, 100, -5, 1, ""),
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

  def __insert_SingleMuonQualityHistograms(self, params, name):

    params += (
        ("Event", "n"+name, 50, 0, 50, ""),
        (name, "nSegments", 100, 0, 100, ""),
        (name, "nDTSegments", 100, 0, 100, ""),
        (name, "nCSCSegments", 100, 0, 100, ""),
        (name, "trkNumPlanes", 100, 0, 100, ""),
        (name, "trkNumHits", 100, 0, 100, ""),
        (name, "trkNumDTHits", 100, 0, 100, ""),
        (name, "trkNumCSCHits", 100, 0, 100, ""),
        (name, "normChi2", 50000, 0, 50, ""),
        (name, "pt", 2000, 0, 1000, ""),
        (name, "ptErr", 2000, 0, 1000, ""),
        (name, "eta", 300, -3, 3, ""),
        (name, "etaErr", 300, -3, 3, ""),
        (name, "phi", 300, -3, 3, ""),
        (name, "phiErr", 300, -3, 3, ""),
        (name, "outerEta", 300, -3, 3, ""),
        (name, "outerPhi", 300, -3, 3, ""),
        (name, "outerPhi", 300, -3, 3, ""),
        (name, "absDzFromLeadingTight", 10000, 0, 1000, ""),
        (name, "logAbsDzFromLeadingTight", 10000, -5, 3, ""),
        (name, "genMuonDR", 1000, 0, 10, ""),
    )
