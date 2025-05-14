import ROOT
import os
from itertools import product

from Sample import SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

from TTAlpsPlotterConfigHelper import TTAlpsPlotterConfigHelper
from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity

year = "2018"
# year = "2022preEE"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms/"

skim = ("skimmed_looseSemimuonic_v2_SR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch", "SR")

# skim = ("skimmed_looseSemimuonic_v2_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch", "SR")
# skim = ("skimmed_looseSemimuonic_v2_SR_looseMuonPtGt8GeV", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch", "SR")

# skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons")

# skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "_JPsiDimuons_LooseNonLeadingMuonsVertexSegmentMatch", "SR")

# skim = ("skimmed_looseSemimuonic_v2_ttbarCR", "", "")
# skim = ("skimmed_looseSemielectronic_v1_ttbarCR", "", "ttCR_electron")

# skim = ("skimmed_looseNonTT_v1_QCDCR", "SRDimuons")  # this is in fact VV CR
# skim = ("skimmed_looseNoBjets_lt4jets_v1_QCDCR", "SRDimuons")
# skim = ("skimmed_looseNoBjets_lt4jets_v1_merged", "JPsiDimuons", "SR")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR", "SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "SRDimuons")

# skim = ("skimmed_looseInvertedMet_v1_SR", "JPsiDimuons", "LooseNonLeadingMuonsVertexSegmentMatch", "SR")

hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_{skim[1]}_{skim[2]}"
if year == "2022preEE" or year == "2022postEE" or year == "2023preBPix" or year == "2023postBPix":
  hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_{skim[1]}_{skim[2]}" # no PUjetIDSFs for Run 3


output_formats = ["pdf"]

output_path = (
    f"../plots/{skim[0].replace('skimmed_', '')}_"
    f"{hist_path.replace('histograms_', '').replace('histograms', '')}_{year}/"
)

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
bkgRawEventsThreshold = 0

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Private Work"

extraMuonVertexCollections = [
  # "MaskedDimuonVerex",      # invariant mass cut only
  "BestDimuonVertex",       # best Dimuon selection without isolation cut
  # "BestPFIsoDimuonVertex",  # best Dimuon selection with isolation cut
  # "BestPFIsoDimuonVertexNminus1",  # best Dimuon selection with isolation cut
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
    
    # "EGamma2018",
]
if not data_to_include:
  show_ratio_plots = False

backgrounds_to_exclude = [
    # "QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    # "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    # "QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
]

