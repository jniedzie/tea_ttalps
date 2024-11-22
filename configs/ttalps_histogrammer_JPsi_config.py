from scale_factors_config import *
from ttalps_extra_collections import extraEventCollections
from ttalps_object_selections import *

nEvents = -1
printEveryNevents = 10000

runDefaultHistograms = True
runCustomTTAlpsHistograms = False
runTriggerHistograms = False
runPileupHistograms = False

# LLPNanoAODHistograms: 
#  - muonMatchingParams loose muons 
#  - muonMatchingParams loose muon vertex
#  - extra muon vertex collections
runLLPNanoAODHistograms = True
runLLPNanoAOD2DHistograms = False
runDimuonNminus1Histograms = False
runMuonMatchingHistograms = False
runGenMuonHistograms = False
runLLPNanoAODVertexHistograms = False

runBestDimuonHistograms = True
nonIsolatedLooseMuons = True
objectSelection = "JPsi"

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)
specialBranchSizes = {}
# redirector = "xrootd-cms.infn.it"

pileupScaleFactorsPath = "/nfs/dust/cms/user/jniedzie/ttalps_cms/pileup_scale_factors.root"
pileupScaleFactorsHistName = "pileup_scale_factors"

applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
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
)

histParams = (
#  collection         variable                      bins   xmin   xmax    dir
  ("Event"          , "normCheck"                 , 1     , 0   , 1     , ""  ),
)
histParams2D = ()

####  LLPnanoAOD Histograms  #### 
LLPNanoAOD_defaultHistParams = ()
LLPNanoAOD_histParams = ()
LLPNanoAOD_histParams2D = ()

muonVertexCollectionCategories = ["_PatDSA", "_DSA", "_Pat"]
muonCollectionCategories = ["", "DSA", "PAT"]
muonCollectionNames = []

muonVertexCollectionNames = ["BaseLooseMuonsVertex", "BaseLooseDimuonsVertex", "BestLooseMuonsVertex", "BestLooseDimuonsVertex", "GoodBestLooseDimuonsVertex"]
for matchingMethod, param in muonMatchingParams.items():
  for category in muonCollectionCategories:
    muonCollectionName = "Loose"+category+"Muons"+matchingMethod+"Match"
    muonCollectionNames.append(muonCollectionName)
  muonVertexCollectionName = "LooseMuonsVertex"+matchingMethod+"Match"
  muonVertexCollectionNames.append(muonVertexCollectionName)

muonVertexNminus1CollectionNames = ["GoodBestVertexNminus1All", "GoodBestVertexNminus1AllVxy", "GoodBestVertexNminus1DR", "GoodBestVertexNminus1Iso", "GoodBestVertexNminus1Collinearity", "GoodBestVertexNminus1Chi2", "GoodBestVertexNminus1DCA", "GoodBestVertexNminus1DPhiMuonpTLxy", "GoodBestVertexNminus1HitsInFrontOfVertex", "GoodBestVertexNminus1InvMass", "GoodBestVertexNminus1Charge"]
if runDimuonNminus1Histograms:
  muonVertexCollectionNames += muonVertexNminus1CollectionNames

for muonCollectionName in muonCollectionNames:
  LLPNanoAOD_histParams += (
    ("Event"      , "n"+muonCollectionName    , 50    , 0     , 50    , ""  ),
    (muonCollectionName  , "pt"               , 2000  , 0     , 1000  , ""  ),
    (muonCollectionName  , "eta"              , 300   , -3    , 3     , ""  ),
    (muonCollectionName  , "phi"              , 300   , -3    , 3     , ""  ),
    (muonCollectionName  , "dxy"              , 20000  , -2000    , 2000   , ""  ),
    (muonCollectionName  , "dxyPVTraj"        , 20000  , -2000    , 2000   , ""  ),
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
  )

