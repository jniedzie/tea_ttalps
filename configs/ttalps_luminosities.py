from Logger import error

luminosities = {
    "2016preVFP": 19493.,
    "2016postVFP": 16811.,
    "2017": 41475.,
    "2018": 59820.,
    "2022preEE": 7970.89,  # 2022preEE eras SingleMuonC, MuonC and MuonD
    "2022postEE": 26667.15,  # 2022postEE eras MuonE, MuonG and MuonF
    "2023preBPix": 17794.,  # CMS recommendation 17.794 fb-1
    "2023postBPix": 9451.,  # CMS recommendation 9.451 fb-1
}

default_luminosity_uncertainties = {
    "2016preVFP": 1.012,
    "2016postVFP": 1.012,
    "2017": 1.023,
    "2018": 1.025,
    "2022preEE": 1.014,
    "2022postEE": 1.014,
    "2023preBPix": 1.013,
    "2023postBPix": 1.013,
}
uncorrelated_luminosity_uncertainties = {
    "2016preVFP": 1.01,
    "2016postVFP": 1.01,
    "2017": 1.02,
    "2018": 1.015,
}

correlated_luminosity_uncertainties = {
    "2016,2017,2018": {
        "2016": 1.006,
        "2017": 1.009,
        "2018": 1.02,
    },
    "2017,2018": {
        "2017": 1.006,
        "2018": 1.002,
    }
}


def get_luminosity(year):
  if year in luminosities and luminosities[year] != 0:
    return luminosities[year]
  else:
    error(f"Luminosity for year {year} is not defined. Luminosity set to 1.")
    return 1.


def get_luminosity_uncertainty_default(year):
  if year in default_luminosity_uncertainties and default_luminosity_uncertainties[year] != 0:
    return default_luminosity_uncertainties[year]
  else:
    error(f"Default luminosity uncertainty for year {year} is not defined. Luminosity uncertainty set to 1.")
    return 1.


def get_luminosity_uncertainty_uncorrelated(year):
  if year in uncorrelated_luminosity_uncertainties and uncorrelated_luminosity_uncertainties[year] != 0:
    return uncorrelated_luminosity_uncertainties[year]
  else:
    error(f"Uncorrelated luminosity uncertainty for year {year} is not defined. Luminosity uncertainty set to 1.")
    return 1.


def get_luminosity_uncertainty_correlated2016to2018(year):
  uncertainties = correlated_luminosity_uncertainties["2016,2017,2018"]
  if year in uncertainties and uncertainties[year] != 0:
    return uncertainties[year]
  else:
    error(
        f"2016-2018 correlated luminosity uncertainty for year {year} is not defined. Luminosity uncertainty set to 1.")
    return 1.


def get_luminosity_uncertainty_correlated2017to2018(year):
  uncertainties = correlated_luminosity_uncertainties["2017,2018"]
  if year in uncertainties and uncertainties[year] != 0:
    return uncertainties[year]
  else:
    error(
        f"2017-2018 correlated luminosity uncertainty for year {year} is not defined. Luminosity uncertainty set to 1.")
    return 1.
