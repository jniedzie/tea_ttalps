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
runGenMuonVertexCollectionHistograms = False  # can only be run on signal samples

runABCDHistograms = False
abcdCollection = "BestPFIsoDimuonVertex"

useLooseIsoPATMuons = False
# dimuonSelection is the name of the selection in ttalps_object_cuts
# dimuonSelection = "GoodDimuonVertex"
dimuonSelection = "SRDimuonVertex"

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)
# redirector = "xrootd-cms.infn.it"
specialBranchSizes = {
  "Proton_multiRP": "nProton_multiRP",
  "Proton_singleRP": "nProton_singleRP",
}

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
  ("Event"              , "PV_npvs"             , 300   , 0     , 300   , ""  ),
  ("Event"              , "PV_npvsGood"         , 300   , 0     , 300   , ""  ),
  ("Event"              , "MET_pt"              , 1000  , 0     , 1000  , ""  ),

  ("Event"              , "PV_x"                , 200   , -100   , 100   , ""  ),
  ("Event"              , "PV_y"                , 200   , -100   , 100   , ""  ),
  ("Event"              , "PV_z"                , 200   , -100   , 100   , ""  ),
  
  ("Event"              , "nJet"                , 50    , 0     , 50    , ""  ),
  ("Jet"                , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("Jet"                , "eta"                 , 100   , -2.5  , 2.5   , ""  ),
  ("Jet"                , "phi"                 , 100   , -2.5  , 2.5   , ""  ),
  ("Jet"                , "btagDeepB"           , 200   , -1    , 1     , ""  ),
  
  ("Event"              , "nGoodJets"           , 50    , 0     , 50    , ""  ),
  ("GoodJets"           , "pt"                  , 2000  , 0     , 2000  , ""  ),
  ("GoodJets"           , "eta"                 , 100   , -2.5  , 2.5   , ""  ),
  ("GoodJets"           , "phi"                 , 100   , -2.5  , 2.5   , ""  ),
  ("GoodJets"           , "btagDeepB"           , 200   , -1    , 1     , ""  ),
  ("GoodJets"           , "btagDeepFlavB"       , 200   , -1    , 1     , ""  ),
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
  "BestPFIsoDimuonVertex" : ["InvariantMassCut", "ChargeCut", "HitsInFrontOfVertexCut", "DPhiBetweenMuonpTAndLxyCut", "DCACut", "CollinearityAngleCut", "Chi2Cut", "PFRelIsolationCut", "BestDimuonVertex"],
}
muonVertexCollectionNames = [collectionName for collectionName in muonVertexCollections.keys()]
# N-1 collections need to be defined above
muonVertexNminus1Collections = [
  "GoodPFIsoDimuonVertex",
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
    (collectionName , "Lxy"                   , 1000   , 0      , 1000   , ""  ),
    (collectionName , "dca"                   , 1000   , 0      , 20     , ""  ),
    (collectionName , "absCollinearityAngle"  , 500    , 0      , 5      , ""  ),
    (collectionName , "invMass"               , 20000  , 0      , 200    , ""  ),
    (collectionName , "pt"                    , 2000   , 0      , 1000   , ""  ),
    (collectionName , "chargeProduct"         , 4      , -2     , 2      , ""  ),
  )
  for category in muonVertexCollectionCategories:
    muonVertexCollectionName = collectionName + category
    LLPNanoAOD_histParams += (
      ("Event"       , "n"+muonVertexCollectionName       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "normChi2"              , 50000  , 0      , 50     , ""  ),
      (muonVertexCollectionName , "Lxy"                   , 1000   , 0      , 1000   , ""  ),
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
      (muonVertexCollectionName , "invMass"               , 20000  , 0      , 200    , ""  ),
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

####  Muon Vertex N-1 Histograms  ####
for muonVertexNminus1Collection in muonVertexNminus1Collections:
  if not muonVertexNminus1Collection.startswith("Best"):
    continue
  muonVertexCollectionName = muonVertexNminus1Collection+"Nminus1"
  for category in allMuonVertexCollectionCategories:
    muonVertexCollectionName = muonVertexNminus1Collection+"Nminus1"+category
    LLPNanoAOD_histParams += (
      (muonVertexCollectionName , "invMass"                     , 20000  , 0      , 200   , ""  ),
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
if runABCDHistograms:
  histParams2D = histParams2D + tuple(ABCD_histParams2D)
