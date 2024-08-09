
#####     LOCAL SAMPLES     #####

###   2018   ###

TT_backgrounds2018 = (
  "backgrounds2018/TTToSemiLeptonic",
  "backgrounds2018/TTToHadronic",
  "backgrounds2018/TTTo2L2Nu",

  "backgrounds2018/TTZToLLNuNu_M-10",
  "backgrounds2018/TTZToLL_M-1to10",

  "backgrounds2018/TTZZ",
  "backgrounds2018/TTZH",
  "backgrounds2018/TTTT",

  "backgrounds2018/TTWJetsToLNu",

  "backgrounds2018/ttHTobb",
  "backgrounds2018/ttHToNonbb",
)
ST_backgrounds2018 = ( 
  "backgrounds2018/ST_tW_antitop",
  "backgrounds2018/ST_t-channel_antitop",
  "backgrounds2018/ST_tW_top",
  "backgrounds2018/ST_t-channel_top",
)
DY_backgrounds2018 = (
  "backgrounds2018/DYJetsToMuMu_M-50",
  "backgrounds2018/DYJetsToMuMu_M-10to50",
)
V_backgrounds2018 = (
  "backgrounds2018/WJetsToLNu",
)
QCD_backgrounds2018 = (
  "backgrounds2018/QCD_Pt-15To20",
  "backgrounds2018/QCD_Pt-20To30",
  # # "backgrounds2018/QCD_Pt-30To50",
  "backgrounds2018/QCD_Pt-50To80",
  "backgrounds2018/QCD_Pt-80To120",
  "backgrounds2018/QCD_Pt-120To170",
  "backgrounds2018/QCD_Pt-170To300",
  "backgrounds2018/QCD_Pt-300To470",
  "backgrounds2018/QCD_Pt-470To600",
  "backgrounds2018/QCD_Pt-600To800",
  "backgrounds2018/QCD_Pt-800To1000",
  "backgrounds2018/QCD_Pt-1000",
)
backgrounds2018 = TT_backgrounds2018 + ST_backgrounds2018 + DY_backgrounds2018 + V_backgrounds2018 + QCD_backgrounds2018
test_backgrounds2018 = (
  "backgrounds2018/TTToHadronic",
)

new_dasBackgrounds2018 = {
  # "backgrounds2018/QCD_Pt-30To50",
  "backgrounds2018/QCD_Pt-80To120",
  # "backgrounds2018/TTToSemiLeptonic",
}

data2018 = (
  # "collision_data2018/SingleMuon2018A",
  "collision_data2018/SingleMuon2018B",
  # "collision_data2018/SingleMuon2018C",
  # "collision_data2018/SingleMuon2018D",
)

signals2018_0p35GeV = (
  "signals/tta_mAlp-0p35GeV_ctau-1e0mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e1mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e2mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e3mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e5mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e-5mm",
)
signals2018_1GeV = (
  "signals/tta_mAlp-1GeV_ctau-1e0mm",
  "signals/tta_mAlp-1GeV_ctau-1e1mm",
  "signals/tta_mAlp-1GeV_ctau-1e2mm",
  "signals/tta_mAlp-1GeV_ctau-1e3mm",
  "signals/tta_mAlp-1GeV_ctau-1e5mm",
  "signals/tta_mAlp-1GeV_ctau-1e-5mm",
)
signals2018 = signals2018_0p35GeV + signals2018_1GeV

test_signals2018 = (
  "signals/tta_mAlp-1GeV_ctau-1e0mm",
)


##############################################################################

#####     DAS SAMPLES     #####

