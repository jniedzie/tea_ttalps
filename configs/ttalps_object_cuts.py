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
  ## No mass cuts
  # "maxInvariantMass": 99999.0,
  # "minJpsiMass": 99999.0,
  # "maxJpsiMass": 0.0,
  # "minpsiMass": 99999.0,
  # "maxpsiMass": 0.0,
  "maxDeltaEta": 0.1,
}
SRDimuonVertexPATCuts = {
  "maxDCA": 9999.0,
  "maxChi2": 3.0,
  "maxHitsInFrontOfVertex": 3.0,
  "maxCollinearityAngle": 2.0,
  # "maxdisplacedTrackIso03Dimuon": 9999.0, # no cut
  "maxdisplacedTrackIso03Dimuon": 0.025, # testing cut
  "maxPFRelIso": 0.25,
  "maxDR": 9999.0, # no cut
  # "maxDR": 0.2,
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
  # "maxdisplacedTrackIso03Dimuon": 9999.0, # no cut
  "maxdisplacedTrackIso03Dimuon": 0.025, # testing cut
  "maxPFRelIso": 0.25,
  "maxDR": 9999.0, # no cut
  # "maxDR": 0.4,
  "maxDEta": 9999.0,
  "maxDPhi": 9999.0,
  "minLxy": 0.0,
  "maxDeltaPixelHits": 9999.0,
}
SRDimuonVertexDSACuts = {
  "maxDCA": 2.0,
  "maxChi2": 3.0,
  "maxCollinearityAngle": 2.0,
  "maxdisplacedTrackIso03Dimuon": 9999.0, # no cut
  "maxDR": 9999.0, # no cut
  # "maxDR": 0.5,
  "maxPFRelIso": 9999.0, # no cut
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
  "maxDR": 9999.0, # no cut
  # "maxDR": 0.2, # tesing cut
  "maxCollinearityAngle": 2.0,
  # "maxdisplacedTrackIso03Dimuon": 9999.0, # no cut
  # "maxdisplacedTrackIso03Dimuon": 0.075, # testing cut
  # "maxdisplacedTrackIso03Dimuon": 0.025, # testing cut
  # "maxPFRelIso": 0.25,
  "maxDEta": 9999.0,
  "maxDPhi": 9999.0,
  "maxpTLxyDPhi": 9999.0,
  "minLxy": 0.0,
}
JPsiDimuonVertexPATDSACuts = {
  "maxDCA": 2.0,
  "maxChi2": 3.0,
  "maxHitsInFrontOfVertex": 3.0,
  "maxDR": 9999.0, # no cut
  # "maxDR": 0.4, # tesing cut
  "maxCollinearityAngle": 2.0,
  "maxpTLxyDPhi": 2.9,
  # "maxdisplacedTrackIso03Dimuon": 9999.0, # no cut
  # "maxdisplacedTrackIso03Dimuon": 0.075, # testing cut
  # "maxdisplacedTrackIso03Dimuon": 0.025, # testing cut
  # "maxPFRelIso": 0.25,
  "maxDEta": 9999.0,
  "maxDPhi": 9999.0,
  "minLxy": 0.0,
}
JPsiDimuonVertexDSACuts = {
  "maxDCA": 2.0,
  "maxChi2": 3.0,
  "maxDR": 9999.0, # no cut
  # "maxDR": 0.5, # tesing cut
  "maxCollinearityAngle": 2.0,
  # "maxdisplacedTrackIso03Dimuon": 9999.0, # no cut
  # "maxdisplacedTrackIso03Dimuon": 0.075, # testing cut
  # "maxdisplacedTrackIso03Dimuon": 0.025, # testing cut
  # "maxPFRelIso": 0.25,
  "maxOuterDEta": 9999.0,
  "maxOuterDPhi": 9999.0,
  "maxpTLxyDPhi": 9999.0,
  "minLxy": 0.0,
}
