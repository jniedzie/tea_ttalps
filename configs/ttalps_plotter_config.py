import ROOT
import os
from itertools import product

from Sample import SampleType
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from TTAlpsPlotterConfigHelper import TTAlpsPlotterConfigHelper
from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity

# years = ["2018",]
# years = ["2017","2018",]
years = ["2016preVFP", "2016postVFP", "2017", "2018", "2022preEE", "2022postEE", "2023preBPix", "2023postBPix",]
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
luminosity_run2 = 0
luminosity_run3 = 0
year_output_str = ""
for year in years:
  lumi = get_luminosity(year)
  if "2016" in year or "2017" in year or "2018" in year:
    luminosity_run2 += lumi
  else:
    luminosity_run3 += lumi
  year_output_str += year

year_str = ""
if len(years) == 1:
  year_str = f"({years[0]})"

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms/"

# skim = ("skimmed_looseSemimuonic_v3_merged", "", "_genALPs_ANv6", "SR")

skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_ABCD_ANv5", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_ABCD_ANv10_regionA", "SR")
# # skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_genInfo_ABCD_ANv3", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_genALPs_ANv6", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_nminus1", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuonsNoChi2", "_genInfo", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_ABCD_ANv5_regionD_2", "SR")

# skim = ("skimmed_looseSemimuonic_v3_SR", "_JPsiDimuons", "_noDimuonEffSFs_ABCD_ANv3", "ttJPsiCR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_JPsiDimuonsPatDSA", "_noDimuonEffSFs_noMatching_ABCD_ANv3", "ttJPsiCR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_JPsiDimuons", "_noDimuonEffSFs_nminus1", "ttJPsiCR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_JPsiDimuons", "_noDimuonEffSFs_revertedMatching_ABCD_ANv3", "ttJPsiCR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_JPsiDimuons", "_noDimuonEffSFs_revertedMatching_nminus1", "ttJPsiCR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_noDimuonEffSFs_revertedMatching_ABCD", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_SSDimuons", "_ABCD_ANv3", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_SSDimuons", "_ABCD_ANv5", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_DCADimuons", "_ABCD_ANv5", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_Chi2Dimuons", "_ABCD_ANv5", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "_HighIsoDimuons", "_ABCD_ANv5", "SR")
# skim = ("skimmed_looseSemimuonic_v3_ttbarCR", "", "_ANv3", "SR")

# data_skim = skim
data_skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_ABCD_ANv10_regionABCD", "SR")
# data_skim = ("skimmed_looseSemimuonic_v3_SR", "_SRDimuons", "_ABCD_ANv10_regionA", "SR")


hist_path = f"histograms{skim[1]}{skim[2]}"
data_hist_path = f"histograms{data_skim[1]}{data_skim[2]}"

output_formats = ["pdf"]

output_path = (
    f"../plots/plots_{year_output_str}/{skim[0].replace('skimmed_', '')}_"
    f"{hist_path.replace('histograms_', '').replace('histograms', '')}/"
)

minIntegral = 1e-7

lumi_label_offset = 0.02
lumi_label_value_run2 = luminosity_run2
lumi_label_value_run3 = luminosity_run3

canvas_size = (800, 600)
canvas_size_2Dhists = (800, 800)
show_ratio_plots = True
ratio_limits = (0.0, 3.0)
# ratio_limits = (0.5, 1.5)

# only plot backgrounds with N_entries > bkgRawEventsThreshold
bkgRawEventsThreshold = -1

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Work in Progress"
# extraText = "Simulation Work in Progress"
# extraText = "Private Work"

extraMuonVertexCollections = [
    # "BestDimuonVertex",       # best Dimuon selection without isolation cut
    "BestPFIsoDimuonVertex",  # best Dimuon selection with isolation cut
    # "BestPFIsoDimuonVertex_revertedMatching",
    # "BestPFIsoDimuonVertexNminus1CollinearityAngleCutFromALP",
    # "BestPFIsoDimuonVertexNminus1DCACut",
    # "BestPFIsoDimuonVertexNminus1InvariantMassCut",
    # "BestPFIsoDimuonVertexNminus1Chi2Cut",
    # "BestDimuonVertexNminus1InvariantMassCut",
    # "BestDimuonVertex_revertedMatching",
    # "BestPFIsoDimuonVertexFromALP", 
    # "GenDimuonFromALP", 
    # "GenALP", 
]

plot_background = True
if not plot_background:
  output_path = (
      f"../plots/plots_{year}/{skim[0].replace('skimmed_', '')}_"
      f"{hist_path.replace('histograms_', '').replace('histograms', '')}_noBkg/"
  )

data_to_include = {}

if not "SR" in skim[1] or "regionD" in skim[2] or "regionABCD" in data_skim[2] or "regionA" in data_skim[2]:
# if not "SR" in skim[1]:
  if len(years) == 1:
    year_number = "".join(filter(str.isdigit, year))
    if "2022" in year:
      data_to_include = [f"Muon{year_number}"]
    elif "2023" in year:
      data_to_include = [f"Muon1{year_number}"]
    else:
      data_to_include = [f"SingleMuon{year_number}"]
  else:
    data_to_include = [f"SingleMuon{year_output_str}"]

if len(data_to_include) == 0:
  show_ratio_plots = False

use_expected_xsec = False
signals_to_include = [
    # "tta_mAlp-0p35GeV_ctau-1e2mm",
    # "tta_mAlp-2GeV_ctau-1e2mm",
    # "tta_mAlp-12GeV_ctau-1e2mm",
    # "tta_mAlp-30GeV_ctau-1e2mm",
    # "tta_mAlp-60GeV_ctau-1e2mm",

    # "tta_mAlp-2GeV_ctau-1e0mm",
    # "tta_mAlp-2GeV_ctau-1e2mm",
    # "tta_mAlp-12GeV_ctau-1e0mm",

    # "tta_mAlp-2GeV_ctau-1e1mm",
    # "tta_mAlp-12GeV_ctau-1e1mm",
    # "tta_mAlp-30GeV_ctau-1e1mm",

    # # "tta_mAlp-12GeV_ctau-1e-5mm",
    "tta_mAlp-12GeV_ctau-1e0mm",
    "tta_mAlp-12GeV_ctau-1e1mm",
    # # "tta_mAlp-12GeV_ctau-1e2mm",
    "tta_mAlp-12GeV_ctau-1e3mm",
]

legend_max_x = 0.75 if show_ratio_plots else 0.75
if not plot_background:
  legend_max_x = 0.70
legend_max_y = 0.88
legend_width = 0.145 if show_ratio_plots else 0.145
legend_height = 0.05 if show_ratio_plots else 0.035
legend_text_size = 20

configHelper = TTAlpsPlotterConfigHelper(
    years,
    base_path,
    skim,
    hist_path,
    data_to_include,
    signals_to_include,
    (legend_max_x, legend_max_y, legend_width, legend_height),
    legend_text_size=legend_text_size, data_skim=data_skim, data_hist_path=data_hist_path
)

samples = []
configHelper.add_samples(SampleType.data, samples)
configHelper.add_samples(SampleType.signal, samples, use_expected_xsec)
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
# default_norm = NormalizationType.to_one
# default_norm = NormalizationType.to_data
# default_norm = NormalizationType.none

histogramsRatio = []
weightsBranchName = "genWeight"

