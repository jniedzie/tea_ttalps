from scale_factors_config import *
from ttalps_extra_collections import *

year = "2018"
extraEventCollections = get_extra_event_collections(year)

nEvents = -1
printEveryNevents = 10000

runDefaultHistograms = True
runCustomTTAlpsHistograms = False
runTriggerHistograms = False
runPileupHistograms = False
runLLPNanoAODHistograms = False
runLLPNanoAOD2DHistograms = False
runMuonMatchingHistograms = False
runGenMuonHistograms = False
runLLPNanoAODVertexHistograms = True

weightsBranchName = "genWeight"
eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Proton_multiRP": "nProton_multiRP",
  "Proton_singleRP": "nProton_singleRP",
}

# histogramsOutputFilePath = "../test_hists.root"

pileupScaleFactorsPath = "/data/dust/user/jniedzie/ttalps_cms/pileup_scale_factors.root"
pileupScaleFactorsHistName = "pileup_scale_factors"

applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
  "jetID": False,
}

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
  
  ("Event"              , "nMuon"               , 50    , 0     , 50    , ""  ),
  ("Muon"               , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("Muon"               , "eta"                 , 100   , -2.5  , 2.5   , ""  ),
  ("Muon"               , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("Muon"               , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  
  ("Event"              , "nTightMuons"         , 50    , 0     , 50    , ""  ),
  ("TightMuons"         , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("TightMuons"         , "eta"                 , 100   , -2.5  , 2.5   , ""  ),
  ("TightMuons"         , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("TightMuons"         , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  ("TightMuons"         , "pfRelIso04_all"      , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "pfRelIso03_chg"      , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "pfRelIso03_all"      , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "tkRelIso"            , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "miniPFRelIso_chg"    , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "miniPFRelIso_all"    , 2000  , -10   , 10    , ""  ),
  ("TightMuons"         , "jetRelIso"           , 2000  , -10   , 10    , ""  ),

  
  ("Event"              , "nLoosePATMuons"         , 50    , 0     , 50    , ""  ),
  ("LoosePATMuons"         , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("LoosePATMuons"         , "eta"                 , 100   , -2.5  , 2.5   , ""  ),
  ("LoosePATMuons"         , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("LoosePATMuons"         , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  ("LoosePATMuons"         , "pfRelIso04_all"      , 2000  , -10   , 10    , ""  ),
  ("LoosePATMuons"         , "pfRelIso03_chg"      , 2000  , -10   , 10    , ""  ),
  ("LoosePATMuons"         , "pfRelIso03_all"      , 2000  , -10   , 10    , ""  ),
  ("LoosePATMuons"         , "tkRelIso"            , 2000  , -10   , 10    , ""  ),
  ("LoosePATMuons"         , "miniPFRelIso_chg"    , 2000  , -10   , 10    , ""  ),
  ("LoosePATMuons"         , "miniPFRelIso_all"    , 2000  , -10   , 10    , ""  ),
  ("LoosePATMuons"         , "jetRelIso"           , 2000  , -10   , 10    , ""  ),
    
  ("Event"              , "nElectron"           , 50    , 0     , 50    , ""  ),
  ("Electron"           , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("Electron"           , "eta"                 , 100   , -2.5  , 2.5   , ""  ),
  ("Electron"           , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("Electron"           , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  
  ("Event"              , "nLooseElectrons"     , 50    , 0     , 50    , ""  ),
  ("LooseElectrons"     , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("LooseElectrons"     , "eta"                 , 100   , -2.5  , 2.5   , ""  ),
  ("LooseElectrons"     , "dxy"                 , 8000  , -1000  , 1000   , ""  ),
  ("LooseElectrons"     , "dz"                  , 8000  , -1000  , 1000   , ""  ),
  
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
  
  ("Event"                    , "nGoodMediumBtaggedJets"    , 50    , 0     , 50    , ""  ),
  ("GoodMediumBtaggedJets"    , "pt"                  , 2000  , 0     , 2000  , ""  ),
  ("GoodMediumBtaggedJets"    , "eta"                 , 100   , -2.5  , 2.5   , ""  ),
  ("GoodMediumBtaggedJets"    , "phi"                 , 100   , -2.5  , 2.5   , ""  ),
  ("GoodMediumBtaggedJets"    , "btagDeepB"           , 200   , -1    , 1     , ""  ),
  ("GoodMediumBtaggedJets"    , "btagDeepFlavB"       , 200   , -1    , 1     , ""  ),
)

LLPNanoAOD_defaultHistParams = (

  ("Event"              , "nDSAMuon"            , 50    , 0     , 50    , ""  ),
  ("DSAMuon"            , "pt"                  , 2000  , 0     , 1000  , ""  ),
  ("DSAMuon"            , "eta"                 , 100   , -2.5  , 2.5   , ""  ),
  ("DSAMuon"            , "dxy"                 , 1600  , -400  , 400   , ""  ),
  ("DSAMuon"            , "dz"                  , 1600  , -400  , 400   , ""  ),

  ("Event"              , "nMuonVertex"         , 50    , 0     , 50    , ""  ),
  ("MuonVertex"         , "chi2"                , 500   , 0     , 500   , ""  ),
  ("MuonVertex"         , "vxy"                 , 500   , 0     , 500   , ""  ),
  ("MuonVertex"         , "vxySigma"            , 500   , 0     , 500   , ""  ),
  ("MuonVertex"         , "vz"                  , 1000  , -500  , 500   , ""  ),
  ("MuonVertex"         , "dR"                  , 500   , 0     , 10    , ""  ),

  ("Event"              , "nDSAMuonVertex"      , 50    , 0     , 50    , ""  ),
  ("DSAMuonVertex"      , "chi2"                , 500   , 0     , 500   , ""  ),
  ("DSAMuonVertex"      , "vxy"                 , 500   , 0     , 500   , ""  ),
  ("DSAMuonVertex"      , "vxySigma"            , 500   , 0     , 500   , ""  ),
  ("DSAMuonVertex"      , "vz"                  , 1000  , -500  , 500   , ""  ),
  ("DSAMuonVertex"      , "dR"                  , 500   , 0     , 10    , ""  ),

  ("Event"              , "nMuonCombVertex"     , 50    , 0     , 50    , ""  ),
  ("MuonCombVertex"     , "chi2"                , 500   , 0     , 500   , ""  ),
  ("MuonCombVertex"     , "vxy"                 , 500   , 0     , 500   , ""  ),
  ("MuonCombVertex"     , "vxySigma"            , 500   , 0     , 500   , ""  ),
  ("MuonCombVertex"     , "vz"                  , 1000  , -500  , 500   , ""  ),
  ("MuonCombVertex"     , "dR"                  , 500   , 0     , 10    , ""  ),
)

if runLLPNanoAODHistograms:
  defaultHistParams = defaultHistParams + LLPNanoAOD_defaultHistParams

histParams = (
#  collection         variable                      bins   xmin   xmax    dir
  ("Muon"           , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("TightMuons"     , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("LoosePATMuons"     , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("Electron"       , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("LooseElectrons" , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("Jet"            , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  ("GoodJets"       , "leadingPt"                 , 2000  , 0   , 1000  , ""  ),
  
  ("Muon"           , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("TightMuons"     , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("LoosePATMuons"     , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("Electron"       , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("LooseElectrons" , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("Jet"            , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  ("GoodJets"       , "subleadingPt"              , 2000  , 0   , 1000  , ""  ),
  
  ("LoosePATMuons"     , "dimuonMinv"                , 200   , 0   , 200   , ""  ),
  ("LoosePATMuons"     , "dimuonMinvClosestToZ"      , 200   , 0   , 200   , ""  ),
  ("LoosePATMuons"     , "dimuonDeltaRclosestToZ"    , 200   , -10 , 10    , ""  ),
  ("LoosePATMuons"     , "dimuonDeltaEtaclosestToZ"  , 200   , -10 , 10    , ""  ),
  ("LoosePATMuons"     , "dimuonDeltaPhiclosestToZ"  , 200   , -10 , 10    , ""  ),
  ("GoodJets"       , "minvBjet2jets"             , 2000  , 0   , 2000  , ""  ),
  ("TightMuons"     , "deltaPhiMuonMET"           , 200   , -4  , 4     , ""  ),
  ("TightMuons"     , "minvMuonMET"               , 1000  , 0   , 1000  , ""  ),
  
  ("Event"          , "normCheck"                 , 1     , 0   , 1     , ""  ),
)

LLPNanoAOD_histParams = (
  ("Event"          , "nAllLooseMuons"            , 50    , 0     , 50    , ""  ),
  ("AllLooseMuons"  , "pt"                        , 2000  , 0     , 1000  , ""  ),
  ("AllLooseMuons"  , "eta"                       , 100   , -2.5  , 2.5   , ""  ),
  ("AllLooseMuons"  , "dxy"                       , 1600  , -400  , 400   , ""  ),
  ("AllLooseMuons"  , "dz"                        , 1600  , -400  , 400   , ""  ),
  ("AllLooseMuons"  , "deltaR"                    , 500   , 0     , 50    , ""  ),
  ("AllLooseMuons"  , "minDeltaR"                 , 500   , 0     , 50    , ""  ),

  ("Event"          , "nLooseDSAMuons"            , 50    , 0     , 50    , ""  ),
  ("LooseDSAMuons"  , "pt"                        , 2000  , 0     , 1000  , ""  ),
  ("LooseDSAMuons"  , "eta"                       , 100   , -2.5  , 2.5   , ""  ),
  ("LooseDSAMuons"  , "dxy"                       , 1600  , -400  , 400   , ""  ),
  ("LooseDSAMuons"  , "dz"                        , 1600  , -400  , 400   , ""  ),
)

if runLLPNanoAODHistograms:
  histParams = histParams + LLPNanoAOD_histParams


if runLLPNanoAODVertexHistograms:

  categories = ["", "_PatDSA", "_DSA", "_Pat"]
  for category in categories:
    hist_name = "GoodBestLooseMuonsVertex" + category
    histParams += (
      (hist_name, "normChi2"              , 50000  , 0      , 50     , ""  ),
      (hist_name, "vxy"                   , 1000   , 0      , 1000   , ""  ),
      (hist_name, "vxySigma"              , 1000   , 0      , 100    , ""  ),
      (hist_name, "vxySignificance"       , 1000   , 0      , 1000   , ""  ),
      (hist_name, "vxySignificanceV2"     , 1000   , 0      , 1000   , ""  ),
      (hist_name, "dca"                   , 1000   , 0      , 20     , ""  ),
      (hist_name, "collinearityAngle"     , 1000   , -10    , 10     , ""  ),
      (hist_name, "invMass"               , 20000  , 0      , 200    , ""  ),
    )
