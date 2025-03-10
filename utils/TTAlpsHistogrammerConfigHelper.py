from itertools import product
from math import pi

class TTAlpsHistogrammerConfigHelper:
  def __init__(self, muonMatchingParams, muonVertexCollections):
    self.muonMatchingParams = muonMatchingParams
    self.muonVertexCollections = muonVertexCollections

    self.muonCollections = []

    for category, matching in product(("", "DSA", "PAT"), muonMatchingParams):
      self.muonCollections.append(f"Tight{category}Muons{matching}Match")
      self.muonCollections.append(f"Loose{category}Muons{matching}Match")

    self.muonVertexCollections = []

    for category, collection in product(("", "_PatDSA", "_DSA", "_Pat"), muonVertexCollections):
      self.muonVertexCollections.append(f"{collection}{category}")

    for category, matching in product(("", "_PatDSA", "_DSA", "_Pat"), muonMatchingParams):
      self.muonVertexCollections.append(f"TightMuonsVertex{matching}Match{category}")
      self.muonVertexCollections.append(f"LooseMuonsVertex{matching}Match{category}")
      # TODO: do we still need these histograms?
      self.muonVertexCollections.append(f"LooseMuonsVertexMinDphi2{matching}Match{category}")
      self.muonVertexCollections.append(f"LooseMuonsVertexMaxDphi2{matching}Match{category}")

  def get_default_params(self):
    return (
        #  collection             variable               bins    xmin    xmax    dir
        ("Event", "MET_pt", 1000, 0, 1000, ""),
        ("Event", "PV_npvs", 300, 0, 300, ""),
        ("Event", "PV_npvsGood", 300, 0, 300, ""),
        ("Event", "PV_x", 200, -100, 100, ""),
        ("Event", "PV_y", 200, -100, 100, ""),
        ("Event", "PV_z", 200, -100, 100, ""),
    )

  def get_basic_params(self):
    return (
        #  collection         variable                      bins   xmin   xmax    dir
        ("Event", "normCheck", 1, 0, 1, ""),
    )

  def get_llp_params(self):
    params = []

    for collection in self.muonCollections:
      params += (
          ("Event", "n"+collection, 50, 0, 50, ""),
          (collection, "pt", 2000, 0, 1000, ""),
          (collection, "eta", 300, -3, 3, ""),
          (collection, "phi", 300, -3, 3, ""),
          (collection, "dxy", 20000, -2000, 2000, ""),
          (collection, "absDxyPVTraj", 10000, 0, 2000, ""),
          (collection, "dxyPVTrajErr", 10000, 0, 2000, ""),
          (collection, "dxyPVTrajSig", 10000, 0, 2000, ""),
          (collection, "ip3DPVSigned", 20000, -2000, 2000, ""),
          (collection, "ip3DPVSignedErr", 10000, 0, 2000, ""),
          (collection, "ip3DPVSignedSig", 10000, 0, 2000, ""),
          (collection, "minDeltaR", 1000, 0, 10, ""),
          (collection, "minOuterDeltaR", 1000, 0, 10, ""),
          (collection, "minProxDeltaR", 1000, 0, 10, ""),
          (collection, "pfRelIso04all", 800, 0, 20, ""),
          (collection, "tkRelIso", 800, 0, 20, ""),
          (collection, "isPAT", 10, 0, 10, ""),
          (collection, "isTight", 10, 0, 10, ""),
      )

      names = (
          self.__insert_into_name(collection, "NotFromALP"),
          self.__insert_into_name(collection, "FromW"),
      )

      for name in names:
        params += (
            ("Event", "n"+name, 50, 0, 50, ""),
            ("Event", "n"+name+"_hmu", 50, 0, 50, ""),
            (name, "pt", 2000, 0, 1000, ""),
            (name, "eta", 300, -3, 3, ""),
            (name, "phi", 300, -3, 3, ""),
            (name, "dxy", 20000, -2000, 2000, ""),
            (name, "absDxyPVTraj", 10000, 0, 2000, ""),
            (name, "dxyPVTrajErr", 10000, 0, 2000, ""),
            (name, "dxyPVTrajSig", 10000, 0, 2000, ""),
            (name, "ip3DPVSigned", 20000, -2000, 2000, ""),
            (name, "ip3DPVSignedErr", 10000, 0, 2000, ""),
            (name, "ip3DPVSignedSig", 10000, 0, 2000, ""),
            (name, "minDeltaR", 1000, 0, 10, ""),
            (name, "minOuterDeltaR", 1000, 0, 10, ""),
            (name, "minProxDeltaR", 1000, 0, 10, ""),
            (name, "pfRelIso04all", 800, 0, 20, ""),
            (name, "tkRelIso", 800, 0, 20, ""),
            (name, "isPAT", 10, 0, 10, ""),
            (name, "isTight", 10, 0, 10, ""),
            (name, "hasLeadingMuon", 10, 0, 10, ""),
            (name, "hmu_hasLeadingMuon", 10, 0, 10, ""),
            (name, "index", 10, 0, 10, ""),
            (name, "hmu_index", 10, 0, 10, ""),
            (name, "hmu_pt", 4000, 0, 1000, ""),
        )

    for collection in self.muonVertexCollections:
      params += (
          ("Event", "n"+collection, 50, 0, 50, ""),
          (collection, "normChi2", 50000, 0, 50, ""),
          (collection, "Lxy", 10000, 0, 1000, ""),
          (collection, "logLxy", 2000, -10, 10, ""),
          (collection, "LxySigma", 10000, 0, 100, ""),
          (collection, "LxySignificance", 1000, 0, 1000, ""),
          (collection, "vxy", 1000, 0, 1000, ""),
          (collection, "vxySigma", 10000, 0, 100, ""),
          (collection, "vxySignificance", 1000, 0, 1000, ""),
          (collection, "dR", 500, 0, 10, ""),
          (collection, "proxDR", 500, 0, 10, ""),
          (collection, "outerDR", 500, 0, 10, ""),
          (collection, "dEta", 500, 0, 10, ""),
          (collection, "dPhi", 500, 0, 10, ""),
          (collection, "outerDEta", 500, 0, 10, ""),
          (collection, "outerDPhi", 500, 0, 10, ""),
          (collection, "maxHitsInFrontOfVert", 100, 0, 100, ""),
          (collection, "sumHitsInFrontOfVert", 100, 0, 100, ""),
          (collection, "maxMissHitsAfterVert", 100, 0, 100, ""),
          (collection, "hitsInFrontOfVert1", 100, 0, 100, ""),
          (collection, "hitsInFrontOfVert2", 100, 0, 100, ""),
          (collection, "dca", 1000, 0, 20, ""),
          (collection, "absCollinearityAngle", 500, 0, 5, ""),
          (collection, "absPtLxyDPhi1", 500, 0, 5, ""),
          (collection, "absPtLxyDPhi2", 500, 0, 5, ""),
          (collection, "invMass", 2000, 0, 200, ""),
          (collection, "logInvMass", 1000, -1, 2, ""),
          (collection, "pt", 2000, 0, 1000, ""),
          (collection, "eta", 500, -10, 10, ""),
          (collection, "chargeProduct", 4, -2, 2, ""),
          (collection, "leadingPt", 2000, 0, 1000, ""),
          (collection, "dxyPVTraj1", 1000, 0, 1000, ""),
          (collection, "dxyPVTraj2", 1000, 0, 1000, ""),
          (collection, "dxyPVTrajSig1", 1000, 0, 1000, ""),
          (collection, "dxyPVTrajSig2", 1000, 0, 1000, ""),
          (collection, "displacedTrackIso03Dimuon1", 800, 0, 20, ""),
          (collection, "displacedTrackIso04Dimuon1", 800, 0, 20, ""),
          (collection, "displacedTrackIso03Dimuon2", 800, 0, 20, ""),
          (collection, "displacedTrackIso04Dimuon2", 800, 0, 20, ""),
          (collection, "displacedTrackIso03Muon1", 800, 0, 20, ""),
          (collection, "displacedTrackIso04Muon1", 800, 0, 20, ""),
          (collection, "displacedTrackIso03Muon2", 800, 0, 20, ""),
          (collection, "displacedTrackIso04Muon2", 800, 0, 20, ""),
          (collection, "pfRelIso04all1", 800, 0, 20, ""),
          (collection, "pfRelIso04all2", 800, 0, 20, ""),
          (collection, "tkRelIsoMuon1", 800, 0, 20, ""),
          (collection, "tkRelIsoMuon2", 800, 0, 20, ""),
          (collection, "3Dangle", 2000, -10, 10, ""),
          (collection, "cos3Dangle", 400, -2, 2, ""),
          (collection, "deltaPixelHits", 50, 0, 50, ""),
          (collection, "nSegments", 50, 0, 50, ""),
          (collection, "nSegments1", 50, 0, 50, ""),
          (collection, "nSegments2", 50, 0, 50, ""),
          (collection, "nDTHits", 100, 0, 100, ""),
          (collection, "nDTHits1", 100, 0, 100, ""),
          (collection, "nDTHits2", 100, 0, 100, ""),
          (collection, "nDTHitsBarrelOnly", 100, 0, 100, ""),
          (collection, "nDTHits1BarrelOnly", 100, 0, 100, ""),
          (collection, "nDTHits2BarrelOnly", 100, 0, 100, ""),
      )

    return tuple(params)

  def get_nminus1_params(self):
    params = []

    for collection in self.muonVertexCollections:
      if not collection.startswith("Best"):
        continue

      name = self.__insert_into_name(collection, "Nminus1")

      params += (
          (name, "invMass", 2000, 0, 200, ""),
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
    return tuple(params)

  def get_gen_matched_params(self):
    params = []

    for collection in self.muonVertexCollections:
      if collection.startswith("Best"):
        continue

      name = self.__insert_into_name(collection, "FromALPNminus1")

      params += (
          (name, "invMass", 2000, 0, 200, ""),
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

      names = (
          self.__insert_into_name(collection, "FromALP"),
          self.__insert_into_name(collection, "NotFromALP"),
          self.__insert_into_name(collection, "NonResonant"),
          self.__insert_into_name(collection, "ResonancesNotFromALP"),
          self.__insert_into_name(collection, "NonresonancesNotFromALP"),
      )

      for name in names:
        params += (
            ("Event", "n"+name, 50, 0, 50, ""),
            ("Event", "n"+name+"_hmu", 50, 0, 50, ""),
            (name, "pt", 2000, 0, 1000, ""),
            (name, "eta", 300, -3, 3, ""),
            (name, "phi", 300, -3, 3, ""),
            (name, "dxy", 20000, -2000, 2000, ""),
            (name, "absDxyPVTraj", 10000, 0, 2000, ""),
            (name, "dxyPVTrajErr", 10000, 0, 2000, ""),
            (name, "dxyPVTrajSig", 10000, 0, 2000, ""),
            (name, "ip3DPVSigned", 20000, -2000, 2000, ""),
            (name, "ip3DPVSignedErr", 10000, 0, 2000, ""),
            (name, "ip3DPVSignedSig", 10000, 0, 2000, ""),
            (name, "minDeltaR", 1000, 0, 10, ""),
            (name, "minOuterDeltaR", 1000, 0, 10, ""),
            (name, "minProxDeltaR", 1000, 0, 10, ""),
            (name, "invMass", 2000, 0, 200, ""),
            (name, "logInvMass", 1000, -1, 2, ""),
            (name, "deltaR", 1000, 0, 10, ""),
            (name, "outerDeltaR", 1000, 0, 10, ""),
            (name, "genMuonMinDR1", 1000, 0, 10, ""),
            (name, "genMuonMinDR2", 1000, 0, 10, ""),
            (name, "pfRelIso04all", 800, 0, 20, ""),
            (name, "tkRelIso", 800, 0, 20, ""),
            (name, "isPAT", 10, 0, 10, ""),
            (name, "isTight", 10, 0, 10, ""),
            (name, "Lxy", 1000, 0, 1000, ""),
            (name, "LxySignificance", 1000, 0, 1000, ""),
            (name, "LxySigma", 10000, 0, 100, ""),
            (name, "3Dangle", 2000, -10, 10, ""),
            (name, "cos3Dangle", 400, -2, 2, ""),
            (name, "normChi2", 50000, 0, 50, ""),
            (name, "logLxy", 2000, -10, 10, ""),
            (name, "dca", 1000, 0, 20, ""),
            (name, "absCollinearityAngle", 500, 0, 5, ""),
            (name, "chargeProduct", 4, -2, 2, ""),
            (name, "vxy", 1000, 0, 1000, ""),
            (name, "vxySigma", 10000, 0, 100, ""),
            (name, "vxySignificance", 1000, 0, 1000, ""),
            (name, "dR", 500, 0, 10, ""),
            (name, "proxDR", 500, 0, 10, ""),
            (name, "outerDR", 500, 0, 10, ""),
            (name, "dEta", 500, 0, 10, ""),
            (name, "dPhi", 500, 0, 10, ""),
            (name, "etaSum", 700, 0, 7, ""),
            (name, "outerDEta", 500, 0, 10, ""),
            (name, "outerDPhi", 500, 0, 10, ""),
            (name, "maxHitsInFrontOfVert", 100, 0, 100, ""),
            (name, "hitsInFrontOfVert1", 100, 0, 100, ""),
            (name, "hitsInFrontOfVert2", 100, 0, 100, ""),
            (name, "dca", 1000, 0, 20, ""),
            (name, "absCollinearityAngle", 500, 0, 5, ""),
            (name, "absPtLxyDPhi1", 500, 0, 5, ""),
            (name, "absPtLxyDPhi2", 500, 0, 5, ""),
            (name, "leadingPt", 2000, 0, 1000, ""),
            (name, "dxyPVTraj1", 1000, 0, 1000, ""),
            (name, "dxyPVTraj2", 1000, 0, 1000, ""),
            (name, "dxyPVTrajSig1", 1000, 0, 1000, ""),
            (name, "dxyPVTrajSig2", 1000, 0, 1000, ""),
            (name, "displacedTrackIso03Dimuon1", 800, 0, 20, ""),
            (name, "displacedTrackIso04Dimuon1", 800, 0, 20, ""),
            (name, "displacedTrackIso03Dimuon2", 800, 0, 20, ""),
            (name, "displacedTrackIso04Dimuon2", 800, 0, 20, ""),
            (name, "displacedTrackIso03Muon1", 800, 0, 20, ""),
            (name, "displacedTrackIso04Muon1", 800, 0, 20, ""),
            (name, "displacedTrackIso03Muon2", 800, 0, 20, ""),
            (name, "displacedTrackIso04Muon2", 800, 0, 20, ""),
            (name, "pfRelIso04all1", 800, 0, 20, ""),
            (name, "pfRelIso04all2", 800, 0, 20, ""),
            (name, "tkRelIsoMuon1", 800, 0, 20, ""),
            (name, "tkRelIsoMuon2", 800, 0, 20, ""),
            (name, "deltaPixelHits", 50, 0, 50, ""),
            (name, "nSegments", 50, 0, 50, ""),
            (name, "nSegments1", 50, 0, 50, ""),
            (name, "nSegments2", 50, 0, 50, ""),
            (name, "nDTHits", 100, 0, 100, ""),
            (name, "nDTHits1", 100, 0, 100, ""),
            (name, "nDTHits2", 100, 0, 100, ""),
            (name, "nDTHitsBarrelOnly", 100, 0, 100, ""),
            (name, "nDTHits1BarrelOnly", 100, 0, 100, ""),
            (name, "nDTHits2BarrelOnly", 100, 0, 100, ""),
            (name, "hasLeadingMuon", 10, 0, 10, ""),
            (name, "hmu_hasLeadingMuon", 10, 0, 10, ""),
            (name, "index", 10, 0, 10, ""),
            (name, "hmu_index", 10, 0, 10, ""),
            (name, "hmu_pt", 4000, 0, 1000, ""),
            (name, "genPlaneAngle", 500, 0, 5, ""),
            (name, "recoPlaneAngle", 500, 0, 5, ""),
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

    for i in range(1, 6):
      params += (
          ("GenMuonFromALP", "motherID"+str(i), 10010, -10, 10000, ""),
          ("GenMuonNotFromALP", "motherID"+str(i), 10010, -10, 10000, ""),
          ("GenDimuonNotFromALP", "motherID1"+str(i), 10010, -10, 10000, ""),
          ("GenDimuonNotFromALP", "motherID2"+str(i), 10010, -10, 10000, ""),
      )

    for name in ["FromALP", "FromW", "NotFromALP"]:
      params += (
          ("Event", "nGenMuon"+name, 50, 0, 50, ""),
          ("GenMuon"+name, "index1", 100, 0, 100, ""),
          ("GenMuon"+name, "index2", 100, 0, 100, ""),
          ("GenMuon"+name, "index3", 100, 0, 100, ""),
          ("GenMuon"+name, "pt1", 4000, 0, 1000, ""),
          ("GenMuon"+name, "pt2", 4000, 0, 1000, ""),
          ("GenMuon"+name, "eta1", 300, -3, 3, ""),
          ("GenMuon"+name, "eta2", 300, -3, 3, ""),
          ("GenMuon"+name, "phi1", 300, -3, 3, ""),
          ("GenMuon"+name, "phi2", 300, -3, 3, ""),
          ("GenMuon"+name, "Lxy", 50000, 0, 5000, ""),
          ("GenMuon"+name, "Lxyz", 50000, 0, 5000, ""),
          ("GenMuon"+name, "properLxy", 50000, 0, 5000, ""),
          ("GenMuon"+name, "properLxyT", 50000, 0, 5000, ""),
          ("GenMuon"+name, "properLxyz", 50000, 0, 5000, ""),
          ("GenMuon"+name, "dxy1", 50000, -5000, 5000, ""),
          ("GenMuon"+name, "dxy2", 50000, -5000, 5000, ""),
          ("GenMuon"+name, "RecoMatch1MinDR", 1000, 0, 10, ""),
          ("GenMuon"+name, "RecoMatch2MinDR", 1000, 0, 10, ""),
          ("GenMuon"+name, "RecoMatch1MinDPhi", 1000, 0, 10, ""),
          ("GenMuon"+name, "RecoMatch2MinDPhi", 1000, 0, 10, ""),
          ("GenMuon"+name, "RecoMatch1MinDEta", 1000, 0, 10, ""),
          ("GenMuon"+name, "RecoMatch2MinDEta", 1000, 0, 10, ""),
          ("GenMuon"+name, "invMass", 2000, 0, 200, ""),
          ("GenMuon"+name, "logInvMass", 1000, -1, 2, ""),
          ("GenMuon"+name, "deltaR", 1000, 0, 10, ""),
          ("GenMuon"+name, "absCollinearityAngle", 500, 0, 5, ""),
          ("GenMuon"+name, "absPtLxyDPhi1", 500, 0, 5, ""),
          ("GenMuon"+name, "absPtLxyDPhi2", 500, 0, 5, ""),
          ("GenMuon"+name, "logLxy", 2000, -10, 10, ""),
      )

      for matchingMethod in self.muonMatchingParams:
        params += (

            ("GenMuonFromALP1", "LooseMuons"+matchingMethod+"MatchMinDR", 1000, 0, 10, ""),
            ("GenMuonFromALP1", "LooseMuons"+matchingMethod+"MatchMinDPhi", 1000, 0, 10, ""),
            ("GenMuonFromALP1", "LooseMuons"+matchingMethod+"MatchMinDEta", 1000, 0, 10, ""),
            ("GenMuonFromALP2", "LooseMuons"+matchingMethod+"MatchMinDR", 1000, 0, 10, ""),
            ("GenMuonFromALP2", "LooseMuons"+matchingMethod+"MatchMinDPhi", 1000, 0, 10, ""),
            ("GenMuonFromALP2", "LooseMuons"+matchingMethod+"MatchMinDEta", 1000, 0, 10, ""),
            ("GenMuonFromW", "LooseMuons"+matchingMethod+"MatchMinDR", 1000, 0, 10, ""),
            ("GenMuonFromW", "LooseMuons"+matchingMethod+"MatchMinDPhi", 1000, 0, 10, ""),
            ("GenMuonFromW", "LooseMuons"+matchingMethod+"MatchMinDEta", 1000, 0, 10, ""),
            ("Event", "nLooseMuonsFromALP"+matchingMethod+"MatchVertex", 50, 0, 50, ""),
        )

      for name in ["FromALP", "FromALPmindPhi2", "NotFromALP"]:
        params += (
            ("Event", "nGenDimuon"+name, 50, 0, 50, ""),
            ("GenDimuon"+name, "invMass", 2000, 0, 200, ""),
            ("GenDimuon"+name, "logInvMass", 1000, -1, 2, ""),
            ("GenDimuon"+name, "deltaR", 1000, 0, 10, ""),
            ("GenDimuon"+name, "absCollinearityAngle", 500, 0, 5, ""),
            ("GenDimuon"+name, "absPtLxyDPhi1", 500, 0, 5, ""),
            ("GenDimuon"+name, "absPtLxyDPhi2", 500, 0, 5, ""),
            ("GenDimuon"+name, "Lxy", 10000, 0, 1000, ""),
            ("GenDimuon"+name, "logLxy", 2000, -10, 10, ""),
            ("GenDimuon"+name, "properLxy", 10000, 0, 1000, ""),
        )

    return tuple(params)

  def get_2D_params(self):
    params = []

    for collection in self.muonVertexCollections:

      names = (
          self.__insert_into_name(collection, "FromALP"),
          self.__insert_into_name(collection, "NotFromALP"),
          self.__insert_into_name(collection, "NonResonant"),
          self.__insert_into_name(collection, "ResonancesNotFromALP"),
          self.__insert_into_name(collection, "NonresonancesNotFromALP"),
      )

      for name in names:
        params += (
            (name+"_Lxy_nTrackerLayers1", 500, 0, 1000, 50, 0, 50, ""),
            (name+"_Lxy_nTrackerLayers2", 500, 0, 1000, 50, 0, 50, ""),
            (name+"_Lxy_maxTrackerLayers", 500, 0, 1000, 50, 0, 50, ""),
            (name+"_Lxy_3Dangle", 500, 0, 1000, 400, -10, 10, ""),
            (name+"_Lxy_cos3Dangle", 500, 0, 1000, 400, -2, 2, ""),
        )

    return tuple(params)

  def get_trigger_params(self):
    params = []

    for name in ["NoExtra", "SingleMuon", "DoubleMuon"]:
      params += (
          ("Event", "n"+name+"TriggerGenMuonFromALP", 50, 0, 50, ""),
          (name+"TriggerGenMuonFromALP", "pt1", 2000, 0, 1000, ""),
          (name+"TriggerGenMuonFromALP", "pt2", 2000, 0, 1000, ""),
          (name+"TriggerGenMuonFromALP", "leadingPt", 2000, 0, 1000, ""),
          (name+"TriggerGenMuonFromALP", "subleadingPt", 2000, 0, 1000, ""),
      )

    return tuple(params)

  def get_abcd_params(self):
    ABCD_variables = {
      "Lxy": (100, 0, 1000),
      "LxySignificance": (100, 0, 100),
      "absCollinearityAngle": (100, 0, 2), 
      "3Dangle": (100, 0, pi),
      
      "logLxy": (100, -2, 3),
      "logLxySignificance": (100, -2, 2),
      "logAbsCollinearityAngle": (100, -5, 1), 
      "log3Dangle": (100, -3, 1),
    }

    params = []

    for variable_1, (nBins_1, xMin_1, xMax_1) in ABCD_variables.items():
      for variable_2, (nBins_2, xMin_2, xMax_2) in ABCD_variables.items():
        if variable_1 == variable_2:
          continue
        params.append((f"{variable_2}_vs_{variable_1}", nBins_1, xMin_1, xMax_1, nBins_2, xMin_2, xMax_2, ""))
    
    return tuple(params)

  def get_matching_params(self):
    params = []
    
    for name in ["MatchLoose", "MatchLooseDSA", "DRMatchLoose", "OuterDRMatchLoose"]:
      params += (
        ("Event", "nSegment"+name+"Muons"         , 50    , 0     , 50    , ""  ),
        ("Segment"+name+"Muons", "genMinDR"       , 1000  , 0     , 10    , ""  ),
        ("Segment"+name+"Muons", "genMinDRidx"    , 100   , 0     , 100   , ""  ),
        ("Segment"+name+"Muons", "nSegments"      , 50    , 0     , 50    , ""  ),
        ("Segment"+name+"Muons", "matchingRatio"  , 600   , 0     , 2     , ""  ),
        ("Segment"+name+"Muons", "maxMatches"     , 50    , 0     , 50    , ""  ),
        ("Segment"+name+"Muons", "muonMatchIdx"   , 50    , 0     , 50    , ""  ),
        ("Segment"+name+"Muons", "pt"             , 2000  , 0     , 1000  , ""  ),
        ("Segment"+name+"Muons", "eta"            , 300   , -3    , 3     , ""  ),
        ("Segment"+name+"Muons", "phi"            , 300   , -3    , 3     , ""  ),
        ("Segment"+name+"Muons", "dxyPVTraj"      , 20000 , -2000 , 2000  , ""  ),
        ("Segment"+name+"Muons", "dxyPVTrajSig"   , 10000 , 0     , 2000  , ""  ),
        ("Segment"+name+"Muons", "ip3DPVSigned"   , 20000 , -2000 , 2000  , ""  ),
        ("Segment"+name+"Muons", "ip3DPVSignedSig", 10000 , 0     , 2000  , ""  ),
      )
    
    params += (
      ("LooseDSAMuons"  , "nSegments"             , 50    , 0     , 50    , ""  ),
      ("LooseDSAMuons"  , "muonMatch1"            , 50    , 0     , 50    , ""  ),
      ("LooseDSAMuons"  , "muonMatch2"            , 50    , 0     , 50    , ""  ),
      ("LooseDSAMuons"  , "matchRatio1"           , 600   , 0     , 2     , ""  ),
      ("LooseDSAMuons"  , "matchRatio2"           , 600   , 0     , 2     , ""  ),
      ("LooseDSAMuons"  , "PATOuterDR"            , 1000  , 0     , 10    , ""  ),
      ("LooseDSAMuons"  , "PATProxDR"             , 1000  , 0     , 10    , ""  ),
      ("LooseDSAMuons"  , "PATDR"                 , 1000  , 0     , 10    , ""  ),
    )
    
    return tuple(params)

  def get_2D_matching_params(self):
    params = ( 
      ("LooseDSAMuons_muonMatch1_nSegments",               50  , 0    , 50, 50  , 0    , 50   , ""  ),
      ("LooseDSAMuons_muonMatch2_nSegments",               50  , 0    , 50, 50  , 0    , 50   , ""  ),

      ("SegmentMatchLooseMuons_LooseDSAMuons_genMinDR",    1000 , 0    , 10  , 1000 , 0    , 10   , ""  ),
      ("SegmentMatchLooseMuons_LooseDSAMuons_genMinDRidx", 100  , 0    , 100 , 100  , 0    , 100  , ""  ),
      ("SegmentMatchLooseMuons_LooseDSAMuons_eta",         60   , -3   , 3   , 60   , -3   , 3    , ""  ),
      ("SegmentMatchLooseMuons_LooseDSAMuons_phi",         60   , -3   , 3   , 60   , -3   , 3    , ""  ),
      ("SegmentMatchLooseMuons_LooseDSAMuons_outerEta",    60   , -3   , 3   , 60   , -3   , 3    , ""  ),
      ("SegmentMatchLooseMuons_LooseDSAMuons_outerPhi",    60   , -3   , 3   , 60   , -3   , 3    , ""  ),

      ("SegmentMatchLooseMuons_eta_outerEta",              60   , -3   , 3   , 60   , -3   , 3    , ""  ),
      ("SegmentMatchLooseMuons_phi_outerPhi",              60   , -3   , 3   , 60   , -3   , 3    , ""  ),
      ("SegmentMatchLooseDSAMuons_eta_outerEta",           60   , -3   , 3   , 60   , -3   , 3    , ""  ),
      ("SegmentMatchLooseDSAMuons_phi_outerPhi",           60   , -3   , 3   , 60   , -3   , 3    , ""  ),
    )
    
    return tuple(params)

  def __insert_into_name(self, collection, to_insert):
    if "_" in collection:
      return collection.rsplit("_", 1)[0] + to_insert + "_" + collection.rsplit("_", 1)[1]

    return collection + to_insert
