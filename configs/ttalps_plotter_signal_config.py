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
hist_path = "histograms_muonSFs_new_muonTriggerSFs_new_pileupSFs_new_bTaggingSFs_new"
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_GenInfo"

# skim = ""
# skim = "skimmed_looseSemileptonic"
# skim = "skimmed_SR_Met50GeV"
# skim = "skimmed_looseSemimuonic_GenInfo"
# skim = "skimmed_looseSemimuonic_SRmuonic"
# skim = "skimmed_looseSemimuonic_SRmuonic_DR"
# skim = "skimmed_looseSemimuonic_SRmuonic_OuterDR"
skim = "skimmed_looseSemimuonic_SRmuonic_Segment"

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
# extraText = "Private Work"

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
#           name                                  title logx  logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
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
  # Histogram("Event_PV_npvs"                       , "", False, True  , default_norm              , 1  , 0     , 150   , 1e-3  , 1e12   , "# Primary vertices"                             , "# events (2018)"   ),
  # Histogram("Event_PV_npvsGood"                   , "", False, True  , default_norm              , 1  , 0     , 150   , 1e-3  , 1e6   , "# Good primary vertices"                        , "# events (2018)"   ),
  
  # Histogram("LooseMuons_dimuonMinv"               , "", False, True  , default_norm              , 1  , 70    , 110   , 1e0   , 1e4   , "loose muons m_{#mu#mu} [GeV]"                   , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonMinvClosestToZ"     , "", False, True  , default_norm              , 1  , 70    , 110   , 1e0   , 1e4   , "loose muons closest to Z m_{#mu#mu} [GeV]"      , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaRclosestToZ"   , "", False, True  , default_norm              , 1  , -1    , 6     , 1e0   , 1e3   , "loose muons closest to Z #Delta R_{#mu#mu}"     , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaEtaclosestToZ" , "", False, True  , default_norm              , 1  , -1    , 6     , 1e-1  , 1e3   , "loose muons closest to Z #Delta #eta_{#mu#mu}"  , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaPhiclosestToZ" , "", False, True  , default_norm              , 1  , -3.5  , 6     , 1e-1  , 1e3   , "loose muons closest to Z #Delta #phi_{#mu#mu}"  , "# events (2018)"   ),
  
  # Histogram("TightMuons_deltaPhiMuonMET"          , "", False, True  , default_norm              , 20 , -4    , 4     , 1e0   , 1e7   , "tight muon #Delta #phi(MET, #mu)"               , "# events (2018)"   ),
  # Histogram("TightMuons_minvMuonMET"              , "", False, True  , default_norm              , 40 , 0     , 1000  , 1e-4  , 1e5   , "tight muon m_{MET, l} [GeV]"                    , "# events (2018)"   ),
  # Histogram("GoodJets_minvBjet2jets"              , "", False, True  , default_norm              , 25 , 0     , 1500  , 1e-1  , 1e5   , "good jets m_{bjj} [GeV]"                        , "# events (2018)"   ),

  Histogram("Event_nMuon"                         , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of #mu"                            , "# events (2018)"   ),
  Histogram("Muon_pt"                             , "", False, True  , default_norm              , 50 , 0     , 1000  , 1e-6  , 1e10   , "#mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("Muon_eta"                            , "", False, True  , default_norm              , 10 , -3.0  , 5.0   , 1e0   , 1e8   , "#mu #eta"                                 , "# events (2018)"   ),
  Histogram("Muon_dxy"                            , "", False, True  , default_norm              , 2  , -0.5  , 0.5   , 1e-1  , 1e10   , "#mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("Muon_dz"                             , "", False, True  , default_norm              , 2  , -1    , 1     , 1e-1  , 1e10   , "#mu d_{z} [cm]"                           , "# events (2018)"   ),

  Histogram("cutFlow"                             , "", False, True  , default_norm , 1  , 0     , 14     , 1e-1   , 1e13  , "Selection"                                      , "Number of events"  ),
  Histogram("Event_normCheck"                     , "", False, True  , default_norm , 1  , 0     , 1     , 1e-1  , 1e7   , "norm check"                                     , "# events (2018)"   ),
)

LLPnanoAOD_histograms = (
#           name                                  title logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
  
  Histogram("Muon_idx"                            , "", False, True  , default_norm              , 1 , 0     , 15  , 1e-6  , 1e10   , "#mu index"                                , "# events (2018)"   ),
  Histogram("Muon_outerEta"                       , "", False, True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "#mu outer #eta"                           , "# events (2018)"   ),
  Histogram("Muon_outerPhi"                       , "", False, True  , default_norm              , 1  , -3.0  , 3.0   , 1e0   , 1e8   , "#mu #phi"                                 , "# events (2018)"   ),
  Histogram("Muon_dsaMatch1"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 1"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch2"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 2"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch3"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 3"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch4"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 4"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch5"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e10  , "Number of matches to DSA #mu 5"           , "# events (2018)"   ),
  Histogram("Muon_dsaMatch1idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 1"                       , "# events (2018)"   ),
  Histogram("Muon_dsaMatch2idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 2"                       , "# events (2018)"   ),
  Histogram("Muon_dsaMatch3idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 3"                       , "# events (2018)"   ),
  Histogram("Muon_dsaMatch4idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 4"                       , "# events (2018)"   ),
  Histogram("Muon_dsaMatch5idx"                   , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e10  , "Index of DSA #mu 5"                       , "# events (2018)"   ),

  # Histogram("Event_nDSAMuon"                      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e9*y_scale   , "Number of dSA #mu"        , "# events (2018)"   ),
  # Histogram("DSAMuon_idx"                         , "", False, True  , default_norm              , 1 , 0     , 15  , 1e-6  , 1e10   , "dSa #mu index"                                , "# events (2018)"   ),
  # Histogram("DSAMuon_pt"                          , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "dSA #mu p_{T} [GeV]"                      , "# events (2018)"   ),
  # Histogram("DSAMuon_eta"                         , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "dSA #mu #eta"                             , "# events (2018)"   ),
  # Histogram("DSAMuon_dxy"                         , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("DSAMuon_dz"                          , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  # Histogram("DSAMuon_dzPV"                        , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  # # Histogram("DSAMuon_dxyPV"                         , "", False, True  , default_norm              , 50  , -800  , 800   , 1e-1  , 1e8   , "dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
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
  
  Histogram("Event_nLooseMuonsDRMatch"            , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_pt"                , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_eta"               , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_dxy"               , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_dz"                , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_hasOuterDRMatch"   , "", False, True  , default_norm              , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with outer #Delta R"            , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_hasSegmentMatch"   , "", False, True  , default_norm              , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with segments/hits"             , "# events (2018)"   ),
  # Histogram("LooseMuonsDRMatch_genMuonDR"         , "", False, True  , default_norm              , 1  , 0     , 6     , 1e-1  , 1e8   , "#Delta R to gen-level #mu from ALP"             , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsOuterDRMatch"       , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_pt"           , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_eta"          , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_dxy"          , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_dz"           , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_hasDRMatch"   , "", False, True  , default_norm              , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with #Delta R"                  , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_hasSegmentMatch"   , "", False, True  , default_norm         , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with segments/hits"             , "# events (2018)"   ),
  # Histogram("LooseMuonsOuterDRMatch_genMuonDR"    , "", False, True  , default_norm              , 1  , 0     , 6     , 1e-1  , 1e8   , "#Delta R to gen-level #mu from ALP"             , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsSegmentMatch"       , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_pt"           , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_eta"          , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_dxy"          , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_dz"           , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_hasDRMatch"   , "", False, True  , default_norm              , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with #Delta R"                  , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_hasOuterDRMatch"   , "", False, True  , default_norm         , 1  , 0     , 3     , 1e-1  , 1e8   , "is also matched with outer #Delta R"            , "# events (2018)"   ),
  # Histogram("LooseMuonsSegmentMatch_genMuonDR"    , "", False, True  , default_norm              , 1  , 0     , 6     , 1e-1  , 1e8   , "#Delta R to gen-level #mu from ALP"             , "# events (2018)"   ),

  # Histogram("Event_nPatMuonVertex"                , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of Pat-Pat #mu vertices"                 , "# events (2018)"   ),
  # Histogram("PatMuonVertex_vxy"                   , "", False, True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  # Histogram("PatMuonVertex_vxySigma"              , "", False, True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  # Histogram("PatMuonVertex_vz"                    , "", False, True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  # Histogram("PatMuonVertex_dR"                    , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat #mu vertex #Delta R"                        , "# events (2018)"   ),
  # Histogram("PatMuonVertex_chi2"                  , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  # Histogram("PatMuonVertex_idx1"                  , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("PatMuonVertex_idx2"                  , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("PatMuonVertex_isDSAMuon1"            , "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("PatMuonVertex_isDSAMuon2"            , "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("Event_nPatDSAMuonVertex"             , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of Pat-DSA #mu vertices"                 , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_vxy"                , "", False, True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat-DSA #mu vertex v_{xy} [cm]"                 , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_vxySigma"           , "", False, True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat-DSA #mu vertex #sigma_{v_{xy}} [cm]"        , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_vz"                 , "", False, True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat-DSA #mu vertex v_{z} [cm]"                  , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_dR"                 , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat-DSA #mu vertex #Delta R"                    , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_chi2"               , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat-DSA #mu vertex #chi^{2}"                    , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_idx1"               , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_idx2"               , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_isDSAMuon1"         , "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("PatDSAMuonVertex_isDSAMuon2"         , "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("Event_nDSAMuonVertex"                , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of DSA-DSA #mu vertices"                 , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_vxy"                   , "", False, True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "DSA #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_vxySigma"              , "", False, True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "DSA #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_vz"                    , "", False, True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "DSA #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_dR"                    , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "DSA #mu vertex #Delta R"                        , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_chi2"                  , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "DSA #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_idx1"                  , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_idx2"                  , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_isDSAMuon1"            , "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("DSAMuonVertex_isDSAMuon2"            , "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  

  # Histogram("Event_nLooseMuonsVertexDRMatch"         , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of Pat-Pat #mu vertices"                 , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_vxy"            , "", False, True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_vxySigma"       , "", False, True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_vz"             , "", False, True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_dR"             , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat #mu vertex #Delta R"                        , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_chi2"           , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_idx1"           , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_idx2"           , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_isDSAMuon1"     , "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_isDSAMuon2"     , "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_displacedTrackIso04Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_displacedTrackIso04Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_displacedTrackIso03Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso03"                , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_displacedTrackIso04Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso04"                , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_displacedTrackIso03Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso03"                , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexDRMatch_displacedTrackIso04Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso04"                , "# events (2018)"   ),
  # Histogram("Event_nLooseMuonsVertexOuterDRMatch"    , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of Pat-Pat #mu vertices"                 , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_vxy"       , "", False, True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_vxySigma"  , "", False, True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_vz"        , "", False, True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_dR"        , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat #mu vertex #Delta R"                        , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_chi2"      , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_idx1"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_idx2"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_isDSAMuon1", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_isDSAMuon2", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_displacedTrackIso04Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_displacedTrackIso04Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_displacedTrackIso03Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso03"                , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_displacedTrackIso04Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso04"                , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_displacedTrackIso03Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso03"                , "# events (2018)"   ),
  # Histogram("LooseMuonsVertexOuterDRMatch_displacedTrackIso04Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsVertexSegmentMatch"    , "", False, True  , default_norm              , 1  , 0     , 20    , 1e1   , 1e6   , "Number of #mu vertices"                 , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_vxy"       , "", False, True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "#mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_vxySigma"  , "", False, True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "#mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_vz"        , "", False, True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "#mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_dR"        , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "#mu vertex #Delta R"                        , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_chi2"      , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "#mu vertex #chi^{2}"                        , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_idx1"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_idx2"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-1  , 1e8   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_isDSAMuon1", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_isDSAMuon2", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-1  , 1e7   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_displacedTrackIso04Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_displacedTrackIso04Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat dimuon #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_displacedTrackIso03Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_displacedTrackIso04Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{1} displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_displacedTrackIso03Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsVertexSegmentMatch_displacedTrackIso04Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Pat #mu_{2} displacedTrackIso04"                , "# events (2018)"   ),

  Histogram("Event_nGenMuonFromALP"               , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen #mu from ALP"                     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vx"                   , "", False, True  , default_norm              , 100, -1000 , 1000  , 1e-2   , 1e6   , "Gen #mu v_{x} [cm]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vy"                   , "", False, True  , default_norm              , 100, -1000 , 1000  , 1e-2   , 1e6   , "Gen #mu v_{y} [cm]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vz"                   , "", False, True  , default_norm              , 100, -1000 , 1000  , 1e-2   , 1e6   , "Gen #mu v_{z} [cm]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxy"                  , "", False, True  , default_norm              , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen #mu v_{xy} [cm]"                            , "# events (2018)"   ),
  # Histogram("GenMuonFromALP_vxyz"                 , "", False, True  , default_norm              , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen #mu v_{xyz} [cm]"                           , "# events (2018)"   ),
  Histogram("GenMuonFromALP_dxy"                  , "", False, True  , default_norm              , 200, -1000 , 1000  , 1e-2   , 1e4   , "Gen #mu d_{xy} [cm]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxyALPboostpT"        , "", False, True  , default_norm              , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen proper #mu v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxyALPboostT"         , "", False, True  , default_norm              , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen proper #mu v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("GenMuonFromALP_vxyzALPboostp"        , "", False, True  , default_norm              , 200, 0     , 1000  , 1e-2   , 1e4   , "Gen proper #mu v_{xyz} [cm]"                    , "# events (2018)"   ),
  Histogram("GenMuonFromALP_pt"                   , "", False, True  , default_norm              , 5  , 0     , 100   , 1e-2   , 1e6   , "Gen #mu p_{T} [GeV]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_boost"                , "", False, True  , default_norm              , 1  , 0     , 500   , 1e-2   , 1e6   , "Gen #mu boost [GeV]"                            , "# events (2018)"   ),
  Histogram("GenMuonFromALP_mass"                 , "", False, True  , default_norm              , 1  , 0     , 1     , 1e-2   , 1e6   , "Gen #mu mass [GeV]"                             , "# events (2018)"   ),
  Histogram("GenMuonFromALP_looseMuonsDRMatchMinDR", "", False, True  , default_norm             , 1  , 0     , 5     , 1e-2   , 1e6   , "#Delta R(Gen #mu, loose #mu)"                   , "# events (2018)"   ),
  Histogram("GenMuonFromALP_looseMuonsOuterDRMatchMinDR", "", False, True  , default_norm        , 1  , 0     , 5     , 1e-2   , 1e6   , "#Delta R(Gen #mu, loose #mu)"                   , "# events (2018)"   ),
  Histogram("GenMuonFromALP_looseMuonsSegmentMatchMinDR", "", False, True  , default_norm        , 1  , 0     , 5     , 1e-2   , 1e6   , "#Delta R(Gen #mu, loose #mu)"                   , "# events (2018)"   ),
  Histogram("Event_nGenDimuonFromALP"             , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen di-muons from ALP"                , "# events (2018)"   ),
  Histogram("GenDimuonFromALP_invMass"            , "", False, True  , default_norm              , 1  , 0     , 0.5   , 1e-1  , 1e8   , "Gen m_{#mu #mu} [GeV]"                          , "# events (2018)"   ),
  Histogram("GenDimuonFromALP_DR"                 , "", False, True  , default_norm              , 1  , 0     , 5     , 1e-1  , 1e8   , "Gen #Delta R(#mu #mu)"                          , "# events (2018)"   ),
  Histogram("GenDimuonFromALP_Dphi"               , "", False, True  , default_norm              , 1  , -3    , 3     , 1e-1  , 1e8   , "Gen #Delta #Phi (#mu #mu)"                          , "# events (2018)"   ),
  Histogram("Event_nGenALP"                       , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of gen ALP"                     , "# events (2018)"   ),
  Histogram("GenALP_vx"                           , "", False, True  , default_norm              , 50 , -1000 , 1000  , 1e-1   , 1e6   , "Gen ALP v_{x} [cm]"                             , "# events (2018)"   ),
  Histogram("GenALP_vy"                           , "", False, True  , default_norm              , 50 , -1000 , 1000  , 1e-1   , 1e6   , "Gen ALP v_{y} [cm]"                             , "# events (2018)"   ),
  Histogram("GenALP_vz"                           , "", False, True  , default_norm              , 50 , -1000 , 1000  , 1e-1   , 1e6   , "Gen ALP v_{z} [cm]"                             , "# events (2018)"   ),
  Histogram("GenALP_vxy"                          , "", False, True  , default_norm              , 50 , 0     , 1000  , 1e-1   , 1e6   , "Gen ALP v_{xy} [cm]"                            , "# events (2018)"   ),
  Histogram("GenALP_pt"                           , "", False, True  , default_norm              , 1  , 0     , 500   , 1e-1  , 1e8   , "Gen ALP p_{T} [GeV]"                            , "# events (2018)"   ),
  # Histogram("GenALP_boost"                        , "", False, True  , default_norm              , 1  , 0     , 500   , 1e-1  , 1e8   , "Gen ALP boost [GeV]"                            , "# events (2018)"   ),
  Histogram("GenALP_mass"                         , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Gen ALP mass [GeV]"                             , "# events (2018)"   ),

  # Histogram("Event_nLooseMuonsFromALPDRMatch"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP"                , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPDRMatch_pt"          , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "Loose muons #mu ALP p_{T} [GeV]"              , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPDRMatch_eta"         , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "Loose muons #mu ALP #eta"                     , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPDRMatch_dxy"         , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{xy} [cm]"              , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPDRMatch_dz"          , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{z} [cm]"               , "# events (2018)"   ),
  # Histogram("Event_nLooseMuonsFromALPOuterDRMatch" , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP"                , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPOuterDRMatch_pt"     , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "Loose muons #mu ALP p_{T} [GeV]"              , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPOuterDRMatch_eta"    , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "Loose muons #mu ALP #eta"                     , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPOuterDRMatch_dxy"    , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{xy} [cm]"              , "# events (2018)"   ),
  # Histogram("LooseMuonsFromALPOuterDRMatch_dz"     , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{z} [cm]"               , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsFromALPSegmentMatch0p2" , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p2_pt"     , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "Loose muons #mu ALP p_{T} [GeV]"              , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p2_eta"    , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "Loose muons #mu ALP #eta"                     , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p2_dxy"    , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{xy} [cm]"              , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p2_dz"     , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{z} [cm]"               , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsFromALPSegmentMatch0p5" , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p5_pt"     , "", False, True  , default_norm              , 20 , 0     , 300   , 1e-1  , 1e8   , "Loose muons #mu ALP p_{T} [GeV]"              , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p5_eta"    , "", False, True  , default_norm              , 10 , -3    , 3     , 1e0*y_scale   , 1e8*y_scale   , "Loose muons #mu ALP #eta"                     , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p5_dxy"    , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{xy} [cm]"              , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPSegmentMatch0p5_dz"     , "", False, True  , default_norm              , 20 , -200  , 200   , 1e-1  , 1e8   , "Loose muons #mu ALP d_{z} [cm]"               , "# events (2018)"   ),

 Histogram("Event_nLooseMuonsFromALPVertexSegmentMatch0p2"    , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP vertices"                 , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_vxy"       , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-2*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_vxySigma"  , "", False, True  , default_norm              , 2  , 0     , 100   , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_vz"        , "", False, True  , default_norm              , 20 , -800  , 800   , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex v_{z} [cm]"                      , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_dR"        , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #Delta R"                        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_chi2"      , "", False, True  , default_norm              , 1  , 0     , 20    , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #chi^{2}"                        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_idx1"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_idx2"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_isDSAMuon1", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_isDSAMuon2", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_displacedTrackIso04Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_displacedTrackIso04Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_displacedTrackIso03Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_displacedTrackIso04Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_displacedTrackIso03Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p2_displacedTrackIso04Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsFromALPVertexSegmentMatch0p5"    , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of loose #mu from ALP vertices"                 , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_vxy"       , "", False, True  , default_norm              , 10 , 0     , 500   , 1e-2*y_scale   , 1e6*y_scale   , "Loose #mu from ALP vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_vxySigma"  , "", False, True  , default_norm              , 2  , 0     , 100   , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_vz"        , "", False, True  , default_norm              , 20 , -800  , 800   , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex v_{z} [cm]"                      , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_dR"        , "", False, True  , default_norm              , 1  , 0     , 10    , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #Delta R"                        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_chi2"      , "", False, True  , default_norm              , 1  , 0     , 20    , 1e-2*y_scale  , 1e6*y_scale   , "Loose #mu from ALP vertex #chi^{2}"                        , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_idx1"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_idx2"      , "", False, True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} vertex index"                           , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_isDSAMuon1", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{1} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_isDSAMuon2", "", False, True  , default_norm              , 1  , 0     , 2     , 1e-2*y_scale  , 1e6*y_scale   , "#mu_{2} == DSAMuon"                             , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_displacedTrackIso03Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_displacedTrackIso04Dimuon1"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{1} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_displacedTrackIso03Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso03"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_displacedTrackIso04Dimuon2"  , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose dimuon from ALP #mu_{2} displacedTrackIso04"         , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_displacedTrackIso03Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_displacedTrackIso04Muon1"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{1} from ALP displacedTrackIso04"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_displacedTrackIso03Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso03"                , "# events (2018)"   ),
  Histogram("LooseMuonsFromALPVertexSegmentMatch0p5_displacedTrackIso04Muon2"    , "", False, True  , default_norm        , 1  , 0     , 10    , 1e-1  , 1e7   , "Loose #mu_{2} from ALP displacedTrackIso04"                , "# events (2018)"   ),
)

histogramsRatio = [
  # ( Histogram("Event_nLooseMuonsDRMatch"       , "", False, False  , default_norm   , 1  , 0     , 15    , 0    , 2   , "Number of loose #mu"         , "#Delta R-matched / Segment matched"   ),
  #   Histogram("Event_nLooseMuonsSegmentMatch"  , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  # ( Histogram("LooseMuonsDRMatch_pt"           , "", False, False  , default_norm   , 20 , 0     , 300   , 0    , 2   , "loose #mu p_{T} [GeV]"       , "#Delta R-matched / Segment matched"   ),
  #   Histogram("LooseMuonsSegmentMatch_pt"      , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  # ( Histogram("LooseMuonsDRMatch_eta"          , "", False, False  , default_norm   , 10  , -3   , 3     , 0    , 2   , "loose #mu #eta"              , "#Delta R-matched / Segment matched"   ),
  #   Histogram("LooseMuonsSegmentMatch_eta"     , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  # ( Histogram("LooseMuonsDRMatch_dxy"          , "", False, False  , default_norm   , 20 , -200  , 200   , 0    , 2   , "loose #mu d_{xy} [cm]"       , "#Delta R-matched / Segment matched"   ),
  #   Histogram("LooseMuonsSegmentMatch_dxy"     , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  # ( Histogram("LooseMuonsDRMatch_dz"           , "", False, False  , default_norm   , 20 , -200  , 200   , 0    , 2   , "loose #mu d_{z} [cm]"        , "#Delta R-matched / Segment matched"   ),
  #   Histogram("LooseMuonsSegmentMatch_dz"      , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  
  # ( Histogram("Event_nLooseMuonsOuterDRMatch"  , "", False, False  , default_norm   , 1  , 0     , 15    , 0    , 2   , "Number of loose #mu"         , "#Delta R-matched / Segment matched"   ),
  #   Histogram("Event_nLooseMuonsSegmentMatch"  , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  # ( Histogram("LooseMuonsOuterDRMatch_pt"      , "", False, False  , default_norm   , 20 , 0     , 300   , 0    , 2   , "loose #mu p_{T} [GeV]"       , "#Delta R-matched / Segment matched"   ),
  #   Histogram("LooseMuonsSegmentMatch_pt"      , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  # ( Histogram("LooseMuonsOuterDRMatch_eta"     , "", False, False  , default_norm   , 10 , -3    , 3     , 0    , 2   , "loose #mu #eta"              , "#Delta R-matched / Segment matched"   ),
  #   Histogram("LooseMuonsSegmentMatch_eta"     , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  # ( Histogram("LooseMuonsOuterDRMatch_dxy"     , "", False, False  , default_norm   , 20 , -200  , 200   , 0    , 2   , "loose #mu d_{xy} [cm]"       , "#Delta R-matched / Segment matched"   ),
  #   Histogram("LooseMuonsSegmentMatch_dxy"     , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  # ( Histogram("LooseMuonsOuterDRMatch_dz"      , "", False, False  , default_norm   , 20 , -200  , 200   , 0    , 2   , "loose #mu d_{z} [cm]"        , "#Delta R-matched / Segment matched"   ),
  #   Histogram("LooseMuonsSegmentMatch_dz"      , "", False, False  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
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
  Sample(
    name="tta_mAlp-0p35GeV_ctau-1e1mm",
    file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e1mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kBlue,
    legend_description="0.35 GeV, 1 cm",
  ),
  Sample(
    name="tta_mAlp-0p35GeV_ctau-1e2mm",
    file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e2mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kMagenta,
    legend_description="0.35 GeV, 10 cm",
  ),
  Sample(
    name="tta_mAlp-0p35GeV_ctau-1e3mm",
    file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e3mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kGreen+1,
    legend_description="0.35 GeV, 1 m",
  ),
  Sample(
    name="tta_mAlp-0p35GeV_ctau-1e5mm",
    file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e5mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kOrange,
    legend_description="0.35 GeV, 100 m",
  ),
  
  # Backgrounds
  # Sample(
  #   name="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
  #   file_path=f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.background,
  #   cross_sections=cross_sections,
  #   line_alpha=0,
  #   fill_color=ROOT.kRed+1,
  #   fill_alpha=1.0,
  #   marker_size=0,
  #   legend_description="tt (semi-leptonic)",
  # ),
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
