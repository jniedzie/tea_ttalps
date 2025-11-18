import ROOT
import os
from itertools import product

from Sample import SampleType
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from TTAlpsPlotterConfigHelper import TTAlpsPlotterConfigHelper
from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms/"

skim = ("skimmed_looseSemimuonic_v3_SR", "_JPsiDimuons", "", "SR")

# skim = ("skimmed_looseSemimuonic_v2_SR", "_ZDimuons", "")
# skim = ("skimmed_looseSemimuonic_v3_ttbarCR", "", "", "ttCR")

hist_path = f"histograms{skim[1]}{skim[2]}"
# hist_path = f"histograms_noDimuonEffSFs{skim[1]}{skim[2]}"

output_formats = ["pdf"]

output_path = (
    f"../plots/plots_{year}/{skim[0].replace('skimmed_', '')}_"
    f"{hist_path.replace('histograms_', '').replace('histograms', '')}/"
)

lumi_label_offset = 0.02
lumi_label_value = luminosity

canvas_size = (800, 600)
canvas_size_2Dhists = (800, 800)
show_ratio_plots = True
ratio_limits = (0.0, 3.0)

# only plot backgrounds with N_entries > bkgRawEventsThreshold
bkgRawEventsThreshold = -1 

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Private Work"

extraMuonVertexCollections = [
    # "BestDimuonVertex",       # best Dimuon selection without isolation cut
    # "BestPFIsoDimuonVertex",  # best Dimuon selection with isolation cut
    # "GoodPFIsoDimuonVertex",  # all Good Dimuons with isolation cut
    # "LooseNonLeadingMuonsVertexSegmentMatch",  # All dimuon vertices before selection
    # "BestPFIsoDimuonVertexNminus1PFRelIsolationCut",
]

plot_background = True
if not plot_background:
  output_path = (
      f"../plots/plots_{year}/{skim[0].replace('skimmed_', '')}_"
      f"{hist_path.replace('histograms_', '').replace('histograms', '')}_noBkg/"
  )

data_to_include = []

if skim[3] != "SR":
  year_number = "".join(filter(str.isdigit, year))
  if "2022" in year or "2023" in year:
    data_to_include = [f"Muon{year_number}"]
  else:
    data_to_include = [f"SingleMuon{year_number}"]

if len(data_to_include) == 0:
  show_ratio_plots = False

signals_to_include = [
    # "tta_mAlp-0p35GeV_ctau-1e1mm",

    # # "tta_mAlp-2GeV_ctau-1e-5mm",
    # # "tta_mAlp-2GeV_ctau-1e0mm",
    # "tta_mAlp-2GeV_ctau-1e1mm",
    # # "tta_mAlp-2GeV_ctau-1e2mm",
    # # "tta_mAlp-2GeV_ctau-1e3mm",

    # "tta_mAlp-12GeV_ctau-1e1mm",
    # # "tta_mAlp-12GeV_ctau-1e0mm",

    # "tta_mAlp-30GeV_ctau-1e1mm",
    # "tta_mAlp-60GeV_ctau-1e1mm",

]

legend_max_x = 0.82 if show_ratio_plots else 0.75
legend_max_y = 0.89
legend_width = 0.17 if show_ratio_plots else 0.15
legend_height = 0.045 if show_ratio_plots else 0.035

configHelper = TTAlpsPlotterConfigHelper(
    year,
    base_path,
    skim,
    hist_path,
    data_to_include,
    signals_to_include,
    (legend_max_x, legend_max_y, legend_width, legend_height)
)

