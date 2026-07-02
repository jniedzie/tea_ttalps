from Logger import error, warn

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

luminosity_uncertainties = {
  "2016": {
    "lumi_13TeV_1516_l" : 1.0118,
    "lumi_13TeV_151617_l": 1.0004,
    "lumi_13TeV_15161718_l": 1.0035,
  },
  "2017": {
    "lumi_13TeV_151617_l": 1.0055,
    "lumi_13TeV_15161718_l": 1.0061,
  },
  "2018": {
    "lumi_13TeV_15161718_l": 1.0084,
  },
  "2022": {
    "lumi_1": 1.0138,
  },
  "2023": {
    "lumi_1": 1.0017,
    "lumi_2": 1.0127,
  }
}

luminosity_uncertainties_Run2_comb = {
  "lumi_13TeV_15161718_l": 1.0073,
}

luminosity_uncertainties_Run3_comb = {
  "lumi_2223_l": 1.0101,
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

def get_luminosity_uncertainty(year):
  if year in luminosity_uncertainties and luminosity_uncertainties[year] != 0:
    return luminosity_uncertainties[year]
  elif year == "2016preVFP" or year == "2016postVFP":
    return luminosity_uncertainties["2016"]
  elif year == "2022preEE" or year == "2022postEE":
    return luminosity_uncertainties["2022"]
  elif year == "2023preBPix" or year == "2023postBPix":
    return luminosity_uncertainties["2023"]
  else:
    error(f"Luminosity uncertainty for year {year} is not defined. Luminosity uncertainty set to 1.")
    return 1.

def get_luminosity_uncertainty_for_years(years):
  if len(years) == 1:
    return get_luminosity_uncertainty(years[0])
  
  if len(years) == 2:
    if {"2016preVFP", "2016postVFP"}.issubset(set(years)) or {"2022preEE", "2022postEE"}.issubset(set(years)) or {"2023preBPix", "2023postBPix"}.issubset(set(years)):
        return get_luminosity_uncertainty(years[0])
  
  lumi_uncertainty_dict = {}
  if {"2016preVFP", "2016postVFP", "2017", "2018"}.issubset(set(years)):
    lumi_uncertainty_dict.update(luminosity_uncertainties_Run2_comb)
  if {"2022preEE", "2022postEE", "2023preBPix", "2023postBPix"}.issubset(set(years)):  
    lumi_uncertainty_dict.update(luminosity_uncertainties_Run3_comb)
  
  if not lumi_uncertainty_dict:
    warn(f"No combined luminosity uncertainty found for years {years}. Returning individual luminosity uncertainties for each year.")
    for year in years:
      lumi_uncertainty_dict.update(get_luminosity_uncertainty(year))

  return lumi_uncertainty_dict

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
