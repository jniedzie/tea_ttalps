import ROOT
import os
from itertools import product

from Sample import SampleType
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from TTAlpsPlotterConfigHelper import TTAlpsPlotterConfigHelper
from ttalps_cross_sections import *
from ttalps_luminosities import *

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms/"

# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_SRDimuons")
skim = ("skimmed_looseSemimuonic_v2_SR", "_JPsiDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons")
# skim = ("skimmed_looseNonTT_v1_QCDCR", "_SRDimuons")  # this is in fact VV CR
# skim = ("skimmed_looseNoBjets_lt4jets_v1_QCDCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons")

# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs{skim[1]}"
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}"
hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}_newSFs" # all SFs
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs{skim[1]}_newSFs" # no PUjetIDSFs
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_PUjetIDSFs{skim[1]}_newSFs" # no bTaggingSFs
# hist_path = f"histograms_muonSFs_muonTriggerSFs_bTaggingSFs_PUjetIDSFs{skim[1]}_newSFs" # no pileup
# hist_path = f"histograms_muonSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}_newSFs" # no muonTriggerSF
# hist_path = f"histograms_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs{skim[1]}_newSFs" # no muonSF

output_formats = ["pdf"]

output_path = f"../plots/{skim[0].replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{year}/"

lumi_label_offset = 0.02
lumi_label_value = luminosity

canvas_size = (800, 600)
canvas_size_2Dhists = (800, 800)
show_ratio_plots = True
ratio_limits = (0.0, 3.0)

legend_max_x = 0.82 if show_ratio_plots else 0.75
legend_max_y = 0.89
legend_width = 0.17 if show_ratio_plots else 0.15
legend_height = 0.045 if show_ratio_plots else 0.035

# only plot backgrounds with N_events > bkgRawEventsThreshold
bkgRawEventsThreshold = 10

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Private Work"

extraMuonVertexCollections = [
  # "MaskedDimuonVerex",      # invariant mass cut only
  "BestDimuonVertex",       # best Dimuon selection without isolation cut
  # "BestPFIsoDimuonVertex",  # best Dimuon selection with isolation cut
]

# Gen-level resonances plots - comment out to avoid plots for these collections 
genMuonVertexCollections = [
  # "BestPFIsoDimuonVertexResonancesNotFromALP",  # Dimuon resonances
  # "GoodPFIsoDimuonVertexResonancesNotFromALP",  # Dimuon resonances
  # "BestPFIsoDimuonVertexNonresonancesNotFromALP",  # Non-resonant Dimuons
  # "GoodPFIsoDimuonVertexNonresonancesNotFromALP",  # Non-resonant Dimuons
]

data_to_include = [
  "SingleMuon2018",
  # "Muon2022preEE",
  # "Muon2022postEE",
]

backgrounds_to_exclude = [
  # "QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  # "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
  # "QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
]

