from Logger import error

luminosities = {
    "2016preVFP": 0.,
    "2016postVFP": 0.,
    "2017": 0.,
    "2018": 59820.,
    "2022preEE": 7970.89,  # 2022preEE eras SingleMuonC, MuonC and MuonD
    "2022postEE": 26667.15,  # 2022postEE eras MuonE, MuonG and MuonF
    "2023preBPix": 0.,
    "2023postBPix": 0.,
}


def get_luminosity(year):
  if year in luminosities:
    return luminosities[year]
  else:
    error(f"Luminosity for year {year} is not defined. Luminosity set to 1.")
    return 1.
