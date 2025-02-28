import ROOT
from Sample import SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from TTAlpsPlotterConfigHelper import TTAlpsPlotterConfigHelper
from ttalps_cross_sections import *
from ttalps_plotting_styles import *

year = "2018"
cross_sections = get_cross_sections(year)

base_path = "/data/dust/user/jniedzie/ttalps_cms/"
# base_path = "/data/dust/user/lrygaard/ttalps_cms/"
# base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps_cms.nosync/data/"

hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons"


skim = "skimmed_looseSemimuonic_v2_ttbarCR"

output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}/"

luminosity = 59830. # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

canvas_size = (800, 600)

show_ratio_plots = True
ratio_limits = (0.5, 1.5)

legend_max_x = 0.83
legend_max_y = 0.89
legend_width = 0.17 if show_ratio_plots else 0.20
legend_height = 0.045 if show_ratio_plots else 0.03

show_cms_labels = True
extraText = "Preliminary"

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

background_uncertainty_style = 3244 # available styles: https://root.cern.ch/doc/master/classTAttFill.html
background_uncertainty_color = ROOT.kBlack
background_uncertainty_alpha = 0.3

plotting_options = {
  SampleType.background: "hist",
  SampleType.signal: "nostack e",
  SampleType.data: "nostack e",
}

default_norm = NormalizationType.to_lumi
# default_norm = NormalizationType.to_background
# default_norm = NormalizationType.to_data
# default_norm = NormalizationType.none

histogramsRatio = []
weightsBranchName = "genWeight"