histograms2D = ()
# histograms = ()
histograms = (
    # # name title logx logy norm_type rebin xmin xmax ymin ymax xlabel ylabel

    # # ----------------------------------------------------------------------------
    # # Event variables
    # # ----------------------------------------------------------------------------
    # Histogram("cutFlow", "", False,  True, default_norm, 1, 0, 15, 1e1, 1e15, "Selection", "Number of events"),
    # Histogram("Event_normCheck", "", False,  True, default_norm, 1,
    #           0, 1, 1e-2, 1e7, "norm check", f"# events {year_str}"),
    # Histogram("Event_isData", "", False,  True, default_norm, 1, 0,
    #           2, 1e-8, 1e7, "Is Data Event", f"# events {year_str}"),
    # # Histogram("Event_MET_pt", "", False,  True, default_norm, 10, 0,
    # #           800, 1e-8, 1e9, "MET p_{T} [GeV]", f"# events {year_str}"),
    # Histogram("Event_MET_pt_corr", "", False,  True, default_norm, 10, 0,
    #           800, 1e-8, 1e9, "MET p_{T} [GeV]", f"Events / 10 GeV"),
    # # Histogram("Event_MET_px", "", False,  True, default_norm, 20, -800,
    # #           800, 1e-6, 1e12, "MET p_{x} [GeV]", f"# events {year_str}"),
    # # Histogram("Event_MET_py", "", False,  True, default_norm, 20, -800,
    # #           800, 1e-6, 1e12, "MET p_{y} [GeV]", f"# events {year_str}"),
    # # Histogram("Event_MET_px_corr", "", False,  True, default_norm, 20, -800,
    # #           800, 1e-6, 1e12, "MET p_{x} [GeV]", f"# events {year_str}"),
    # # Histogram("Event_MET_py_corr", "", False,  True, default_norm, 20, -800,
    # #           800, 1e-6, 1e12, "MET p_{y} [GeV]", f"# events {year_str}"),
    # Histogram("Event_MET_pt_smeared", "", False,  True, default_norm, 5, 0,
    #           200, 1e-8, 1e9, "MET p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("Event_MET_phi", "", False,  True, default_norm, 10, -3,
    # #           3, 1e-8, 1e13, "MET #phi", f"# events {year_str}"),
    # Histogram("Event_MET_phi_corr", "", False,  True, default_norm, 10, -3,
    #           3, 1e-8, 1e13, "MET #phi", f"# events {year_str}"),
    # Histogram("Event_nTightMuons", "", False,  True, default_norm, 1, 0,
    #           10, 1e1, 1e9, "Number of tight #mu", f"Events"),
    # # Histogram("Event_nLoosePATMuons", "", False,  True, default_norm, 1,
    # #           0, 10, 1e1, 1e9, "Number of loose #mu", f"# events {year_str}"),
    # # Histogram("Event_nLooseDSAMuons", "", False,  True, default_norm, 1, 0,
    # #           10, 1e1, 1e9, "Number of loose dSA #mu", f"# events {year_str}"),
    # # Histogram("Event_nLooseElectrons", "", False,  True, default_norm, 1, 0,
    # #           10, 1e1, 1e9, "Number of loose electrons", f"# events {year_str}"),
    # Histogram("Event_nGoodJets", "", False,  True, default_norm, 1, 2,
    #           16, 1e-3, 1e10, "Number of good jets", f"Events"),
    # Histogram("Event_nGoodMediumBtaggedJets", "", False,  True, default_norm,
    #           1, 0, 16, 1e-3, 1e9, "Number of good b-jets", f"Events"),
    # # ----------------------------------------------------------------------------
    # # Tight muons
    # # ----------------------------------------------------------------------------
    # Histogram("TightMuons_pt", "", False,  True, default_norm, 20, 0,
    #           1000, 1e-6, 1e8, "tight #mu p_{T} [GeV]", f"Events / 10 GeV"),
    # Histogram("TightMuons_leadingPt", "", False,  True, default_norm, 50, 0, 1000,
    #           1e-5, 1e5, "leading tight #mu p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("TightMuons_subleadingPt", "", False,  True, default_norm, 50, 0, 1000,
    # #           1e-5, 1e4, "all subleading tight #mu p_{T} [GeV]", f"# events {year_str}"),
    # Histogram("TightMuons_eta", "", False,  True, default_norm, 10, -
    #           3.0, 5.0, 1e-3, 1e10, "tight #mu #eta", f"Events / 0.2"),
    # Histogram("TightMuons_dxy", "", False,  True, default_norm, 2, -0.5,
    #           0.5, 1e-2, 1e10, "tight #mu d_{xy} [cm]", f"# events {year_str}"),
    # # Histogram("TightMuons_dz", "", False,  True, default_norm, 2, -1,
    # #           1, 1e-2, 1e8, "tight #mu d_{z} [cm]", f"# events {year_str}"),
    # # Histogram("TightMuons_pfRelIso04_all", "", False,  True, default_norm, 1, 0.0,
    # #           0.2, 1e-2, 1e6, "tight #mu PF Rel Iso 0.4 (all)", f"# events {year_str}"),
    # # Histogram("TightMuons_pfRelIso03_chg", "", False,  True, default_norm, 1, 0,
    # #           0.5, 1e-2, 1e6, "tight #mu PF Rel Iso 0.3 (chg)", f"# events {year_str}"),
    # # Histogram("TightMuons_pfRelIso03_all", "", False,  True, default_norm, 1, 0,
    # #           0.5, 1e-2, 1e6, "tight #mu PF Rel Iso 0.3 (all)", f"# events {year_str}"),
    # # Histogram("TightMuons_miniPFRelIso_chg", "", False,  True, default_norm, 10, -0.1,
    # #           3.5, 1e-2, 1e6, "tight #mu mini PF Rel Iso (chg)", f"# events {year_str}"),
    # # Histogram("TightMuons_miniPFRelIso_all", "", False,  True, default_norm, 5, -0.1,
    # #           3.5, 1e-2, 1e6, "tight #mu mini PF Rel Iso (all)", f"# events {year_str}"),
    # # Histogram("TightMuons_jetRelIso", "", False,  True, default_norm, 50, -
    # #           1, 8.0, 1e-2, 1e6, "tight #mu jet Rel Iso", f"# events {year_str}"),
    # # Histogram("TightMuons_tkRelIso", "", False,  True, default_norm, 20, -0.1,
    # #           8.0, 1e-2, 1e6, "tight #mu track Rel Iso", f"# events {year_str}"),
    # # Histogram("TightMuons_deltaPhiMuonMET", "", False,  True, default_norm, 20, -4,
    # #           4, 1e0, 1e7, "tight muon #Delta #phi(MET, #mu)", f"# events {year_str}"),
    # # Histogram("TightMuons_minvMuonMET", "", False,  True, default_norm, 40, 0,
    # #           1000, 1e-4, 1e5, "tight muon m_{MET, l} [GeV]", f"# events {year_str}"),

    # # ----------------------------------------------------------------------------
    # # Loose muons
    # # ----------------------------------------------------------------------------
    # # Histogram("LooseMuonsSegmentMatch_pt", "", False,  True, default_norm, 1,
    # #           0, 100, 1e-2, 1e6, "loose #mu p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_leadingPt", "", False,  True, default_norm, 20,
    # #           0, 500, 1e-2, 1e6, "leading loose #mu p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_subleadingPt", "", False,  True, default_norm, 20, 0,
    # #           500, 1e-2, 1e6, "all subleading loose #mu p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_eta", "", False,  True, default_norm,
    # #           5, -3.5, 3.5, 1e0, 1e6, "loose #mu #eta", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_dxy", "", False,  True, default_norm, 20, -
    # #           200, 200, 1e-2, 1e6, "loose #mu d_{xy} [cm]", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_dz", "", False,  True, default_norm, 20, -
    # #           200, 200, 1e-2, 1e6, "loose #mu d_{z} [cm]", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_pfRelIso04_all", "", False,  True, default_norm, 1,
    # #           0.0, 0.2, 1e-2, 1e6, "Loose #mu PF Rel Iso 0.4 (all)", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_pfRelIso03_chg", "", False,  True, default_norm,
    # #           1, 0, 0.5, 1e-2, 1e6, "Loose #mu PF Rel Iso 0.3 (chg)", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_pfRelIso03_all", "", False,  True, default_norm,
    # #           1, 0, 0.5, 1e-2, 1e6, "Loose #mu PF Rel Iso 0.3 (all)", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_miniPFRelIso_chg", "", False,  True, default_norm,
    # #           10, -0.1, 3.5, 1e-2, 1e6, "Loose #mu mini PF Rel Iso (chg)", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_miniPFRelIso_all", "", False,  True, default_norm,
    # #           5, -0.1, 3.5, 1e-2, 1e6, "Loose #mu mini PF Rel Iso (all)", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_jetRelIso", "", False,  True, default_norm,
    # #           50, -1, 8.0, 1e-2, 1e6, "Loose #mu jet Rel Iso", f"# events {year_str}"),
    # # Histogram("LooseMuonsSegmentMatch_tkRelIso", "", False,  True, default_norm,
    # #           20, -0.1, 8.0, 1e-2, 1e6, "Loose #mu track Rel Iso", f"# events {year_str}"),

    # # Histogram("LooseMuonsSegmentMatch_logAbsDzFromLeadingTight", "", False,  True, default_norm,
    # #           100, -5, 3, 1e-2, 1e6, "|#Delta z(Loose #mu, Tight #mu_{1})|", f"# events {year_str}"),

    # # Histogram("LooseMuonsVertexSegmentMatch_3Dangle", "", False, True, default_norm,
    # #           2, 0, 3.15, 1e-4, 1e8, "#mu vertex 3Dangle", f"# events {year_str}"),
    # # Histogram("LooseMuonsVertexSegmentMatch_cos3Dangle", "", False, True, default_norm,
    # # 2, -1, 1, 1e-4, 1e8, "#mu vertex cos 3Dangle", f"# events {year_str}"),

    # # ----------------------------------------------------------------------------
    # # Loose DSA muons
    # # ----------------------------------------------------------------------------
    # # Histogram("LooseDSAMuonsSegmentMatch_pt", "", False,  True, default_norm, 40, 0, 600,
    # #           1e-4, 1e10, "loose dSA #mu p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_pt_irr", "", False,  True, default_norm, 1, 0, 2000,
    # #           1e-5, 1e10, "loose dSA #mu p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_pt_irr2", "", False,  True, default_norm, 1, 0, 600,
    # #           1e-5, 1e10, "loose dSA #mu p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_absDxyPVTraj", "", False,  True, default_norm, 50, 0,
    # #           500, 1e-2, 1e12, "loose dSA #mu |d_{xy}| [cm]", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_absDxyPVTraj_irr", "", False,  True, default_norm, 1, 0,
    # #           700, 1e-2, 1e12, "loose dSA #mu |d_{xy}| [cm]", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_eta", "", False,  True, default_norm, 5, -3, 3,
    # #           1e-2, 1e10, "loose dSA #mu #eta", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_ptErr", "", False,  True, default_norm, 20, 0, 2000,
    # #           1e-5, 1e8, "loose dSA #mu #sigma p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_outerEta", "", False,  True, default_norm, 5, -
    # #           3.5, 3.5, 1e-2, 1e10, "loose dSA #mu outer #eta", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_phi", "", False,  True, default_norm, 5, -
    # #           3.5, 3.5, 1e-2, 1e10, "loose dSA #mu #phi", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_outerPhi", "", False,  True, default_norm, 5, -
    # #           3.5, 3.5, 1e-2, 1e10, "loose dSA #mu outer #phi", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_normChi2", "", False,  True, default_norm, 50, 0,
    # #           2.5, 1e-2, 1e10, "loose dSA #mu #chi^{2}/ndof", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_nSegments", "", False,  True, default_norm, 1, 0,
    # #           20, 1e-2, 1e10, "loose dSA #mu segments", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_nDTSegments", "", False,  True, default_norm, 1, 0,
    # #           20, 1e-2, 1e10, "loose dSA #mu DT segments", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_nCSCSegments", "", False,  True, default_norm, 1, 0,
    # #           20, 1e-2, 1e10, "loose dSA #mu CSC segments", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_logAbsDzFromLeadingTight", "", False,  True, default_norm, 50, -5,
    # #           3, 1e-2, 1e10, "loose dSA #mu log |#Delta z(#mu_{DSA}, #mu_{tight} |", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_trkNumPlanes", "", False,  True, default_norm, 1, 0,
    # #           20, 1e-2, 1e10, "loose dSA #mu track planes", f"# events {year_str}"),
    # # Histogram("LooseDSAMuonsSegmentMatch_trkNumHits", "", False,  True, default_norm, 1, 0,
    # #           50, 1e-2, 1e10, "loose dSA #mu track hits", f"# events {year_str}"),

    # # ----------------------------------------------------------------------------
    # # Loose electrons
    # # ----------------------------------------------------------------------------
    # # Histogram("LooseElectrons_pt", "", False,  True, default_norm, 10, 0, 500,
    # #           1e-2, 1e6, "loose electron p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseElectrons_leadingPt", "", False,  True, default_norm, 10, 0, 500,
    # #           1e-2, 1e6, "leading loose electron p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseElectrons_subleadingPt", "", False,  True, default_norm, 10, 0, 500,
    # #           1e-2, 1e6, "all subleading loose electron p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LooseElectrons_eta", "", False,  True, default_norm, 5, -
    # #           3.5, 3.5, 1e-2, 1e6, "loose electron #eta", f"# events {year_str}"),
    # # Histogram("LooseElectrons_dxy", "", False,  True, default_norm, 10, -
    # #           10, 10, 1e-2, 1e6, "loose electron d_{xy}", f"# events {year_str}"),
    # # Histogram("LooseElectrons_dz", "", False,  True, default_norm, 10, -
    # #           10, 10, 1e-2, 1e6, "loose electron d_{z}", f"# events {year_str}"),

    # # ----------------------------------------------------------------------------
    # # Good jets
    # # ----------------------------------------------------------------------------
    # Histogram("GoodJets_pt", "", False,  True, default_norm, 10, 0, 1300,
    #           1e-3, 1e8, "good jet p_{T} [GeV]", f"Events / 10 GeV"),
    # Histogram("GoodJets_pt_smeared", "", False,  True, default_norm, 20, 0, 1300,
    #           1e-3, 1e8, "Good jet p_{T} [GeV]", f"# events {year_str}"),
    # Histogram("GoodJets_eta", "", False,  True, default_norm, 10, -
    #           3, 5.0, 1e-3, 1e11, "Good jet #eta", f"Events / 0.2"),
    # # Histogram("GoodJets_btagDeepB", "", False,  True, default_norm, 10, 0,
    # #           1.5, 2e0, 1e8, "good jet deepCSV score", f"# events {year_str}"),
    # # Histogram("GoodJets_btagDeepFlavB", "", False,  True, default_norm, 10,
    # #           0, 1.8, 1e-1, 1e8, "good jet deepJet score", f"# events {year_str}"),
    # # Histogram("GoodJets_minvBjet2jets", "", False,  True, default_norm, 25, 0,
    # #           1500, 1e-1, 1e5, "good jets m_{bjj} [GeV]", f"# events {year_str}"),

    # # ----------------------------------------------------------------------------
    # # Good b-jets
    # # ----------------------------------------------------------------------------
    # Histogram("GoodMediumBtaggedJets_pt", "", False,  True, default_norm, 10,
    #           0, 2000, 1e-3, 1e8, "Good b-jet p_{T} [GeV]", f"Events / 10 GeV"),
    # Histogram("GoodMediumBtaggedJets_pt_smeared", "", False,  True, default_norm, 20,
    #           0, 2000, 1e-3, 1e8, "Good b-jet p_{T} [GeV]", f"# events {year_str}"),
    # Histogram("GoodMediumBtaggedJets_eta", "", False,  True, default_norm,
    #           10, -3.5, 3.5, 1e-3, 1e10, "Good b-jet #eta", f"Events / 0.2"),
    # # Histogram("GoodMediumBtaggedJets_btagDeepB", "", False,  True, default_norm,
    # #           10, -1, 1, 1e0, 1e8, "good b-jet deepCSV score", f"# events {year_str}"),
    # # Histogram("GoodMediumBtaggedJets_btagDeepFlavB", "", False,  True, default_norm,
    # # 10, -1, 1, 1e0, 1e8, "good b-jet deepJet score", f"# events {year_str}"),

    # # ----------------------------------------------------------------------------
    # # Primary vertices
    # # ----------------------------------------------------------------------------
    # # Histogram("Event_PV_npvs", "", False,  True, default_norm, 1, 0,
    # #           150, 1e-3, 1e12, "# Primary vertices", f"# events {year_str}"),
    # # Histogram("Event_PV_npvsGood", "", False,  True, default_norm, 1, 0,
    # #           80, 1e-4, 1e8, "# Good primary vertices", f"# events {year_str}"),
    # # Histogram("Event_PV_x", "", False, True, default_norm, 1, -0.2, 0.2, 1e-5, 1e10, "PV x [cm]", f"# events {year_str}"),
    # # Histogram("Event_PV_y", "", False, True, default_norm, 1, -0.2, 0.2, 1e-5, 1e10, "PV y [cm]", f"# events {year_str}"),
    # # Histogram("Event_PV_z", "", False, True, default_norm, 50, -10, 10, 1e-2, 1e8, "PV z [cm]", f"# events {year_str}"),
    # # Histogram("Event_PV_chi2" , "", False, True, default_norm , 1, 0, 1.4, 1e-3, 1e6, "PV #chi^{2}", f"# events {year_str}"),

    # # ----------------------------------------------------------------------------
    # # Muon Trigger Objects
    # # ----------------------------------------------------------------------------
    # # Histogram("Event_nMuonTriggerObjects", "", False, True, default_norm, 1, 0, 10,
    # #           1e-5, 1e8, "Number of muon trigger objects", f"# events {year_str}"),
    # # Histogram("MuonTriggerObjects_pt", "", False, True, default_norm, 5, 0, 200,
    # #           1e-5, 1e8, "Muon trigger objects p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("MuonTriggerObjects_eta", "", False, True, default_norm, 5, -3, 3,
    # #           1e-5, 1e8, "Muon trigger objects #eta", f"# events {year_str}"),
    # # Histogram("MuonTriggerObjects_phi", "", False, True, default_norm, 5, -3, 3,
    # #           1e-5, 1e8, "Muon trigger objects #phi", f"# events {year_str}"),
    # # Histogram("MuonTriggerObjects_hasFilterBits2", "", False, True, default_norm, 1,
    # #           0, 10, 1e-5, 1e8, "Muon trigger objects has filerBits 2", f"# events {year_str}"),
    # # Histogram("MuonTriggerObjects_minDRTightLooseMuon", "", False, True, default_norm, 1,
    # #           0, 10, 1e-5, 1e8, "min #Delta R (Muon trigger, tight muons)", f"# events {year_str}"),
    # # Histogram("MuonTriggerObjects_tightLooseMuonMatch0p3", "", False, True, default_norm, 1,
    # #           0, 10, 1e-5, 1e8, "min #Delta R (Muon trigger, tight muons) < 0.3", f"# events {year_str}"),
    # # Histogram("MuonTriggerObjects_tightLooseMuonMatch0p1", "", False, True, default_norm, 1,
    # #           0, 10, 1e-5, 1e8, "min #Delta R (Muon trigger, tight muons) < 0.1", f"# events {year_str}"),
    # # Histogram("Event_nLeadingMuonTriggerObject", "", False, True, default_norm, 1, 0, 10,
    # #           1e-5, 1e8, "Number of muon trigger objects", f"# events {year_str}"),
    # # Histogram("LeadingMuonTriggerObject_pt", "", False, True, default_norm, 5, 0, 200,
    # #           1e-5, 1e8, "Muon trigger objects p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("LeadingMuonTriggerObject_eta", "", False, True, default_norm, 5, -3, 3,
    # #           1e-5, 1e8, "Muon trigger objects #eta", f"# events {year_str}"),
    # # Histogram("LeadingMuonTriggerObject_phi", "", False, True, default_norm, 5, -3, 3,
    # #           1e-5, 1e8, "Muon trigger objects #phi", f"# events {year_str}"),
    # # Histogram("LeadingMuonTriggerObject_hasFilterBits2", "", False, True, default_norm, 1, 0,
    # #           10, 1e-5, 1e8, "Muon trigger objects has filerBits 2", f"# events {year_str}"),
    # # Histogram("LeadingMuonTriggerObject_minDRTightLooseMuon", "", False, True, default_norm, 1,
    # #           0, 1, 1e-5, 1e8, "min #Delta R (Muon trigger, tight muons)", f"# events {year_str}"),
    # # Histogram("LeadingMuonTriggerObject_tightLooseMuonMatch0p3", "", False, True, default_norm,
    # #           1, 0, 2, 1e-5, 1e10, "min #Delta R (Muon trigger, tight muons) < 0.3", f"# events {year_str}"),
    # # Histogram("LeadingMuonTriggerObject_tightLooseMuonMatch0p1", "", False, True, default_norm,
    # #           1, 0, 2, 1e-5, 1e10, "min #Delta R (Muon trigger, tight muons) < 0.1", f"# events {year_str}"),

    # # ----------------------------------------------------------------------------
    # # Gen ALP
    # # ----------------------------------------------------------------------------
    # # Histogram("GenALP_pt", "", False,  True, NormalizationType.to_one, 40,
    # #           0, 300, 1e-3, 1e0, "ALP p_{T} [GeV]", f"# events {year_str}"),
    # # Histogram("GenALP_boost", "", False,  True, NormalizationType.to_one, 50,
    # #           0, 500, 1e-3, 1e1, "ALP boost [GeV]", f"# events {year_str}"),
    # Histogram("GenALP_eta", "", False,  True, NormalizationType.to_one,
    #           10, -3.5, 3.5, 1e-3, 1e1, "ALP #eta", f"# events {year_str}"),
    # Histogram("GenDimuonFromALP_Lxy", "", False,  True, NormalizationType.to_one,
    #           500, 0, 500, 1e-4, 1e1, "Gen Dimuon from ALP L_{xy} [cm]", f"Fraction of events"),
    # Histogram("GenDimuonFromALP_eta", "", False,  True, NormalizationType.to_one,
    #           10, -3.5, 3.5, 1e-3, 1e1, "Gen Dimuon from ALP #eta", f"# events {year_str}"),
    # Histogram("GenDimuonFromALP_eta1", "", False,  True, NormalizationType.to_one,
    #           10, -3.5, 3.5, 1e-3, 1e1, "Gen muon1 from ALP #eta", f"# events {year_str}"),
    # Histogram("GenDimuonFromALP_eta2", "", False,  True, NormalizationType.to_one,
    #           10, -3.5, 3.5, 1e-3, 1e1, "Gen muon2 from ALP #eta", f"# events {year_str}"),
)

