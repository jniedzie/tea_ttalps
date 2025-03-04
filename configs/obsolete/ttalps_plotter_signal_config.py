import ROOT
from ROOT import TColor
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from ttalps_cross_sections import *

year = "2018"
cross_sections = get_cross_sections(year)

base_path = "/data/dust/user/lrygaard/ttalps_cms/"

# Default settings
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
# SR dimuon cuts applied
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons"
# JPsi dimuon cuts applied
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_JPsiDimuons"

# Loose semimuonic skim
# skim = "skimmed_looseSemimuonicv1"
# For signal like skim: SR and J/Psi CR with no isolation requirement on the loose muons
skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"

output_formats = ["pdf"]

# luminosity = 63670. # pb^-1
luminosity = 59830. # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2
lumi_label_value = luminosity

canvas_size = (800, 600)
canvas_size_2Dhists = (800, 800)
show_ratio_plots = False
ratio_limits = (0.5, 1.5)

legend_width = 0.17 if show_ratio_plots else 0.23
legend_min_x = 0.45
legend_max_x = 0.82
legend_height = 0.045 if show_ratio_plots else 0.03
legend_max_y = 0.89

# Minimuon requirements on number of background events to be uncluded in plots
# requierement is # events >= bkgRawEventsThreshold
bkgRawEventsThreshold = 1

n_default_backgrounds = 10

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Private Work"

## SETTINGS ##
plots_from_LLPNanoAOD = True
plot_genALP_info = False
plot_genCollinearityStudy = False
plot_genMuonFromTopStudy = False
plot_muonMatching_info = False
plot_background = True
plot_data = False


# To include plots with collection names "LooseMuons"+muonMatchingMethods+"Match"
muonMatchingMethods = [
#   # # "DR", 
#   # # "OuterDR", 
#   # # "ProxDR", 
  "Segment"
]

# for genALP plots
genMuonMatchingMethods = [
  "Segment"
]

extraMuonVertexCollections = [
  # invariant mass cut only:
  # # "MaskedDimuonVertices", 
  # Good Dimuon selection without isolation cut:
  # # "GoodDimuonVertices", 
  # "BestDimuonVertex", 
  # Good Dimuon selection with isolation cut:
  "BestPFIsoDimuonVertex",
]

dimuonNminus1CollectionNames = [
  "BestPFIsoDimuonVertexNminus1",
]

signal_legend = Legend(legend_max_x-legend_width, legend_max_y-5*legend_height, legend_max_x-2*legend_width, legend_max_y, "l")
sampletype = "sig"

if plot_background:
  plot_genALP_info = False
  signal_legend = Legend(legend_max_x-2.5*legend_width, legend_max_y-0.13-5*legend_height, legend_max_x-2*legend_width, legend_max_y-0.13, "l")
  sampletype = "bkg"

if plot_data:
  plot_genALP_info = False
  signal_legend = Legend(legend_max_x-2.5*legend_width, legend_max_y-0.13-3*legend_height, legend_max_x-2*legend_width, legend_max_y-0.13, "l")
  sampletype = "data"

legends = {
  SampleType.signal: signal_legend,
  SampleType.background: Legend(legend_max_x-legend_width, legend_max_y-n_default_backgrounds*legend_height, legend_max_x, legend_max_y, "f"),
  SampleType.data: Legend(legend_max_x-3*(legend_width), legend_max_y-legend_height, legend_max_x-2*(legend_width), legend_max_y, "pl"),
}

output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{sampletype}/"

background_uncertainty_style = 3244 # available styles: https://root.cern.ch/doc/master/classTAttFill.html
background_uncertainty_color = ROOT.kBlack
background_uncertainty_alpha = 0.3

plotting_options = {
  SampleType.background: "hist",
  SampleType.signal: "nostack hist",
  SampleType.data: "nostack e",
}

default_norm = NormalizationType.to_lumi

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
  
  Histogram("cutFlow"                                 , "", False, True  , default_norm , 1  , 0     , 13     , 1e1   , 1e23   , "Selection"                      , "Number of events"  ),  
  Histogram("dimuonCutFlow_BestPFIsoDimuonVertex"       , "", False, True  , default_norm , 1  , 0     , 11     , 1e3           , 1e9            , "Selection"                      , "Number of events"  ),
  Histogram("Event_normCheck"                         , "", False, True  , default_norm , 1  , 0     , 1      , 1e-1*y_scale  , 1e20*y_scale   , "norm check"                     , "# events (2018)"   ),
)

