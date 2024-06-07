
# local samples

backgrounds2018 = (
  "backgrounds2018/TTToSemiLeptonic",
  "backgrounds2018/TTToHadronic",
  "backgrounds2018/TTTo2L2Nu",

  "backgrounds2018/TTZToLLNuNu_M-10",
  "backgrounds2018/TTZToLL_M-1to10",
  
  "backgrounds2018/ST_tW_antitop",
  "backgrounds2018/ST_t-channel_antitop",
  "backgrounds2018/ST_tW_top",
  # # "backgrounds2018/ST_t-channel_top",
  
  "backgrounds2018/DYJetsToMuMu_M-50",
  "backgrounds2018/DYJetsToMuMu_M-10to50",
    
  # "backgrounds2018/ttWJets",
  "backgrounds2018/TTWJetsToLNu",
  "backgrounds2018/WJetsToLNu",
  
  "backgrounds2018/ttHToMuMu",
  "backgrounds2018/ttHTobb",
  "backgrounds2018/ttHToNonbb",
  
  "backgrounds2018/TTZZ",
  "backgrounds2018/TTZH",
  # # "backgrounds2018/TTTT",
  
  # # # # # # # QCD (LLPnanoAOD mu enhanced)
  "backgrounds2018/QCD_Pt-15To20",
  "backgrounds2018/QCD_Pt-20To30",
  # # "backgrounds2018/QCD_Pt-30To50",
  # # "backgrounds2018/QCD_Pt-50To80",
  # # "backgrounds2018/QCD_Pt-80To120",
  "backgrounds2018/QCD_Pt-120To170",
  "backgrounds2018/QCD_Pt-170To300",
  "backgrounds2018/QCD_Pt-300To470",
  "backgrounds2018/QCD_Pt-470To600",
  "backgrounds2018/QCD_Pt-600To800",
  "backgrounds2018/QCD_Pt-800To1000",
  # # "backgrounds2018/QCD_Pt-1000",
)

data2018 = (
  # "collision_data2018/SingleMuon2018A",
  "collision_data2018/SingleMuon2018B",
  # "collision_data2018/SingleMuon2018C",
  # "collision_data2018/SingleMuon2018D",
)

signals2018 = (
  # "signals/tta_mAlp-0p35GeV_ctau-1e0mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e1mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e2mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e3mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e5mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e-5mm",

  "signals/tta_mAlp-1GeV_ctau-1e0mm",
  "signals/tta_mAlp-1GeV_ctau-1e1mm",
  "signals/tta_mAlp-1GeV_ctau-1e2mm",
  "signals/tta_mAlp-1GeV_ctau-1e3mm",
  "signals/tta_mAlp-1GeV_ctau-1e5mm",
  "signals/tta_mAlp-1GeV_ctau-1e-5mm",
)

# DAS samples

dasBackgrounds2018 = {
#   "backgrounds2018/TTToSemiLeptonic" : "",
  "backgrounds2018/TTToHadronic" : "/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_TTToHadronic_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#   "backgrounds2018/TTTo2L2Nu" : "",

  "backgrounds2018/TTZToLLNuNu_M-10" : "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_TTZToLLNuNu_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
  "backgrounds2018/TTZToLL_M-1to10" : "/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_TTZToLL_M-1to10_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
  
#   "backgrounds2018/ST_tW_antitop" : "",
  "backgrounds2018/ST_t-channel_antitop" : "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_ST_t-channel_antitop_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
  "backgrounds2018/ST_tW_top" : "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_ST_tW_top_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#   "backgrounds2018/ST_t-channel_top" : "",
  
#   "backgrounds2018/DYJetsToMuMu_M-50" : "",
  "backgrounds2018/DYJetsToMuMu_M-10to50" : "/DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/lrygaard-LLPnanoAODv1_lrygaard-crab_DYJetsToMuMu_M-10to50_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
    
#   "backgrounds2018/ttWJets" : "",
  "backgrounds2018/TTWJetsToLNu" : "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#   "backgrounds2018/WJetsToLNu" : "",
  
#   "backgrounds2018/ttHToMuMu" : "",
  "backgrounds2018/ttHTobb" : "/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#   "backgrounds2018/ttHToNonbb" : "",
  
  "backgrounds2018/TTZZ" : "/TTZZ_TuneCP5_13TeV-madgraph-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_TTZZ_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#   "backgrounds2018/TTZH" : "",
#   "backgrounds2018/TTTT" : "",
  
  "backgrounds2018/QCD_Pt-15To20" : "/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_QCD_Pt-15To20_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
  "backgrounds2018/QCD_Pt-20To30" : "/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v1-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#   "backgrounds2018/QCD_Pt-30To50" : "",
  "backgrounds2018/QCD_Pt-50To80" : "/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v1-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#   "backgrounds2018/QCD_Pt-80To120" : "",
  "backgrounds2018/QCD_Pt-120To170" : "/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#   "backgrounds2018/QCD_Pt-170To300" : "",
#   "backgrounds2018/QCD_Pt-300To470" : "",
#   "backgrounds2018/QCD_Pt-470To600" : "",
#   "backgrounds2018/QCD_Pt-600To800" : "",
  "backgrounds2018/QCD_Pt-800To1000" : "/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
#   "backgrounds2018/QCD_Pt-1000" : "",
}

dasData2018 = {
#   "collision_data2018/SingleMuon2018A" : "",
  "collision_data2018/SingleMuon2018B" : "/SingleMuon/lrygaard-LLPnanoAODv1_lrygaard-crab_SingleMuonB_LLPminiAOD-9cdbfc999b77f606d32dabc67655eebd-00000000000000000000000000000000/USER",
#   "collision_data2018/SingleMuon2018C" : "",
#   "collision_data2018/SingleMuon2018D" : "",
}

dasSignals2018 = {
  "signals/tta_mAlp-0p35GeV_ctau-1e0mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e0mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e1mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e1mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e2mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e2mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e3mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e3mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e5mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e-5mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e-5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",

  "signals/tta_mAlp-1GeV_ctau-1e0mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e0mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e1mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e1mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e2mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e2mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e3mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e3mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e5mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e-5mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e-5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
}
