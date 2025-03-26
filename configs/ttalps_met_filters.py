
met_filters_run2_base = {
  "Flag_goodVertices",
  "Flag_globalSuperTightHalo2016Filter",
  "Flag_HBHENoiseFilter",
  "Flag_HBHENoiseIsoFilter",
  "Flag_BadPFMuonFilter",
  "Flag_BadPFMuonDzFilter",
  "Flag_hfNoisyHitsFilter",
  "Flag_eeBadScFilter",
}

met_filters_2017_2018 = {
  "Flag_EcalDeadCellTriggerPrimitiveFilter",
  "Flag_ecalBadCalibFilter",
}

met_filters_2016 = {
  "EcalDeadCellTriggerPrimitiveFilter",
}

# Filters given for preompt-reco Run 3 data and MC, not rereco yet:
met_filters_run3_base = {
  "Flag_goodVertices",
  "Flag_globalSuperTightHalo2016Filter",
  "Flag_BadPFMuonFilter",
  "Flag_BadPFMuonDzFilter",
  "Flag_hfNoisyHitsFilter",
  "Flag_eeBadScFilter",
  "Flag_EcalDeadCellTriggerPrimitiveFilter",
  "Flag_ecalBadCalibFilter",
}

def get_met_filters(year):
  if year == "2016preVFP" or year == "2016postVFP":
    return met_filters_run2_base.union(met_filters_2016)
  elif year == "2018" or year == "2017":
    return met_filters_run2_base.union(met_filters_2017_2018)
  elif year == "2022preEE" or year == "2022postEE" or year == "2023preBPix" or year == "2023postBPix":
    return met_filters_run3_base
