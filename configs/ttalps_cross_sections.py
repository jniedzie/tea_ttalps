
signal_xsec_scale = 1e1


def get_theory_cross_section(mass):
  # these are calculated at coupling 0.1
  
  cross_section_for_mass = {
      0.35: 0.003912,  # +- 2.935e-05 pb
      1.0: 0.004088,  # +- 3.1e-05 pb,
      2.0: 0.004233,  # +- 3.199e-05 pb
      12.0: 0.004019,  # +- 3.065e-05 pb
      30.0: 0.003504,  # +- 2.162e-05 pb
      60.0: 0.002679,  # +- 1.323e-05 pb
      70.0: 0.002438,  # +- 1.888e-05 pb
      # "TTALPto2Mu_MALP-2": 0.004233,  # +- 3.199e-05 pb
  }
  return cross_section_for_mass[mass]


# Cross sections in (pb) from XSDB
cross_sectionsRun2 = {
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8": 365.34,
    "TTToHadronic_TuneCP5_13TeV-powheg-pythia8": 377.96,
    "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8": 88.29,

    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8": 32.45,
    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8": 32.51,
    "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8": 115.3,
    "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8": 69.09,

    "DYJetsToMuMu_M-10to50_H2ErratumFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos": 7013.0,
    "DYJetsToMuMu_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos": 1976.0,

    "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8": 52850.0,
    "W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8": 9024.0,
    "W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8": 2832.0,
    "W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8": 820.7,
    "W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8": 385.5,

    "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8":  0.2439,  # 0.28136
    "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8": 0.05324,
    # "TTZToLL_TuneCP5_13TeV_amcatnlo-pythia8": 0.07468,
    "TTZToQQ_TuneCP5_13TeV_amcatnlo-pythia8": 0.5104,  # 0.5297
    "ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8": 5.407,  # 0.5407,

    "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8": 0.2163,
    "ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8": 0.4611,

    # ttHToMuMu cross section is wrong and shouldn't be used by us
    "ttHToMuMu_M125_TuneCP5_13TeV-powheg-pythia8": 0.5269,
    # ttH cross sections from HIG-19-011 (ttH H to bb Run 2)
    "ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8": 0.2953,
    "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8": 0.2118,

    "TTZZ_TuneCP5_13TeV-madgraph-pythia8": 0.001386,
    "TTZH_TuneCP5_13TeV-madgraph-pythia8": 0.00113,
    "TTTT_TuneCP5_13TeV-amcatnlo-pythia8": 0.008213,

    "TT4b_TuneCP5_13TeV_madgraph_pythia8": 0.06784,
    "TTbb_tttosemileptonic_TuneCP5-Powheg-Openloops-Pythia8": 19.2,
    "TTbb_ttto2l2nu_TuneCP5-Powheg-Openloops-Pythia8": 4.6,
    "TTbb_tttohadronic_TuneCP5-Powheg-Openloops-Pythia8": 19.9,

    "BBLLNuNu_TuneCP5_13TeV-powheg-pythia8": 80.91,

    "QCD_Pt_15to30_TuneCP5_13TeV_pythia8": 1248000000.0,
    "QCD_Pt_30to50_TuneCP5_13TeV_pythia8": 106600000.0,
    "QCD_Pt_50to80_TuneCP5_13TeV_pythia8": 15680000.0,
    "QCD_Pt_80to120_TuneCP5_13TeV_pythia8": 2363000.0,
    "QCD_Pt_120to170_TuneCP5_13TeV_pythia8": 406800.0,
    "QCD_Pt_170to300_TuneCP5_13TeV_pythia8": 103300.0,
    "QCD_Pt_300to470_TuneCP5_13TeV_pythia8": 6826.0,
    "QCD_Pt_470to600_TuneCP5_13TeV_pythia8": 552.6,
    "QCD_Pt_600to800_TuneCP5_13TeV_pythia8": 156.6,
    "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8": 26.32,
    "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8": 7.5,
    "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8": 0.6479,
    "QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8": 0.08715,
    "QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8": 0.005242,
    "QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8": 0.0001349,

    "QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 2800000.0,
    "QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 2527000.0,
    "QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1367000.0,
    "QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 381700.0,
    "QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 87740.0,
    "QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 21280.0,
    "QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 7000.0,
    "QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 622.6,
    "QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 58.9,
    "QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 18.12,
    "QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 3.318,
    "QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8": 1.085,

    "SingleMuon2018": 1.0,
    "EGamma2018": 1.0,

    "tta_mAlp-0p35GeV_ctau-1e-5mm": signal_xsec_scale * get_theory_cross_section(0.35),
    "tta_mAlp-0p35GeV_ctau-1e0mm": signal_xsec_scale * get_theory_cross_section(0.35),
    "tta_mAlp-0p35GeV_ctau-1e1mm": signal_xsec_scale * get_theory_cross_section(0.35),
    "tta_mAlp-0p35GeV_ctau-1e2mm": signal_xsec_scale * get_theory_cross_section(0.35),
    "tta_mAlp-0p35GeV_ctau-1e3mm": 100*signal_xsec_scale * get_theory_cross_section(0.35),
    "tta_mAlp-0p35GeV_ctau-1e5mm": 100*signal_xsec_scale * get_theory_cross_section(0.35),
    "tta_mAlp-0p35GeV_ctau-1e7mm": 100*signal_xsec_scale * get_theory_cross_section(0.35),

    "tta_mAlp-1GeV_ctau-1e-5mm": signal_xsec_scale * get_theory_cross_section(1.0),
    "tta_mAlp-1GeV_ctau-1e0mm": signal_xsec_scale * get_theory_cross_section(1.0),
    "tta_mAlp-1GeV_ctau-1e1mm": signal_xsec_scale * get_theory_cross_section(1.0),
    "tta_mAlp-1GeV_ctau-1e2mm": signal_xsec_scale * get_theory_cross_section(1.0),
    "tta_mAlp-1GeV_ctau-1e3mm": 10 * signal_xsec_scale * get_theory_cross_section(1.0),
    "tta_mAlp-1GeV_ctau-1e5mm": 10 * signal_xsec_scale * get_theory_cross_section(1.0),

    "tta_mAlp-2GeV_ctau-1e-5mm": signal_xsec_scale * get_theory_cross_section(2.0),
    "tta_mAlp-2GeV_ctau-1e0mm": signal_xsec_scale * get_theory_cross_section(2.0),
    "tta_mAlp-2GeV_ctau-1e1mm": signal_xsec_scale * get_theory_cross_section(2.0),
    "tta_mAlp-2GeV_ctau-1e2mm": signal_xsec_scale * get_theory_cross_section(2.0),
    "tta_mAlp-2GeV_ctau-1e3mm": 10 * signal_xsec_scale * get_theory_cross_section(2.0),

    "tta_mAlp-12GeV_ctau-1e-5mm": signal_xsec_scale * get_theory_cross_section(12.0),
    "tta_mAlp-12GeV_ctau-1e0mm": signal_xsec_scale * get_theory_cross_section(12.0),
    "tta_mAlp-12GeV_ctau-1e1mm": signal_xsec_scale * get_theory_cross_section(12.0),
    "tta_mAlp-12GeV_ctau-1e2mm": signal_xsec_scale * get_theory_cross_section(12.0),
    "tta_mAlp-12GeV_ctau-1e3mm": 10 * signal_xsec_scale * get_theory_cross_section(12.0),

    "tta_mAlp-30GeV_ctau-1e-5mm": signal_xsec_scale * get_theory_cross_section(30.0),
    "tta_mAlp-30GeV_ctau-1e0mm": signal_xsec_scale * get_theory_cross_section(30.0),
    "tta_mAlp-30GeV_ctau-1e1mm": signal_xsec_scale * get_theory_cross_section(30.0),
    "tta_mAlp-30GeV_ctau-1e2mm": signal_xsec_scale * get_theory_cross_section(30.0),
    "tta_mAlp-30GeV_ctau-1e3mm": 10 * signal_xsec_scale * get_theory_cross_section(30.0),

    "tta_mAlp-60GeV_ctau-1e-5mm": signal_xsec_scale * get_theory_cross_section(60.0),
    "tta_mAlp-60GeV_ctau-1e0mm": signal_xsec_scale * get_theory_cross_section(60.0),
    "tta_mAlp-60GeV_ctau-1e1mm": signal_xsec_scale * get_theory_cross_section(60.0),
    "tta_mAlp-60GeV_ctau-1e2mm": signal_xsec_scale * get_theory_cross_section(60.0),
    "tta_mAlp-60GeV_ctau-1e3mm": 10 * signal_xsec_scale * get_theory_cross_section(60.0),

    "tta_mAlp-70GeV_ctau-1e0mm": signal_xsec_scale * get_theory_cross_section(70.0),
}

