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

hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_JPsiDimuons"

# skim = "skimmed_looseSemimuonicv1"
skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"

output_formats = ["pdf"]

# luminosity = 63670. # pb^-1
luminosity = 59820. # 2018 eras A+B+C+D (A+B+C) was 27972.887358 before)
# luminosity = 59830. # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2
lumi_label_offset = 0.02
lumi_label_value = luminosity

canvas_size = (800, 600)
canvas_size_2Dhists = (800, 800)
show_ratio_plots = True
ratio_limits = (0.5, 1.5)

legend_width = 0.17 if show_ratio_plots else 0.23
legend_min_x = 0.45
legend_max_x = 0.82
legend_height = 0.045 if show_ratio_plots else 0.03
legend_max_y = 0.89

# requierement is num. events >= bkgRawEventsThreshold
bkgRawEventsThreshold = 0

n_default_backgrounds = 8

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Private Work"

## SETTINGS ##
plots_from_LLPNanoAOD = True
plot_background = True
plot_data = True

muonMatchingMethods = [
  # # "DR", 
  # # "OuterDR", 
  # # "ProxDR", 
  # "Segment"
]

extraMuonVertexCollections = [
  # invariant mass cut only:
  # # "MaskedDimuonVerex", 
  # Best Dimuon selection without isolation cut:
  "BestDimuonVertex", 
  # Best Dimuon selection with isolation cut:
  # "BestPFIsoDimuonVertex",
]

signal_legend = Legend(legend_max_x-legend_width, legend_max_y-5*legend_height, legend_max_x-2*legend_width, legend_max_y, "l")
sampletype = "sig"

if plot_background:
  signal_legend = Legend(legend_max_x-2.5*legend_width, legend_max_y-0.13-3*legend_height, legend_max_x-2*legend_width, legend_max_y-0.13, "l")
  sampletype = "bkg"

if plot_data:
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
  default_norm = NormalizationType.to_lumi
  y_scale = 0.1
if plot_data:
  # default_norm = NormalizationType.to_data
  default_norm = NormalizationType.to_lumi
  y_scale=0.00001

