import ROOT
from ROOT import TColor
from Sample import Sample, SampleType
from Legend import Legend
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

from ttalps_cross_sections import *

base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms/"
skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1"
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"


output_formats = ["pdf"]

luminosity = 59830.  # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

canvas_size = (800, 600)
canvas_size_2Dhists = (800, 800)
show_ratio_plots = False
ratio_limits = (0.5, 1.5)

legend_width = 0.17 if show_ratio_plots else 0.23
legend_min_x = 0.45
legend_max_x = 0.82
legend_height = 0.045 if show_ratio_plots else 0.03
legend_max_y = 0.89

n_default_backgrounds = 10

show_cms_labels = True
extraText = "Preliminary"
# extraText = "Private Work"

## SETTINGS ##
plots_from_LLPNanoAOD = True
plot_genALP_info = True
plot_muonMatching_info = False
plot_background = True
plot_ratio_hists = False

signal_legend = Legend(legend_max_x - legend_width, 
                       legend_max_y - 7*legend_height, 
                       legend_max_x - 2*legend_width, 
                       legend_max_y, "l")
sampletype = "sig"

if plot_background:
    plot_genALP_info = False
    plot_ratio_hists = False
    signal_legend = Legend(legend_max_x - 2.5*legend_width, 
                           legend_max_y - 0.13 - 5*legend_height, 
                           legend_max_x - 2*legend_width, 
                           legend_max_y - 0.13, 
                           "l")
    sampletype = "bkg"

legends = {
    SampleType.signal: signal_legend,
    SampleType.background: Legend(legend_max_x-legend_width, legend_max_y-n_default_backgrounds*legend_height, legend_max_x, legend_max_y, "f"),
    SampleType.data: Legend(legend_max_x-3*(legend_width), legend_max_y-legend_height, legend_max_x-2*(legend_width), legend_max_y, "pl"),
}

output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{sampletype}/"
# output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{sampletype}_goodVertices/"
# output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{sampletype}_bestVertices/"
# output_path = f"../plots/{skim.replace('skimmed_', '')}_{hist_path.replace('histograms_', '').replace('histograms', '')}_{sampletype}_secondBestVertices/"

# available styles: https://root.cern.ch/doc/master/classTAttFill.html
background_uncertainty_style = 3244
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

y_scale = 1

if plot_background:
    default_norm = NormalizationType.to_background
else:
    # default_norm = NormalizationType.to_one
    default_norm = NormalizationType.to_lumi
    y_scale = 0.1


#
# LooseMuonsVertexSegmentMatch
# BestLooseMuonsVertex
# GoodBestLooseMuonsVertex
#

# LooseMuonsVertexSegmentMatch_Pat
# _Pat, _DSA, _PatDSA

y_title = "# events (2018)"

