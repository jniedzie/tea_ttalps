import ROOT
from ROOT import TColor
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from ttalps_cross_sections import *

base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms/"

hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"

skim = "skimmed_looseSemimuonic_redo"
# skim = "skimmed_looseSemimuonic_GenInfo"
# skim = "skimmed_looseSemimuonic_SRmuonic"
# skim = "skimmed_looseSemimuonic_SRmuonic_DR"
# skim = "skimmed_looseSemimuonic_SRmuonic_OuterDR"
# skim = "skimmed_looseSemimuonic_SRmuonic_Segment"

output_path = f"../plots/LLPtest_{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}/"

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
  Histogram("Event_nMuon"                         , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of #mu"                            , "# events (2018)"   ),
  Histogram("Muon_pt"                             , "", True  , default_norm              , 5 , 0     , 1000  , 1e-6  , 1e10   , "#mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("Muon_eta"                            , "", True  , default_norm              , 1 , -3.0  , 5.0   , 1e0   , 1e8   , "#mu #eta"                                 , "# events (2018)"   ),
  Histogram("Muon_dxy"                            , "", True  , default_norm              , 2  , -0.5  , 0.5   , 1e-1  , 1e10   , "#mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("Muon_dz"                             , "", True  , default_norm              , 2  , -1    , 1     , 1e-1  , 1e10   , "#mu d_{z} [cm]"                           , "# events (2018)"   ),

  Histogram("cutFlow"                             , "", True  , default_norm , 1  , 0     , 14     , 1e-1   , 1e13  , "Selection"                                      , "Number of events"  ),
  Histogram("Event_normCheck"                     , "", True  , default_norm , 1  , 0     , 1     , 1e-1  , 1e7   , "norm check"                                     , "# events (2018)"   ),
)

LLPnanoAOD_histograms = (
#           name                                  title logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
  
  Histogram("Muon_idx"                            , "", True  , default_norm              , 1 , 0     , 15  , 1e-6  , 1e10   , "#mu index"                                , "# events (2018)"   ),
  Histogram("Muon_pt"                             , "", True  , default_norm              , 5 , 0     , 1000  , 1e-6  , 1e10   , "#mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("Muon_eta"                            , "", True  , default_norm              , 1  , -3.0  , 3.0   , 1e2*y_scale   , 1e5*y_scale   , "#mu #eta"                                 , "# events (2018)"   ),
  Histogram("Muon_outerEta"                       , "", True  , default_norm              , 1  , -3.0  , 3.0   , 1e2*y_scale   , 1e5*y_scale   , "#mu outer #eta"                           , "# events (2018)"   ),
  Histogram("Muon_outerPhi"                       , "", True  , default_norm              , 1  , -3.0  , 3.0   , 1e2*y_scale   , 1e5*y_scale   , "#mu #phi"                                 , "# events (2018)"   ),
  Histogram("Muon_dxyPVTraj"                      , "", True  , default_norm              , 30 , -800  , 800   , 1e-1  , 1e8   , "#mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("Muon_dxyPVSigned"                    , "", True  , default_norm              , 30 , -800  , 800   , 1e-1  , 1e8   , "#mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("Muon_ip3DPVSigned"                   , "", True  , default_norm              , 30 , -800  , 800   , 1e-1  , 1e8   , "#mu 3D ip [cm]"                           , "# events (2018)"   ),
  Histogram("Muon_dxyBS"                          , "", True  , default_norm              , 30 , -800  , 800   , 1e-1  , 1e8   , "#mu 3D ip [cm]"                           , "# events (2018)"   ),
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

  Histogram("Event_nDSAMuon"                      , "", True  , default_norm              , 1  , 0     , 15    , 1e-2*y_scale   , 1e9*y_scale   , "Number of dSA #mu"                        , "# events (2018)"   ),
  Histogram("DSAMuon_idx"                         , "", True  , default_norm              , 1 , 0     , 15  , 1e-6  , 1e10   , "dSa #mu index"                                , "# events (2018)"   ),
  Histogram("DSAMuon_pt"                          , "", True  , default_norm              , 1 , 0     , 500   , 1e-1  , 1e8   , "dSA #mu p_{T} [GeV]"                      , "# events (2018)"   ),
  Histogram("DSAMuon_eta"                         , "", True  , default_norm              , 1 , -3.5  , 3.5   , 1e2*y_scale   , 1e5*y_scale   , "dSA #mu #eta"                             , "# events (2018)"   ),
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
  Histogram("DSAMuon_outerEta"                    , "", True  , default_norm              , 1  , -3.0  , 3.0   , 1e2*y_scale   , 1e5*y_scale   , "DSA #mu outer #eta"                           , "# events (2018)"   ),
  Histogram("DSAMuon_outerPhi"                    , "", True  , default_norm              , 1  , -3.0  , 3.0   , 1e2*y_scale   , 1e5*y_scale   , "DSA #mu #phi"                                 , "# events (2018)"   ),
  
  Histogram("Event_nLooseMuonsDRMatch"            , "", True  , default_norm              , 1  , 0     , 15    , 1e2*y_scale   , 1e7*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_pt"                , "", True  , default_norm              , 20 , 0     , 500   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_eta"               , "", True  , default_norm              , 20 , -3.5  , 3.5   , 1e0   , 1e8   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_dxy"               , "", True  , default_norm              , 30 , -800  , 800   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsDRMatch_dz"                , "", True  , default_norm              , 30 , -800  , 800   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsOuterDRMatch"       , "", True  , default_norm              , 1  , 0     , 15    , 1e2*y_scale   , 1e7*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_pt"           , "", True  , default_norm              , 20 , 0     , 500   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_eta"          , "", True  , default_norm              , 20 , -3.5  , 3.5   , 1e0   , 1e8   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_dxy"          , "", True  , default_norm              , 30 , -800  , 800   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsOuterDRMatch_dz"           , "", True  , default_norm              , 30 , -800  , 800   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("Event_nLooseMuonsSegmentMatch"       , "", True  , default_norm              , 1  , 0     , 15    , 1e2*y_scale   , 1e7*y_scale   , "Number of loose #mu"                            , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_pt"           , "", True  , default_norm              , 20 , 0     , 500   , 1e-1  , 1e8   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_eta"          , "", True  , default_norm              , 20 , -3.5  , 3.5   , 1e0   , 1e8   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_dxy"          , "", True  , default_norm              , 30 , -600  , 600   , 1e-1  , 1e8   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_dz"           , "", True  , default_norm              , 30 , -600  , 600   , 1e-1  , 1e8   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),

  Histogram("Event_nPatMuonVertex"                , "", True  , default_norm              , 1  , 0     , 15    , 1e2*y_scale   , 1e7*y_scale   , "Number of Pat-Pat #mu vertices"                 , "# events (2018)"   ),
  Histogram("PatMuonVertex_vxy"                   , "", True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("PatMuonVertex_vxySigma"              , "", True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  Histogram("PatMuonVertex_vz"                    , "", True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  Histogram("PatMuonVertex_dR"                    , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat #mu vertex #Delta R"                        , "# events (2018)"   ),
  Histogram("PatMuonVertex_chi2"                  , "", True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  
  Histogram("Event_nPatDSAMuonVertex"             , "", True  , default_norm              , 1  , 0     , 15    , 1e2*y_scale   , 1e7*y_scale   , "Number of Pat-DSA #mu vertices"                 , "# events (2018)"   ),
  Histogram("PatDSAMuonVertex_vxy"                , "", True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "Pat-DSA #mu vertex v_{xy} [cm]"                 , "# events (2018)"   ),
  Histogram("PatDSAMuonVertex_vxySigma"           , "", True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "Pat-DSA #mu vertex #sigma_{v_{xy}} [cm]"        , "# events (2018)"   ),
  Histogram("PatDSAMuonVertex_vz"                 , "", True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "Pat-DSA #mu vertex v_{z} [cm]"                  , "# events (2018)"   ),
  Histogram("PatDSAMuonVertex_dR"                 , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "Pat-DSA #mu vertex #Delta R"                    , "# events (2018)"   ),
  Histogram("PatDSAMuonVertex_chi2"               , "", True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "Pat-DSA #mu vertex #chi^{2}"                    , "# events (2018)"   ),
  
  Histogram("Event_nDSAMuonVertex"                , "", True  , default_norm              , 1  , 0     , 15    , 1e2*y_scale   , 1e7*y_scale   , "Number of DSA-DSA #mu vertices"                 , "# events (2018)"   ),
  Histogram("DSAMuonVertex_vxy"                   , "", True  , default_norm              , 10 , 0     , 600   , 1e0   , 1e8   , "DSA #mu vertex v_{xy} [cm]"                     , "# events (2018)"   ),
  Histogram("DSAMuonVertex_vxySigma"              , "", True  , default_norm              , 2  , 0     , 100   , 1e-1  , 1e8   , "DSA #mu vertex #sigma_{v_{xy}} [cm]"            , "# events (2018)"   ),
  Histogram("DSAMuonVertex_vz"                    , "", True  , default_norm              , 20 , -800  , 800   , 1e-1  , 1e8   , "DSA #mu vertex v_{z} [cm]"                      , "# events (2018)"   ),
  Histogram("DSAMuonVertex_dR"                    , "", True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e8   , "DSA #mu vertex #Delta R"                        , "# events (2018)"   ),
  Histogram("DSAMuonVertex_chi2"                  , "", True  , default_norm              , 10 , 0     , 500   , 1e-1  , 1e8   , "DSA #mu vertex #chi^{2}"                        , "# events (2018)"   ),
  
)

histogramsRatio = [
  ( Histogram("Event_nLooseMuonsDRMatch"       , "", True  , default_norm   , 1  , 0     , 15    , 1e-2    , 1e2   , "Number of loose #mu"         , "#Delta R-matched / Segment matched"   ),
    Histogram("Event_nLooseMuonsSegmentMatch"  , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsDRMatch_pt"           , "", True  , default_norm   , 10 , 0     , 500   , 1e-2    , 1e2   , "loose #mu p_{T} [GeV]"       , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_pt"      , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsDRMatch_eta"          , "", True  , default_norm   , 10  , -3.5  , 3.5  , 1e-2    , 1e2   , "loose #mu #eta"              , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_eta"     , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsDRMatch_dxy"          , "", True  , default_norm   , 10 , -400  , 400   , 1e-2    , 1e2   , "loose #mu d_{xy} [cm]"       , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_dxy"     , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsDRMatch_dz"           , "", True  , default_norm   , 10 , -400  , 400   , 1e-2    , 1e2   , "loose #mu d_{z} [cm]"        , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_dz"      , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  
  ( Histogram("Event_nLooseMuonsOuterDRMatch"  , "", True  , default_norm   , 1  , 0     , 15    , 1e-2    , 1e2   , "Number of loose #mu"         , "#Delta R-matched / Segment matched"   ),
    Histogram("Event_nLooseMuonsSegmentMatch"  , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsOuterDRMatch_pt"      , "", True  , default_norm   , 10 , 0     , 500   , 1e-2    , 1e2   , "loose #mu p_{T} [GeV]"       , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_pt"      , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsOuterDRMatch_eta"     , "", True  , default_norm   , 10 , -3.5  , 3.5   , 1e-2    , 1e2   , "loose #mu #eta"              , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_eta"     , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsOuterDRMatch_dxy"     , "", True  , default_norm   , 10 , -400  , 400   , 1e-2    , 1e2   , "loose #mu d_{xy} [cm]"       , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_dxy"     , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
  ( Histogram("LooseMuonsOuterDRMatch_dz"      , "", True  , default_norm   , 10 , -400  , 400   , 1e-2    , 1e2   , "loose #mu d_{z} [cm]"        , "#Delta R-matched / Segment matched"   ),
    Histogram("LooseMuonsSegmentMatch_dz"      , "", True  , default_norm   , 1  , 0     , 1     , 1       , 1     , ""                            , ""   ) ),
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
  #   legend_description="0.35 GeV, 1 mm",
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
  #   legend_description="0.35 GeV, 10 cm, restricted keep-statements old",
  # ),
  Sample(
    name="tta_mAlp-0p35GeV_ctau-1e2mm",
    file_path=f"{base_path}/LLPtest/signals/tta_mAlp-0p35GeV_ctau-1e2mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kGreen+1,
    legend_description="0.35 GeV, 10 cm, restricted keep-statements new",
  ),
  Sample(
    name="tta_mAlp-0p35GeV_ctau-1e2mm",
    file_path=f"{base_path}/LLPtest/signals_all/tta_mAlp-0p35GeV_ctau-1e2mm/{skim}/{hist_path}/histograms.root",
    type=SampleType.signal,
    cross_sections=cross_sections,
    line_alpha=1,
    line_style=1,
    fill_alpha=0,
    marker_size=0,
    line_color=ROOT.kBlue,
    legend_description="0.35 GeV, 10 cm, all keep-statements",
  ),
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
  #   name="tta_mAlp-0p35GeV_ctau-1e3mm_test",
  #   file_path=f"{base_path}/signals_LLPnanoAOD/tta_mAlp-0p35GeV_ctau-1e3mm/{skim}_test/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=1,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kBlue,
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
  # Sample(
  #   name="tta_mAlp-0p35GeV_ctau-1e7mm",
  #   file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e7mm_nEvents-1000/{skim}/{hist_path}/histograms.root",
  #   type=SampleType.signal,
  #   cross_sections=cross_sections,
  #   line_alpha=1,
  #   line_style=2,
  #   fill_alpha=0,
  #   marker_size=0,
  #   line_color=ROOT.kMagenta,
  #   legend_description="0.35 GeV, 10 km",
  # ),
  
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