TT_dasBackgrounds2018 = {
#   "backgrounds2018/TTToSemiLeptonic" : "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/TTToHadronic" : "/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  "backgrounds2018/TTTo2L2Nu" : "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",

  # "backgrounds2018/TTZToLLNuNu_M-10" : "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/TTZToLL_M-1to10" : "/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",

  # "backgrounds2018/TTWJetsToLNu" : "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",

  # "backgrounds2018/ttHTobb" : "/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/ttHToNonbb" : "/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  
  # "backgrounds2018/TTZZ" : "/TTZZ_TuneCP5_13TeV-madgraph-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/TTZH" : "/TTZH_TuneCP5_13TeV-madgraph-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/TTTT" : "/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
}
ST_dasBackgrounds2018 = {
  # "backgrounds2018/ST_tW_antitop" : "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/ST_t-channel_antitop" : "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/ST_tW_top" : "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  "backgrounds2018/ST_t-channel_top" : "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
}
DY_dasBackgrounds2018 = {
  "backgrounds2018/DYJetsToMuMu_M-50" : "/DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/DYJetsToMuMu_M-10to50" : "/DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
} 
V_dasBackgrounds2018 = {
  "backgrounds2018/WJetsToLNu" : "/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
} 
QCD_dasBackgrounds2018 = {
  # "backgrounds2018/QCD_Pt-15To20" : "/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-crab_QCD_Pt-15To20_LLPminiAOD-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER,",
  "backgrounds2018/QCD_Pt-20To30" : "/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
#   "backgrounds2018/QCD_Pt-30To50" : "",
  # "backgrounds2018/QCD_Pt-50To80" : "/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  "backgrounds2018/QCD_Pt-80To120" : "/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/QCD_Pt-120To170" : "/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
  "backgrounds2018/QCD_Pt-170To300" : "/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  "backgrounds2018/QCD_Pt-300To470" : "/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
#   "backgrounds2018/QCD_Pt-470To600" : "",
  "backgrounds2018/QCD_Pt-600To800" : "/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/QCD_Pt-800To1000" : "/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_lrygaard-LLPminiAODv1_RunIISummer20UL18RECO-106X_v11-v2-c15273f0b6812ff053a850f456209388-00000000000000000000000000000000/USER",
  "backgrounds2018/QCD_Pt-1000" : "/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
}

new_dasBackgrounds2018 = {
  # "backgrounds2018/QCD_Pt-30To50" : "",
  "backgrounds2018/QCD_Pt-80To120" : "/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",
  # "backgrounds2018/TTToSemiLeptonic" : "",
}

dasBackgrounds2018test = {"backgrounds2018/ttHToNonbb" : "/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/lrygaard-LLPnanoAODv1_LLPminiAOD-00000000000000000000000000000000/USER",}
dasBackgrounds2018 = {key: value for d in (TT_dasBackgrounds2018, ST_dasBackgrounds2018, DY_dasBackgrounds2018, V_dasBackgrounds2018, QCD_dasBackgrounds2018) for key, value in d.items()}

dasData2018 = {
#   "collision_data2018/SingleMuon2018A" : "",
  "collision_data2018/SingleMuon2018B" : "/SingleMuon/lrygaard-LLPnanoAODv1_lrygaard-crab_SingleMuonB_LLPminiAOD-9cdbfc999b77f606d32dabc67655eebd-00000000000000000000000000000000/USER",
#   "collision_data2018/SingleMuon2018C" : "",
#   "collision_data2018/SingleMuon2018D" : "",
}

dasSignals2018_0p35GeV = {
  "signals/tta_mAlp-0p35GeV_ctau-1e0mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e0mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e1mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e1mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e2mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e2mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e3mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e3mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e5mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-0p35GeV_ctau-1e-5mm" : "/ttalps/lrygaard-ttalps_m-0p35GeV_ctau-1e-5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
}
dasSignals2018_1GeV = {
  "signals/tta_mAlp-1GeV_ctau-1e0mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e0mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e1mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e1mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e2mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e2mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e3mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e3mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e5mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
  "signals/tta_mAlp-1GeV_ctau-1e-5mm" : "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e-5mm_LLPnanoAODv1-00000000000000000000000000000000/USER",
}
dasSignals2018 = {key: value for d in (dasSignals2018_0p35GeV, dasSignals2018_1GeV) for key, value in d.items()}