samples = []
configHelper.add_samples(SampleType.data, samples)
configHelper.add_samples(SampleType.signal, samples)
if plot_background:
  configHelper.add_samples(SampleType.background, samples)

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
    Histogram("cutFlow", "", False,  True, default_norm, 1, 0, 20, 1e1, 1e15, "Selection", "Number of events"),
    Histogram("Event_normCheck", "", False,  True, default_norm, 1,
              0, 1, 1e-2, 1e7, "norm check", f"# events ({year})"),
    Histogram("Event_isData", "", False,  True, default_norm, 1, 0,
              2, 1e-8, 1e7, "Is Data Event", f"# events ({year})"),
    Histogram("Event_MET_pt", "", False,  True, default_norm, 10, 0,
              800, 1e-8, 1e9, "MET p_{T} [GeV]", f"# events ({year})"),
    Histogram("Event_nTightMuons", "", False,  True, default_norm, 1, 0,
              10, 1e1, 1e9, "Number of tight #mu", f"# events ({year})"),
    # Histogram("Event_nLoosePATMuons", "", False,  True, default_norm, 1,
    #           0, 10, 1e1, 1e9, "Number of loose #mu", f"# events ({year})"),
    # Histogram("Event_nLooseDSAMuons", "", False,  True, default_norm, 1, 0,
    #           10, 1e1, 1e9, "Number of loose dSA #mu", f"# events ({year})"),
    # Histogram("Event_nLooseElectrons", "", False,  True, default_norm, 1, 0,
    #           10, 1e1, 1e9, "Number of loose electrons", f"# events ({year})"),
    Histogram("Event_nGoodJets", "", False,  True, default_norm, 1, 2,
              16, 1e-2, 1e10, "Number of good jets", f"# events ({year})"),
    Histogram("Event_nGoodMediumBtaggedJets", "", False,  True, default_norm,
              1, 0, 20, 1e0, 1e9, "Number of good b-jets", f"# events ({year})"),
    # ----------------------------------------------------------------------------
    # Tight muons
    # ----------------------------------------------------------------------------
    Histogram("TightMuons_pt", "", False,  True, default_norm, 50, 0,
              1000, 1e-6, 1e8, "tight #mu p_{T} [GeV]", f"# events ({year})"),
    Histogram("TightMuons_leadingPt", "", False,  True, default_norm, 50, 0, 1000,
              1e-5, 1e5, "leading tight #mu p_{T} [GeV]", f"# events ({year})"),
    # Histogram("TightMuons_subleadingPt", "", False,  True, default_norm, 50, 0, 1000,
    #           1e-5, 1e4, "all subleading tight #mu p_{T} [GeV]", f"# events ({year})"),
    Histogram("TightMuons_eta", "", False,  True, default_norm, 10, -
              3.0, 5.0, 1e-3, 1e6, "tight #mu #eta", f"# events ({year})"),
    Histogram("TightMuons_dxy", "", False,  True, default_norm, 2, -0.5,
              0.5, 1e-2, 1e10, "tight #mu d_{xy} [cm]", f"# events ({year})"),
    # Histogram("TightMuons_dz", "", False,  True, default_norm, 2, -1,
    #           1, 1e-2, 1e8, "tight #mu d_{z} [cm]", f"# events ({year})"),
    # Histogram("TightMuons_pfRelIso04_all", "", False,  True, default_norm, 1, 0.0,
    #           0.2, 1e-2, 1e6, "tight #mu PF Rel Iso 0.4 (all)", f"# events ({year})"),
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
    # Histogram("LooseMuonsSegmentMatch_pt", "", False,  True, default_norm, 1,
    #           0, 100, 1e-2, 1e6, "loose #mu p_{T} [GeV]", f"# events ({year})"),
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

    # Histogram("LooseMuonsSegmentMatch_logAbsDzFromLeadingTight", "", False,  True, default_norm,
    #           100, -5, 3, 1e-2, 1e6, "|#Delta z(Loose #mu, Tight #mu_{1})|", f"# events ({year})"),

    # Histogram("LooseMuonsVertexSegmentMatch_3Dangle", "", False, True, default_norm,
    #           2, 0, 3.15, 1e-4, 1e8, "#mu vertex 3Dangle", f"# events ({year})"),
    # Histogram("LooseMuonsVertexSegmentMatch_cos3Dangle", "", False, True, default_norm,
    # 2, -1, 1, 1e-4, 1e8, "#mu vertex cos 3Dangle", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Loose DSA muons
    # ----------------------------------------------------------------------------
    # Histogram("LooseDSAMuonsSegmentMatch_pt", "", False,  True, default_norm, 40, 0, 600,
    #           1e-4, 1e10, "loose dSA #mu p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_pt_irr", "", False,  True, default_norm, 1, 0, 2000,
    #           1e-5, 1e10, "loose dSA #mu p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_pt_irr2", "", False,  True, default_norm, 1, 0, 600,
    #           1e-5, 1e10, "loose dSA #mu p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_absDxyPVTraj", "", False,  True, default_norm, 50, 0,
    #           500, 1e-2, 1e12, "loose dSA #mu |d_{xy}| [cm]", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_absDxyPVTraj_irr", "", False,  True, default_norm, 1, 0,
    #           700, 1e-2, 1e12, "loose dSA #mu |d_{xy}| [cm]", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_eta", "", False,  True, default_norm, 5, -3, 3,
    #           1e-2, 1e10, "loose dSA #mu #eta", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_ptErr", "", False,  True, default_norm, 20, 0, 2000,
    #           1e-5, 1e8, "loose dSA #mu #sigma p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_outerEta", "", False,  True, default_norm, 5, -
    #           3.5, 3.5, 1e-2, 1e10, "loose dSA #mu outer #eta", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_phi", "", False,  True, default_norm, 5, -
    #           3.5, 3.5, 1e-2, 1e10, "loose dSA #mu #phi", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_outerPhi", "", False,  True, default_norm, 5, -
    #           3.5, 3.5, 1e-2, 1e10, "loose dSA #mu outer #phi", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_normChi2", "", False,  True, default_norm, 50, 0,
    #           2.5, 1e-2, 1e10, "loose dSA #mu #chi^{2}/ndof", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_nSegments", "", False,  True, default_norm, 1, 0,
    #           20, 1e-2, 1e10, "loose dSA #mu segments", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_nDTSegments", "", False,  True, default_norm, 1, 0,
    #           20, 1e-2, 1e10, "loose dSA #mu DT segments", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_nCSCSegments", "", False,  True, default_norm, 1, 0,
    #           20, 1e-2, 1e10, "loose dSA #mu CSC segments", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_logAbsDzFromLeadingTight", "", False,  True, default_norm, 50, -5,
    #           3, 1e-2, 1e10, "loose dSA #mu log |#Delta z(#mu_{DSA}, #mu_{tight} |", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_trkNumPlanes", "", False,  True, default_norm, 1, 0,
    #           20, 1e-2, 1e10, "loose dSA #mu track planes", f"# events ({year})"),
    # Histogram("LooseDSAMuonsSegmentMatch_trkNumHits", "", False,  True, default_norm, 1, 0,
    #           50, 1e-2, 1e10, "loose dSA #mu track hits", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Loose electrons
    # ----------------------------------------------------------------------------
    # Histogram("LooseElectrons_pt", "", False,  True, default_norm, 10, 0, 500,
    #           1e-2, 1e6, "loose electron p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseElectrons_leadingPt", "", False,  True, default_norm, 10, 0, 500,
    #           1e-2, 1e6, "leading loose electron p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseElectrons_subleadingPt", "", False,  True, default_norm, 10, 0, 500,
    #           1e-2, 1e6, "all subleading loose electron p_{T} [GeV]", f"# events ({year})"),
    # Histogram("LooseElectrons_eta", "", False,  True, default_norm, 5, -
    #           3.5, 3.5, 1e-2, 1e6, "loose electron #eta", f"# events ({year})"),
    # Histogram("LooseElectrons_dxy", "", False,  True, default_norm, 10, -
    #           10, 10, 1e-2, 1e6, "loose electron d_{xy}", f"# events ({year})"),
    # Histogram("LooseElectrons_dz", "", False,  True, default_norm, 10, -
    #           10, 10, 1e-2, 1e6, "loose electron d_{z}", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Good jets
    # ----------------------------------------------------------------------------
    Histogram("GoodJets_pt", "", False,  True, default_norm, 10, 0, 1300,
              1e-3, 1e6, "good jet p_{T} [GeV]", f"# events ({year})"),
    Histogram("GoodJets_eta", "", False,  True, default_norm, 10, -
              3, 5.0, 1e-3, 1e6, "good jet #eta", f"# events ({year})"),
    # Histogram("GoodJets_btagDeepB", "", False,  True, default_norm, 10, 0,
    #           1.5, 2e0, 1e8, "good jet deepCSV score", f"# events ({year})"),
    # Histogram("GoodJets_btagDeepFlavB", "", False,  True, default_norm, 10,
    #           0, 1.8, 1e-1, 1e8, "good jet deepJet score", f"# events ({year})"),
    # Histogram("GoodJets_minvBjet2jets", "", False,  True, default_norm, 25, 0,
    #           1500, 1e-1, 1e5, "good jets m_{bjj} [GeV]", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Good b-jets
    # ----------------------------------------------------------------------------
    Histogram("GoodMediumBtaggedJets_pt", "", False,  True, default_norm, 20,
              0, 2000, 1e-3, 1e6, "good b-jet p_{T} [GeV]", f"# events ({year})"),
    Histogram("GoodMediumBtaggedJets_eta", "", False,  True, default_norm,
              5, -3.5, 3.5, 1e-3, 1e6, "good b-jet #eta", f"# events ({year})"),
    # Histogram("GoodMediumBtaggedJets_btagDeepB", "", False,  True, default_norm,
    #           10, -1, 1, 1e0, 1e8, "good b-jet deepCSV score", f"# events ({year})"),
    # Histogram("GoodMediumBtaggedJets_btagDeepFlavB", "", False,  True, default_norm,
    # 10, -1, 1, 1e0, 1e8, "good b-jet deepJet score", f"# events ({year})"),

    # ----------------------------------------------------------------------------
    # Primary vertices
    # ----------------------------------------------------------------------------
    # Histogram("Event_PV_npvs", "", False,  True, default_norm, 1, 0,
    #           150, 1e-3, 1e12, "# Primary vertices", f"# events ({year})"),
    # Histogram("Event_PV_npvsGood", "", False,  True, default_norm, 1, 0,
    #           80, 1e-4, 1e8, "# Good primary vertices", f"# events ({year})"),
    # Histogram("Event_PV_x", "", False, True, default_norm, 1, -0.2, 0.2, 1e-5, 1e10, "PV x [cm]", f"# events ({year})"),
    # Histogram("Event_PV_y", "", False, True, default_norm, 1, -0.2, 0.2, 1e-5, 1e10, "PV y [cm]", f"# events ({year})"),
    # Histogram("Event_PV_z", "", False, True, default_norm, 50, -10, 10, 1e-2, 1e8, "PV z [cm]", f"# events ({year})"),
    # Histogram("Event_PV_chi2" , "", False, True, default_norm , 1, 0, 1.4, 1e-3, 1e6, "PV #chi^{2}", f"# events ({year})"),

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

