from scale_factors_config import *
from ttalps_extra_collections import *
from ttalps_object_cuts import *
from math import pi

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
extraEventCollections = get_extra_event_collections(year)
scaleFactors = get_scale_factors(year)

nEvents = -1
printEveryNevents = 10000

runDefaultHistograms = True
runLLPTriggerHistograms = False
runPileupHistograms = False

# LLPNanoAODHistograms: 
#  - muonMatchingParams loose muons 
#  - muonMatchingParams loose muon vertex
#  - extra muon vertex collections
runLLPNanoAODHistograms = False

runMuonMatchingHistograms = False
runGenMuonHistograms = False  # can only be run on signal samples
runGenMuonVertexCollectionHistograms = True

runABCDHistograms = False
abcdCollection = "BestPFIsoDimuonVertex"
# abcdCollection = "BestDimuonVertex"

# dimuonSelection is the name of the selection in ttalps_object_cuts
dimuonSelection = "SRDimuonVertex"

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

specialBranchSizes = {
  "Proton_multiRP": "nProton_multiRP",
  "Proton_singleRP": "nProton_singleRP",
}
# redirector = "xrootd-cms.infn.it"

pileupScaleFactorsPath = "/data/dust/user/jniedzie/ttalps_cms/pileup_scale_factors.root"
pileupScaleFactorsHistName = "pileup_scale_factors"

applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
  "jetID": False,
}

# For the signal histogramming all given mathcing methods are applied separately to histograms
# More than one given method will not affect the other histograms
# Matching methods implemented are:
# "Segment" : max matching ratio (eg. 2.0f/3.0f)
# "DR" : max Delta R (eg. 0.1)
# "OuterDR" : max Delta R (eg. 0.1)
# "ProxDR" : max Delta R (eg. 0.1)
muonMatchingParams = {
    "Segment" : 2.0/3.0,
    # "DR" : 0.1
    # "OuterDR" : 0.1
    # "ProxDR" : 0.1
}

defaultHistParams = (
#  collection             variable               bins    xmin    xmax    dir
  ("Event"              , "MET_pt"              , 1000  , 0      , 1000  , ""  ),
  ("Event"              , "PV_npvs"             , 300   , 0      , 300   , ""  ),
  ("Event"              , "PV_npvsGood"         , 300   , 0      , 300   , ""  ),
  ("Event"              , "PV_x"                , 200   , -100   , 100   , ""  ),
  ("Event"              , "PV_y"                , 200   , -100   , 100   , ""  ),
  ("Event"              , "PV_z"                , 200   , -100   , 100   , ""  ),
)

histParams = (
#  collection         variable                      bins   xmin   xmax    dir
  ("Event"          , "normCheck"                 , 1     , 0   , 1     , ""  ),
)
histParams2D = ()

####  LLPnanoAOD Histograms  #### 
LLPNanoAOD_defaultHistParams = ()
LLPNanoAOD_histParams = ()

muonVertexCollectionCategories = ["_PatDSA", "_DSA", "_Pat"]
allMuonVertexCollectionCategories = ["", "_PatDSA", "_DSA", "_Pat"]
muonCollectionCategories = ["", "DSA", "PAT"]
muonCollectionNames = []

# Note: only the first "Best" dimuon collection will be used for passedDimuonCuts!
muonVertexCollections = {
  "GoodPFIsoDimuonVertex" : ["InvariantMassCut", "ChargeCut", "HitsInFrontOfVertexCut", "DPhiBetweenMuonpTAndLxyCut", "DCACut", "CollinearityAngleCut", "Chi2Cut", "PFRelIsolationCut"],
  "BestDimuonVertex" :      ["InvariantMassCut", "ChargeCut", "HitsInFrontOfVertexCut", "DPhiBetweenMuonpTAndLxyCut", "DCACut", "CollinearityAngleCut", "Chi2Cut", "BestDimuonVertex"],
  "BestPFIsoDimuonVertex" : ["InvariantMassCut", "ChargeCut", "HitsInFrontOfVertexCut", "DPhiBetweenMuonpTAndLxyCut", "DCACut", "CollinearityAngleCut", "Chi2Cut", "PFRelIsolationCut", "BestDimuonVertex"],
}
muonVertexCollectionNames = [collectionName for collectionName in muonVertexCollections.keys()]
# N-1 collections need to be defined above
muonVertexNminus1Collections = [
  "GoodPFIsoDimuonVertex",
  "BestDimuonVertex",
  "BestPFIsoDimuonVertex",
]

for matchingMethod, param in muonMatchingParams.items():
  for category in muonCollectionCategories:
    muonCollectionName = "Loose"+category+"Muons"+matchingMethod+"Match"
    muonCollectionNames.append(muonCollectionName)
  muonVertexCollectionName = "LooseMuonsVertex"+matchingMethod+"Match"
  muonVertexCollectionNames.append(muonVertexCollectionName)

####  Muon Histograms  ####
for muonCollectionName in muonCollectionNames:
  LLPNanoAOD_histParams += (
    ("Event"      , "n"+muonCollectionName    , 50    , 0     , 50    , ""  ),
    (muonCollectionName  , "pt"               , 2000  , 0     , 1000  , ""  ),
    (muonCollectionName  , "eta"              , 300   , -3    , 3     , ""  ),
    (muonCollectionName  , "phi"              , 300   , -3    , 3     , ""  ),
    (muonCollectionName  , "dxy"              , 20000  , -2000    , 2000   , ""  ),
    (muonCollectionName  , "absDxyPVTraj"     , 10000  , 0        , 2000   , ""  ),
    (muonCollectionName  , "dxyPVTrajErr"     , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName  , "dxyPVTrajSig"     , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName  , "ip3DPVSigned"     , 20000  , -2000    , 2000   , ""  ),
    (muonCollectionName  , "ip3DPVSignedErr"  , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName  , "ip3DPVSignedSig"  , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName  , "minDeltaR"        , 1000   , 0    , 10     , ""  ),
    (muonCollectionName  , "minOuterDeltaR"   , 1000   , 0    , 10     , ""  ),
    (muonCollectionName  , "minProxDeltaR"    , 1000   , 0    , 10     , ""  ),
    (muonCollectionName  , "pfRelIso04all"    , 800    , 0    , 20     , ""  ),
    (muonCollectionName  , "tkRelIso"         , 800    , 0    , 20     , ""  ),
    (muonCollectionName  , "isPAT"            , 10     , 0    , 10     , ""  ),
    (muonCollectionName  , "isTight"          , 10     , 0    , 10     , ""  ),
  )

