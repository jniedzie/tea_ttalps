from Sample import Sample, SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType
from ttalps_cross_sections import *

base_path = "/data/dust/user/lrygaard/ttalps_cms/"

# For signal like skim: SR and J/Psi CR with no isolation requirement on the loose muons
# skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"
skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_corrected"

# SR dimuon cuts applied
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons"

output_path = f"../datacards/"

# If True, poisson error on empty bins (1.84) will be added to data histograms
add_uncertainties_on_zero = False

# signal_name = "tta_mAlp-1GeV_ctau-1e-5mm"
signal_name = "tta_mAlp-1GeV_ctau-1e0mm"
# signal_name = "tta_mAlp-1GeV_ctau-1e1mm"
# signal_name = "tta_mAlp-1GeV_ctau-1e2mm"
# signal_name = "tta_mAlp-1GeV_ctau-1e3mm"
# signal_name = "tta_mAlp-1GeV_ctau-1e5mm"

# signal_name = "tta_mAlp-2GeV_ctau-1e0mm"
# signal_name = "tta_mAlp-2GeV_ctau-1e1mm"
# signal_name = "tta_mAlp-2GeV_ctau-1e2mm"
# signal_name = "tta_mAlp-2GeV_ctau-1e3mm"

# signal_name = "tta_mAlp-12GeV_ctau-1e0mm"
# signal_name = "tta_mAlp-70GeV_ctau-1e0mm"

luminosity = 59830. # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2
include_shapes = True

