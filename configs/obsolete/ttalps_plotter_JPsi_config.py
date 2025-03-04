import ROOT
import os

from Sample import SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from TTAlpsPlotterConfigHelper import TTAlpsPlotterConfigHelper
from ttalps_cross_sections import *

year = "2018"
cross_sections = get_cross_sections(year)

base_path = f"/data/dust/user/{os.environ["USER"]}/ttalps_cms/"

# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_JPsiDimuons"
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_ZDimuons"

skim = "skimmed_looseSemimuonic_v2_SR"

output_formats = ["pdf"]

luminosity = 59820. # 2018 eras A+B+C+D (A+B+C) was 27972.887358 before)
# luminosity = 59830. # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2
lumi_label_offset = 0.02
lumi_label_value = luminosity

canvas_size = (800, 600)
canvas_size_2Dhists = (800, 800)
show_ratio_plots = True
ratio_limits = (0.5, 1.5)

legend_max_x = 0.82
legend_max_y = 0.89
legend_width = 0.17 if show_ratio_plots else 0.23
legend_height = 0.045 if show_ratio_plots else 0.03


# only plot backgrounds with N_events > bkgRawEventsThreshold
bkgRawEventsThreshold = 10

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
  "BestPFIsoDimuonVertex",
]

sampletype = "sig"
if plot_background:
  sampletype = "bkg"
if plot_data:
  sampletype = "data"

output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{sampletype}/"

background_uncertainty_style = 3244 # available styles: https://root.cern.ch/doc/master/classTAttFill.html
background_uncertainty_color = ROOT.kBlack
background_uncertainty_alpha = 0.3

plotting_options = {
  SampleType.background: "hist",
  SampleType.signal: "nostack hist",
  SampleType.data: "nostack e",
}

data_to_include = [
  "SingleMuon2018",
]

backgrounds_to_exclude = [
  "QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  "QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
]

signals_to_include = [
  "tta_mAlp-0p35GeV_ctau-1e2mm", 
  "tta_mAlp-0p35GeV_ctau-1e3mm", 
  "tta_mAlp-0p35GeV_ctau-1e5mm"
]

configHelper = TTAlpsPlotterConfigHelper(
  year,
  base_path,
  skim,
  hist_path,
  data_to_include,
  backgrounds_to_exclude,
  signals_to_include,
  (legend_max_x, legend_max_y, legend_width, legend_height)
)

samples = []
configHelper.add_samples(SampleType.data, samples)
configHelper.add_samples(SampleType.background, samples)
configHelper.add_samples(SampleType.signal, samples)
custom_stacks_order = configHelper.get_custom_stacks_order(samples)

weightsBranchName = "genWeight"

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
  Histogram("Event_MET_pt"                        , "", False,  True  , default_norm             , 10 , 0     , 800   , 1e-8  , 1e9   , "MET p_{T} [GeV]"                     , "# events (2018)"   ),
  
  Histogram("cutFlow"                             , "", False, True  , default_norm , 1  , 0     , 13     , 1e-3*y_scale   , 1e23*y_scale  , "Selection"                      , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex"      , "", False, True  , default_norm , 1  , 0     , 8      , 1e4*y_scale   , 1e7*y_scale  , "Selection"                      , "Number of events"  ),
  Histogram("Event_normCheck"                     , "", False, True  , default_norm , 1  , 0     , 1      , 1e-1*y_scale  , 1e20*y_scale   , "norm check"                     , "# events (2018)"   ),
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
    # Histogram(muonCollectionName+"_dxyPVTraj"       , "", False, True  , default_norm        , 100, -300  , 300   , 1e-3  , 1e6   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_dxyPVTrajErr"    , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu #sigma_{dxy} uncertainty [cm]"        , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_dxyPVTrajSig"    , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} / #sigma_{dxy}"                , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_ip3DPVSigned"    , "", False, True  , default_norm        , 250, -600  , 600   , 1e-3  , 1e6   , "loose #mu 3D IP [cm]"                           , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_ip3DPVSignedErr" , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu #sigma_{3DIP} [cm]"                   , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_ip3DPVSignedSig" , "", False, True  , default_norm        , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu 3D IP / #sigma_{3DIP}"                , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_minDeltaR"       , "", False, True  , default_norm        , 5  , 0     , 3     , 1e-1  , 1e8   , "min #Delta R(loose #mu, loose #mu)"             , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_minOuterDeltaR"  , "", False, True  , default_norm        , 5  , 0     , 3     , 1e-1  , 1e8   , "min outer #Delta R(loose #mu, loose #mu)"       , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_minProxDeltaR"   , "", False, True  , default_norm        , 5  , 0     , 3     , 1e-1  , 1e8   , "min proximity #Delta R(loose #mu, loose #mu)"   , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_pfRelIso04all"   , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-2  , 1e8   , "loose #mu I_{PF}^{rel} ( #Delta R < 0.4 )"      , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_tkRelIso"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-2  , 1e8   , "loose #mu I_{tk}^{rel} ( #Delta R < 0.3 )"      , "# events (2018)"   ),
    # Histogram(muonCollectionName+"_nSegments"       , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-2  , 1e8   , "# loose #mu segments"                           , "# events (2018)"   ),
  )