LLPnanoAOD_histograms = ()
histograms2D_LLPnanoAOD = ()

muonVertexCategories = ["_PatDSA", "_DSA", "_Pat"]
muonCollectionCategories = ["", "DSA", "PAT"]
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
    Histogram(muonCollectionName+"_absDxyPVTraj"    , "", False, True  , default_norm        , 100, -300  , 300   , 1e-3  , 1e6   , "loose #mu |d_{xy}| [cm]"                        , "# events (2018)"   ),
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
  LLPnanoAOD_histograms += (
    Histogram(muonVertexCollectionName+"_Lxy"                  , "", False, True  , default_norm        , 20 , 0     , 800   , 1e-4  , 1e9   , "#mu vertex L_{xy} [cm]"                 , "# events (2018)"   ),
    Histogram(muonVertexCollectionName+"_logLxy"               , "", False, True  , default_norm        , 10 , -5    , 3     , 1e-4  , 1e9   , "#mu vertex log_{10}(L_{xy}) [cm]"                 , "# events (2018)"   ),
    Histogram(muonVertexCollectionName+"_invMass"              , "", False, True  , default_norm        , 10, 0      , 10    , 1e-5  , 1e6   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
    Histogram(muonVertexCollectionName+"_logInvMass"           , "", False, True  , default_norm        , 10 , -1     , 2   , 1e-6  , 1e7   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
  )
  for category in muonVertexCategories:
    LLPnanoAOD_histograms += (
      Histogram("Event_n"+muonVertexCollectionName+category               , "", False, True  , default_norm        , 1  , 0     , 45    , 1e-4  , 1e3   , "Number of loose #mu vertices"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_Lxy"                  , "", False, True  , default_norm        , 20 , 0     , 800   , 1e-4  , 1e9   , "#mu vertex L_{xy} [cm]"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_LxySigma"             , "", False, True  , default_norm        , 100, 0     , 100   , 1e-5  , 1e4   , "#mu vertex #sigma_{Lxy} [cm]"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_LxySignificance"      , "", False, True  , default_norm        , 2  , 0     , 150   , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"       , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_vxySigma"             , "", False, True  , default_norm        , 50 , 0     , 100   , 1e-3  , 1e6   , "#mu vertex #sigma_{Vxy} [cm]"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_vxySignificance"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex V_{xy} / #sigma_{Vxy}"       , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_hitsInFrontOfVert1"   , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-6  , 1e6   , "N(hits before vertex)"                  , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_hitsInFrontOfVert2"   , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-7  , 1e5   , "N(hits before vertex)"                  , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_invMass"              , "", False, True  , default_norm        , 10, 0      , 10    , 1e-5  , 1e6   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_logInvMass"           , "", False, True  , default_norm        , 10 , -1     , 2     , 1e-5  , 1e6   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_pt"                   , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex p_{T} [GeV]"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_leadingPt"            , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex leading p_{T} [GeV]"         , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dxyPVTraj1"           , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} [cm]"             , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dxyPVTraj2"           , "", False, True  , default_norm        , 20 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} [cm]"             , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig1"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} / #sigma_{dxy}^{1}"  , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig2"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} / #sigma_{dxy}^{2}"  , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_3Dangle"                , "", False, True  , default_norm        , 10 , 0      , 3.5  , 1e-4  , 1e6   , "#mu vertex #alpha"                      , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_cos3Dangle"             , "", False, True  , default_norm        , 5  , -1     , 1    , 1e-4  , 1e7   , "#mu vertex cos #alpha"                  , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_deltaPixelHits"       , "", False, True  , default_norm        , 1  , 0      , 15   , 1e-3  , 1e6   , "#mu vertex #Delta(Pixel Hits)"          , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_nSegments"            , "", False, True  , default_norm        , 1  , 0      , 20   , 1e-4  , 1e7   , "#mu vertex N(Segments)"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_nSegments1"           , "", False, True  , default_norm        , 1  , 0      , 20   , 1e-4  , 1e7   , "#mu_{1} vertex N(Segments)"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_nSegments2"           , "", False, True  , default_norm        , 1  , 0      , 20   , 1e-4  , 1e7   , "#mu_{2} vertex N(Segments)"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_nDTHits"              , "", False, True  , default_norm        , 1  , 0      , 50   , 1e-4  , 1e8   , "#mu vertex N(DT Hits)"                  , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_nDTHits1"             , "", False, True  , default_norm        , 1  , 0      , 50   , 1e-4  , 1e8   , "#mu_{1} vertex N(DT Hits)"              , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_nDTHits2"             , "", False, True  , default_norm        , 1  , 0      , 50   , 1e-4  , 1e8   , "#mu_{2} vertex N(DT Hits)"              , "# events (2018)"   ),
    )

for dimuonCollectionName in dimuonNminus1CollectionNames:
  Histogram(dimuonCollectionName+"_logInvMass"                  , "", True,  True  , default_norm        , 1  , 0.1   , 100  , 1e-4  , 1e7   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
  for category in muonVertexCategories:
    LLPnanoAOD_histograms += (
      Histogram(dimuonCollectionName+category+"_invMass"                     , "", False, True  , default_norm        , 10 , 0     , 10   , 1e-4  , 1e7   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_logInvMass"                  , "", True,  True  , default_norm        , 1  , 0.1   , 100  , 1e-4  , 1e7   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_chargeProduct"               , "", False, True  , default_norm        , 1  , -1    , 2    , 1e-2  , 1e10  , "Dimuon charge"                          , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_maxHitsInFrontOfVert"        , "", False, True  , default_norm        , 1  , 0     , 35   , 1e-3  , 1e9   , "Max N(hits before vertex)"              , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_absPtLxyDPhi1"               , "", False, True  , default_norm        , 10 , 0     , 3.15 , 1e-3  , 1e9   , "#mu vertex |#Delta #phi_{#mu1}|"        , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_dca"                         , "", False, True  , default_norm        , 20 , 0     , 15   , 1e-4  , 1e9   , "DCA [cm]"                               , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_absCollinearityAngle"        , "", False, True  , default_norm        , 10 , 0     , 3.15 , 1e-3  , 1e9   , "#mu vertex |#Delta #Phi|"               , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_normChi2"                    , "", False, True  , default_norm        , 1000,0     , 100  , 1e-5  , 1e6   , "#mu vertex #chi^{2}/ndof"               , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_pfRelIso1"                   , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-3  , 1e9   , "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
      Histogram(dimuonCollectionName+category+"_pfRelIso2"                   , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-3  , 1e9   , "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
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
  Histogram("Event_nGenMuonFromALP"               , "", False, True  , default_norm     , 1  , 0     , 4     , 1e-6   , 1e4   , "# Gen #mu from ALP"     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_pdgId"                , "", False, True  , default_norm     , 1  , -100  , 100   , 1e-2   , 1e4   , "Gen #mu particle ID"                    , "# events (2018)"   ),
  Histogram("GenMuonFromALP_Lxy"                  , "", False, True  , default_norm     , 200, 0     , 1000  , 1e-8   , 1e1   , "Gen #mu L_{xy} [cm]"                    , "# events (2018)"   ),
  Histogram("GenMuonFromALP_properLxy"            , "", False, True  , default_norm     , 1  , 0     , 1     , 1e-6   , 1e2   , "Gen proper #mu L_{xy} [cm]"             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_properLxyT"           , "", False, True  , default_norm     , 1  , 0     , 1     , 1e-6   , 1e2   , "Gen proper #mu L_{xy} [cm]"             , "# events (2018)"   ),
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
)

histograms_genCollinearityStudy = (
  Histogram("GenMuonFromALP_index1"               , "", False, True  , default_norm     , 1  , 0     , 40    , 1e-4   , 1e3   , "Leading #mu from ALP index"             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_index2"               , "", False, True  , default_norm     , 1  , 0     , 40    , 1e-4   , 1e3   , "Subleading #mu from ALP index"          , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatchVertex_genPlaneAngle"            , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatchVertex_recoPlaneAngle"           , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatchVertex_etaSum"                   , "", False, True  , default_norm     , 10 , 0     , 7     , 1e-6   , 1e1   , "Dimuon |#eta^{#mu1}| + |#eta^{#mu2}|" , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmaxdPhi2SegmentMatchVertex_genPlaneAngle"    , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmaxdPhi2SegmentMatchVertex_recoPlaneAngle"   , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmaxdPhi2SegmentMatchVertex_etaSum"           , "", False, True  , default_norm     , 10 , 0     , 7     , 1e-6   , 1e1   , "Dimuon |#eta^{#mu1}| + |#eta^{#mu2}|" , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_genPlaneAngle"    , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_recoPlaneAngle"   , "", False, True  , default_norm     , 10 , 0     , 3     , 1e-6   , 1e1   , "#phi between dimuon and ALP plane"    , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_etaSum"           , "", False, True  , default_norm     , 10 , 0     , 7     , 1e-6   , 1e1   , "Dimuon |#eta^{#mu1}| + |#eta^{#mu2}|" , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_Lxy"                  , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex L_{xy} [cm]"                 , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_absCollinearityAngle" , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-5  , 1e2   , "#mu vertex |#Delta #Phi|"               , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_absPtLxyDPhi1"        , "", False, False , default_norm        , 10 , 0     , 3.15  , 0     , 0.25  , "#mu vertex |#Delta #phi_{#mu1}|"        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPmindPhi2SegmentMatchVertex_absPtLxyDPhi2"        , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-6  , 1e3   , "#mu vertex |#Delta #phi_{#mu2}|"        , "# events (2018)"   ),
)

histograms_genMuonFromTopStudy = (
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
  Histogram("LooseMuonsFromALPSegmentMatch_hasLeadingMuon"     , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from ALP"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch_hmu_hasLeadingMuon" , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from ALP"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromWSegmentMatch_hasLeadingMuon"       , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from W boson"            , "# events (2018)"   ),
  Histogram("LooseMuonsFromWSegmentMatch_hmu_hasLeadingMuon"   , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from W boson"            , "# events (2018)"   ),
  Histogram("LooseMuonsFromWSegmentMatch_hmu_hasLeadingMuon"   , "", False, True  , default_norm     , 1  , 0     , 2     , 1e-2   , 1e4   , "Leading muon from W boson"            , "# events (2018)"   ),
  Histogram("LooseMuonsFromWSegmentMatch_pt"                   , "", False, True  , default_norm     , 20 , 0     , 500   , 1e-6  , 1e2    , "loose #mu p_{T} [GeV]"                 , "# events (2018)"   ),
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
  Histogram("GenMuonFromALP1_LooseMuonsSegmentMatchMinDR"   , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta R (gen #mu_{1}, loose #mu)"         , "# events (2018)"   ),
  Histogram("GenMuonFromALP1_LooseMuonsSegmentMatchMinDPhi" , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta #Phi (gen #mu_{1}, loose #mu)"      , "# events (2018)"   ),
  Histogram("GenMuonFromALP1_LooseMuonsSegmentMatchMinDEta" , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta #eta (gen #mu_{1}, loose #mu)"      , "# events (2018)"   ),
  Histogram("GenMuonFromALP2_LooseMuonsSegmentMatchMinDR"   , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta R (gen #mu_{2}, loose #mu)"         , "# events (2018)"   ),
  Histogram("GenMuonFromALP2_LooseMuonsSegmentMatchMinDPhi" , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta #Phi (gen #mu_{2}, loose #mu)"      , "# events (2018)"   ),
  Histogram("GenMuonFromALP2_LooseMuonsSegmentMatchMinDEta" , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta #eta (gen #mu_{2}, loose #mu)"      , "# events (2018)"   ),
  Histogram("GenMuonFromALP_pt1"                  , "", False, True  , default_norm     , 20 , 0     , 500   , 1e-6  , 1e2   , "Gen #mu_{1} p_{T} [GeV]"      , "# events (2018)"   ),
  Histogram("GenMuonFromALP_pt2"                  , "", False, True  , default_norm     , 20 , 0     , 500   , 1e-6  , 1e2   , "Gen #mu_{2} p_{T} [GeV]"      , "# events (2018)"   ),
)

histograms2D_genALPs = ()

genDimuonCollectionNames = [
  "GenDimuonFromALP",
  "GenMuonNotFromALP",
  "GenDimuonNotFromALP",
]
genmuonCollectionNames = [
  "LooseMuonsFromALP",
  "LooseMuonsNotFromALP",
]
genmuonVertexCollectionNames = [
  "LooseMuonsFromALP",
  "LooseMuonsNotFromALP",
  "LooseDimuonsNotFromALP",
]
genDimuonNminus1CollectionNames = [
  "GoodPFIsoDimuonVerticesFromALPNminus1",
]
genVertexCollectionNames = [
  "GoodPFIsoDimuonVertexFromALP",
  "GoodPFIsoDimuonVertexResonancesNotFromALP",
  "GoodPFIsoDimuonVertexNonresonancesNotFromALP",
]
muonVertexCategories = ["", "_Pat", "_DSA", "_PatDSA"]

for genDimuonCollectionName in genDimuonCollectionNames:
  histograms_genALPs += (
    Histogram("Event_n"+genDimuonCollectionName                     , "", False, True  , default_norm    , 1   , 0    , 5     , 1e-7   , 1e4   , "# Gen Dimuons not from ALP"     , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_invMass"                    , "", False, True  , default_norm    , 100 , 0    , 100   , 1e-6   , 1e4   , "Gen m_{#mu #mu} [GeV]"          , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_deltaR"                     , "", False, True  , default_norm    , 10  , 0    , 3     , 1e-4   , 1e2   , "Gen #Delta R(#mu #mu)"          , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_absCollinearityAngle"       , "", False, True  , default_norm    , 10  , 0    , 3.15  , 1e-6   , 1e2   , "Gen Dimuon |#Delta #Phi|"       , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_absPtLxyDPhi1"              , "", False, True  , default_norm    , 10  , 0    , 3.15  , 1e-5   , 1e3   , "Gen |#Delta #phi_{#mu1}|"       , "# events (2018)"   ),  
    Histogram(genDimuonCollectionName+"_absPtLxyDPhi2"              , "", False, True  , default_norm    , 10  , 0    , 3.15  , 1e-5   , 1e3   , "Gen |#Delta #phi_{#mu2}|"       , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_Lxy"                        , "", False, True  , default_norm    , 100 , 0    , 700   , 1e-2   , 1e6   , "Gen #mu L_{xy} [cm]"            , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_properLxy"                  , "", False, True  , default_norm    , 100  , 0    , 700   , 1e-2   , 1e6   , "Gen #mu L_{xy} / ALP boost [cm]"             , "# events (2018)"   ),
)

for genDimuonCollectionName in genDimuonNminus1CollectionNames:
  histograms_genALPs += (
    Histogram(genDimuonCollectionName+"_invMass"                     , "", False, True  , default_norm        , 10 , 0     , 10   , 1e-4  , 1e7   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_chargeProduct"               , "", False, True  , default_norm        , 1  , -1    , 2    , 1e-2  , 1e10  , "Dimuon charge"                          , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_maxHitsInFrontOfVert"        , "", False, True  , default_norm        , 1  , 0     , 35   , 1e-3  , 1e9   , "Max N(hits before vertex)"              , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_absPtLxyDPhi1"               , "", False, True  , default_norm        , 10 , 0     , 3.15 , 1e-3  , 1e9   , "#mu vertex |#Delta #phi_{#mu1}|"        , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_dca"                         , "", False, True  , default_norm        , 20 , 0     , 15   , 1e-4  , 1e9   , "DCA [cm]"                               , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_absCollinearityAngle"        , "", False, True  , default_norm        , 10 , 0     , 3.15 , 1e-3  , 1e9   , "#mu vertex |#Delta #Phi|"               , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_normChi2"                    , "", False, True  , default_norm        , 1000,0     , 100  , 1e-5  , 1e6   , "#mu vertex #chi^{2}/ndof"               , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_pfRelIso1"                   , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-3  , 1e9   , "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
    Histogram(genDimuonCollectionName+"_pfRelIso2"                   , "", False, True  , default_norm        , 1  , 0     , 1    , 1e-3  , 1e9   , "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
  )

for muonVertexCollectionName in genVertexCollectionNames:
  for category in {"_Pat", "_PatDSA", "_DSA"}:
    histograms_genALPs += (
      Histogram(muonVertexCollectionName+category+"_Lxy"                  , "", False, True  , default_norm        , 20 , 0     , 800   , 1e-4  , 1e9   , "#mu vertex L_{xy} [cm]"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_LxySignificance"      , "", False, True  , default_norm        , 2  , 0     , 150   , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"       , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_3Dangle"                , "", False, True  , default_norm        , 10 , 0      , 3.5  , 1e-4  , 1e6   , "#mu vertex #alpha"                      , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_cos3Dangle"             , "", False, True  , default_norm        , 5  , -1     , 1    , 1e-4  , 1e7   , "#mu vertex cos #alpha"                  , "# events (2018)"   ),
    )
    histograms2D_genALPs += (
      Histogram2D(muonVertexCollectionName+category+"_Lxy_3Dangle",            "",  False,  False,  True,  NormalizationType.to_lumi,  2,  2,   0, 250,  0,3.15,  1e-5,  1e1,  "L_{xy} [cm]",  "#mu vertex #alpha",    "# events (2018)",  ""  ),
      Histogram2D(muonVertexCollectionName+category+"_Lxy_cos3Dangle",         "",  False,  False,  True,  NormalizationType.to_lumi,  2,  2,   0, 250, -1,   1,  1e-5,  1e1,  "L_{xy} [cm]",  "#mu vertex cos #alpha",    "# events (2018)",  ""  ),
    )

for i in range(1,6):
  histograms_genALPs += (
    Histogram("GenDimuonNotFromALP_motherID1"+str(i)  , "", False, True  , default_norm  , 1  , -10   , 30   , 1e-8   , 1e1   , "Gen #mu_{1} mother PDG ID"  , "# events (2018)"   ),
    Histogram("GenDimuonNotFromALP_motherID1"+str(i)  , "", False, True  , default_norm  , 1  , -10   , 30   , 1e-8   , 1e1   , "Gen #mu_{2} mother PDG ID"  , "# events (2018)"   ),
    Histogram("GenMuonNotFromALP_motherID"+str(i)     , "", False, True  , default_norm  , 1  , -10   , 600  , 1e-8   , 1e1   , "Gen #mu 1st mother PDG ID"  , "# events (2018)"   ),
    Histogram("GenMuonFromALP_motherID"+str(i)        , "", False, True  , default_norm  , 1  , -10   , 60   , 1e-2   , 1e2   , "Gen #mu 1st mother PDG ID"  , "# events (2018)"   ),
  )

for method in genMuonMatchingMethods:
  for genmuonCollectionName in genmuonCollectionNames:
    collectionName = genmuonCollectionName+method+"Match"
    histograms_genALPs += (
      Histogram("Event_n"+collectionName       , "", False, True  , default_norm     , 1  , 0     , 6     , 1e-8  , 1e6   , "Number of loose #mu"                   , "# events (2018)"   ),
      Histogram(collectionName+"_pt"           , "", False, True  , default_norm     , 20 , 0     , 500   , 1e-6  , 1e2   , "loose #mu p_{T} [GeV]"                 , "# events (2018)"   ),
      Histogram(collectionName+"_eta"          , "", False, True  , default_norm     , 10 , -3    , 3     , 1e-6  , 1e2   , "loose #mu #eta"                        , "# events (2018)"   ),
      Histogram(collectionName+"_phi"          , "", False, True  , default_norm     , 10 , -3    , 3     , 1e-6  , 1e2   , "loose #mu #phi"                        , "# events (2018)"   ),
      Histogram(collectionName+"_dxyPVTraj"    , "", False, True  , default_norm     , 20 , -100  , 100   , 1e-6  , 1e2   , "loose #mu d_{xy} [cm]"                 , "# events (2018)"   ),
      Histogram(collectionName+"_dxyPVTrajErr" , "", False, True  , default_norm     , 20 , 0     , 200   , 1e-6  , 1e2   , "loose #mu #sigma_{dxy} [cm]"           , "# events (2018)"   ),
      Histogram(collectionName+"_dxyPVTrajSig" , "", False, True  , default_norm     , 20 , 0     , 200   , 1e-6  , 1e2   , "loose #mu d_{xy} / #sigma_{dxy}"       , "# events (2018)"   ),
      Histogram(collectionName+"_ip3DPVSigned"    , "", False, True  , default_norm  , 100, -500  , 500   , 1e-6  , 1e2   , "loose #mu 3D IP [cm]"                  , "# events (2018)"   ),
      Histogram(collectionName+"_ip3DPVSignedErr" , "", False, True  , default_norm  , 20 , 0     , 200   , 1e-6  , 1e2   , "loose #mu #sigma_{3DIP} [cm]"          , "# events (2018)"   ),
      Histogram(collectionName+"_ip3DPVSignedSig" , "", False, True  , default_norm  , 20 , 0     , 200   , 1e-6  , 1e2   , "loose #mu 3D IP / #sigma_{3DIP}"       , "# events (2018)"   ),
      Histogram(collectionName+"_invMass"      , "", False, True  , default_norm     , 20 , 0     , 20    , 1e-6  , 1e2   , "loose m_{#mu #mu} [GeV]"               , "# events (2018)"   ),
      Histogram(collectionName+"_deltaR"       , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-6  , 1e2   , "loose #Delta R (#mu #mu)"              , "# events (2018)"   ),
      Histogram(collectionName+"_outerDeltaR"  , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-6  , 1e2   , "loose outer #Delta R (#mu #mu)"        , "# events (2018)"   ),
      Histogram(collectionName+"_genMuonMinDR" , "", False, True  , default_norm     , 1  , 0     , 0.4   , 1e-6  , 1e2   , "min #Delta R (loose #mu, gen #mu)"              , "# events (2018)"   ),
      Histogram("GenMuonFromALP_LooseMuons"+method+"MatchMinDR"   , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta R (gen #mu, loose #mu)"         , "# events (2018)"   ),
      Histogram("GenMuonFromALP_LooseMuons"+method+"MatchMinDPhi" , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta #Phi (gen #mu, loose #mu)"      , "# events (2018)"   ),
      Histogram("GenMuonFromALP_LooseMuons"+method+"MatchMinDEta" , "", False, True  , default_norm     , 1 , 0     , 0.5    , 1e-5  , 1e3   , "min #Delta #eta (gen #mu, loose #mu)"      , "# events (2018)"   ),
    )
  for genmuonVertexCollectionName in genmuonVertexCollectionNames:
    muonVertexCollectionName = genmuonVertexCollectionName+method+"MatchVertex"
    for category in muonVertexCategories:
      histograms_genALPs += (
        Histogram("Event_n"+muonVertexCollectionName+category               , "", False, True  , default_norm        , 1  , 0     , 4     , 1e-8  , 1e6   , "Number of loose #mu vertices"           , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_Lxy"                  , "", False, True  , default_norm        , 10 , 0     , 700   , 1e-2  , 1e6   , "Reco #mu vertex L_{xy} [cm]"                 , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_absCollinearityAngle" , "", False, False  , default_norm        , 10 , 0     , 3.15 , 0    , 6   , "#mu vertex |#Delta #Phi|"               , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_invMass"              , "", False, True  , default_norm        , 100, 0     , 100   , 1e-6  , 1e3   , "#mu vertex M_{#mu #mu} [GeV]"                 , "# events (2018)"   ),
        Histogram(muonVertexCollectionName+category+"_pt"                   , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex p_{T} [GeV]"                 , "# events (2018)"   ),
      )

if plots_from_LLPNanoAOD:
  histograms += LLPnanoAOD_histograms

if plot_genALP_info:
  histograms = histograms + histograms_genALPs

if plot_genCollinearityStudy:
  histograms = histograms + histograms_genCollinearityStudy

if plot_genMuonFromTopStudy:
  histograms = histograms + histograms_genMuonFromTopStudy

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

signal_colors = [ROOT.kBlue,ROOT.kGreen+1,ROOT.kOrange+1,ROOT.kMagenta,ROOT.kBlue+2]

signals = {
  # "tta_mAlp-0p35GeV_ctau-1e-5mm" : {"label": "m_{a} = 0.35 GeV, c#tau_{a} = 10 #mu m"},
  # "tta_mAlp-0p35GeV_ctau-1e0mm" : {"label": "m_{a} = 0.35 GeV, c#tau_{a} = 1 mm"},
  # "tta_mAlp-0p35GeV_ctau-1e1mm" : {"label": "m_{a} = 0.35 GeV, c#tau_{a} = 1 cm"},
  # "tta_mAlp-0p35GeV_ctau-1e2mm" : {"label": "m_{a} = 0.35 GeV, c#tau_{a} = 10 cm"},
  # "tta_mAlp-0p35GeV_ctau-1e3mm" : {"label": "m_{a} = 0.35 GeV, c#tau_{a} = 1 m"},
  # "tta_mAlp-1GeV_ctau-1e-5mm" : {"label": "m_{a} = 1 GeV, c#tau_{a} = 10 #mu m"},
  # "tta_mAlp-1GeV_ctau-1e0mm" : {"label": "m_{a} = 1 GeV, c#tau_{a} = 1 mm"},
  # "tta_mAlp-1GeV_ctau-1e1mm" : {"label": "m_{a} = 1 GeV, c#tau_{a} = 1 cm"},
  # "tta_mAlp-1GeV_ctau-1e2mm" : {"label": "m_{a} = 1 GeV, c#tau_{a} = 10 cm"},
  # "tta_mAlp-1GeV_ctau-1e3mm" : {"label": "m_{a} = 1 GeV, c#tau_{a} = 1 m"},
  "tta_mAlp-2GeV_ctau-1e-5mm" : {"label": "m_{a} = 2 GeV, c#tau_{a} = 10 #mu m"},
  "tta_mAlp-2GeV_ctau-1e0mm" : {"label": "m_{a} = 2 GeV, c#tau_{a} = 1 mm"},
  "tta_mAlp-2GeV_ctau-1e1mm" : {"label": "m_{a} = 2 GeV, c#tau_{a} = 1 cm"},
  "tta_mAlp-2GeV_ctau-1e2mm" : {"label": "m_{a} = 2 GeV, c#tau_{a} = 10 cm"},
  "tta_mAlp-2GeV_ctau-1e3mm" : {"label": "m_{a} = 2 GeV, c#tau_{a} = 1 m"},
  # "tta_mAlp-12GeV_ctau-1e0mm" : {"label": "m_{a} = 12 GeV, c#tau_{a} = 1 mm"},
  # "tta_mAlp-12GeV_ctau-1e1mm" : {"label": "m_{a} = 12 GeV, c#tau_{a} = 1 cm"},
  # "tta_mAlp-12GeV_ctau-1e2mm" : {"label": "m_{a} = 12 GeV, c#tau_{a} = 10 cm"},
  # "tta_mAlp-60GeV_ctau-1e0mm" : {"label": "m_{a} = 60 GeV, c#tau_{a} = 1 mm"},
  # "tta_mAlp-60GeV_ctau-1e2mm" : {"label": "m_{a} = 60 GeV, c#tau_{a} = 10 cm"},
  # "tta_mAlp-70GeV_ctau-1e0mm" : {"label": "m_{a} = 70 GeV, c#tau_{a} = 1 mm"},
}
signal_samples = ()
for i, (signal_name, signal_info) in enumerate(signals.items()):
  signal_samples += (
    Sample(
      name=signal_name,
      file_path=f"{base_path}/signals/{signal_name}/{skim}/{hist_path}/histograms.root",
      # file_path=f"{base_path}/signals_gridpack_hadronizer_test/{signal_name}/{skim}/{hist_path}/histograms.root",
      type=SampleType.signal,
      cross_sections=cross_sections,
      line_alpha=1,
      line_style=1,
      fill_alpha=0,
      marker_size=0,
      line_color=signal_colors[i],
      legend_description=signal_info["label"],
    ),
  )

background_samples = (
  
  # Backgrounds
  Sample(
    name="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
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
#   # "SingleMuon",
  
#   "ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8",
#   "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
#   "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
  
#   "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
#   "TTZH_TuneCP5_13TeV-madgraph-pythia8",
#   "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
  
#   "ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8",
#   "ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8",
#   "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",
  
#   "DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
#   "DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
  
#   "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
#   "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
  
  
#   "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
#   "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
  
#   "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
#   "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
  
#   "QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
#   "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
#   "QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
#   "QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
#   "QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#   "QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
#   "QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
#   "QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
#   "QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
#   "QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
#   "QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#   "QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  
#   "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
#   "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
#   "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
# )

# if it's just signal we can define a new custom_stacks_order
if not plot_background:
  custom_stacks_order = ()
  for signal_name, signal_info in signals.items():
    custom_stacks_order += (signal_name,)
else:
  # sometimes I don't use the custom stacks orders with background:
  if "custom_stacks_order" in globals():
    for signal_name, signal_info in signals.items():
      custom_stacks_order += (signal_name,)