signals_to_include = [
    # "tta_mAlp-0p35GeV_ctau-1e1mm",

    # "tta_mAlp-2GeV_ctau-1e-5mm",
    # "tta_mAlp-2GeV_ctau-1e1mm",
    # "tta_mAlp-2GeV_ctau-1e2mm",
    # "tta_mAlp-2GeV_ctau-1e3mm"

    # "tta_mAlp-12GeV_ctau-1e1mm",
    # "tta_mAlp-12GeV_ctau-1e2mm",

    # "TTALPto2Mu_MALP-2_ctau-1e0mm"
    # "TTALPto2Mu_MALP-2_ctau-1e2mm"
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
if year == "2018":  # can change this when central samples are done
  configHelper.add_samples(SampleType.signal, samples)

custom_stacks_order = configHelper.get_custom_stacks_order(samples)

background_uncertainty_style = 3244  # available styles: https://root.cern.ch/doc/master/classTAttFill.html
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
# default_norm = NormalizationType.none

histogramsRatio = []
weightsBranchName = "genWeight"

histograms2D = ()
histograms = (
    # name title logx logy norm_type rebin xmin xmax ymin ymax xlabel ylabel

    # ----------------------------------------------------------------------------
    # Event variables
    # ----------------------------------------------------------------------------
    Histogram("cutFlow", "", False,  True, default_norm, 1, 0, 10, 1e1, 1e15, "Selection", "Number of events"),
    Histogram("dimuonCutFlow_BestDimuonVertex", "", False,  True, default_norm,
              1, 0, 10, 1e2, 1e7, "Selection", "Number of events"),
    Histogram("dimuonCutFlow_BestDimuonVertex_Pat", "", False,  True,
              default_norm, 1, 0, 10, 2e2, 1e7, "Selection", "Number of events"),
    Histogram("dimuonCutFlow_BestDimuonVertex_PatDSA", "", False,  True,
              default_norm, 1, 0, 10, 1e2, 1e7, "Selection", "Number of events"),
    Histogram("dimuonCutFlow_BestDimuonVertex_DSA", "", False,  False,
              default_norm, 1, 0, 10, 0, 2000, "Selection", "Number of events"),
    Histogram("Event_normCheck", "", False,  True, default_norm, 1, 0, 1, 1e-2, 1e7, "norm check", f"# events ({year})"),
    Histogram("Event_isData", "", False,  True, default_norm, 1, 0, 2, 1e-8, 1e7, "Is Data Event", f"# events ({year})"),
    Histogram("Event_MET_pt", "", False,  True, default_norm, 10, 0,
              800, 1e-8, 1e9, "MET p_{T} [GeV]", f"# events ({year})"),
    # Histogram("Event_nTightMuons", "", False,  True, default_norm, 1, 0,
    #           10, 1e1, 1e9, "Number of tight #mu", f"# events ({year})"),
    # Histogram("Event_nLoosePATMuons", "", False,  True, default_norm, 1,
    #           0, 10, 1e1, 1e9, "Number of loose #mu", f"# events ({year})"),
    # Histogram("Event_nLooseDSAMuons", "", False,  True, default_norm, 1, 0,
    #           10, 1e1, 1e9, "Number of loose dSA #mu", f"# events ({year})"),
    # Histogram("Event_nLooseElectrons", "", False,  True, default_norm, 1, 0,
    #           10, 1e1, 1e9, "Number of loose electrons", f"# events ({year})"),
    # Histogram("Event_nGoodJets", "", False,  True, default_norm, 1, 2,
    #           16, 1e-2, 1e10, "Number of good jets", f"# events ({year})"),
    # Histogram("Event_nGoodMediumBtaggedJets", "", False,  True, default_norm,
    #           1, 0, 20, 1e0, 1e9, "Number of good b-jets", f"# events ({year})"),
    # ----------------------------------------------------------------------------
    # Tight muons
    # ----------------------------------------------------------------------------
    Histogram("TightMuons_pt", "", False,  True, default_norm, 50, 0,
              1000, 1e-6, 1e8, "tight #mu p_{T} [GeV]", f"# events ({year})"),
    Histogram("TightMuons_leadingPt", "", False,  True, default_norm, 50, 0, 1000,
              1e-5, 1e5, "leading tight #mu p_{T} [GeV]", f"# events ({year})"),
    Histogram("TightMuons_subleadingPt", "", False,  True, default_norm, 50, 0, 1000,
              1e-5, 1e4, "all subleading tight #mu p_{T} [GeV]", f"# events ({year})"),
    Histogram("TightMuons_eta", "", False,  True, default_norm, 10, -
              3.0, 5.0, 1e-3, 1e6, "tight #mu #eta", f"# events ({year})"),
    Histogram("TightMuons_dxy", "", False,  True, default_norm, 2, -0.5,
              0.5, 1e-2, 1e10, "tight #mu d_{xy} [cm]", f"# events ({year})"),
    Histogram("TightMuons_dz", "", False,  True, default_norm, 2, -1,
              1, 1e-2, 1e8, "tight #mu d_{z} [cm]", f"# events ({year})"),
    Histogram("TightMuons_pfRelIso04_all", "", False,  True, default_norm, 1, 0.0,
              0.2, 1e-2, 1e6, "tight #mu PF Rel Iso 0.4 (all)", f"# events ({year})"),
    # Histogram("TightMuons_pfRelIso03_chg", "", False,  True, default_norm, 1, 0,
    #           0.5, 1e-2, 1e6, "tight #mu PF Rel Iso 0.3 (chg)", f"# events ({year})"),
    # Histogram("TightMuons_pfRelIso03_all", "", False,  True, default_norm, 1, 0,
    #           0.5, 1e-2, 1e6, "tight #mu PF Rel Iso 0.3 (all)", f"# events ({year})"),
    # Histogram("TightMuons_miniPFRelIso_chg", "", False,  True, default_norm, 10, -0.1,
    #           3.5, 1e-2, 1e6, "tight #mu mini PF Rel Iso (chg)", f"# events ({year})"),
    # Histogram("TightMuons_miniPFRelIso_all", "", False,  True, default_norm, 5, -0.1,
    #           3.5, 1e-2, 1e6, "tight #mu mini PF Rel Iso (all)", f"# events ({year})"),
    # Histogram("TightMuons_jetRelIso", "", False,  True, default_norm, 50, -
    #           1, 8.0, 1e-2, 1e6, "tight #mu jet Rel Iso", f"# events ({year})"),
    # Histogram("TightMuons_tkRelIso", "", False,  True, default_norm, 20, -0.1,
    #           8.0, 1e-2, 1e6, "tight #mu track Rel Iso", f"# events ({year})"),
    # Histogram("TightMuons_deltaPhiMuonMET", "", False,  True, default_norm, 20, -4,
    #           4, 1e0, 1e7, "tight muon #Delta #phi(MET, #mu)", f"# events ({year})"),
    # Histogram("TightMuons_minvMuonMET", "", False,  True, default_norm, 40, 0,
    #           1000, 1e-4, 1e5, "tight muon m_{MET, l} [GeV]", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Loose muons
    # ----------------------------------------------------------------------------
    # Histogram("LooseMuonsSegmentMatch_pt", "", False,  True, default_norm, 20,
    #           0, 500, 1e-2, 1e6, "loose #mu p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_leadingPt", "", False,  True, default_norm, 20,
    #           0, 500, 1e-2, 1e6, "leading loose #mu p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_subleadingPt", "", False,  True, default_norm, 20, 0,
    #           500, 1e-2, 1e6, "all subleading loose #mu p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_eta", "", False,  True, default_norm,
    #           5, -3.5, 3.5, 1e0, 1e6, "loose #mu #eta", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_dxy", "", False,  True, default_norm, 20, -
    #           200, 200, 1e-2, 1e6, "loose #mu d_{xy} [cm]", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_dz", "", False,  True, default_norm, 20, -
    #           200, 200, 1e-2, 1e6, "loose #mu d_{z} [cm]", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_pfRelIso04_all", "", False,  True, default_norm, 1,
    #           0.0, 0.2, 1e-2, 1e6, "Loose #mu PF Rel Iso 0.4 (all)", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_pfRelIso03_chg", "", False,  True, default_norm,
    #           1, 0, 0.5, 1e-2, 1e6, "Loose #mu PF Rel Iso 0.3 (chg)", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_pfRelIso03_all", "", False,  True, default_norm,
    #           1, 0, 0.5, 1e-2, 1e6, "Loose #mu PF Rel Iso 0.3 (all)", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_miniPFRelIso_chg", "", False,  True, default_norm,
    #           10, -0.1, 3.5, 1e-2, 1e6, "Loose #mu mini PF Rel Iso (chg)", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_miniPFRelIso_all", "", False,  True, default_norm,
    #           5, -0.1, 3.5, 1e-2, 1e6, "Loose #mu mini PF Rel Iso (all)", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_jetRelIso", "", False,  True, default_norm,
    #           50, -1, 8.0, 1e-2, 1e6, "Loose #mu jet Rel Iso", f"# events ({year})"),
    # Histogram("LooseMuonsSegmentMatch_tkRelIso", "", False,  True, default_norm,
    #           20, -0.1, 8.0, 1e-2, 1e6, "Loose #mu track Rel Iso", f"# events ({year})"),

    # Histogram("LooseMuonsVertexSegmentMatch_3Dangle", "", False, True, default_norm,
    #           2, 0, 3.15, 1e-4, 1e8, "#mu vertex 3Dangle", f"# events ({year})"),
    # Histogram("LooseMuonsVertexSegmentMatch_cos3Dangle", "", False, True, default_norm,
    # 2, -1, 1, 1e-4, 1e8, "#mu vertex cos 3Dangle", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Loose DSA muons
    # ----------------------------------------------------------------------------
    # Histogram("LooseDSAMuons_pt", "", False,  True, default_norm, 20, 0, 500,
    #           1e-2, 1e6, "loose dSA #mu p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseDSAMuons_eta", "", False,  True, default_norm, 5, -
    #           3.5, 3.5, 1e0, 1e6, "loose dSA #mu #eta", f"# events ({year})"),
    # Histogram("LooseDSAMuons_dxy", "", False,  True, default_norm, 20, -200,
    #           200, 1e-2, 1e6, "loose dSA #mu d_{xy} [cm]", f"# events ({year})"),
    # Histogram("LooseDSAMuons_dz", "", False,  True, default_norm, 20, -200,
    #           200, 1e-2, 1e6, "loose dSA #mu d_{z} [cm]", f"# events ({year})"),


    # ----------------------------------------------------------------------------
    # Loose electrons
    # ----------------------------------------------------------------------------
    Histogram("LooseElectrons_pt", "", False,  True, default_norm, 10, 0, 500,
              1e-2, 1e6, "loose electron p_{T} [GeV]", f"# events ({year})"),
    Histogram("LooseElectrons_leadingPt", "", False,  True, default_norm, 10, 0, 500,
              1e-2, 1e6, "leading loose electron p_{T} [GeV]", f"# events ({year})"),
    Histogram("LooseElectrons_subleadingPt", "", False,  True, default_norm, 10, 0, 500,
              1e-2, 1e6, "all subleading loose electron p_{T} [GeV]", f"# events ({year})"),
    Histogram("LooseElectrons_eta", "", False,  True, default_norm, 5, -
              3.5, 3.5, 1e-2, 1e6, "loose electron #eta", f"# events ({year})"),
    Histogram("LooseElectrons_dxy", "", False,  True, default_norm, 10, -
              10, 10, 1e-2, 1e6, "loose electron d_{xy}", f"# events ({year})"),
    Histogram("LooseElectrons_dz", "", False,  True, default_norm, 10, -
              10, 10, 1e-2, 1e6, "loose electron d_{z}", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Good jets
    # ----------------------------------------------------------------------------
    Histogram("GoodJets_pt", "", False,  True, default_norm, 10, 0, 1300,
              1e-3, 1e6, "good jet p_{T} [GeV]", f"# events ({year})"),
    Histogram("GoodJets_eta", "", False,  True, default_norm, 10, -
              3, 5.0, 1e-3, 1e6, "good jet #eta", f"# events ({year})"),
    Histogram("GoodJets_btagDeepB", "", False,  True, default_norm, 10, 0,
              1.5, 2e0, 1e8, "good jet deepCSV score", f"# events ({year})"),
    Histogram("GoodJets_btagDeepFlavB", "", False,  True, default_norm, 10,
              0, 1.8, 1e-1, 1e8, "good jet deepJet score", f"# events ({year})"),
    Histogram("GoodJets_minvBjet2jets", "", False,  True, default_norm, 25, 0,
              1500, 1e-1, 1e5, "good jets m_{bjj} [GeV]", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Good b-jets
    # ----------------------------------------------------------------------------
    Histogram("GoodMediumBtaggedJets_pt", "", False,  True, default_norm, 20,
              0, 2000, 1e-3, 1e6, "good b-jet p_{T} [GeV]", f"# events ({year})"),
    Histogram("GoodMediumBtaggedJets_eta", "", False,  True, default_norm,
              5, -3.5, 3.5, 1e-3, 1e6, "good b-jet #eta", f"# events ({year})"),
    Histogram("GoodMediumBtaggedJets_btagDeepB", "", False,  True, default_norm,
              10, -1, 1, 1e0, 1e8, "good b-jet deepCSV score", f"# events ({year})"),
    Histogram("GoodMediumBtaggedJets_btagDeepFlavB", "", False,  True, default_norm,
    10, -1, 1, 1e0, 1e8, "good b-jet deepJet score", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Primary vertices
    # ----------------------------------------------------------------------------
    Histogram("Event_PV_npvs", "", False,  True, default_norm, 1, 0,
              150, 1e-3, 1e12, "# Primary vertices", f"# events ({year})"),
    Histogram("Event_PV_npvsGood", "", False,  True, default_norm, 1, 0,
              80, 1e-4, 1e8, "# Good primary vertices", f"# events ({year})"),
    Histogram("Event_PV_x", "", False, True, default_norm, 1, -0.2, 0.2, 1e-5, 1e10, "PV x [cm]", f"# events ({year})"),
    Histogram("Event_PV_y", "", False, True, default_norm, 1, -0.2, 0.2, 1e-5, 1e10, "PV y [cm]", f"# events ({year})"),
    Histogram("Event_PV_z", "", False, True, default_norm, 50, -10, 10, 1e-2, 1e8, "PV z [cm]", f"# events ({year})"),
    Histogram("Event_PV_chi2" , "", False, True, default_norm , 1, 0, 1.4, 1e-3, 1e6, "PV #chi^{2}", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Muon Trigger Objects
    # ----------------------------------------------------------------------------
    # Histogram("Event_nMuonTriggerObjects", "", False, True, default_norm, 1, 0, 10, 
    #           1e-5, 1e8, "Number of muon trigger objects", f"# events ({year})"),
    # Histogram("MuonTriggerObjects_pt", "", False, True, default_norm, 5, 0, 200, 
    #           1e-5, 1e8, "Muon trigger objects p_{T} [GeV]", f"# events ({year})"),
    # Histogram("MuonTriggerObjects_eta", "", False, True, default_norm, 5, -3, 3, 
    #           1e-5, 1e8, "Muon trigger objects #eta", f"# events ({year})"),
    # Histogram("MuonTriggerObjects_phi", "", False, True, default_norm, 5, -3, 3, 
    #           1e-5, 1e8, "Muon trigger objects #phi", f"# events ({year})"),
    # Histogram("MuonTriggerObjects_hasFilterBits2", "", False, True, default_norm, 1, 
    #           0, 10, 1e-5, 1e8, "Muon trigger objects has filerBits 2", f"# events ({year})"),
    # Histogram("MuonTriggerObjects_minDRTightLooseMuon", "", False, True, default_norm, 1, 
    #           0, 10, 1e-5, 1e8, "min #Delta R (Muon trigger, tight muons)", f"# events ({year})"),
    # Histogram("MuonTriggerObjects_tightLooseMuonMatch0p3", "", False, True, default_norm, 1, 
    #           0, 10, 1e-5, 1e8, "min #Delta R (Muon trigger, tight muons) < 0.3", f"# events ({year})"),
    # Histogram("MuonTriggerObjects_tightLooseMuonMatch0p1", "", False, True, default_norm, 1, 
    #           0, 10, 1e-5, 1e8, "min #Delta R (Muon trigger, tight muons) < 0.1", f"# events ({year})"),
    # Histogram("Event_nLeadingMuonTriggerObject", "", False, True, default_norm, 1, 0, 10, 
    #           1e-5, 1e8, "Number of muon trigger objects", f"# events ({year})"),
    # Histogram("LeadingMuonTriggerObject_pt", "", False, True, default_norm, 5, 0, 200, 
    #           1e-5, 1e8, "Muon trigger objects p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LeadingMuonTriggerObject_eta", "", False, True, default_norm, 5, -3, 3, 
    #           1e-5, 1e8, "Muon trigger objects #eta", f"# events ({year})"),
    # Histogram("LeadingMuonTriggerObject_phi", "", False, True, default_norm, 5, -3, 3, 
    #           1e-5, 1e8, "Muon trigger objects #phi", f"# events ({year})"),
    # Histogram("LeadingMuonTriggerObject_hasFilterBits2", "", False, True, default_norm, 1, 0, 
    #           10, 1e-5, 1e8, "Muon trigger objects has filerBits 2", f"# events ({year})"),
    # Histogram("LeadingMuonTriggerObject_minDRTightLooseMuon", "", False, True, default_norm, 1, 
    #           0, 1, 1e-5, 1e8, "min #Delta R (Muon trigger, tight muons)", f"# events ({year})"),
    # Histogram("LeadingMuonTriggerObject_tightLooseMuonMatch0p3", "", False, True, default_norm, 
    #           1, 0, 2, 1e-5, 1e10, "min #Delta R (Muon trigger, tight muons) < 0.3", f"# events ({year})"),
    # Histogram("LeadingMuonTriggerObject_tightLooseMuonMatch0p1", "", False, True, default_norm, 
    #           1, 0, 2, 1e-5, 1e10, "min #Delta R (Muon trigger, tight muons) < 0.1", f"# events ({year})"),

)

# ----------------------------------------------------------------------------
# Dimuons
# ----------------------------------------------------------------------------

mass_rebin = 200
mass_min = 0.0
mass_max = 70.0

if "JPsiDimuons" in skim[1]:
  mass_rebin = 1
  mass_min = 2.9
  mass_max = 3.3
elif "ZDimuons" in skim[1]:
  mass_rebin = 20
  mass_min = 70.0
  mass_max = 110.0

norm_one = NormalizationType.to_one

for collection, category in product(extraMuonVertexCollections, ("", "_PatDSA", "_DSA", "_Pat")):
  histograms += (
      Histogram("Event_n"+collection + category, "", False, True, default_norm, 1,
                0, 5, 1e0, 1e3, "Number of #mu vertices", f"# events ({year})"),
      Histogram(collection + category+"_invMass", "", False, False, default_norm, mass_rebin,
                mass_min, mass_max, 0, 100, "#mu vertex M_{#mu #mu} [GeV]", f"# events ({year})"),
      # Histogram(collection + category+"_invMass", "", False, True, default_norm, mass_rebin,
      #           mass_min, mass_max, 1e-5, 1e6, "#mu vertex M_{#mu #mu} [GeV]", f"# events ({year})"),
      Histogram(collection + category+"_logInvMass", "", False, True, default_norm, 1, 0.45,
                0.53, 1e-2, 1e6, "#mu vertex log_{10}(M_{#mu #mu} [GeV])", f"# events ({year})"),
      Histogram(collection + category+"_eta", "", False, True, default_norm,
                5, -3.5, 3.5, 1e-3, 1e6, "#mu vertex #eta", f"# events ({year})"),
      Histogram(collection + category+"_pt", "", False, True, default_norm, 50,
                0, 500, 1e-5, 1e5, "#mu vertex p_{T} [GeV]", f"# events ({year})"),
      Histogram(collection + category+"_leadingPt", "", False, True, default_norm, 5,
                0, 200, 1e-3, 1e6, "#mu vertex leading p_{T} [GeV]", f"# events ({year})"),
      Histogram(collection + category+"_subleadingPt", "", False, True, default_norm, 5,
                0, 200, 1e-3, 1e6, "#mu vertex subleading p_{T} [GeV]", f"# events ({year})"),
      Histogram(collection + category+"_leadingEta", "", False, True, default_norm,
                5, -3.5, 3.5, 1e-3, 1e6, "#mu vertex leading #eta", f"# events ({year})"),
      Histogram(collection + category+"_subleadingEta", "", False, True, default_norm,
                5, -3.5, 3.5, 1e-3, 1e6, "#mu vertex subleading #eta", f"# events ({year})"),

      Histogram(collection + category+"_LxySignificance", "", False, True, default_norm, 2,
                0, 200, 1e-3, 1e6, "#mu vertex L_{xy} / #sigma_{Lxy}", f"# events ({year})"),
      Histogram(collection + category+"_Lxy", "", False, True, default_norm, 100,
                0, 300, 1e-4, 1e5, "#mu vertex L_{xy} [cm]", f"# events ({year})"),
      Histogram(collection + category+"_LxySigma", "", False, True, default_norm, 1,
                0, 1.4, 1e-3, 1e6, "#mu vertex #sigma_{Lxy} [cm]", f"# events ({year})"),
      # Histogram(collection + category+"_vxySigma", "", False, True, default_norm, 1,
      #           0, 0.5, 1e-3, 1e6, "#mu vertex #sigma_{Vxy} [cm]", f"# events ({year})"),
      # Histogram(collection + category+"_vxErr", "", False, True, default_norm, 1,
      #           0, 2, 1e-3, 1e6, "#mu vertex #sigma_{Vx} [cm]", f"# events ({year})"),
      # Histogram(collection + category+"_vyErr", "", False, True, default_norm, 1,
      #           0, 2, 1e-3, 1e6, "#mu vertex #sigma_{Vy} [cm]", f"# events ({year})"),
      # Histogram(collection + category+"_vzErr", "", False, True, default_norm, 1,
      #           0, 2, 1e-3, 1e6, "#mu vertex #sigma_{Vz} [cm]", f"# events ({year})"),

      Histogram(collection + category+"_deltaIso03", "", False, True, default_norm, 1, 0,
                0.1, 1e-6, 2e2, "#Delta Iso_{0.3}(#mu_{1}, #mu_{2})", f"# events ({year})"),
      Histogram(collection + category+"_deltaIso04", "", False, True, default_norm, 1, 0,
                0.1, 1e-6, 2e2, "#Delta Iso_{0.4}(#mu_{1}, #mu_{2})", f"# events ({year})"),
      Histogram(collection + category+"_logDeltaIso03", "", False, False, default_norm, 1, -
                3, 1, 1e-6, 500, "log(#Delta Iso_{0.3}(#mu_{1}, #mu_{2}))", f"# events ({year})"),
      Histogram(collection + category+"_logDeltaIso04", "", False, False, default_norm, 1, -
                3, 1, 1e-6, 500, "log(#Delta Iso_{0.4}(#mu_{1}, #mu_{2}))", f"# events ({year})"),

      Histogram(collection + category+"_deltaSquaredIso03", "", False, True, default_norm, 10,
                0, 2, 1e-6, 1e6, "#Delta^{2} Iso_{0.3}(#mu_{1}, #mu_{2})", f"# events ({year})"),
      Histogram(collection + category+"_deltaSquaredIso04", "", False, True, default_norm, 10,
                0, 2, 1e-6, 1e6, "#Delta^{2} Iso_{0.4}(#mu_{1}, #mu_{2})", f"# events ({year})"),
      Histogram(collection + category+"_logDeltaSquaredIso03", "", False, False, default_norm, 20, -
                5, 1, 1e-6, 40, "log(#Delta^{2} Iso_{0.3}(#mu_{1}, #mu_{2}))", f"# events ({year})"),
      Histogram(collection + category+"_logDeltaSquaredIso04", "", False, False, default_norm, 20, -
                5, 1, 1e-6, 40, "log(#Delta^{2} Iso_{0.4}(#mu_{1}, #mu_{2}))", f"# events ({year})"),

      # Histogram(collection + category+"_normChi2", "", False, True, default_norm,
      #           100, 0, 5, 1e-5, 1e4, "#mu vertex #chi^{2}/ndof", f"# events ({year})"),
      # Histogram(collection + category+"_maxHitsInFrontOfVert", "", False, True, default_norm,
      #           1, 0, 35, 1e-6, 1e6, "Max N(hits before vertex)", f"# events ({year})"),
      # Histogram(collection + category+"_dca", "", False, True, default_norm,
      #           10, 0, 10, 1e-6, 1e6, "DCA [cm]", f"# events ({year})"),
      # Histogram(collection + category+"_absCollinearityAngle", "", False, True, default_norm,
      #           10, 0, 3.15, 1e-6, 1e6, "#mu vertex |#Delta #Phi|", f"# events ({year})"),
      # Histogram(collection + category+"_3Dangle", "", False, True, default_norm,
      #           2, 0, 3.15, 1e-5, 1e7, "#mu vertex 3Dangle", f"# events ({year})"),
      # Histogram(collection + category+"_cos3Dangle", "", False, True, default_norm,
      #           2, -1, 1, 1e-5, 1e7, "#mu vertex cos 3Dangle", f"# events ({year})"),
      # Histogram(collection + category+"_absPtLxyDPhi1", "", False, True, default_norm, 10,
      #           0, 3.15, 1e-4, 1e5, "#mu vertex |#Delta #phi_{#mu1}|", f"# events ({year})"),
      # Histogram(collection + category+"_pfRelIso04all1", "", False, True, default_norm, 4, 0,
      #           10, 1e-3, 1e6, "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )", f"# events ({year})"),
      # Histogram(collection + category+"_pfRelIso04all2", "", False, True, default_norm, 4, 0,
      #           10, 1e-3, 1e6, "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )", f"# events ({year})"),
      # Histogram(collection + category+"_chargeProduct", "", False, True, default_norm,
      #           1, 0, 2, 1e-6, 1e6, "#mu vertex charge", f"# events ({year})"),

  )

for collection in genMuonVertexCollections:
  for category in ["_PatDSA", "_DSA", "_Pat"]:
    histograms += (
        Histogram("Event_n"+collection + category, "", False, True, default_norm,
                  1, 0, 5, 1e-3, 1e6, "Number of #mu vertices", f"# events ({year})"),
    )


muonMatchingRatiosVertexCollections = [
  # "BestDimuonVertex",
  # "BestDimuonVertex2over3",
]

for collection in muonMatchingRatiosVertexCollections:
  for category1 in ("_Pat", "_PatDSA", "_DSA"):
    for category2 in ("_Pat", "_PatDSA", "_DSA"):
      histograms += (
        Histogram("Event_n"+collection + category1 + category2 , "", False, False, default_norm, 1,
                  0, 5, 0, 10, "Number of #mu vertices", f"# events ({year})"),
        Histogram(collection + category1 + category2 +"_invMass", "", False, False, default_norm, mass_rebin,
                  mass_min, mass_max, 0, 20, "#mu vertex M_{#mu #mu} [GeV]", f"# events ({year})"),


