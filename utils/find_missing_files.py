import os
import glob

# Loose skims
# skim = "skimmed_looseSemimuonic_tightMuon/"
# skim = "skimmed_looseSemimuonic_tightMuon_newBtag/"
# skim = "skimmed_looseSemimuonic/"
skim = "skimmed_looseSemimuonic_looseMuon_looseBjet/"

# CRs and SRs
# skim = "skimmed_ttbarSemimuonicCR_tightMuon/"
# skim = "skimmed_ttbarSemimuonicCR_tightMuon_newBtag/"
# skim = "skimmed_ttbarSemimuonicCR/"
# skim = "skimmed_ttZSemimuonicCR_tightMuon_noLooseMuonIso/"

# Histograms
# skim = "skimmed_ttbarLike/histograms/"

base_path = "/data/dust/user/jniedzie/ttalps_cms"

samples = (
# tt̄
#   ("/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/TTToSemiLeptonic/{skim}/"),

# # Single top
#   ("/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
#    f"{base_path}/backgrounds2018/ST_tW_antitop/{skim}/"),
#   ("/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/ST_tW_top/{skim}/"),
#   ("/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/ST_t-channel_antitop/{skim}/"),
#   ("/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/ST_t-channel_top/{skim}/"),

# # DY
#   ("/DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/DYJetsToMuMu_M-10to50/{skim}/"),
#   ("/DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
#    f"{base_path}/backgrounds2018/DYJetsToMuMu_M-50/{skim}/"),

# # W+jets
#   ("/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/WJetsToLNu/{skim}/"),

# # ttV
#   ("/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/TTZToLLNuNu/{skim}/"),
#   ("/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/TTZToLLNuNu_M-1to10/{skim}/"),
#   # ("/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
#   #  f"{base_path}/backgrounds2018/ttZJets/{skim}/"),

#   ("/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/TTWJetsToLNu/{skim}/"),
#   # ("/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
#   #  f"{base_path}/backgrounds2018/ttWJets/{skim}/"),

# # ttH
#   ("/ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/ttHToMuMu/{skim}/"),
#   ("/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/ttHTobb/{skim}/"),
#   ("/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
#    f"{base_path}/backgrounds2018/ttHToNonbb/{skim}/"),
  
# # TTZZ, TTZH, TTTT
#   ("/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#    f"{base_path}/backgrounds2018/TTZZ/{skim}/"),
#   ("/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
#    f"{base_path}/backgrounds2018/TTZH/{skim}/"),
#   ("/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
#    f"{base_path}/backgrounds2018/TTTT/{skim}/"),


# QCD
  # ("/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_15to30/{skim}/"),
  # ("/QCD_Pt_30to50_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_30to50/{skim}/"),
  # ("/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_50to80/{skim}/"),
  # ("/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_80to120/{skim}/"),
  # ("/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_120to170/{skim}/"),
  # ("/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_170to300/{skim}/"),
  # ("/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_300to470/{skim}/"),
  # ("/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_470to600/{skim}/"),
  # ("/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_600to800/{skim}/"),
  # ("/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_800to1000/{skim}/"),
  # ("/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_1000to1400/{skim}/"),
  # ("/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_1400to1800/{skim}/"),
  # ("/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_1800to2400/{skim}/"),
  # ("/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_2400to3200/{skim}/"),
  # ("/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
  # f"{base_path}/backgrounds2018/QCD_Pt_3200toInf/{skim}/"),

  # QCD mu enriched
  # ("/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_15to20_MuEnriched/{skim}/"),
  # ("/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_20to30_MuEnriched/{skim}/"),
  # ("/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_30to50_MuEnriched/{skim}/"),
  # ("/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_50to80_MuEnriched/{skim}/"),
  # ("/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_80to120_MuEnriched/{skim}/"),
  # ("/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_120to170_MuEnriched/{skim}/"),
  # ("/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_170to300_MuEnriched/{skim}/"),
  # ("/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_300to470_MuEnriched/{skim}/"),
  # ("/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_470to600_MuEnriched/{skim}/"),
  # ("/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_600to800_MuEnriched/{skim}/"),
  # ("/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_800to1000_MuEnriched/{skim}/"),
  # ("/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #  f"{base_path}/backgrounds2018/QCD_Pt_1000_MuEnriched/{skim}/"),


  # Data
  ("/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD",
   f"{base_path}/collision_data2018/SingleMuon2018A/{skim}/"),
  # ("/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD",
  #  f"{base_path}/collision_data2018/SingleMuon2018B/{skim}/"),
  # ("/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD",
  #  f"{base_path}/collision_data2018/SingleMuon2018C/{skim}/"),
  # ("/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD",
  #  f"{base_path}/collision_data2018/SingleMuon2018D/{skim}/"),
)

def main():
  
  for dataset, output_dir in samples:
    print(f"\n\nSearching in {output_dir}")
    input_files = glob.glob(output_dir + "/*.root")
    input_files = [file.split("/")[-1] for file in input_files]

    das_files = os.popen(f"dasgoclient -query='file dataset={dataset}'").read().split("\n")
    
    print(f"DAS path: {'/'.join(das_files[0].split('/')[0:-1])}")
    
    das_files = [file.split("/")[-1] for file in das_files]
    
    for file in das_files:
      if file not in input_files:
        print(file)
  

if __name__ == '__main__':
  main()
  
  
# ./ttalps_skimmer ttalps_skimmer_ttbarLike_config.py /data/dust/user/jniedzie/ttalps_cms/backgrounds2018/DYJetsToMuMu_M-50/skimmed_looseSemileptonic/2D47004A-E7E8-4A49-9EA2-374FAB2437BA.root /data/dust/user/jniedzie/ttalps_cms/backgrounds2018/DYJetsToMuMu_M-50/skimmed_ttbarLike/2D47004A-E7E8-4A49-9EA2-374FAB2437BA.root

# ./ttalps_skimmer ttalps_skimmer_ttbarLike_config.py /data/dust/user/jniedzie/ttalps_cms/backgrounds2018/ST_tW_antitop/skimmed_looseSemileptonic/EEA943A9-2FA6-634D-AAAA-66055F00E547.root /data/dust/user/jniedzie/ttalps_cms/backgrounds2018/ST_tW_antitop/skimmed_ttbarLike/EEA943A9-2FA6-634D-AAAA-66055F00E547.root

# ./ttalps_histogrammer ttalps_histogrammer_default_config.py /data/dust/user/jniedzie/ttalps_cms/backgrounds2018/TTToSemiLeptonic/skimmed_ttZLike/10AE0CA0-AD1E-5A47-8437-B0D867A62B80.root /data/dust/user/jniedzie/ttalps_cms/backgrounds2018/TTToSemiLeptonic/skimmed_ttZLike/histograms/10AE0CA0-AD1E-5A47-8437-B0D867A62B80.root