# good object definitions for SR
SRDimuonsCuts = {
    # For different dimuon categories in order: PAT-PAT,PAT-DSA,DSA-DSA
    "maxChargeProduct": [-0.1, -0.1, -0.1],
    # SR mass cut
    "maxInvariantMass": [70.0, 70.0, 70.0],
    "minInvariantMass": [0.0, 0.0, 0.0],
    "minJpsiMass": [2.9, 2.9, 2.9],
    "maxJpsiMass": [3.3, 3.3, 3.3],
    "minpsiMass": [3.5, 3.5, 3.5],
    "maxpsiMass": [3.86, 3.86, 3.86],
    "maxDeltaEta": [0.1, 0.1, 0.1],  # for barrel muon studies
    "maxDCA": [9999.0, 2.0, 2.0],
    "maxChi2": [3.0, 3.0, 3.0],
    "maxHitsInFrontOfVertex": [3.0, 6.0, 9999.0],
    "maxCollinearityAngle": [2.0, 2.0, 2.0],
    "maxpTLxyDPhi": [9999.0, 2.9, 9999.0],
    "maxPFRelIso": [0.25, 0.25, 9999.0],
    # No cuts:
    "maxdisplacedTrackIso03Dimuon": [9999.0, 9999.0, 9999.0],  # used 0.025 before but now using PRFRelIso instead
    "maxDR": [9999.0, 9999.0, 9999.0],
    "maxDEta": [9999.0, 9999.0, 9999.0],
    "maxDPhi": [9999.0, 9999.0, 9999.0],
    "minLxy": [0.0, 0.0, 0.0],
    "maxDeltaPixelHits": [9999.0, 9999.0, 9999.0],
}

SRDimuonNoIsosCuts = SRDimuonsCuts

SRDimuonsDSAChi2DCADPhiCuts = {
    # For different dimuon categories in order: PAT-PAT,PAT-DSA,DSA-DSA
    "maxChargeProduct": [-0.1, -0.1, -0.1],
    # SR mass cut
    "maxInvariantMass": [70.0, 70.0, 70.0],
    "minInvariantMass": [0.0, 0.0, 0.0],
    "minJpsiMass": [2.9, 2.9, 2.9],
    "maxJpsiMass": [3.3, 3.3, 3.3],
    "minpsiMass": [3.5, 3.5, 3.5],
    "maxpsiMass": [3.86, 3.86, 3.86],
    "maxDeltaEta": [0.1, 0.1, 0.1],  # for barrel muon studies
    "maxDCA": [9999.0, 2.0, 2.0],
    "maxChi2": [3.0, 3.0, 3.0],
    "maxHitsInFrontOfVertex": [3.0, 6.0, 9999.0],
    "maxCollinearityAngle": [2.0, 2.0, 2.0],
    "maxpTLxyDPhi": [9999.0, 2.9, 0.4],
    "maxPFRelIso": [0.25, 0.25, 9999.0],
    "applyChi2DCA": [0.0, 0.0, 1.0], # apply linear cut for logNormChi2 > 2logDCA - 1.5
    # No cuts:
    "maxdisplacedTrackIso03Dimuon": [9999.0, 9999.0, 9999.0],  # used 0.025 before but now using PRFRelIso instead
    "maxDR": [9999.0, 9999.0, 9999.0],
    "maxDEta": [9999.0, 9999.0, 9999.0],
    "maxDPhi": [9999.0, 9999.0, 9999.0],
    "minLxy": [0.0, 0.0, 0.0],
    "maxDeltaPixelHits": [9999.0, 9999.0, 9999.0],
}

JPsiDimuonsDSAChi2DCADPhiCuts = {
    # For different dimuon categories in order: PAT-PAT,PAT-DSA,DSA-DSA
    "maxChargeProduct": [-0.1, -0.1, -0.1],
    # J/Psi mass cut
    "maxInvariantMass": [3.2, 3.2, 3.2],
    "minInvariantMass": [3.0, 3.0, 3.0],
    "maxDCA": [9999.0, 2.0, 2.0],
    "maxChi2": [3.0, 3.0, 3.0],
    "maxHitsInFrontOfVertex": [3.0, 6.0, 9999.0],
    "maxCollinearityAngle": [2.0, 2.0, 2.0],
    "maxpTLxyDPhi": [9999.0, 2.9, 0.4],
    "maxPFRelIso": [0.25, 0.25, 9999.0],
    "applyChi2DCA": [0.0, 0.0, 1.0], # apply linear cut for logNormChi2 > 2logDCA - 1.5
    # No cuts:
    "minJpsiMass": [9999.0, 9999.0, 9999.0],
    "maxJpsiMass": [0.0, 0.0, 0.0],
    "minpsiMass": [9999.0, 9999.0, 9999.0],
    "maxpsiMass": [0.0, 0.0, 0.0],
    "maxdisplacedTrackIso03Dimuon": [9999.0, 9999.0, 9999.0],  # used 0.025 before but now using PRFRelIso instead
    "maxDR": [9999.0, 9999.0, 9999.0],
    "maxDEta": [9999.0, 9999.0, 9999.0],
    "maxDPhi": [9999.0, 9999.0, 9999.0],
    "minLxy": [0.0, 0.0, 0.0],
    "maxDeltaPixelHits": [9999.0, 9999.0, 9999.0],
}

