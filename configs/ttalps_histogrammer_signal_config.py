from scale_factors_config import *
from ttalps_extra_collections import extraEventCollections
from ttalps_signal_selections import *

nEvents = -1
printEveryNevents = 10000

runDefaultHistograms = True
runTriggerHistograms = False
runPileupHistograms = False
runLLPNanoAODHistograms = True
runMuonMatchingHistograms = False
runGenMuonHistograms = False

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
  
  ("Event"              , "nMuon"               , 50    , 0     , 50    , ""  ),
  ("Muon"               , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("Muon"               , "eta"                 , 300   , -3    , 3     , ""  ),
  ("Muon"               , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("Muon"               , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  
  ("Event"              , "nTightMuons"         , 50    , 0     , 50    , ""  ),
  ("TightMuons"         , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("TightMuons"         , "eta"                 , 300   , -3    , 3     , ""  ),
  ("TightMuons"         , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("TightMuons"         , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  ("TightMuons"         , "pfRelIso04_all"      , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "pfRelIso03_chg"      , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "pfRelIso03_all"      , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "tkRelIso"            , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "miniPFRelIso_chg"    , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "miniPFRelIso_all"    , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "jetRelIso"           , 2000  , -10   , 10    , ""  ),

  
  ("Event"              , "nLooseMuons"         , 50    , 0     , 50    , ""  ),
  ("LooseMuons"         , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("LooseMuons"         , "eta"                 , 300   , -3    , 3     , ""  ),
  ("LooseMuons"         , "phi"                 , 300   , -3    , 3     , ""  ),
  ("LooseMuons"         , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("LooseMuons"         , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  ("LooseMuons"         , "pfRelIso04_all"      , 2000  , -10   , 10    , ""  ),
  ("LooseMuons"         , "pfRelIso03_chg"      , 2000  , -10   , 10    , ""  ),
  ("LooseMuons"         , "pfRelIso03_all"      , 2000  , -10   , 10    , ""  ),
  ("LooseMuons"         , "tkRelIso"            , 2000  , -10   , 10    , ""  ),
  ("LooseMuons"         , "miniPFRelIso_chg"    , 2000  , -10   , 10    , ""  ),
  ("LooseMuons"         , "miniPFRelIso_all"    , 2000  , -10   , 10    , ""  ),
  ("LooseMuons"         , "jetRelIso"           , 2000  , -10   , 10    , ""  ),
  
  ("Event"              , "nElectron"           , 50    , 0     , 50    , ""  ),
  ("Electron"           , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("Electron"           , "eta"                 , 300   , -3    , 3     , ""  ),
  ("Electron"           , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("Electron"           , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  
  ("Event"              , "nLooseElectrons"     , 50    , 0     , 50    , ""  ),
  ("LooseElectrons"     , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("LooseElectrons"     , "eta"                 , 300   , -3    , 3     , ""  ),
  ("LooseElectrons"     , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("LooseElectrons"     , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  
  ("Event"              , "nJet"                , 50    , 0     , 50    , ""  ),
  ("Jet"                , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("Jet"                , "eta"                 , 300   , -3    , 3     , ""  ),
  ("Jet"                , "phi"                 , 300   , -3    , 3     , ""  ),
  ("Jet"                , "btagDeepB"           , 200   , -1    , 1     , ""  ),
  
  ("Event"              , "nGoodJets"           , 50    , 0     , 50    , ""  ),
  ("GoodJets"           , "pt"                  , 2000  , 0     , 2000  , ""  ),
  ("GoodJets"           , "eta"                 , 300   , -3    , 3     , ""  ),
  ("GoodJets"           , "phi"                 , 300   , -3    , 3     , ""  ),
  ("GoodJets"           , "btagDeepB"           , 200   , -1    , 1     , ""  ),
  ("GoodJets"           , "btagDeepFlavB"       , 200   , -1    , 1     , ""  ),
  
  ("Event"                    , "nGoodMediumBtaggedJets"    , 50    , 0     , 50    , ""  ),
  ("GoodMediumBtaggedJets"    , "pt"                  , 2000  , 0     , 2000  , ""  ),
  ("GoodMediumBtaggedJets"    , "eta"                 , 300   , -3    , 3     , ""  ),
  ("GoodMediumBtaggedJets"    , "phi"                 , 300   , -3    , 3     , ""  ),
  ("GoodMediumBtaggedJets"    , "btagDeepB"           , 200   , -1    , 1     , ""  ),
  ("GoodMediumBtaggedJets"    , "btagDeepFlavB"       , 200   , -1    , 1     , ""  ),
  
  ("Event"                    , "nGoodNonTightBtaggedJets" , 50    , 0     , 50    , ""  ),
  ("GoodNonTightBtaggedJets"  , "pt"                  , 2000  , 0     , 2000  , ""  ),
  ("GoodNonTightBtaggedJets"  , "eta"                 , 300   , -3    , 3     , ""  ),
  ("GoodNonTightBtaggedJets"  , "phi"                 , 300   , -3    , 3     , ""  ),
  ("GoodNonTightBtaggedJets"  , "btagDeepB"           , 200   , -1    , 1     , ""  ),
  ("GoodNonTightBtaggedJets"  , "btagDeepFlavB"       , 200   , -1    , 1     , ""  ),

)

LLPNanoAOD_defaultHistParams = (

  ("Muon"               , "idx"                 , 50    , 0     , 50    , ""  ),
  ("Muon"               , "dsaMatch1"           , 100   , 0     , 100   , ""  ),
  ("Muon"               , "dsaMatch1idx"        , 100   , 0     , 100   , ""  ),
  ("Muon"               , "dsaMatch2"           , 100   , 0     , 100   , ""  ),
  ("Muon"               , "dsaMatch2idx"        , 100   , 0     , 100   , ""  ),
  ("Muon"               , "dsaMatch3"           , 100   , 0     , 100   , ""  ),
  ("Muon"               , "dsaMatch3idx"        , 100   , 0     , 100   , ""  ),
  ("Muon"               , "dsaMatch4"           , 100   , 0     , 100   , ""  ),
  ("Muon"               , "dsaMatch4idx"        , 100   , 0     , 100   , ""  ),
  ("Muon"               , "dsaMatch5"           , 100   , 0     , 100   , ""  ),
  ("Muon"               , "dsaMatch5idx"        , 100   , 0     , 100   , ""  ),
  ("Muon"               , "outerEta"            , 300   , -3    , 3     , ""  ),
  ("Muon"               , "outerPhi"            , 300   , -3    , 3     , ""  ),

  ("LooseMuons"               , "idx"                 , 50    , 0     , 50    , ""  ),
  ("LooseMuons"               , "dzPV"                , 8000  , -1000 , 1000  , ""  ),
  ("LooseMuons"               , "dxyPVTraj"           , 8000  , -1000 , 1000  , ""  ),
  ("LooseMuons"               , "dxyPVSigned"         , 8000  , -1000 , 1000  , ""  ),
  ("LooseMuons"               , "ip3DPVSigned"        , 8000  , -1000 , 1000  , ""  ),
  # ("LooseMuons"               , "dxyBS"               , 8000  , -1000 , 1000  , ""  ),
  ("LooseMuons"               , "dzBS"                , 8000  , -1000 , 1000  , ""  ),
  ("LooseMuons"               , "dxyBSTraj"           , 8000  , -1000 , 1000  , ""  ),
  ("LooseMuons"               , "dxyBSSigned"         , 8000  , -1000 , 1000  , ""  ),
  ("LooseMuons"               , "ip3DBSSigned"        , 8000  , -1000 , 1000  , ""  ),
  ("LooseMuons"               , "dsaMatch1"           , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "dsaMatch1idx"        , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "dsaMatch2"           , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "dsaMatch2idx"        , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "dsaMatch3"           , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "dsaMatch3idx"        , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "dsaMatch4"           , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "dsaMatch4idx"        , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "dsaMatch5"           , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "dsaMatch5idx"        , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "outerEta"            , 300   , -3    , 3     , ""  ),
  ("LooseMuons"               , "outerPhi"            , 300   , -3    , 3     , ""  ),
  ("LooseMuons"               , "trkNumPlanes"        , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "trkNumHits"          , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "trkNumDTHits"        , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "trkNumCSCHits"       , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "trkNumPixelHits"     , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "trkNumTrkLayers"     , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "normChi2"            , 100   , 0     , 100   , ""  ),
  ("LooseMuons"               , "trkPt"               , 2000  , 0     , 1000  , ""  ),
  ("LooseMuons"               , "trkPtErr"            , 2000  , 0     , 1000  , ""  ),

  ("Event"              , "nDSAMuon"            , 50    , 0     , 50    , ""  ),
  ("DSAMuon"            , "idx"                 , 50    , 0     , 50    , ""  ),
  ("DSAMuon"            , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("DSAMuon"            , "eta"                 , 300   , -3    , 3     , ""  ),
  ("DSAMuon"            , "dxy"                 , 8000  , -1000 , 1000  , ""  ),
  ("DSAMuon"            , "dz"                  , 8000  , -1000 , 1000  , ""  ),
  ("DSAMuon"            , "muonMatch1"          , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "muonMatch1idx"       , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "muonMatch2"          , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "muonMatch2idx"       , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "muonMatch3"          , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "muonMatch3idx"       , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "muonMatch4"          , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "muonMatch4idx"       , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "muonMatch5"          , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "muonMatch5idx"       , 100   , 0     , 100   , ""  ),
  ("DSAMuon"            , "outerEta"            , 300   , -3    , 3     , ""  ),
  ("DSAMuon"            , "outerPhi"            , 300   , -3    , 3     , ""  ),
  ("DSAMuon"            , "displacedID"         , 50    , 0     , 50    , ""  ),

  ("Event"              , "nLooseDSAMuons"            , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"            , "idx"                 , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"            , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("LooseDSAMuons"            , "eta"                 , 300   , -3    , 3     , ""  ),
  ("LooseDSAMuons"            , "phi"                 , 300   , -3    , 3     , ""  ),
  ("LooseDSAMuons"            , "dxy"                 , 20000  , -2000    , 2000  , ""  ),
  ("LooseDSAMuons"            , "dz"                  , 20000  , -2000    , 2000  , ""  ),
  ("LooseDSAMuons"            , "idx"                 , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "dzPV"                , 20000  , -2000    , 2000  , ""  ),
  ("LooseDSAMuons"            , "dxyPVTraj"           , 20000  , -2000    , 2000  , ""  ),
  ("LooseDSAMuons"            , "dxyPVSigned"         , 10000  , 0    , 2000  , ""  ),
  ("LooseDSAMuons"            , "ip3DPVSigned"        , 20000  , -2000    , 2000  , ""  ),
  # ("LooseDSAMuons"            , "dxyBS"               , 10000  , 0    , 2000  , ""  ),
  ("LooseDSAMuons"            , "dxyBSTraj"           , 20000  , -2000    , 2000  , ""  ),
  ("LooseDSAMuons"            , "dxyBSSigned"         , 10000  , 0    , 2000  , ""  ),
  ("LooseDSAMuons"            , "ip3DBSSigned"        , 10000  , 0    , 2000  , ""  ),
  ("LooseDSAMuons"            , "muonMatch1"          , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "muonMatch1idx"       , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "muonMatch2"          , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "muonMatch2idx"       , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "muonMatch3"          , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "muonMatch3idx"       , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "muonMatch4"          , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "muonMatch4idx"       , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "muonMatch5"          , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "muonMatch5idx"       , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "outerEta"            , 300   , -3    , 3     , ""  ),
  ("LooseDSAMuons"            , "outerPhi"            , 300   , -3    , 3     , ""  ),
  ("LooseDSAMuons"            , "trkNumPlanes"        , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "trkNumHits"          , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "trkNumDTHits"        , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "trkNumCSCHits"       , 100   , 0     , 100   , ""  ),
  ("LooseDSAMuons"            , "displacedID"         , 50    , 0     , 50    , ""  ),

  ("Event"              , "nPatMuonVertex"      , 50    , 0     , 50    , ""  ),
  ("PatMuonVertex"      , "isValid"             , 10    , 0     , 10    , ""  ),
  ("PatMuonVertex"      , "dca"                 , 1000  , 0     , 20    , ""  ),
  ("PatMuonVertex"      , "dcaStatus"           , 10    , 0     , 10    , ""  ),
  ("PatMuonVertex"      , "chi2"                , 500   , 0     , 500   , ""  ),
  ("PatMuonVertex"      , "vxy"                 , 10000  , -1000  , 1000   , ""  ),
  ("PatMuonVertex"      , "vxySigma"            , 10000  , 0      , 100    , ""  ),
  ("PatMuonVertex"      , "vz"                  , 10000  , -1000  , 1000   , ""  ),
  ("PatMuonVertex"      , "dR"                  , 500   , 0     , 10    , ""  ),
  ("PatMuonVertex"      , "originalMuonIdx1"    , 100   , 0     , 100   , ""  ),
  ("PatMuonVertex"      , "originalMuonIdx2"    , 100   , 0     , 100   , ""  ),
  ("PatMuonVertex"      , "isDSAMuon1"          , 10    , 0     , 10    , ""  ),
  ("PatMuonVertex"      , "isDSAMuon2"          , 10    , 0     , 10    , ""  ),

  ("Event"              , "nPatDSAMuonVertex"   , 50    , 0     , 50    , ""  ),
  ("PatDSAMuonVertex"   , "isValid"             , 10    , 0     , 10    , ""  ),
  ("PatDSAMuonVertex"   , "dca"                 , 1000  , 0     , 20    , ""  ),
  ("PatDSAMuonVertex"   , "dcaStatus"           , 10    , 0     , 10    , ""  ),
  ("PatDSAMuonVertex"   , "chi2"                , 500   , 0     , 500   , ""  ),
  ("PatDSAMuonVertex"   , "vxy"                 , 10000  , -1000  , 1000   , ""  ),
  ("PatDSAMuonVertex"   , "vxySigma"            , 10000  , 0      , 100    , ""  ),
  ("PatDSAMuonVertex"   , "vz"                  , 10000  , -1000  , 1000   , ""  ),
  ("PatDSAMuonVertex"   , "dR"                  , 500   , 0     , 10    , ""  ),
  ("PatDSAMuonVertex"   , "originalMuonIdx1"    , 100   , 0     , 100   , ""  ),
  ("PatDSAMuonVertex"   , "originalMuonIdx2"    , 100   , 0     , 100   , ""  ),
  ("PatDSAMuonVertex"   , "isDSAMuon1"          , 10    , 0     , 10    , ""  ),
  ("PatDSAMuonVertex"   , "isDSAMuon2"          , 10    , 0     , 10    , ""  ),

  ("Event"              , "nDSAMuonVertex"      , 50    , 0     , 50    , ""  ),
  ("DSAMuonVertex"      , "isValid"             , 10    , 0     , 10    , ""  ),
  ("DSAMuonVertex"      , "dca"                 , 1000  , 0     , 20    , ""  ),
  ("DSAMuonVertex"      , "dcaStatus"           , 10    , 0     , 10    , ""  ),
  ("DSAMuonVertex"      , "chi2"                , 500   , 0     , 500   , ""  ),
  ("DSAMuonVertex"      , "vxy"                 , 10000  , -1000  , 1000   , ""  ),
  ("DSAMuonVertex"      , "vxySigma"            , 10000  , 0      , 100    , ""  ),
  ("DSAMuonVertex"      , "vz"                  , 10000  , -1000  , 1000   , ""  ),
  ("DSAMuonVertex"      , "dR"                  , 500   , 0     , 10    , ""  ),
  ("DSAMuonVertex"      , "originalMuonIdx1"    , 100   , 0     , 100   , ""  ),
  ("DSAMuonVertex"      , "originalMuonIdx2"    , 100   , 0     , 100   , ""  ),
  ("DSAMuonVertex"      , "isDSAMuon1"          , 10    , 0     , 10    , ""  ),
  ("DSAMuonVertex"      , "isDSAMuon2"          , 10    , 0     , 10    , ""  ),

  # ("Event"              , "nBS"                 , 50    , 0     , 50    , ""  ),
  # ("BS"                 , "chi2"                , 500   , 0     , 500   , ""  ),
  # ("BS"                 , "ndof"                , 100   , 0     , 100   , ""  ),
  # ("BS"                 , "x"                   , 500   , 0     , 500   , ""  ),
  # ("BS"                 , "y"                   , 500   , 0     , 500   , ""  ),
  # ("BS"                 , "z"                   , 500   , 0     , 500   , ""  ),
)

if runLLPNanoAODHistograms:
  defaultHistParams = defaultHistParams + LLPNanoAOD_defaultHistParams

histParams = (
#  collection         variable                      bins   xmin   xmax    dir
  ("Muon"           , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("TightMuons"     , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("LooseMuons"     , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("Electron"       , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("LooseElectrons" , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("Jet"            , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("GoodJets"       , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  
  ("Muon"           , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("TightMuons"     , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("LooseMuons"     , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("Electron"       , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("LooseElectrons" , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("Jet"            , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("GoodJets"       , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  
  ("LooseMuons"     , "dimuonMinv"                , 200   , 0   , 200   , ""  ),
  ("LooseMuons"     , "dimuonMinvClosestToZ"      , 200   , 0   , 200   , ""  ),
  ("LooseMuons"     , "dimuonDeltaRclosestToZ"    , 200   , -10 , 10    , ""  ),
  ("LooseMuons"     , "dimuonDeltaEtaclosestToZ"  , 200   , -10 , 10    , ""  ),
  ("LooseMuons"     , "dimuonDeltaPhiclosestToZ"  , 200   , -10 , 10    , ""  ),
  ("GoodJets"       , "minvBjet2jets"             , 2000  , 0   , 2000  , ""  ),
  ("TightMuons"     , "deltaPhiMuonMET"           , 200   , -4  , 4     , ""  ),
  ("TightMuons"     , "minvMuonMET"               , 1000  , 0   , 1000  , ""  ),
  
  ("Event"          , "normCheck"                 , 1     , 0   , 1     , ""  ),
)

LLPNanoAOD_histParams = ()

LLPNanoAOD_histParams2D = (
  #  collection + variables                           binsx   xmin  xmax binsy ymin   ymax   name
  ("GoodLooseMuonsVertex_normChi2_ndof",               1000, 0    , 10,   10  , 0    , 10   , ""  ),
  ("GoodLooseMuonsVertex_vxySigma_vxy",                1000, 0    , 10,   1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_vxyzSigma_vxyz",              1000, 0    , 10,   1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_vxySigma_vxySignificance",    1000, 0    , 50,   1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_vxyzSigma_vxyzSignificance",  1000, 0    , 50,   1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_vxySignificance_vxy",         1000, 0    , 1000, 1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_vxyzSignificance_vxyz",       1000, 0    , 1000, 1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_vxErr_vx",                    1000, 0    , 10,   1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_vyErr_vy",                    1000, 0    , 10,   1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_vzErr_vz",                    1000, 0    , 10,   1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_normChi2_vxy",                1000, 0    , 10,   1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_normChi2_vxyz",               1000, 0    , 10,   1000, 0    , 1000 , ""  ),
  ("GoodLooseMuonsVertex_normChi2_vxyz",               1000, 0    , 10,   1000, 0    , 1000 , ""  ),
)

muonVertexCollectionCategories = ["", "_PatDSA", "_DSA", "_Pat"]
muonCollectionCategories = ["", "DSA", "PAT"]
for matchingMethod, param in muonMatchingParams.items():
  for category in muonCollectionCategories:
    muonCollectionName = "Loose"+category+"Muons"+matchingMethod+"Match"
    LLPNanoAOD_histParams += (
      ("Event"      , "n"+muonCollectionName    , 50    , 0     , 50    , ""  ),
      (muonCollectionName  , "pt"               , 2000  , 0     , 1000  , ""  ),
      (muonCollectionName  , "eta"              , 300   , -3    , 3     , ""  ),
      (muonCollectionName  , "phi"              , 300   , -3    , 3     , ""  ),
      (muonCollectionName  , "dxy"              , 20000  , -2000    , 2000   , ""  ),
      (muonCollectionName  , "dxyPVTraj"        , 20000  , -2000    , 2000   , ""  ),
      (muonCollectionName  , "dxyPVTrajErr"     , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "dxyPVTrajSig"     , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "dz"               , 20000  , -2000    , 2000   , ""  ),
      (muonCollectionName  , "dzPV"             , 20000  , -2000    , 2000   , ""  ),
      (muonCollectionName  , "dzPVErr"          , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "dzPVSig"          , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "ip3DPVSigned"     , 20000  , -2000    , 2000   , ""  ),
      (muonCollectionName  , "ip3DPVSignedErr"  , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "ip3DPVSignedSig"  , 10000  , 0    , 2000   , ""  ),
      (muonCollectionName  , "minDeltaR"        , 1000   , 0    , 10     , ""  ),
      (muonCollectionName  , "minOuterDeltaR"   , 1000   , 0    , 10     , ""  ),
      (muonCollectionName  , "minProxDeltaR"    , 1000   , 0    , 10     , ""  ),
    )
  muonVertexCollectionName = "LooseMuonsVertex"+matchingMethod+"Match"
  LLPNanoAOD_histParams += (
    (muonVertexCollectionName , "vxErr"                    , 1000   , 0      , 100    , ""  ),
    (muonVertexCollectionName , "vyErr"                    , 1000   , 0      , 100    , ""  ),
    (muonVertexCollectionName , "vzErr"                    , 1000   , 0      , 100    , ""  ),
    (muonVertexCollectionName , "originalMuonIdx1"         , 100    , 0      , 100    , ""  ),
    (muonVertexCollectionName , "originalMuonIdx2"         , 100    , 0      , 100    , ""  ),
    (muonVertexCollectionName , "isDSAMuon1"            , 10     , 0      , 10     , ""  ),
    (muonVertexCollectionName , "isDSAMuon2"            , 10     , 0      , 10     , ""  ),
    (muonVertexCollectionName , "displacedTrackIso03Dimuon1"   , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso04Dimuon1"   , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso03Dimuon2"   , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso04Dimuon2"   , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso03Muon1"     , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso04Muon1"     , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso03Muon2"     , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso04Muon2"     , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "chargeProduct"         , 10     , -5    , 5     , ""  ),
    (muonVertexCollectionName , "lxyFromPVvxyDiff"      , 10000  , -1000  , 1000   , ""  ),
  )
  for category in muonVertexCollectionCategories:
    muonVertexCollectionName = "LooseMuonsVertex"+matchingMethod+"Match"+category
    LLPNanoAOD_histParams += (
      ("Event"       , "n"+muonVertexCollectionName       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "chi2"                  , 10000  , 0      , 500    , ""  ),
      (muonVertexCollectionName , "ndof"                  , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "normChi2"              , 50000  , 0      , 50     , ""  ),
      (muonVertexCollectionName , "vxy"                   , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxySigma"              , 10000  , 0      , 100    , ""  ),
      (muonVertexCollectionName , "vxySignificance"       , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxySignificanceV2"     , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vx"                    , 10000  , -1000  , 1000   , ""  ),
      (muonVertexCollectionName , "vy"                    , 10000  , -1000  , 1000   , ""  ),
      (muonVertexCollectionName , "vz"                    , 10000  , -1000  , 1000   , ""  ),
      (muonVertexCollectionName , "vxSignificance"        , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vySignificance"        , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vzSignificance"        , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxyz"                  , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxyzSigma"             , 10000  , 0      , 100    , ""  ),
      (muonVertexCollectionName , "vxyzSignificance"      , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dR"                    , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "proxDR"                , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "outerDR"               , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVert1"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVert2"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVertSum"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "maxHitsInFrontOfVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "missHitsAfterVert1"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "missHitsAfterVert2"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "missHitsAfterVertSum"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "maxMissHitsAfterVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "dca"                   , 1000   , 0      , 20     , ""  ),
      (muonVertexCollectionName , "dcaStatus"             , 10     , 0      , 10     , ""  ),
      (muonVertexCollectionName , "collinearityAngle"     , 1000   , -10    , 10     , ""  ),
      (muonVertexCollectionName , "absCollinearityAngle"  , 1000   , 0      , 10     , ""  ),
      (muonVertexCollectionName , "absPATPtLxyDPhi"       , 1000   , 0      , 10     , ""  ),
      (muonVertexCollectionName , "nPixelHits1"           , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "nPixelHits2"           , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "deltaPixelHits"        , 100    , -50    , 50     , ""  ),
      (muonVertexCollectionName , "nTrackerLayers1"      , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "nTrackerLayers2"      , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "lxyFromPV"             , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "invMass"               , 20000  , 0      , 200    , ""  ),
      (muonVertexCollectionName , "pt"                    , 2000   , 0      , 1000   , ""  ),
    )
    LLPNanoAOD_histParams2D += (
      (muonVertexCollectionName+"_invMass_absCollinearityAngle",  2000, 0  , 200 ,  700 , 0  , 7  , ""  ),
      (muonVertexCollectionName+"_Lxy_nTrackerLayers1"         ,  1000, 0  , 1000,  50  , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_Lxy_nTrackerLayers2"         ,  1000, 0  , 1000,  50  , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_Lxy_maxTrackerLayers"        ,  1000, 0  , 1000,  50  , 0  , 50 , ""  ),
    )

extraMuonVertexCollections = ["GoodLooseMuonsVertexWithLargeDR", "MaskedLooseMuonsVertex", "GoodLooseMuonsVertex", "GoodLooseMuonsVertexTight", "GoodMaskedLooseMuonsVertex", "BestLooseMuonsVertex", "SecondBestLooseMuonsVertex", "GoodBestLooseMuonsVertex", "GoodSecondBestLooseMuonsVertex", "GoodBestLooseMuonsVertexTight", "GoodSecondBestLooseMuonsVertexTight"]
for extraMuonVertexCollectionName in extraMuonVertexCollections:
  LLPNanoAOD_histParams += (
    (extraMuonVertexCollectionName , "vxErr"                    , 1000  , 0      , 100    , ""  ),
    (extraMuonVertexCollectionName , "vyErr"                    , 1000  , 0      , 100    , ""  ),
    (extraMuonVertexCollectionName , "vzErr"                    , 1000  , 0      , 100    , ""  ),
    (extraMuonVertexCollectionName , "originalMuonIdx1"         , 100    , 0      , 100    , ""  ),
    (extraMuonVertexCollectionName , "originalMuonIdx2"         , 100    , 0      , 100    , ""  ),
    (extraMuonVertexCollectionName , "isDSAMuon1"            , 10     , 0      , 10     , ""  ),
    (extraMuonVertexCollectionName , "isDSAMuon2"            , 10     , 0      , 10     , ""  ),
    (extraMuonVertexCollectionName , "displacedTrackIso03Dimuon1"   , 5000  , 0     , 500    , ""  ),
    (extraMuonVertexCollectionName , "displacedTrackIso04Dimuon1"   , 5000  , 0     , 500    , ""  ),
    (extraMuonVertexCollectionName , "displacedTrackIso03Dimuon2"   , 5000  , 0     , 500    , ""  ),
    (extraMuonVertexCollectionName , "displacedTrackIso04Dimuon2"   , 5000  , 0     , 500    , ""  ),
    (extraMuonVertexCollectionName , "displacedTrackIso03Muon1"     , 5000  , 0     , 500    , ""  ),
    (extraMuonVertexCollectionName , "displacedTrackIso04Muon1"     , 5000  , 0     , 500    , ""  ),
    (extraMuonVertexCollectionName , "displacedTrackIso03Muon2"     , 5000  , 0     , 500    , ""  ),
    (extraMuonVertexCollectionName , "displacedTrackIso04Muon2"     , 5000  , 0     , 500    , ""  ),
    (extraMuonVertexCollectionName , "chargeProduct"         , 10     , -5    , 5     , ""  ),
    (extraMuonVertexCollectionName , "lxyFromPVvxyDiff"      , 10000  , -1000  , 1000   , ""  ),
  )
  for category in muonVertexCollectionCategories:
    muonVertexCollectionName = extraMuonVertexCollectionName + category
    LLPNanoAOD_histParams += (
      ("Event"       , "n"+muonVertexCollectionName       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "chi2"                  , 10000  , 0      , 500    , ""  ),
      (muonVertexCollectionName , "ndof"                  , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "normChi2"              , 50000  , 0      , 50     , ""  ),
      (muonVertexCollectionName , "vxy"                   , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxySigma"              , 10000  , 0      , 100    , ""  ),
      (muonVertexCollectionName , "vxySignificance"       , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxySignificanceV2"     , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vx"                    , 10000  , -1000  , 1000   , ""  ),
      (muonVertexCollectionName , "vy"                    , 10000  , -1000  , 1000   , ""  ),
      (muonVertexCollectionName , "vz"                    , 10000  , -1000  , 1000   , ""  ),
      (muonVertexCollectionName , "vxSignificance"        , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vySignificance"        , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vzSignificance"        , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxyz"                  , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxyzSigma"             , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxyzSignificance"      , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dR"                    , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "proxDR"                , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "outerDR"               , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVert1"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVert2"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVertSum"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "maxHitsInFrontOfVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "missHitsAfterVert1"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "missHitsAfterVert2"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "missHitsAfterVertSum"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "maxMissHitsAfterVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "dca"                   , 1000   , 0      , 20     , ""  ),
      (muonVertexCollectionName , "dcaStatus"             , 10     , 0      , 10     , ""  ),
      (muonVertexCollectionName , "collinearityAngle"     , 1000   , -10    , 10     , ""  ),
      (muonVertexCollectionName , "absCollinearityAngle"  , 1000   , 0      , 10     , ""  ),
      (muonVertexCollectionName , "absPATPtLxyDPhi"       , 1000   , 0      , 10     , ""  ),
      (muonVertexCollectionName , "nPixelHits1"           , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "nPixelHits2"           , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "deltaPixelHits"        , 100    , -50    , 50     , ""  ),
      (muonVertexCollectionName , "nTrackerLayers1"       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "nTrackerLayers2"       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "lxyFromPV"             , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "invMass"               , 20000  , 0      , 200    , ""  ),
      (muonVertexCollectionName , "pt"                    , 2000   , 0      , 1000   , ""  ),
    )
    LLPNanoAOD_histParams2D += (
      (muonVertexCollectionName+"_invMass_absCollinearityAngle",  2000, 0  , 200,  700 , 0  , 7 , ""  ),
      (muonVertexCollectionName+"_Lxy_nTrackerLayers1"         ,  1000, 0  , 1000,  50  , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_Lxy_nTrackerLayers2"         ,  1000, 0  , 1000,  50  , 0  , 50 , ""  ),
      (muonVertexCollectionName+"_Lxy_maxTrackerLayers"        ,  1000, 0  , 1000,  50  , 0  , 50 , ""  ),
    )

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
  ("SegmentMatchLooseMuons"  , "dxy"                        , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseMuons"  , "dxyPVTraj"                  , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseMuons"  , "dxyPVTrajSig"               , 10000  , 0    , 2000   , ""  ),
  ("SegmentMatchLooseMuons"  , "dzPV"                       , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseMuons"  , "dzPVSig"                    , 10000  , 0    , 2000   , ""  ),
  ("SegmentMatchLooseMuons"  , "ip3DPVSigned"               , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseMuons"  , "ip3DPVSignedSig"            , 10000  , 0    , 2000   , ""  ),

  ("Event"             , "nSegmentMatchLooseDSAMuons"       , 50    , 0     , 50    , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "genMinDR"                , 1000  , 0     , 10    , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "genMinDRidx"             , 100   , 0     , 100   , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "pt"                      , 2000  , 0     , 1000  , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "eta"                     , 300   , -3    , 3     , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "phi"                     , 300   , -3    , 3     , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "dxy"                     , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "dxyPVTraj"               , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "dxyPVTrajSig"            , 10000  , 0    , 2000   , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "dzPV"                    , 20000  , -2000    , 2000   , ""  ),
  ("SegmentMatchLooseDSAMuons"  , "dzPVSig"                 , 10000  , 0    , 2000   , ""  ),
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
  ("SegmentDRMatchLooseMuons"  , "dxy"                      , 20000  , -2000    , 2000   , ""  ),
  ("SegmentDRMatchLooseMuons"  , "dxyPVTraj"                , 20000  , -2000    , 2000   , ""  ),
  ("SegmentDRMatchLooseMuons"  , "dxyPVTrajSig"             , 10000  , 0    , 2000   , ""  ),
  ("SegmentDRMatchLooseMuons"  , "dzPV"                     , 20000  , -2000    , 2000   , ""  ),
  ("SegmentDRMatchLooseMuons"  , "dzPVSig"                  , 10000  , 0    , 2000   , ""  ),
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
  ("SegmentOuterDRMatchLooseMuons"  , "dxy"                 , 20000  , -2000    , 2000   , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "dxyPVTraj"           , 20000  , -2000    , 2000   , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "dxyPVTrajSig"        , 10000  , 0    , 2000   , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "dzPV"                , 20000  , -2000    , 2000   , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "dzPVSig"             , 10000  , 0    , 2000   , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "ip3DPVSigned"        , 20000  , -2000    , 2000   , ""  ),
  ("SegmentOuterDRMatchLooseMuons"  , "ip3DPVSignedSig"     , 10000  , 0    , 2000   , ""  ),

  ("LooseDSAMuons"  , "nSegments"              , 50  , 0    , 50   , ""  ),
  ("LooseDSAMuons"  , "nDTHits"                , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"  , "nCSCHits"               , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"  , "nDTplusCSCHits"         , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"  , "muonMatch1"             , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"  , "muonMatch2"             , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"  , "muonMatch3"             , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"  , "matchRatio1"            , 600   , 0     , 2     , ""  ),
  ("LooseDSAMuons"  , "matchRatio2"            , 600   , 0     , 2     , ""  ),
  ("LooseDSAMuons"  , "matchRatio3"            , 600   , 0     , 2     , ""  ),

  ("LooseDSAMuons"  , "PATOuterDR"             , 1000  , 0     , 10    , ""  ),
  ("LooseDSAMuons"  , "PATProxDR"              , 1000  , 0     , 10    , ""  ),
  ("LooseDSAMuons"  , "PATDR"                  , 1000  , 0     , 10    , ""  ),
  ("LooseDSAMuons"  , "PATDEta"                , 600   , -6    , 6     , ""  ),
  ("LooseDSAMuons"  , "PATDPhi"                , 600   , -6    , 6     , ""  ),
  ("LooseDSAMuons"  , "PATDOuterEta"           , 600   , -6    , 6     , ""  ),
  ("LooseDSAMuons"  , "PATDOuterPhi"           , 600   , -6    , 6     , ""  ),
)

GenMuon_histParams = (
  ("Event"                     , "nGenMuonFromALP" , 50    , 0     , 50    , ""  ),
  ("GenMuonFromALP"            , "pdgId"           , 200   , -100  , 100   , ""  ),
  ("GenMuonFromALP"            , "pt"              , 4000  , 0     , 1000  , ""  ),
  ("GenMuonFromALP"            , "mass"            , 10000 , 0     , 100   , ""  ),
  ("GenMuonFromALP"            , "eta"             , 300   , -3    , 3     , ""  ),
  ("GenMuonFromALP"            , "phi"             , 300   , -3    , 3     , ""  ),
  ("GenMuonFromALP"            , "vx"              , 50000 , -5000 , 5000  , ""  ),
  ("GenMuonFromALP"            , "vy"              , 50000 , -5000 , 5000  , ""  ),
  ("GenMuonFromALP"            , "vz"              , 50000 , -5000 , 5000  , ""  ),
  ("GenMuonFromALP"            , "vxy"             , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "vxyz"            , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "boost"           , 2000 , 0      , 1000  , ""  ),
  ("GenMuonFromALP"            , "vxyALPboostpT"   , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "vxyALPboostT"    , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "vxyzALPboostp"   , 50000 , 0     , 5000  , ""  ),
  ("GenMuonFromALP"            , "dxy"             , 50000 , -5000 , 5000  , ""  ),
  ("GenMuonFromALP"            , "LoosePATMuonsMinDR"          , 1000  , 0     , 10    , ""  ),
  ("GenMuonFromALP"            , "LooseDSAMuonsMinDR"          , 1000  , 0     , 10    , ""  ),
  ("Event"                     , "nGenDimuonFromALP" , 50  , 0     , 50    , ""  ),
  ("GenDimuonFromALP"          , "invMass"         , 10000 , 0     , 100   , ""  ),
  ("GenDimuonFromALP"          , "deltaR"          , 1000  , 0     , 10    , ""  ),
  ("GenDimuonFromALP"          , "deltaEta"        , 300   , -3    , 3     , ""  ),
  ("GenDimuonFromALP"          , "deltaPhi"        , 300   , -3    , 3     , ""  ),
  ("Event"                     , "nGenALP"         , 50    , 0     , 50    , ""  ),
  ("GenALP"                    , "pdgId"           , 200   , -100  , 100   , ""  ),
  ("GenALP"                    , "pt"              , 4000  , 0     , 1000  , ""  ),
  ("GenALP"                    , "mass"            , 10000 , 0     , 100   , ""  ),
  ("GenALP"                    , "massT"           , 10000 , 0     , 100   , ""  ),
  ("GenALP"                    , "eta"             , 300   , -3    , 3     , ""  ),
  ("GenALP"                    , "phi"             , 300   , -3    , 3     , ""  ),
  ("GenALP"                    , "vx"              , 10000 , -1000 , 1000  , ""  ),
  ("GenALP"                    , "vy"              , 10000 , -1000 , 1000  , ""  ),
  ("GenALP"                    , "vz"              , 10000 , -1000 , 1000  , ""  ),
  ("GenALP"                    , "vxy"             , 10000 , -1000 , 1000  , ""  ),
  ("GenALP"                    , "vxyz"            , 10000 , -1000 , 1000  , ""  ),
  ("GenALP"                    , "boost_pT"        , 2000 , 0      , 1000  , ""  ),
  ("GenALP"                    , "boost_p"         , 2000 , 0      , 1000  , ""  ),
  ("GenALP"                    , "boost_T"         , 2000 , 0      , 1000  , ""  ),
  ("GenALP"                    , "dxy"             , 10000 , -1000 , 1000  , ""  ),
)

for matchingMethod, param in muonMatchingParams.items():
  muonCollectionName = "LooseMuonsFromALP"+matchingMethod+"Match"
  GenMuon_histParams += (
    ("Event"       , "n"+muonCollectionName        , 50    , 0     , 50    , ""  ),
    (muonCollectionName       , "pt"               , 2000  , 0     , 1000  , ""  ),
    (muonCollectionName       , "eta"              , 300   , -3    , 3     , ""  ),
    (muonCollectionName       , "phi"              , 300   , -3    , 3     , ""  ),
    (muonCollectionName       , "dxy"              , 20000  , -2000    , 2000   , ""  ),
    (muonCollectionName       , "dxyPVTraj"        , 20000  , -2000    , 2000   , ""  ),
    (muonCollectionName       , "dxyPVTrajErr"     , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName       , "dxyPVTrajSig"     , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName       , "dz"               , 20000  , -2000    , 2000   , ""  ),
    (muonCollectionName       , "dzPV"             , 20000  , -2000    , 2000   , ""  ),
    (muonCollectionName       , "dzPVErr"          , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName       , "dzPVSig"          , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName       , "ip3DPVSigned"     , 20000  , -2000    , 2000   , ""  ),
    (muonCollectionName       , "ip3DPVSignedErr"  , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName       , "ip3DPVSignedSig"  , 10000  , 0    , 2000   , ""  ),
    (muonCollectionName       , "nSegments"         , 50     , 0    , 50   , ""  ),
    (muonCollectionName       , "invMass"          , 10000 , 0     , 100   , ""  ),
    (muonCollectionName       , "deltaR"           , 1000  , 0     , 10    , ""  ),
    (muonCollectionName       , "minDeltaR"        , 1000  , 0     , 10    , ""  ),
    (muonCollectionName       , "outerDeltaR"      , 1000  , 0     , 10    , ""  ),
    (muonCollectionName       , "minOuterDeltaR"   , 1000  , 0     , 10    , ""  ),
    (muonCollectionName       , "minProxDeltaR"    , 1000  , 0     , 10    , ""  ),
    (muonCollectionName       , "deltaEta"         , 1000  , 0     , 10    , ""  ),
    (muonCollectionName       , "deltaPhi"         , 1000  , 0     , 10    , ""  ),
  )

  GenMuon_histParams += (
    ("GenMuonFromALP"         , "LooseMuons"+matchingMethod+"MatchMinDR"      , 1000  , 0     , 10    , ""  ),
  )

  muonVertexCollectionName = "LooseMuonsFromALP"+matchingMethod+"MatchVertex"
  GenMuon_histParams += (
    (muonVertexCollectionName , "vxErr"                 , 1000   , 0      , 100    , ""  ),
    (muonVertexCollectionName , "vyErr"                 , 1000   , 0      , 100    , ""  ),
    (muonVertexCollectionName , "vzErr"                 , 1000   , 0      , 100    , ""  ),
    (muonVertexCollectionName , "originalMuonIdx1"      , 100    , 0      , 100    , ""  ),
    (muonVertexCollectionName , "originalMuonIdx2"      , 100    , 0      , 100    , ""  ),
    (muonVertexCollectionName , "isDSAMuon1"            , 10     , 0      , 10     , ""  ),
    (muonVertexCollectionName , "isDSAMuon2"            , 10     , 0      , 10     , ""  ),
    (muonVertexCollectionName , "displacedTrackIso03Dimuon1"   , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso04Dimuon1"   , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso03Dimuon2"   , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso04Dimuon2"   , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso03Muon1"     , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso04Muon1"     , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso03Muon2"     , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "displacedTrackIso04Muon2"     , 5000  , 0     , 500    , ""  ),
    (muonVertexCollectionName , "chargeProduct"         , 10     , -5    , 5     , ""  ),
    (muonVertexCollectionName , "lxyFromPVvxyDiff"      , 1000   , 0      , 1000   , ""  ),

  )

  for category in muonVertexCollectionCategories:
    muonVertexCollectionName = "LooseMuonsFromALP"+matchingMethod+"MatchVertex"+category
    GenMuon_histParams += (
      ("Event"       , "n"+muonVertexCollectionName       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "chi2"                  , 10000  , 0      , 500    , ""  ),
      (muonVertexCollectionName , "ndof"                  , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "normChi2"              , 50000  , 0      , 50     , ""  ),
      (muonVertexCollectionName , "vxy"                   , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxySigma"              , 1000   , 0      , 100    , ""  ),
      (muonVertexCollectionName , "vxySignificance"       , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxySignificanceV2"     , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vx"                    , 5000   , -1000  , 1000   , ""  ),
      (muonVertexCollectionName , "vy"                    , 5000   , -1000  , 1000   , ""  ),
      (muonVertexCollectionName , "vz"                    , 5000   , -1000  , 1000   , ""  ),
      (muonVertexCollectionName , "vxSignificance"        , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vySignificance"        , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vzSignificance"        , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxyz"                  , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "vxyzSigma"             , 10000  , 0      , 100    , ""  ),
      (muonVertexCollectionName , "vxyzSignificance"      , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "dR"                    , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "proxDR"                , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "outerDR"               , 500    , 0      , 10     , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVert1"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVert2"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "hitsInFrontOfVertSum"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "maxHitsInFrontOfVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "missHitsAfterVert1"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "missHitsAfterVert2"    , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "missHitsAfterVertSum"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "maxMissHitsAfterVert"  , 100    , 0      , 100    , ""  ),
      (muonVertexCollectionName , "dca"                   , 1000   , 0      , 20     , ""  ),
      (muonVertexCollectionName , "dcaStatus"             , 10     , 0      , 10     , ""  ),
      (muonVertexCollectionName , "collinearityAngle"     , 1000   , -10    , 10     , ""  ),
      (muonVertexCollectionName , "absCollinearityAngle"  , 1000   , 0      , 10     , ""  ),
      (muonVertexCollectionName , "absPATPtLxyDPhi"       , 1000   , 0      , 10     , ""  ),
      (muonVertexCollectionName , "nPixelHits1"           , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "nPixelHits2"           , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "deltaPixelHits"        , 100    , -50    , 50     , ""  ),
      (muonVertexCollectionName , "nTrackerLayers1"       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "nTrackerLayers2"       , 50     , 0      , 50     , ""  ),
      (muonVertexCollectionName , "lxyFromPV"             , 1000   , 0      , 1000   , ""  ),
      (muonVertexCollectionName , "invMass"               , 20000  , 0      , 200    , ""  ),
      (muonVertexCollectionName , "pt"                    , 2000   , 0      , 1000   , ""  ),
    )
  
if runLLPNanoAODHistograms:
  histParams = histParams + LLPNanoAOD_histParams
if runMuonMatchingHistograms:
  histParams = histParams + MuonMatching_histParams
if runGenMuonHistograms:
  histParams = histParams + GenMuon_histParams

histParams2D = (
)

MuonMatching_histParams2D = ( 
  ("LooseDSAMuons_muonMatch1_nSegments",               50  , 0    , 50, 50  , 0    , 50   , ""  ),
  ("LooseDSAMuons_muonMatch2_nSegments",               50  , 0    , 50, 50  , 0    , 50   , ""  ),
  ("LooseDSAMuons_muonMatch3_nSegments",               50  , 0    , 50, 50  , 0    , 50   , ""  ),

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

GenMuon_histParams2D = (

)

if runLLPNanoAODHistograms:
  histParams2D = histParams2D + LLPNanoAOD_histParams2D
if runMuonMatchingHistograms:
  histParams2D = histParams2D + MuonMatching_histParams2D
if runGenMuonHistograms:
  histParams2D = histParams2D + GenMuon_histParams2D
