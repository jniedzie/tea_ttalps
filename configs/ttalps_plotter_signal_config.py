import ROOT
from ROOT import TColor
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from ttalps_cross_sections import *

base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms/"

hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"

# skim = "skimmed_looseSemimuonic"
skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1"

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

n_default_backgrounds = 10

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Private Work"

## SETTINGS ##
plots_from_LLPNanoAOD = True
plot_genALP_info = True
plot_muonMatching_info = False
plot_background = True
plot_ratio_hists = False

muonMatchingMethods = [
  # "DR", 
  # "OuterDR", 
  # "ProxDR", 
  "Segment"
]

signal_legend = Legend(legend_max_x-legend_width, legend_max_y-5*legend_height, legend_max_x-2*legend_width, legend_max_y, "l")
sampletype = "sig"

if plot_background:
  plot_genALP_info = False
  plot_ratio_hists = False
  signal_legend = Legend(legend_max_x-2.5*legend_width, legend_max_y-0.13-3*legend_height, legend_max_x-2*legend_width, legend_max_y-0.13, "l")
  sampletype = "bkg"

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
# default_norm = NormalizationType.to_background
# default_norm = NormalizationType.to_data

y_scale = 1

if plot_background:
  default_norm = NormalizationType.to_background
else:
  # default_norm = NormalizationType.to_one
  default_norm = NormalizationType.to_lumi
  y_scale = 0.1

histograms = (
# #           name                                  title logx  logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
  # Histogram("Event_nTightMuons"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of tight #mu"                            , "# events (2018)"   ),
  # Histogram("TightMuons_pt"                       , "", False, True  , default_norm              , 50 , 0     , 1000  , 1e-6  , 1e8   , "tight #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # # Histogram("TightMuons_leadingPt"                , "", False, True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e5   , "leading tight #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  # # # Histogram("TightMuons_subleadingPt"             , "", False, True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e4   , "all subleading tight #mu p_{T} [GeV]"           , "# events (2018)"   ),
  # Histogram("TightMuons_eta"                      , "", False, True  , default_norm              , 10 , -3.0  , 5.0   , 1e0   , 1e5   , "tight #mu #eta"                                 , "# events (2018)"   ),
  # Histogram("TightMuons_dxy"                      , "", False, True  , default_norm              , 2  , -0.5  , 0.5   , 1e-2  , 1e10   , "tight #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  # Histogram("TightMuons_dz"                       , "", False, True  , default_norm              , 2  , -1    , 1     , 1e-2  , 1e8   , "tight #mu d_{z} [cm]"                           , "# events (2018)"   ),
  
  # Histogram("TightMuons_pfRelIso04_all"           , "", False, True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_pfRelIso03_chg"           , "", False, True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_pfRelIso03_all"           , "", False, True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_miniPFRelIso_chg"         , "", False, True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  # Histogram("TightMuons_miniPFRelIso_all"         , "", False, True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  # Histogram("TightMuons_jetRelIso"                , "", False, True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "tight #mu jet Rel Iso"                          , "# events (2018)"   ),
  # Histogram("TightMuons_tkRelIso"                 , "", False, True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "tight #mu track Rel Iso"                       , "# events (2018)"   ),
  
  # Histogram("Event_nLooseMuons"                   , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2   , 1e7   , "Number of loose #mu"                            , "# events (2018)"   ),
  # Histogram("LooseMuons_pt"                       , "", False, True  , default_norm              , 1  , 0     , 50    , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # Histogram("LooseMuons_leadingPt"                , "", False, True  , default_norm              , 1  , 0     , 50    , 1e-1  , 1e8   , "leading loose #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  # # Histogram("LooseMuons_subleadingPt"             , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "all subleading loose #mu p_{T} [GeV]"           , "# events (2018)"   ),
  # Histogram("LooseMuons_eta"                      , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  # Histogram("LooseMuons_dxy"                      , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  # Histogram("LooseMuons_dz"                       , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  
  # Histogram("LooseMuons_pfRelIso04_all"           , "", False, True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  # Histogram("LooseMuons_pfRelIso03_chg"           , "", False, True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  # Histogram("LooseMuons_pfRelIso03_all"           , "", False, True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  # Histogram("LooseMuons_miniPFRelIso_chg"         , "", False, True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  # Histogram("LooseMuons_miniPFRelIso_all"         , "", False, True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  # Histogram("LooseMuons_jetRelIso"                , "", False, True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "Loose #mu jet Rel Iso"                          , "# events (2018)"   ),
  # Histogram("LooseMuons_tkRelIso"                 , "", False, True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "Loose #mu track Rel Iso"                       , "# events (2018)"   ),
  
  # # # Histogram("Event_nLooseElectrons"               , "", False, True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose electrons"                      , "# events (2018)"   ),
  # # # Histogram("LooseElectrons_pt"                   , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "loose electron p_{T} [GeV]"                     , "# events (2018)"   ),
  # # # Histogram("LooseElectrons_leadingPt"            , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "leading loose electron p_{T} [GeV]"             , "# events (2018)"   ),
  # # # Histogram("LooseElectrons_subleadingPt"         , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "all subleading loose electron p_{T} [GeV]"      , "# events (2018)"   ),
  # # # Histogram("LooseElectrons_eta"                  , "", False, True  , default_norm              , 5  , -3.5  , 3.5   , 1e-2  , 1e6   , "loose electron #eta"                            , "# events (2018)"   ),
  # # # Histogram("LooseElectrons_dxy"                  , "", False, True  , default_norm              , 10 , -10   , 10    , 1e-2  , 1e6   , "loose electron d_{xy}"                          , "# events (2018)"   ),
  # # # Histogram("LooseElectrons_dz"                   , "", False, True  , default_norm              , 10 , -10   , 10    , 1e-2  , 1e6   , "loose electron d_{z}"                           , "# events (2018)"   ),
  
  # Histogram("Event_nGoodJets"                     , "", False, True  , default_norm              , 1  , 2     , 16    , 1e-2  , 1e10   , "Number of good jets"                            , "# events (2018)"   ),
  # # Histogram("GoodJets_pt"                         , "", False, True  , default_norm              , 25 , 0     , 1300  , 1e-3  , 1e6   , "good jet p_{T} [GeV]"                           , "# events (2018)"   ),
  # # Histogram("GoodJets_eta"                        , "", False, True  , default_norm              , 10 , -3    , 5.0   , 1e1   , 1e6   , "good jet #eta"                                  , "# events (2018)"   ),
  # # Histogram("GoodJets_btagDeepB"                  , "", False, True  , default_norm              , 10 , 0     , 1.5   , 2e0   , 1e6   , "good jet deepCSV score"                         , "# events (2018)"   ),
  # Histogram("GoodJets_btagDeepFlavB"              , "", False, True  , default_norm              , 10 , 0     , 1.8   , 1e-1   , 1e8   , "good jet deepJet score"                         , "# events (2018)"   ),
  
  # Histogram("Event_nGoodMediumBtaggedJets"              , "", False, True  , default_norm              , 1  , 0     , 20    , 1e0   , 1e9   , "Number of good b-jets"                          , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_pt"                  , "", False, True  , default_norm              , 50 , 0     , 2000  , 1e-5  , 1e4   , "good b-jet p_{T} [GeV]"                         , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_eta"                 , "", False, True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e10  , "good b-jet #eta"                                , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_btagDeepB"           , "", False, True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good b-jet btagDeepB"                           , "# events (2018)"   ),
  
  # Histogram("Event_nGoodNonTightBtaggedJets"           , "", False, True  , default_norm              , 1  , 0     , 20    , 1e0   , 1e9   , "Number of good non-b jets"                      , "# events (2018)"   ),
  # Histogram("GoodNonTightBtaggedJets_pt"               , "", False, True  , default_norm              , 50 , 0     , 2000  , 1e-5  , 1e4   , "good non-b jet p_{T} [GeV]"                     , "# events (2018)"   ),
  # Histogram("GoodNonTightBtaggedJets_eta"              , "", False, True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e10  , "good non-b jet #eta"                            , "# events (2018)"   ),
  # Histogram("GoodNonTightBtaggedJets_btagDeepB"        , "", False, True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good non-b jet btagDeepB"                       , "# events (2018)"   ),
  
  # Histogram("Event_METpt"                         , "", False, True  , default_norm              , 10 , 0     , 800   , 1e-5  , 1e9   , "MET p_{T} [GeV]"                                , "# events (2018)"   ),
  Histogram("Event_PV_npvs"                       , "", False, True  , default_norm              , 1  , 0     , 90   , 1e-2  , 1e8   , "# Primary vertices"                             , "# events (2018)"   ),
  Histogram("Event_PV_npvsGood"                   , "", False, True  , default_norm              , 1  , 0     , 20   , 1e-10  , 1e8   , "# Good primary vertices"                        , "# events (2018)"   ),
  
  # Histogram("LooseMuons_dimuonMinv"               , "", False, True  , default_norm              , 1  , 70    , 110   , 1e0   , 1e4   , "loose muons m_{#mu#mu} [GeV]"                   , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonMinvClosestToZ"     , "", False, True  , default_norm              , 1  , 70    , 110   , 1e0   , 1e4   , "loose muons closest to Z m_{#mu#mu} [GeV]"      , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaRclosestToZ"   , "", False, True  , default_norm              , 1  , -1    , 6     , 1e0   , 1e3   , "loose muons closest to Z #Delta R_{#mu#mu}"     , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaEtaclosestToZ" , "", False, True  , default_norm              , 1  , -1    , 6     , 1e-1  , 1e3   , "loose muons closest to Z #Delta #eta_{#mu#mu}"  , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaPhiclosestToZ" , "", False, True  , default_norm              , 1  , -3.5  , 6     , 1e-1  , 1e3   , "loose muons closest to Z #Delta #phi_{#mu#mu}"  , "# events (2018)"   ),
  
  # Histogram("TightMuons_deltaPhiMuonMET"          , "", False, True  , default_norm              , 20 , -4    , 4     , 1e0   , 1e7   , "tight muon #Delta #phi(MET, #mu)"               , "# events (2018)"   ),
  # Histogram("TightMuons_minvMuonMET"              , "", False, True  , default_norm              , 40 , 0     , 1000  , 1e-4  , 1e5   , "tight muon m_{MET, l} [GeV]"                    , "# events (2018)"   ),
  # Histogram("GoodJets_minvBjet2jets"              , "", False, True  , default_norm              , 25 , 0     , 1500  , 1e-1  , 1e5   , "good jets m_{bjj} [GeV]"                        , "# events (2018)"   ),

  # Histogram("Event_nMuon"                         , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of #mu"                            , "# events (2018)"   ),
  # Histogram("Muon_pt"                             , "", False, True  , default_norm              , 50 , 0     , 1000  , 1e-6  , 1e10   , "#mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # Histogram("Muon_eta"                            , "", False, True  , default_norm              , 10 , -3.0  , 5.0   , 1e0   , 1e8   , "#mu #eta"                                 , "# events (2018)"   ),
  # Histogram("Muon_dxy"                            , "", False, True  , default_norm              , 2  , -0.5  , 0.5   , 1e-1  , 1e10   , "#mu d_{xy} [cm]"                          , "# events (2018)"   ),
  # Histogram("Muon_dz"                             , "", False, True  , default_norm              , 2  , -1    , 1     , 1e-1  , 1e10   , "#mu d_{z} [cm]"                           , "# events (2018)"   ),

  Histogram("cutFlow"                             , "", False, True  , default_norm , 1  , 0     , 13     , 1e-1*y_scale   , 1e23*y_scale  , "Selection"                                      , "Number of events"  ),
  Histogram("Event_normCheck"                     , "", False, True  , default_norm , 1  , 0     , 1      , 1e-1*y_scale  , 1e20*y_scale   , "norm check"                                     , "# events (2018)"   ),
)