categories = ("", "_PatDSA", "_DSA", "_Pat")
mass_rebin = {c: 5   for c in categories}
mass_min   = {c: 2.0 for c in categories}
mass_max   = {c: 5.0 for c in categories}
mass_y_max = {c: 200 for c in categories}

if "JPsiDimuons" in skim[1]:
  # mass_rebin["_DSA"] = 10
  # mass_min["_DSA"]   = 2.3
  # mass_max["_DSA"]   = 4.0
  # mass_y_max["_DSA"] = 4
  mass_rebin["_DSA"] = 10
  mass_min["_DSA"]   = 1
  mass_max["_DSA"]   = 5.0
  mass_y_max["_DSA"] = 50
  # mass_rebin["_PatDSA"] = 4
  # mass_min["_PatDSA"]   = 2.6
  # mass_max["_PatDSA"]   = 3.8
  # mass_y_max["_PatDSA"] = 6
  mass_rebin["_PatDSA"] = 5
  mass_min["_PatDSA"]   = 2.5
  mass_max["_PatDSA"]   = 3.9
  mass_y_max["_PatDSA"] = 70
  mass_rebin["_Pat"] = 1
  mass_min["_Pat"]   = 2.9
  mass_max["_Pat"]   = 3.3
  mass_y_max["_Pat"] = 200

