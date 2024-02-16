import ROOT
from ROOT import TColor
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from ttalps_cross_sections import *

# base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms/"
# base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps_cms.nosync/data/"
base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms/"

# hist_path = "histograms"
# hist_path = "histograms_pileup"
# hist_path = "histograms_pileupSFs"
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_GenInfo"

# skim = ""
# skim = "skimmed_looseSemileptonic"
# skim = "skimmed_SR_Met50GeV"
skim = "skimmed_looseSemimuonic_GenInfo"
# skim = "skimmed_looseSemimuonic_SRmuonic"
# skim = "skimmed_looseSemimuonic_SRmuonic_DR"
# skim = "skimmed_looseSemimuonic_SRmuonic_OuterDR"
# skim = "skimmed_looseSemimuonic_SRmuonic_Segment"

output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}/"

# luminosity = 63670. # pb^-1
luminosity = 59830. # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

canvas_size = (800, 600)
show_ratio_plots = False
ratio_limits = (0.5, 1.5)

legend_width = 0.17 if show_ratio_plots else 0.20
legend_min_x = 0.45
legend_max_x = 0.80

legend_height = 0.045 if show_ratio_plots else 0.03
legend_max_y = 0.89

n_default_backgrounds = 1

show_cms_labels = True
extraText = "Preliminary"

legends = {
  SampleType.signal: Legend(legend_max_x-2.5*legend_width, legend_max_y-5*legend_height, legend_max_x-2*legend_width, legend_max_y, "l"),
  SampleType.background: Legend(legend_max_x-legend_width, legend_max_y-n_default_backgrounds*legend_height, legend_max_x, legend_max_y, "f"),
  SampleType.data: Legend(legend_max_x-3*(legend_width), legend_max_y-legend_height, legend_max_x-2*(legend_width), legend_max_y, "pl"),
}


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

plots_from_LLPNanoAOD = True

y_scale = 1

if plots_from_LLPNanoAOD:
  # default_norm = NormalizationType.to_background
  default_norm = NormalizationType.to_lumi
  y_scale = 0.1