histograms = (
#           name                                  title logx logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
  Histogram("Event_nTightMuons"                   , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of tight #mu"                            , "# events (2018)"   ),
  Histogram("TightMuons_pt"                       , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-6  , 1e8   , "tight #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # Histogram("TightMuons_leadingPt"                , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e5   , "leading tight #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  # # Histogram("TightMuons_subleadingPt"             , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e4   , "all subleading tight #mu p_{T} [GeV]"           , "# events (2018)"   ),
  Histogram("TightMuons_eta"                      , "", False,  True  , default_norm              , 10 , -3.0  , 5.0   , 1e0   , 1e5   , "tight #mu #eta"                                 , "# events (2018)"   ),
  Histogram("TightMuons_dxy"                      , "", False,  True  , default_norm              , 2  , -0.5  , 0.5   , 1e-2  , 1e10   , "tight #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("TightMuons_dz"                       , "", False,  True  , default_norm              , 2  , -1    , 1     , 1e-2  , 1e8   , "tight #mu d_{z} [cm]"                           , "# events (2018)"   ),
  
  # Histogram("TightMuons_pfRelIso04_all"           , "", False,  True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_pfRelIso03_chg"           , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_pfRelIso03_all"           , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_miniPFRelIso_chg"         , "", False,  True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  # Histogram("TightMuons_miniPFRelIso_all"         , "", False,  True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  # Histogram("TightMuons_jetRelIso"                , "", False,  True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "tight #mu jet Rel Iso"                          , "# events (2018)"   ),
  # Histogram("TightMuons_tkRelIso"                 , "", False,  True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "tight #mu track Rel Iso"                       , "# events (2018)"   ),
  
  # Histogram("Event_nLoosePATMuons"                   , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose #mu"                            , "# events (2018)"   ),
  # Histogram("LoosePATMuons_pt"                       , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # Histogram("LoosePATMuons_leadingPt"                , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "leading loose #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  # # Histogram("LoosePATMuons_subleadingPt"             , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "all subleading loose #mu p_{T} [GeV]"           , "# events (2018)"   ),
  # Histogram("LoosePATMuons_eta"                      , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e6   , "loose #mu #eta"                                 , "# events (2018)"   ),
  # Histogram("LoosePATMuons_dxy"                      , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  # Histogram("LoosePATMuons_dz"                       , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  
  # Histogram("LoosePATMuons_pfRelIso04_all"           , "", False,  True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  # Histogram("LoosePATMuons_pfRelIso03_chg"           , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  # Histogram("LoosePATMuons_pfRelIso03_all"           , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  # Histogram("LoosePATMuons_miniPFRelIso_chg"         , "", False,  True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  # Histogram("LoosePATMuons_miniPFRelIso_all"         , "", False,  True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  # Histogram("LoosePATMuons_jetRelIso"                , "", False,  True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "Loose #mu jet Rel Iso"                          , "# events (2018)"   ),
  # Histogram("LoosePATMuons_tkRelIso"                 , "", False,  True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "Loose #mu track Rel Iso"                       , "# events (2018)"   ),
  
  # Histogram("Event_nLooseDSAMuons"                 , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose dSA #mu"                        , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_pt"                     , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "loose dSA #mu p_{T} [GeV]"                      , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_eta"                    , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e6   , "loose dSA #mu #eta"                             , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_dxy"                    , "", False,  True  , default_norm              , 20 , -10   , 10    , 1e-2  , 1e6   , "loose dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_dz"                     , "", False,  True  , default_norm              , 20 , -10   , 10    , 1e-2  , 1e6   , "loose dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  
  # # Histogram("Event_nLooseElectrons"               , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose electrons"                      , "# events (2018)"   ),
  # # Histogram("LooseElectrons_pt"                   , "", False,  True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "loose electron p_{T} [GeV]"                     , "# events (2018)"   ),
  # # Histogram("LooseElectrons_leadingPt"            , "", False,  True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "leading loose electron p_{T} [GeV]"             , "# events (2018)"   ),
  # # Histogram("LooseElectrons_subleadingPt"         , "", False,  True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "all subleading loose electron p_{T} [GeV]"      , "# events (2018)"   ),
  # # Histogram("LooseElectrons_eta"                  , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e-2  , 1e6   , "loose electron #eta"                            , "# events (2018)"   ),
  # # Histogram("LooseElectrons_dxy"                  , "", False,  True  , default_norm              , 10 , -10   , 10    , 1e-2  , 1e6   , "loose electron d_{xy}"                          , "# events (2018)"   ),
  # # Histogram("LooseElectrons_dz"                   , "", False,  True  , default_norm              , 10 , -10   , 10    , 1e-2  , 1e6   , "loose electron d_{z}"                           , "# events (2018)"   ),
  
  Histogram("Event_nGoodJets"                     , "", False,  True  , default_norm              , 1  , 2     , 16    , 1e-2  , 1e10   , "Number of good jets"                            , "# events (2018)"   ),
  Histogram("GoodJets_pt"                         , "", False,  True  , default_norm              , 10 , 0     , 1300  , 1e-3  , 1e6   , "good jet p_{T} [GeV]"                           , "# events (2018)"   ),
  Histogram("GoodJets_eta"                        , "", False,  True  , default_norm              , 10 , -3    , 5.0   , 1e1   , 1e8   , "good jet #eta"                                  , "# events (2018)"   ),
  Histogram("GoodJets_btagDeepB"                  , "", False,  True  , default_norm              , 10 , 0     , 1.5   , 2e0   , 1e8   , "good jet deepCSV score"                         , "# events (2018)"   ),
  Histogram("GoodJets_btagDeepFlavB"              , "", False,  True  , default_norm              , 10 , 0     , 1.8   , 1e-1  , 1e8   , "good jet deepJet score"                         , "# events (2018)"   ),
  
  Histogram("Event_nGoodMediumBtaggedJets"              , "", False,  True  , default_norm              , 1  , 0     , 20    , 1e0   , 1e9   , "Number of good b-jets"                          , "# events (2018)"   ),
  Histogram("GoodMediumBtaggedJets_pt"                  , "", False,  True  , default_norm              , 50 , 0     , 2000  , 1e-5  , 1e4   , "good b-jet p_{T} [GeV]"                         , "# events (2018)"   ),
  Histogram("GoodMediumBtaggedJets_eta"                 , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e10  , "good b-jet #eta"                                , "# events (2018)"   ),
  Histogram("GoodMediumBtaggedJets_btagDeepB"           , "", False,  True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good b-jet deepCSV score"                           , "# events (2018)"   ),
  Histogram("GoodMediumBtaggedJets_btagDeepFlavB"       , "", False,  True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good b-jet deepJet score"                           , "# events (2018)"   ),
  
  Histogram("Event_MET_pt"                         , "", False,  True  , default_norm              , 10 , 0     , 800   , 1e-8  , 1e9   , "MET p_{T} [GeV]"                                , "# events (2018)"   ),
  Histogram("Event_PV_npvs"                       , "", False,  True  , default_norm              , 1  , 0     , 150   , 1e-3  , 1e12   , "# Primary vertices"                             , "# events (2018)"   ),
  Histogram("Event_PV_npvsGood"                   , "", False,  True  , default_norm              , 1  , 0     , 150   , 1e-3  , 1e6   , "# Good primary vertices"                        , "# events (2018)"   ),
  
  # Histogram("LooseMuons_dimuonMinv"               , "", False,  True  , default_norm              , 1  , 70    , 110   , 1e0   , 1e4   , "loose muons m_{#mu#mu} [GeV]"                   , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonMinvClosestToZ"     , "", False,  True  , default_norm              , 1  , 70    , 110   , 1e0   , 1e4   , "loose muons closest to Z m_{#mu#mu} [GeV]"      , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaRclosestToZ"   , "", False,  True  , default_norm              , 1  , -1    , 6     , 1e0   , 1e3   , "loose muons closest to Z #Delta R_{#mu#mu}"     , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaEtaclosestToZ" , "", False,  True  , default_norm              , 1  , -1    , 6     , 1e-1  , 1e3   , "loose muons closest to Z #Delta #eta_{#mu#mu}"  , "# events (2018)"   ),
  # Histogram("LooseMuons_dimuonDeltaPhiclosestToZ" , "", False,  True  , default_norm              , 1  , -3.5  , 6     , 1e-1  , 1e3   , "loose muons closest to Z #Delta #phi_{#mu#mu}"  , "# events (2018)"   ),
  
  # Histogram("TightMuons_deltaPhiMuonMET"          , "", False,  True  , default_norm              , 20 , -4    , 4     , 1e0   , 1e7   , "tight muon #Delta #phi(MET, #mu)"               , "# events (2018)"   ),
  # Histogram("TightMuons_minvMuonMET"              , "", False,  True  , default_norm              , 40 , 0     , 1000  , 1e-4  , 1e5   , "tight muon m_{MET, l} [GeV]"                    , "# events (2018)"   ),
  # Histogram("GoodJets_minvBjet2jets"              , "", False,  True  , default_norm              , 25 , 0     , 1500  , 1e-1  , 1e5   , "good jets m_{bjj} [GeV]"                        , "# events (2018)"   ),

  Histogram("cutFlow"                             , "", False,  True  , default_norm , 1  , 0     , 12    , 1e1   , 1e15  , "Selection"                                      , "Number of events"  ),
  Histogram("Event_normCheck"                     , "", False,  True  , default_norm , 1  , 0     , 1     , 1e-2  , 1e7   , "norm check"                                     , "# events (2018)"   ),

  Histogram("Event_nLooseDSAMuons"                , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose dSA #mu"                        , "# events (2018)"   ),
  Histogram("LooseDSAMuons_pt"                    , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "loose dSA #mu p_{T} [GeV]"                      , "# events (2018)"   ),
  Histogram("LooseDSAMuons_eta"                   , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e6   , "loose dSA #mu #eta"                             , "# events (2018)"   ),
  Histogram("LooseDSAMuons_dxy"                   , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  Histogram("LooseDSAMuons_dz"                    , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  
  Histogram("Event_nAllLooseMuons"                , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("AllLooseMuons_pt"                    , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("AllLooseMuons_eta"                   , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e6   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("AllLooseMuons_dxy"                   , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("AllLooseMuons_dz"                    , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("AllLooseMuons_deltaR"                , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e-2  , 1e6   , "loose #mu #Delta R"                             , "# events (2018)"   ),
  Histogram("AllLooseMuons_minDeltaR"             , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e-2  , 1e6   , "loose #mu min #Delta R"                         , "# events (2018)"   ),

  Histogram("MuonVertex_vxy"                      , "", False,  True  , default_norm              , 4  , 0     , 120   , 1e0   , 1e6   , "#mu vertex v_{xy} [cm]"                         , "# events (2018)"   ),
  Histogram("MuonVertex_vxySigma"                 , "", False,  True  , default_norm              , 2  , 0     , 100   , 1e-2  , 1e6   , "#mu vertex #sigma_{v_{xy}} [cm]"                , "# events (2018)"   ),
  Histogram("MuonVertex_vz"                       , "", False,  True  , default_norm              , 2  , -250  , 250   , 1e-2  , 1e6   , "#mu vertex v_{z} [cm]"                          , "# events (2018)"   ),
  Histogram("MuonVertex_dR"                       , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e-2  , 1e6   , "#mu vertex #Delta R"                            , "# events (2018)"   ),
  Histogram("MuonVertex_chi2"                     , "", False,  True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "#mu vertex #chi^{2}"                            , "# events (2018)"   ),

  Histogram("DSAMuonVertex_vxy"                   , "", False,  True  , default_norm              , 4  , 0     , 120   , 1e0   , 1e6   , "DSA #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("DSAMuonVertex_vxySigma"              , "", False,  True  , default_norm              , 2  , 0     , 100   , 1e-2  , 1e6   , "DSA #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  Histogram("DSAMuonVertex_vz"                    , "", False,  True  , default_norm              , 2  , -250  , 250   , 1e-2  , 1e6   , "DSA #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  Histogram("DSAMuonVertex_dR"                    , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e-2  , 1e6   , "DSA #mu vertex #Delta R"                        , "# events (2018)"   ),
  Histogram("DSAMuonVertex_chi2"                  , "", False,  True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "DSA #mu vertex #chi^{2}"                        , "# events (2018)"   ),

  Histogram("MuonCombVertex_vxy"                  , "", False,  True  , default_norm              , 4  , 0     , 120   , 1e0   , 1e6   , "standard-DSA #mu vertex v_{xy} [cm]"             , "# events (2018)"   ),
  Histogram("MuonCombVertex_vxySigma"             , "", False,  True  , default_norm              , 2  , 0     , 100   , 1e-2  , 1e6   , "standard-DSA #mu vertex #sigma_{v_{xy}} [cm]"    , "# events (2018)"   ),
  Histogram("MuonCombVertex_vz"                   , "", False,  True  , default_norm              , 2  , -250  , 250   , 1e-2  , 1e6   , "standard-DSA #mu vertex v_{z} [cm]"              , "# events (2018)"   ),
  Histogram("MuonCombVertex_dR"                   , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e-2  , 1e6   , "standard-DSA #mu vertex #Delta R"                , "# events (2018)"   ),
  Histogram("MuonCombVertex_chi2"                 , "", False,  True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "standard-DSA #mu vertex #chi^{2}"                , "# events (2018)"   ),

)