# ----------------------------------------------------------------------------
# Dimuons
# ----------------------------------------------------------------------------

categories = ("", "_PatDSA", "_DSA", "_Pat")
# categories = ("",)
mass_rebin = {c: 5   for c in categories}
mass_min   = {c: 2.0 for c in categories}
mass_max   = {c: 5.0 for c in categories}
mass_y_max = {c: 4000 for c in categories}
mass_y_title = {c: "Events / 0.01 GeV" for c in categories}

if "JPsiDimuons" in skim[1]:
  mass_rebin["_DSA"] = 10
  mass_min["_DSA"]   = 2.1
  mass_max["_DSA"]   = 4.2
  mass_y_title["_DSA"] = "Events / 0.1 GeV"
  mass_rebin["_PatDSA"] = 4
  mass_min["_PatDSA"]   = 2.6
  mass_max["_PatDSA"]   = 3.8
  mass_y_title["_PatDSA"] = "Events / 0.04 GeV"
  mass_rebin["_Pat"] = 1
  mass_min["_Pat"]   = 2.9
  mass_max["_Pat"]   = 3.3
  mass_y_title["_Pat"] = "Events / 0.01 GeV"
  if year == "2016preVFP" or year == "2016postVFP":
    mass_y_max["_DSA"] = 20
    mass_y_max["_PatDSA"] = 30
    mass_y_max["_Pat"] = 70
  if year == "2016postVFP":
    mass_y_max["_DSA"] = 25
    mass_y_max["_PatDSA"] = 40
  if year == "2017":
    mass_y_max["_DSA"] = 40
    mass_y_max["_PatDSA"] = 110
    mass_y_max["_Pat"] = 200
  if year == "2018":
    mass_y_max["_DSA"] = 60
    mass_y_max["_PatDSA"] = 150
    mass_y_max["_Pat"] = 200
  if year == "2022preEE":
    mass_y_max["_DSA"] = 20
    mass_y_max["_PatDSA"] = 20
    mass_y_max["_Pat"] = 40
  if year == "2022postEE":
    mass_y_max["_DSA"] = 20
    mass_y_max["_PatDSA"] = 60
    mass_y_max["_Pat"] = 100
  if year == "2023preBPix":
    mass_y_max["_DSA"] = 20
    mass_y_max["_PatDSA"] = 40
    mass_y_max["_Pat"] = 120
  if year == "2023postBPix":
    mass_y_max["_DSA"] = 15
    mass_y_max["_PatDSA"] = 50
    mass_y_max["_Pat"] = 70