####  Muon Vertex Histograms  ####
for collectionName in muonVertexCollectionNames:
  LLPNanoAOD_histParams += (
    ("Event"       , "n"+collectionName       , 50     , 0      , 50     , ""  ),
    (collectionName , "normChi2"              , 50000  , 0      , 50     , ""  ),
    (collectionName , "Lxy"                   , 10000  , 0      , 1000   , ""  ),
    (collectionName , "logLxy"                , 2000   , -10    , 10     , ""  ),
    (collectionName , "dca"                   , 1000   , 0      , 20     , ""  ),
    (collectionName , "absCollinearityAngle"  , 500    , 0      , 5      , ""  ),
    (collectionName , "invMass"               , 2000   , 0      , 200    , ""  ),
    (collectionName , "logInvMass"            , 1000   , -1     , 2      , ""  ),
    (collectionName , "pt"                    , 2000   , 0      , 1000   , ""  ),
    (collectionName , "chargeProduct"         , 4      , -2     , 2      , ""  ),
  )
  for category in muonVertexCollectionCategories:
    muonVertexCollectionName = collectionName + category
    LLPNanoAOD_histParams += (
      ("Event"       , "n"+muonVertexCollectionName       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "normChi2"              , 50000  , 0      , 50     , ""  ),
      (muonVertexCollectionName , "Lxy"                   , 10000  , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "logLxy"                , 2000   , -10    , 10     , ""  ),
      (muonVertexCollectionName , "LxySigma"              , 10000  , 0      , 100    , ""  ),
      (muonVertexCollectionName , "LxySignificance"       , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxy"                   , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxySigma"              , 10000  , 0      , 100    , ""  ),
      (muonVertexCollectionName , "vxySignificance"       , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dR"                    , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "proxDR"                , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "outerDR"               , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "dEta"                  , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "dPhi"                  , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "outerDEta"             , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "outerDPhi"             , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "maxHitsInFrontOfVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "sumHitsInFrontOfVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "maxMissHitsAfterVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVert1"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVert2"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "dca"                   , 1000   , 0      , 20     , ""  ),
      (muonVertexCollectionName , "absCollinearityAngle"  , 500    , 0      , 5      , ""  ),
      (muonVertexCollectionName , "absPtLxyDPhi1"         , 500    , 0      , 5      , ""  ),
      (muonVertexCollectionName , "absPtLxyDPhi2"         , 500    , 0      , 5      , ""  ),
      (muonVertexCollectionName , "invMass"               , 2000   , 0      , 200    , ""  ),
      (muonVertexCollectionName , "logInvMass"            , 1000   , -1     , 2      , ""  ),
      (muonVertexCollectionName , "pt"                    , 2000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "eta"                   , 500    , -10    , 10     , ""  ),
      (muonVertexCollectionName , "chargeProduct"         , 4      , -2     , 2      , ""  ),
      (muonVertexCollectionName , "leadingPt"             , 2000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dxyPVTraj1"            , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dxyPVTraj2"            , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dxyPVTrajSig1"         , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dxyPVTrajSig2"         , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "displacedTrackIso03Dimuon1"    , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "displacedTrackIso04Dimuon1"    , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "displacedTrackIso03Dimuon2"    , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "displacedTrackIso04Dimuon2"    , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "displacedTrackIso03Muon1"      , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "displacedTrackIso04Muon1"      , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "displacedTrackIso03Muon2"      , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "displacedTrackIso04Muon2"      , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "pfRelIso04all1"                , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "pfRelIso04all2"                , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "tkRelIsoMuon1"                 , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "tkRelIsoMuon2"                 , 800   , 0      , 20   , ""  ),
      (muonVertexCollectionName , "3Dangle"                         , 2000  , -10    , 10   , ""  ),
      (muonVertexCollectionName , "cos3Dangle"                      , 400   , -2     , 2    , ""  ),
      (muonVertexCollectionName , "deltaPixelHits"                , 50    , 0      , 50   , ""  ),
      (muonVertexCollectionName , "nSegments"                     , 50    , 0      , 50   , ""  ),
      (muonVertexCollectionName , "nSegments1"                    , 50    , 0      , 50   , ""  ),
      (muonVertexCollectionName , "nSegments2"                    , 50    , 0      , 50   , ""  ),
      (muonVertexCollectionName , "nDTHits"                       , 100   , 0      , 100  , ""  ),
      (muonVertexCollectionName , "nDTHits1"                      , 100   , 0      , 100  , ""  ),
      (muonVertexCollectionName , "nDTHits2"                      , 100   , 0      , 100  , ""  ),
      (muonVertexCollectionName , "nDTHitsBarrelOnly"             , 100   , 0      , 100  , ""  ),
      (muonVertexCollectionName , "nDTHits1BarrelOnly"            , 100   , 0      , 100  , ""  ),
      (muonVertexCollectionName , "nDTHits2BarrelOnly"            , 100   , 0      , 100  , ""  ),
    )