norm_one = NormalizationType.to_one

for collection, category in product(extraMuonVertexCollections, categories):
  histograms += (
      Histogram("Event_n"+collection + category, "", False, True, default_norm, 1,
                0, 30, 1e-4, 1e1, "Number of #mu vertices", f"# events ({year})"),
      Histogram("dimuonCutFlow_"+collection + category, "", False,  True,
                default_norm, 1, 0, 10, 1e-2, 1e9, "Selection", "Number of events"),
      Histogram(collection + category+"_invMass", "", False, False, default_norm, mass_rebin[category],
                mass_min[category], mass_max[category], 0, mass_y_max[category], "#mu vertex M_{#mu #mu} [GeV]", f"# events ({year})"),
      # Histogram(collection + category+"_invMassJPsiBin", "", False, False, default_norm,
      #           1, 2.2, 4.0, 0, 30, "#mu vertex M_{#mu #mu} [GeV]", f"# events ({year})"),
      # Histogram(collection + category+"_logInvMass", "", False, True, default_norm, 15, -0.7, 1.9,
      #           1e-2, 1e5, "Dimuon vertex log_{10}(M_{#mu #mu} [GeV])", f"# events ({year})"),
      # Histogram(collection + category+"_eta", "", False, True, default_norm, 5, -
      #           3.5, 3.5, 1e-2, 1e6, "Dimuon vertex #eta", f"# events ({year})"),
      # Histogram(collection + category+"_pt", "", False, True, default_norm, 20, 0,
      #           500, 1e-2, 1e5, "#mu vertex p_{T} [GeV]", f"# events ({year})"),
      # # Histogram(collection + category+"_muonPt", "", False, True, default_norm, 20, 0, 500, 1e-2, 1e5, "Dimuon vertex #mu p_{T} [GeV]", f"# events ({year})"),
      # Histogram(collection + category+"_muonPtErr", "", False, True, default_norm, 2, 0,
      #           50, 1e-2, 1e5, "Dimuon vertex #mu #sigma_{pT} [GeV]", f"# events ({year})"),
      # Histogram(collection + category+"_leadingPt", "", False, True, default_norm, 20, 0,
      #           500, 1e-2, 1e6, "#mu vertex leading p_{T} [GeV]", f"# events ({year})"),

      # Histogram(collection + category+"_LxySignificance", "", False, True, default_norm, 1, 0,
      #           20, 1e-4, 1e6, "Dimuon vertex L_{xy} / #sigma_{Lxy}", f"# events ({year})"),
      # Histogram(collection + category+"_Lxy", "", False, True, default_norm, 400, 0,
      #           500, 1e-4, 1e6, "Dimuon vertex L_{xy} [cm]", f"# events ({year})"),
      # Histogram(collection + category+"_absDxyPVTraj1", "", False, True, default_norm, 100,
      #           0, 100, 1e-4, 1e6, "Dimuon vertex |d_{xy}^{#mu1}|", f"# events ({year})"),
      # Histogram(collection + category+"_absDxyPVTraj2", "", False, True, default_norm, 100,
      #           0, 100, 1e-4, 1e6, "Dimuon vertex |d_{xy}^{#mu1}|", f"# events ({year})"),
      # # Histogram(collection + category+"_dxyPVTrajSig1", "", False, True, default_norm, 1, 0, 30, 1e-4, 1e6, "Dimuon vertex d_{xy}^{#mu1} / #sigma_{dxy}^{#mu1}", f"# events ({year})"),
      # # Histogram(collection + category+"_dxyPVTrajSig2", "", False, True, default_norm, 1, 0, 30, 1e-4, 1e6, "Dimuon vertex d_{xy}^{#mu2} / #sigma_{dxy}^{#mu2}", f"# events ({year})"),
      # # Histogram(collection + category+"_LxySigma", "", False, True, default_norm, 200, 0, 100, 1e-5, 1e6, "#mu vertex #sigma_{Lxy} [cm]", f"# events ({year})"),

      # Histogram(collection + category+"_nSegments", "", False, True, default_norm,
      #           1, 0, 20, 1e-3, 1e8, "#mu vertex N(segments)", f"# events ({year})"),

      # Histogram(collection + category+"_dR", "", False, True, default_norm, 5,
      #           0, 3.15, 1e-2, 1e6, "#mu vertex #Delta R", f"# events ({year})"),
      # # Histogram(collection + category+"_proxDR", "", False, True, default_norm, 1, 0, 3.15, 1e-3, 1e6, "#mu vertex proximity #Delta R", f"# events ({year})"),
      # Histogram(collection + category+"_outerDR", "", False, True, default_norm, 3, 0,
      #           3.15, 1e-3, 1e7, "#mu vertex outer #Delta R", f"# events ({year})"),
      # # Histogram(collection + category+"_logOuterDR", "", False, True, default_norm, 10, -2, 1, 1e-3, 1e7, "#mu vertex log outer #Delta R", f"# events ({year})"),
      # # Histogram(collection + category+"_dEta", "", False, True, default_norm, 1, 0, 3.15, 1e-3, 1e6, "#mu vertex #Delta #eta", f"# events ({year})"),
      # # Histogram(collection + category+"_dPhi", "", False, True, default_norm, 1, 0, 3.15, 1e-3, 1e6, "#mu vertex #Delta #phi", f"# events ({year})"),

      # Histogram(collection + category+"_displacedTrackIso03Dimuon1", "", False, True,
      #           default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.3}(#mu_{1})", f"# events ({year})"),
      # Histogram(collection + category+"_displacedTrackIso03Dimuon2", "", False, True,
      #           default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.3}(#mu_{2})", f"# events ({year})"),
      # # Histogram(collection + category+"_displacedTrackIso04Dimuon1", "", False, True, default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.4}(#mu_{1})", f"# events ({year})"),
      # # Histogram(collection + category+"_displacedTrackIso04Dimuon2", "", False, True, default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.4}(#mu_{2})", f"# events ({year})"),
      # # Histogram(collection + category+"_displacedTrackIso03Muon1", "", False, True, default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.3}(#mu_{1})", f"# events ({year})"),
      # # Histogram(collection + category+"_displacedTrackIso03Muon2", "", False, True, default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.3}(#mu_{2})", f"# events ({year})"),
      # # Histogram(collection + category+"_displacedTrackIso04Muon1", "", False, True, default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.4}(#mu_{1})", f"# events ({year})"),
      # # Histogram(collection + category+"_displacedTrackIso04Muon2", "", False, True, default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.4}(#mu_{2})", f"# events ({year})"),

      # Histogram(collection + category+"_normChi2", "", False, True, default_norm, 100,
      #           0, 5, 1e-4, 1e5, "Dimuon vertex #chi^{2}/ndof", f"# events ({year})"),
      # # Histogram(collection + category+"_maxHitsInFrontOfVert", "", False, True, default_norm, 1, 0, 35, 1e-4, 1e6, "Max N(hits before vertex)", f"# events ({year})"),
      # Histogram(collection + category+"_sumHitsInFrontOfVert", "", False, True, default_norm,
      #           1, 0, 35, 1e-4, 1e6, "Sum N(hits before vertex)", f"# events ({year})"),
      # Histogram(collection + category+"_dca", "", False, True, default_norm,
      #           20, 0, 15, 1e-4, 1e5, "Dimuon DCA [cm]", f"# events ({year})"),
      # Histogram(collection + category+"_absCollinearityAngle", "", False, True, default_norm, 10,
      #           0, 3.15, 1e-4, 1e6, "Dimuon vertex |#Delta #Phi_{coll}|", f"# events ({year})"),
      # # Histogram(collection + category+"_3Dangle", "", False, True, default_norm, 5, 0, 3.15, 1e-3, 1e8, "#mu vertex 3Dangle", f"# events ({year})"),
      # # Histogram(collection + category+"_cos3Dangle", "", False, True, default_norm, 5, -1, 1, 1e-3, 1e8, "#mu vertex cos 3Dangle", f"# events ({year})"),
      # Histogram(collection + category+"_absPtLxyDPhi1", "", False, True, default_norm, 10,
      #           0, 3.15, 1e-3, 1e6, "#mu vertex |#Delta #phi_{#mu1}|", f"# events ({year})"),
      # Histogram(collection + category+"_absPtLxyDPhi2", "", False, True, default_norm, 10,
      #           0, 3.15, 1e-3, 1e6, "#mu vertex |#Delta #phi_{#mu2}|", f"# events ({year})"),
      # # Histogram(collection + category+"_pfRelIso04all1", "", False, True, default_norm, 4, 0, 10, 1e-3, 1e6, "#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )", f"# events ({year})"),
      # # Histogram(collection + category+"_pfRelIso04all2", "", False, True, default_norm, 4, 0, 10, 1e-3, 1e6, "#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )", f"# events ({year})"),
      # Histogram(collection + category+"_chargeProduct", "", False, True, default_norm,
      #           1, -1, 2, 1e-1, 1e7, "Dimuon vertex charge", f"# events ({year})"),
  )

  muonQualityFlags = []
  # muonQualityFlags = ["PU", "fake", "real"]  # uncomment to include plots
  for flag in muonQualityFlags:
    histograms += (
        Histogram("Event_n" + collection + category + "_" + flag, "", False, True, default_norm, 1,
                  0, 2, 1e0, 1e5, f"#mu is {flag}", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_absDzFromLeadingTight", "", True, True, default_norm, 1,
                  1e-5, 1e3, 1e-4, 1e2, f"{flag} #mu |#DeltaZ(leading tight #mu)|", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_logAbsDzFromLeadingTight", "", False, True, default_norm, 50,
                  -5, 3, 1e-4, 1e2, f"{flag} #mu log |#DeltaZ(leading tight #mu)|", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_genMuonDR", "", False, True, default_norm, 1,
                  0, 0.1, 1e-4, 1e2, f"{flag} #mu #DeltaR(gen #mu)", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_normChi2", "", False, True, default_norm, 40,
                  0, 3, 1e-4, 1e2, f"{flag} #mu #chi^{2}/ndof", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_nSegments", "", False, True, default_norm, 1,
                  0, 20, 1e-2, 1e6, f"{flag} #mu segments", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_nDTSegments", "", False, True, default_norm, 1,
                  0, 20, 1e-4, 1e2, f"{flag} #mu DT segments", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_nCSCSegments", "", False, True, default_norm, 1,
                  0, 20, 1e-4, 1e2, f"{flag} #mu CSC segments", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_trkNumPlanes", "", False, True, default_norm, 1,
                  0, 6, 1e-2, 1e6, f"{flag} #mu track planes", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_trkNumHits", "", False, True, default_norm, 1,
                  0, 70, 1e-2, 1e6, f"{flag} #mu track hits", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_eta", "", False, True, default_norm, 10,
                  -3, 3, 1e-4, 1e2, f"{flag} #mu #eta", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_etaErr", "", False, True, default_norm, 10,
                  -3, 3, 1e-4, 1e2, f"{flag} #mu #sigma_#eta", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_pt", "", False, True, default_norm, 10,
                  0, 300, 1e-3, 1e5, f"{flag} #mu p_T", f"# events ({year})"),
        Histogram(collection + category + "_" + flag + "_ptErr", "", False, True, default_norm, 10,
                  0, 300, 1e-3, 1e5, f"{flag} #mu #sigma p_T", f"# events ({year})"),

    )
