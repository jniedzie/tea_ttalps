import copy

# good object definitions for SR
SRDimuonsCuts = {
    # For different dimuon categories in order: PAT-PAT,PAT-DSA,DSA-DSA
    "maxBaseDCA": [15.0, 15.0, 15.0],
    "maxChargeProduct": [-0.1, -0.1, -0.1],
    "minChargeProduct": [-9999.0, -9999.0, -9999.0],
    # SR mass cut
    "maxInvariantMass": [70.0, 70.0, 70.0],
    "minInvariantMass": [0.0, 0.0, 0.0],
    "minJpsiMass": [2.9, 2.9, 2.4],
    "maxJpsiMass": [3.9, 3.9, 3.9],
    "maxDCA": [2.0, 2.0, 2.0],
    "maxChi2": [3.0, 3.0, 3.0],
    "maxCollinearityAngle": [0.5, 0.5, 0.5],
    "maxPFRelIso": [0.25, 0.25, 9999.0],
    "applyChi2DCA": [0.0, 1.0, 1.0], # apply linear cut for logNormChi2 > 2logDCA - 1.5
    "minDR": [0.0, 0.05, 0.0],
    # No cuts:
    # "minCos3Dangle": [-0.8, -0.8, -0.8],
    "maxDisplTrkIso": [9999.0, 9999.0, 9999.0],
    "minpsiMass": [9999.0, 9999.0, 9999.0],
    "maxpsiMass": [0.0, 0.0, 0.0],
    "maxHitsInFrontOfVertex": [9999.0, 9999.0, 9999.0],
    "maxpTLxyDPhi": [9999.0, 9999.0, 9999.0],
    "maxdisplacedTrackIso03Dimuon": [9999.0, 9999.0, 9999.0],  # used 0.025 before but now using PRFRelIso instead
    "maxDR": [9999.0, 9999.0, 9999.0],
    "maxDEta": [9999.0, 9999.0, 9999.0],
    "maxDeltaEta": [9999.0, 9999.0, 9999.0],  # for barrel muon studies
    "maxDPhi": [9999.0, 9999.0, 9999.0],
    "minLxy": [0.0, 0.0, 0.0],
    "maxDeltaPixelHits": [9999.0, 9999.0, 9999.0],
}

# For N-2 plots
SRDimuonsNoChi2Cuts = copy.deepcopy(SRDimuonsCuts)
SRDimuonsNoChi2Cuts["maxChi2"] = [9999.0, 9999.0, 9999.0]
SRDimuonsNoChi2Cuts["applyChi2DCA"] = [0.0, 0.0, 0.0]

# With cut on hits in front of vertex - for comparisons
SRDimuonsHitsInFrontOfVertexCuts = copy.deepcopy(SRDimuonsCuts)
SRDimuonsHitsInFrontOfVertexCuts["maxHitsInFrontOfVertex"] = [3.0, 6.0, 9999.0]

# With cut on pTLxyDPhi - for comparisons
SRDimuonsDPhiBetweenMuonpTAndLxyCuts = copy.deepcopy(SRDimuonsCuts)
SRDimuonsDPhiBetweenMuonpTAndLxyCuts["maxpTLxyDPhi"] = [0.5, 0.5, 0.5]

SRDimuonsNoPATIsoCuts = copy.deepcopy(SRDimuonsCuts)
SRDimuonsNoPATIsoCuts["maxPFRelIso"] = [9999.0, 0.25, 9999.0]

JPsiDimuonsCuts = {
    # For different dimuon categories in order: PAT-PAT,PAT-DSA,DSA-DSA
    "maxBaseDCA": [15.0, 15.0, 15.0],
    "maxChargeProduct": [-0.1, -0.1, -0.1],
    "minChargeProduct": [-9999.0, -9999.0, -9999.0],
    # J/Psi mass cut
    "maxInvariantMass": [3.2, 3.5, 3.9],
    "minInvariantMass": [3.0, 2.9, 2.4],
    "maxDCA": [2.0, 2.0, 2.0],
    "maxChi2": [3.0, 3.0, 3.0],
    "maxCollinearityAngle": [0.5, 0.5, 0.5],
    "applyChi2DCA": [0.0, 1.0, 1.0], # apply linear cut for logNormChi2 > 2logDCA - 1.5
    # No cuts:
    # "minCos3Dangle": [-0.8, -0.8, -0.8],
    "maxpTLxyDPhi": [9999.0, 9999.0, 9999.0],
    "maxHitsInFrontOfVertex": [9999.0, 9999.0, 9999.0],
    "minJpsiMass": [9999.0, 9999.0, 9999.0],
    "maxJpsiMass": [0.0, 0.0, 0.0],
    "minpsiMass": [9999.0, 9999.0, 9999.0],
    "maxpsiMass": [0.0, 0.0, 0.0],
    "maxPFRelIso": [9999.0, 9999.0, 9999.0],
    "maxDR": [9999.0, 9999.0, 9999.0],
    "maxDEta": [9999.0, 9999.0, 9999.0],
    "maxDPhi": [9999.0, 9999.0, 9999.0],
    "minLxy": [0.0, 0.0, 0.0],
    "maxDeltaPixelHits": [9999.0, 9999.0, 9999.0],
}

JPsiDimuonsNoChi2Cuts = copy.deepcopy(JPsiDimuonsCuts)
JPsiDimuonsNoChi2Cuts["maxChi2"] = [9999.0, 9999.0, 9999.0]
JPsiDimuonsNoChi2Cuts["applyChi2DCA"] = [0.0, 0.0, 0.0]

JPsiDimuonsPatDSACuts = copy.deepcopy(JPsiDimuonsCuts)

SSDimuonsCuts = copy.deepcopy(SRDimuonsCuts)
SSDimuonsCuts["maxChargeProduct"] = [9999.0, 9999.0, 9999.0]
SSDimuonsCuts["minChargeProduct"] = [0.1, 0.1, 0.1]