samples = (
    Sample(
        name="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    Sample(
        name="TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTToHadronic/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    Sample(
        name="TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTTo2L2Nu/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    Sample(
        name="ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/ST_tW_top/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/ST_tW_antitop/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    Sample(
      name="ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
      file_path=f"{base_path}/backgrounds2018/ST_t-channel_top/{skim}/{hist_path}/histograms.root",
      type=SampleType.background,
      cross_sections=cross_sections,
    ),
    Sample(
        name="ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
        file_path=f"{base_path}/backgrounds2018/ST_t-channel_antitop/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    Sample(
        name="DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
        file_path=f"{base_path}/backgrounds2018/DYJetsToMuMu_M-10to50/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos",
        file_path=f"{base_path}/backgrounds2018/DYJetsToMuMu_M-50/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    Sample(
        name="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
        file_path=f"{base_path}/backgrounds2018/WJetsToLNu/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    # Sample(
    #   name="ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8",
    #   file_path=f"{base_path}/backgrounds2018/ttZJets/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    # ),
    Sample(
        name="TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTZToLLNuNu_M-10/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTZToLL_M-1to10/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    # Sample(
    #   name="ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8",
    #   file_path=f"{base_path}/backgrounds2018/ttWJets/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    # ),
    Sample(
        name="TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTWJetsToLNu/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    # Sample(
    #   name="ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8",
    #   file_path=f"{base_path}/backgrounds2018/ttHToMuMu/{skim}/{hist_path}/histograms.root",
    #   type=SampleType.background,
    #   cross_sections=cross_sections,
    # ),
    Sample(
        name="ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/ttHTobb/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",
        file_path=f"{base_path}/backgrounds2018/ttHToNonbb/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),

    Sample(
        name="TTZZ_TuneCP5_13TeV-madgraph-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTZZ/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="TTZH_TuneCP5_13TeV-madgraph-pythia8",
        file_path=f"{base_path}/backgrounds2018/TTZH/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
      name="TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
      file_path=f"{base_path}/backgrounds2018/TTTT/{skim}/{hist_path}/histograms.root",
      type=SampleType.background,
      cross_sections=cross_sections,
    ),

    Sample(
        name="QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-15To20/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-20To30/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
      name="QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
      file_path=f"{base_path}/backgrounds2018/QCD_Pt-30To50/{skim}/{hist_path}/histograms.root",
      type=SampleType.background,
      cross_sections=cross_sections,
    ),
    Sample(
      name="QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
      file_path=f"{base_path}/backgrounds2018/QCD_Pt-50To80/{skim}/{hist_path}/histograms.root",
      type=SampleType.background,
      cross_sections=cross_sections,
    ),
    Sample(
      name="QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
      file_path=f"{base_path}/backgrounds2018/QCD_Pt-80To120/{skim}/{hist_path}/histograms.root",
      type=SampleType.background,
      cross_sections=cross_sections,
    ),
    Sample(
        name="QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-120To170/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-170To300/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-300To470/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-470To600/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-600To800/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
        name="QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-800To1000/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    Sample(
      name="QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
      file_path=f"{base_path}/backgrounds2018/QCD_Pt-1000/{skim}/{hist_path}/histograms.root",
      type=SampleType.background,
      cross_sections=cross_sections,
    ),


    Sample(
        name="signal_"+signal_name,
        file_path=f"{base_path}/signals/{signal_name}/{skim}/{hist_path}/histograms.root",
        type=SampleType.signal,
        cross_sections=cross_sections,
    ),
    
    # Sample(
    #     name="data_obs",
    #     file_path=f"{base_path}/histograms/data.root",
    #     type=SampleType.data,
    # ),
)

# List histograms for which to create datacards
histograms = [
    # Histogram(name="LooseMuonsDRMatch_dxyPVTrajSig", norm_type=NormalizationType.to_lumi, x_max=90.0, rebin=1),
    
    # Histogram(name="BestIsoDimuonVertex_DSA_Lxy"               , norm_type=NormalizationType.to_lumi, x_max=800    , rebin=20  ),
    # Histogram(name="BestIsoDimuonVertex_DSA_vxySigma"          , norm_type=NormalizationType.to_lumi, x_max=200    , rebin=200 ),
    # Histogram(name="BestIsoDimuonVertex_DSA_vxySignificance"   , norm_type=NormalizationType.to_lumi, x_max=200    , rebin=5   ),
    
    # Histogram(name="BestIsoDimuonVertex_Pat_Lxy"               , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),
    # Histogram(name="BestIsoDimuonVertex_Pat_vxySigma"          , norm_type=NormalizationType.to_lumi, x_max=10     , rebin=20  ),
    # Histogram(name="BestIsoDimuonVertex_Pat_vxySignificance"   , norm_type=NormalizationType.to_lumi, x_max=1000   , rebin=40  ),
    
    # Histogram(name="BestIsoDimuonVertex_PatDSA_Lxy"            , norm_type=NormalizationType.to_lumi, x_max=800    , rebin=40  ),
    # Histogram(name="BestIsoDimuonVertex_PatDSA_vxySigma"       , norm_type=NormalizationType.to_lumi, x_max=100    , rebin=200 ),
    # Histogram(name="BestIsoDimuonVertex_PatDSA_vxySignificance", norm_type=NormalizationType.to_lumi, x_max=800    , rebin=20  ),

    Histogram(name="BestPFIsoDimuonVertex_Pat_Lxy"               , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),
    Histogram(name="BestPFIsoDimuonVertex_PatDSA_Lxy"            , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),
    Histogram(name="BestPFIsoDimuonVertex_DSA_Lxy"               , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),

    # Histogram(name="BestPFIsoDimuonVertex_Pat_LxySignificance"     , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),
    # Histogram(name="BestPFIsoDimuonVertex_PatDSA_LxySignificance"  , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),    
    # Histogram(name="BestPFIsoDimuonVertex_DSA_LxySignificance"     , norm_type=NormalizationType.to_lumi, x_max=140    , rebin=5   ),
]


# output_path = f"../datacards/datacard_{histograms[0].getName()}_{signal_name}_displacedIso"
output_path = f"../datacards/datacard_{histograms[0].getName()}_{signal_name}_pfIso"

background_name = [sample.name for sample in samples if sample.type == SampleType.background]

# List nuisance parameters (they will only be added for processes for which they were listed)
nuisances = {
    "bck_syst": {name: 1.1 for name in background_name},
    "signal_unc": {
        "signal_"+signal_name: 1.05,
    }
}


# # combineCards.py datacard_BestPFIsoDimuonVertex_Pat_Lxy_tta_mAlp-1GeV_ctau-1e-5mm.txt datacard_BestPFIsoDimuonVertex_PatDSA_Lxy_tta_mAlp-1GeV_ctau-1e-5mm.txt datacard_BestPFIsoDimuonVertex_DSA_Lxy_tta_mAlp-1GeV_ctau-1e-5mm.txt > datacard_BestPFIsoDimuonVertex_combined_Lxy_tta_mAlp-1GeV_ctau-1e-5mm.txt
# combineCards.py datacard_BestPFIsoDimuonVertex_Pat_Lxy_tta_mAlp-1GeV_ctau-1e0mm.txt datacard_BestPFIsoDimuonVertex_PatDSA_Lxy_tta_mAlp-1GeV_ctau-1e0mm.txt datacard_BestPFIsoDimuonVertex_DSA_Lxy_tta_mAlp-1GeV_ctau-1e0mm.txt > datacard_BestPFIsoDimuonVertex_combined_Lxy_tta_mAlp-1GeV_ctau-1e0mm.txt
# combineCards.py datacard_BestPFIsoDimuonVertex_Pat_Lxy_tta_mAlp-1GeV_ctau-1e1mm.txt datacard_BestPFIsoDimuonVertex_PatDSA_Lxy_tta_mAlp-1GeV_ctau-1e1mm.txt datacard_BestPFIsoDimuonVertex_DSA_Lxy_tta_mAlp-1GeV_ctau-1e1mm.txt > datacard_BestPFIsoDimuonVertex_combined_Lxy_tta_mAlp-1GeV_ctau-1e1mm.txt
# combineCards.py datacard_BestPFIsoDimuonVertex_Pat_Lxy_tta_mAlp-1GeV_ctau-1e2mm.txt datacard_BestPFIsoDimuonVertex_PatDSA_Lxy_tta_mAlp-1GeV_ctau-1e2mm.txt datacard_BestPFIsoDimuonVertex_DSA_Lxy_tta_mAlp-1GeV_ctau-1e2mm.txt > datacard_BestPFIsoDimuonVertex_combined_Lxy_tta_mAlp-1GeV_ctau-1e2mm.txt
# combineCards.py datacard_BestPFIsoDimuonVertex_Pat_Lxy_tta_mAlp-1GeV_ctau-1e3mm.txt datacard_BestPFIsoDimuonVertex_PatDSA_Lxy_tta_mAlp-1GeV_ctau-1e3mm.txt datacard_BestPFIsoDimuonVertex_DSA_Lxy_tta_mAlp-1GeV_ctau-1e3mm.txt > datacard_BestPFIsoDimuonVertex_combined_Lxy_tta_mAlp-1GeV_ctau-1e3mm.txt
# # combineCards.py datacard_BestPFIsoDimuonVertex_Pat_Lxy_tta_mAlp-1GeV_ctau-1e5mm.txt datacard_BestPFIsoDimuonVertex_PatDSA_Lxy_tta_mAlp-1GeV_ctau-1e5mm.txt datacard_BestPFIsoDimuonVertex_DSA_Lxy_tta_mAlp-1GeV_ctau-1e5mm.txt > datacard_BestPFIsoDimuonVertex_combined_Lxy_tta_mAlp-1GeV_ctau-1e5mm.txt