histograms = (
# #           name                                  title logx  logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel

  Histogram("Event_PV_npvs"                       , "", False, True  , default_norm              , 1  , 0     , 90   , 1e-2   , 1e8   , "# Primary vertices"                  , "# events (2018)"   ),
  Histogram("Event_PV_npvsGood"                   , "", False, True  , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "# Good primary vertices"             , "# events (2018)"   ),
  Histogram("Event_PV_x"                          , "", False, True  , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV x [cm]"                           , "# events (2018)"   ),
  Histogram("Event_PV_y"                          , "", False, True  , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV y [cm]"                           , "# events (2018)"   ),
  Histogram("Event_PV_z"                          , "", False, True  , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV z [cm]"                           , "# events (2018)"   ),
  
  Histogram("cutFlow"                               , "", False, True  , default_norm , 1  , 0     , 13     , 1e5   , 1e18   , "Selection"         , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex"        , "", False, True  , default_norm , 1  , 0     , 10     , 1e3   , 4e3    , "Selection"         , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex_Pat"    , "", False, True  , default_norm , 1  , 0     , 10     , 2e2   , 1e4    , "Selection"         , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex_PatDSA" , "", False, True  , default_norm , 1  , 0     , 10     , 1e1   , 1e4    , "Selection"         , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex_DSA"    , "", False, True  , default_norm , 1  , 0     , 10     , 1e-1  , 1e4    , "Selection"         , "Number of events"  ),
  Histogram("Event_normCheck"                       , "", False, True  , default_norm , 1  , 0     , 1      , 1e-1  , 1e20   , "norm check"        , "# events (2018)"   ),
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
    Histogram("Event_n"+muonCollectionName          , "", False, True  , default_norm        , 1  , 0     , 15    , 1e-1  , 1e8   , "Number of loose #mu"                            , "# events (2018)"   ),
    Histogram(muonCollectionName+"_pt"              , "", False, True  , default_norm        , 10 , 0     , 300   , 1e-1  , 1e5   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
    Histogram(muonCollectionName+"_eta"             , "", False, True  , default_norm        , 10 , -3    , 3     , 1e-1  , 1e7   , "loose #mu #eta"                                 , "# events (2018)"   ),
    Histogram(muonCollectionName+"_dxyPVTraj"       , "", False, True  , default_norm        , 100, -300  , 300   , 1e-3  , 1e6   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
    Histogram(muonCollectionName+"_dxyPVTrajErr"    , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu #sigma_{dxy} uncertainty [cm]"        , "# events (2018)"   ),
    Histogram(muonCollectionName+"_dxyPVTrajSig"    , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} / #sigma_{dxy}"                , "# events (2018)"   ),
    Histogram(muonCollectionName+"_ip3DPVSigned"    , "", False, True  , default_norm        , 250, -600  , 600   , 1e-3  , 1e6   , "loose #mu 3D IP [cm]"                           , "# events (2018)"   ),
    Histogram(muonCollectionName+"_ip3DPVSignedErr" , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu #sigma_{3DIP} [cm]"                   , "# events (2018)"   ),
    Histogram(muonCollectionName+"_ip3DPVSignedSig" , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu 3D IP / #sigma_{3DIP}"                , "# events (2018)"   ),
    Histogram(muonCollectionName+"_minDeltaR"       , "", False, True  , default_norm        , 5  , 0     , 3     , 1e-1  , 1e8   , "min #Delta R(loose #mu, loose #mu)"             , "# events (2018)"   ),
    Histogram(muonCollectionName+"_minOuterDeltaR"  , "", False, True  , default_norm        , 5  , 0     , 3     , 1e-1  , 1e8   , "min outer #Delta R(loose #mu, loose #mu)"       , "# events (2018)"   ),
    Histogram(muonCollectionName+"_minProxDeltaR"   , "", False, True  , default_norm        , 5  , 0     , 3     , 1e-1  , 1e8   , "min proximity #Delta R(loose #mu, loose #mu)"   , "# events (2018)"   ),
    Histogram(muonCollectionName+"_pfRelIso04all"   , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-2  , 1e8   , "loose #mu I_{PF}^{rel} ( #Delta R < 0.4 )"      , "# events (2018)"   ),
    Histogram(muonCollectionName+"_tkRelIso"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-2  , 1e8   , "loose #mu I_{tk}^{rel} ( #Delta R < 0.3 )"      , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_nSegments"       , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-2  , 1e8   , "# loose #mu segments"                           , "# events (2018)"   ),
  )

for muonVertexCollectionName in muonVertexCollectionNames:
  LLPnanoAOD_histograms += (
    Histogram(muonVertexCollectionName+"_invMass"              , "", False, False , default_norm        , 2  , 2.7     , 3.5     , 0  , 160   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
  )
  for category in muonVertexCategories:
    LLPnanoAOD_histograms += (
      Histogram("Event_n"+muonVertexCollectionName+category               , "", False, True  , default_norm        , 1  , 0     , 5     , 1e-3  , 1e8   , "Number of loose #mu vertices"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_vxy"                  , "", False, True  , default_norm        , 10  , 0     , 400   , 1e-5*y_scale  , 1e11*y_scale   , "#mu vertex L_{xy} [cm]"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_vxySigma"             , "", False, True  , default_norm        , 50 , 0     , 100   , 1e-3  , 1e6   , "#mu vertex #sigma_{Lxy} [cm]"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_vxySignificance"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"       , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_vxySignificanceV2"    , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"       , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dR"                   , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex #Delta R"                    , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_proxDR"               , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex proximity #Delta R"          , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_outerDR"              , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex outer #Delta R"              , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_normChi2"             , "", False, True  , default_norm        , 100, 0     , 5     , 1e-5  , 1e4   , "#mu vertex #chi^{2}/ndof"               , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_chargeProduct"        , "", False, True  , default_norm        , 1  , -1    , 2     , 1e-3  , 1e8   , "Dimuon charge"                          , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_maxHitsInFrontOfVert" , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-6  , 1e6   , "Max N(hits before vertex)"              , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dca"                  , "", False, True  , default_norm        , 20 , 0     , 15    , 1e-6  , 1e6   , "DCA [cm]"                               , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_absCollinearityAngle" , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-6  , 1e6   , "#mu vertex |#Delta #Phi|"               , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_absPtLxyDPhi1"        , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-4  , 1e5   , "#mu vertex |#Delta #phi_{#mu1}|"        , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_absPtLxyDPhi2"        , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-4  , 1e5   , "#mu vertex |#Delta #phi_{#mu2}|"        , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nTrackerLayers1"      , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-3  , 1e10  , "#mu_{1} N(tracker layers)"              , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nTrackerLayers2"      , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-3  , 1e6   , "#mu_{2} N(tracker layers)"              , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nSegments1"           , "", False, True  , NormalizationType.to_one        , 1  , 0     , 10    , 1e-6  , 1e4  , "#mu_{1} N(muon segments)"               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nSegments2"           , "", False, True  , NormalizationType.to_one        , 1  , 0     , 10    , 1e-6  , 1e4  , "#mu_{2} N(muon segments)"               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nSegmentsSum"         , "", False, True  , default_norm        , 1  , 0     , 20    , 1e-3  , 1e10  , "#mu_{1} + #mu_{2} N(muon segments)"     , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_invMass"              , "", False, False , default_norm        , 2  , 2.7     , 3.5     , 0  , 10   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_pt"                   , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex p_{T} [GeV]"                 , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_leadingPt"            , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex leading p_{T} [GeV]"         , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dxyPVTraj1"           , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} [cm]"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dxyPVTraj2"           , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} [cm]"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_minDxyPVTraj"         , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex min d_{xy} [cm]"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_maxDxyPVTraj"         , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex max d_{xy} [cm]"             , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig1"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} / #sigma_{dxy}^{1}"  , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig2"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} / #sigma_{dxy}^{2}"  , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_minDxyPVTrajSig"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex min d_{xy} / #sigma_{dxy}"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_maxDxyPVTrajSig"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex max d_{xy} / #sigma_{dxy}"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Dimuon1"      , "", False, True  , default_norm        , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Dimuon1"      , "", False, True  , default_norm        , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Dimuon2"      , "", False, True  , default_norm        , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Dimuon2"      , "", False, True  , default_norm        , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Muon1"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Muon1"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Muon2"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Muon2"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_pfRelIso04all1"                  , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_pfRelIso04all2"                  , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_tkRelIsoMuon1"                   , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{1} I_{tk}^{rel} ( #Delta R < 0.3 )"    , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_tkRelIsoMuon2"                   , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{2} I_{tk}^{rel} ( #Delta R < 0.3 )"    , "# events (2018)"   ),
    )

histograms2D_LLPnanoAOD = ()


if plots_from_LLPNanoAOD:
  histograms += LLPnanoAOD_histograms

histograms2D = ()

if plots_from_LLPNanoAOD:
  histograms2D = histograms2D + histograms2D_LLPnanoAOD


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
    file_path=f"{base_path}/collision_data2018/SingleMuon_{skim}_{hist_path}.root",
    type=SampleType.data,
    cross_sections=cross_sections,
    line_alpha=1,
    fill_alpha=0,
    marker_size=0.7,
    marker_style=20,
    marker_color=ROOT.kBlack,
    legend_description="SingleMuon2018",
  ),
  # Sample(
  #   name="SingleMuon",
  #   file_path=f"{base_path}/collision_data2018/SingleMuon2018_{skim}_{hist_path}_C.root",
  #   type=SampleType.data,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   fill_alpha=0,
  #   marker_size=0.7,
  #   marker_style=20,
  #   marker_color=ROOT.kBlack,
  #   legend_description="SingleMuon2018",
  # ),
  # Sample(
  #  name="SingleMuon",
  #  file_path=f"{base_path}/collision_data2018/SingleMuon2018_{skim}_{hist_path}_B.root",
  #  type=SampleType.data,
  #  cross_sections=cross_sections,
  #  line_alpha=1,
  #  fill_alpha=0,
  #  marker_size=0.7,
  #  marker_style=20,
  #  marker_color=ROOT.kBlack,
  #  legend_description="SingleMuon2018",
  #),
  # Sample(
  #   name="SingleMuon",
  #   file_path=f"{base_path}/collision_data2018/SingleMuon2018_{skim}_{hist_path}_A.root",
  #   type=SampleType.data,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   fill_alpha=0,
  #   marker_size=0.7,
  #   marker_style=20,
  #   marker_color=ROOT.kBlack,
  #   legend_description="SingleMuon2018",
  # ),
)

signal_samples = (
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
    line_color=ROOT.kCyan,
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
  Sample(
    name="tta_mAlp-1GeV_ctau-1e3mm",
    file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e3mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kGreen+1,
    legend_description="m_{a} = 1 GeV, c#tau_{a} = 1 m",
  ),
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
  
  Backgrounds
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
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f")
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
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-5*legend_height, legend_max_x-legend_width, legend_max_y-4*legend_height, "f")
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
    fill_color=ROOT.kViolet+1,
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
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-1*legend_height, legend_max_x-legend_width, legend_max_y-0*legend_height, "f")
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
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-2*legend_height, legend_max_x-legend_width, legend_max_y-1*legend_height, "f")

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
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-3*legend_height, legend_max_x-legend_width, legend_max_y-2*legend_height, "f")
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
  # Sample(
  #   name="QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-30To50/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.background,
  #   cross_sections=cross_sections,
  #   line_alpha=0,
  #   # fill_color=color_palette_wong[0],
  #   fill_color=TColor.GetColor(color_palette_petroff_8[5]),
  #   fill_alpha=1.0,
  #   marker_size=0,
  #   legend_description=" ",
  #   custom_legend=Legend(0, 0, 0, 0, "")
  # ),
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
  # Sample(
  #   name="QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-80To120/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.background,
  #   cross_sections=cross_sections,
  #   line_alpha=0,
  # #   fill_color=color_palette_wong[0],
  #   fill_color=TColor.GetColor(color_palette_petroff_8[5]),
  #   fill_alpha=1.0,
  #   marker_size=0,
  #   legend_description=" ",
  #   custom_legend=Legend(0, 0, 0, 0, "")
  # ),
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
    # legend_description="QCD (#mu enriched)",
    # custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, ""),
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
    # legend_description=" ",
    # custom_legend=Legend(0, 0, 0, 0, "")
    legend_description="QCD (#mu enriched)",
    custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-6*legend_height, legend_max_x-legend_width, legend_max_y-5*legend_height, "f")
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
    # legend_description="QCD (#mu enriched)",
    # custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
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
