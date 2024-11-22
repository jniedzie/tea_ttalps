import ROOT
from ROOT import TColor
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from ttalps_cross_sections import *

base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms/"

# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_GenLevel"
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons"
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_JPsiDimuons"

# skim = "skimmed_looseSemimuonicv1"
# skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1"
# skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_Iso"
skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"

output_formats = ["pdf"]

# luminosity = 63670. # pb^-1
luminosity = 59830. # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

canvas_size = (800, 600)
canvas_size_2Dhists = (800, 800)
show_ratio_plots = False
ratio_limits = (0.5, 1.5)

legend_width = 0.17 if show_ratio_plots else 0.23
legend_min_x = 0.45
legend_max_x = 0.82
legend_height = 0.045 if show_ratio_plots else 0.03
legend_max_y = 0.89

# requierement is num. events >= bkgRawEventsThreshold
bkgRawEventsThreshold = 10

n_default_backgrounds = 10

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Private Work"

## SETTINGS ##
plots_from_LLPNanoAOD = True
plot_genALP_info = True
plot_muonMatching_info = False
plot_ratio_hists = True
plot_background = True
plot_data = False

# for LLPNanoAOD plots
muonMatchingMethods = [
#   # # "DR", 
#   # # "OuterDR", 
#   # # "ProxDR", 
  # "Segment"
]

# for genALP plots
genMuonMatchingMethods = [
  "Segment"
]

extraMuonVertexCollections = [
  # # "MaskedDimuonVertices",
  # # "GoodDimuonVertices",
  # "BestDimuonVertex", 
  # # "GoodIsoDimuonVertices", 
  # "BestIsoDimuonVertex",
  # # "BestDimuonVertexNminus1InvMassCut",
  # # "BestDimuonVertexNminus1DRCut",
  # # "BestDimuonVertexNminus1CollinearityCut",
  # # "BestDimuonVertexNminus1IsoCut",
  # # "BestDimuonVertexNminus1Chi2Cut",
  # # "BestDimuonVertexNminus1DCACut",
  # # "BestDimuonVertexNminus1DPhiMuonpTLxyCutCut",
  # # "BestDimuonVertexNminus1HitsInFrontOfVertexCut",
  # # "BestDimuonVertexNminus1ChargeCut",
]

signal_legend = Legend(legend_max_x-legend_width, legend_max_y-5*legend_height, legend_max_x-2*legend_width, legend_max_y, "l")
sampletype = "sig"

if plot_background:
  plot_genALP_info = False
  plot_ratio_hists = False
  signal_legend = Legend(legend_max_x-2.5*legend_width, legend_max_y-0.13-3*legend_height, legend_max_x-2*legend_width, legend_max_y-0.13, "l")
  sampletype = "bkg"

if plot_data:
  plot_genALP_info = False
  plot_ratio_hists = False 
  signal_legend = Legend(legend_max_x-2.5*legend_width, legend_max_y-0.13-3*legend_height, legend_max_x-2*legend_width, legend_max_y-0.13, "l")
  sampletype = "data"

legends = {
  SampleType.signal: signal_legend,
  SampleType.background: Legend(legend_max_x-legend_width, legend_max_y-n_default_backgrounds*legend_height, legend_max_x, legend_max_y, "f"),
  SampleType.data: Legend(legend_max_x-3*(legend_width), legend_max_y-legend_height, legend_max_x-2*(legend_width), legend_max_y, "pl"),
}

output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{sampletype}/"
# output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{sampletype}_test/"

background_uncertainty_style = 3244 # available styles: https://root.cern.ch/doc/master/classTAttFill.html
background_uncertainty_color = ROOT.kBlack
background_uncertainty_alpha = 0.3

plotting_options = {
  SampleType.background: "hist",
  SampleType.signal: "nostack hist",
  SampleType.data: "nostack e",
}

default_norm = NormalizationType.to_lumi
# default_norm = NormalizationType.to_background
# default_norm = NormalizationType.to_data

y_scale = 0.01

if plot_background:
  default_norm = NormalizationType.to_background
else:
  # default_norm = NormalizationType.to_one
  default_norm = NormalizationType.to_lumi
  y_scale = 0.1
if plot_data:
  default_norm = NormalizationType.to_data
  y_scale=0.00001
  