####  Muon Vertex N-1 Histograms  ####
for muonVertexNminus1Collection in muonVertexNminus1Collections:
  if not muonVertexNminus1Collection.startswith("Best"):
    continue
  muonVertexCollectionName = muonVertexNminus1Collection+"Nminus1"
  for category in allMuonVertexCollectionCategories:
    muonVertexCollectionName = muonVertexNminus1Collection+"Nminus1"+category
    LLPNanoAOD_histParams += (
      (muonVertexCollectionName , "invMass"                     , 2000   , 0      , 200   , ""  ),
      (muonVertexCollectionName , "logInvMass"                  , 1000   , -1     , 2     , ""  ),
      (muonVertexCollectionName , "chargeProduct"               , 4      , -2     , 2     , ""  ),
      (muonVertexCollectionName , "maxHitsInFrontOfVert"        , 100    , 0      , 100   , ""  ),
      (muonVertexCollectionName , "absPtLxyDPhi1"               , 500    , 0      , 5     , ""  ),
      (muonVertexCollectionName , "dca"                         , 1000   , 0      , 20    , ""  ),
      (muonVertexCollectionName , "absCollinearityAngle"        , 500    , 0      , 5     , ""  ),
      (muonVertexCollectionName , "normChi2"                    , 50000  , 0      , 50    , ""  ),
      (muonVertexCollectionName , "displacedTrackIso03Dimuon1"  , 800    , 0      , 20    , ""  ),
      (muonVertexCollectionName , "displacedTrackIso03Dimuon2"  , 800    , 0      , 20    , ""  ),
      (muonVertexCollectionName , "pfRelIso1"                   , 800    , 0      , 20    , ""  ),
      (muonVertexCollectionName , "pfRelIso2"                   , 800    , 0      , 20    , ""  ),
    )