signals_to_include = [
  # "tta_mAlp-2GeV_ctau-1e0mm", 
  # "tta_mAlp-2GeV_ctau-1e1mm", 
  # "tta_mAlp-2GeV_ctau-1e2mm"
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

background_uncertainty_style = 3244  # available styles: https://root.cern.ch/doc/master/classTAttFill.html
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

histograms2D = ()
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
  Histogram("Event_isData"                         , "", False,  True  , default_norm              , 1  , 0     , 2     , 1e-8  , 1e7   , "Is Data Event"                                  , "# events (2018)"   ),
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
  Histogram("TightMuons_pt"                       , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-6  , 1e8   , "tight #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("TightMuons_leadingPt"                , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e5   , "leading tight #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  Histogram("TightMuons_subleadingPt"             , "", False,  True  , default_norm              , 50 , 0     , 1000  , 1e-5  , 1e4   , "all subleading tight #mu p_{T} [GeV]"           , "# events (2018)"   ),
  Histogram("TightMuons_eta"                      , "", False,  True  , default_norm              , 10 , -3.0  , 5.0   , 1e-3  , 1e6   , "tight #mu #eta"                                 , "# events (2018)"   ),
  Histogram("TightMuons_dxy"                      , "", False,  True  , default_norm              , 2  , -0.5  , 0.5   , 1e-2  , 1e10  , "tight #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("TightMuons_dz"                       , "", False,  True  , default_norm              , 2  , -1    , 1     , 1e-2  , 1e8   , "tight #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("TightMuons_pfRelIso04_all"           , "", False,  True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_pfRelIso03_chg"           , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_pfRelIso03_all"           , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "tight #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  # Histogram("TightMuons_miniPFRelIso_chg"         , "", False,  True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  # Histogram("TightMuons_miniPFRelIso_all"         , "", False,  True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "tight #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  # Histogram("TightMuons_jetRelIso"                , "", False,  True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "tight #mu jet Rel Iso"                          , "# events (2018)"   ),
  # Histogram("TightMuons_tkRelIso"                 , "", False,  True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "tight #mu track Rel Iso"                        , "# events (2018)"   ),
  # Histogram("TightMuons_deltaPhiMuonMET"          , "", False,  True  , default_norm              , 20 , -4    , 4     , 1e0   , 1e7   , "tight muon #Delta #phi(MET, #mu)"               , "# events (2018)"   ),
  # Histogram("TightMuons_minvMuonMET"              , "", False,  True  , default_norm              , 40 , 0     , 1000  , 1e-4  , 1e5   , "tight muon m_{MET, l} [GeV]"                    , "# events (2018)"   ),
  
  # ----------------------------------------------------------------------------
  # Loose muons
  # ----------------------------------------------------------------------------
  Histogram("LooseMuonsSegmentMatch_pt"                    , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "loose #mu p_{T} [GeV]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_leadingPt"             , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "leading loose #mu p_{T} [GeV]"                  , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_subleadingPt"          , "", False,  True  , default_norm              , 20 , 0     , 500   , 1e-2  , 1e6   , "all subleading loose #mu p_{T} [GeV]"           , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_eta"                   , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e0   , 1e6   , "loose #mu #eta"                                 , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_dxy"                   , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose #mu d_{xy} [cm]"                          , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_dz"                    , "", False,  True  , default_norm              , 20 , -200  , 200   , 1e-2  , 1e6   , "loose #mu d_{z} [cm]"                           , "# events (2018)"   ),
  Histogram("LooseMuonsSegmentMatch_pfRelIso04_all"        , "", False,  True  , default_norm              , 1  , 0.0   , 0.2   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.4 (all)"                 , "# events (2018)"   ),
  # Histogram("LooseMuonsSegmentMatch_pfRelIso03_chg"        , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (chg)"                 , "# events (2018)"   ),
  # Histogram("LooseMuonsSegmentMatch_pfRelIso03_all"        , "", False,  True  , default_norm              , 1  , 0     , 0.5   , 1e-2  , 1e6   , "Loose #mu PF Rel Iso 0.3 (all)"                 , "# events (2018)"   ),
  # Histogram("LooseMuonsSegmentMatch_miniPFRelIso_chg"      , "", False,  True  , default_norm              , 10 , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (chg)"                , "# events (2018)"   ),
  # Histogram("LooseMuonsSegmentMatch_miniPFRelIso_all"      , "", False,  True  , default_norm              , 5  , -0.1  , 3.5   , 1e-2  , 1e6   , "Loose #mu mini PF Rel Iso (all)"                , "# events (2018)"   ),
  # Histogram("LooseMuonsSegmentMatch_jetRelIso"             , "", False,  True  , default_norm              , 50 , -1    , 8.0   , 1e-2  , 1e6   , "Loose #mu jet Rel Iso"                          , "# events (2018)"   ),
  # Histogram("LooseMuonsSegmentMatch_tkRelIso"              , "", False,  True  , default_norm              , 20 , -0.1  , 8.0   , 1e-2  , 1e6   , "Loose #mu track Rel Iso"                        , "# events (2018)"   ),
  
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
  Histogram("GoodJets_pt"                         , "", False,  True  , default_norm              , 10 , 0     , 1300  , 1e-3  , 1e6   , "good jet p_{T} [GeV]"                           , "# events (2018)"   ),
  Histogram("GoodJets_eta"                        , "", False,  True  , default_norm              , 10 , -3    , 5.0   , 1e-3  , 1e6   , "good jet #eta"                                  , "# events (2018)"   ),
  # Histogram("GoodJets_btagDeepB"                  , "", False,  True  , default_norm              , 10 , 0     , 1.5   , 2e0   , 1e8   , "good jet deepCSV score"                         , "# events (2018)"   ),
  # Histogram("GoodJets_btagDeepFlavB"              , "", False,  True  , default_norm              , 10 , 0     , 1.8   , 1e-1  , 1e8   , "good jet deepJet score"                         , "# events (2018)"   ),
  # Histogram("GoodJets_minvBjet2jets"              , "", False,  True  , default_norm              , 25 , 0     , 1500  , 1e-1  , 1e5   , "good jets m_{bjj} [GeV]"                        , "# events (2018)"   ),
  
  # ----------------------------------------------------------------------------
  # Good b-jets
  # ----------------------------------------------------------------------------
  Histogram("GoodMediumBtaggedJets_pt"            , "", False,  True  , default_norm              , 20 , 0     , 2000  , 1e-3   , 1e6   , "good b-jet p_{T} [GeV]"                         , "# events (2018)"   ),
  Histogram("GoodMediumBtaggedJets_eta"           , "", False,  True  , default_norm              , 5  , -3.5  , 3.5   , 1e-3   , 1e6   , "good b-jet #eta"                                , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_btagDeepB"     , "", False,  True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good b-jet deepCSV score"                       , "# events (2018)"   ),
  # Histogram("GoodMediumBtaggedJets_btagDeepFlavB" , "", False,  True  , default_norm              , 10 , -1    , 1     , 1e0   , 1e8   , "good b-jet deepJet score"                       , "# events (2018)"   ),
  
  # ----------------------------------------------------------------------------
  # Primary vertices
  # ----------------------------------------------------------------------------
  Histogram("Event_PV_npvs"                       , "", False,  True  , default_norm              , 1  , 0     , 150   , 1e-3  , 1e12  , "# Primary vertices"                             , "# events (2018)"   ),
  Histogram("Event_PV_npvsGood"                   , "", False,  True  , default_norm              , 1  , 0     , 80   , 1e-4  , 1e8   , "# Good primary vertices"                        , "# events (2018)"   ),
  Histogram("Event_PV_x"                          , "", False, True   , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV x [cm]"                                      , "# events (2018)"   ),
  Histogram("Event_PV_y"                          , "", False, True   , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV y [cm]"                                      , "# events (2018)"   ),
  Histogram("Event_PV_z"                          , "", False, True   , default_norm              , 1  , 0     , 20   , 1e-2   , 1e8   , "PV z [cm]"                                      , "# events (2018)"   ),
  
)

# ----------------------------------------------------------------------------
# Dimuons
# ----------------------------------------------------------------------------

if skim[1] == "_SRDimuons":
  mass_rebin = 1
  mass_min = 0.0
  mass_max = 100.0
elif skim[1] == "_JPsiDimuons":
  mass_rebin = 1
  mass_min = 2.8
  mass_max = 3.4
elif skim[1] == "_ZDimuons":
  mass_rebin = 20
  mass_min = 70.0
  mass_max = 110.0

for collection, category in product(extraMuonVertexCollections, ("","_PatDSA", "_DSA", "_Pat")):
  histograms += (
    Histogram("Event_n"+collection + category                          , "", False, True  , default_norm            , 1           , 0         , 5         , 1e-3  , 1e8   , "Number of loose #mu vertices"             , "# events (2018)" ),
    Histogram(collection + category+"_invMass"                         , "", False, False , default_norm            , mass_rebin  , mass_min  , mass_max  , 0     , 300   , "#mu vertex M_{#mu #mu} [GeV]"             , "# events (2018)" ),
    Histogram(collection + category+"_logInvMass"                      , "", False, True  , default_norm            , 10          , -1        , 2         , 1e-5  , 1e3   , "#mu vertex log_{10}(M_{#mu #mu} [GeV])"   , "# events (2018)" ),
    Histogram(collection + category+"_eta"                             , "", False, True  , default_norm            , 5           , -3.5      , 3.5       , 1e-3  , 1e6   , "#mu vertex p_{T} [GeV]"                   , "# events (2018)" ),
    Histogram(collection + category+"_pt"                              , "", False, True  , default_norm            , 10          , 0         , 200       , 1e-3  , 1e6   , "#mu vertex p_{T} [GeV]"                   , "# events (2018)" ),
    Histogram(collection + category+"_leadingPt"                       , "", False, True  , default_norm            , 5           , 0         , 200       , 1e-3  , 1e6   , "#mu vertex leading p_{T} [GeV]"           , "# events (2018)" ),
    
    Histogram(collection + category+"_LxySignificance"                 , "", False, True  , default_norm            , 10           , 0         , 100       , 1e-3  , 1e6   , "#mu vertex L_{xy} / #sigma_{Lxy}"         , "# events (2018)" ),
    Histogram(collection + category+"_Lxy"                             , "", False, True  , default_norm            , 20          , 0         , 300       , 1e-8  , 1e7   , "#mu vertex L_{xy} [cm]"                   , "# events (2018)" ),
    Histogram(collection + category+"_logLxy"                          , "", False, True  , default_norm            , 10          , -4        , 3         , 1e-8  , 1e7   , "#mu vertex L_{xy} [cm]"                   , "# events (2018)" ),
    Histogram(collection + category+"_LxySigma"                        , "", False, True  , default_norm            , 1           , 0         , 2         , 1e-3  , 1e6   , "#mu vertex #sigma_{Lxy} [cm]"             , "# events (2018)" ),
    
    # Histogram(collection + category+"_normChi2"                        , "", False, True  , default_norm            , 100         , 0         , 5         , 1e-5  , 1e4   , "#mu vertex #chi^{2}/ndof"                 , "# events (2018)" ),
    # Histogram(collection + category+"_maxHitsInFrontOfVert"            , "", False, True  , default_norm            , 1           , 0         , 35        , 1e-6  , 1e6   , "Max N(hits before vertex)"                , "# events (2018)" ),
    # Histogram(collection + category+"_dca"                             , "", False, True  , default_norm            , 10          , 0         , 10        , 1e-6  , 1e6   , "DCA [cm]"                                 , "# events (2018)" ),
    # Histogram(collection + category+"_absCollinearityAngle"            , "", False, True  , default_norm            , 10          , 0         , 3.15      , 1e-6  , 1e6   , "#mu vertex |#Delta #Phi|"                 , "# events (2018)" ),
    # Histogram(collection + category+"_absPtLxyDPhi1"                   , "", False, True  , default_norm            , 10          , 0         , 3.15      , 1e-4  , 1e5   , "#mu vertex |#Delta #phi_{#mu1}|"          , "# events (2018)" ),
    # Histogram(collection + category+"_pfRelIso04all1"                  , "", False, True  , default_norm            , 4           , 0         , 10        , 1e-3  , 1e6   , "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )"  , "# events (2018)" ),
    # Histogram(collection + category+"_pfRelIso04all2"                  , "", False, True  , default_norm            , 4           , 0         , 10        , 1e-3  , 1e6   , "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )"  , "# events (2018)" ),
  )
  histograms2D += (
    Histogram2D(collection + category+"_log3Dangle_logLxySignificance",  "",  False,  False,  True,  NormalizationType.to_lumi, 4, 4, -3, 1, -2,  20, 1e-3,  1e2,  "#mu vertex #alpha",  "#mu vertex L_{xy} / #sigma_{Lxy}",   "# events (2018)",  ""  ),
  )
  
for collection in genMuonVertexCollections:
  for category in ["_PatDSA", "_DSA", "_Pat"]:
    histograms += (
      Histogram("Event_n"+collection + category                     , "", False, True  , default_norm     , 1  , 0     , 5     , 1e-3  , 1e6   , "Number of #mu vertices"            , "# events (2018)" ),
    )
    histograms2D += (
      Histogram2D(collection + category+"_log3Dangle_logLxySignificance",  "",  False,  False,  True,  NormalizationType.to_lumi, 4, 4, -3, 1, -2,  20, 1e-3,  1e2,  "#mu vertex #alpha",  "#mu vertex L_{xy} / #sigma_{Lxy}",   "# events (2018)",  ""  ),
    )