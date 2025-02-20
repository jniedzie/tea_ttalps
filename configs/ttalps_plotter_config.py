import ROOT
from ROOT import TColor
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from ttalps_cross_sections import *
from ttalps_samples_list import backgrounds2018, signals2018, data2018

year = "2018"
cross_sections = get_cross_sections(year)

base_path = "/data/dust/user/jniedzie/ttalps_cms/"
# base_path = "/Users/jeremi/Documents/Physics/DESY/ttalps_cms.nosync/data/"
# base_path = "/data/dust/user/lrygaard/ttalps_cms/"

# hist_path = "histograms"
# hist_path = "histograms_pileup"
# hist_path = "histograms_pileupSFs"
# hist_path = "histograms_pileupSFs_bTaggingSFs"
# hist_path = "histograms_muonSFs_pileupSFs_bTaggingSFs"
# hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons"

# skim = ""
# skim = "skimmed_looseSemileptonic"
# skim = "skimmed_signalLike"
# skim = "skimmed_ttbarLike"

# skim = "skimmed_ttbarSemimuonicCR_tightMuon"
# skim = "skimmed_ttbarSemimuonicCR_tightMuon_newBtag"
# skim = "skimmed_ttbarSemimuonicCR"
# skim = "skimmed_ttbarSemimuonicCR_Met30GeV"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_2mediumBjets"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_2tightBjets"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso"
# skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso_goldenJson"

skim = "skimmed_looseSemimuonic_ttbarCR"

# skim = "skimmed_ttZLike"
# skim = "skimmed_ttZSemimuonicCR_tightMuon_noLooseMuonIso"
# skim = "skimmed_ttZSemimuonicCR_Met50GeV"

# skim = "skimmed_SR_Met50GeV"

output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}/"

# luminosity = 63670. # pb^-1
luminosity = 59830. # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

canvas_size = (800, 600)
show_ratio_plots = True
ratio_limits = (0.5, 1.5)

legend_width = 0.17 if show_ratio_plots else 0.20
legend_min_x = 0.45
legend_max_x = 0.83

legend_height = 0.045 if show_ratio_plots else 0.03
legend_max_y = 0.89

n_default_backgrounds = 10

show_cms_labels = True
extraText = "Preliminary"

legends = {
  SampleType.signal: Legend(legend_max_x-3*legend_width, legend_max_y-2*legend_height, legend_max_x-2*legend_width, legend_max_y-legend_height, "l"),
  SampleType.background: Legend(legend_max_x-legend_width, legend_max_y-n_default_backgrounds*legend_height, legend_max_x, legend_max_y, "f"),
  SampleType.data: Legend(legend_max_x-3*(legend_width), legend_max_y-legend_height, legend_max_x-2*(legend_width), legend_max_y, "pl"),
}



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

plots_from_LLPNanoAOD = False

if plots_from_LLPNanoAOD:
  default_norm = NormalizationType.to_background

histograms = (
#           name                                  title logx logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
  # Histogram("Event_nTightMuons"                   , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of tight #mu"                            , "# events (2018)"   ),
  # Histogram("TightMuons_pt"                       , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-6  , 1e8   , "tight #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # # Histogram("TightMuons_leadingPt"                , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e5   , "leading tight #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  # # # Histogram("TightMuons_subleadingPt"             , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e4   , "all subleading tight #mu p_{T} [GeV]"           , "# events (2018)"   ),
  # Histogram("TightMuons_eta"                      , "", False,  True  , default_norm              , 10 , -3.0  , 5.0   , 1e0   , 1e5   , "tight #mu #eta"                                 , "# events (2018)"   ),
  # Histogram("TightMuons_dxy"                      , "", False,  True  , default_norm              , 2  , -0.5  , 0.5   , 1e-2  , 1e10   , "tight #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  # Histogram("TightMuons_dz"                       , "", False,  True  , default_norm              , 2  , -1    , 1     , 1e-2  , 1e8   , "tight #mu d_{z} [cm]"                           , "# events (2018)"   ),
  
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
  Histogram("GoodJets_pt"                         , "", False,  True  , default_norm              , 1 , 0     , 1300  , 1e-3  , 1e6   , "good jet p_{T} [GeV]"                           , "# events (2018)"   ),
  Histogram("GoodJets_eta"                        , "", False,  True  , default_norm              , 10 , -3    , 5.0   , 1e1   , 1e6   , "good jet #eta"                                  , "# events (2018)"   ),
  Histogram("GoodJets_btagDeepB"                  , "", False,  True  , default_norm              , 10 , 0     , 1.5   , 2e0   , 1e6   , "good jet deepCSV score"                         , "# events (2018)"   ),
  Histogram("GoodJets_btagDeepFlavB"              , "", False,  True  , default_norm              , 10 , 0     , 1.8   , 1e-1   , 1e8   , "good jet deepJet score"                         , "# events (2018)"   ),
  
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
)

