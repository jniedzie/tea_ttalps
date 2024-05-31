from Sample import Sample, SampleType
from Histogram import Histogram
from HistogramNormalizer import NormalizationType
from ttalps_cross_sections import *

base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms/"
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
skim = "skimmed_SRmuonic_DR"


output_path = f"../datacards/"

# If True, poisson error on empty bins (1.84) will be added to data histograms
add_uncertainties_on_zero = False

luminosity = 59830. # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

samples = (
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
    
    # Sample(
    #     name="QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #     file_path=f"{base_path}/backgrounds2018/QCD_Pt-20To30/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    # Sample(
    #     name="QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #     file_path=f"{base_path}/backgrounds2018/QCD_Pt-50To80/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    # Sample(
    #     name="QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #     file_path=f"{base_path}/backgrounds2018/QCD_Pt-80To120/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    # Sample(
    #     name="QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #     file_path=f"{base_path}/backgrounds2018/QCD_Pt-120To170/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    # Sample(
    #     name="QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #     file_path=f"{base_path}/backgrounds2018/QCD_Pt-170To300/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    Sample(
        name="QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-300To470/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
        line_alpha=0,
    ),
    Sample(
        name="QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
        file_path=f"{base_path}/backgrounds2018/QCD_Pt-470To600/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),
    # Sample(
    #     name="QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #     file_path=f"{base_path}/backgrounds2018/QCD_Pt-600To800/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    # Sample(
    #     name="QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #     file_path=f"{base_path}/backgrounds2018/QCD_Pt-800To1000/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    # Sample(
    #     name="QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8",
    #     file_path=f"{base_path}/backgrounds2018/QCD_Pt-1000/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),




    # Sample(
    #     name="signal_tta_mAlp-0p35GeV_ctau-1e0mm",
    #     file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e0mm/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    # Sample(
    #     name="signal_tta_mAlp-0p35GeV_ctau-1e1mm",
    #     file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e1mm/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    # Sample(
    #     name="signal_tta_mAlp-0p35GeV_ctau-1e2mm",
    #     file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e2mm/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    # Sample(
    #     name="signal_tta_mAlp-0p35GeV_ctau-1e3mm",
    #     file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e3mm/{skim}/{hist_path}/histograms.root",
    #     type=SampleType.background,
    #     cross_sections=cross_sections,
    # ),
    Sample(
        name="signal_tta_mAlp-0p35GeV_ctau-1e5mm",
        file_path=f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e3mm/{skim}/{hist_path}/histograms.root",
        type=SampleType.background,
        cross_sections=cross_sections,
    ),


    # Sample(
    #     name="data_obs",
    #     file_path=f"{base_path}/histograms/data.root",
    #     type=SampleType.data,
    # ),
)

# List histograms for which to create datacards
histograms = [Histogram(name="LooseMuonsDRMatch_dxyPVTrajSig",
                        norm_type=NormalizationType.to_lumi,
                        x_max=90.0,
                        rebin=1)]

# List nuisance parameters (they will only be added for processes for which they were listed)
nuisances = {
    "bck_syst": {
        "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8": 1.1,
        "TTToHadronic_TuneCP5_13TeV-powheg-pythia8": 1.1,
        "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8": 1.1,
        "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
        "QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
        "QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
        "QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
        "QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
        "QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
        "QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
        "QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
        "QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
        "QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.1,
    },
    "signal_unc": {
        "signal_tta_mAlp-0p35GeV_ctau-1e0mm": 1.05,
        "signal_tta_mAlp-0p35GeV_ctau-1e1mm": 1.05,
        "signal_tta_mAlp-0p35GeV_ctau-1e2mm": 1.05,
        "signal_tta_mAlp-0p35GeV_ctau-1e3mm": 1.05,
    }
}
