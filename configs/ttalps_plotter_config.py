import ROOT
import os

from Sample import SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from TTAlpsPlotterConfigHelper import TTAlpsPlotterConfigHelper
from ttalps_cross_sections import *

year = "2018"
cross_sections = get_cross_sections(year)

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms/"

# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons")
skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons")

hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs{skim[1]}"

output_formats = ["pdf"]

output_path = f"../plots/{skim[0].replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{year}/"

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
legend_width = 0.17 if show_ratio_plots else 0.20
legend_height = 0.045 if show_ratio_plots else 0.03

# only plot backgrounds with N_events > bkgRawEventsThreshold
bkgRawEventsThreshold = 10

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Private Work"

extraMuonVertexCollections = [
  # "MaskedDimuonVerex",      # invariant mass cut only
  "BestDimuonVertex",       # best Dimuon selection without isolation cut
  "BestPFIsoDimuonVertex",  # best Dimuon selection with isolation cut
]

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
  skim[0],
  hist_path,
  data_to_include,
  backgrounds_to_exclude,
  signals_to_include,
  (legend_max_x, legend_max_y, legend_width, legend_height)
)

samples = []
configHelper.add_samples(SampleType.data, samples)
configHelper.add_samples(SampleType.background, samples)
if year == "2018":  # can change this when central samples are done
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
#           name                                  title logx    logy    norm_type                 rebin xmin   xmax    ymin    ymax,     xlabel                                             ylabel
  
  # ----------------------------------------------------------------------------
  # Event variables
  # ----------------------------------------------------------------------------
  Histogram("cutFlow"                              , "", False,  True  , default_norm              , 1  , 0     , 12    , 1e1   , 1e15  , "Selection"                                      , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex"       , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e3   , 4e3   , "Selection"                                      , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex_Pat"   , "", False,  True  , default_norm              , 1  , 0     , 10    , 2e2   , 1e4   , "Selection"                                      , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex_PatDSA", "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e4   , "Selection"                                      , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex_DSA"   , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e-1  , 1e4   , "Selection"                                      , "Number of events"  ),
  Histogram("dimuonCutFlow_BestDimuonVertex"       , "", False,  True  , default_norm              , 1  , 0     , 8     , 1e-1  , 1e2   , "Selection"                                      , "Number of events"  ),
  Histogram("Event_normCheck"                      , "", False,  True  , default_norm              , 1  , 0     , 1     , 1e-2  , 1e7   , "norm check"                                     , "# events (2018)"   ),
  Histogram("Event_MET_pt"                         , "", False,  True  , default_norm              , 10 , 0     , 800   , 1e-8  , 1e9   , "MET p_{T} [GeV]"                                , "# events (2018)"   ),
  # Histogram("Event_nTightMuons"                   , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of tight #mu"                            , "# events (2018)"   ),
  # Histogram("Event_nLoosePATMuons"                , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose #mu"                            , "# events (2018)"   ),
  # Histogram("Event_nLooseDSAMuons"                , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose dSA #mu"                        , "# events (2018)"   ),
  # Histogram("Event_nLooseElectrons"               , "", False,  True  , default_norm              , 1  , 0     , 10    , 1e1   , 1e9   , "Number of loose electrons"                      , "# events (2018)"   ),
  # Histogram("Event_nGoodJets"                     , "", False,  True  , default_norm              , 1  , 2     , 16    , 1e-2  , 1e10  , "Number of good jets"                            , "# events (2018)"   ),
  # Histogram("Event_nGoodMediumBtaggedJets"        , "", False,  True  , default_norm              , 1  , 0     , 20    , 1e0   , 1e9   , "Number of good b-jets"                          , "# events (2018)"   ),
  # ----------------------------------------------------------------------------
  # Tight muons
  # ----------------------------------------------------------------------------
  # Histogram("TightMuons_pt"                       , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-6  , 1e8   , "tight #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # Histogram("TightMuons_leadingPt"                , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e5   , "leading tight #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  # Histogram("TightMuons_subleadingPt"             , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e4   , "all subleading tight #mu p_{T} [GeV]"           , "# events (2018)"   ),
  # Histogram("TightMuons_eta"                      , "", False,  True  , default_norm              , 10 , -3.0  , 5.0   , 1e0   , 1e5   , "tight #mu #eta"                                 , "# events (2018)"   ),
  # Histogram("TightMuons_dxy"                      , "", False,  True  , default_norm              , 2  , -0.5  , 0.5   , 1e-2  , 1e10  , "tight #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  # Histogram("TightMuons_dz"                       , "", False,  True  , default_norm              , 2  , -1    , 1     , 1e-2  , 1e8   , "tight #mu d_{z} [cm]"                           , "# events (2018)"   ),
  # Histogram("TightMuons_pfRelIso04_all"           , "", False,  True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_pfRelIso03_chg"           , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_pfRelIso03_all"           , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_miniPFRelIso_chg"         , "", False,  True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  # Histogram("TightMuons_miniPFRelIso_all"         , "", False,  True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  # Histogram("TightMuons_jetRelIso"                , "", False,  True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "tight #mu jet Rel Iso"                          , "# events (2018)"   ),
  # Histogram("TightMuons_tkRelIso"                 , "", False,  True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "tight #mu track Rel Iso"                        , "# events (2018)"   ),
  # Histogram("TightMuons_deltaPhiMuonMET"          , "", False,  True  , default_norm              , 20 , -4    , 4     , 1e0   , 1e7   , "tight muon #Delta #phi(MET, #mu)"               , "# events (2018)"   ),
  # Histogram("TightMuons_minvMuonMET"              , "", False,  True  , default_norm              , 40 , 0     , 1000  , 1e-4  , 1e5   , "tight muon m_{MET, l} [GeV]"                    , "# events (2018)"   ),
  
  # ----------------------------------------------------------------------------
  # Loose PAT muons
  # ----------------------------------------------------------------------------
  # Histogram("LoosePATMuons_pt"                    , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  # Histogram("LoosePATMuons_leadingPt"             , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "leading loose #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  # Histogram("LoosePATMuons_subleadingPt"          , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "all subleading loose #mu p_{T} [GeV]"           , "# events (2018)"   ),
  # Histogram("LoosePATMuons_eta"                   , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e6   , "loose #mu #eta"                                 , "# events (2018)"   ),
  # Histogram("LoosePATMuons_dxy"                   , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  # Histogram("LoosePATMuons_dz"                    , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  # Histogram("LoosePATMuons_pfRelIso04_all"        , "", False,  True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  # Histogram("LoosePATMuons_pfRelIso03_chg"        , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  # Histogram("LoosePATMuons_pfRelIso03_all"        , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  # Histogram("LoosePATMuons_miniPFRelIso_chg"      , "", False,  True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  # Histogram("LoosePATMuons_miniPFRelIso_all"      , "", False,  True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  # Histogram("LoosePATMuons_jetRelIso"             , "", False,  True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "Loose #mu jet Rel Iso"                          , "# events (2018)"   ),
  # Histogram("LoosePATMuons_tkRelIso"              , "", False,  True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "Loose #mu track Rel Iso"                        , "# events (2018)"   ),
  
  # ----------------------------------------------------------------------------
  # Loose DSA muons
  # ----------------------------------------------------------------------------
  # Histogram("LooseDSAMuons_pt"                    , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "loose dSA #mu p_{T} [GeV]"                      , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_eta"                   , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e6   , "loose dSA #mu #eta"                             , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_dxy"                   , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose dSA #mu d_{xy} [cm]"                      , "# events (2018)"   ),
  # Histogram("LooseDSAMuons_dz"                    , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose dSA #mu d_{z} [cm]"                       , "# events (2018)"   ),
  
  
  # ----------------------------------------------------------------------------
  # Loose electrons
  # ----------------------------------------------------------------------------
  # Histogram("LooseElectrons_pt"                   , "", False,  True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "loose electron p_{T} [GeV]"                     , "# events (2018)"   ),
  # Histogram("LooseElectrons_leadingPt"            , "", False,  True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "leading loose electron p_{T} [GeV]"             , "# events (2018)"   ),
  # Histogram("LooseElectrons_subleadingPt"         , "", False,  True  , default_norm              , 10 , 0     , 500   , 1e-2  , 1e6   , "all subleading loose electron p_{T} [GeV]"      , "# events (2018)"   ),
  # Histogram("LooseElectrons_eta"                  , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e-2  , 1e6   , "loose electron #eta"                            , "# events (2018)"   ),
  # Histogram("LooseElectrons_dxy"                  , "", False,  True  , default_norm              , 10 , -10   , 10    , 1e-2  , 1e6   , "loose electron d_{xy}"                          , "# events (2018)"   ),
  # Histogram("LooseElectrons_dz"                   , "", False,  True  , default_norm              , 10 , -10   , 10    , 1e-2  , 1e6   , "loose electron d_{z}"                           , "# events (2018)"   ),
  
  # ----------------------------------------------------------------------------
  # Good jets
  # ----------------------------------------------------------------------------
  # Histogram("GoodJets_pt"                         , "", False,  True  , default_norm              , 10 , 0     , 1300  , 1e-3  , 1e6   , "good jet p_{T} [GeV]"                           , "# events (2018)"   ),
  # Histogram("GoodJets_eta"                        , "", False,  True  , default_norm              , 10 , -3    , 5.0   , 1e1   , 1e8   , "good jet #eta"                                  , "# events (2018)"   ),
  # Histogram("GoodJets_btagDeepB"                  , "", False,  True  , default_norm              , 10 , 0     , 1.5   , 2e0   , 1e8   , "good jet deepCSV score"                         , "# events (2018)"   ),
  # Histogram("GoodJets_btagDeepFlavB"              , "", False,  True  , default_norm              , 10 , 0     , 1.8   , 1e-1  , 1e8   , "good jet deepJet score"                         , "# events (2018)"   ),
  # Histogram("GoodJets_minvBjet2jets"              , "", False,  True  , default_norm              , 25 , 0     , 1500  , 1e-1  , 1e5   , "good jets m_{bjj} [GeV]"                        , "# events (2018)"   ),
  
  # ----------------------------------------------------------------------------
  # Good b-jets
  # ----------------------------------------------------------------------------
  # Histogram("GoodMediumBtaggedJets_pt"            , "", False,  True  , default_norm              , 50 , 0     , 2000  , 1e-5  , 1e4   , "good b-jet p_{T} [GeV]"                         , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_eta"           , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e10  , "good b-jet #eta"                                , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_btagDeepB"     , "", False,  True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good b-jet deepCSV score"                       , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_btagDeepFlavB" , "", False,  True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good b-jet deepJet score"                       , "# events (2018)"   ),
  
  # ----------------------------------------------------------------------------
  # Primary vertices
  # ----------------------------------------------------------------------------
  Histogram("Event_PV_npvs"                       , "", False,  True  , default_norm              , 1  , 0     , 150   , 1e-3  , 1e12  , "# Primary vertices"                             , "# events (2018)"   ),
  Histogram("Event_PV_npvsGood"                   , "", False,  True  , default_norm              , 1  , 0     , 150   , 1e-3  , 1e6   , "# Good primary vertices"                        , "# events (2018)"   ),
  Histogram("Event_PV_x"                          , "", False, True   , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV x [cm]"                                      , "# events (2018)"   ),
  Histogram("Event_PV_y"                          , "", False, True   , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV y [cm]"                                      , "# events (2018)"   ),
  Histogram("Event_PV_z"                          , "", False, True   , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV z [cm]"                                      , "# events (2018)"   ),
  
)

for collection in extraMuonVertexCollections:
  for category in ["_PatDSA", "_DSA", "_Pat"]:
    histograms += (
      Histogram("Event_n"+collection + category                          , "", False, True  , default_norm            , 1  , 0     , 5     , 1e-3  , 1e8   , "Number of loose #mu vertices"             , "# events (2018)" ),
      # Histogram(collection + category+"_invMass"                         , "", False, False , default_norm            , 1  , 2.7   , 3.5   , 0     , 1500  , "#mu vertex M_{#mu #mu} [GeV]"             , "# events (2018)" ),
      Histogram(collection + category+"_invMass"                         , "", False, False , default_norm            , 20 , 70    , 110   , 0     , 30    , "#mu vertex M_{#mu #mu} [GeV]"             , "# events (2018)" ),
      Histogram(collection + category+"_pt"                              , "", False, True  , default_norm            , 10 , 0     , 200   , 1e-3  , 1e6   , "#mu vertex p_{T} [GeV]"                   , "# events (2018)" ),
      Histogram(collection + category+"_vxySignificance"                 , "", False, True  , default_norm            , 2  , 0     , 200   , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"         , "# events (2018)" ),
      Histogram(collection + category+"_vxy"                             , "", False, True  , default_norm            , 5  , 0     , 10    , 1e-10 , 1e6   , "#mu vertex L_{xy} [cm]"                   , "# events (2018)" ),
      Histogram(collection + category+"_vxySigma"                        , "", False, True  , default_norm            , 2  , 0     , 1     , 1e-3  , 1e6   , "#mu vertex #sigma_{Lxy} [cm]"             , "# events (2018)" ),
      Histogram(collection + category+"_vxySignificanceV2"               , "", False, True  , default_norm            , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"         , "# events (2018)" ),
      Histogram(collection + category+"_dR"                              , "", False, True  , default_norm            , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex #Delta R"                      , "# events (2018)" ),
      Histogram(collection + category+"_proxDR"                          , "", False, True  , default_norm            , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex proximity #Delta R"            , "# events (2018)" ),
      Histogram(collection + category+"_outerDR"                         , "", False, True  , default_norm            , 5  , 0     , 6     , 1e-5  , 1e6   , "#mu vertex outer #Delta R"                , "# events (2018)" ),
      Histogram(collection + category+"_normChi2"                        , "", False, True  , default_norm            , 100, 0     , 5     , 1e-5  , 1e4   , "#mu vertex #chi^{2}/ndof"                 , "# events (2018)" ),
      Histogram(collection + category+"_chargeProduct"                   , "", False, True  , default_norm            , 1  , -1    , 2     , 1e-3  , 1e8   , "Dimuon charge"                            , "# events (2018)" ),
      Histogram(collection + category+"_maxHitsInFrontOfVert"            , "", False, True  , default_norm            , 1  , 0     , 35    , 1e-6  , 1e6   , "Max N(hits before vertex)"                , "# events (2018)" ),
      Histogram(collection + category+"_dca"                             , "", False, True  , default_norm            , 20 , 0     , 15    , 1e-6  , 1e6   , "DCA [cm]"                                 , "# events (2018)" ),
      Histogram(collection + category+"_absCollinearityAngle"            , "", False, True  , default_norm            , 10 , 0     , 3.15  , 1e-6  , 1e6   , "#mu vertex |#Delta #Phi|"                 , "# events (2018)" ),
      Histogram(collection + category+"_absPtLxyDPhi1"                   , "", False, True  , default_norm            , 10 , 0     , 3.15  , 1e-4  , 1e5   , "#mu vertex |#Delta #phi_{#mu1}|"          , "# events (2018)" ),
      Histogram(collection + category+"_absPtLxyDPhi2"                   , "", False, True  , default_norm            , 10 , 0     , 3.15  , 1e-4  , 1e5   , "#mu vertex |#Delta #phi_{#mu2}|"          , "# events (2018)" ),
      Histogram(collection + category+"_nTrackerLayers1"                 , "", False, True  , default_norm            , 1  , 0     , 50    , 1e-3  , 1e10  , "#mu_{1} N(tracker layers)"                , "# events (2018)" ),
      Histogram(collection + category+"_nTrackerLayers2"                 , "", False, True  , default_norm            , 1  , 0     , 50    , 1e-3  , 1e6   , "#mu_{2} N(tracker layers)"                , "# events (2018)" ),
      Histogram(collection + category+"_nSegments1"                      , "", False, True  , NormalizationType.to_one, 1  , 0     , 10    , 1e-6  , 1e4   , "#mu_{1} N(muon segments)"                 , "# events (2018)" ),
      Histogram(collection + category+"_nSegments2"                      , "", False, True  , NormalizationType.to_one, 1  , 0     , 10    , 1e-6  , 1e4   , "#mu_{2} N(muon segments)"                 , "# events (2018)" ),
      Histogram(collection + category+"_nSegmentsSum"                    , "", False, True  , default_norm            , 1  , 0     , 20    , 1e-3  , 1e10  , "#mu_{1} + #mu_{2} N(muon segments)"       , "# events (2018)" ),
      Histogram(collection + category+"_leadingPt"                       , "", False, True  , default_norm            , 5  , 0     , 50    , 1e-3  , 1e6   , "#mu vertex leading p_{T} [GeV]"           , "# events (2018)" ),
      Histogram(collection + category+"_dxyPVTraj1"                      , "", False, True  , default_norm            , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} [cm]"               , "# events (2018)" ),
      Histogram(collection + category+"_dxyPVTraj2"                      , "", False, True  , default_norm            , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} [cm]"               , "# events (2018)" ),
      Histogram(collection + category+"_minDxyPVTraj"                    , "", False, True  , default_norm            , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex min d_{xy} [cm]"               , "# events (2018)" ),
      Histogram(collection + category+"_maxDxyPVTraj"                    , "", False, True  , default_norm            , 10 , 0     , 800   , 1e-3  , 1e6   , "#mu vertex max d_{xy} [cm]"               , "# events (2018)" ),
      Histogram(collection + category+"_dxyPVTrajSig1"                   , "", False, True  , default_norm            , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{1} / #sigma_{dxy}^{1}" , "# events (2018)" ),
      Histogram(collection + category+"_dxyPVTrajSig2"                   , "", False, True  , default_norm            , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex d_{xy}^{2} / #sigma_{dxy}^{2}" , "# events (2018)" ),
      Histogram(collection + category+"_minDxyPVTrajSig"                 , "", False, True  , default_norm            , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex min d_{xy} / #sigma_{dxy}"     , "# events (2018)" ),
      Histogram(collection + category+"_maxDxyPVTrajSig"                 , "", False, True  , default_norm            , 2  , 0     , 80    , 1e-3  , 1e6   , "#mu vertex max d_{xy} / #sigma_{dxy}"     , "# events (2018)" ),
      Histogram(collection + category+"_displacedTrackIso03Dimuon1"      , "", False, True  , default_norm            , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)" ),
      Histogram(collection + category+"_displacedTrackIso04Dimuon1"      , "", False, True  , default_norm            , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )" , "# events (2018)" ),
      Histogram(collection + category+"_displacedTrackIso03Dimuon2"      , "", False, True  , default_norm            , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)" ),
      Histogram(collection + category+"_displacedTrackIso04Dimuon2"      , "", False, True  , default_norm            , 1  , 0     , 0.5   , 1e-7  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )" , "# events (2018)" ),
      Histogram(collection + category+"_displacedTrackIso03Muon1"        , "", False, True  , default_norm            , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)" ),
      Histogram(collection + category+"_displacedTrackIso04Muon1"        , "", False, True  , default_norm            , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{1} I_{trk}^{rel} ( #Delta R < 0.4 )" , "# events (2018)" ),
      Histogram(collection + category+"_displacedTrackIso03Muon2"        , "", False, True  , default_norm            , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.3 )" , "# events (2018)" ),
      Histogram(collection + category+"_displacedTrackIso04Muon2"        , "", False, True  , default_norm            , 1  , 0     , 1     , 1e-3  , 1e9   , "#mu_{2} I_{trk}^{rel} ( #Delta R < 0.4 )" , "# events (2018)" ),
      Histogram(collection + category+"_pfRelIso04all1"                  , "", False, True  , default_norm            , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )"  , "# events (2018)" ),
      Histogram(collection + category+"_pfRelIso04all2"                  , "", False, True  , default_norm            , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )"  , "# events (2018)" ),
      Histogram(collection + category+"_tkRelIsoMuon1"                   , "", False, True  , default_norm            , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{1} I_{tk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)" ),
      Histogram(collection + category+"_tkRelIsoMuon2"                   , "", False, True  , default_norm            , 4  , 0     , 10    , 1e-3  , 1e6   , "#mu_{2} I_{tk}^{rel} ( #Delta R < 0.3 )"  , "# events (2018)" ),
    )
    