norm_one = NormalizationType.to_one

Lxy_max = {
  "": 500,
  # "": 200,
  "_Pat": 120,
  "_PatDSA": 400,
  "_DSA": 400,
}
Lxy_rebin = {
  "": 1000,
  "_Pat": 200,
  "_PatDSA": 800,
  "_DSA": 800,
}

combined_categories = ["_Pat","_DSA"]

for collection, category in product(extraMuonVertexCollections, categories):
  histograms += (
      Histogram("Event_n"+collection + category, "", False, False, default_norm, 1,
                0, 10, 0, 10, "Number of #mu vertices", f"# events {year_str}"),
      Histogram("dimuonCutFlow_"+collection + category, "", False,  True,
                default_norm, 1, 0, 12, 1e1, 1e6, "Selection", "Number of events"),
      
      # Histogram(collection + category+"_pt", "", False, True, norm_one, 40, 0,
      #           400, 1e-3, 1e0, "p_{T}^{#mu#mu} [GeV]", f"Fraction of events / 25 GeV"),
      # Histogram(collection + category+"_logInvMass", "", False, True, norm_one, 17, -0.7, 2.0,
      #           1e-3, 1e2, "log_{10}(M_{#mu #mu} [GeV])", "Fraction of events / log_{10}(0.05 [GeV])"),
      # Histogram(collection + category+"_logInvMass", "", False, True, norm_one, 13, -0.7, 2.0,
      #           1e-3, 1e2, "log_{10}(M_{#mu #mu} [GeV])", "Fraction of events / log_{10}(0.05 [GeV])"),
      # Histogram(collection + category+"_Lxy", "", False, True, norm_one, Lxy_rebin[category], 0,
      #           Lxy_max[category], 1e-3, 1e1, "L_{xy} [cm]", f"Fraction of events / 25 cm"),
      # Histogram(collection + category+"_Lxy", "", False, True, norm_one, 250, 0,
      #           Lxy_max[category], 1e-3, 1e1, "L_{xy} [cm]", f"Fraction of events / 25 cm"),
      
      ##### Paper plots
      Histogram(collection + category+"_Lxy", "", False, True, default_norm, Lxy_rebin[category], 0,
                Lxy_max[category], 1e-4, 1e5, "L_{xy} [cm]", f"Events / 20 cm"),
      Histogram(collection + category+"_pt", "", False, True, default_norm, 20, 0,
                500, 1e-3, 1e4, "p_{T}^{#mu#mu} [GeV]", f"Events / 10 GeV"),
      Histogram(collection + category+"_absCollinearityAngle", "", False, True, default_norm, 2,
                0, 0.5, 1e-2, 1e4, "|#Delta#Phi_{coll}|", f"Events / 0.02"),
      Histogram(collection + category+"_dxyPVTraj1", "", False, True, default_norm, 500, 0,
                350, 1e-4, 1e4, "d_{xy}^{#mu1} [cm]", f"Events / 10 cm"),
      Histogram(collection + category+"_dxyPVTraj2", "", False, True, default_norm, 500, 0,
                350, 1e-4, 1e4, "d_{xy}^{#mu2} [cm]", f"Events / 10 cm"),
      Histogram(collection + category+"_logInvMass", "", False, True, default_norm, 17, -0.7, 2.0,
                1e-3, 1e5, "log_{10}(M_{#mu #mu} [GeV])", "Fraction of events / log_{10}(0.05 [GeV])"),

      ##### Thesis plots
      ### Signal sample plots
      # Histogram(collection + category+"_pt", "", False, True, norm_one, 40, 0,
      #           400, 1e-3, 1e0, "p_{T}^{#mu#mu} [GeV]", f"Fraction of events / 20 GeV"),
      # Histogram(collection + category+"_logInvMass", "", False, True, norm_one, 13, -0.7, 2.0,
      #           1e-3, 1e2, "log_{10}(M_{#mu #mu} [GeV])", "Fraction of events / log_{10}(0.05 [GeV])"),
      # Histogram(collection + category+"_Lxy", "", False, True, norm_one, Lxy_rebin[category], 0,
      #           Lxy_max[category], 1e-3, 1e1, "L_{xy} [cm]", f"Fraction of events / 25 cm"),
      ## GenDimuonFromALP
      # Histogram(collection + category+"_logInvMass", "", False, True, norm_one, 17, -0.7, 2.0,
      #           1e-3, 1e2, "log_{10}(M_{#mu #mu} [GeV])", "Fraction of events / log_{10}(0.05 [GeV])"),
      # Histogram(collection + category+"_Lxy", "", False, True, norm_one, 250, 0,
      #           Lxy_max[category], 1e-3, 1e1, "L_{xy} [cm]", f"Fraction of events / 25 cm"),
      ### Dimuon selection plots
      # Histogram(collection + category+"_absCollinearityAngle", "", False, True, NormalizationType.to_background, 10,
      #           0, 3.1, 1e-2, 1e3, "|#Delta#Phi_{coll}|", f"Number of events / 0.1"),
      # Histogram(collection + category+"_dca", "", False, True, NormalizationType.to_background,
      #           25, 0, 10, 1e-3, 1e4, "DCA(#mu#mu) [cm]", f"Number of events / 0.5 cm"),
      # Histogram(collection + category+"_logInvMass", "", False, True, NormalizationType.to_background, 
      #           17, -0.7, 2.0, 1e-2, 1e5, "log_{10}(M_{#mu#mu} [GeV])", "Number of events / log_{10}(0.05 [GeV])"),
      # Histogram(collection + category+"_invMass", "", False, True, default_norm, 5,
      #           2, 5, 1e-3, 1e3, "M_{#mu#mu} [GeV]", "Number of events / 0.05 GeV"),
      # Histogram(collection + category+"_normChi2", "", False, True, NormalizationType.to_background, 200,
      #           0, 5, 1e-3, 1e5, "Vertex fit #chi^{2}/ndof", f"Number of events / 0.2"),
      ### SS CR 
      # Histogram(collection + category+"_eta", "", False, True, default_norm, 10, -3.4,
      #           3.4, 1e-3, 1e4, "|#eta^{#mu#mu}|", f"Events / 0.2"),
      # Histogram(collection + category+"_dR", "", False, True, default_norm, 20,
      #           0, 6, 1e-3, 1e5, "#Delta R(#mu#mu)", f"Events"),
      # Histogram(collection + category+"_Lxy", "", False, True, default_norm, Lxy_rebin[category], 0,
      #           Lxy_max[category], 1e-4, 1e5, "L_{xy} [cm]", f"Events / 20 cm"),
      # Histogram(collection + category+"_pt", "", False, True, default_norm, 40, 0,
      #           350, 1e-3, 1e4, "p_{T}^{#mu#mu} [GeV]", f"Events / 20 GeV"),
      ### Comsic muons SR bin D
      # Histogram(collection + category+"_3Dangle", "", False, True, default_norm, 10, 
      #           0, 3.15, 1e-3, 1e4, "3D angle(#mu#mu)", f"Events / 0.1"),
      ### DSA reverted macthing plots
      # Histogram(collection + category+"_pt", "", False, True, norm_one, 40, 0,
      #           400, 1e-3, 2e0, "p_{T}^{#mu#mu} [GeV]", f"Fraction of events / 20 GeV"),
      ### J/Psi CR
      # Histogram(collection + category+"_pt", "", False, True, default_norm, 40, 0,
      #           300, 1e-3, 1e4, "p_{T}^{#mu#mu} [GeV]", f"Events / 20 GeV"),
      # Histogram(collection + category+"_pt_irr", "", False, True, default_norm, 1, 0,
      #           120, 1e-3, 1e7, "p_{T}^{#mu#mu} [GeV]", f"Events"),
      # Histogram(collection + category+"_invMass", "", False, False, default_norm, mass_rebin[category],
      #           mass_min[category], mass_max[category], 0, mass_y_max[category], "M_{#mu#mu} [GeV]", mass_y_title[category]),

      # Histogram(collection + category+"_invMass", "", False, False, default_norm, mass_rebin[category],
      #           2.5, 3.9, 0, 60, "M_{#mu#mu} [GeV]", mass_y_title[category]),

      # Histogram(collection + category+"_invMass", "", False, False, default_norm, mass_rebin[category],
      #           mass_min[category], mass_max[ca§tegory], 0, mass_y_max[category], "#mu vertex M_{#mu #mu} [GeV]", f"# events {year_str}"),
      # Histogram(collection + category+"_invMass", "", False, True, default_norm, 50,
      #           0, 70, 1e-3, 1e5, "#mu vertex M_{#mu #mu} [GeV]", f"# events {year_str}"),
      # # Histogram(collection + category+"_invMassJPsiBin", "", False, False, default_norm,
      # #           1, 2.2, 4.0, 0, 500, "#mu vertex M_{#mu #mu} [GeV]", f"# events {year_str}"),
      # Histogram(collection + category+"_logInvMass", "", False, True, default_norm, 15, -0.7, 1.9,
      #           1e-2, 1e5, "Dimuon vertex log_{10}(M_{#mu #mu} [GeV])", f"# events {year_str}"),
      # Histogram(collection + category+"_eta", "", False, True, default_norm, 10,
      #           -3.5, 4, 1e-3, 1e7, "Dimuon vertex #eta", f"# events {year_str}"),
      # Histogram(collection + category+"_pt", "", False, True, default_norm, 20, 0,
      #           500, 1e-3, 1e5, "#mu vertex p_{T} [GeV]", f"# events {year_str}"),
      # Histogram(collection + category+"_pt_irr", "", False, True, default_norm, 1, 0,
                # 120, 1e-3, 1e7, "#mu vertex p_{T} [GeV]", f"# events {year_str}"),
      # Histogram(collection + category+"_muonPtErr", "", False, True, default_norm, 2, 0,
      #           50, 1e-2, 1e5, "Dimuon vertex #mu #sigma_{pT} [GeV]", f"# events {year_str}"),
      # Histogram(collection + category+"_leadingPt", "", False, True, default_norm, 20, 0,
      #           500, 1e-2, 1e2, "#mu vertex leading p_{T} [GeV]", f"# events {year_str}"),
      # Histogram(collection + category+"_muonPt1", "", False, True, default_norm, 20, 0,
      #           300, 1e-3, 1e5, "#mu_{1} p_{T} [GeV]", f"# events {year_str}"),
      # Histogram(collection + category+"_muonPt2", "", False, True, default_norm, 10, 0,
      #           300, 1e-3, 1e5, "#mu_{2} p_{T} [GeV]", f"# events {year_str}"),
      # Histogram(collection + category+"_muonEta1", "", False, True, default_norm, 5, -
      #           3.5, 3.5, 1e-3, 1e6, "#mu_{1} #eta", f"# events {year_str}"),
      # Histogram(collection + category+"_muonEta2", "", False, True, default_norm, 5, -
      #           3.5, 3.5, 1e-3, 1e6, "#mu_{2} #eta", f"# events {year_str}"),
      # Histogram(collection + category+"_muonPtErr1", "", False, True, default_norm, 1, 0,
      #           25, 1e-2, 1e5, "#mu_{1} #sigma_{pT} [GeV]", f"# events {year_str}"),
      # Histogram(collection + category+"_muonPtErr2", "", False, True, default_norm, 1, 0,
      #           25, 1e-2, 1e5, "#mu_{2} #sigma_{pT} [GeV]", f"# events {year_str}"),

      # Histogram(collection + category+"_LxySignificance", "", False, True, default_norm, 20, 0,
      #           200, 1e-4, 1e5, "Dimuon vertex L_{xy} / #sigma_{Lxy}", f"# events {year_str}"),
      # Histogram(collection + category+"_Lxy", "", False, True, default_norm, Lxy_rebin[category], 0,
      #           Lxy_max[category], 1e-4, 1e6, "Dimuon vertex L_{xy} [cm]", f"# events {year_str}"),
      # Histogram(collection + category+"_Lxy", "", False, True, default_norm, 200, 0,
      #           200, 1e-4, 1e6, "Dimuon vertex L_{xy} [cm]", f"# events {year_str}"),
      # Histogram(collection + category+"_absDxyPVTraj1", "", False, True, default_norm, 1,
      #           0, 1, 1e-3, 1e5, "Dimuon vertex |d_{xy}^{#mu1}|", f"# events {year_str}"),
      # Histogram(collection + category+"_dxyPVTraj1", "", False, True, default_norm, 1,
      #           -1, 1, 1e-3, 1e5, "Dimuon vertex |d_{xy}^{#mu1}|", f"# events {year_str}"),
      # Histogram(collection + category+"_absDxyPVTraj2", "", False, True, default_norm, 1,
      #           0, 1, 1e-3, 1e5, "Dimuon vertex |d_{xy}^{#mu2}|", f"# events {year_str}"),
      # Histogram(collection + category+"_dxyPVTrajSig1", "", False, True, default_norm, 1, 0, 30, 1e-4, 1e6, "Dimuon vertex d_{xy}^{#mu1} / #sigma_{dxy}^{#mu1}", f"# events {year_str}"),
      # Histogram(collection + category+"_dxyPVTrajSig2", "", False, True, default_norm, 1, 0, 30, 1e-4, 1e6, "Dimuon vertex d_{xy}^{#mu2} / #sigma_{dxy}^{#mu2}", f"# events {year_str}"),
      # Histogram(collection + category+"_LxySigma", "", False, True, default_norm, 20, 0, 100, 1e-5, 1e6, "#mu vertex #sigma_{Lxy} [cm]", f"# events {year_str}"),
      # Histogram(collection + category+"_vxySigma", "", False, True, default_norm, 20, 0, 100, 1e-5, 1e6, "#mu vertex #sigma_{Lxy} [cm]", f"# events {year_str}"),

      # Histogram(collection + category+"_nSegments", "", False, True, default_norm,
      #           1, 0, 20, 1e-3, 1e8, "#mu vertex N(segments)", f"# events {year_str}"),
      # Histogram(collection + category+"_nSegments1", "", False, True, default_norm,
      #           1, 0, 20, 1e-3, 1e8, "#mu_{1} N(segments)", f"# events {year_str}"),
      # Histogram(collection + category+"_nSegments2", "", False, True, default_norm,
      #           1, 0, 20, 1e-3, 1e8, "#mu_{2} N(segments)", f"# events {year_str}"),

      # Histogram(collection + category+"_dR", "", False, True, default_norm, 2,
      #           0, 3.15, 1e-3, 1e5, "#mu vertex #Delta R", f"# events {year_str}"),
      # Histogram(collection + category+"_dR", "", False, True, default_norm, 10,
      #           0, 6, 1e-3, 1e5, "#mu vertex #Delta R", f"# events {year_str}"),
      # Histogram(collection + category+"_dRprox", "", False, True, default_norm, 10, 0, 3, 1e-3, 1e5, "#mu vertex proximity #Delta R", f"# events {year_str}"),
      # Histogram(collection + category+"_outerDR", "", False, True, default_norm, 4, 0,
      #           3, 1e-3, 1e5, "#mu vertex outer #Delta R", f"# events {year_str}"),
      # Histogram(collection + category+"_logOuterDR", "", False, True, default_norm, 10, -2, 1, 1e-3, 1e7, "#mu vertex log outer #Delta R", f"# events {year_str}"),
      # Histogram(collection + category+"_dEta", "", False, True, default_norm, 1, 0, 3.15, 1e-3, 1e6, "#mu vertex #Delta #eta", f"# events {year_str}"),
      # Histogram(collection + category+"_dPhi", "", False, True, default_norm, 1, 0, 3.15, 1e-3, 1e6, "#mu vertex #Delta #phi", f"# events {year_str}"),

      # Histogram(collection + category+"_displacedTrackIso03Dimuon1", "", False, True,
      #           default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.3}(#mu_{1})", f"# events {year_str}"),
      # Histogram(collection + category+"_displacedTrackIso03Dimuon2", "", False, True,
      #           default_norm, 1, 0, 1, 1e-4, 1e7, "Iso_{0.3}(#mu_{2})", f"# events {year_str}"),
      # Histogram(collection + category+"_displacedTrackIso04Muon1", "", False, True, default_norm, 2, 0, 2, 1e-3, 1e7, "#mu_{1} Iso_{Trk}^{Rel}(#Delta R < 0.4)", f"# events {year_str}"),
      # Histogram(collection + category+"_displacedTrackIso04Muon2", "", False, True, default_norm, 2, 0, 2, 1e-3, 1e7, "#mu_{2} Iso_{Trk}^{Rel}(#Delta R < 0.4)", f"# events {year_str}"),
      # Histogram(collection + category+"_displacedTrackIso04Dimuon1", "", False, True, default_norm, 8, 0, 2, 1e-3, 1e7, "#mu_{1} Iso_{Trk}^{Rel}(#Delta R < 0.4)", f"# events {year_str}"),
      # Histogram(collection + category+"_displacedTrackIso04Dimuon2", "", False, True, default_norm, 8, 0, 2, 1e-3, 1e7, "#mu_{2} Iso_{Trk}^{Rel}(#Delta R < 0.4)", f"# events {year_str}"),
      # # Histogram(collection + category+"_logDisplacedTrackIso04Dimuon1", "", False, True, default_norm, 10, -3, 2, 1e-3, 1e7, "log Iso_{Dipl.Trk}^{#mu_{1}}(0.4)", f"# events {year_str}"),
      # # Histogram(collection + category+"_logDisplacedTrackIso04Dimuon2", "", False, True, default_norm, 10, -3, 2, 1e-3, 1e7, "log Iso_{Dipl.Trk}^{#mu_{2}}(0.4)", f"# events {year_str}"),
      # Histogram(collection + category+"_pfRelIso04all1", "", False, True, default_norm, 2, 0, 1.0, 1e-3, 1e7, "#mu_{1} I_{PF}^{rel} (#Delta R < 0.4)", f"# events {year_str}"),
      # Histogram(collection + category+"_pfRelIso04all2", "", False, True, default_norm, 2, 0, 1.0, 1e-3, 1e7, "#mu_{2} I_{PF}^{rel} (#Delta R < 0.4)", f"# events {year_str}"),
      # Histogram(collection + category+"_logPfRelIso04all1", "", False, True, default_norm, 10, -4, 3, 1e-3, 1e7, "#mu_{1} log I_{PF}^{rel} ( #Delta R < 0.4 )", f"# events {year_str}"),
      # Histogram(collection + category+"_logPfRelIso04all2", "", False, True, default_norm, 10, -4, 3, 1e-3, 1e7, "#mu_{2} log I_{PF}^{rel} ( #Delta R < 0.4 )", f"# events {year_str}"),
      
      # Histogram(collection + category+"_normChi2", "", False, True, default_norm, 200,
      #           0, 7, 1e-3, 1e5, "Dimuon vertex #chi^{2}/ndof", f"# events {year_str}"),
      # Histogram(collection + category+"_normChi2", "", False, True, norm_one, 3000,
      #           0, 9, 1e-4, 1e1, "Dimuon vertex #chi^{2}/ndof", f"# events {year_str}"),
      # Histogram(collection + category+"_maxHitsInFrontOfVert", "", False, True, default_norm, 1, 0, 35, 1e-4, 1e5, "Max N(hits before vertex)", f"# events {year_str}"),
      # Histogram(collection + category+"_sumHitsInFrontOfVert", "", False, True, default_norm,
      #           1, 0, 35, 1e-4, 1e5, "Sum N(hits before vertex)", f"# events {year_str}"),
      # Histogram(collection + category+"_hitsInFrontOfVert1", "", False, True, default_norm,
      #           1, 0, 35, 1e-4, 1e5, "#mu_{1} N(hits before vertex)", f"# events {year_str}"),
      # Histogram(collection + category+"_hitsInFrontOfVert2", "", False, True, default_norm,
      #           1, 0, 35, 1e-4, 1e5, "#mu_{2} N(hits before vertex)", f"# events {year_str}"),
      # Histogram(collection + category+"_missHitsAfterVert1", "", False, True, default_norm,
      #           1, 0, 35, 1e-4, 1e5, "#mu_{1} N(hits after vertex)", f"# events {year_str}"),
      # Histogram(collection + category+"_missHitsAfterVert2", "", False, True, default_norm,
      #           1, 0, 35, 1e-4, 1e5, "#mu_{2} N(hits after vertex)", f"# events {year_str}"),
      # Histogram(collection + category+"_dca", "", False, True, default_norm,
      #           10, 0, 15, 1e-3, 1e5, "Dimuon DCA [cm]", f"# events {year_str}"),
      
      # Histogram(collection + category+"_3Dangle", "", False, True, default_norm, 10, 0, 3.15, 1e-3, 1e5, "#mu vertex 3Dangle", f"# events {year_str}"),
      # Histogram(collection + category+"_cos3Dangle", "", False, True, default_norm, 5, -1, 1, 1e-3, 1e8, "#mu vertex cos 3Dangle", f"# events {year_str}"),
      # Histogram(collection + category+"_absPtLxyDPhi1", "", False, True, default_norm, 10,
      #           0, 3.15, 1e-4, 1e5, "#mu vertex |#Delta #phi_{#mu1}|", f"# events {year_str}"),
      # Histogram(collection + category+"_absPtLxyDPhi2", "", False, True, default_norm, 10,
      #           0, 3.15, 1e-4, 1e5, "#mu vertex |#Delta #phi_{#mu2}|", f"# events {year_str}"),
      
      # Histogram(collection + category+"_chargeProduct", "", False, True, default_norm,
      #           1, -1, 2, 1e-3, 1e5, "Dimuon vertex charge", f"# events {year_str}"),
      
      # Histogram(collection + category+"_absDzFromLeadingTight1", "", False, True, default_norm,
      #           2, 0, 2, 1e-3, 1e5, "|#Delta z(#mu_{1}, tight #mu)|", f"# events {year_str}"),
      # Histogram(collection + category+"_absDzFromLeadingTight2", "", False, True, default_norm,
      #           2, 0, 2, 1e-3, 1e5, "|#Delta z(#mu_{2}, tight #mu)|", f"# events {year_str}"),
      # Histogram(collection + category+"_dRFromLeadingTight1", "", False, True, default_norm,
      #           10, 0, 3.15, 1e-3, 1e5, "|#Delta R(#mu_{1}, tight #mu)|", f"# events {year_str}"),
      # Histogram(collection + category+"_dRFromLeadingTight2", "", False, True, default_norm,
      #           10, 0, 3.15, 1e-3, 1e5, "|#Delta R(#mu_{2}, tight #mu)|", f"# events {year_str}"),
      # Histogram(collection + category+"_proxDRFromLeadingTight1", "", False, True, default_norm,
      #           10, 0, 3.15, 1e-3, 1e5, "|#Delta R(#mu_{1}, tight #mu)|", f"# events {year_str}"),
      # Histogram(collection + category+"_proxDRFromLeadingTight2", "", False, True, default_norm,
      #           10, 0, 3.15, 1e-3, 1e5, "|#Delta R(#mu_{2}, tight #mu)|", f"# events {year_str}"),

      # Histogram(collection + category+"_pfRelIso04all1_noOuterTrk", "", False, True, default_norm, 
      #           10, 0, 2.0, 1e-3, 1e7, "#mu_{1} I_{PF}^{rel} (#Delta R < 0.4)", f"# events {year_str}"),
      # Histogram(collection + category+"_pfRelIso04all1_noOuterTrk", "", False, True, default_norm, 
      #           10, 0, 2.0, 1e-3, 1e7, "#mu_{1} I_{PF}^{rel} (#Delta R < 0.4)", f"# events {year_str}"),
      
      # Histogram(collection + category + "_trkNumPlanes1", "", False, True, default_norm, 1,
      #             0, 6, 1e-2, 1e6, f"#mu_{1} track planes", f"# events {year_str}"),
      # Histogram(collection + category + "_trkNumPlanes2", "", False, True, default_norm, 1,
      #             0, 6, 1e-2, 1e6, f"#mu_{2} track planes", f"# events {year_str}"),
      # Histogram(collection + category + "_trkNumHits1", "", False, True, default_norm, 1,
      #             0, 70, 1e-2, 1e6, f"#mu_{1} track hits", f"# events {year_str}"),
      # Histogram(collection + category + "_trkNumHits2", "", False, True, default_norm, 1,
      #             0, 70, 1e-2, 1e6, f"#mu_{2} track hits", f"# events {year_str}"),
      # Histogram(collection + category + "_trkNumDTHits1", "", False, True, default_norm, 1,
      #             0, 70, 1e-2, 1e6, f"#mu_{1} track DT hits", f"# events {year_str}"),
      # Histogram(collection + category + "_trkNumDTHits2", "", False, True, default_norm, 1,
      #             0, 70, 1e-2, 1e6, f"#mu_{2} track DT hits", f"# events {year_str}"),
      # Histogram(collection + category + "_trkNumCSCHits1", "", False, True, default_norm, 1,
      #             0, 70, 1e-2, 1e6, f"#mu_{1} track CSC hits", f"# events {year_str}"),
      # Histogram(collection + category + "_trkNumCSCHits2", "", False, True, default_norm, 1,
      #             0, 70, 1e-2, 1e6, f"#mu_{2} track CSC hits", f"# events {year_str}"),

  )

  muonQualityFlags = []
  # muonQualityFlags = ["PU", "fake", "real"]  # uncomment to include plots
  for flag in muonQualityFlags:
    histograms += (
        Histogram("Event_n" + collection + category + "_" + flag, "", False, True, default_norm, 1,
                  0, 2, 1e0, 1e5, f"#mu is {flag}", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_absDzFromLeadingTight", "", True, True, default_norm, 1,
                  1e-5, 1e3, 1e-4, 1e2, f"{flag} #mu |#DeltaZ(leading tight #mu)|", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_logAbsDzFromLeadingTight", "", False, True, default_norm, 50,
                  -5, 3, 1e-4, 1e2, f"{flag} #mu log |#DeltaZ(leading tight #mu)|", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_genMuonDR", "", False, True, default_norm, 1,
                  0, 0.1, 1e-4, 1e2, f"{flag} #mu #DeltaR(gen #mu)", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_normChi2", "", False, True, default_norm, 40,
                  0, 3, 1e-4, 1e2, f"{flag} #mu #chi^{2}/ndof", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_nSegments", "", False, True, default_norm, 1,
                  0, 20, 1e-2, 1e6, f"{flag} #mu segments", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_nDTSegments", "", False, True, default_norm, 1,
                  0, 20, 1e-4, 1e2, f"{flag} #mu DT segments", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_nCSCSegments", "", False, True, default_norm, 1,
                  0, 20, 1e-4, 1e2, f"{flag} #mu CSC segments", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_trkNumPlanes", "", False, True, default_norm, 1,
                  0, 6, 1e-2, 1e6, f"{flag} #mu track planes", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_trkNumHits", "", False, True, default_norm, 1,
                  0, 70, 1e-2, 1e6, f"{flag} #mu track hits", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_eta", "", False, True, default_norm, 10,
                  -3, 3, 1e-4, 1e2, f"{flag} #mu #eta", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_etaErr", "", False, True, default_norm, 10,
                  -3, 3, 1e-4, 1e2, f"{flag} #mu #sigma_#eta", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_pt", "", False, True, default_norm, 10,
                  0, 300, 1e-3, 1e5, f"{flag} #mu p_T", f"# events {year_str}"),
        Histogram(collection + category + "_" + flag + "_ptErr", "", False, True, default_norm, 10,
                  0, 300, 1e-3, 1e5, f"{flag} #mu #sigma p_T", f"# events {year_str}"),

    )