for collectionName in muonVertexCollectionNames:
  LLPNanoAOD_histParams += (
    ("Event"       , "n"+collectionName       , 50     , 0      , 50     , ""  ),
  )
  for category in muonVertexCollectionCategories:
    muonVertexCollectionName = collectionName + category
    LLPNanoAOD_histParams += (
      ("Event"       , "n"+muonVertexCollectionName       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "normChi2"              , 50000  , 0      , 50     , ""  ),
      (muonVertexCollectionName , "vxy"                   , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxySigma"              , 10000  , 0      , 100    , ""  ),
      (muonVertexCollectionName , "vxySignificance"       , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxySignificanceV2"     , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dR"                    , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "proxDR"                , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "outerDR"               , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "dEta"                  , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "dPhi"                  , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "outerDEta"             , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "outerDPhi"             , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "maxHitsInFrontOfVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "maxMissHitsAfterVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "dca"                   , 1000   , 0      , 20     , ""  ),
      (muonVertexCollectionName , "absCollinearityAngle"  , 500    , 0      , 5      , ""  ),
      (muonVertexCollectionName , "absPtLxyDPhi1"         , 500    , 0      , 5      , ""  ),
      (muonVertexCollectionName , "absPtLxyDPhi2"         , 500    , 0      , 5      , ""  ),
      (muonVertexCollectionName , "absPtPtMissDPhi"       , 500    , 0      , 5      , ""  ),
      (muonVertexCollectionName , "deltaPixelHits"        , 100    , -50    , 50     , ""  ),
      (muonVertexCollectionName , "nTrackerLayers1"       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "nTrackerLayers2"       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "invMass"               , 20000  , 0      , 200    , ""  ),
      (muonVertexCollectionName , "OSinvMass"             , 20000  , 0      , 200    , ""  ),
      (muonVertexCollectionName , "SSinvMass"             , 20000  , 0      , 200    , ""  ),
      (muonVertexCollectionName , "pt"                    , 2000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "nSegments1"            , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "nSegments2"            , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "nSegmentsSum"          , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "chargeProduct"         , 4      , -2     , 2      , ""  ),
      (muonVertexCollectionName , "leadingPt"             , 2000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "subleadingPt"          , 2000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dxyPVTraj1"            , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dxyPVTraj2"            , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "minDxyPVTraj"          , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "maxDxyPVTraj"          , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dxyPVTrajSig1"         , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dxyPVTrajSig2"         , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "minDxyPVTrajSig"       , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "maxDxyPVTrajSig"       , 1000   , 0      , 1000   , ""  ),
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
    )
    LLPNanoAOD_histParams2D += (
    #  collection + variables                           binsx   xmin  xmax binsy ymin   ymax   name
      (muonVertexCollectionName+"_vxySigma_vxy",                1000, 0    , 10,   1000, 0    , 1000 , ""  ),
      (muonVertexCollectionName+"_vxySigma_vxySignificance",    1000, 0    , 50,   1000, 0    , 1000 , ""  ),
      (muonVertexCollectionName+"_vxySignificance_vxy",         1000, 0    , 1000, 1000, 0    , 1000 , ""  ),
      (muonVertexCollectionName+"_normChi2_vxy",                1000, 0    , 10,   1000, 0    , 1000 , ""  ),
      (muonVertexCollectionName+"_absCollinearityAngle_invMass",  500 , 0  , 5   ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_nSegmentsSum_invMass"        ,  50  , 0  , 50  ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_chargeProduct_invMass"       ,  4   , -2 , 2   ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_dEta_invMass"                ,  500 , 0  , 10  ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_outerDEta_invMass"           ,  500 , 0  , 10  ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_dR_invMass"                  ,  500 , 0  , 10  ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_outerDR_invMass"             ,  500 , 0  , 10  ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_dca_normChi2"                ,  1000, 0  , 20  ,  5000, 0  , 50 , ""  ),
      (muonVertexCollectionName+"_Lxy_nTrackerLayers1"         ,  1000, 0  , 1000,  50  , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_Lxy_nTrackerLayers2"         ,  1000, 0  , 1000,  50  , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_Lxy_maxTrackerLayers"        ,  1000, 0  , 1000,  50  , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_displacedTrackIso03Dimuon1_invMass"             ,  500 , 0  , 10  ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_displacedTrackIso03Dimuon2_invMass"             ,  500 , 0  , 10  ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_displacedTrackIso04Dimuon1_invMass"             ,  500 , 0  , 10  ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_displacedTrackIso04Dimuon2_invMass"             ,  500 , 0  , 10  ,  700 , 0  , 70 , ""  ),
      (muonVertexCollectionName+"_dEta_displacedTrackIso03Dimuon1"                ,  500 , 0  , 10  ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_outerDEta_displacedTrackIso03Dimuon1"           ,  500 , 0  , 10  ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_dR_displacedTrackIso03Dimuon1"                  ,  500 , 0  , 10  ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_outerDR_displacedTrackIso03Dimuon1"             ,  500 , 0  , 10  ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_dEta_absCollinearityAngle"                      ,  500 , 0  , 10  ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_outerDEta_absCollinearityAngle"                 ,  500 , 0  , 10  ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_dR_absCollinearityAngle"                        ,  500 , 0  , 10  ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_outerDR_absCollinearityAngle"                   ,  500 , 0  , 10  ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_proxDR_absCollinearityAngle"                   ,  500 , 0  , 10  ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_absCollinearityAngle_displacedTrackIso03Dimuon1",  500 , 0  , 5   ,  500 , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_absCollinearityAngle_Lxy"                       ,  500 , 0  , 5   , 1000 , 0  ,1000, ""  ),
      (muonVertexCollectionName+"_absCollinearityAngle_normChi2"                  ,  500 , 0  , 5   , 1000 , 0  ,1000, ""  ),
      (muonVertexCollectionName+"_absCollinearityAngle_chargeProduct"             ,  500 , 0  , 5   ,   10 , -5 ,  5 , ""  ),
    )

if runLLPNanoAODHistograms:
  histParams = histParams + LLPNanoAOD_defaultHistParams
  histParams = histParams + LLPNanoAOD_histParams
if runLLPNanoAOD2DHistograms:
  histParams2D = histParams2D + LLPNanoAOD_histParams2D
  