cross_sectionsRun3 = {
    "Muon2022preEE": 1.0,
    "Muon2022postEE": 1.0,
    "TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8": 405.8099,
    "TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8": 98.0963,
    "TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8": 19.36,
    "TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8": 19.36,
    "WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8": 64481.58,  # 62552.7
    "TTLL_MLL-4to50_TuneCP5_13p6TeV_amcatnlo-pythia8": 0.03949,
    "TTLL_MLL-50_TuneCP5_13p6TeV_amcatnlo-pythia8": 0.08646,
    "TTHto2B_M-125_TuneCP5_13p6TeV_powheg-pythia8": 0.331968,
    # Cross sections from XSDB
    "TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8": 123.8,
    "TTto4Q_TuneCP5Up_13p6TeV_powheg-pythia8": 762.1,
    "DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8": 5558.0,  # 6345.99
    "WtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8": 55390.0,
    "TTHtoNon2B_M-125_TuneCP5_13p6TeV_powheg-pythia8": 0.5742,
    "TTZZ_TuneCP5_13p6TeV_madgraph-madspin-pythia8": 0.001579,
    "TTZH_TuneCP5_13p6TeV_madgraph-pythia8": 0.001288,
    "TTTT_TuneCP5_13p6TeV_amcatnlo-pythia8": 0.009652,
    # QCD from XSDB
    "QCD_PT-15To20_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 2982000.0,  # 2022 postEE: 2960000.0
    "QCD_PT-20To30_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 2679000.0,
    "QCD_PT-30To50_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 1465000.0,  # miniaodsim v2: 1497000.0
    "QCD_PT-50To80_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 402900.0,  # 2022 postEE: 409500.0
    "QCD_PT-80To120_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 95130.0,  # 2022 postEE: 96200.0,
    "QCD_PT-120To170_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 22980.0,
    "QCD_PT-170To300_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 7763.0,
    "QCD_PT-300To470_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 699.1,
    "QCD_PT-470To600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 68.24,
    "QCD_PT-600To800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 21.37,
    "QCD_PT-800To1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 3.913,
    "QCD_PT-1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8": 1.323,
}


def get_cross_sections(year):
  if year == "2016preVFP" or year == "2016postVFP" or year == "2017" or year == "2018":
    return cross_sectionsRun2
  elif year == "2022preEE" or year == "2022postEE" or year == "2023preBPix" or year == "2023postBPix":
    return cross_sectionsRun3
  else:
    raise ValueError(f"Year {year} not supported.")