histograms = (
#           name                                  title logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
  Histogram("Event_nTightMuons"                   , "", True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of tight #mu"                            , "# events (2018)"   ),
  Histogram("TightMuons_pt"                       , "", True  , default_norm              , 50 , 0     , 1000  , 1e-6  , 1e8   , "tight #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # Histogram("TightMuons_leadingPt"                , "", True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e5   , "leading tight #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  # # Histogram("TightMuons_subleadingPt"             , "", True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e4   , "all subleading tight #mu p_{T} [GeV]"           , "# events (2018)"   ),
  Histogram("TightMuons_eta"                      , "", True  , default_norm              , 10 , -3.0  , 5.0   , 1e0   , 1e5   , "tight #mu #eta"                                 , "# events (2018)"   ),
  Histogram("TightMuons_dxy"                      , "", True  , default_norm              , 2  , -0.5  , 0.5   , 1e-2  , 1e10   , "tight #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("TightMuons_dz"                       , "", True  , default_norm              , 2  , -1    , 1     , 1e-2  , 1e8   , "tight #mu d_{z} [cm]"                           , "# events (2018)"   ),
  
  Histogram("TightMuons_pfRelIso04_all"           , "", True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  Histogram("TightMuons_pfRelIso03_chg"           , "", True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  Histogram("TightMuons_pfRelIso03_all"           , "", True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  Histogram("TightMuons_miniPFRelIso_chg"         , "", True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  Histogram("TightMuons_miniPFRelIso_all"         , "", True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  Histogram("TightMuons_jetRelIso"                , "", True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "tight #mu jet Rel Iso"                          , "# events (2018)"   ),
  Histogram("TightMuons_tkRelIso"                 , "", True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "tight #mu track Rel Iso"                       , "# events (2018)"   ),
  
  Histogram("Event_nLooseMuons"                   , "", True  , default_norm              , 1  , 0     , 15    , 1e-2   , 1e7   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuons_pt"                       , "", True  , default_norm              , 1  , 0     , 50    , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuons_leadingPt"                , "", True  , default_norm              , 1  , 0     , 50    , 1e-1  , 1e8   , "leading loose #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  # Histogram("LooseMuons_subleadingPt"             , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "all subleading loose #mu p_{T} [GeV]"           , "# events (2018)"   ),
  Histogram("LooseMuons_eta"                      , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuons_dxy"                      , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuons_dz"                       , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  
  Histogram("LooseMuons_pfRelIso04_all"           , "", True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  Histogram("LooseMuons_pfRelIso03_chg"           , "", True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  Histogram("LooseMuons_pfRelIso03_all"           , "", True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  Histogram("LooseMuons_miniPFRelIso_chg"         , "", True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  Histogram("LooseMuons_miniPFRelIso_all"         , "", True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  Histogram("LooseMuons_jetRelIso"                , "", True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "Loose #mu jet Rel Iso"                          , "# events (2018)"   ),
  Histogram("LooseMuons_tkRelIso"                 , "", True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "Loose #mu track Rel Iso"                       , "# events (2018)"   ),
  
  # # Histogram("Event_nLooseElectrons"               , "", True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose electrons"                      , "# events (2018)"   ),
  # # Histogram("LooseElectrons_pt"                   , "", True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "loose electron p_{T} [GeV]"                     , "# events (2018)"   ),
  # # Histogram("LooseElectrons_leadingPt"            , "", True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "leading loose electron p_{T} [GeV]"             , "# events (2018)"   ),
  # # Histogram("LooseElectrons_subleadingPt"         , "", True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "all subleading loose electron p_{T} [GeV]"      , "# events (2018)"   ),
  # # Histogram("LooseElectrons_eta"                  , "", True  , default_norm              , 5  , -3.5  , 3.5   , 1e-2  , 1e6   , "loose electron #eta"                            , "# events (2018)"   ),
  # # Histogram("LooseElectrons_dxy"                  , "", True  , default_norm              , 10 , -10   , 10    , 1e-2  , 1e6   , "loose electron d_{xy}"                          , "# events (2018)"   ),
  # # Histogram("LooseElectrons_dz"                   , "", True  , default_norm              , 10 , -10   , 10    , 1e-2  , 1e6   , "loose electron d_{z}"                           , "# events (2018)"   ),
  
  Histogram("Event_nGoodJets"                     , "", True  , default_norm              , 1  , 2     , 16    , 1e-2  , 1e10   , "Number of good jets"                            , "# events (2018)"   ),
  # Histogram("GoodJets_pt"                         , "", True  , default_norm              , 25 , 0     , 1300  , 1e-3  , 1e6   , "good jet p_{T} [GeV]"                           , "# events (2018)"   ),
  # Histogram("GoodJets_eta"                        , "", True  , default_norm              , 10 , -3    , 5.0   , 1e1   , 1e6   , "good jet #eta"                                  , "# events (2018)"   ),
  # Histogram("GoodJets_btagDeepB"                  , "", True  , default_norm              , 10 , 0     , 1.5   , 2e0   , 1e6   , "good jet deepCSV score"                         , "# events (2018)"   ),
  Histogram("GoodJets_btagDeepFlavB"              , "", True  , default_norm              , 10 , 0     , 1.8   , 1e-1   , 1e8   , "good jet deepJet score"                         , "# events (2018)"   ),
  
  # Histogram("Event_nGoodMediumBtaggedJets"              , "", True  , default_norm              , 1  , 0     , 20    , 1e0   , 1e9   , "Number of good b-jets"                          , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_pt"                  , "", True  , default_norm              , 50 , 0     , 2000  , 1e-5  , 1e4   , "good b-jet p_{T} [GeV]"                         , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_eta"                 , "", True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e10  , "good b-jet #eta"                                , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_btagDeepB"           , "", True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good b-jet btagDeepB"                           , "# events (2018)"   ),
  
  # Histogram("Event_nGoodNonTightBtaggedJets"           , "", True  , default_norm              , 1  , 0     , 20    , 1e0   , 1e9   , "Number of good non-b jets"                      , "# events (2018)"   ),
  # Histogram("GoodNonTightBtaggedJets_pt"               , "", True  , default_norm              , 50 , 0     , 2000  , 1e-5  , 1e4   , "good non-b jet p_{T} [GeV]"                     , "# events (2018)"   ),
  # Histogram("GoodNonTightBtaggedJets_eta"              , "", True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e10  , "good non-b jet #eta"                            , "# events (2018)"   ),
  # Histogram("GoodNonTightBtaggedJets_btagDeepB"        , "", True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good non-b jet btagDeepB"                       , "# events (2018)"   ),
  
  Histogram("Event_METpt"                         , "", True  , default_norm              , 10 , 0     , 800   , 1e-5  , 1e9   , "MET p_{T} [GeV]"                                , "# events (2018)"   ),
  # Histogram("Event_PV_npvs"                       , "", True  , default_norm              , 1  , 0     , 150   , 1e-3  , 1e12   , "# Primary vertices"                             , "# events (2018)"   ),
  # Histogram("Event_PV_npvsGood"                   , "", True  , default_norm              , 1  , 0     , 150   , 1e-3  , 1e6   , "# Good primary vertices"                        , "# events (2018)"   ),
  
  # Histogram("LooseMuons_dimuonMinv"               , "", True  , default_norm              , 1  , 70    , 110   , 1e0   , 1e4   , "loose muons m_{#mu#mu} [GeV]"                   , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonMinvClosestToZ"     , "", True  , default_norm              , 1  , 70    , 110   , 1e0   , 1e4   , "loose muons closest to Z m_{#mu#mu} [GeV]"      , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaRclosestToZ"   , "", True  , default_norm              , 1  , -1    , 6     , 1e0   , 1e3   , "loose muons closest to Z #Delta R_{#mu#mu}"     , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaEtaclosestToZ" , "", True  , default_norm              , 1  , -1    , 6     , 1e-1  , 1e3   , "loose muons closest to Z #Delta #eta_{#mu#mu}"  , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaPhiclosestToZ" , "", True  , default_norm              , 1  , -3.5  , 6     , 1e-1  , 1e3   , "loose muons closest to Z #Delta #phi_{#mu#mu}"  , "# events (2018)"   ),
  
  # Histogram("TightMuons_deltaPhiMuonMET"          , "", True  , default_norm              , 20 , -4    , 4     , 1e0   , 1e7   , "tight muon #Delta #phi(MET, #mu)"               , "# events (2018)"   ),
  # Histogram("TightMuons_minvMuonMET"              , "", True  , default_norm              , 40 , 0     , 1000  , 1e-4  , 1e5   , "tight muon m_{MET, l} [GeV]"                    , "# events (2018)"   ),
  # Histogram("GoodJets_minvBjet2jets"              , "", True  , default_norm              , 25 , 0     , 1500  , 1e-1  , 1e5   , "good jets m_{bjj} [GeV]"                        , "# events (2018)"   ),

  Histogram("Event_nMuon"                         , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of #mu"                            , "# events (2018)"   ),
  Histogram("Muon_pt"                             , "", True  , default_norm              , 50 , 0     , 1000  , 1e-6  , 1e10   , "#mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("Muon_eta"                            , "", True  , default_norm              , 10 , -3.0  , 5.0   , 1e0   , 1e8   , "#mu #eta"                                 , "# events (2018)"   ),
  Histogram("Muon_dxy"                            , "", True  , default_norm              , 2  , -0.5  , 0.5   , 1e-1  , 1e10   , "#mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("Muon_dz"                             , "", True  , default_norm              , 2  , -1    , 1     , 1e-1  , 1e10   , "#mu d_{z} [cm]"                           , "# events (2018)"   ),

  Histogram("cutFlow"                             , "", True  , default_norm , 1  , 0     , 14     , 1e-1   , 1e13  , "Selection"                                      , "Number of events"  ),
  Histogram("Event_normCheck"                     , "", True  , default_norm , 1  , 0     , 1     , 1e-1  , 1e7   , "norm check"                                     , "# events (2018)"   ),
)

LLPnanoAOD_histograms = (
#           name                                  title logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
  
  Histogram("Muon_idx"                            , "", True  , default_norm              , 1 , 0     , 15  , 1e-6  , 1e10   , "#mu index"                                , "# events (2018)"   ),
  Histogram("Muon_outerEta"                       , "", True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "#mu outer #eta"                           , "# events (2018)"   ),
  Histogram("Muon_outerPhi"                       , "", True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "#mu #phi"                                 , "# events (2018)"   ),
  Histogram("Muon_dsaMatch1"                      , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 1"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch2"                      , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 2"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch3"                      , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 3"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch4"                      , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 4"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch5"                      , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 5"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch1idx"                   , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 1"                       , "# events (2018)"   ),
  Histogram("Muon_dsaMatch2idx"                   , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 2"                       , "# events (2018)"   ),
  Histogram("Muon_dsaMatch3idx"                   , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 3"                       , "# events (2018)"   ),
  Histogram("Muon_dsaMatch4idx"                   , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 4"                       , "# events (2018)"   ),
  Histogram("Muon_dsaMatch5idx"                   , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 5"                       , "# events (2018)"   ),

  Histogram("Event_nDSAMuon"                      , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e9*y_scale   , "Number of dSA #mu"        , "# events (2018)"   ),
  Histogram("DSAMuon_idx"                         , "", True  , default_norm              , 1 , 0     , 15  , 1e-6  , 1e10   , "dSa #mu index"                                , "# events (2018)"   ),
  Histogram("DSAMuon_pt"                          , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "dSA #mu p_{T} [GeV]"                      , "# events (2018)"   ),
  Histogram("DSAMuon_eta"                         , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "dSA #mu #eta"                             , "# events (2018)"   ),
  Histogram("DSAMuon_dxy"                         , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  Histogram("DSAMuon_dz"                          , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  Histogram("DSAMuon_dzPV"                        , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_dxyPV"                         , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  Histogram("DSAMuon_dxyPVTraj"                   , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  Histogram("DSAMuon_dxyPVSigned"                 , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  Histogram("DSAMuon_dzBS"                        , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  Histogram("DSAMuon_dxyBS"                       , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  Histogram("DSAMuon_dxyBSTraj"                   , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  Histogram("DSAMuon_dxyBSSigned"                 , "", True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch1"                  , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 1"           , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch2"                  , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 2"           , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch3"                  , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 3"           , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch4"                  , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 4"           , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch5"                  , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to Pat #mu 5"           , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch1idx"               , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 1"                       , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch2idx"               , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 2"                       , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch3idx"               , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 3"                       , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch4idx"               , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 4"                       , "# events (2018)"   ),
  Histogram("DSAMuon_muonMatch5idx"               , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of Pat #mu 5"                       , "# events (2018)"   ),
  Histogram("DSAMuon_outerEta"                    , "", True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "DSA #mu outer #eta"                           , "# events (2018)"   ),
  Histogram("DSAMuon_outerPhi"                    , "", True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "DSA #mu #phi"                                 , "# events (2018)"   ),

  Histogram("Event_nLooseDSAMuons"                , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose dSA #mu"                        , "# events (2018)"   ),
  Histogram("LooseDSAMuons_pt"                    , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose dSA #mu p_{T} [GeV]"                      , "# events (2018)"   ),
  Histogram("LooseDSAMuons_eta"                   , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose dSA #mu #eta"                             , "# events (2018)"   ),
  Histogram("LooseDSAMuons_dxy"                   , "", True  , default_norm              , 40  , -600  , 600   , 1e-1  , 1e8   , "loose dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  Histogram("LooseDSAMuons_dz"                    , "", True  , default_norm              , 40  , -600  , 600   , 1e-1  , 1e8   , "loose dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  
  Histogram("Event_nLooseMuonsDRMatch"            , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_pt"                , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_eta"               , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_dxy"               , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_dz"                , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_hasOuterDRMatch"   , "", True  , default_norm              , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with outer #Delta R"            , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_hasSegmentMatch"   , "", True  , default_norm              , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with segments/hits"             , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_genMuonDR"         , "", True  , default_norm              , 1  , 0     , 6     , 1e-1  , 1e8   , "#Delta R to gen-level #mu from ALP"             , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsOuterDRMatch"       , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_pt"           , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_eta"          , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_dxy"          , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_dz"           , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_hasDRMatch"   , "", True  , default_norm              , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with #Delta R"                  , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_hasSegmentMatch"   , "", True  , default_norm         , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with segments/hits"             , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_genMuonDR"    , "", True  , default_norm              , 1  , 0     , 6     , 1e-1  , 1e8   , "#Delta R to gen-level #mu from ALP"             , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsSegmentMatch"       , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_pt"           , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_eta"          , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_dxy"          , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_dz"           , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_hasDRMatch"   , "", True  , default_norm              , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with #Delta R"                  , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_hasOuterDRMatch"   , "", True  , default_norm         , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with outer #Delta R"            , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_genMuonDR"    , "", True  , default_norm              , 1  , 0     , 6     , 1e-1  , 1e8   , "#Delta R to gen-level #mu from ALP"             , "# events (2018)"   ),

  # Histogram("Event_nLooseDSAMuonsDRMatch"            , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  # Histogram("LooseDSAMuonsDRMatch_pt"                , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # Histogram("LooseDSAMuonsDRMatch_eta"               , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  # Histogram("LooseDSAMuonsDRMatch_dxy"               , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  # Histogram("LooseDSAMuonsDRMatch_dz"                , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  # Histogram("Event_nLooseDSAMuonsOuterDRMatch"       , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  # Histogram("LooseDSAMuonsOuterDRMatch_pt"           , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # Histogram("LooseDSAMuonsOuterDRMatch_eta"          , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  # Histogram("LooseDSAMuonsOuterDRMatch_dxy"          , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  # Histogram("LooseDSAMuonsOuterDRMatch_dz"           , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("Event_nLooseDSAMuonsSegmentMatch"       , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseDSAMuonsSegmentMatch_pt"           , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseDSAMuonsSegmentMatch_eta"          , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseDSAMuonsSegmentMatch_dxy"          , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseDSAMuonsSegmentMatch_dz"           , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),

  # Histogram("Event_nPatMuonVertex"                , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of Pat-Pat #mu vertices"                 , "# events (2018)"   ),
  # Histogram("PatMuonVertex_vxy"                   , "", True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  # Histogram("PatMuonVertex_vxySigma"              , "", True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  # Histogram("PatMuonVertex_vz"                    , "", True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  # Histogram("PatMuonVertex_dR"                    , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat #mu vertex #Delta R"                        , "# events (2018)"   ),
  # Histogram("PatMuonVertex_chi2"                  , "", True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  # Histogram("PatMuonVertex_idx1"                  , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("PatMuonVertex_idx2"                  , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("PatMuonVertex_isDSAMuon1"            , "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("PatMuonVertex_isDSAMuon2"            , "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("Event_nPatDSAMuonVertex"             , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of Pat-DSA #mu vertices"                 , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_vxy"                , "", True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat-DSA #mu vertex v_{xy} [cm]"                 , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_vxySigma"           , "", True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat-DSA #mu vertex #sigma_{v_{xy}} [cm]"        , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_vz"                 , "", True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat-DSA #mu vertex v_{z} [cm]"                  , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_dR"                 , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat-DSA #mu vertex #Delta R"                    , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_chi2"               , "", True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat-DSA #mu vertex #chi^{2}"                    , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_idx1"               , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_idx2"               , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_isDSAMuon1"         , "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_isDSAMuon2"         , "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("Event_nDSAMuonVertex"                , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of DSA-DSA #mu vertices"                 , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_vxy"                   , "", True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "DSA #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_vxySigma"              , "", True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "DSA #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_vz"                    , "", True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "DSA #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_dR"                    , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "DSA #mu vertex #Delta R"                        , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_chi2"                  , "", True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "DSA #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_idx1"                  , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_idx2"                  , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_isDSAMuon1"            , "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_isDSAMuon2"            , "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  

  # Histogram("Event_nLooseMuonVertexDRMatch"         , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of Pat-Pat #mu vertices"                 , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_vxy"            , "", True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_vxySigma"       , "", True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_vz"             , "", True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_dR"             , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat #mu vertex #Delta R"                        , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_chi2"           , "", True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_idx1"           , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_idx2"           , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_isDSAMuon1"     , "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_isDSAMuon2"     , "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_displacedTrackIso03Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_displacedTrackIso04Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_displacedTrackIso03Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_displacedTrackIso04Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_displacedTrackIso03Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso03"                , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_displacedTrackIso04Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso04"                , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_displacedTrackIso03Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso03"                , "# events (2018)"   ),
  # Histogram("LooseMuonVertexDRMatch_displacedTrackIso04Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso04"                , "# events (2018)"   ),
  # Histogram("Event_nLooseMuonVertexOuterDRMatch"    , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of Pat-Pat #mu vertices"                 , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_vxy"       , "", True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_vxySigma"  , "", True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_vz"        , "", True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_dR"        , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat #mu vertex #Delta R"                        , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_chi2"      , "", True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_idx1"      , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_idx2"      , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_isDSAMuon1", "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_isDSAMuon2", "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_displacedTrackIso03Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_displacedTrackIso04Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_displacedTrackIso03Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_displacedTrackIso04Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_displacedTrackIso03Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso03"                , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_displacedTrackIso04Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso04"                , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_displacedTrackIso03Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso03"                , "# events (2018)"   ),
  # Histogram("LooseMuonVertexOuterDRMatch_displacedTrackIso04Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("Event_nLooseMuonVertexSegmentMatch"    , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of Pat-Pat #mu vertices"                 , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_vxy"       , "", True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_vxySigma"  , "", True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_vz"        , "", True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_dR"        , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat #mu vertex #Delta R"                        , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_chi2"      , "", True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_idx1"      , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_idx2"      , "", True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_isDSAMuon1", "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_isDSAMuon2", "", True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_displacedTrackIso03Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_displacedTrackIso04Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_displacedTrackIso03Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_displacedTrackIso04Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_displacedTrackIso03Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_displacedTrackIso04Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_displacedTrackIso03Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonVertexSegmentMatch_displacedTrackIso04Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso04"                , "# events (2018)"   ),

  Histogram("Event_nGenMuonFromALP"               , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen #mu from ALP"                     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vx"                   , "", True  , default_norm              , 100, -1000 , 1000  , 1e-1   , 1e6   , "Gen #mu v_{x} [cm]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vy"                   , "", True  , default_norm              , 100, -1000 , 1000  , 1e-1   , 1e6   , "Gen #mu v_{y} [cm]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vz"                   , "", True  , default_norm              , 100, -1000 , 1000  , 1e-1   , 1e6   , "Gen #mu v_{z} [cm]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxy"                  , "", True  , default_norm              , 200, 0     , 1000  , 1e-1   , 1e4   , "Gen #mu v_{xy} [cm]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_properVxy"            , "", True  , default_norm              , 200, 0     , 1000  , 1e0   , 1e4   , "Gen proper #mu v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_properVxyALPboost"    , "", True  , default_norm              , 100, 0     , 1000  , 1e0   , 1e4   , "Gen proper #mu v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_pt"                   , "", True  , default_norm              , 5  , 0     , 100    , 1e-1  , 1e8   , "Gen #mu p_{T} [GeV]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_boost"                , "", True  , default_norm              , 1  , 0     , 500   , 1e-1  , 1e8   , "Gen #mu boost [GeV]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_mass"                 , "", True  , default_norm              , 1  , 0     , 1     , 1e-1  , 1e8   , "Gen #mu mass [GeV]"                             , "# events (2018)"   ),
  Histogram("Event_nGenDimuonFromALP"             , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen di-muons from ALP"                , "# events (2018)"   ),
  Histogram("GenDimuonFromALP_invMass"            , "", True  , default_norm              , 1  , 0     , 0.5     , 1e-1  , 1e8   , "Gen m_{#mu #mu} [GeV]"                          , "# events (2018)"   ),
  Histogram("Event_nGenALP"                       , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen ALP"                     , "# events (2018)"   ),
  Histogram("GenALP_vx"                           , "", True  , default_norm              , 50 , -1000 , 1000  , 1e-1   , 1e6   , "Gen ALP v_{x} [cm]"                             , "# events (2018)"   ),
  Histogram("GenALP_vy"                           , "", True  , default_norm              , 50 , -1000 , 1000  , 1e-1   , 1e6   , "Gen ALP v_{y} [cm]"                             , "# events (2018)"   ),
  Histogram("GenALP_vz"                           , "", True  , default_norm              , 50 , -1000 , 1000  , 1e-1   , 1e6   , "Gen ALP v_{z} [cm]"                             , "# events (2018)"   ),
  Histogram("GenALP_vxy"                          , "", True  , default_norm              , 50 , 0     , 1000  , 1e-1   , 1e6   , "Gen ALP v_{xy} [cm]"                            , "# events (2018)"   ),
  Histogram("GenALP_properVxy"                    , "", True  , default_norm              , 50 , 0     , 1000  , 1e0   , 1e8   , "Gen proper ALP v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("GenALP_pt"                           , "", True  , default_norm              , 1  , 0     , 500   , 1e-1  , 1e8   , "Gen ALP p_{T} [GeV]"                            , "# events (2018)"   ),
  Histogram("GenALP_boost"                        , "", True  , default_norm              , 1  , 0     , 500   , 1e-1  , 1e8   , "Gen ALP boost [GeV]"                            , "# events (2018)"   ),
  Histogram("GenALP_mass"                         , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Gen ALP mass [GeV]"                             , "# events (2018)"   ),

  # Histogram("Event_nLooseMuonsFromALPDRMatch"      , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP"                , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPDRMatch_pt"          , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "Loose muons #mu ALP p_{T} [GeV]"              , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPDRMatch_eta"         , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "Loose muons #mu ALP #eta"                     , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPDRMatch_dxy"         , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{xy} [cm]"              , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPDRMatch_dz"          , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{z} [cm]"               , "# events (2018)"   ),
  # Histogram("Event_nLooseMuonsFromALPOuterDRMatch" , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP"                , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPOuterDRMatch_pt"     , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "Loose muons #mu ALP p_{T} [GeV]"              , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPOuterDRMatch_eta"    , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "Loose muons #mu ALP #eta"                     , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPOuterDRMatch_dxy"    , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{xy} [cm]"              , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPOuterDRMatch_dz"     , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{z} [cm]"               , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsFromALPSegmentMatch" , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch_pt"     , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "Loose muons #mu ALP p_{T} [GeV]"              , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch_eta"    , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "Loose muons #mu ALP #eta"                     , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch_dxy"    , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{xy} [cm]"              , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch_dz"     , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{z} [cm]"               , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsFromALPSegmentMatch0p1" , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p1_pt"     , "", True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "Loose muons #mu ALP p_{T} [GeV]"              , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p1_eta"    , "", True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "Loose muons #mu ALP #eta"                     , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p1_dxy"    , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{xy} [cm]"              , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p1_dz"     , "", True  , default_norm              , 10 , -400  , 400   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{z} [cm]"               , "# events (2018)"   ),

 Histogram("Event_nLooseMuonsFromALPVertexSegmentMatch"    , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP vertices"                 , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_vxy"       , "", True  , default_norm              , 10 , 0     , 600   , 1e-2*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_vxySigma"  , "", True  , default_norm              , 2  , 0     , 100   , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_vz"        , "", True  , default_norm              , 20 , -800  , 800   , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex v_{z} [cm]"                      , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_dR"        , "", True  , default_norm              , 1  , 0     , 10    , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #Delta R"                        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_chi2"      , "", True  , default_norm              , 1  , 0     , 20    , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #chi^{2}"                        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_idx1"      , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_idx2"      , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_isDSAMuon1", "", True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_isDSAMuon2", "", True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_displacedTrackIso03Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_displacedTrackIso04Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_displacedTrackIso03Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_displacedTrackIso04Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_displacedTrackIso03Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_displacedTrackIso04Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_displacedTrackIso03Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch_displacedTrackIso04Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsFromALPVertexSegmentMatch0p1"    , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP vertices"                 , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_vxy"       , "", True  , default_norm              , 10 , 0     , 600   , 1e-2*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_vxySigma"  , "", True  , default_norm              , 2  , 0     , 100   , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_vz"        , "", True  , default_norm              , 20 , -800  , 800   , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex v_{z} [cm]"                      , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_dR"        , "", True  , default_norm              , 1  , 0     , 10    , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #Delta R"                        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_chi2"      , "", True  , default_norm              , 1  , 0     , 20    , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #chi^{2}"                        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_idx1"      , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_idx2"      , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_isDSAMuon1", "", True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_isDSAMuon2", "", True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_displacedTrackIso03Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_displacedTrackIso04Dimuon1"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_displacedTrackIso03Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_displacedTrackIso04Dimuon2"  , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_displacedTrackIso03Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_displacedTrackIso04Muon1"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_displacedTrackIso03Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p1_displacedTrackIso04Muon2"    , "", True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso04"                , "# events (2018)"   ),
)

histogramsRatio = [
  ( Histogram("Event_nLooseMuonsDRMatch"       , "", False  , default_norm   , 1  , 0     , 15    , 0    , 2   , "Number of loose #mu"         , "#Delta R-matched / Segment matched"   ),
    Histogram("Event_nLooseMuonsSegmentMatch"  , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsDRMatch_pt"           , "", False  , default_norm   , 20 , 0     , 300   , 0    , 2   , "loose #mu p_{T} [GeV]"       , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_pt"      , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsDRMatch_eta"          , "", False  , default_norm   , 10  , -3   , 3     , 0    , 2   , "loose #mu #eta"              , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_eta"     , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsDRMatch_dxy"          , "", False  , default_norm   , 10 , -400  , 400   , 0    , 2   , "loose #mu d_{xy} [cm]"       , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_dxy"     , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsDRMatch_dz"           , "", False  , default_norm   , 10 , -400  , 400   , 0    , 2   , "loose #mu d_{z} [cm]"        , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_dz"      , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  
  ( Histogram("Event_nLooseMuonsOuterDRMatch"  , "", False  , default_norm   , 1  , 0     , 15    , 0    , 2   , "Number of loose #mu"         , "#Delta R-matched / Segment matched"   ),
    Histogram("Event_nLooseMuonsSegmentMatch"  , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsOuterDRMatch_pt"      , "", False  , default_norm   , 20 , 0     , 300   , 0    , 2   , "loose #mu p_{T} [GeV]"       , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_pt"      , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsOuterDRMatch_eta"     , "", False  , default_norm   , 10 , -3    , 3     , 0    , 2   , "loose #mu #eta"              , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_eta"     , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsOuterDRMatch_dxy"     , "", False  , default_norm   , 10 , -400  , 400   , 0    , 2   , "loose #mu d_{xy} [cm]"       , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_dxy"     , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsOuterDRMatch_dz"      , "", False  , default_norm   , 10 , -400  , 400   , 0    , 2   , "loose #mu d_{z} [cm]"        , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_dz"      , "", False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
]

if plots_from_LLPNanoAOD:
  histograms = histograms + LLPnanoAOD_histograms

weightsBranchName = "genWeight"

color_palette_wong = (
    TColor.GetColor(230, 159, 0),
    TColor.GetColor(86, 180, 233),
    TColor.GetColor(0, 158, 115),
    TColor.GetColor(0, 114, 178),
    TColor.GetColor(213, 94, 0),
)

samples = (
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
  Sample(
    name="tta_mAlp-0p35GeV_ctau-1e0mm",
    file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e0mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kCyan,
    legend_description="0.35 GeV, 1 mm",
  ),
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e1mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e1mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kBlue,
  #   legend_description="0.35 GeV, 1 cm",
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
  #   line_color=ROOT.kMagenta,
  #   legend_description="0.35 GeV, 10 cm",
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
  #   legend_description="0.35 GeV, 1 m",
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
  #   legend_description="0.35 GeV, 100 m",
  # ),
  
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
  # ),
)


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
  
  "QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  "QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8", 
  "QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  "QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  
  "QCD_Pt_120to170_TuneCP5_13TeV_pythia8",
  "QCD_Pt_170to300_TuneCP5_13TeV_pythia8",
  "QCD_Pt_300to470_TuneCP5_13TeV_pythia8",
  "QCD_Pt_470to600_TuneCP5_13TeV_pythia8",
  "QCD_Pt_600to800_TuneCP5_13TeV_pythia8",
  "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8",
  "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8",
  "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8",
  
  "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
  "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
  "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
  
  "tta_mAlp-0p35GeV_ctau-1e0mm",
  "tta_mAlp-0p35GeV_ctau-1e1mm",
  "tta_mAlp-0p35GeV_ctau-1e2mm",
  "tta_mAlp-0p35GeV_ctau-1e3mm",
  "tta_mAlp-0p35GeV_ctau-1e5mm",
  "tta_mAlp-0p35GeV_ctau-1e7mm",
)