####  Muon Matching Histograms  #### 
MuonMatching_histParams = (
  ("Event"             , "nSegmentMatchLooseMuons"          , 50    , 0     , 50    , ""  ),
  ("SegmentMatchLooseMuons"  , "genMinDR"                   , 1000  , 0     , 10    , ""  ),
  ("SegmentMatchLooseMuons"  , "genMinDRidx"                , 100   , 0     , 100   , ""  ),
  ("SegmentMatchLooseMuons"  , "nSegments"                  , 50    , 0     , 50    , ""  ),
  ("SegmentMatchLooseMuons"  , "matchingRatio"              , 600   , 0     , 2     , ""  ),
  ("SegmentMatchLooseMuons"  , "maxMatches"                 , 50    , 0     , 50    , ""  ),
  ("SegmentMatchLooseMuons"  , "muonMatchIdx"               , 50    , 0     , 50    , ""  ),
  ("SegmentMatchLooseMuons"  , "pt"                         , 2000  , 0     , 1000  , ""  ),
  ("SegmentMatchLooseMuons"  , "eta"                        , 300   , -3    , 3     , ""  ),
  ("SegmentMatchLooseMuons"  , "phi"                        , 300   , -3    , 3     , ""  ),
  ("SegmentMatchLooseMuons"  , "dxyPVTraj"                  , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseMuons"  , "dxyPVTrajSig"               , 10000  , 0    , 2000   , ""  ),
  ("SegmentMatchLooseMuons"  , "ip3DPVSigned"               , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseMuons"  , "ip3DPVSignedSig"            , 10000  , 0    , 2000   , ""  ),
  ("Event"             , "nSegmentMatchLooseDSAMuons"       , 50    , 0     , 50    , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "genMinDR"                , 1000  , 0     , 10    , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "genMinDRidx"             , 100   , 0     , 100   , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "pt"                      , 2000  , 0     , 1000  , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "eta"                     , 300   , -3    , 3     , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "phi"                     , 300   , -3    , 3     , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "dxyPVTraj"               , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "dxyPVTrajSig"            , 10000  , 0    , 2000   , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "ip3DPVSigned"            , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "ip3DPVSignedSig"         , 10000  , 0    , 2000   , ""  ),
  
  ("Event"             , "nSegmentDRMatchLooseMuons"        , 50    , 0     , 50    , ""  ),
  ("SegmentDRMatchLooseMuons"  , "nSegments"                 , 50    , 0     , 50    , ""  ),
  ("SegmentDRMatchLooseMuons"  , "matchingRatio"            , 600   , 0     , 2     , ""  ),
  ("SegmentDRMatchLooseMuons"  , "maxMatches"               , 50    , 0     , 50    , ""  ),
  ("SegmentDRMatchLooseMuons"  , "muonMatchIdx"               , 50    , 0     , 50    , ""  ),
  ("SegmentDRMatchLooseMuons"  , "pt"                       , 2000  , 0     , 1000  , ""  ),
  ("SegmentDRMatchLooseMuons"  , "eta"                      , 300   , -3    , 3     , ""  ),
  ("SegmentDRMatchLooseMuons"  , "phi"                      , 300   , -3    , 3     , ""  ),
  ("SegmentDRMatchLooseMuons"  , "dxyPVTraj"                , 20000  , -2000    , 2000   , ""  ),
  ("SegmentDRMatchLooseMuons"  , "dxyPVTrajSig"             , 10000  , 0    , 2000   , ""  ),
  ("SegmentDRMatchLooseMuons"  , "ip3DPVSigned"             , 20000  , -2000    , 2000   , ""  ),
  ("SegmentDRMatchLooseMuons"  , "ip3DPVSignedSig"          , 10000  , 0    , 2000   , ""  ),
  ("Event"             , "nSegmentOuterDRMatchLooseMuons"   , 50    , 0     , 50    , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "nSegments"           , 50    , 0     , 50    , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "matchingRatio"       , 600   , 0     , 2     , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "maxMatches"          , 50    , 0     , 50    , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "muonMatchIdx"               , 50    , 0     , 50    , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "eta"                 , 300   , -3    , 3     , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "phi"                 , 300   , -3    , 3     , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "dxyPVTraj"           , 20000  , -2000    , 2000   , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "dxyPVTrajSig"        , 10000  , 0    , 2000   , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "ip3DPVSigned"        , 20000  , -2000    , 2000   , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "ip3DPVSignedSig"     , 10000  , 0    , 2000   , ""  ),

  ("LooseDSAMuons"  , "nSegments"              , 50  , 0    , 50   , ""  ),
  ("LooseDSAMuons"  , "muonMatch1"             , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"  , "muonMatch2"             , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"  , "matchRatio1"            , 600   , 0     , 2     , ""  ),
  ("LooseDSAMuons"  , "matchRatio2"            , 600   , 0     , 2     , ""  ),

  ("LooseDSAMuons"  , "PATOuterDR"             , 1000  , 0     , 10    , ""  ),
  ("LooseDSAMuons"  , "PATProxDR"              , 1000  , 0     , 10    , ""  ),
  ("LooseDSAMuons"  , "PATDR"                  , 1000  , 0     , 10    , ""  ),
)
MuonMatching_histParams2D = ( 
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

####  Gen Muon Histograms  #### 
GenMuon_histParams = (
  ("Event"                     , "nGenMuonFromALP" , 50    , 0     , 50    , ""  ),
  ("GenMuonFromALP"            , "index1"          , 100   , 0     , 100   , ""  ),
  ("GenMuonFromALP"            , "index2"          , 100   , 0     , 100   , ""  ),
  ("GenMuonFromALP"            , "pt1"             , 4000  , 0     , 1000  , ""  ),
  ("GenMuonFromALP"            , "pt2"             , 4000  , 0     , 1000  , ""  ),
  ("GenMuonFromALP"            , "eta1"            , 300   , -3    , 3     , ""  ),
  ("GenMuonFromALP"            , "eta2"            , 300   , -3    , 3     , ""  ),
  ("GenMuonFromALP"            , "phi1"            , 300   , -3    , 3     , ""  ),
  ("GenMuonFromALP"            , "phi2"            , 300   , -3    , 3     , ""  ),
  ("GenMuonFromALP"            , "Lxy"             , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "Lxyz"            , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "properLxy"       , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "properLxyT"      , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "properLxyz"      , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "dxy1"            , 50000 , -5000 , 5000  , ""  ),
  ("GenMuonFromALP"            , "dxy2"            , 50000 , -5000 , 5000  , ""  ),
  ("GenMuonFromALP"            , "RecoMatch1MinDR"   , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromALP"            , "RecoMatch2MinDR"   , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromALP"            , "RecoMatch1MinDPhi" , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromALP"            , "RecoMatch2MinDPhi" , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromALP"            , "RecoMatch1MinDEta" , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromALP"            , "RecoMatch2MinDEta" , 1000  , 0     , 10    , ""  ),
  ("Event"                     , "nGenMuonFromW"     , 50    , 0     , 50    , ""  ),
  ("GenMuonFromW"              , "index1"            , 100   , 0     , 100   , ""  ),
  ("GenMuonFromW"              , "index2"            , 100   , 0     , 100   , ""  ),
  ("GenMuonFromW"              , "index3"            , 100   , 0     , 100   , ""  ),
  ("GenMuonFromW"              , "RecoMatch1MinDR"   , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromW"              , "RecoMatch2MinDR"   , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromW"              , "RecoMatch1MinDPhi" , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromW"              , "RecoMatch2MinDPhi" , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromW"              , "RecoMatch1MinDEta" , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromW"              , "RecoMatch2MinDEta" , 1000  , 0     , 10    , ""  ),
  ("Event"                     , "nGenALP"         , 50    , 0     , 50    , ""  ),
  ("GenALP"                    , "pdgId"           , 200   , -100  , 100   , ""  ),
  ("GenALP"                    , "pt"              , 4000  , 0     , 1000  , ""  ),
  ("GenALP"                    , "mass"            , 10000 , 0     , 100   , ""  ),
  ("GenALP"                    , "eta"             , 300   , -3    , 3     , ""  ),
  ("GenALP"                    , "phi"             , 300   , -3    , 3     , ""  ),
  ("LooseMuonsFromALPSegmentMatchVertex"         , "genPlaneAngle"   , 500   , 0      , 5     , ""  ),
  ("LooseMuonsFromALPSegmentMatchVertex"         , "recoPlaneAngle"  , 500   , 0      , 5     , ""  ),
  ("LooseMuonsFromALPSegmentMatchVertex"         , "etaSum"          , 700   , 0      , 7     , ""  ),
  ("LooseMuonsFromALPmaxdPhi2SegmentMatchVertex" , "genPlaneAngle"   , 500   , 0      , 5     , ""  ),
  ("LooseMuonsFromALPmaxdPhi2SegmentMatchVertex" , "recoPlaneAngle"  , 500   , 0      , 5     , ""  ),
  ("LooseMuonsFromALPmaxdPhi2SegmentMatchVertex" , "etaSum"          , 700   , 0      , 7     , ""  ),
  ("LooseMuonsFromALPmindPhi2SegmentMatchVertex" , "genPlaneAngle"   , 500   , 0      , 5     , ""  ),
  ("LooseMuonsFromALPmindPhi2SegmentMatchVertex" , "recoPlaneAngle"  , 500   , 0      , 5     , ""  ),
  ("LooseMuonsFromALPmindPhi2SegmentMatchVertex" , "etaSum"          , 700   , 0      , 7     , ""  ),
  ("LooseMuonsFromALPSegmentMatch"  , "hasLeadingMuon"     , 10    , 0     , 10    , ""  ),
  ("LooseMuonsFromALPSegmentMatch"  , "hmu_hasLeadingMuon" , 10    , 0     , 10    , ""  ),
  ("LooseMuonsFromWSegmentMatch"    , "hasLeadingMuon"     , 10    , 0     , 10    , ""  ),
  ("LooseMuonsFromWSegmentMatch"    , "hmu_hasLeadingMuon" , 10    , 0     , 10    , ""  ),
  ("Event"  , "nTightMuonsFromALPSegmentMatch"             , 50    , 0     , 50    , ""  ),
  ("Event"  , "nTightMuonsFromALPSegmentMatch_hmu"         , 50    , 0     , 50    , ""  ),
  ("TightMuonsFromALPSegmentMatch"  , "hasLeadingMuon"     , 10    , 0     , 10    , ""  ),
  ("TightMuonsFromALPSegmentMatch"  , "hmu_hasLeadingMuon" , 10    , 0     , 10    , ""  ),
  ("TightMuonsFromALPSegmentMatch"  , "index"              , 10    , 0     , 10    , ""  ),
  ("TightMuonsFromALPSegmentMatch"  , "hmu_index"          , 10    , 0     , 10    , ""  ),
  ("TightMuonsFromALPSegmentMatch"  , "pt"                 , 4000  , 0     , 1000  , ""  ),
  ("TightMuonsFromALPSegmentMatch"  , "hmu_pt"             , 4000  , 0     , 1000  , ""  ),
  ("Event"  , "nTightMuonsFromWSegmentMatch"               , 50    , 0     , 50    , ""  ),
  ("Event"  , "nTightMuonsFromWSegmentMatch_hmu"           , 50    , 0     , 50    , ""  ),
  ("TightMuonsFromWSegmentMatch"    , "hasLeadingMuon"     , 10    , 0     , 10    , ""  ),
  ("TightMuonsFromWSegmentMatch"    , "hmu_hasLeadingMuon" , 10    , 0     , 10    , ""  ),
  ("TightMuonsFromWSegmentMatch"    , "index"              , 10    , 0     , 10    , ""  ),
  ("TightMuonsFromWSegmentMatch"    , "hmu_index"          , 10    , 0     , 10    , ""  ),
  ("TightMuonsFromWSegmentMatch"    , "pt"                 , 4000  , 0     , 1000  , ""  ),
  ("TightMuonsFromWSegmentMatch"    , "hmu_pt"             , 4000  , 0     , 1000  , ""  ),
)

for i in range(1,6):
  GenMuon_histParams += (
    ("GenMuonFromALP"            , "motherID"+str(i)  , 10010 , -10   , 10000 , ""  ),
    ("GenMuonNotFromALP"         , "motherID"+str(i)  , 10010 , -10   , 10000 , ""  ),
    ("GenDimuonNotFromALP"       , "motherID1"+str(i) , 10010 , -10   , 10000 , ""  ),
    ("GenDimuonNotFromALP"       , "motherID2"+str(i) , 10010 , -10   , 10000 , ""  ), 
  )

GenMuon_histParams2D = ()

genDimuonCollectionNames = ["GenDimuonFromALP","GenDimuonFromALPmindPhi2","GenMuonNotFromALP","GenDimuonNotFromALP"]
genmuonCollectionNames = ["LooseMuonsFromALP","LooseMuonsFromALPmindPhi2","LooseMuonsNotFromALP", "LooseMuonsFromW"]
genmuonVertexCollectionNames = ["LooseMuonsFromALP","LooseMuonsFromALPmindPhi2","LooseMuonsNotFromALP", "LooseDimuonsNotFromALP", "LooseNonResonantDimuons", "LooseMuonsFromW"]

for genDimuonCollectionName in genDimuonCollectionNames:
  GenMuon_histParams += (
    ("Event"                   , "n"+genDimuonCollectionName   , 50    , 0     , 50    , ""  ),
    (genDimuonCollectionName   , "invMass"                     , 2000  , 0     , 200   , ""  ),
    (genDimuonCollectionName   , "logInvMass"                  , 1000  , -1    , 2     , ""  ),
    (genDimuonCollectionName   , "deltaR"                      , 1000  , 0     , 10    , ""  ),
    (genDimuonCollectionName   , "absCollinearityAngle"        , 500   , 0     , 5     , ""  ),
    (genDimuonCollectionName   , "absPtLxyDPhi1"               , 500   , 0     , 5     , ""  ),
    (genDimuonCollectionName   , "absPtLxyDPhi2"               , 500   , 0     , 5     , ""  ),
    (genDimuonCollectionName   , "Lxy"                         , 10000 , 0     , 1000  , ""  ),
    (genDimuonCollectionName   , "logLxy"                      , 2000  , -10   , 10    , ""  ),
    (genDimuonCollectionName   , "properLxy"                   , 10000 , 0     , 1000  , ""  ),
  )

####  Loose Muons Matched to Gen Muons Histograms  ####
for matchingMethod, param in muonMatchingParams.items():
  for genmuonCollectionName in genmuonCollectionNames:
    muonCollectionName = genmuonCollectionName+matchingMethod+"Match"
    GenMuon_histParams += (
      ("Event"      , "n"+muonCollectionName    , 50    , 0     , 50    , ""  ),
      (muonCollectionName  , "pt"               , 2000  , 0     , 1000  , ""  ),
      (muonCollectionName  , "eta"              , 300   , -3    , 3     , ""  ),
      (muonCollectionName  , "phi"              , 300   , -3    , 3     , ""  ),
      (muonCollectionName  , "dxy"              , 20000  , -2000    , 2000   , ""  ),
      (muonCollectionName  , "absDxyPVTraj"     , 10000  , 0        , 2000   , ""  ),
      (muonCollectionName  , "dxyPVTrajErr"     , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "dxyPVTrajSig"     , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "ip3DPVSigned"     , 20000  , -2000    , 2000   , ""  ),
      (muonCollectionName  , "ip3DPVSignedErr"  , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "ip3DPVSignedSig"  , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "minDeltaR"        , 1000   , 0    , 10     , ""  ),
      (muonCollectionName  , "minOuterDeltaR"   , 1000   , 0    , 10     , ""  ),
      (muonCollectionName  , "minProxDeltaR"    , 1000   , 0    , 10     , ""  ),
      (muonCollectionName  , "invMass"          , 2000   , 0    , 200    , ""  ),
      (muonCollectionName  , "logInvMass"       , 1000   , -1   , 2      , ""  ),
      (muonCollectionName  , "deltaR"           , 1000   , 0    , 10     , ""  ),
      (muonCollectionName  , "outerDeltaR"      , 1000   , 0    , 10     , ""  ),
      (muonCollectionName  , "genMuonMinDR1"    , 1000   , 0    , 10     , ""  ),
      (muonCollectionName  , "genMuonMinDR2"    , 1000   , 0    , 10     , ""  ),
      (muonCollectionName  , "pfRelIso04all"    , 800    , 0    , 20     , ""  ),
      (muonCollectionName  , "tkRelIso"         , 800    , 0    , 20     , ""  ),
      (muonCollectionName  , "isPAT"            , 10     , 0    , 10     , ""  ),
      (muonCollectionName  , "isTight"          , 10     , 0    , 10     , ""  ),
    )
  GenMuon_histParams += (
    ("GenMuonFromALP1"   , "LooseMuons"+matchingMethod+"MatchMinDR"    , 1000 , 0  , 10    , ""  ),
    ("GenMuonFromALP1"   , "LooseMuons"+matchingMethod+"MatchMinDPhi"  , 1000 , 0  , 10    , ""  ),
    ("GenMuonFromALP1"   , "LooseMuons"+matchingMethod+"MatchMinDEta"  , 1000 , 0  , 10    , ""  ),
    ("GenMuonFromALP2"   , "LooseMuons"+matchingMethod+"MatchMinDR"    , 1000 , 0  , 10    , ""  ),
    ("GenMuonFromALP2"   , "LooseMuons"+matchingMethod+"MatchMinDPhi"  , 1000 , 0  , 10    , ""  ),
    ("GenMuonFromALP2"   , "LooseMuons"+matchingMethod+"MatchMinDEta"  , 1000 , 0  , 10    , ""  ),
    ("GenMuonFromW"      , "LooseMuons"+matchingMethod+"MatchMinDR"    , 1000 , 0  , 10    , ""  ),
    ("GenMuonFromW"      , "LooseMuons"+matchingMethod+"MatchMinDPhi"  , 1000 , 0  , 10    , ""  ),
    ("GenMuonFromW"      , "LooseMuons"+matchingMethod+"MatchMinDEta"  , 1000 , 0  , 10    , ""  ),
    ("Event"       , "nLooseMuonsFromALP"+matchingMethod+"MatchVertex" , 50     , 0      , 50     , ""  ),
  )
  for genmuonVertexCollectionName in genmuonVertexCollectionNames:
    collectionName = genmuonVertexCollectionName+matchingMethod+"MatchVertex"
    GenMuon_histParams += (
      ("Event"       , "n"+collectionName       , 50     , 0      , 50     , ""  ),
      (collectionName , "normChi2"              , 50000  , 0      , 50     , ""  ),
      (collectionName , "Lxy"                   , 1000   , 0      , 1000   , ""  ),
      (collectionName , "logLxy"                , 2000   , -10    , 10     , ""  ),
      (collectionName , "dca"                   , 1000   , 0      , 20     , ""  ),
      (collectionName , "absCollinearityAngle"  , 500    , 0      , 5      , ""  ),
      (collectionName , "invMass"               , 2000   , 0      , 200    , ""  ),
      (collectionName , "logInvMass"            , 1000   , -1     , 2      , ""  ),
      (collectionName , "pt"                    , 2000   , 0      , 1000   , ""  ),
      (collectionName , "chargeProduct"         , 4      , -2     , 2      , ""  ),
    )
    for category in muonVertexCollectionCategories:
      muonVertexCollectionName = genmuonVertexCollectionName+matchingMethod+"MatchVertex"+category
      GenMuon_histParams += (
        ("Event"       , "n"+muonVertexCollectionName       , 50     , 0      , 50     , ""  ),
        (muonVertexCollectionName , "normChi2"              , 50000  , 0      , 50     , ""  ),
        (muonVertexCollectionName , "Lxy"                   , 1000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "logLxy"                , 2000   , -10    , 10     , ""  ),
        (muonVertexCollectionName , "LxySigma"              , 10000  , 0      , 100    , ""  ),
        (muonVertexCollectionName , "LxySignificance"       , 1000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "vxy"                   , 1000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "vxySigma"              , 10000  , 0      , 100    , ""  ),
        (muonVertexCollectionName , "vxySignificance"       , 1000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "dR"                    , 500    , 0      , 10     , ""  ),
        (muonVertexCollectionName , "proxDR"                , 500    , 0      , 10     , ""  ),
        (muonVertexCollectionName , "outerDR"               , 500    , 0      , 10     , ""  ),
        (muonVertexCollectionName , "eta"                   , 300    , -3     , 3      , ""  ),
        (muonVertexCollectionName , "dEta"                  , 500    , 0      , 10     , ""  ),
        (muonVertexCollectionName , "dPhi"                  , 500    , 0      , 10     , ""  ),
        (muonVertexCollectionName , "outerDEta"             , 500    , 0      , 10     , ""  ),
        (muonVertexCollectionName , "outerDPhi"             , 500    , 0      , 10     , ""  ),
        (muonVertexCollectionName , "maxHitsInFrontOfVert"  , 100    , 0      , 100    , ""  ),
        (muonVertexCollectionName , "hitsInFrontOfVert1"    , 100    , 0      , 100    , ""  ),
        (muonVertexCollectionName , "hitsInFrontOfVert2"    , 100    , 0      , 100    , ""  ),
        (muonVertexCollectionName , "dca"                   , 1000   , 0      , 20     , ""  ),
        (muonVertexCollectionName , "absCollinearityAngle"  , 500    , 0      , 5      , ""  ),
        (muonVertexCollectionName , "absPtLxyDPhi1"         , 500    , 0      , 5      , ""  ),
        (muonVertexCollectionName , "absPtLxyDPhi2"         , 500    , 0      , 5      , ""  ),
        (muonVertexCollectionName , "invMass"               , 2000   , 0      , 200    , ""  ),
        (muonVertexCollectionName , "logInvMass"            , 1000   , -1     , 2      , ""  ),
        (muonVertexCollectionName , "pt"                    , 2000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "chargeProduct"         , 4      , -2     , 2      , ""  ),
        (muonVertexCollectionName , "leadingPt"             , 2000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "dxyPVTraj1"            , 1000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "dxyPVTraj2"            , 1000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "dxyPVTrajSig1"         , 1000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "dxyPVTrajSig2"         , 1000   , 0      , 1000   , ""  ),
        (muonVertexCollectionName , "displacedTrackIso03Dimuon1"    , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "displacedTrackIso04Dimuon1"    , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "displacedTrackIso03Dimuon2"    , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "displacedTrackIso04Dimuon2"    , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "displacedTrackIso03Muon1"      , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "displacedTrackIso04Muon1"      , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "displacedTrackIso03Muon2"      , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "displacedTrackIso04Muon2"      , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "pfRelIso04all1"                , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "pfRelIso04all2"                , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "tkRelIsoMuon1"                 , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "tkRelIsoMuon2"                 , 800   , 0      , 20   , ""  ),
        (muonVertexCollectionName , "3Dangle"                         , 2000  , -10    , 10   , ""  ),
        (muonVertexCollectionName , "cos3Dangle"                      , 400   , -2     , 2    , ""  ),
        (muonVertexCollectionName , "deltaPixelHits"                , 50    , 0      , 50   , ""  ),
        (muonVertexCollectionName , "nSegments"                     , 50    , 0      , 50   , ""  ),
        (muonVertexCollectionName , "nSegments1"                    , 50    , 0      , 50   , ""  ),
        (muonVertexCollectionName , "nSegments2"                    , 50    , 0      , 50   , ""  ),
        (muonVertexCollectionName , "nDTHits"                       , 100   , 0      , 100  , ""  ),
        (muonVertexCollectionName , "nDTHits1"                      , 100   , 0      , 100  , ""  ),
        (muonVertexCollectionName , "nDTHits2"                      , 100   , 0      , 100  , ""  ),
        (muonVertexCollectionName , "nDTHitsBarrelOnly"             , 100   , 0      , 100  , ""  ),
        (muonVertexCollectionName , "nDTHits1BarrelOnly"            , 100   , 0      , 100  , ""  ),
        (muonVertexCollectionName , "nDTHits2BarrelOnly"            , 100   , 0      , 100  , ""  ),
      )
      GenMuon_histParams2D += (
        (muonVertexCollectionName+"_invMass_absCollinearityAngle",  2000, 0  , 200 ,  700 , 0  , 7  , ""  ),
        (muonVertexCollectionName+"_dca_normChi2"                ,  1000, 0  , 20  ,  5000, 0  , 50 , ""  ),
      )

####  Loose Muon Vertex to Gen Muons  ####
GenMuonVertexCollection_histParams = ()
GenMuonVertexCollection_histParams2D = ()
for muonVertexNminus1Collection in muonVertexNminus1Collections:
  ####  From ALP, From Resonance and From Non-Resonant  ####
  for category in muonVertexCollectionCategories:
    dimuonFromALPsCollectionName = muonVertexNminus1Collection+"FromALP"+category
    dimuonNotFromALPsVertexCollectionName = muonVertexNminus1Collection+"ResonancesNotFromALP"+category
    muonNotFromALPsVertexCollectionName = muonVertexNminus1Collection+"NonresonancesNotFromALP"+category
    GenMuonVertexCollection_histParams += (
      ("Event"  , "n"+dimuonFromALPsCollectionName                , 10     , 0    , 10    , ""  ),
      ("Event"  , "n"+dimuonNotFromALPsVertexCollectionName       , 10     , 0    , 10    , ""  ),
      ("Event"  , "n"+muonNotFromALPsVertexCollectionName         , 10     , 0    , 10    , ""  ),
      (dimuonFromALPsCollectionName          , "Lxy"              , 1000   , 0    , 1000  , ""  ),
      (dimuonNotFromALPsVertexCollectionName , "Lxy"              , 1000   , 0    , 1000  , ""  ),
      (muonNotFromALPsVertexCollectionName   , "Lxy"              , 1000   , 0    , 1000  , ""  ),
      (dimuonFromALPsCollectionName          , "logLxy"           , 100    , -2   , 3     , ""  ),
      (dimuonNotFromALPsVertexCollectionName , "logLxy"           , 100    , -2   , 3     , ""  ),
      (muonNotFromALPsVertexCollectionName   , "logLxy"           , 100    , -2   , 3     , ""  ),
      (dimuonFromALPsCollectionName          , "LxySignificance"  , 1000   , 0    , 1000  , ""  ),
      (dimuonNotFromALPsVertexCollectionName , "LxySignificance"  , 1000   , 0    , 1000  , ""  ),
      (muonNotFromALPsVertexCollectionName   , "LxySignificance"  , 1000   , 0    , 1000  , ""  ),
      (dimuonFromALPsCollectionName          , "logLxySignificance"  , 100   , -2    , 2  , ""  ),
      (dimuonNotFromALPsVertexCollectionName , "logLxySignificance"  , 100   , -2    , 2  , ""  ),
      (muonNotFromALPsVertexCollectionName   , "logLxySignificance"  , 100   , -2    , 2  , ""  ),
      (dimuonFromALPsCollectionName          , "3Dangle"            , 2000   , -10  , 10    , ""  ),
      (dimuonNotFromALPsVertexCollectionName , "3Dangle"            , 2000   , -10  , 10    , ""  ),
      (muonNotFromALPsVertexCollectionName   , "3Dangle"            , 2000   , -10  , 10    , ""  ),
      (dimuonFromALPsCollectionName          , "log3Dangle"         , 100    , -3   , 1     , ""  ),
      (dimuonNotFromALPsVertexCollectionName , "log3Dangle"         , 100    , -3   , 1     , ""  ),
      (muonNotFromALPsVertexCollectionName   , "log3Dangle"         , 100    , -3   , 1     , ""  ),
      (dimuonFromALPsCollectionName          , "cos3Dangle"         , 400    , -2   , 2     , ""  ),
      (dimuonNotFromALPsVertexCollectionName , "cos3Dangle"         , 400    , -2   , 2     , ""  ),
      (muonNotFromALPsVertexCollectionName   , "cos3Dangle"         , 400    , -2   , 2     , ""  ),
    )
    GenMuonVertexCollection_histParams2D += (
      (dimuonFromALPsCollectionName+"_Lxy_nTrackerLayers1"           , 500   , 0    , 1000  , 50   , 0    , 50  , ""  ),
      (dimuonNotFromALPsVertexCollectionName+"_Lxy_nTrackerLayers1"  , 500   , 0    , 1000  , 50   , 0    , 50  , ""  ),
      (muonNotFromALPsVertexCollectionName+"_Lxy_nTrackerLayers1"    , 500   , 0    , 1000  , 50   , 0    , 50  , ""  ),
      (dimuonFromALPsCollectionName+"_Lxy_nTrackerLayers2"           , 500   , 0    , 1000  , 50   , 0    , 50  , ""  ),
      (dimuonNotFromALPsVertexCollectionName+"_Lxy_nTrackerLayers2"  , 500   , 0    , 1000  , 50   , 0    , 50  , ""  ),
      (muonNotFromALPsVertexCollectionName+"_Lxy_nTrackerLayers2"    , 500   , 0    , 1000  , 50   , 0    , 50  , ""  ),
      (dimuonFromALPsCollectionName+"_Lxy_maxTrackerLayers"          , 500   , 0    , 1000  , 50   , 0    , 50  , ""  ),
      (dimuonNotFromALPsVertexCollectionName+"_Lxy_maxTrackerLayers" , 500   , 0    , 1000  , 50   , 0    , 50  , ""  ),
      (muonNotFromALPsVertexCollectionName+"_Lxy_maxTrackerLayers"   , 500   , 0    , 1000  , 50   , 0    , 50  , ""  ),
      (dimuonFromALPsCollectionName+"_log3Dangle_logLxySignificance"           , 100   , -3    , 1   , 100  , -2  , 2  , ""  ),
      (dimuonNotFromALPsVertexCollectionName+"_log3Dangle_logLxySignificance"  , 100   , -3    , 1   , 100  , -2  , 2  , ""  ),
      (muonNotFromALPsVertexCollectionName+"_log3Dangle_logLxySignificance"    , 100   , -3    , 1   , 100  , -2  , 2  , ""  ),
    )
    if muonVertexNminus1Collection.startswith("Best"):
      continue
    ####  N-1 Histograms  ####
    muonVertexCollectionName = muonVertexNminus1Collection+"FromALPNminus1"
    for category in allMuonVertexCollectionCategories:
      muonVertexCollectionName = muonVertexNminus1Collection+"FromALPNminus1"+category
      GenMuonVertexCollection_histParams += (
      (muonVertexCollectionName , "invMass"                     , 2000   , 0      , 200   , ""  ),
      (muonVertexCollectionName , "logInvMass"                  , 1000   , -1     , 2     , ""  ),
      (muonVertexCollectionName , "chargeProduct"               , 4      , -2     , 2     , ""  ),
      (muonVertexCollectionName , "maxHitsInFrontOfVert"        , 100    , 0      , 100   , ""  ),
      (muonVertexCollectionName , "absPtLxyDPhi1"  , 500        , 0      , 5     , ""  ),
      (muonVertexCollectionName , "dca"                         , 1000   , 0      , 20    , ""  ),
      (muonVertexCollectionName , "absCollinearityAngle"        , 500    , 0      , 5     , ""  ),
      (muonVertexCollectionName , "normChi2"                    , 50000  , 0      , 50    , ""  ),
      (muonVertexCollectionName , "displacedTrackIso03Dimuon1"  , 800    , 0      , 20    , ""  ),
      (muonVertexCollectionName , "displacedTrackIso03Dimuon2"  , 800    , 0      , 20    , ""  ),
      (muonVertexCollectionName , "pfRelIso1"                   , 800    , 0      , 20    , ""  ),
      (muonVertexCollectionName , "pfRelIso2"                   , 800    , 0      , 20    , ""  ),
    )

####  LLP Trigger Histograms  ####
LLPTrigger_histParams = (
  ("Event" , "nNoExtraTriggerGenMuonFromALP"              , 50     , 0      , 50     , ""  ),
  ("NoExtraTriggerGenMuonFromALP"    , "pt1"              , 2000   , 0      , 1000   , ""  ),
  ("NoExtraTriggerGenMuonFromALP"    , "pt2"              , 2000   , 0      , 1000   , ""  ),
  ("NoExtraTriggerGenMuonFromALP"    , "leadingPt"        , 2000   , 0      , 1000   , ""  ),
  ("NoExtraTriggerGenMuonFromALP"    , "subleadingPt"     , 2000   , 0      , 1000   , ""  ),
  ("Event" , "nSingleMuonTriggerGenMuonFromALP"           , 50     , 0      , 50     , ""  ),
  ("SingleMuonTriggerGenMuonFromALP" , "pt1"              , 2000   , 0      , 1000   , ""  ),
  ("SingleMuonTriggerGenMuonFromALP" , "pt2"              , 2000   , 0      , 1000   , ""  ),
  ("SingleMuonTriggerGenMuonFromALP" , "leadingPt"        , 2000   , 0      , 1000   , ""  ),
  ("SingleMuonTriggerGenMuonFromALP" , "subleadingPt"     , 2000   , 0      , 1000   , ""  ),
  ("Event" , "nDoubleMuonTriggerGenMuonFromALP"           , 50     , 0      , 50     , ""  ),
  ("DoubleMuonTriggerGenMuonFromALP" , "pt1"              , 2000   , 0      , 1000   , ""  ),
  ("DoubleMuonTriggerGenMuonFromALP" , "pt2"              , 2000   , 0      , 1000   , ""  ),
  ("DoubleMuonTriggerGenMuonFromALP" , "leadingPt"        , 2000   , 0      , 1000   , ""  ),
  ("DoubleMuonTriggerGenMuonFromALP" , "subleadingPt"     , 2000   , 0      , 1000   , ""  ),
)


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

ABCD_histParams2D = []

for variable_1, (nBins_1, xMin_1, xMax_1) in ABCD_variables.items():
  for variable_2, (nBins_2, xMin_2, xMax_2) in ABCD_variables.items():
    if variable_1 == variable_2:
      continue
    ABCD_histParams2D.append((f"{variable_2}_vs_{variable_1}", nBins_1, xMin_1, xMax_1, nBins_2, xMin_2, xMax_2, ""))


if runLLPNanoAODHistograms:
  histParams = histParams + LLPNanoAOD_defaultHistParams
  histParams = histParams + LLPNanoAOD_histParams
if runMuonMatchingHistograms:
  histParams = histParams + MuonMatching_histParams
  histParams2D = histParams2D + MuonMatching_histParams2D
if runGenMuonHistograms:
  histParams = histParams + GenMuon_histParams
  histParams2D = histParams2D + GenMuon_histParams2D
if runGenMuonVertexCollectionHistograms:
  histParams = histParams + GenMuonVertexCollection_histParams
  histParams2D = histParams2D + GenMuonVertexCollection_histParams2D
if runLLPTriggerHistograms:
  histParams = histParams + LLPTrigger_histParams
if runABCDHistograms:
  histParams2D = histParams2D + tuple(ABCD_histParams2D)