for muonVertexCollectionName in muonVertexCollectionNames:
  for category in muonVertexCategories:
    LLPnanoAOD_histograms += (
      Histogram("Event_n"+muonVertexCollectionName+category               , "", False, True  , default_norm        , 1  , 0     , 5     , 1e-3  , 1e8   , "Number of loose #mu vertices"           , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_vxy"                  , "", False, True  , default_norm        , 10  , 0     , 400   , 1e-5*y_scale  , 1e11*y_scale   , "#mu vertex L_{xy} [cm]"                 , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_vxySigma"             , "", False, True  , default_norm        , 50 , 0     , 100   , 1e-3  , 1e6   , "#mu vertex #sigma_{Lxy} [cm]"           , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_vxySignificance"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"       , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_vxySignificanceV2"    , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"       , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dR"                   , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex #Delta R"                    , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_proxDR"               , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex proximity #Delta R"          , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_outerDR"              , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex outer #Delta R"              , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_normChi2"             , "", False, True  , default_norm        , 100, 0     , 5     , 1e-5  , 1e4   , "#mu vertex #chi^{2}/ndof"               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_chargeProduct"        , "", False, True  , default_norm        , 1  , -1    , 2     , 1e-3  , 1e8   , "Dimuon charge"                          , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_maxHitsInFrontOfVert" , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-6  , 1e6   , "Max N(hits before vertex)"              , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dca"                  , "", False, True  , default_norm        , 20 , 0     , 15    , 1e-6  , 1e6   , "DCA [cm]"                               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_absCollinearityAngle" , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-6  , 1e6   , "#mu vertex |#Delta #Phi|"               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_absPtLxyDPhi1"        , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-4  , 1e5   , "#mu vertex |#Delta #phi_{#mu1}|"        , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_absPtLxyDPhi2"        , "", False, True  , default_norm        , 10 , 0     , 3.15  , 1e-4  , 1e5   , "#mu vertex |#Delta #phi_{#mu2}|"        , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nTrackerLayers1"      , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-3  , 1e10  , "#mu_{1} N(tracker layers)"              , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nTrackerLayers2"      , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-3  , 1e6   , "#mu_{2} N(tracker layers)"              , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nSegments1"           , "", False, True  , NormalizationType.to_one        , 1  , 0     , 10    , 1e-6  , 1e4  , "#mu_{1} N(muon segments)"               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nSegments2"           , "", False, True  , NormalizationType.to_one        , 1  , 0     , 10    , 1e-6  , 1e4  , "#mu_{2} N(muon segments)"               , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_nSegmentsSum"         , "", False, True  , default_norm        , 1  , 0     , 20    , 1e-3  , 1e10  , "#mu_{1} + #mu_{2} N(muon segments)"     , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_invMass"              , "", False, False , default_norm        , 1  , 2.7   , 3.5     , 0  , 1500   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
      Histogram(muonVertexCollectionName+category+"_invMass"              , "", False, False , default_norm        , 20  , 70   , 110     , 0  , 30   , "#mu vertex M_{#mu #mu} [GeV]"           , "# events (2018)"   ),
      
      
      Histogram(muonVertexCollectionName+category+"_pt"                   , "", False, True  , default_norm        , 10  , 0     , 200     , 1e-3  , 1e6   , "#mu vertex p_{T} [GeV]"                 , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_leadingPt"            , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex leading p_{T} [GeV]"         , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dxyPVTraj1"           , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} [cm]"             , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dxyPVTraj2"           , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} [cm]"             , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_minDxyPVTraj"         , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex min d_{xy} [cm]"             , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_maxDxyPVTraj"         , "", False, True  , default_norm        , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex max d_{xy} [cm]"             , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig1"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} / #sigma_{dxy}^{1}"  , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_dxyPVTrajSig2"        , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} / #sigma_{dxy}^{2}"  , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_minDxyPVTrajSig"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex min d_{xy} / #sigma_{dxy}"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_maxDxyPVTrajSig"      , "", False, True  , default_norm        , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex max d_{xy} / #sigma_{dxy}"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Dimuon1"      , "", False, True  , default_norm        , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Dimuon1"      , "", False, True  , default_norm        , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Dimuon2"      , "", False, True  , default_norm        , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Dimuon2"      , "", False, True  , default_norm        , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Muon1"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Muon1"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_displacedTrackIso03Muon2"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_displacedTrackIso04Muon2"        , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )"   , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_pfRelIso04all1"                  , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_pfRelIso04all2"                  , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )"    , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_tkRelIsoMuon1"                   , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{1} I_{tk}^{rel} ( #Delta R < 0.3 )"    , "# events (2018)"   ),
      # Histogram(muonVertexCollectionName+category+"_tkRelIsoMuon2"                   , "", False, True  , default_norm        , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{2} I_{tk}^{rel} ( #Delta R < 0.3 )"    , "# events (2018)"   ),
    )

histograms2D_LLPnanoAOD = ()

if plots_from_LLPNanoAOD:
  histograms += LLPnanoAOD_histograms

histograms2D = ()

if plots_from_LLPNanoAOD:
  histograms2D = histograms2D + histograms2D_LLPnanoAOD