histograms = (
# #           name                                  title logx  logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
  
  Histogram("Event_PV_npvs"                       , "", False, True  , default_norm              , 1  , 0     , 90   , 1e-2   , 1e8   , "# Primary vertices"                  , "# events (2018)"   ),
  Histogram("Event_PV_npvsGood"                   , "", False, True  , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "# Good primary vertices"             , "# events (2018)"   ),
  Histogram("Event_PV_x"                          , "", False, True  , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV x [cm]"                           , "# events (2018)"   ),
  Histogram("Event_PV_y"                          , "", False, True  , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV y [cm]"                           , "# events (2018)"   ),
  Histogram("Event_PV_z"                          , "", False, True  , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV z [cm]"                           , "# events (2018)"   ),
  
  Histogram("cutFlow"                             , "", False, True  , default_norm , 1  , 0     , 13     , 1e1*y_scale   , 1e23*y_scale  , "Selection"                      , "Number of events"  ),
  Histogram("Event_normCheck"                     , "", False, True  , default_norm , 1  , 0     , 1      , 1e-1*y_scale  , 1e20*y_scale   , "norm check"                     , "# events (2018)"   ),
)

LLPnanoAOD_histograms = ()
histograms2D_LLPnanoAOD = ()

muonVertexCategories = ["_PatDSA", "_DSA", "_Pat", ""]
# muonVertexCategories = [""]
muonCollectionCategories = ["", "DSA", "PAT"]
# muonCollectionCategories = [""]
muonCollectionNames = []
muonVertexCollectionNames = extraMuonVertexCollections
for matchingMethod in muonMatchingMethods:
  for category in muonCollectionCategories:
    muonCollectionName = "Loose"+category+"Muons"+matchingMethod+"Match"
    muonCollectionNames.append(muonCollectionName)
  muonVertexCollectionName = "LooseMuonsVertex"+matchingMethod+"Match"
  muonVertexCollectionNames.append(muonVertexCollectionName)

for muonCollectionName in muonCollectionNames:
  LLPnanoAOD_histograms += (
    Histogram("Event_n"+muonCollectionName          , "", False, True  , default_norm        , 1  , 0     , 15    , 1e-5  , 1e3   , "Number of loose #mu"                            , "# events (2018)"   ),
    Histogram(muonCollectionName+"_pt"              , "", False, True  , default_norm        , 10 , 0     , 300   , 1e-1  , 1e5   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
    Histogram(muonCollectionName+"_eta"             , "", False, True  , default_norm        , 10 , -3    , 3     , 1e-1  , 1e7   , "loose #mu #eta"                                 , "# events (2018)"   ),
    Histogram(muonCollectionName+"_absDxyPVTraj"       , "", False, True  , default_norm        , 100, -300  , 300   , 1e-3  , 1e6   , "loose #mu |d_{xy}| [cm]"                          , "# events (2018)"   ),
    Histogram(muonCollectionName+"_dxyPVTrajErr"    , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu #sigma_{dxy} uncertainty [cm]"        , "# events (2018)"   ),
    Histogram(muonCollectionName+"_dxyPVTrajSig"    , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} / #sigma_{dxy}"                , "# events (2018)"   ),
    Histogram(muonCollectionName+"_ip3DPVSigned"    , "", False, True  , default_norm        , 250, -600  , 600   , 1e-3  , 1e6   , "loose #mu 3D IP [cm]"                           , "# events (2018)"   ),
    Histogram(muonCollectionName+"_ip3DPVSignedErr" , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu #sigma_{3DIP} [cm]"                   , "# events (2018)"   ),
    Histogram(muonCollectionName+"_ip3DPVSignedSig" , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu 3D IP / #sigma_{3DIP}"                , "# events (2018)"   ),
    Histogram(muonCollectionName+"_minDeltaR"       , "", False, True  , default_norm        , 5  , 0     , 3     , 1e-1  , 1e8   , "min #Delta R(loose #mu, loose #mu)"             , "# events (2018)"   ),
    Histogram(muonCollectionName+"_minOuterDeltaR"  , "", False, True  , default_norm        , 5  , 0     , 3     , 1e-1  , 1e8   , "min outer #Delta R(loose #mu, loose #mu)"       , "# events (2018)"   ),
    Histogram(muonCollectionName+"_minProxDeltaR"   , "", False, True  , default_norm        , 5  , 0     , 3     , 1e-1  , 1e8   , "min proximity #Delta R(loose #mu, loose #mu)"   , "# events (2018)"   ),
  )

for muonVertexCollectionName in muonVertexCollectionNames:
  for category in muonVertexCategories:
    LLPnanoAOD_histograms += (
      Histogram("Event_n"+muonVertexCollectionName+category               , "", False, True  , default_norm        , 1  , 0     , 45    , 1e-4  , 1e3   , "Number of loose #mu vertices"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_vxy"                  , "", False, True  , default_norm        , 10 , 0     , 200   , 1e-6*y_scale  , 1e11*y_scale   , "#mu vertex v_{xy} [cm]"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_Lxy"                  , "", False, True  , default_norm        , 10 , 0     , 200   , 1e-6*y_scale  , 1e11*y_scale   , "#mu vertex L_{xy} [cm]"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_vxySigma"             , "", False, True  , default_norm        , 50 , 0     , 100   , 1e-3  , 1e6   , "#mu vertex #sigma_{Lxy} [cm]"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_vxySignificance"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"       , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dR"                   , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex #Delta R"                    , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_proxDR"               , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex proximity #Delta R"          , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_outerDR"              , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex outer #Delta R"              , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dEta"                 , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-3  , 1e6   , "#mu vertex #Delta #eta"                 , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_outerDEta"            , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-3  , 1e6   , "#mu vertex outer #Delta #eta"           , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dPhi"                 , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-3  , 1e6   , "#mu vertex #Delta #phi"                 , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_outerDPhi"            , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-3  , 1e6   , "#mu vertex outer #Delta #phi"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_normChi2"             , "", False, True  , default_norm        , 100, 0     , 5     , 1e-5  , 1e4   , "#mu vertex #chi^{2}/ndof"               , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_chargeProduct"        , "", False, True  , default_norm        , 1  , -1    , 2     , 1e-3  , 1e8   , "Dimuon charge"                          , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_maxHitsInFrontOfVert" , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-4  , 1e6   , "Max N(hits before vertex)"              , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_sumHitsInFrontOfVert" , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-6  , 1e6   , "Sum N(hits before vertex)"              , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_hitsInFrontOfVert1"   , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-6  , 1e6   , "N(hits before vertex)"                  , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_hitsInFrontOfVert2"   , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-7  , 1e5   , "N(hits before vertex)"                  , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_maxMissHitsAfterVert" , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-6  , 1e6   , "Max N(hits after vertex)"               , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dca"                  , "", False, True  , default_norm        , 20 , 0     , 15    , 1e-6  , 1e6   , "DCA [cm]"                               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_absCollinearityAngle" , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-5  , 1e6   , "#mu vertex |#Delta #Phi|"               , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_absCollinearityAngle" , "", False, False , default_norm        , 10 , 0     , 3.15  , 0     , 500   , "#mu vertex |#Delta #Phi|"               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_absPtLxyDPhi1"        , "", False, False , default_norm        , 10 , 0     , 3.15  , 0     , 0.6   , "#mu vertex |#Delta #phi_{#mu1}|"        , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_absPtLxyDPhi1"        , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-4  , 1e2   , "#mu vertex |#Delta #phi_{#mu1}|"        , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_absPtLxyDPhi2"        , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-4  , 1e5   , "#mu vertex |#Delta #phi_{#mu2}|"        , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_absPtPtMissDPhi"      , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-3  , 1e6   , "#mu vertex |#Delta #phi(p_{T}^{2}, p_{T}^{miss})|"        , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_deltaPixelHits"       , "", False, True  , default_norm        , 1  , 0     , 15    , 1e-3  , 1e10  , "#Delta N(pixel hits)"                   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nTrackerLayers1"      , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-3  , 1e10  , "#mu_{1} N(tracker layers)"              , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nTrackerLayers2"      , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-3  , 1e6   , "#mu_{2} N(tracker layers)"              , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nSegments1"           , "", False, True  , NormalizationType.to_one        , 1  , 0     , 10    , 1e-6  , 1e4  , "#mu_{1} N(muon segments)"               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nSegments2"           , "", False, True  , NormalizationType.to_one        , 1  , 0     , 10    , 1e-6  , 1e4  , "#mu_{2} N(muon segments)"               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nSegmentsSum"         , "", False, True  , default_norm        , 1  , 0     , 20    , 1e-3  , 1e10  , "#mu_{1} + #mu_{2} N(muon segments)"     , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_OSinvMass"            , "", False, True  , default_norm        , 1  , 2.5     , 3.5     , 1e-4  , 1e9   , "#mu vertex M_{#mu #mu} [GeV]"                 , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_SSinvMass"            , "", False, True  , default_norm        , 1  , 2.5     , 3.5     , 1e-4  , 1e9   , "#mu vertex M_{#mu #mu} [GeV]"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_invMass"              , "", False, True  , default_norm        , 20, 0     , 10   , 1e-7  , 1e6   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_invMass"              , "", False, True  , default_norm        , 2  , 2.7     , 3.5     , 1e-4*y_scale  , 1e10*y_scale   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_pt"                   , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex p_{T} [GeV]"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_leadingPt"            , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex leading p_{T} [GeV]"         , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_subleadingPt"         , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex subleading p_{T} [GeV]"      , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dxyPVTraj1"           , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} [cm]"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dxyPVTraj2"           , "", False, True  , default_norm        , 20 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} [cm]"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_minDxyPVTraj"         , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex min d_{xy} [cm]"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_maxDxyPVTraj"         , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex max d_{xy} [cm]"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig1"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} / #sigma_{dxy}^{1}"  , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig2"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} / #sigma_{dxy}^{2}"  , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_minDxyPVTrajSig"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex min d_{xy} / #sigma_{dxy}"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_maxDxyPVTrajSig"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex max d_{xy} / #sigma_{dxy}"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Dimuon1"      , "", False, True  , default_norm        , 1  , 0     , 1   , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Dimuon1"      , "", False, True  , default_norm        , 1  , 0     , 1   , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Dimuon2"      , "", False, True  , default_norm        , 1  , 0     , 1   , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Dimuon2"      , "", False, True  , default_norm        , 1  , 0     , 1   , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Muon1"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Muon1"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Muon2"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Muon2"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_pfRelIso04all1"                  , "", False, True  , default_norm        , 4  , 0     , 1    , 1e-3  , 1e6   , "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_pfRelIso04all2"                  , "", False, True  , default_norm        , 4  , 0     , 1    , 1e-3  , 1e6   , "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_tkRelIsoMuon1"                   , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{1} I_{tk}^{rel} ( #Delta R < 0.3 )"    , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_tkRelIsoMuon2"                   , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{2} I_{tk}^{rel} ( #Delta R < 0.3 )"    , "# events (2018)"   ),
    )

histograms2D_LLPnanoAOD = (

# #   Histogram2D("BestLooseMuonsVertex_Pat_dca_normChi2"             , "", False, False, True  , NormalizationType.to_lumi , 1   , 20  , 0 , 1   , 0 , 15   , 1e-2  , 1e3   , "#mu vertex DCA [cm]"  , "#mu vertex #chi^{2}/ndof"  , "# events (2018)"   ),
# #   Histogram2D("BestLooseMuonsVertex_PatDSA_dca_normChi2"          , "", False, False, True  , NormalizationType.to_lumi , 10  , 20  , 0 , 15  , 0 , 15   , 1e-2  , 1e3   , "#mu vertex DCA [cm]"  , "#mu vertex #chi^{2}/ndof"  , "# events (2018)"   ),
# #   Histogram2D("BestLooseMuonsVertex_DSA_dca_normChi2"             , "", False, False, True  , NormalizationType.to_lumi , 10  , 5   , 0 , 15  , 0 , 5    , 1e-2  , 1e3   , "#mu vertex DCA [cm]"  , "#mu vertex #chi^{2}/ndof"  , "# events (2018)"   ),
# #   Histogram2D("BestLooseMuonsVertexHitsInFrontOfVertex_Pat_dca_normChi2"             , "", False, False, True  , NormalizationType.to_lumi , 1   , 20  , 0 , 1   , 0 , 15   , 1e-2  , 1e3   , "#mu vertex DCA [cm]"  , "#mu vertex #chi^{2}/ndof"  , "# events (2018)"   ),
# #   Histogram2D("BestLooseMuonsVertexHitsInFrontOfVertex_PatDSA_dca_normChi2"          , "", False, False, True  , NormalizationType.to_lumi , 10  , 5   , 0 , 15  , 0 , 5    , 1e-2  , 1e3   , "#mu vertex DCA [cm]"  , "#mu vertex #chi^{2}/ndof"  , "# events (2018)"   ),
# #   Histogram2D("BestLooseMuonsVertexHitsInFrontOfVertex_DSA_dca_normChi2"             , "", False, False, True  , NormalizationType.to_lumi , 10  , 5   , 0 , 15  , 0 , 5    , 1e-2  , 1e3   , "#mu vertex DCA [cm]"  , "#mu vertex #chi^{2}/ndof"  , "# events (2018)"   ),
# #   Histogram2D("GoodBestLooseMuonsVertex_Pat_dca_normChi2"             , "", False, False, True  , NormalizationType.to_lumi , 1   , 5   , 0 , 1   , 0 , 5   , 1e-2  , 1e3   , "#mu vertex DCA [cm]"  , "#mu vertex #chi^{2}/ndof"  , "# events (2018)"   ),
# #   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_dca_normChi2"          , "", False, False, True  , NormalizationType.to_lumi , 2   , 5   , 0 , 2  , 0 , 5    , 1e-2  , 1e3   , "#mu vertex DCA [cm]"  , "#mu vertex #chi^{2}/ndof"  , "# events (2018)"   ),
# #   Histogram2D("GoodBestLooseMuonsVertex_DSA_dca_normChi2"             , "", False, False, True  , NormalizationType.to_lumi , 2   , 5   , 0 , 2  , 0 , 5    , 1e-2  , 1e3   , "#mu vertex DCA [cm]"  , "#mu vertex #chi^{2}/ndof"  , "# events (2018)"   ),

  # Histogram2D("GoodBestLooseMuonsVertex_Pat_absCollinearityAngle_invMass"     , "", False, False, True  , NormalizationType.to_lumi , 5  , 2  , 0 , 3.15, 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|"  , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
  # Histogram2D("GoodBestLooseMuonsVertex_PatDSA_absCollinearityAngle_invMass"  , "", False, False, True  , NormalizationType.to_lumi , 5  , 2  , 0 , 3.15, 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|"  , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
  # Histogram2D("GoodBestLooseMuonsVertex_DSA_absCollinearityAngle_invMass"     , "", False, False, True  , NormalizationType.to_lumi , 5  , 2  , 0 , 3.15, 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|"  , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),

  # Histogram2D("LooseMuonsVertexSegmentMatch_Pat_absCollinearityAngle_invMass"     , "", False, False, True  , NormalizationType.to_lumi , 5  , 2  , 0 , 3.15, 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|"  , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
  # Histogram2D("LooseMuonsVertexSegmentMatch_PatDSA_absCollinearityAngle_invMass"  , "", False, False, True  , NormalizationType.to_lumi , 5  , 2  , 0 , 3.15, 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|"  , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
  # Histogram2D("LooseMuonsVertexSegmentMatch_DSA_absCollinearityAngle_invMass"     , "", False, False, True  , NormalizationType.to_lumi , 5  , 2  , 0 , 3.15, 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|"  , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),

#   # Histogram2D("GoodBestLooseMuonsVertex_PatDSA_nSegmentsSum_invMass"          , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 15  , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #segments"      , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_DSA_nSegmentsSum_invMass"             , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 15  , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #segments"      , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_Pat_chargeProduct_invMass"            , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , -1, 2   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex charge product" , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_PatDSA_chargeProduct_invMass"         , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , -1, 2   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex charge product" , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_DSA_chargeProduct_invMass"            , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , -1, 2   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex charge product" , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_Pat_dEta_invMass"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 1   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_PatDSA_dEta_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 1   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_DSA_dEta_invMass"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 1   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_DSA_outerDEta_invMass"                , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 1   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta outer #eta" , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_Pat_dR_invMass"                       , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 1   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_PatDSA_dR_invMass"                    , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 1   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_DSA_dR_invMass"                       , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 1   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),
#   # Histogram2D("GoodBestLooseMuonsVertex_DSA_outerDR_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 1   , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta outer R" , "#mu vertex M_{#mu #mu} [GeV]"  , "# events (2018)"   ),

#   Histogram2D("BestLooseMuonsVertex_Pat_dEta_displacedTrackIso03Dimuon1"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_PatDSA_dEta_displacedTrackIso03Dimuon1"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_dEta_displacedTrackIso03Dimuon1"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_outerDEta_displacedTrackIso03Dimuon1"                , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta outer #eta" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_Pat_dPhi_displacedTrackIso03Dimuon1"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_PatDSA_dPhi_displacedTrackIso03Dimuon1"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_dPhi_displacedTrackIso03Dimuon1"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_outerDPhi_displacedTrackIso03Dimuon1"                , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta outer #phi" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_Pat_dR_displacedTrackIso03Dimuon1"                       , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_PatDSA_dR_displacedTrackIso03Dimuon1"                    , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_dR_displacedTrackIso03Dimuon1"                       , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_outerDR_displacedTrackIso03Dimuon1"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta outer R" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),

#   Histogram2D("BestLooseMuonsVertex_Pat_dEta_absCollinearityAngle"                           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_PatDSA_dEta_absCollinearityAngle"                        , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_dEta_absCollinearityAngle"                           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_outerDEta_absCollinearityAngle"                      , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta outer #eta" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_Pat_dPhi_absCollinearityAngle"                           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_PatDSA_dPhi_absCollinearityAngle"                        , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_dPhi_absCollinearityAngle"                           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_outerDPhi_absCollinearityAngle"                      , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta outer #phi" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
  # Histogram2D("BestLooseMuonsVertex_Pat_dR_absCollinearityAngle"                             , "", False, False, True  , NormalizationType.to_lumi , 10  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
  # Histogram2D("BestLooseMuonsVertex_PatDSA_dR_absCollinearityAngle"                          , "", False, False, True  , NormalizationType.to_lumi , 10  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
  # Histogram2D("BestLooseMuonsVertex_DSA_dR_absCollinearityAngle"                             , "", False, False, True  , NormalizationType.to_lumi , 10  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
  # Histogram2D("BestLooseMuonsVertex_Pat_outerDR_absCollinearityAngle"                        , "", False, False, True  , NormalizationType.to_lumi , 10  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex outer #Delta R" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
  # Histogram2D("BestLooseMuonsVertex_PatDSA_outerDR_absCollinearityAngle"                     , "", False, False, True  , NormalizationType.to_lumi , 10  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex outer #Delta R" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
  # Histogram2D("BestLooseMuonsVertex_DSA_outerDR_absCollinearityAngle"                        , "", False, False, True  , NormalizationType.to_lumi , 10  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex outer #Delta R" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
  # Histogram2D("BestLooseMuonsVertex_Pat_proxDR_absCollinearityAngle"                         , "", False, False, True  , NormalizationType.to_lumi , 10  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex proximity #Delta R" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
  # Histogram2D("BestLooseMuonsVertex_PatDSA_proxDR_absCollinearityAngle"                      , "", False, False, True  , NormalizationType.to_lumi , 10  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex proximity #Delta R" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
  # Histogram2D("BestLooseMuonsVertex_DSA_proxDR_absCollinearityAngle"                         , "", False, False, True  , NormalizationType.to_lumi , 10  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex proximity #Delta R" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),

#   Histogram2D("BestLooseMuonsVertex_Pat_displacedTrackIso03Dimuon1_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_Pat_displacedTrackIso04Dimuon1_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_PatDSA_displacedTrackIso03Dimuon1_invMass"               , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_PatDSA_displacedTrackIso04Dimuon1_invMass"               , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_displacedTrackIso03Dimuon1_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_displacedTrackIso04Dimuon1_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),

#   Histogram2D("BestLooseMuonsVertex_Pat_absCollinearityAngle_displacedTrackIso03Dimuon1"     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.2 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_PatDSA_absCollinearityAngle_displacedTrackIso03Dimuon1"  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.2 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_absCollinearityAngle_displacedTrackIso03Dimuon1"     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.2 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_Pat_absCollinearityAngle_Lxy"                            , "", False, False, True  , NormalizationType.to_lumi , 5  , 5  , 0 , 3.15, 0 , 300   , 1e-2  , 1e2   , "|#Delta #Phi|" , "Lxy [cm]" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_PatDSA_absCollinearityAngle_Lxy"                         , "", False, False, True  , NormalizationType.to_lumi , 5  , 5  , 0 , 3.15, 0 , 300   , 1e-2  , 1e2   , "|#Delta #Phi|" , "Lxy [cm]" , "# events (2018)"   ),
#   Histogram2D("BestLooseMuonsVertex_DSA_absCollinearityAngle_Lxy"                            , "", False, False, True  , NormalizationType.to_lumi , 5  , 5  , 0 , 3.15, 0 , 300   , 1e-2  , 1e2   , "|#Delta #Phi|" , "Lxy [cm]" , "# events (2018)"   ),

#   Histogram2D("GoodBestLooseMuonsVertex_Pat_dEta_displacedTrackIso03Dimuon1"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_dEta_displacedTrackIso03Dimuon1"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_dEta_displacedTrackIso03Dimuon1"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_outerDEta_displacedTrackIso03Dimuon1"                , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta outer #eta" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_Pat_dPhi_displacedTrackIso03Dimuon1"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_dPhi_displacedTrackIso03Dimuon1"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_dPhi_displacedTrackIso03Dimuon1"                     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_outerDPhi_displacedTrackIso03Dimuon1"                , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta outer #phi" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_Pat_dR_displacedTrackIso03Dimuon1"                       , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_dR_displacedTrackIso03Dimuon1"                    , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_dR_displacedTrackIso03Dimuon1"                       , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_outerDR_displacedTrackIso03Dimuon1"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex #Delta outer R" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)"   ),

#   Histogram2D("GoodBestLooseMuonsVertex_Pat_dEta_absCollinearityAngle"                           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_dEta_absCollinearityAngle"                        , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_dEta_absCollinearityAngle"                           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #eta"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_outerDEta_absCollinearityAngle"                      , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta outer #eta" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_Pat_dPhi_absCollinearityAngle"                           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_dPhi_absCollinearityAngle"                        , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_dPhi_absCollinearityAngle"                           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta #phi"    , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_outerDPhi_absCollinearityAngle"                      , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta outer #phi" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_Pat_dR_absCollinearityAngle"                             , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_dR_absCollinearityAngle"                          , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_dR_absCollinearityAngle"                             , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta R"       , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_outerDR_absCollinearityAngle"                        , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 3.5   , 1e-2  , 1e2   , "#mu vertex #Delta outer R" , "#mu vertex |#Delta #Phi|"  , "# events (2018)"   ),

#   Histogram2D("GoodBestLooseMuonsVertex_Pat_displacedTrackIso03Dimuon1_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_Pat_displacedTrackIso04Dimuon1_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_displacedTrackIso03Dimuon1_invMass"               , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_displacedTrackIso04Dimuon1_invMass"               , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_displacedTrackIso03Dimuon1_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_displacedTrackIso04Dimuon1_invMass"                  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 10  , 0 , 10    , 1e-2  , 1e2   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )" , "#mu vertex M_{#mu #mu} [GeV]" , "# events (2018)"   ),

#   Histogram2D("GoodBestLooseMuonsVertex_Pat_absCollinearityAngle_displacedTrackIso03Dimuon1"     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_absCollinearityAngle_displacedTrackIso03Dimuon1"  , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_absCollinearityAngle_displacedTrackIso03Dimuon1"     , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 3.5 , 0 , 10    , 1e-2  , 1e2   , "#mu vertex |#Delta #Phi|" , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_Pat_absCollinearityAngle_Lxy"                            , "", False, False, True  , NormalizationType.to_lumi , 5  , 5  , 0 , 3.15, 0 , 300   , 1e-2  , 1e2   , "|#Delta #Phi|" , "Lxy [cm]" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_PatDSA_absCollinearityAngle_Lxy"                         , "", False, False, True  , NormalizationType.to_lumi , 5  , 5  , 0 , 3.15, 0 , 300   , 1e-2  , 1e2   , "|#Delta #Phi|" , "Lxy [cm]" , "# events (2018)"   ),
#   Histogram2D("GoodBestLooseMuonsVertex_DSA_absCollinearityAngle_Lxy"                            , "", False, False, True  , NormalizationType.to_lumi , 5  , 5  , 0 , 3.15, 0 , 300   , 1e-2  , 1e2   , "|#Delta #Phi|" , "Lxy [cm]" , "# events (2018)"   ),

# #   Histogram2D("BestLooseMuonsVertex_PatDSA_Lxy_nTrackerLayers1"           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 800 , 0 , 20    , 1e-1  , 1e8   , "#mu vertex L_{xy} [cm]"         , "#mu_{1} N(tracker layers)" , "# events (2018)"   ),
# #   Histogram2D("BestLooseMuonsVertex_PatDSA_Lxy_nTrackerLayers2"           , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 800 , 0 , 20    , 1e-1  , 1e8   , "#mu vertex L_{xy} [cm]"         , "#mu_{2} N(tracker layers)" , "# events (2018)"   ),
# #   Histogram2D("BestLooseMuonsVertex_PatDSA_Lxy_maxTrackerLayers"          , "", False, False, True  , NormalizationType.to_lumi , 1  , 1  , 0 , 800 , 0 , 20    , 1e-1  , 1e8   , "#mu vertex L_{xy} [cm]"         , "max N(tracker layers)"     , "# events (2018)"   ),
)

histograms_muonMatching = (
  Histogram("Event_nSegmentMatchLooseMuons"             , "", False, True  , default_norm       , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale  , "Number of segment matched loose PAT #mu" , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_genMinDR"           , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "min #Delta R(loose PAT #mu, gen #mu)"                    , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_genMinDRidx"        , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "gen #mu index"                                           , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_nSegments"          , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "Segment matched loose PAT #mu #segments"                 , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_matchingRatio"      , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "Segment matched loose PAT #mu matching ratio"            , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_maxMatches"         , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "Segment matched loose PAT #mu max #matched segments"     , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_muonMatchIdx"       , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "Segment matched loose PAT #mu matched index"             , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_pt"                 , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "Segment matched loose PAT #mu p_{T} [GeV]"               , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_eta"                , "", False, True  , default_norm       , 10 , -3    , 3     , 1e-1  , 1e7   , "Segment matched loose PAT #mu #eta"                      , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_dxyPVTraj"          , "", False, True  , default_norm       , 20 , -100  , 100   , 1e-3  , 1e6   , "Segment matched loose PAT #mu d_{xy} [cm]"               , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_dxyPVTrajSig"       , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose PAT #mu d_{xy} / #sigma_{dxy}"     , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_ip3DPVSigned"       , "", False, True  , default_norm       , 100, -500  , 500   , 1e-3  , 1e6   , "Segment matched loose PAT #mu 3D IP [cm]"                , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_ip3DPVSignedSig"    , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose PAT #mu 3D IP / #sigma_{3DIP}"     , "# events (2018)"   ),

  Histogram("Event_nSegmentMatchLooseDSAMuons"          , "", False, True  , default_norm       , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale  , "Number of segment matched loose DSA #mu" , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_genMinDR"        , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "min #Delta R(loose DSA #mu, gen #mu)"                    , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_genMinDRidx"     , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "gen #mu index"                                           , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_pt"              , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "Segment matched loose DSA #mu p_{T} [GeV]"               , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_eta"             , "", False, True  , default_norm       , 10 , -3    , 3     , 1e-1  , 1e7   , "Segment matched loose DSA #mu #eta"                      , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_dxyPVTraj"       , "", False, True  , default_norm       , 20 , -100  , 100   , 1e-3  , 1e6   , "Segment matched loose DSA #mu d_{xy} [cm]"               , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_dxyPVTrajSig"    , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose DSA #mu d_{xy} / #sigma_{dxy}"     , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_ip3DPVSigned"    , "", False, True  , default_norm       , 100, -500  , 500   , 1e-3  , 1e6   , "Segment matched loose DSA #mu 3D IP [cm]"                , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_ip3DPVSignedSig" , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose DSA #mu 3D IP / #sigma_{3DIP}"     , "# events (2018)"   ),

  Histogram("Event_nSegmentOuterDRMatchLooseMuons"           , "", False, True  , default_norm       , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale  , "Number of loose PAT #mu"     , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_nSegments"        , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu #segments"                     , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_matchingRatio"    , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu matching ratio"                , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_maxMatches"       , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu max #matched segments"         , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_muonMatchIdx"     , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu matched index"                 , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_pt"               , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu p_{T} [GeV]"                   , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_eta"              , "", False, True  , default_norm       , 10 , -3    , 3     , 1e-1  , 1e7   , "loose PAT #mu #eta"                          , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_dxyPVTraj"        , "", False, True  , default_norm       , 20 , -100  , 100   , 1e-3  , 1e6   , "loose PAT #mu d_{xy} [cm]"                   , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_dxyPVTrajSig"     , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "loose PAT #mu d_{xy} / #sigma_{dxy}"         , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_ip3DPVSigned"     , "", False, True  , default_norm       , 100, -500  , 500   , 1e-3  , 1e6   , "loose PAT #mu 3D IP [cm]"                    , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_ip3DPVSignedSig"  , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "loose PAT #mu 3D IP / #sigma_{3DIP}"         , "# events (2018)"   ),

  Histogram("LooseDSAMuons_nSegments"             , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #segments"                     , "# events (2018)"   ),
  Histogram("LooseDSAMuons_muonMatch1"            , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #matching PAT segments"        , "# events (2018)"   ),
  Histogram("LooseDSAMuons_muonMatch2"            , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #matching PAT segments"        , "# events (2018)"   ),
  Histogram("LooseDSAMuons_matchRatio1"           , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu matching ratio"                , "# events (2018)"   ),
  Histogram("LooseDSAMuons_matchRatio2"           , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu matching ratio"                , "# events (2018)"   ),

  Histogram("LooseDSAMuons_PATOuterDR"            , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Outer #Delta R(loose DSA #mu, loose PAT #mu)"        , "# events (2018)"   ),
  Histogram("LooseDSAMuons_PATProxDR"             , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Proximity #Delta R(loose DSA #mu, loose PAT #mu)"    , "# events (2018)"   ),
  Histogram("LooseDSAMuons_PATDR"                 , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "#Delta R(loose DSA #mu, loose PAT #mu)"              , "# events (2018)"   ),
)

histograms2D_muonMatching = (
  # name  title  logx  logy  logz  normtype  rebinX  rebinY  xmin  xmax  ymin  ymax  zmin  zmax  xlabel  ylabel  zlabel  suffix

  Histogram2D("LooseDSAMuons_muonMatch1_nSegments",               "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,   0, 50,   0, 50,  1e-1,  1e5,  "Loose DSA #matching segments",  "Loose DSA #segments",    "# events (2018)",  ""  ),
  Histogram2D("LooseDSAMuons_muonMatch2_nSegments",               "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,   0, 50,   0, 50,  1e-1,  1e5,  "Loose DSA #matching segments",  "Loose DSA #segments",    "# events (2018)",  ""  ),

  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_genMinDR",    "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "min #Delta R(PAT #mu, gen #mu)",        "min #Delta R(DSA #mu, gen #mu)",        "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_genMinDRidx", "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "min #Delta R(PAT #mu, gen #mu) index",  "min #Delta R(DSA #mu, gen #mu) index",  "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_eta",         "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT #eta^{#mu}",        "DSA #eta^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_phi",         "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT #phi^{#mu}",        "DSA #phi^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_outerEta",    "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT outer #eta^{#mu}",  "DSA outer #eta^{#mu}", "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_outerPhi",    "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT outer #phi^{#mu}",  "DSA outer #phi^{#mu}", "# events (2018)",  ""  ),

  Histogram2D("SegmentMatchLooseMuons_eta_outerEta",              "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT #eta^{#mu}",  "PAT outer #eta^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_phi_outerPhi",              "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT #phi^{#mu}",  "PAT outer #phi^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseDSAMuons_eta_outerEta",           "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "DSA #eta^{#mu}",  "DSA outer #eta^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseDSAMuons_phi_outerPhi",           "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "DSA #phi^{#mu}",  "DSA outer #phi^{#mu}",       "# events (2018)",  ""  ),
)

histograms_genALPs = (
  # Histogram("Event_nGenALP"                       , "", False, True  , default_norm      , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen ALP"                     , "# events (2018)"   ),
  # Histogram("GenALP_pt"                           , "", False, True  , default_norm      , 1  , 0     , 500   , 1e-1  , 1e8   , "Gen ALP p_{T} [GeV]"                            , "# events (2018)"   ),
  # Histogram("GenALP_mass"                         , "", False, True  , default_norm      , 1  , 0     , 10    , 1e-1  , 1e8   , "Gen ALP mass [GeV]"                             , "# events (2018)"   ),
  Histogram("GenALP_eta"                          , "", False, True  , default_norm     , 1  , 0     , 3    , 1e-6  , 1e4   , "Gen ALP #eta"                            , "# events (2018)"   ),
  Histogram("Event_nGenMuonFromALP"               , "", False, True  , default_norm     , 1  , 0     , 4     , 1e-6   , 1e4   , "# Gen #mu from ALP"     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_index1"               , "", False, True  , default_norm     , 1  , 0     , 40    , 1e-4   , 1e3   , "Leading #mu from ALP index"             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_index2"               , "", False, True  , default_norm     , 1  , 0     , 40    , 1e-4   , 1e3   , "Subleading #mu from ALP index"          , "# events (2018)"   ),
  Histogram("GenMuonFromALP_pdgId"                , "", False, True  , default_norm     , 1  , -100  , 100   , 1e-2   , 1e4   , "Gen #mu particle ID"                    , "# events (2018)"   ),
  Histogram("GenMuonFromALP_Lxy"                  , "", False, True  , default_norm     , 200, 0     , 1000  , 1e-8   , 1e1   , "Gen #mu L_{xy} [cm]"                    , "# events (2018)"   ),
  Histogram("GenMuonFromALP_Lxyz"                 , "", False, True  , default_norm     , 100, 0     , 600   , 1e-8   , 1e1   , "Gen #mu L_{xyz} [cm]"                   , "# events (2018)"   ),
  Histogram("GenMuonFromALP_properLxy"            , "", False, True  , default_norm     , 2  , 0     , 10    , 1e-2   , 1e4   , "Gen proper #mu L_{xy} [cm]"             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_properLxyT"           , "", False, True  , default_norm     , 200, 0     , 1000  , 1e-8   , 1e1   , "Gen proper #mu L_{xy} [cm]"             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_properLxyz"           , "", False, True  , default_norm     , 100, 0     , 600   , 1e-8   , 1e1   , "Gen proper #mu L_{xyz} [cm]"            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_pt"                   , "", False, True  , default_norm     , 40 , 0     , 500   , 1e-3   , 1e3   , "Gen #mu p_{T} [GeV]"                    , "# events (2018)"   ),
  Histogram("GenMuonFromALP_eta"                  , "", False, True  , default_norm     , 10 , -3    , 3     , 1e-1   , 1e5   , "Gen #mu #eta"                           , "# events (2018)"   ),
  Histogram("GenMuonFromALP_mass"                 , "", False, True  , default_norm     , 1  , 0     , 1     , 1e-2   , 1e4   , "Gen #mu mass [GeV]"                     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_RecoMatch1MinDR"      , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta R(Gen #mu, loose #mu)"           , "# events (2018)"   ),
  Histogram("GenMuonFromALP_RecoMatch2MinDR"      , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta R(Gen #mu, loose #mu)"           , "# events (2018)"   ),
  Histogram("GenMuonFromALP_RecoMatch1MinDPhi"    , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta #Phi(Gen #mu, loose #mu)"        , "# events (2018)"   ),
  Histogram("GenMuonFromALP_RecoMatch2MinDPhi"    , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta #Phi(Gen #mu, loose #mu)"        , "# events (2018)"   ),
  Histogram("GenMuonFromALP_RecoMatch1MinDEta"    , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta #eta(Gen #mu, loose #mu)"        , "# events (2018)"   ),
  Histogram("GenMuonFromALP_RecoMatch2MinDEta"    , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta #eta(Gen #mu, loose #mu)"        , "# events (2018)"   ),
  Histogram("Event_nGenMuonFromW"                 , "", False, True  , default_norm     , 1  , 0     , 6     , 1e-6   , 1e4   , "# Gen #mu from W"                       , "# events (2018)"   ),
  Histogram("GenMuonFromW_index1"                 , "", False, True  , default_norm     , 1  , 0     , 40    , 1e-4   , 1e3   , "Leading #mu from W index"               , "# events (2018)"   ),
  Histogram("GenMuonFromW_index2"                 , "", False, True  , default_norm     , 1  , 0     , 40    , 1e-4   , 1e3   , "Subleading #mu from W index"            , "# events (2018)"   ),
  Histogram("GenMuonFromW_index3"                 , "", False, True  , default_norm     , 1  , 0     , 40    , 1e-4   , 1e3   , "Third leading #mu from W index"         , "# events (2018)"   ),
  Histogram("GenMuonFromW_RecoMatch1MinDR"        , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta R(Gen #mu, loose #mu)"           , "# events (2018)"   ),
  Histogram("GenMuonFromW_RecoMatch2MinDR"        , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta R(Gen #mu, loose #mu)"           , "# events (2018)"   ),
  Histogram("GenMuonFromW_RecoMatch1MinDPhi"      , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta #Phi(Gen #mu, loose #mu)"        , "# events (2018)"   ),
  Histogram("GenMuonFromW_RecoMatch2MinDPhi"      , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta #Phi(Gen #mu, loose #mu)"        , "# events (2018)"   ),
  Histogram("GenMuonFromW_RecoMatch1MinDEta"      , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta #eta(Gen #mu, loose #mu)"        , "# events (2018)"   ),
  Histogram("GenMuonFromW_RecoMatch2MinDEta"      , "", False, True  , default_norm     , 1  , 0     , 0.5   , 1e-5   , 1e2   , "#Delta #eta(Gen #mu, loose #mu)"        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatchVertex_genPlaneAngle"            , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatchVertex_recoPlaneAngle"           , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatchVertex_etaSum"                   , "", False, True  , default_norm     , 10 , 0     , 7     , 1e-6   , 1e1   , "Dimuon |#eta^{#mu1}| + |#eta^{#mu2}|" , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmaxdPhi2SegmentMatchVertex_genPlaneAngle"    , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmaxdPhi2SegmentMatchVertex_recoPlaneAngle"   , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmaxdPhi2SegmentMatchVertex_etaSum"           , "", False, True  , default_norm     , 10 , 0     , 7     , 1e-6   , 1e1   , "Dimuon |#eta^{#mu1}| + |#eta^{#mu2}|" , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_genPlaneAngle"    , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_recoPlaneAngle"   , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_etaSum"           , "", False, True  , default_norm     , 10 , 0     , 7     , 1e-6   , 1e1   , "Dimuon |#eta^{#mu1}| + |#eta^{#mu2}|" , "# events (2018)"   ),
  Histogram("LooseMuonsFromALegmentMatch_hasLeadingMuon"                   , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from ALP"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALegmentMatch_hmu_hasLeadingMuon"               , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from ALP"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromWSegmentMatch_hasLeadingMuon"                   , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from W boson"            , "# events (2018)"   ),
  Histogram("LooseMuonsFromWSegmentMatch_hmu_hasLeadingMuon"               , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from W boson"            , "# events (2018)"   ),
  Histogram("Event_nTightMuonsFromALPSegmentMatch"             , "", False, True  , default_norm     , 1  , 0     , 5     , 1e-2   , 1e4   , "# tight #mu from ALP"                 , "# events (2018)"   ),
  Histogram("TightMuonsFromALPSegmentMatch_hasLeadingMuon"     , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from ALP"                , "# events (2018)"   ),
  Histogram("TightMuonsFromALPSegmentMatch_hmu_hasLeadingMuon" , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from ALP"                , "# events (2018)"   ),
  Histogram("TightMuonsFromALPSegmentMatch_index"              , "", False, True  , default_norm     , 1  , 0     , 10    , 1e-4   , 1e2   , "Tight #mu from ALP index"             , "# events (2018)"   ),
  Histogram("TightMuonsFromALPSegmentMatch_hmu_index"          , "", False, True  , default_norm     , 1  , 0     , 10    , 1e-4   , 1e2   , "Tight #mu from ALP index"             , "# events (2018)"   ),
  Histogram("Event_nTightMuonsFromWSegmentMatch"               , "", False, True  , default_norm     , 1  , 0     , 5     , 1e-2   , 1e4   , "# tight #mu from W boson"             , "# events (2018)"   ),
  Histogram("TightMuonsFromWSegmentMatch_hasLeadingMuon"       , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from W boson"            , "# events (2018)"   ),
  Histogram("TightMuonsFromWSegmentMatch_hmu_hasLeadingMuon"   , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from W boson"            , "# events (2018)"   ),
  Histogram("TightMuonsFromWSegmentMatch_index"                , "", False, True  , default_norm     , 1  , 0     , 10    , 1e-4   , 1e2   , "Tight #mu from W index"               , "# events (2018)"   ),
  Histogram("TightMuonsFromWSegmentMatch_hmu_index"            , "", False, True  , default_norm     , 1  , 0     , 10    , 1e-4   , 1e2   , "Tight #mu from W index"               , "# events (2018)"   ),
)

histograms2D_genALPs = ()

genDimuonCollectionNames = [
  "GenDimuonFromALP",
  "GenMuonNotFromALP",
  "GenDimuonNotFromALP",
]
genmuonCollectionNames = [
  "LooseMuonsFromALP",
  "LooseMuonsFromALPmindPhi2",
  "LooseMuonsNotFromALP",
  "LooseMuonsFromW",
]
genmuonVertexCollectionNames = [
  "LooseMuonsFromALP",
  "LooseMuonsFromALPmindPhi2",
  "LooseMuonsNotFromALP",
  "LooseDimuonsNotFromALP",
]
muonVertexCategories = ["", "_Pat", "_DSA", "_PatDSA"]

for genDimuonCollectionName in genDimuonCollectionNames:
  histograms_genALPs += (
    Histogram("Event_n"+genDimuonCollectionName                     , "", False, True  , default_norm    , 1   , 0    , 5     , 1e-7   , 1e4   , "# Gen Dimuons not from ALP"     , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_invMass"                    , "", False, True  , default_norm    , 200 , 0    , 200   , 1e-6   , 1e4   , "Gen m_{#mu #mu} [GeV]"          , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_deltaR"                     , "", False, True  , default_norm    , 10  , 0    , 3     , 1e-4   , 1e2   , "Gen #Delta R(#mu #mu)"          , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_absCollinearityAngle"       , "", False, True  , default_norm    , 10  , 0    , 3.15  , 1e-6   , 1e2   , "Gen Dimuon |#Delta #Phi|"       , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_absPtLxyDPhi1"              , "", False, True  , default_norm    , 10  , 0    , 3.15  , 1e-5   , 1e3   , "Gen |#Delta #phi_{#mu1}|"       , "# events (2018)"   ),  
    Histogram(genDimuonCollectionName+"_absPtLxyDPhi2"              , "", False, True  , default_norm    , 10  , 0    , 3.15  , 1e-5   , 1e3   , "Gen |#Delta #phi_{#mu2}|"       , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_Lxy"                        , "", False, True  , default_norm    , 2   , 0    , 10    , 1e-6   , 1e4   , "Gen #mu L_{xy} [cm]"            , "# events (2018)"   ),
  )

for i in range(1,6):
  histograms_genALPs += (
    Histogram("GenDimuonNotFromALP_motherID1"+str(i)  , "", False, True  , default_norm  , 1  , -10   , 30   , 1e-8   , 1e1   , "Gen #mu_{1} mother PDG ID"  , "# events (2018)"   ),
    Histogram("GenDimuonNotFromALP_motherID1"+str(i)  , "", False, True  , default_norm  , 1  , -10   , 30   , 1e-8   , 1e1   , "Gen #mu_{2} mother PDG ID"  , "# events (2018)"   ),
    Histogram("GenMuonNotFromALP_motherID"+str(i)     , "", False, True  , default_norm  , 1  , -10   , 600  , 1e-8   , 1e1   , "Gen #mu 1st mother PDG ID"  , "# events (2018)"   ),
    Histogram("GenMuonFromALP_motherID"+str(i)        , "", False, True  , default_norm  , 1  , -10   , 60   , 1e-8   , 1e1   , "Gen #mu 1st mother PDG ID"  , "# events (2018)"   ),
  )

for method in genMuonMatchingMethods:
  for genmuonCollectionName in genmuonCollectionNames:
    collectionName = genmuonCollectionName+method+"Match"
    histograms_genALPs += (
      Histogram("Event_n"+collectionName       , "", False, True  , default_norm     , 1  , 0     , 6     , 1e-6  , 1e4   , "Number of loose #mu"                   , "# events (2018)"   ),
      Histogram(collectionName+"_pt"           , "", False, True  , default_norm     , 20 , 0     , 500   , 1e-6  , 1e2   , "loose #mu p_{T} [GeV]"                 , "# events (2018)"   ),
      Histogram(collectionName+"_eta"          , "", False, True  , default_norm     , 10 , -3    , 3     , 1e-6  , 1e2   , "loose #mu #eta"                        , "# events (2018)"   ),
      Histogram(collectionName+"_phi"          , "", False, True  , default_norm     , 10 , -3    , 3     , 1e-6  , 1e2   , "loose #mu #phi"                        , "# events (2018)"   ),
      Histogram(collectionName+"_dxyPVTraj"    , "", False, True  , default_norm     , 20 , -100  , 100   , 1e-6  , 1e2   , "loose #mu d_{xy} [cm]"                 , "# events (2018)"   ),
      Histogram(collectionName+"_dxyPVTrajErr" , "", False, True  , default_norm     , 20 , 0     , 200   , 1e-6  , 1e2   , "loose #mu #sigma_{dxy} [cm]"           , "# events (2018)"   ),
      Histogram(collectionName+"_dxyPVTrajSig" , "", False, True  , default_norm     , 20 , 0     , 200   , 1e-6  , 1e2   , "loose #mu d_{xy} / #sigma_{dxy}"       , "# events (2018)"   ),
      Histogram(collectionName+"_ip3DPVSigned"    , "", False, True  , default_norm  , 100, -500  , 500   , 1e-6  , 1e2   , "loose #mu 3D IP [cm]"                  , "# events (2018)"   ),
      Histogram(collectionName+"_ip3DPVSignedErr" , "", False, True  , default_norm  , 20 , 0     , 200   , 1e-6  , 1e2   , "loose #mu #sigma_{3DIP} [cm]"          , "# events (2018)"   ),
      Histogram(collectionName+"_ip3DPVSignedSig" , "", False, True  , default_norm  , 20 , 0     , 200   , 1e-6  , 1e2   , "loose #mu 3D IP / #sigma_{3DIP}"       , "# events (2018)"   ),
      Histogram(collectionName+"_invMass"      , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-6  , 1e2   , "loose m_{#mu #mu} [GeV]"               , "# events (2018)"   ),
      Histogram(collectionName+"_deltaR"       , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-6  , 1e2   , "loose #Delta R (#mu #mu)"              , "# events (2018)"   ),
      Histogram(collectionName+"_outerDeltaR"  , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-6  , 1e2   , "loose outer #Delta R (#mu #mu)"        , "# events (2018)"   ),
      Histogram(collectionName+"_genMuonMinDR" , "", False, True  , default_norm     , 1  , 0     , 0.4   , 1e-6  , 1e2   , "min #Delta R (loose #mu, gen #mu)"              , "# events (2018)"   ),
      # Histogram(collectionName+"_pfRelIso04all"   , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-2  , 1e8   , "loose #mu I_{PF}^{rel} ( #Delta R < 0.4 )"      , "# events (2018)"   ),
      # Histogram(collectionName+"_tkRelIso"        , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-2  , 1e8   , "loose #mu I_{tk}^{rel} ( #Delta R < 0.3 )"      , "# events (2018)"   ),
      Histogram("GenMuonFromALP_LooseMuons"+method+"MatchMinDR"   , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta R (gen #mu, loose #mu)"         , "# events (2018)"   ),
      Histogram("GenMuonFromALP_LooseMuons"+method+"MatchMinDPhi" , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta #Phi (gen #mu, loose #mu)"      , "# events (2018)"   ),
      Histogram("GenMuonFromALP_LooseMuons"+method+"MatchMinDEta" , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta #eta (gen #mu, loose #mu)"      , "# events (2018)"   ),
    )
  for genmuonVertexCollectionName in genmuonVertexCollectionNames:
    muonVertexCollectionName = genmuonVertexCollectionName+method+"MatchVertex"
    for category in muonVertexCategories:
      histograms_genALPs += (
        Histogram("Event_n"+muonVertexCollectionName+category               , "", False, True  , default_norm        , 1  , 0     , 4     , 1e-3  , 1e6   , "Number of loose #mu vertices"           , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_Lxy"                  , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex L_{xy} [cm]"                 , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_vxySigma"             , "", False, True  , default_norm        , 50 , 0     , 100   , 1e-3  , 1e6   , "#mu vertex #sigma_{vxy} [cm]"           , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_vxySignificance"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex v_{xy} / #sigma_{vxy}"       , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_dR"                   , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-4  , 1e6   , "#mu vertex #Delta R"                    , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_proxDR"               , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-4  , 1e6   , "#mu vertex proximity #Delta R"          , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_outerDR"              , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-4  , 1e6   , "#mu vertex outer #Delta R"              , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_dEta"                 , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-3  , 1e6   , "#mu vertex #Delta #eta"                 , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_outerDEta"            , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-3  , 1e6   , "#mu vertex outer #Delta #eta"           , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_dPhi"                 , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-3  , 1e6   , "#mu vertex #Delta #phi"                 , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_outerDPhi"            , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-3  , 1e6   , "#mu vertex outer #Delta #phi"           , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_normChi2"             , "", False, True  , default_norm        , 100, 0     , 5     , 1e-6  , 1e1   , "#mu vertex #chi^{2}/ndof"               , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_chargeProduct"        , "", False, True  , default_norm        , 1  , -1    , 2     , 1e-5  , 1e6   , "Dimuon charge"                          , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_maxHitsInFrontOfVert" , "", False, True  , default_norm        , 1  , 0     , 30    , 1e-6  , 1e3   , "Max N(hits in front of vertex)"    , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_maxMissHitsAfterVert" , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-3  , 1e6   , "max hits after #mu vertex fit"          , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_dca"                  , "", False, True  , default_norm        , 20 , 0     , 15    , 1e-6  , 1e4   , "DCA(#mu#mu) [cm]"                               , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_absCollinearityAngle" , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-5  , 1e2   , "#mu vertex |#Delta #Phi|"               , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_absPtLxyDPhi1"        , "", False, False , default_norm        , 10 , 0     , 3.15  , 0     , 0.25  , "#mu vertex |#Delta #phi_{#mu1}|"        , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_absPtLxyDPhi2"        , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-6  , 1e3   , "#mu vertex |#Delta #phi_{#mu2}|"        , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_invMass"              , "", False, True  , default_norm        , 20 , 0     , 10    , 1e-6  , 1e3   , "#mu vertex M_{#mu #mu} [GeV]"                 , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_pt"                   , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex p_{T} [GeV]"                 , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_leadingPt"            , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex leading p_{T} [GeV]"         , "# events (2018)"   ),
        # Histogram(muonVertexCollectionName+category+"_subleadingPt"         , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex subleading p_{T} [GeV]"      , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_dxyPVTraj1"           , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} [cm]"             , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_dxyPVTraj2"           , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} [cm]"             , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_minDxyPVTraj"         , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex min d_{xy} [cm]"             , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_maxDxyPVTraj"         , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex max d_{xy} [cm]"             , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig1"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} / #sigma_{dxy}^{1}"  , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig2"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} / #sigma_{dxy}^{2}"  , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_minDxyPVTrajSig"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex min d_{xy} / #sigma_{dxy}"   , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_maxDxyPVTrajSig"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex max d_{xy} / #sigma_{dxy}"   , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Dimuon1"      , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-6  , 1e6   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Dimuon1"      , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-6  , 1e6   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Dimuon2"      , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-6  , 1e6   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Dimuon2"      , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-6  , 1e6   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Muon1"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e6   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Muon1"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e6   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Muon2"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e6   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Muon2"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e6   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
        # Histogram(muonVertexCollectionName+category+"_pfRelIso04all1"                  , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-8  , 1e6   , "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
        # Histogram(muonVertexCollectionName+category+"_pfRelIso04all2"                  , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-8  , 1e6   , "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
        # Histogram(muonVertexCollectionName+category+"_tkRelIsoMuon1"                   , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{1} I_{tk}^{rel} ( #Delta R < 0.3 )"    , "# events (2018)"   ),
        # Histogram(muonVertexCollectionName+category+"_tkRelIsoMuon2"                   , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{2} I_{tk}^{rel} ( #Delta R < 0.3 )"    , "# events (2018)"   ),
      )

histogramsRatio_plots = [

  # ( Histogram("SegmentDRMatchMuon_pt"                   , "", False, False  , default_norm   , 40 , 0     , 500   , 0    , 1.5 , "p_{T}^{#mu} [GeV]"         , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_pt"                     , "", False, False  , default_norm   , 40 , 0     , 500   , 0    , 1.5 , "p_{T}^{#mu} [GeV]"         , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentDRMatchMuon_eta"                  , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#eta^{#mu}"                , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_eta"                    , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#eta^{#mu}"                , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentDRMatchMuon_phi"                  , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#phi^{#mu}"                , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_phi"                    , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#phi^{#mu}"                , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentDRMatchMuon_dxyPVTraj"            , "", False, False  , default_norm   , 1  , 0     , 5     , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_dxyPVTraj"              , "", False, False  , default_norm   , 1  , 0     , 5     , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentDRMatchMuon_dxyPVTrajSig"         , "", False, False  , default_norm   , 50 , 0     , 250   , 0    , 1.5 , "d_{xy}^{#mu} / #sigma_{dxy}^{#mu}" , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_dxyPVTrajSig"           , "", False, False  , default_norm   , 50 , 0     , 250   , 0    , 1.5 , "d_{xy}^{#mu} / #sigma_{dxy}^{#mu}" , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentDRMatchMuon_ip3DPVSigned"         , "", False, False  , default_norm   , 50 , 0     , 500   , 0    , 1.5 , "#mu 3D IP [cm]"            , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_ip3DPVSigned"           , "", False, False  , default_norm   , 50 , 0     , 500   , 0    , 1.5 , "#mu 3D IP [cm]"            , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentDRMatchMuon_ip3DPVSignedSig"      , "", False, False  , default_norm   , 50 , 0     , 200   , 0    , 1.5 , "#mu 3D IP / #sigma_{3DIP}" , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_ip3DPVSignedSig"        , "", False, False  , default_norm   , 50 , 0     , 200   , 0    , 1.5 , "#mu 3D IP / #sigma_{3DIP}" , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentDRMatchMuon_matchingRatio"        , "", False, False  , default_norm   , 10 , 0     , 1.033 , 0    , 1.5 , "Muon segment matches / DSA segments"    , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_matchingRatio"          , "", False, False  , default_norm   , 10 , 0     , 1.033 , 0    , 1.5 , "Muon segment matches / DSA segments"    , "Outer #Delta R-matched efficiency"   ) ),
  
  # ( Histogram("SegmentOuterDRMatchMuon_pt"              , "", False, False  , default_norm   , 40 , 0     , 500   , 0    , 1.5 , "p_{T}^{#mu} [GeV]"         , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_pt"                     , "", False, False  , default_norm   , 40 , 0     , 500   , 0    , 1.5 , "p_{T}^{#mu} [GeV]"         , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentOuterDRMatchMuon_eta"             , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#eta^{#mu}"                , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_eta"                    , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#eta^{#mu}"                , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentOuterDRMatchMuon_phi"             , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#phi^{#mu}"                , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_phi"                    , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#phi^{#mu}"                , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentOuterDRMatchMuon_dxyPVTraj"       , "", False, False  , default_norm   , 1  , 0     , 5     , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_dxyPVTraj"              , "", False, False  , default_norm   , 1  , 0     , 5     , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentOuterDRMatchMuon_dxyPVTrajSig"    , "", False, False  , default_norm   , 50 , 0     , 250   , 0    , 1.5 , "d_{xy}^{#mu} / #sigma_{dxy}^{#mu}" , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_dxyPVTrajSig"           , "", False, False  , default_norm   , 50 , 0     , 250   , 0    , 1.5 , "d_{xy}^{#mu} / #sigma_{dxy}^{#mu}" , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentOuterDRMatchMuon_ip3DPVSigned"    , "", False, False  , default_norm   , 50 , 0     , 500   , 0    , 1.5 , "#mu 3D IP [cm]"            , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_ip3DPVSigned"           , "", False, False  , default_norm   , 50 , 0     , 500   , 0    , 1.5 , "#mu 3D IP [cm]"            , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentOuterDRMatchMuon_ip3DPVSignedSig" , "", False, False  , default_norm   , 50 , 0     , 200   , 0    , 1.5 , "#mu 3D IP / #sigma_{3DIP}" , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_ip3DPVSignedSig"        , "", False, False  , default_norm   , 50 , 0     , 200   , 0    , 1.5 , "#mu 3D IP / #sigma_{3DIP}" , "Outer #Delta R-matched efficiency"   ) ),
  # ( Histogram("SegmentOuterDRMatchMuon_matchingRatio"   , "", False, False  , default_norm   , 10 , 0     , 1.033 , 0    , 1.5 , "Muon segment matches / DSA segments"    , "Outer #Delta R-matched efficiency"   ),
  #   Histogram("SegmentMatchMuon_matchingRatio"          , "", False, False  , default_norm   , 10 , 0     , 1.033 , 0    , 1.5 , "Muon segment matches / DSA segments"    , "Outer #Delta R-matched efficiency"   ) ),
]

histogramsRatio = []
if plot_ratio_hists:
  histogramsRatio = histogramsRatio_plots

if plots_from_LLPNanoAOD:
  histograms += LLPnanoAOD_histograms

if plot_genALP_info:
  histograms = histograms + histograms_genALPs

if plot_muonMatching_info:
  histograms = histograms + histograms_muonMatching

histograms2D = ()

if plots_from_LLPNanoAOD:
  histograms2D = histograms2D + histograms2D_LLPnanoAOD

if plot_genALP_info:
  histograms2D = histograms2D + histograms2D_genALPs

if plot_muonMatching_info:
  histograms2D = histograms2D + histograms2D_muonMatching

weightsBranchName = "genWeight"

color_palette_wong = (
    TColor.GetColor(230, 159, 0),
    TColor.GetColor(86, 180, 233),
    TColor.GetColor(0, 158, 115),
    TColor.GetColor(0, 114, 178),
    TColor.GetColor(213, 94, 0),
)

color_palette_petroff_6 = ["#5790fc", "#f89c20", "#e42536", "#964a8b", "#9c9ca1", "#7a21dd"]
color_palette_petroff_8 = ["#1845fb", "#ff5e02", "#c91f16", "#c849a9", "#adad7d", "#86c8dd", "#578dff", "#656364"]
color_palette_petroff_10 = ["#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70", "#717581", "#92dadd"]

data_samples = (
  # Data
  Sample(
    name="SingleMuon",
    file_path=f"{base_path}/collision_data2018/SingleMuon2018B/{skim}/{hist_path}/histograms.root",
    type=SampleType.data,
    cross_sections=cross_sections,
    line_alpha=1,
    fill_alpha=0,
    marker_size=0.7,
    marker_style=20,
    marker_color=ROOT.kBlack,
    legend_description="SingleMuon2018",
  ),
)

signal_samples = (
  
  # Signal
  # # Sample(
  # #   name="tta_mAlp-0p35GeV_ctau-1e-5mm",
  # #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e-5mm/{skim}/{hist_path}/histograms.root",
  # #   type=SampleType.signal,
  # #   cross_sections=cross_sections,
  # #   line_alpha=1,
  # #   line_style=1,
  # #   fill_alpha=0,
  # #   marker_size=0,
  # #   line_color=ROOT.kMagenta,
  # #   legend_description="m_{a} = 0.35 GeV, c#tau_{a} = 10 nm",
  # # ),
  
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e0mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e0mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kCyan,
  #   legend_description="m_{a} = 0.35 GeV, c#tau_{a} = 1 mm",
  # ),
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e1mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e1mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kCyan,
  #   legend_description="m_{a} = 0.35 GeV, c#tau_{a} = 1 cm",
  # ),
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e2mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e2mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kOrange,
  #   legend_description="m_{a} = 0.35 GeV, c#tau_{a} = 10 cm",
  # ),
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e3mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e3mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kOrange,
  #   legend_description="m_{a} = 0.35 GeV, c#tau_{a} = 1 m",
  # ),
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e5mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e5mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1, 
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kOrange,
  #   legend_description="m_{a} = 0.35 GeV, c#tau_{a} = 100 m",
  # ),

  Sample(
    name="tta_mAlp-1GeV_ctau-1e0mm",
    file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e0mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kBlue,
    legend_description="m_{a} = 1 GeV, c#tau_{a} = 1 mm",
  ),
  Sample(
    name="tta_mAlp-1GeV_ctau-1e1mm",
    file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e1mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kGreen+1,
    legend_description="m_{a} = 1 GeV, c#tau_{a} = 1 cm",
  ),
  Sample(
    name="tta_mAlp-1GeV_ctau-1e2mm",
    file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e2mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kOrange+1,
    legend_description="m_{a} = 1 GeV, c#tau_{a} = 10 cm",
  ),
  # Sample(
  #   name="tta_mAlp-1GeV_ctau-1e3mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e3mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kRed+1,
  #   legend_description="m_{a} = 1 GeV, c#tau_{a} = 1 m",
  # ),
  # Sample(
  #   name="tta_mAlp-1GeV_ctau-1e5mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e5mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1, 
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kRed+2,
  #   legend_description="m_{a} = 1 GeV, c#tau_{a} = 100 m",
  # ),
)

background_samples = (
  
  # Backgrounds
  Sample(
    name="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kRed+1,
    fill_color=TColor.GetColor(color_palette_petroff_10[0]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description="tt (semi-leptonic)",
  ),
  
  Sample(
    name="TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTToHadronic/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kRed+3,
    fill_color=TColor.GetColor(color_palette_petroff_10[1]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description="tt (hadronic)",
  ),
    
  Sample(
    name="TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTTo2L2Nu/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kRed+4,
    fill_color=TColor.GetColor(color_palette_petroff_10[2]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description="tt (leptonic)",
  ),
  
  Sample(
    name="ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/ST_tW_top/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[1],
    fill_color=TColor.GetColor(color_palette_petroff_10[3]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="Single top (tW)",
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-1*legend_height, legend_max_x-legend_width, legend_max_y-0*legend_height, "f")
  ),
  Sample(
    name="ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/ST_tW_antitop/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[1],
    fill_color=TColor.GetColor(color_palette_petroff_10[3]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),

  Sample(
    name="ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
    file_path=f"{base_path}/backgrounds2018/ST_t-channel_top/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[2],
    fill_color=TColor.GetColor(color_palette_petroff_10[4]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="Single top (t-ch.)",
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-2*legend_height, legend_max_x-legend_width, legend_max_y-1*legend_height, "f")
  ),
  Sample(
    name="ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
    file_path=f"{base_path}/backgrounds2018/ST_t-channel_antitop/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[2],
    fill_color=TColor.GetColor(color_palette_petroff_10[4]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  
  Sample(
    name="DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
    file_path=f"{base_path}/backgrounds2018/DYJetsToMuMu_M-10to50/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kMagenta+1,
    fill_color=TColor.GetColor(color_palette_petroff_10[5]),
    fill_alpha=0.7,
    marker_size=0,
    # legend_description="DY",
    # custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-3*legend_height, legend_max_x-legend_width, legend_max_y-2*legend_height, "f"),
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, ""),
  ),
  Sample(
    name="DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
    file_path=f"{base_path}/backgrounds2018/DYJetsToMuMu_M-50/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kMagenta+1,
    fill_color=TColor.GetColor(color_palette_petroff_10[5]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="DY",
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-3*legend_height, legend_max_x-legend_width, legend_max_y-2*legend_height, "f"),
    # legend_description=" ",
    # custom_legend=Legend(0, 0, 0, 0, ""),
  ),
  
  Sample(
    name="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
    file_path=f"{base_path}/backgrounds2018/WJetsToLNu/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kViolet+1,
    fill_color=TColor.GetColor(color_palette_petroff_10[6]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="W+jets",
  ),
  
  Sample(
    name="TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTZToLLNuNu_M-10/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kYellow+3,
    fill_color=TColor.GetColor(color_palette_petroff_10[7]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="ttZ",
  ),
  Sample(
    name="TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTZToLL_M-1to10/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kGray,
    fill_color=TColor.GetColor(color_palette_petroff_10[8]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="ttZ (1-10)",
  ),
  
  Sample(
    name="TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTWJetsToLNu/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kYellow+1,
    fill_color=TColor.GetColor(color_palette_petroff_10[9]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="ttW",
  ),
  
  Sample(
    name="ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/ttHTobb/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[4],
    fill_color=TColor.GetColor(color_palette_petroff_8[0]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description="ttH (bb)",
  ),
  Sample(
    name="ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/ttHToNonbb/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kBlue+1,
    fill_color=TColor.GetColor(color_palette_petroff_8[1]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description="ttH (non-bb)",
  ),
  
  Sample(
    name="TTZZ_TuneCP5_13TeV-madgraph-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTZZ/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kGray+1,
    fill_color=TColor.GetColor(color_palette_petroff_8[2]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="ttZZ",
  ),
  Sample(
    name="TTZH_TuneCP5_13TeV-madgraph-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTZH/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kGray+2,
    fill_color=TColor.GetColor(color_palette_petroff_8[3]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="ttZH",
  ),
  Sample(
    name="TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTTT/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=ROOT.kGray+3,
    fill_color=TColor.GetColor(color_palette_petroff_8[4]),
    fill_alpha=0.7,
    marker_size=0,
    legend_description="TTTT",
  ),
    
  Sample(
    name="QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-15To20/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  Sample(
    name="QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-20To30/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  Sample(
    name="QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-30To50/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  Sample(
    name="QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-50To80/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  Sample(
    name="QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-80To120/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
  #   fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  Sample(
    name="QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-120To170/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    # legend_description="QCD (#mu enriched)",
    # custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, ""),
  ),
  Sample(
    name="QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-170To300/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description="QCD (#mu enriched)",
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
    # legend_description=" ",
    # custom_legend=Legend(0, 0, 0, 0, ""),
  ),
  Sample(
    name="QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-300To470/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  Sample(
    name="QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-470To600/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  Sample(
    name="QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-600To800/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  Sample(
    name="QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-800To1000/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    # legend_description="QCD (#mu enriched)",
    # custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  Sample(
    name="QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-1000/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    # fill_color=color_palette_wong[0],
    fill_color=TColor.GetColor(color_palette_petroff_8[5]),
    fill_alpha=1.0,
    marker_size=0,
    legend_description="QCD (#mu enriched)",
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
    # legend_description=" ",
    # custom_legend=Legend(0, 0, 0, 0, "")
  ),
)

if plot_data:
  samples = data_samples
else: 
  samples = signal_samples
if plot_background:
  samples = samples + background_samples


# custom_stacks_order = (
  # "SingleMuon",
  
  
  # "ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8",
  # "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
  # "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
  
  # "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
  # "TTZH_TuneCP5_13TeV-madgraph-pythia8",
  # "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
  
  # "ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8",
  # "ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8",
  # "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",
  
  # "DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
  # "DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
  
  # "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
  # "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
  
  
  # "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
  # "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
  
  # "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
  # "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
  
  # "QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  # "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  # "QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  # "QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  # "QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  # "QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  # "QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  # "QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  # "QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  # "QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  # "QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  # "QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  
  # "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
  # "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
  # "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
  
  # "tta_mAlp-0p35GeV_ctau-1e-5mm",
  # "tta_mAlp-0p35GeV_ctau-1e0mm",
  # "tta_mAlp-0p35GeV_ctau-1e1mm",
  # "tta_mAlp-0p35GeV_ctau-1e2mm",
  # "tta_mAlp-0p35GeV_ctau-1e3mm",
  # "tta_mAlp-0p35GeV_ctau-1e5mm",

  # "tta_mAlp-1GeV_ctau-1e-5mm",
  # "tta_mAlp-1GeV_ctau-1e0mm",
  # "tta_mAlp-1GeV_ctau-1e1mm",
  # "tta_mAlp-1GeV_ctau-1e2mm",
  # "tta_mAlp-1GeV_ctau-1e3mm",
  # "tta_mAlp-1GeV_ctau-1e5mm",
# )