JPsiDimuonsCuts = {
    # For different dimuon categories in order: PAT-PAT,PAT-DSA,DSA-DSA
    "maxChargeProduct": [-0.1, -0.1, -0.1],
    # J/Psi mass cut
    "maxInvariantMass": [3.2, 3.2, 3.2],
    "minInvariantMass": [3.0, 3.0, 3.0],
    "maxDCA": [9999.0, 2.0, 2.0],
    "maxChi2": [3.0, 3.0, 3.0],
    "maxHitsInFrontOfVertex": [3.0, 6.0, 9999.0],
    "maxCollinearityAngle": [2.0, 2.0, 2.0],
    "maxpTLxyDPhi": [9999.0, 2.9, 9999.0],
    "maxPFRelIso": [0.25, 0.25, 9999.0],
    # No cuts:
    "minJpsiMass": [9999.0, 9999.0, 9999.0],
    "maxJpsiMass": [0.0, 0.0, 0.0],
    "minpsiMass": [9999.0, 9999.0, 9999.0],
    "maxpsiMass": [0.0, 0.0, 0.0],
    "maxdisplacedTrackIso03Dimuon": [9999.0, 9999.0, 9999.0],  # used 0.025 before but now using PRFRelIso instead
    "maxDR": [9999.0, 9999.0, 9999.0],
    "maxDEta": [9999.0, 9999.0, 9999.0],
    "maxDPhi": [9999.0, 9999.0, 9999.0],
    "minLxy": [0.0, 0.0, 0.0],
    "maxDeltaPixelHits": [9999.0, 9999.0, 9999.0],
}

# good object definitions for ALP in a narrow mass window (2 GeV)
AlpDimuonsCuts = {
    # For different dimuon categories in order: PAT-PAT,PAT-DSA,DSA-DSA
    "maxChargeProduct": [-0.1, -0.1, -0.1],
    # J/Psi mass cut
    "maxInvariantMass": [2.5, 2.5, 2.5],
    "minInvariantMass": [1.5, 1.5, 1.5],
    "maxDCA": [9999.0, 2.0, 2.0],
    "maxChi2": [3.0, 3.0, 3.0],
    "maxHitsInFrontOfVertex": [3.0, 6.0, 9999.0],
    "maxCollinearityAngle": [2.0, 2.0, 2.0],
    "maxpTLxyDPhi": [9999.0, 2.9, 9999.0],
    "maxPFRelIso": [0.25, 0.25, 9999.0],
    # No cuts:
    "minJpsiMass": [9999.0, 9999.0, 9999.0],
    "maxJpsiMass": [0.0, 0.0, 0.0],
    "minpsiMass": [9999.0, 9999.0, 9999.0],
    "maxpsiMass": [0.0, 0.0, 0.0],
    "maxdisplacedTrackIso03Dimuon": [9999.0, 9999.0, 9999.0],  # used 0.025 before but now using PRFRelIso instead
    "maxDR": [9999.0, 9999.0, 9999.0],
    "maxDEta": [9999.0, 9999.0, 9999.0],
    "maxDPhi": [9999.0, 9999.0, 9999.0],
    "minLxy": [0.0, 0.0, 0.0],
    "maxDeltaPixelHits": [9999.0, 9999.0, 9999.0],
}

JPsiDimuonIsosCuts = JPsiDimuonsCuts

# good object definitions for ttZ CR
ZDimuonsCuts = {
    # For different dimuon categories in order: PAT-PAT,PAT-DSA,DSA-DSA
    "maxChargeProduct": [-0.1, -0.1, -0.1],
    # Z mass cut
    "maxInvariantMass": [110.0, 110.0, 110.0],
    "minInvariantMass": [70.0, 70.0, 70.0],
    "minJpsiMass": [9999.0, 9999.0, 9999.0],
    "maxJpsiMass": [0.0, 0.0, 0.0],
    "minpsiMass": [9999.0, 9999.0, 9999.0],
    "maxpsiMass": [0.0, 0.0, 0.0],
    "maxDCA": [9999.0, 2.0, 2.0],
    "maxChi2": [3.0, 3.0, 3.0],
    "maxHitsInFrontOfVertex": [3.0, 6.0, 9999.0],
    "maxCollinearityAngle": [2.0, 2.0, 2.0],
    "maxpTLxyDPhi": [9999.0, 2.9, 9999.0],
    "maxPFRelIso": [0.25, 0.25, 9999.0],
    # No cuts:
    "maxdisplacedTrackIso03Dimuon": [9999.0, 9999.0, 9999.0],  # used 0.025 before but now using PRFRelIso instead
    "maxDR": [9999.0, 9999.0, 9999.0],
    "maxDEta": [9999.0, 9999.0, 9999.0],
    "maxDPhi": [9999.0, 9999.0, 9999.0],
    "minLxy": [0.0, 0.0, 0.0],
    "maxDeltaPixelHits": [9999.0, 9999.0, 9999.0],
}