LLP_histograms = (
#           name                                  title logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
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

histogramsRatio = (
)

if plots_from_LLPNanoAOD:
  histograms = histograms + LLP_histograms

weightsBranchName = "genWeight"

color_palette_wong = (
    TColor.GetColor(230, 159, 0),
    TColor.GetColor(86, 180, 233),
    TColor.GetColor(0, 158, 115),
    TColor.GetColor(0, 114, 178),
    TColor.GetColor(213, 94, 0),
)

samples = [
  # Data
  Sample(
    name="SingleMuon",
    file_path=f"{base_path}/collision_data2018/SingleMuon2018_{skim}_{hist_path}.root",
    type=SampleType.data,
    cross_sections=cross_sections,
    line_alpha=1,
    fill_alpha=0,
    marker_size=0.7,
    marker_style=20,
    marker_color=ROOT.kBlack,
    legend_description="SingleMuon2018",
  ),
  
  # Signal
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e2mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e2mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=2,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kGreen+1,
  #   legend_description="0.35 GeV, 1e2 mm",
  # ),
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e3mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e3mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=2,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kBlue,
  #   legend_description="0.35 GeV, 1e3 mm",
  # ),
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e5mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e5mm/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=2,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kMagenta,
  #   legend_description="0.35 GeV, 1e5 mm",
  # ),
]

def get_legend(column, row):
  legend = Legend(
    legend_max_x-(column+1)*legend_width, 
    legend_max_y-(row+1)*legend_height, 
    legend_max_x-(column)*legend_width, 
    legend_max_y-(row)*legend_height, "f")
  
  return legend


backgrounds_to_exclude = [
  "QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  "QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
]

for background_name in backgrounds2018:
  short_name = background_name.split("/")[-1]
  
  exclude_background = False
  for background_to_exclude in backgrounds_to_exclude:
    if short_name in background_to_exclude:
      exclude_background = True
      break
  
  if exclude_background:
    continue
  
  
  
  
  long_name = None
  
  for sample_name in cross_sections.keys():
    if short_name in sample_name:
      long_name = sample_name
      break
  
  if not long_name:
    print(f"Error: Could not find long name for {short_name}")
    continue
  
  color = None
  custom_legend = Legend(0, 0, 0, 0, "")
  legend_description = " "
  
  
  if "TTToSemiLeptonic" in long_name:
    color = ROOT.kRed+1
    custom_legend = get_legend(column=1, row=0)
    legend_description = "tt (semi-leptonic)"
  elif "TTToHadronic" in long_name:
    color = ROOT.kRed+3
    custom_legend = get_legend(column=1, row=1)
    legend_description = "tt (hadronic)"
  elif "TTTo2L2Nu" in long_name:
    color = ROOT.kRed+4
    custom_legend = get_legend(column=1, row=2)
    legend_description = "tt (leptonic)"
  
  elif "QCD" in long_name:
    color = color_palette_wong[0]  
    if "120To170" in long_name:
      custom_legend = get_legend(column=1, row=3)
      legend_description = "QCD (#mu enriched)"
  
  elif "WJets" in long_name:
    color = ROOT.kViolet+1
    custom_legend = get_legend(column=1, row=4)
    legend_description = "W+jets"
  
  elif "ST_t" in long_name:
    color = color_palette_wong[1]
    if "antitop" in long_name:
      custom_legend = get_legend(column=1, row=5)
      legend_description = "Single top (tW)"
  
  elif "ttH" in long_name:
    color = color_palette_wong[4]
    if "ttHTobb" in long_name:
      custom_legend = get_legend(column=1, row=6)
      legend_description = "ttH"
  
  elif "TTZToLL" in long_name:
    color = ROOT.kYellow+3
    if "NuNu" in long_name:
      custom_legend = get_legend(column=0, row=0)
      legend_description = "ttZ"
  elif "TTZZ" in long_name:
    color = ROOT.kGray+1
    custom_legend = get_legend(column=0, row=1)
    legend_description = "ttZZ"
  elif "TTZH" in long_name:
    color = ROOT.kGray+2
    custom_legend = get_legend(column=0, row=2)
    legend_description = "ttZH"
  elif "TTTT" in long_name:
    color = ROOT.kGray+3
    custom_legend = get_legend(column=0, row=3)
    legend_description = "TTTT"
  elif "DYJets" in long_name:
    color = ROOT.kMagenta+1
    if "M-10to50" in long_name:
      custom_legend = get_legend(column=0, row=4)
      legend_description = "DY+jets"
  else:
    print(f"Error: Could not determine color for {long_name}")
    continue
    
  samples.append(
    Sample(
      name=long_name,
      file_path=f"{base_path}/{background_name}/{skim}/{hist_path}/histograms.root",
      type=SampleType.background,
      cross_sections=cross_sections,
      line_alpha=0,
      fill_color=color,
      fill_alpha=0.7,
      marker_size=0,
      legend_description=legend_description,
      custom_legend=custom_legend,
    )
  )


custom_stacks_order = (
  "SingleMuon",
  
  "DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
  "DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
  
  "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
  "TTZH_TuneCP5_13TeV-madgraph-pythia8",
  "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",

  "ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8",
  "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
  "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
  
  "ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8",
  "ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8",
  "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",

  "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
  "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
  "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
  "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
  
  "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
  "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
  
  "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
  "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
  
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
  
  "QCD_Pt_120to170_TuneCP5_13TeV_pythia8",
  "QCD_Pt_170to300_TuneCP5_13TeV_pythia8",
  "QCD_Pt_300to470_TuneCP5_13TeV_pythia8",
  "QCD_Pt_470to600_TuneCP5_13TeV_pythia8",
  "QCD_Pt_600to800_TuneCP5_13TeV_pythia8",
  "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8",
  "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8",
  "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8",
  
  "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
  
  "tta_mAlp-0p35GeV_ctau-1e0mm",
  "tta_mAlp-0p35GeV_ctau-1e1mm",
  "tta_mAlp-0p35GeV_ctau-1e2mm",
  "tta_mAlp-0p35GeV_ctau-1e3mm",
  "tta_mAlp-0p35GeV_ctau-1e5mm",
)