histograms = (
    # #           name                                  title logx  logy    norm_type                 rebin xmin   xmax    ymin    ymax,   xlabel                                             ylabel
    Histogram("cutFlow", "", False, True, default_norm, 1, 0, 13, 1e-1*y_scale, 1e23*y_scale, "Selection", y_title),

    # Histogram("BestLooseMuonsVertex_DSA_vxy"                    , "", False, True, default_norm, 20 , 0, 1000  , 1e-1, 1e8, "#mu vertex v_{xy} [cm]"                 , y_title),
    # Histogram("BestLooseMuonsVertex_DSA_vxySigma"               , "", False, True, default_norm, 80 , 0, 200  , 1e-3, 1e8, "#mu vertex #sigma_{v_{xy}} [cm]"        , y_title),
    # Histogram("BestLooseMuonsVertex_DSA_vxySignificance"        , "", False, True, default_norm, 5  , 0, 150  , 1e-3, 1e8, "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , y_title),
    # Histogram("BestLooseMuonsVertex_Pat_vxy"                    , "", False, True, default_norm, 20 , 0, 600  , 1e-1, 1e8, "#mu vertex v_{xy} [cm]"                 , y_title),
    # Histogram("BestLooseMuonsVertex_Pat_vxySigma"               , "", False, True, default_norm, 20  , 0, 10   , 1e-1, 1e8, "#mu vertex #sigma_{v_{xy}} [cm]"        , y_title),
    # Histogram("BestLooseMuonsVertex_Pat_vxySignificance"        , "", False, True, default_norm, 20 , 0, 1000 , 1e-1, 1e8, "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , y_title),
    # Histogram("BestLooseMuonsVertex_PatDSA_vxy"                    , "", False, True, default_norm, 20 , 0, 1000  , 1e-1, 1e8, "#mu vertex v_{xy} [cm]"                 , y_title),
    # Histogram("BestLooseMuonsVertex_PatDSA_vxySigma"               , "", False, True, default_norm, 80 , 0, 200  , 1e-3, 1e8, "#mu vertex #sigma_{v_{xy}} [cm]"        , y_title),
    # Histogram("BestLooseMuonsVertex_PatDSA_vxySignificance"        , "", False, True, default_norm, 20 , 0, 800  , 1e-3, 1e8, "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , y_title),
    
    Histogram("GoodBestLooseMuonsVertex_DSA_vxy"                , "", False, True, default_norm, 20 , 0, 800  , 1e-3, 1e8, "#mu vertex v_{xy} [cm]"                 , y_title),
    Histogram("GoodBestLooseMuonsVertex_DSA_vxySigma"           , "", False, True, default_norm, 200, 0, 200  , 1e-3, 1e8, "#mu vertex #sigma_{v_{xy}} [cm]"        , y_title),
    Histogram("GoodBestLooseMuonsVertex_DSA_vxySignificance"    , "", False, True, default_norm, 5  , 0, 200  , 1e-3, 1e8, "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , y_title),
    Histogram("GoodBestLooseMuonsVertex_Pat_vxy"                , "", False, True, default_norm, 5  , 0, 140  , 1e-3, 1e8, "#mu vertex v_{xy} [cm]"                 , y_title),
    Histogram("GoodBestLooseMuonsVertex_Pat_vxySigma"           , "", False, True, default_norm, 20 , 0, 10   , 1e-3, 1e8, "#mu vertex #sigma_{v_{xy}} [cm]"        , y_title),
    Histogram("GoodBestLooseMuonsVertex_Pat_vxySignificance"    , "", False, True, default_norm, 40 , 0, 1000 , 1e-3, 1e8, "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , y_title),
    Histogram("GoodBestLooseMuonsVertex_PatDSA_vxy"             , "", False, True, default_norm, 40 , 0, 800  , 1e-3, 1e8, "#mu vertex v_{xy} [cm]"                 , y_title),
    Histogram("GoodBestLooseMuonsVertex_PatDSA_vxySigma"        , "", False, True, default_norm, 200, 0, 100  , 1e-3, 1e8, "#mu vertex #sigma_{v_{xy}} [cm]"        , y_title),
    Histogram("GoodBestLooseMuonsVertex_PatDSA_vxySignificance" , "", False, True, default_norm, 20 , 0, 800  , 1e-3, 1e8, "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , y_title),
    
    # Histogram("LooseMuonsVertexSegmentMatch_DSA_vxy"            , "", False, True, default_norm, 20 , 0, 1000  , 1e-1, 1e8, "#mu vertex v_{xy} [cm]"                 , y_title),
    # Histogram("LooseMuonsVertexSegmentMatch_DSA_vxySigma"       , "", False, True, default_norm, 80 , 0, 200   , 1e-1, 1e8, "#mu vertex #sigma_{v_{xy}} [cm]"        , y_title),
    # Histogram("LooseMuonsVertexSegmentMatch_DSA_vxySignificance", "", False, True, default_norm, 10 , 0, 400 , 1e-1, 1e8, "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , y_title),
    # Histogram("LooseMuonsVertexSegmentMatch_Pat_vxy"            , "", False, True, default_norm, 40 , 0, 600  , 1e-1, 1e8, "#mu vertex v_{xy} [cm]"                 , y_title),
    # Histogram("LooseMuonsVertexSegmentMatch_Pat_vxySigma"       , "", False, True, default_norm, 20  , 0, 10   , 1e-1, 1e8, "#mu vertex #sigma_{v_{xy}} [cm]"        , y_title),
    # Histogram("LooseMuonsVertexSegmentMatch_Pat_vxySignificance", "", False, True, default_norm, 40 , 0, 1000 , 1e-1, 1e8, "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , y_title),
    # Histogram("LooseMuonsVertexSegmentMatch_PatDSA_vxy"            , "", False, True, default_norm, 20 , 0, 1000  , 1e-1, 1e8, "#mu vertex v_{xy} [cm]"                 , y_title),
    # Histogram("LooseMuonsVertexSegmentMatch_PatDSA_vxySigma"       , "", False, True, default_norm, 80 , 0, 200   , 1e-1, 1e8, "#mu vertex #sigma_{v_{xy}} [cm]"        , y_title),
    # Histogram("LooseMuonsVertexSegmentMatch_PatDSA_vxySignificance", "", False, True, default_norm, 20 , 0, 800 , 1e-1, 1e8, "#mu vertex v_{xy}/#sigma_{v_{xy}} [cm]" , y_title),
)

weightsBranchName = "genWeight"

color_palette_wong = (
    TColor.GetColor(230, 159, 0),
    TColor.GetColor(86, 180, 233),
    TColor.GetColor(0, 158, 115),
    TColor.GetColor(0, 114, 178),
    TColor.GetColor(213, 94, 0),
)

signal_samples = (

    Sample(
        name="tta_mAlp-1GeV_ctau-1e0mm",
        file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e0mm/{skim}/{hist_path}/histograms.root",
        type=SampleType.signal,
        cross_sections=cross_sections,
        line_alpha=1,
        line_style=1,
        fill_alpha=0,
        marker_size=0,
        line_color=ROOT.kViolet,
        legend_description="m_{a} = 1 GeV, c#tau_{a} = 1 mm",
    ),
    Sample(
        name="tta_mAlp-1GeV_ctau-1e1mm",
        file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e1mm/{skim}/{hist_path}/histograms.root",
        type=SampleType.signal,
        cross_sections=cross_sections,
        line_alpha=1,
        line_style=1,
        fill_alpha=0,
        marker_size=0,
        line_color=ROOT.kBlue,
        legend_description="m_{a} = 1 GeV, c#tau_{a} = 1 cm",
    ),
    Sample(
        name="tta_mAlp-1GeV_ctau-1e2mm",
        file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e2mm/{skim}/{hist_path}/histograms.root",
        type=SampleType.signal,
        cross_sections=cross_sections,
        line_alpha=1,
        line_style=1,
        fill_alpha=0,
        marker_size=0,
        line_color=ROOT.kCyan,
        legend_description="m_{a} = 1 GeV, c#tau_{a} = 10 cm",
    ),
    Sample(
        name="tta_mAlp-1GeV_ctau-1e3mm",
        file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e3mm/{skim}/{hist_path}/histograms.root",
        type=SampleType.signal,
        cross_sections=cross_sections,
        line_alpha=1,
        line_style=1,
        fill_alpha=0,
        marker_size=0,
        line_color=ROOT.kGreen+1,
        legend_description="m_{a} = 1 GeV, c#tau_{a} = 1 m",
    ),
    Sample(
        name="tta_mAlp-1GeV_ctau-1e5mm",
        file_path=f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e5mm/{skim}/{hist_path}/histograms.root",
        type=SampleType.signal,
        cross_sections=cross_sections,
        line_alpha=1,
        line_style=1,
        fill_alpha=0,
        marker_size=0,
        line_color=ROOT.kOrange,
        legend_description="m_{a} = 1 GeV, c#tau_{a} = 100 m",
    ),
)

background_samples = (

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

    Sample(
        name="TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTToHadronic/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kRed+3,
        fill_alpha=1.0,
        marker_size=0,
        legend_description="tt (hadronic)",
    ),

    Sample(
        name="TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTTo2L2Nu/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kRed+4,
        fill_alpha=1.0,
        marker_size=0,
        legend_description="tt (leptonic)",
    ),

    Sample(
        name="ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/ST_tW_top/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[1],
        fill_alpha=0.7,
        marker_size=0,
        legend_description="Single top (tW)",
        custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-1*legend_height,
                             legend_max_x-legend_width, legend_max_y-0*legend_height, "f")
    ),
    Sample(
        name="ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/ST_tW_antitop/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[1],
        fill_alpha=0.7,
        marker_size=0,
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, "")
    ),

    # Sample(
    #   name="ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
    #   file_path=f"{base_path}/backgrounds2018/ST_t-channel_top/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    #   line_alpha=0,
    #   fill_color=color_palette_wong[2],
    #   fill_alpha=0.7,
    #   marker_size=0,
    #   legend_description="Single top (t-ch.)",
    #   custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-2*legend_height, legend_max_x-legend_width, legend_max_y-1*legend_height, "f")
    # ),
    Sample(
        name="ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
        file_path=f"{base_path}/backgrounds2018/ST_t-channel_antitop/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[2],
        fill_alpha=0.7,
        marker_size=0,
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, "")
    ),

    Sample(
        name="DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
        file_path=f"{base_path}/backgrounds2018/DYJetsToMuMu_M-10to50/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kMagenta+1,
        fill_alpha=0.7,
        marker_size=0,
        # legend_description="DY",
        # custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-3*legend_height, legend_max_x-legend_width, legend_max_y-2*legend_height, "f"),
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, ""),
    ),
    Sample(
        name="DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
        file_path=f"{base_path}/backgrounds2018/DYJetsToMuMu_M-50/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kMagenta+1,
        fill_alpha=0.7,
        marker_size=0,
        legend_description="DY",
        custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-3*legend_height,
                             legend_max_x-legend_width, legend_max_y-2*legend_height, "f"),
        # legend_description=" ",
        # custom_legend=Legend(0, 0, 0, 0, ""),
    ),

    Sample(
        name="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
        file_path=f"{base_path}/backgrounds2018/WJetsToLNu/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kViolet+1,
        fill_alpha=0.7,
        marker_size=0,
        legend_description="W+jets",
    ),

    # Sample(
    #   name="ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8",
    #   file_path=f"{base_path}/backgrounds2018/ttZJets/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    #   line_alpha=0,
    #   fill_color=41,
    #   fill_alpha=0.7,F
    #   marker_size=0,
    #   legend_description="ttZJets",
    # ),
    Sample(
        name="TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTZToLLNuNu_M-10/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kYellow+3,
        fill_alpha=0.7,
        marker_size=0,
        legend_description="ttZ",
    ),
    Sample(
        name="TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTZToLL_M-1to10/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kGray,
        fill_alpha=0.7,
        marker_size=0,
        legend_description="ttZ (1-10)",
    ),

    # Sample(
    #   name="ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8",
    #   file_path=f"{base_path}/backgrounds2018/ttWJets/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    #   line_alpha=0,
    #   fill_color=ROOT.kOrange,
    #   fill_alpha=0.7,
    #   marker_size=0,
    #   legend_description="ttWJets",
    # ),
    Sample(
        name="TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTWJetsToLNu/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kYellow+1,
        fill_alpha=0.7,
        marker_size=0,
        legend_description="ttW",
    ),

    # Sample(
    #   name="ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8",
    #   file_path=f"{base_path}/backgrounds2018/ttHToMuMu/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    #   line_alpha=0,
    #   fill_color=color_palette_wong[3],
    #   fill_alpha=1.0,
    #   marker_size=0,
    #   legend_description="ttH (#mu#mu)",
    # ),
    Sample(
        name="ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/ttHTobb/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[4],
        fill_alpha=1.0,
        marker_size=0,
        legend_description="ttH (bb)",
    ),
    Sample(
        name="ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/ttHToNonbb/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kBlue+1,
        fill_alpha=1.0,
        marker_size=0,
        legend_description="ttH (non-bb)",
    ),

    Sample(
        name="TTZZ_TuneCP5_13TeV-madgraph-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTZZ/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kGray+1,
        fill_alpha=0.7,
        marker_size=0,
        legend_description="ttZZ",
    ),
    Sample(
        name="TTZH_TuneCP5_13TeV-madgraph-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTZH/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=ROOT.kGray+2,
        fill_alpha=0.7,
        marker_size=0,
        legend_description="ttZH",
    ),
    # Sample(
    #   name="TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
    #   file_path=f"{base_path}/backgrounds2018/TTTT/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    #   line_alpha=0,
    #   fill_color=ROOT.kGray+3,
    #   fill_alpha=0.7,
    #   marker_size=0,
    #   legend_description="TTTT",
    # ),

    Sample(
        name="QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-15To20/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[0],
        fill_alpha=1.0,
        marker_size=0,
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, "")
    ),
    Sample(
        name="QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-20To30/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[0],
        fill_alpha=1.0,
        marker_size=0,
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, "")
    ),
    # # Sample(
    # #   name="QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    # #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-30To50/{skim}/{hist_path}/histograms.root",
    # #   type=SampleType.background,
    # #   cross_sections=cross_sections,
    # #   line_alpha=0,
    # #   fill_color=color_palette_wong[0],
    # #   fill_alpha=1.0,
    # #   marker_size=0,
    # #   legend_description=" ",
    # #   custom_legend=Legend(0, 0, 0, 0, "")
    # # ),
    # Sample(
    #   name="QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-50To80/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    #   line_alpha=0,
    #   fill_color=color_palette_wong[0],
    #   fill_alpha=1.0,
    #   marker_size=0,
    #   legend_description=" ",
    #   custom_legend=Legend(0, 0, 0, 0, "")
    # ),
    # # Sample(
    # #   name="QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    # #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-80To120/{skim}/{hist_path}/histograms.root",
    # #   type=SampleType.background,
    # #   cross_sections=cross_sections,
    # #   line_alpha=0,
    # #   fill_color=color_palette_wong[0],
    # #   fill_alpha=1.0,
    # #   marker_size=0,
    # #   legend_description=" ",
    # #   custom_legend=Legend(0, 0, 0, 0, "")
    # # ),
    Sample(
        name="QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-120To170/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[0],
        fill_alpha=1.0,
        marker_size=0,
        # legend_description="QCD (#mu enriched)",
        # custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, ""),
    ),
    Sample(
        name="QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-170To300/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[0],
        fill_alpha=1.0,
        marker_size=0,
        legend_description="QCD (#mu enriched)",
        custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height,
                             legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
        # legend_description=" ",
        # custom_legend=Legend(0, 0, 0, 0, ""),
    ),
    Sample(
        name="QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-300To470/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[0],
        fill_alpha=1.0,
        marker_size=0,
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, "")
    ),
    Sample(
        name="QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-470To600/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[0],
        fill_alpha=1.0,
        marker_size=0,
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, "")
    ),
    Sample(
        name="QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-600To800/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[0],
        fill_alpha=1.0,
        marker_size=0,
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, "")
    ),
    Sample(
        name="QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-800To1000/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
        fill_color=color_palette_wong[0],
        fill_alpha=1.0,
        marker_size=0,
        # legend_description="QCD (#mu enriched)",
        # custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
        legend_description=" ",
        custom_legend=Legend(0, 0, 0, 0, "")
    ),
    # Sample(
    #   name="QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #   file_path=f"{base_path}/backgrounds2018/QCD_Pt-1000/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    #   line_alpha=0,
    #   fill_color=color_palette_wong[0],
    #   fill_alpha=1.0,
    #   marker_size=0,
    #   legend_description="QCD (#mu enriched)",
    #   custom_legend=Legend(legend_max_x-2*legend_width, legend_max_y-4*legend_height, legend_max_x-legend_width, legend_max_y-3*legend_height, "f"),
    #   # legend_description=" ",
    #   # custom_legend=Legend(0, 0, 0, 0, "")
    # ),
)

