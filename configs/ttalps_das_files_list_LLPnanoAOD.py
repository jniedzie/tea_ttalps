max_files = 1

base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms"
# base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"

skim = "skimmed_looseSemimuonic"
# skim = "skimmed_looseSemimuonic_looseMuon_looseBjet"
# skim = "skimmed_looseSemimuonic_looseMuon_looseBjet_goldenJson"

# skim = "histograms_pileup"

# file_name = "02D6A1FE-C8EB-1A48-8B31-149FDFB64893.root"

# dbs_instance = "prod/global"
dbs_instance = "prod/phys03"

# input_output_dirs = (
  # tt̄
#   (f"{base_path}/backgrounds2018/TTToSemiLeptonic/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim}/"),
#   (f"{base_path}/backgrounds2018/TTTo2L2Nu/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/TTTo2L2Nu/{skim}/"),

#   # # Single top
#   (f"{base_path}/backgrounds2018/ST_tW_antitop/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/ST_tW_antitop/{skim}/"),
#   (f"{base_path}/backgrounds2018/ST_t-channel_top/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/ST_t-channel_top/{skim}/"),

#   # # DY
#   (f"{base_path}/backgrounds2018/DYJetsToMuMu_M-50/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/DYJetsToMuMu_M-50/{skim}/"),

#   # # W+jets
#   (f"{base_path}/backgrounds2018/WJetsToLNu/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/WJetsToLNu/{skim}/"),

#   # # ttV
#   (f"{base_path}/backgrounds2018/ttZJets/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/ttZJets/{skim}/"),
#   # ("",
#   #  f"{base_path}/backgrounds2018/ttWJets/{skim}/"),

#   # # ttH
#   (f"{base_path}/backgrounds2018/ttHToNonbb/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/ttHToNonbb/{skim}/"),
  
# # TTZZ, TTZH, TTTT
#   (f"{base_path}/backgrounds2018/TTZH/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/TTZH/{skim}/"),

# # QCD mu enriched
#   # ("",
#   #  f"{base_path}/backgrounds2018/QCD_Pt_30to50_MuEnriched/{skim}/"),
#   # ("",
#   #  f"{base_path}/backgrounds2018/QCD_Pt_80to120_MuEnriched/{skim}/"),
#   (f"{base_path}/backgrounds2018/QCD_Pt-170To300/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/QCD_Pt-170To300/{skim}/"),
#   (f"{base_path}/backgrounds2018/QCD_Pt-300To470/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/QCD_Pt-300To470/{skim}/"),
#   (f"{base_path}/backgrounds2018/QCD_Pt-470To600/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/QCD_Pt-470To600/{skim}/"),
#   (f"{base_path}/backgrounds2018/QCD_Pt-600To800/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/QCD_Pt-600To800/{skim}/"),
#   (f"{base_path}/backgrounds2018/QCD_Pt-1000/LLPnanoAODv2merged/",
#    f"{base_path}/backgrounds2018/QCD_Pt-1000/{skim}/"),

# )

datasets_and_output_trees_dirs = (
# # # tt̄
#   ("",
#    f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim}/"),
  ("/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_TTToHadronic_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/TTToHadronic/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/TTTo2L2Nu/{skim}/"),

# # Single top
#   ("",
#    f"{base_path}/backgrounds2018/ST_tW_antitop/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/ST_tW_top/{skim}/"),
  ("/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_ST_t-channel_antitop_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/ST_t-channel_antitop/{skim}/"),
  ("/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_ST_tW_top_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/ST_t-channel_top/{skim}/"),

# # DY
  ("/DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/lrygaard-LLPnanoAODv1_lrygaard-crab_DYJetsToMuMu_M-10to50_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/DYJetsToMuMu_M-10to50/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/DYJetsToMuMu_M-50/{skim}/"),

# # W+jets
#   ("",
#    f"{base_path}/backgrounds2018/WJetsToLNu/{skim}/"),

# # ttV
  ("/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_TTZToLLNuNu_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/TTZToLLNuNu/{skim}/"),
  ("/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_TTZToLL_M-1to10_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/TTZToLLNuNu_M-1to10/{skim}/"),
#   # ("",
#   #  f"{base_path}/backgrounds2018/ttZJets/{skim}/"),

  ("/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/TTWJetsToLNu/{skim}/"),
#   # ("",
#   #  f"{base_path}/backgrounds2018/ttWJets/{skim}/"),

# # ttH
  ("/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/ttHTobb/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/ttHToNonbb/{skim}/"),
  
# # TTZZ, TTZH, TTTT
  ("/TTZZ_TuneCP5_13TeV-madgraph-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_TTZZ_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/TTZZ/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/TTZH/{skim}/"),
#   ("/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_TTTT_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#    f"{base_path}/backgrounds2018/TTTT/{skim}/"),

# # QCD mu enriched
  ("/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_QCD_Pt-15To20_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/QCD_Pt_15to20_MuEnriched/{skim}/"),
  ("/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v1-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/QCD_Pt_20to30_MuEnriched/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/QCD_Pt_30to50_MuEnriched/{skim}/"),
  ("/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v1-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/QCD_Pt_50to80_MuEnriched/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/QCD_Pt_80to120_MuEnriched/{skim}/"),
  ("/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/QCD_Pt_120to170_MuEnriched/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/QCD_Pt_170to300_MuEnriched/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/QCD_Pt_300to470_MuEnriched/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/QCD_Pt_470to600_MuEnriched/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/QCD_Pt_600to800_MuEnriched/{skim}/"),
  ("/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
   f"{base_path}/backgrounds2018/QCD_Pt_800to1000_MuEnriched/{skim}/"),
#   ("",
#    f"{base_path}/backgrounds2018/QCD_Pt_1000_MuEnriched/{skim}/"),

# # Data LLPnanoAODs
# ("",
#   f"{base_path}/data/SingleMuonA/{skim}/"),
## 3 files are missing in SingleMuonB
("/SingleMuon/lrygaard-LLPnanoAODv1_lrygaard-crab_SingleMuonB_LLPminiAOD-9cdbfc999b77f606d32dabc67655eebd-00000000000000000000000000000000/USER",
  f"{base_path}/data/SingleMuonB/{skim}/"),
# ("",
#   f"{base_path}/data/SingleMuonC/{skim}/"),
# ("",
#   f"{base_path}/data/SingleMuonD/{skim}/"),

## Signals LLPnanoAODs
  ("/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e0mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e0mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e1mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e1mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e2mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e2mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e3mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e3mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e5mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e-5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-0p35GeV_ctau-1e-5mm/{skim}/"),

  ("/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e0mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e0mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e1mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e1mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e2mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e2mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e3mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e3mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e5mm/{skim}/"),
  ("/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e-5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  f"{base_path}/signals/tta_mAlp-1GeV_ctau-1e-5mm/{skim}/"),  
)

# # this has to be here, otherwise the script will not work:
dataset = ""
output_trees_dir = ""
output_hists_dir = ""
input_directory = ""
