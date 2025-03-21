
luminosities = {
  "2016preVFP": 0.,
  "2016postVFP": 0.,
  "2017": 0.,
  "2018": 59820., 
  "2022preEE": 3508.191415, # 2022preEE eras SingleMuonC and MuonD
  "2022postEE": 20861.879243, # 2022postEE eras MuonG and MuonF
  "2023preBPix": 0.,
  "2023postBPix": 0.,
}

def get_luminosity(year):
  if year in luminosities:
    return luminosities[year]
  else:
    warn(f"Luminosity for year {year} is not defined. Luminosity set to 1.")
    return 1.