samples = signal_samples
if plot_background:
    samples = samples + background_samples


# custom_stacks_order = (
#     "SingleMuon",


#     "ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8",
#     "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
#     "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",

#     "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
#     "TTZH_TuneCP5_13TeV-madgraph-pythia8",
#     "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",

#     "ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8",
#     "ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8",
#     "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",

#     "DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
#     "DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",

#     "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
#     "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",


#     "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
#     "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",

#     "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
#     "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",

#     "QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
#     "QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",

#     "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
#     "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
#     "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",

#     "tta_mAlp-0p35GeV_ctau-1e-5mm",
#     "tta_mAlp-0p35GeV_ctau-1e0mm",
#     "tta_mAlp-0p35GeV_ctau-1e1mm",
#     "tta_mAlp-0p35GeV_ctau-1e2mm",
#     "tta_mAlp-0p35GeV_ctau-1e3mm",
#     "tta_mAlp-0p35GeV_ctau-1e5mm",

#     "tta_mAlp-1GeV_ctau-1e-5mm",
#     "tta_mAlp-1GeV_ctau-1e0mm",
#     "tta_mAlp-1GeV_ctau-1e1mm",
#     "tta_mAlp-1GeV_ctau-1e2mm",
#     "tta_mAlp-1GeV_ctau-1e3mm",
#     "tta_mAlp-1GeV_ctau-1e5mm",
# )
