# good object definitions
SRDimuonVertexBaseCuts = {
  "maxDCA": 15.0,
  "maxChargeProduct": -0.1,
  ## SR mass cut
  "maxInvariantMass": 70.0,
  "minInvariantMass": 0.0,
  "minJpsiMass": 2.9,
  "maxJpsiMass": 3.3,
  "minpsiMass": 3.5,
  "maxpsiMass": 3.86,
  "maxDeltaEta": 0.1,  # for barrel muon studies
}
SRDimuonVertexPATCuts = {
  "maxDCA": 9999.0,
  "maxChi2": 3.0,
  "maxHitsInFrontOfVertex": 3.0,
  "maxCollinearityAngle": 2.0,
  "maxPFRelIso": 0.25,
  # No cuts:
  "maxdisplacedTrackIso03Dimuon": 9999.0, # used 0.025 before but now using PRFRelIso instead
  "maxDR": 9999.0, 
  "maxDEta": 9999.0,
  "maxDPhi": 9999.0,
  "maxpTLxyDPhi": 9999.0,
  "minLxy": 0.0,
  "maxDeltaPixelHits": 9999.0,
}
SRDimuonVertexPATDSACuts = {
  "maxDCA": 2.0,
  "maxChi2": 3.0,
  "maxHitsInFrontOfVertex": 6.0,
  "maxCollinearityAngle": 2.0,
  "maxpTLxyDPhi": 2.9,
  "maxPFRelIso": 0.25,
    # No cuts:
  "maxdisplacedTrackIso03Dimuon": 9999.0, # used 0.025 before but now using PRFRelIso instead
  "maxDR": 9999.0,
  "maxDEta": 9999.0,
  "maxDPhi": 9999.0,
  "minLxy": 0.0,
  "maxDeltaPixelHits": 9999.0,
}
SRDimuonVertexDSACuts = {
  "maxDCA": 2.0,
  "maxChi2": 3.0,
  "maxCollinearityAngle": 2.0,
  # No cuts:
  "maxdisplacedTrackIso03Dimuon": 9999.0, # used 0.025 before but now using PRFRelIso instead
  "maxDR": 9999.0, 
  "maxPFRelIso": 9999.0, 
  "maxOuterDEta": 9999.0,
  "maxOuterDPhi": 9999.0,
  "maxpTLxyDPhi": 9999.0,
  "minLxy": 0.0,
  "maxDeltaPixelHits": 9999.0,
}

# good object definitions
JPsiDimuonVertexBaseCuts = {
  "maxDCA": 15.0,
  "maxChargeProduct": -0.1,
  ## JPsi CR cut
  "maxInvariantMass": 3.3,
  "minInvariantMass": 2.9,
  "minJpsiMass": 9999.0,
  "maxJpsiMass": 0.0,
  "minpsiMass": 9999.0,
  "maxpsiMass": 0.0,
}
JPsiDimuonVertexPATCuts = {
  "maxDCA": 9999.0,
  "maxChi2": 3.0,
  "maxHitsInFrontOfVertex": 3.0,
  "maxDeltaPixelHits": 3.0,
  "maxCollinearityAngle": 2.0,
  # No cuts:
  "maxDR": 9999.0, # no cut
  "maxdisplacedTrackIso03Dimuon": 9999.0,
  "maxPFRelIso": 9999.0,
  "maxDEta": 9999.0,
  "maxDPhi": 9999.0,
  "maxpTLxyDPhi": 9999.0,
  "minLxy": 0.0,
}
JPsiDimuonVertexPATDSACuts = {
  "maxDCA": 2.0,
  "maxChi2": 3.0,
  "maxHitsInFrontOfVertex": 3.0,
  "maxCollinearityAngle": 2.0,
  "maxpTLxyDPhi": 2.9,
  # No cuts:
  "maxDR": 9999.0, 
  "maxdisplacedTrackIso03Dimuon": 9999.0, 
  "maxPFRelIso": 999.0,
  "maxDEta": 9999.0,
  "maxDPhi": 9999.0,
  "minLxy": 0.0,
}
JPsiDimuonVertexDSACuts = {
  "maxDCA": 2.0,
  "maxChi2": 3.0,
  "maxCollinearityAngle": 2.0,
  # No cuts:
  "maxDR": 9999.0,
  "maxdisplacedTrackIso03Dimuon": 9999.0, 
  "maxPFRelIso": 9999.0,
  "maxOuterDEta": 9999.0,
  "maxOuterDPhi": 9999.0,
  "maxpTLxyDPhi": 9999.0,
  "minLxy": 0.0,
}