LLPnanoAOD_histograms = (
#           name                                  title logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
  # Histogram("Muon_idx"                            , "", False, True  , default_norm              , 1 , 0     , 15  , 1e-6  , 1e10   , "#mu index"                                , "# events (2018)"   ),
  # Histogram("Muon_outerEta"                       , "", False, True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "#mu outer #eta"                           , "# events (2018)"   ),
  # Histogram("Muon_outerPhi"                       , "", False, True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "#mu #phi"                                 , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch1"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 1"           , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch2"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 2"           , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch3"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 3"           , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch4"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 4"           , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch5"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 5"           , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch1idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 1"                       , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch2idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 2"                       , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch3idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 3"                       , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch4idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 4"                       , "# events (2018)"   ),
  # Histogram("Muon_dsaMatch5idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 5"                       , "# events (2018)"   ),

  # Histogram("Event_nDSAMuon"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e9*y_scale   , "Number of dSA #mu"        , "# events (2018)"   ),
  # Histogram("DSAMuon_idx"                         , "", False, True  , default_norm              , 1 , 0     , 15  , 1e-6  , 1e10   , "dSa #mu index"                                , "# events (2018)"   ),
  # Histogram("DSAMuon_pt"                          , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "dSA #mu p_{T} [GeV]"                      , "# events (2018)"   ),
  # Histogram("DSAMuon_eta"                         , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "dSA #mu #eta"                             , "# events (2018)"   ),
  # Histogram("DSAMuon_dxy"                         , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("DSAMuon_dz"                          , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_dzPV"                        , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_dxyPVTraj"                   , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("DSAMuon_dxyPVSigned"                 , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("DSAMuon_dzBS"                        , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_dxyBS"                       , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("DSAMuon_dxyBSTraj"                   , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("DSAMuon_dxyBSSigned"                 , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch1"                  , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 1"           , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch2"                  , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 2"           , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch3"                  , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 3"           , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch4"                  , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 4"           , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch5"                  , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 5"           , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch1idx"               , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 1"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch2idx"               , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 2"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch3idx"               , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 3"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch4idx"               , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 4"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_muonMatch5idx"               , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 5"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_outerEta"                    , "", False, True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "DSA #mu outer #eta"                           , "# events (2018)"   ),
  # Histogram("DSAMuon_outerPhi"                    , "", False, True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "DSA #mu #phi"                                 , "# events (2018)"   ),

  # Histogram("Event_nLooseDSAMuons"                , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose dSA #mu"                        , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_pt"                    , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose dSA #mu p_{T} [GeV]"                      , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_eta"                   , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose dSA #mu #eta"                             , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_dxy"                   , "", False, True  , default_norm              , 40  , -600  , 600   , 1e-1  , 1e8   , "loose dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_dz"                    , "", False, True  , default_norm              , 40  , -600  , 600   , 1e-1  , 1e8   , "loose dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  
  # Histogram("LooseDSAMuons_nSegments"            , "", False, True  , default_norm   , 1  , 0     , 10    , 1e-1    , 1e7 , "Number of DSA segments"          , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_nDTHits"              , "", False, True  , default_norm   , 1  , 0     , 50    , 1e-1    , 1e7 , "number of DT hits"               , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_nCSCHits"             , "", False, True  , default_norm   , 1  , 0     , 50    , 1e-1    , 1e7 , "number of CSC hits"              , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_nDTplusCSCHits"       , "", False, True  , default_norm   , 1  , 0     , 50    , 1e-1    , 1e7 , "number of DT+CSC hits"           , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_muonMatch1"           , "", False, True  , default_norm   , 1  , 0     , 10    , 1e-1    , 1e7 , "Most muon segment matches"       , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_muonMatch2"           , "", False, True  , default_norm   , 1  , 0     , 10    , 1e-1    , 1e7 , "2nd most muon segment matches"   , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_muonMatch3"           , "", False, True  , default_norm   , 1  , 0     , 10    , 1e-1    , 1e7 , "3rd most muon segment matches"   , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_matchRatio1"          , "", False, True  , default_norm   , 10  , 0     , 1.033    , 1e-3    , 1e5 , "Most muon segment matches / number of DSA segments"   , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_matchRatio2"          , "", False, True  , default_norm   , 10  , 0     , 1.033    , 1e-3    , 1e5 , "2nd most muon segment matches / number of DSA segments"   , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_matchRatio3"          , "", False, True  , default_norm   , 10  , 0     , 1.033    , 1e-3    , 1e5 , "3rd most muon segment matches / number of DSA segments"   , "# events (2018)"   ),

  # Histogram("LooseDSAMuons_PATOuterDR"           , "", False, True  , default_norm   , 10   , 0     , 6  , 1e-1    , 1e6 , "Outer #Delta R(loose DSA #mu, loose PAT #mu)"   , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_PATProxDR"            , "", False, True  , default_norm   , 10  , 0     , 6  , 1e-1    , 1e6 , "Proximity #Delta R(loose DSA #mu, loose PAT #mu)"   , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_PATDR"                , "", False, True  , default_norm   , 10  , 0     , 6  , 1e-1    , 1e6 , "#Delta R(loose DSA #mu, loose PAT #mu)"         , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_PATDEta"              , "", False, True  , default_norm   , 10  , 0     , 6  , 1e-1    , 1e6 , "#Delta #eta(loose DSA #mu, loose PAT #mu)"      , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_PATDPhi"              , "", False, True  , default_norm   , 10  , 0     , 6  , 1e-1    , 1e6 , "#Delta #phi(loose DSA #mu, loose PAT #mu)"      , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_PATDOuterEta"         , "", False, True  , default_norm   , 10  , 0     , 6  , 1e-1    , 1e6 , "Outer #Delta #eta(loose DSA #mu, loose PAT #mu)"    , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_PATDOuterPhi"         , "", False, True  , default_norm   , 10  , 0     , 6  , 1e-1    , 1e6 , "Outer #Delta #phi(loose DSA #mu, loose PAT #mu)"    , "# events (2018)"   ),

)

# muonCategories = ["", "DSA", "PAT"]
muonCategories = [""]
muonVertexCategories = ["", "_PatDSA", "_DSA", "_Pat"]
for method in muonMatchingMethods:
  for category in muonCategories:
    collectionName = "Loose"+category+"Muons"+method+"Match"
    LLPnanoAOD_histograms += (
      Histogram("Event_n"+collectionName          , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "Number of loose #mu"           , "# events (2018)"   ),
      Histogram(collectionName+"_pt"              , "", False, True  , default_norm              , 10 , 0     , 300   , 1e-1  , 1e5   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
      Histogram(collectionName+"_eta"             , "", False, True  , default_norm              , 10 , -3    , 3     , 1e-1   , 1e7   , "loose #mu #eta"                                 , "# events (2018)"   ),
      Histogram(collectionName+"_dxy"             , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
      Histogram(collectionName+"_dxyPVTraj"       , "", False, True  , default_norm              , 100 , -300  , 300   , 1e-3  , 1e6   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
      Histogram(collectionName+"_dxyPVTrajErr"    , "", False, True  , default_norm              , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} uncertainty [cm]"              , "# events (2018)"   ),
      Histogram(collectionName+"_dxyPVTrajSig"    , "", False, True  , default_norm              , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} significance"                  , "# events (2018)"   ),
      Histogram(collectionName+"_dz"              , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
      Histogram(collectionName+"_dzPV"            , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
      Histogram(collectionName+"_dzPVErr"         , "", False, True  , default_norm              , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu d_{z} uncertainty [cm]"               , "# events (2018)"   ),
      Histogram(collectionName+"_dzPVSig"         , "", False, True  , default_norm              , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu d_{z} significance"                   , "# events (2018)"   ),
      Histogram(collectionName+"_ip3DPVSigned"    , "", False, True  , default_norm              , 250, -600  , 600   , 1e-3  , 1e6   , "loose #mu 3D IP [cm]"                           , "# events (2018)"   ),
      Histogram(collectionName+"_ip3DPVSignedErr" , "", False, True  , default_norm              , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu 3D IP uncertainty [cm]"               , "# events (2018)"   ),
      Histogram(collectionName+"_ip3DPVSignedSig" , "", False, True  , default_norm              , 20 , 0     , 200   , 1e-1  , 1e8   , "loose #mu 3D IP significance"                   , "# events (2018)"   ),
      Histogram(collectionName+"_minDeltaR"       , "", False, True  , default_norm              , 5  , 0     , 3     , 1e-1  , 1e8   , "min #Delta R(loose #mu, loose #mu)"              , "# events (2018)"   ),
      Histogram(collectionName+"_minOuterDeltaR"  , "", False, True  , default_norm              , 5  , 0     , 3     , 1e-1  , 1e8   , "min outer #Delta R(loose #mu, loose #mu)"        , "# events (2018)"   ),
      Histogram(collectionName+"_minProxDeltaR"   , "", False, True  , default_norm              , 5  , 0     , 3     , 1e-1  , 1e8   , "min proximity #Delta R(loose #mu, loose #mu)"    , "# events (2018)"   ),
    )
  vertexCollectionName = "LooseMuonsVertex"+method+"Match"
  LLPnanoAOD_histograms += (
    # Histogram(vertexCollectionName+"_vxErr"     , "", False, True  , default_norm              , 1  , 0     , 10    , 1e0   , 1e8   , "#mu vertex #sigma_{v_{x}} [cm]"                      , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vxSignificance" , "", False, True  , default_norm         , 10 , 0     , 100   , 1e0   , 1e8   , "#mu vertex v_{x}/#sigma_{v_{x}} [cm]"                , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vyErr"     , "", False, True  , default_norm              , 1  , 0     , 10    , 1e0   , 1e8   , "#mu vertex #sigma_{v_{y}} [cm]"                      , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vySignificance" , "", False, True  , default_norm         , 10 , 0     , 100   , 1e0   , 1e8   , "#mu vertex v_{y}/#sigma_{v_{y}} [cm]"                , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vzErr"     , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "#mu vertex #sigma_{v_{z}} [cm]"                      , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vzSignificance" , "", False, True  , default_norm         , 10 , 0     , 100   , 1e-1  , 1e8   , "#mu vertex v_{z}/#sigma_{v_{z}} [cm]"                , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_originalMuonIdx1"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_originalMuonIdx2"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_isDSAMuon1", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_isDSAMuon2", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "dimuon #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso04Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "dimuon #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "dimuon #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso04Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "dimuon #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso03Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "#mu_{1} displacedTrackIso03"                , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso04Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "#mu_{1} displacedTrackIso04"                , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso03Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "#mu_{2} displacedTrackIso03"                , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso04Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "#mu_{2} displacedTrackIso04"                , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_chargeProduct"               , "", False, True  , default_norm        , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu vertex charge"                          , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_lxyFromPVvxyDiff"            , "", False, True  , default_norm        , 50 , 0     , 600   , 1e-1  , 1e7   , "#mu vertex |l_{xy}(PV) - v_{xy}|"           , "# events (2018)"   ),
  )
  for category in muonVertexCategories:
    LLPnanoAOD_histograms += (
      Histogram("Event_n"+vertexCollectionName+category               , "", False, True  , default_norm        , 1  , 0     , 20    , 1e-1  , 1e8   , "Number of loose #mu vertices"           , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxy"                  , "", False, True  , default_norm        , 50 , 0     , 600   , 1e-1  , 1e8   , "#mu vertex v_{xy} [cm]"                 , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxySigma"             , "", False, True  , default_norm        , 2  , 0     , 1     , 1e-1  , 1e8   , "#mu vertex #sigma_{v_{xy}} [cm]"        , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxySignificance"      , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-1  , 1e8   , "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vx"                   , "", False, True  , default_norm        , 10 , -600  , 600   , 1e-1  , 1e8   , "#mu vertex v_{x} [cm]"                  , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vy"                   , "", False, True  , default_norm        , 10 , -600  , 600   , 1e-1  , 1e8   , "#mu vertex v_{y} [cm]"                  , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vz"                   , "", False, True  , default_norm        , 20 , -600  , 600   , 1e-1  , 1e8   , "#mu vertex v_{z} [cm]"                  , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxyz"                 , "", False, True  , default_norm        , 50 , 0     , 600   , 1e-1  , 1e8   , "#mu vertex v_{xyz} [cm]"                , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxyzSigma"            , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-1  , 1e8   , "#mu vertex #sigma_{v_{xyz}} [cm]"       , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxyzSignificance"     , "", False, True  , default_norm        , 10 , 0     , 200   , 1e-1  , 1e8   , "#mu vertex v_{xyz}/#sigma_{v_{xyz}} [cm]", "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_dR"                   , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-1  , 1e8   , "#mu vertex #Delta R"                    , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_chi2"                 , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e8   , "#mu vertex #chi^{2}"                    , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_normChi2"             , "", False, True  , default_norm        , 500 , 0     , 50    , 1e-2  , 1e6   , "#mu vertex #chi^{2}/ndof"               , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_ndof"                 , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-1  , 1e8   , "#mu vertex ndof"                        , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_hitsInFrontOfVert1"   , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-2  , 1e8   , "# #mu_{1} hits in front of #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_hitsInFrontOfVert2"   , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-2  , 1e8   , "# #mu_{1} hits in front of #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_hitsInFrontOfVertSum" , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "# #mu_{1} hits + #mu_{2} hits in front of #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_maxHitsInFrontOfVert" , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "max hits after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_missHitsAfterVert1"   , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "# #mu_{1} hits after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_missHitsAfterVert2"   , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "# #mu_{2} hits after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_missHitsAfterVertSum" , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "# #mu_{1} hits + #mu_{2} after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_maxMissHitsAfterVert" , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "max hits after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_dca"                  , "", False, True  , default_norm        , 1  , 0     , 15    , 1e-2  , 1e8   , "#mu vertex DCA [cm]"                      , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_collinearityAngle"    , "", False, True  , default_norm        , 1  , -4    , 4     , 1e-2  , 1e8   , "#mu vertex |#Delta #Phi|"                 , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_nPixelHits1"          , "", False, True  , default_norm        , 1  , 0     , 15    , 1e-2  , 1e8   , "#mu_{1} N(pixel hits)"                    , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_nPixelHits2"          , "", False, True  , default_norm        , 1  , 0     , 15    , 1e-2  , 1e8   , "#mu_{1} N(pixel hits)"                    , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_deltaPixelHits"       , "", False, True  , default_norm        , 1  , 0     , 15    , 1e-2  , 1e8   , "#Delta N(pixel hits)"                     , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_nTrackeryLayers1"     , "", False, True  , default_norm        , 1  , 0     , 20    , 1e-2  , 1e8   , "#mu_{1} N(tracker layers)"                , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_nTrackeryLayers2"     , "", False, True  , default_norm        , 1  , 0     , 20    , 1e-2  , 1e8   , "#mu_{1} N(tracker layers)"                , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_lxyFromPV"            , "", False, True  , default_norm        , 50 , 0     , 600   , 1e-2  , 1e8   , "#mu vertex L_{xy}"                        , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_invMass"              , "", False, True  , default_norm        , 1  , 0     , 200   , 1e-2  , 1e8   , "#mu vertex M_{#mu #mu}"                   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_pt"                   , "", False, True  , default_norm        , 10 , 0     , 300   , 1e-2  , 1e8   , "#mu vertex p_{T}"                         , "# events (2018)"   ),
    )
  
extraMuonVertexCollections = ["GoodLooseMuonsVertexWithLargeDR", "GoodLooseMuonsVertex", "GoodDisplacedLooseMuonsVertex"]
for vertexCollectionName in extraMuonVertexCollections:
  LLPnanoAOD_histograms += (
    # Histogram(vertexCollectionName+"_vxErr"     , "", False, True  , default_norm              , 1  , 0     , 10    , 1e0   , 1e8   , "#mu vertex #sigma_{v_{x}} [cm]"                      , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vxSignificance" , "", False, True  , default_norm         , 10 , 0     , 100   , 1e0   , 1e8   , "#mu vertex v_{x}/#sigma_{v_{x}} [cm]"                , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vyErr"     , "", False, True  , default_norm              , 1  , 0     , 10    , 1e0   , 1e8   , "#mu vertex #sigma_{v_{y}} [cm]"                      , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vySignificance" , "", False, True  , default_norm         , 10 , 0     , 100   , 1e0   , 1e8   , "#mu vertex v_{y}/#sigma_{v_{y}} [cm]"                , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vzErr"     , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "#mu vertex #sigma_{v_{z}} [cm]"                      , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_vzSignificance" , "", False, True  , default_norm         , 10 , 0     , 100   , 1e-1  , 1e8   , "#mu vertex v_{z}/#sigma_{v_{z}} [cm]"                , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_originalMuonIdx1"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_originalMuonIdx2"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_isDSAMuon1", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
    # Histogram(vertexCollectionName+"_isDSAMuon2", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "dimuon #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso04Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "dimuon #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "dimuon #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso04Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "dimuon #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso03Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "#mu_{1} displacedTrackIso03"                , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso04Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "#mu_{1} displacedTrackIso04"                , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso03Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "#mu_{2} displacedTrackIso03"                , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_displacedTrackIso04Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "#mu_{2} displacedTrackIso04"                , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_chargeProduct"               , "", False, True  , default_norm        , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu vertex charge"                          , "# events (2018)"   ),
    Histogram(vertexCollectionName+"_lxyFromPVvxyDiff"            , "", False, True  , default_norm        , 50 , 0     , 600   , 1e-1  , 1e7   , "#mu vertex |l_{xy}(PV) - v_{xy}|"           , "# events (2018)"   ),
  )
  for category in muonVertexCategories:
    LLPnanoAOD_histograms += (
      Histogram("Event_n"+vertexCollectionName+category               , "", False, True  , default_norm        , 1  , 0     , 20    , 1e-1  , 1e8   , "Number of loose #mu vertices"           , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxy"                  , "", False, True  , default_norm        , 50 , 0     , 600   , 1e-1  , 1e8   , "#mu vertex v_{xy} [cm]"                 , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxySigma"             , "", False, True  , default_norm        , 2  , 0     , 1     , 1e-1  , 1e8   , "#mu vertex #sigma_{v_{xy}} [cm]"        , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxySignificance"      , "", False, True  , default_norm        , 5  , 0     , 50    , 1e-1  , 1e8   , "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vx"                   , "", False, True  , default_norm        , 10 , -600  , 600   , 1e-1  , 1e8   , "#mu vertex v_{x} [cm]"                  , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vy"                   , "", False, True  , default_norm        , 10 , -600  , 600   , 1e-1  , 1e8   , "#mu vertex v_{y} [cm]"                  , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vz"                   , "", False, True  , default_norm        , 20 , -600  , 600   , 1e-1  , 1e8   , "#mu vertex v_{z} [cm]"                  , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxyz"                 , "", False, True  , default_norm        , 50 , 0     , 600   , 1e-1  , 1e8   , "#mu vertex v_{xyz} [cm]"                , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxyzSigma"            , "", False, True  , default_norm        , 1  , 0     , 1     , 1e-1  , 1e8   , "#mu vertex #sigma_{v_{xyz}} [cm]"       , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_vxyzSignificance"     , "", False, True  , default_norm        , 10 , 0     , 200   , 1e-1  , 1e8   , "#mu vertex v_{xyz}/#sigma_{v_{xyz}} [cm]", "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_dR"                   , "", False, True  , default_norm        , 5  , 0     , 6     , 1e-1  , 1e8   , "#mu vertex #Delta R"                    , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_chi2"                 , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e8   , "#mu vertex #chi^{2}"                    , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_normChi2"             , "", False, True  , default_norm        , 500 , 0     , 50    , 1e-2  , 1e6   , "#mu vertex #chi^{2}/ndof"               , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_ndof"                 , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-1  , 1e8   , "#mu vertex ndof"                        , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_hitsInFrontOfVert1"   , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-2  , 1e8   , "# #mu_{1} hits in front of #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_hitsInFrontOfVert2"   , "", False, True  , default_norm        , 1  , 0     , 35    , 1e-2  , 1e8   , "# #mu_{1} hits in front of #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_hitsInFrontOfVertSum" , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "# #mu_{1} hits + #mu_{2} hits in front of #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_maxHitsInFrontOfVert" , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "max hits after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_missHitsAfterVert1"   , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "# #mu_{1} hits after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_missHitsAfterVert2"   , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "# #mu_{2} hits after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_missHitsAfterVertSum" , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "# #mu_{1} hits + #mu_{2} after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_maxMissHitsAfterVert" , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "max hits after #mu vertex fit"   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_dca"                  , "", False, True  , default_norm        , 1  , 0     , 500   , 1e-2  , 1e8   , "#mu vertex DCA [cm]"                      , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_collinearityAngle"    , "", False, True  , default_norm        , 1  , -4    , 4     , 1e-2  , 1e8   , "#mu vertex |#Delta #Phi|"                 , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_nPixelHits1"          , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "#mu_{1} N(pixel hits)"                    , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_nPixelHits2"          , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "#mu_{1} N(pixel hits)"                    , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_deltaPixelHits"       , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "#Delta N(pixel hits)"                     , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_nTrackeryLayers1"     , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "#mu_{1} N(tracker layers)"                , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_nTrackeryLayers2"     , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "#mu_{1} N(tracker layers)"                , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_lxyFromPV"            , "", False, True  , default_norm        , 50 , 0     , 600   , 1e-2  , 1e8   , "#mu vertex L_{xy}"                        , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_invMass"              , "", False, True  , default_norm        , 1  , 0     , 200   , 1e-2  , 1e8   , "#mu vertex M_{#mu #mu}"                   , "# events (2018)"   ),
      Histogram(vertexCollectionName+category+"_pt"                   , "", False, True  , default_norm        , 1  , 0     , 50    , 1e-2  , 1e8   , "#mu vertex p_{T}"                         , "# events (2018)"   ),
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
  Histogram("SegmentMatchLooseMuons_dxy"                , "", False, True  , default_norm       , 20 , -200  , 200   , 1e-1  , 1e8   , "Segment matched loose PAT #mu d_{xy} [cm]"               , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_dxyPVTraj"          , "", False, True  , default_norm       , 20 , -100  , 100   , 1e-3  , 1e6   , "Segment matched loose PAT #mu d_{xy} [cm]"               , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_dxyPVTrajSig"       , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose PAT #mu d_{xy} significance"       , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_dz"                 , "", False, True  , default_norm       , 20 , -200  , 200   , 1e-1  , 1e8   , "Segment matched loose PAT #mu d_{z} [cm]"                , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_dzPV"               , "", False, True  , default_norm       , 20 , -200  , 200   , 1e-1  , 1e8   , "Segment matched loose PAT #mu d_{z} [cm]"                , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_dzPVErr"            , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose PAT #mu d_{z} uncertainty [cm]"    , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_dzPVSig"            , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose PAT #mu d_{z} significance"        , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_ip3DPVSigned"       , "", False, True  , default_norm       , 100, -500  , 500   , 1e-3  , 1e6   , "Segment matched loose PAT #mu 3D IP [cm]"                , "# events (2018)"   ),
  Histogram("SegmentMatchLooseMuons_ip3DPVSignedSig"    , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose PAT #mu 3D IP significance"        , "# events (2018)"   ),

  Histogram("Event_nSegmentMatchLooseDSAMuons"          , "", False, True  , default_norm       , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale  , "Number of segment matched loose DSA #mu" , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_genMinDR"        , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "min #Delta R(loose DSA #mu, gen #mu)"                    , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_genMinDRidx"     , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "gen #mu index"                                           , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_pt"              , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "Segment matched loose DSA #mu p_{T} [GeV]"               , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_eta"             , "", False, True  , default_norm       , 10 , -3    , 3     , 1e-1  , 1e7   , "Segment matched loose DSA #mu #eta"                      , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_dxy"             , "", False, True  , default_norm       , 20 , -200  , 200   , 1e-1  , 1e8   , "Segment matched loose DSA #mu d_{xy} [cm]"               , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_dxyPVTraj"       , "", False, True  , default_norm       , 20 , -100  , 100   , 1e-3  , 1e6   , "Segment matched loose DSA #mu d_{xy} [cm]"               , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_dxyPVTrajSig"    , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose DSA #mu d_{xy} significance"       , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_dz"              , "", False, True  , default_norm       , 20 , -200  , 200   , 1e-1  , 1e8   , "Segment matched loose DSA #mu d_{z} [cm]"                , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_dzPV"            , "", False, True  , default_norm       , 20 , -200  , 200   , 1e-1  , 1e8   , "Segment matched loose DSA #mu d_{z} [cm]"                , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_dzPVErr"         , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose DSA #mu d_{z} uncertainty [cm]"    , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_dzPVSig"         , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose DSA #mu d_{z} significance"        , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_ip3DPVSigned"    , "", False, True  , default_norm       , 100, -500  , 500   , 1e-3  , 1e6   , "Segment matched loose DSA #mu 3D IP [cm]"                , "# events (2018)"   ),
  Histogram("SegmentMatchLooseDSAMuons_ip3DPVSignedSig" , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "Segment matched loose DSA #mu 3D IP significance"        , "# events (2018)"   ),

  Histogram("Event_nSegmentOuterDRMatchLooseMuons"           , "", False, True  , default_norm       , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale  , "Number of loose PAT #mu"     , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_genMinDR"         , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "min #Delta R(loose PAT #mu, gen #mu)"        , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_genMinDRidx"      , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "gen #mu index"                               , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_nSegments"        , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu #segments"                     , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_matchingRatio"    , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu matching ratio"                , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_maxMatches"       , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu max #matched segments"         , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_muonMatchIdx"     , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu matched index"                 , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_pt"               , "", False, True  , default_norm       , 20 , 0     , 500   , 1e-1  , 1e5   , "loose PAT #mu p_{T} [GeV]"                   , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_eta"              , "", False, True  , default_norm       , 10 , -3    , 3     , 1e-1  , 1e7   , "loose PAT #mu #eta"                          , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_dxy"              , "", False, True  , default_norm       , 20 , -200  , 200   , 1e-1  , 1e8   , "loose PAT #mu d_{xy} [cm]"                   , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_dxyPVTraj"        , "", False, True  , default_norm       , 20 , -100  , 100   , 1e-3  , 1e6   , "loose PAT #mu d_{xy} [cm]"                   , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_dxyPVTrajSig"     , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "loose PAT #mu d_{xy} significance"           , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_dz"               , "", False, True  , default_norm       , 20 , -200  , 200   , 1e-1  , 1e8   , "loose PAT #mu d_{z} [cm]"                    , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_dzPV"             , "", False, True  , default_norm       , 20 , -200  , 200   , 1e-1  , 1e8   , "loose PAT #mu d_{z} [cm]"                    , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_dzPVErr"          , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "loose PAT #mu d_{z} uncertainty [cm]"        , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_dzPVSig"          , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "loose PAT #mu d_{z} significance"            , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_ip3DPVSigned"     , "", False, True  , default_norm       , 100, -500  , 500   , 1e-3  , 1e6   , "loose PAT #mu 3D IP [cm]"                    , "# events (2018)"   ),
  Histogram("SegmentOuterDRMatchLooseMuons_ip3DPVSignedSig"  , "", False, True  , default_norm       , 20 , 0     , 200   , 1e-1  , 1e8   , "loose PAT #mu 3D IP significance"            , "# events (2018)"   ),

  Histogram("LooseDSAMuons_nSegments"             , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #segments"                     , "# events (2018)"   ),
  Histogram("LooseDSAMuons_nDTHits"               , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #DT segments"                  , "# events (2018)"   ),
  Histogram("LooseDSAMuons_nCSCHits"              , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #CSC segments"                 , "# events (2018)"   ),
  Histogram("LooseDSAMuons_nDTpluCSCHits"         , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #DT + CSC segments"            , "# events (2018)"   ),
  Histogram("LooseDSAMuons_muonMatch1"            , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #matching PAT segments"        , "# events (2018)"   ),
  Histogram("LooseDSAMuons_muonMatch2"            , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #matching PAT segments"        , "# events (2018)"   ),
  Histogram("LooseDSAMuons_muonMatch3"            , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu #matching PAT segments"        , "# events (2018)"   ),
  Histogram("LooseDSAMuons_matchRatio1"           , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu matching ratio"                , "# events (2018)"   ),
  Histogram("LooseDSAMuons_matchRatio2"           , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu matching ratio"                , "# events (2018)"   ),
  Histogram("LooseDSAMuons_matchRatio3"           , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Loose DSA #mu matching ratio"                , "# events (2018)"   ),

  Histogram("LooseDSAMuons_PATOuterDR"            , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Outer #Delta R(loose DSA #mu, loose PAT #mu)"        , "# events (2018)"   ),
  Histogram("LooseDSAMuons_PATProxDR"             , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Proximity #Delta R(loose DSA #mu, loose PAT #mu)"    , "# events (2018)"   ),
  Histogram("LooseDSAMuons_PATDR"                 , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "#Delta R(loose DSA #mu, loose PAT #mu)"              , "# events (2018)"   ),
  Histogram("LooseDSAMuons_PATDEta"               , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "#Delta #eta (loose DSA #mu, loose PAT #mu)"          , "# events (2018)"   ),
  Histogram("LooseDSAMuons_PATDPhi"               , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "#Delta #phi (loose DSA #mu, loose PAT #mu)"          , "# events (2018)"   ),
  Histogram("LooseDSAMuons_PATDOuterEta"          , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Outer #Delta #eta (loose DSA #mu, loose PAT #mu)"    , "# events (2018)"   ),
  Histogram("LooseDSAMuons_PATDOuterPhi"          , "", False, True  , default_norm       , 1  , 0     , 50    , 1e-1  , 1e5   , "Outer #Delta #phi (loose DSA #mu, loose PAT #mu)"    , "# events (2018)"   ),
)

histograms_genALPs = (
  Histogram("Event_nGenMuonFromALP"               , "", False, True  , default_norm            , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen #mu from ALP"     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_pdgId"                , "", False, True  , default_norm            , 1  , -100  , 100   , 1e-2   , 1e6   , "Gen #mu particle ID"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vx"                   , "", False, True  , default_norm            , 100, -1000 , 1000  , 1e-2   , 1e6   , "Gen #mu v_{x} [cm]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vy"                   , "", False, True  , default_norm            , 100, -1000 , 1000  , 1e-2   , 1e6   , "Gen #mu v_{y} [cm]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vz"                   , "", False, True  , default_norm            , 100, -1000 , 1000  , 1e-2   , 1e6   , "Gen #mu v_{z} [cm]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxy"                  , "", False, True  , default_norm            , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen #mu v_{xy} [cm]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxyz"                 , "", False, True  , default_norm            , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen #mu v_{xyz} [cm]"                           , "# events (2018)"   ),
  Histogram("GenMuonFromALP_dxy"                  , "", False, True  , default_norm            , 200, -1000 , 1000  , 1e-2   , 1e4   , "Gen #mu d_{xy} [cm]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxyALPboostpT"        , "", False, True  , default_norm            , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen proper #mu v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxyALPboostT"         , "", False, True  , default_norm            , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen proper #mu v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxyzALPboostp"        , "", False, True  , default_norm            , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen proper #mu v_{xyz} [cm]"                    , "# events (2018)"   ),
  Histogram("GenMuonFromALP_pt"                   , "", False, True  , default_norm            , 40 , 0     , 500   , 1e-1   , 1e5   , "Gen #mu p_{T} [GeV]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_eta"                  , "", False, True  , default_norm            , 10 , -3    , 3     , 1e-1   , 1e5   , "Gen #mu #eta"                                   , "# events (2018)"   ),
  Histogram("GenMuonFromALP_boost"                , "", False, True  , default_norm            , 1  , 0     , 500   , 1e-2   , 1e6   , "Gen #mu boost [GeV]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_mass"                 , "", False, True  , default_norm            , 1  , 0     , 1     , 1e-2   , 1e6   , "Gen #mu mass [GeV]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_LoosePATMuonsMinDR"     , "", False, True  , default_norm          , 10  , 0     , 3     , 1e-2   , 1e6   , "#Delta R(Gen #mu, loose #mu)"                   , "# events (2018)"   ),
  Histogram("GenMuonFromALP_LooseDSAMuonsMinDR"     , "", False, True  , default_norm          , 10  , 0     , 3     , 1e-2   , 1e6   , "#Delta R(Gen #mu, loose #mu)"                   , "# events (2018)"   ),
  Histogram("GenMuonFromALP_LooseMuonsDRMatchMinDR" , "", False, True  , default_norm          , 10  , 0     , 3     , 1e-2   , 1e6   , "#Delta R(Gen #mu, loose #mu)"                   , "# events (2018)"   ),
  Histogram("GenMuonFromALP_LooseMuonsOuterDRMatchMinDR", "", False, True  , default_norm      , 10  , 0     , 3     , 1e-2   , 1e6   , "#Delta R(Gen #mu, loose #mu)"                   , "# events (2018)"   ),
  Histogram("GenMuonFromALP_LooseMuonsSegmentMatchMinDR", "", False, True  , default_norm      , 10  , 0     , 3     , 1e-2   , 1e6   , "#Delta R(Gen #mu, loose #mu)"                   , "# events (2018)"   ),
  Histogram("Event_nGenDimuonFromALP"             , "", False, True  , default_norm            , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen di-muons from ALP"                , "# events (2018)"   ),
  Histogram("GenDimuonFromALP_invMass"            , "", False, True  , default_norm            , 10 , 0     , 10    , 1e-1  , 1e5   , "Gen m_{#mu #mu} [GeV]"                          , "# events (2018)"   ),
  Histogram("GenDimuonFromALP_deltaR"             , "", False, True  , default_norm            , 1  , 0     , 1     , 1e-1  , 1e8   , "Gen #Delta R(#mu #mu)"                          , "# events (2018)"   ),
  Histogram("GenDimuonFromALP_deltaEta"           , "", False, True  , default_norm            , 1  , -3    , 3     , 1e-1  , 1e8   , "Gen #Delta #eta (#mu #mu)"                      , "# events (2018)"   ),
  Histogram("GenDimuonFromALP_deltaPhi"           , "", False, True  , default_norm            , 1  , -3    , 3     , 1e-1  , 1e8   , "Gen #Delta #phi (#mu #mu)"                      , "# events (2018)"   ),
  # Histogram("Event_nGenALP"                       , "", False, True  , default_norm             , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen ALP"                     , "# events (2018)"   ),
  # Histogram("GenALP_vx"                           , "", False, True  , default_norm             , 50 , -1000 , 1000  , 1e-1   , 1e6   , "Gen ALP v_{x} [cm]"                             , "# events (2018)"   ),
  # Histogram("GenALP_vy"                           , "", False, True  , default_norm             , 50 , -1000 , 1000  , 1e-1   , 1e6   , "Gen ALP v_{y} [cm]"                             , "# events (2018)"   ),
  # Histogram("GenALP_vz"                           , "", False, True  , default_norm             , 50 , -1000 , 1000  , 1e-1   , 1e6   , "Gen ALP v_{z} [cm]"                             , "# events (2018)"   ),
  # Histogram("GenALP_vxy"                          , "", False, True  , default_norm             , 50 , 0     , 1000  , 1e-1   , 1e6   , "Gen ALP v_{xy} [cm]"                            , "# events (2018)"   ),
  # Histogram("GenALP_pt"                           , "", False, True  , default_norm             , 1  , 0     , 500   , 1e-1  , 1e8   , "Gen ALP p_{T} [GeV]"                            , "# events (2018)"   ),
  # # Histogram("GenALP_boost"                        , "", False, True  , default_norm             , 1  , 0     , 500   , 1e-1  , 1e8   , "Gen ALP boost [GeV]"                            , "# events (2018)"   ),
  # Histogram("GenALP_mass"                         , "", False, True  , default_norm             , 1  , 0     , 10    , 1e-1  , 1e8   , "Gen ALP mass [GeV]"                             , "# events (2018)"   ),

)

for method in muonMatchingMethods:
  collectionName = "LooseMuonsFromALP"+method+"Match"
  histograms_genALPs += (
    Histogram("Event_n"+collectionName       , "", False, True  , default_norm     , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP"           , "# events (2018)"   ),
    Histogram(collectionName+"_pt"           , "", False, True  , default_norm     , 20 , 0     , 500   , 1e-1  , 1e5   , "loose #mu from ALP p_{T} [GeV]"                          , "# events (2018)"   ),
    Histogram(collectionName+"_eta"          , "", False, True  , default_norm     , 10 , -3    , 3     , 1e-1  , 1e5   , "loose #mu from ALP #eta"                                 , "# events (2018)"   ),
    Histogram(collectionName+"_phi"          , "", False, True  , default_norm     , 10 , -3    , 3     , 1e-1  , 1e5   , "loose #mu from ALP #phi"                                 , "# events (2018)"   ),
    Histogram(collectionName+"_dxy"          , "", False, True  , default_norm     , 20 , -200  , 200   , 1e-3  , 1e5   , "loose #mu from ALP d_{xy} [cm]"                          , "# events (2018)"   ),
    Histogram(collectionName+"_dxyPVTraj"    , "", False, True  , default_norm     , 20 , -100  , 100   , 1e-3  , 1e5   , "loose #mu from ALP d_{xy} [cm]"                          , "# events (2018)"   ),
    Histogram(collectionName+"_dxyPVTrajErr" , "", False, True  , default_norm     , 20 , 0     , 200   , 1e-3  , 1e5   , "loose #mu from ALP d_{xy} uncertainty [cm]"              , "# events (2018)"   ),
    Histogram(collectionName+"_dxyPVTrajSig" , "", False, True  , default_norm     , 20 , 0     , 200   , 1e-3  , 1e5   , "loose #mu from ALP d_{xy} significance"                  , "# events (2018)"   ),
    Histogram(collectionName+"_dz"           , "", False, True  , default_norm     , 20 , -200  , 200   , 1e-3  , 1e5   , "loose #mu from ALP d_{z} [cm]"                           , "# events (2018)"   ),
    Histogram(collectionName+"_dzPV"         , "", False, True  , default_norm     , 20 , -200  , 200   , 1e-3  , 1e5   , "loose #mu from ALP d_{z} [cm]"                           , "# events (2018)"   ),
    Histogram(collectionName+"_dzPVErr"      , "", False, True  , default_norm     , 20 , 0     , 200   , 1e-3  , 1e5   , "loose #mu from ALP d_{z} uncertainty [cm]"               , "# events (2018)"   ),
    Histogram(collectionName+"_dzPVSig"      , "", False, True  , default_norm     , 20 , 0     , 200   , 1e-3  , 1e5   , "loose #mu from ALP d_{z} significance"                   , "# events (2018)"   ),
    Histogram(collectionName+"_ip3DPVSigned"    , "", False, True  , default_norm  , 100, -500  , 500   , 1e-3  , 1e5   , "loose #mu from ALP 3D IP [cm]"                           , "# events (2018)"   ),
    Histogram(collectionName+"_ip3DPVSignedErr" , "", False, True  , default_norm  , 20 , 0     , 200   , 1e-3  , 1e5   , "loose #mu from ALP 3D IP uncertainty [cm]"               , "# events (2018)"   ),
    Histogram(collectionName+"_ip3DPVSignedSig" , "", False, True  , default_norm  , 20 , 0     , 200   , 1e-3  , 1e5   , "loose #mu from ALP 3D IP significance"                   , "# events (2018)"   ),
    Histogram(collectionName+"_nSegments"    , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-1  , 1e5   , "loose #mu from ALP number of segments"                   , "# events (2018)"   ),
    Histogram(collectionName+"_invMass"      , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-1  , 1e5   , "loose m_{#mu #mu} from ALP [GeV]"                        , "# events (2018)"   ),
    Histogram(collectionName+"_deltaR"       , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-1  , 1e5   , "loose #Delta R (#mu #mu) from ALP [GeV]"                 , "# events (2018)"   ),
    Histogram(collectionName+"_outerDeltaR"  , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-1  , 1e5   , "loose outer #Delta R (#mu #mu) from ALP [GeV]"           , "# events (2018)"   ),
    Histogram(collectionName+"_deltaEta"     , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-1  , 1e5   , "loose #Delta #eta (#mu #mu) from ALP [GeV]"              , "# events (2018)"   ),
    Histogram(collectionName+"_deltaPhi"     , "", False, True  , default_norm     , 10 , 0     , 10    , 1e-1  , 1e5   , "loose #Delta #phi (#mu #mu) from ALP [GeV]"              , "# events (2018)"   ),
  
    Histogram("Event_n"+collectionName+"Vertex"    , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e9*y_scale   , "Number of loose #mu from ALP vertices"                     , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_vxy"       , "", False, True  , default_norm              , 50 , 0     , 600   , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{xy} [cm]"                     , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_vxySigma"  , "", False, True  , default_norm              , 10 , 0     , 100   , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_vxySignificance"  , "", False, True  , default_norm       , 50 , 0     , 600   , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{xy}/#sigma_{v_{xy}} [cm]"     , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_vxyz"      , "", False, True  , default_norm              , 50 , 0     , 600   , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{xyz} [cm]"                    , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_vxyzSigma" , "", False, True  , default_norm              , 10 , 0     , 100   , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex #sigma_{v_{xyz}} [cm]"           , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_vxyzSignificance" , "", False, True  , default_norm       , 50 , 0     , 600   , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{xyz}/#sigma_{v_{xyz}} [cm]"   , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_vx"        , "", False, True  , default_norm              , 20 , -600  , 600   , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{x} [cm]"                      , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_vy"        , "", False, True  , default_norm              , 20 , -600  , 600   , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{y} [cm]"                      , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_vz"        , "", False, True  , default_norm              , 20 , -600  , 600   , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{z} [cm]"                      , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_dR"        , "", False, True  , default_norm              , 1  , 0     , 1     , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex #Delta R"                        , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_proxDR"    , "", False, True  , default_norm              , 1  , 0     , 1     , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex #Delta R"                        , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_chi2"      , "", False, True  , default_norm              , 1  , 0     , 10    , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex #chi^{2}"                        , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_normChi2"  , "", False, True  , default_norm              , 10 , 0     , 50    , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex #chi^{2}/ndof"                   , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_ndof"      , "", False, True  , default_norm              , 1  , 0     , 10    , 1e0*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex ndof"                            , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_originalMuonIdx1"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_originalMuonIdx2"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_isDSAMuon1", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_isDSAMuon2", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_displacedTrackIso04Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_displacedTrackIso04Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_displacedTrackIso03Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso03"                , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_displacedTrackIso04Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso04"                , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_displacedTrackIso03Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso03"                , "# events (2018)"   ),
    Histogram(collectionName+"Vertex_displacedTrackIso04Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso04"                , "# events (2018)"   ),
  )

histogramsRatio_plots = [

  ( Histogram("SegmentDRMatchMuon_pt"                   , "", False, False  , default_norm   , 40 , 0     , 500   , 0    , 1.5 , "p_{T}^{#mu} [GeV]"         , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_pt"                     , "", False, False  , default_norm   , 40 , 0     , 500   , 0    , 1.5 , "p_{T}^{#mu} [GeV]"         , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_eta"                  , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#eta^{#mu}"                , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_eta"                    , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#eta^{#mu}"                , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_phi"                  , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#phi^{#mu}"                , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_phi"                    , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#phi^{#mu}"                , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_dxy"                  , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dxy"                    , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_dzPV"                 , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{z}^{#mu} [cm]"          , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dzPV"                   , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{z}^{#mu} [cm]"          , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_dzPVSig"              , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{z}^{#mu} significance"  , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dzPVSig"                , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{z}^{#mu} significance"  , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_dxyPVTraj"            , "", False, False  , default_norm   , 1  , 0     , 5    , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dxyPVTraj"              , "", False, False  , default_norm   , 1  , 0     , 5    , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_dxyPVTrajSig"         , "", False, False  , default_norm   , 50 , 0     , 250   , 0    , 1.5 , "d_{xy}^{#mu} significance" , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dxyPVTrajSig"           , "", False, False  , default_norm   , 50 , 0     , 250   , 0    , 1.5 , "d_{xy}^{#mu} significance" , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_ip3DPVSigned"         , "", False, False  , default_norm   , 50 , 0     , 500   , 0    , 1.5 , "#mu 3D IP [cm]"            , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_ip3DPVSigned"           , "", False, False  , default_norm   , 50 , 0     , 500   , 0    , 1.5 , "#mu 3D IP [cm]"            , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_ip3DPVSignedSig"      , "", False, False  , default_norm   , 50 , 0     , 200   , 0    , 1.5 , "#mu 3D IP significance"    , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_ip3DPVSignedSig"        , "", False, False  , default_norm   , 50 , 0     , 200   , 0    , 1.5 , "#mu 3D IP significance"    , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentDRMatchMuon_matchingRatio"        , "", False, False  , default_norm   , 10 , 0     , 1.033 , 0    , 1.5 , "Muon segment matches / DSA segments"    , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_matchingRatio"          , "", False, False  , default_norm   , 10 , 0     , 1.033 , 0    , 1.5 , "Muon segment matches / DSA segments"    , "Outer #Delta R-matched efficiency"   ) ),
  
  ( Histogram("SegmentOuterDRMatchMuon_pt"              , "", False, False  , default_norm   , 40 , 0     , 500   , 0    , 1.5 , "p_{T}^{#mu} [GeV]"         , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_pt"                     , "", False, False  , default_norm   , 40 , 0     , 500   , 0    , 1.5 , "p_{T}^{#mu} [GeV]"         , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_eta"             , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#eta^{#mu}"                , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_eta"                    , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#eta^{#mu}"                , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_phi"             , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#phi^{#mu}"                , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_phi"                    , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 1.5 , "#phi^{#mu}"                , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_dxy"             , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dxy"                    , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_dzPV"            , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{z}^{#mu} [cm]"          , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dzPV"                   , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{z}^{#mu} [cm]"          , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_dzPVSig"         , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{z}^{#mu} significance"  , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dzPVSig"                , "", False, False  , default_norm   , 40 , 0     , 200   , 0    , 1.5 , "d_{z}^{#mu} significance"  , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_dxyPVTraj"       , "", False, False  , default_norm   , 1  , 0     , 5    , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dxyPVTraj"              , "", False, False  , default_norm   , 1  , 0     , 5    , 0    , 1.5 , "d_{xy}^{#mu} [cm]"         , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_dxyPVTrajSig"    , "", False, False  , default_norm   , 50 , 0     , 250   , 0    , 1.5 , "d_{xy}^{#mu} significance" , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_dxyPVTrajSig"           , "", False, False  , default_norm   , 50 , 0     , 250   , 0    , 1.5 , "d_{xy}^{#mu} significance" , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_ip3DPVSigned"    , "", False, False  , default_norm   , 50 , 0     , 500   , 0    , 1.5 , "#mu 3D IP [cm]"            , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_ip3DPVSigned"           , "", False, False  , default_norm   , 50 , 0     , 500   , 0    , 1.5 , "#mu 3D IP [cm]"            , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_ip3DPVSignedSig" , "", False, False  , default_norm   , 50 , 0     , 200   , 0    , 1.5 , "#mu 3D IP significance"    , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_ip3DPVSignedSig"        , "", False, False  , default_norm   , 50 , 0     , 200   , 0    , 1.5 , "#mu 3D IP significance"    , "Outer #Delta R-matched efficiency"   ) ),
  ( Histogram("SegmentOuterDRMatchMuon_matchingRatio"   , "", False, False  , default_norm   , 10 , 0     , 1.033 , 0    , 1.5 , "Muon segment matches / DSA segments"    , "Outer #Delta R-matched efficiency"   ),
    Histogram("SegmentMatchMuon_matchingRatio"          , "", False, False  , default_norm   , 10 , 0     , 1.033 , 0    , 1.5 , "Muon segment matches / DSA segments"    , "Outer #Delta R-matched efficiency"   ) ),
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

histograms2D = (
  # name  title  logx  logy  logz  normtype  rebinX  rebinY  xmin  xmax  ymin  ymax  zmin  zmax  xlabel  ylabel  zlabel  suffix
)

histograms2D_LLPnanoAOD = (
  # name  title  logx  logy  logz  normtype  rebinX  rebinY  xmin  xmax  ymin  ymax  zmin  zmax  xlabel  ylabel  zlabel  suffix
  # Histogram2D("GoodLooseMuonsVertex_normChi2_ndof",             "",  False,  False,  True,  NormalizationType.to_lumi,  1 ,  1 ,   0, 2   , 0, 5   , 1e0,  1e5,  "Loose #mu #chi^{2}/ndof",                   "Loose #mu ",                      "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_vxySigma_vxy",              "",  False,  False,  True,  NormalizationType.to_lumi,  2 ,  2 ,   0, 1   , 0, 50  , 1e0,  1e5,  "Loose #mu #sigma_{vxy}",                    "Loose #mu v_{xy}",                "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_vxyzSigma_vxyz",            "",  False,  False,  True,  NormalizationType.to_lumi,  2 ,  2 ,   0, 1   , 0, 50  , 1e0,  1e5,  "Loose #mu #sigma_{vxyz}",                   "Loose #mu v_{xyz}",               "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_vxySigma_vxySignificance",  "",  False,  False,  True,  NormalizationType.to_lumi,  5 ,  5 ,   0, 10  , 0, 600 , 1e0,  1e5,  "Loose #mu #sigma_{vxy}",                    "Loose #mu v_{xy}/#sigma_{vxy}",   "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_vxyzSigma_vxyzSignificance","",  False,  False,  True,  NormalizationType.to_lumi,  5 ,  5 ,   0, 10  , 0, 800 , 1e0,  1e5,  "Loose #mu #sigma_{vxyz}",                   "Loose #mu v_{xyz}/#sigma_{vxyz}", "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_vxySignificance_vxy",       "",  False,  False,  True,  NormalizationType.to_lumi,  1 ,  5 ,   0, 100 , 0, 250 , 1e0,  1e5,  "Loose #mu v_{xy}/#sigma_{vxy}",   "Loose #mu v_{xy}",                "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_vxyzSignificance_vxyz",     "",  False,  False,  True,  NormalizationType.to_lumi,  1 ,  5 ,   0, 20  , 0, 250 , 1e0,  1e5,  "Loose #mu v_{xyz}/#sigma_{vxyz}", "Loose #mu v_{xyz}",               "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_vxErr_vx",                  "",  False,  False,  True,  NormalizationType.to_lumi,  10,  10,   0, 10  , 0, 500 , 1e0,  1e5,  "Loose #mu #sigma_{vx}",                     "Loose #mu v_{x}",                 "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_vyErr_vy",                  "",  False,  False,  True,  NormalizationType.to_lumi,  10,  10,   0, 10  , 0, 500 , 1e0,  1e5,  "Loose #mu #sigma_{vy}",                     "Loose #mu v_{y}",                 "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_vzErr_vz",                  "",  False,  False,  True,  NormalizationType.to_lumi,  10,  10,   0, 10  , 0, 500 , 1e0,  1e5,  "Loose #mu #sigma_{vz}",                     "Loose #mu v_{z}",                 "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_normChi2_vxy",              "",  False,  False,  True,  NormalizationType.to_lumi,  2 ,  10,   0, 2   , 0, 200 , 1e0,  1e5,  "Loose #mu #chi^{2}/ndof",                   "Loose #mu v_{xy}",                "# events (2018)",  ""  ),
  # Histogram2D("GoodLooseMuonsVertex_normChi2_vxyz",             "",  False,  False,  True,  NormalizationType.to_lumi,  2 ,  10,   0, 2   , 0, 200 , 1e0,  1e5,  "Loose #mu #chi^{2}/ndof",                   "Loose #mu v_{xyz}",               "# events (2018)",  ""  ),
)

if plots_from_LLPNanoAOD:
  histograms2D = histograms2D + histograms2D_LLPnanoAOD

histograms2D_muonMatching = (
  # name  title  logx  logy  logz  normtype  rebinX  rebinY  xmin  xmax  ymin  ymax  zmin  zmax  xlabel  ylabel  zlabel  suffix

  Histogram2D("LooseDSAMuons_muonMatch1_nSegments",      "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,   0, 50,   0, 50,  1e-1,  1e5,  "Loose DSA #matching segments",  "Loose DSA #segments",    "# events (2018)",  ""  ),
  Histogram2D("LooseDSAMuons_muonMatch2_nSegments",      "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,   0, 50,   0, 50,  1e-1,  1e5,  "Loose DSA #matching segments",  "Loose DSA #segments",    "# events (2018)",  ""  ),
  Histogram2D("LooseDSAMuons_muonMatch3_nSegments",      "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,   0, 50,   0, 50,  1e-1,  1e5,  "Loose DSA #matching segments",  "Loose DSA #segments",    "# events (2018)",  ""  ),

  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_genMinDR",       "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "min #Delta R(PAT #mu, gen #mu)",  "min #Delta R(DSA #mu, gen #mu)",   "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_genMinDRidx",    "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "min #Delta R(PAT #mu, gen #mu) index",  "min #Delta R(DSA #mu, gen #mu) index",   "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_eta",            "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT #eta^{#mu}",        "DSA #eta^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_phi",            "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT #phi^{#mu}",        "DSA #phi^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_outerEta",       "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT outer #eta^{#mu}",  "DSA outer #eta^{#mu}", "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_LooseDSAMuons_outerPhi",       "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT outer #phi^{#mu}",  "DSA outer #phi^{#mu}", "# events (2018)",  ""  ),

  Histogram2D("SegmentMatchLooseMuons_eta_outerEta",              "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT #eta^{#mu}",  "PAT outer #eta^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseMuons_phi_outerPhi",              "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "PAT #phi^{#mu}",  "PAT outer #phi^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseDSAMuons_eta_outerEta",           "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "DSA #eta^{#mu}",  "DSA outer #eta^{#mu}",       "# events (2018)",  ""  ),
  Histogram2D("SegmentMatchLooseDSAMuons_phi_outerPhi",           "",  False,  False,  True,  NormalizationType.to_lumi,  1,  1,  -3,  3,  -3,  3,  1e-1,  1e5,  "DSA #phi^{#mu}",  "DSA outer #phi^{#mu}",       "# events (2018)",  ""  ),
)

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

signal_samples = (
  # Data
  # Sample(
  #   name="SingleMuon",
  #   file_path=f"{base_path}/collision_data2018/SingleMuon2018_{skim}_{hist_path}.root",
  #   type=SampleType.data,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   fill_alpha=0,
  #   marker_size=0.7,
  #   marker_style=20,
  #   marker_color=ROOT.kBlack,
  #   legend_description="SingleMuon2018",
  # ),
  
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
  #   line_color=ROOT.kBlue,
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
  #   line_color=ROOT.kGreen+1,
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
    line_color=ROOT.kCyan,
    legend_description="m_{a} = 1 GeV, c#tau_{a} = 1 cm",
  ),
  # Sample(
  #   name="tta_mAlp-1GeV_ctau-1e2mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e2mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kOrange,
  #   legend_description="m_{a} = 1 GeV, c#tau_{a} = 10 cm",
  # ),
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
  #   line_color=ROOT.kOrange,
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
    fill_color=ROOT.kRed+1,
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
    fill_color=ROOT.kRed+3,
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
    fill_color=ROOT.kRed+4,
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
    fill_color=color_palette_wong[1],
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
    fill_color=color_palette_wong[1],
    fill_alpha=0.7,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),

  # Sample(
  #   name="ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
  #   file_path=f"{base_path}/backgrounds2018/ST_t-channel_top/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.background,
  #   cross_sections=cross_sections,
  #   line_alpha=0,
  #   fill_color=color_palette_wong[2],
  #   fill_alpha=0.7,
  #   marker_size=0,
  #   legend_description="Single top (t-ch.)",
  #   custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-2*legend_height, legend_max_x-legend_width, legend_max_y-1*legend_height, "f")
  # ),
  Sample(
    name="ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
    file_path=f"{base_path}/backgrounds2018/ST_t-channel_antitop/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    fill_color=color_palette_wong[2],
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
    fill_color=ROOT.kMagenta+1,
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
    fill_color=ROOT.kMagenta+1,
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
    fill_alpha=0.7,
    marker_size=0,
    legend_description="W+jets",
  ),
  
  # Sample(
  #   name="ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8",
  #   file_path=f"{base_path}/backgrounds2018/ttZJets/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.background,
  #   cross_sections=cross_sections,
  #   line_alpha=0,
  #   fill_color=41,
  #   fill_alpha=0.7,F
  #   marker_size=0,
  #   legend_description="ttZJets",
  # ),
  Sample(
    name="TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTZToLLNuNu_M-10/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    fill_color=ROOT.kYellow+3,
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
    fill_color=ROOT.kGray,
    fill_alpha=0.7,
    marker_size=0,
    legend_description="ttZ (1-10)",
  ),
  
  # Sample(
  #   name="ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8",
  #   file_path=f"{base_path}/backgrounds2018/ttWJets/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.background,
  #   cross_sections=cross_sections,
  #   line_alpha=0,
  #   fill_color=ROOT.kOrange,
  #   fill_alpha=0.7,
  #   marker_size=0,
  #   legend_description="ttWJets",
  # ),
  Sample(
    name="TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
    file_path=f"{base_path}/backgrounds2018/TTWJetsToLNu/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    fill_color=ROOT.kYellow+1,
    fill_alpha=0.7,
    marker_size=0,
    legend_description="ttW",
  ),
  
  Sample(
    name="ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/ttHToMuMu/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    fill_color=color_palette_wong[3],
    fill_alpha=1.0,
    marker_size=0,
    legend_description="ttH (#mu#mu)",
  ),
  Sample(
    name="ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8",
    file_path=f"{base_path}/backgrounds2018/ttHTobb/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    fill_color=color_palette_wong[4],
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
    fill_color=ROOT.kBlue+1,
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
    fill_color=ROOT.kGray+1,
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
    fill_color=ROOT.kGray+2,
    fill_alpha=0.7,
    marker_size=0,
    legend_description="ttZH",
  ),
  # Sample(
  #   name="TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
  #   file_path=f"{base_path}/backgrounds2018/TTTT/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.background,
  #   cross_sections=cross_sections,
  #   line_alpha=0,
  #   fill_color=ROOT.kGray+3,
  #   fill_alpha=0.7,
  #   marker_size=0,
  #   legend_description="TTTT",
  # ),
    
  Sample(
    name="QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-15To20/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    fill_color=color_palette_wong[0],
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
    fill_color=color_palette_wong[0],
    fill_alpha=1.0,
    marker_size=0,
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  # # Sample(
  # #   name="QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  # #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-30To50/{skim}/{hist_path}/histograms.root",
  # #   type=SampleType.background,
  # #   cross_sections=cross_sections,
  # #   line_alpha=0,
  # #   fill_color=color_palette_wong[0],
  # #   fill_alpha=1.0,
  # #   marker_size=0,
  # #   legend_description=" ",
  # #   custom_legend=Legend(0, 0, 0, 0, "")
  # # ),
  # Sample(
  #   name="QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-50To80/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.background,
  #   cross_sections=cross_sections,
  #   line_alpha=0,
  #   fill_color=color_palette_wong[0],
  #   fill_alpha=1.0,
  #   marker_size=0,
  #   legend_description=" ",
  #   custom_legend=Legend(0, 0, 0, 0, "")
  # ),
  # # Sample(
  # #   name="QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  # #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-80To120/{skim}/{hist_path}/histograms.root",
  # #   type=SampleType.background,
  # #   cross_sections=cross_sections,
  # #   line_alpha=0,
  # #   fill_color=color_palette_wong[0],
  # #   fill_alpha=1.0,
  # #   marker_size=0,
  # #   legend_description=" ",
  # #   custom_legend=Legend(0, 0, 0, 0, "")
  # # ),
  Sample(
    name="QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    file_path=f"{base_path}/backgrounds2018/QCD_Pt-120To170/{skim}/{hist_path}/histograms.root",
    type=SampleType.background,
    cross_sections=cross_sections,
    line_alpha=0,
    fill_color=color_palette_wong[0],
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
    fill_color=color_palette_wong[0],
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
    fill_color=color_palette_wong[0],
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
    fill_color=color_palette_wong[0],
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
    fill_color=color_palette_wong[0],
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
    fill_color=color_palette_wong[0],
    fill_alpha=1.0,
    marker_size=0,
    # legend_description="QCD (#mu enriched)",
    # custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
    legend_description=" ",
    custom_legend=Legend(0, 0, 0, 0, "")
  ),
  # Sample(
  #   name="QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-1000/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.background,
  #   cross_sections=cross_sections,
  #   line_alpha=0,
  #   fill_color=color_palette_wong[0],
  #   fill_alpha=1.0,
  #   marker_size=0,
  #   legend_description="QCD (#mu enriched)",
  #   custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
  #   # legend_description=" ",
  #   # custom_legend=Legend(0, 0, 0, 0, "")
  # ),
)

samples = signal_samples
if plot_background:
  samples = samples + background_samples


custom_stacks_order = (
  "SingleMuon",
  
  
  "ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8",
  "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
  "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
  
  "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
  "TTZH_TuneCP5_13TeV-madgraph-pythia8",
  "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
  
  "ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8",
  "ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8",
  "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",
  
  "DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
  "DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
  
  "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
  "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
  
  
  "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
  "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
  
  "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
  "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
  
  "QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  "QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  "QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  
  "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
  "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
  "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
  
  "tta_mAlp-0p35GeV_ctau-1e-5mm",
  "tta_mAlp-0p35GeV_ctau-1e0mm",
  "tta_mAlp-0p35GeV_ctau-1e1mm",
  "tta_mAlp-0p35GeV_ctau-1e2mm",
  "tta_mAlp-0p35GeV_ctau-1e3mm",
  "tta_mAlp-0p35GeV_ctau-1e5mm",

  "tta_mAlp-1GeV_ctau-1e-5mm",
  "tta_mAlp-1GeV_ctau-1e0mm",
  "tta_mAlp-1GeV_ctau-1e1mm",
  "tta_mAlp-1GeV_ctau-1e2mm",
  "tta_mAlp-1GeV_ctau-1e3mm",
  "tta_mAlp-1GeV_ctau-1e5mm",
)
