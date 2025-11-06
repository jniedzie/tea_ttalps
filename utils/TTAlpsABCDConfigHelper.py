from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity
from Sample import Sample, SampleType
from ttalps_samples_list import dasBackgrounds2018,dasBackgrounds2017,dasBackgrounds2016PreVFP,dasBackgrounds2016PostVFP
from ttalps_samples_list import dasBackgrounds2022preEE,dasBackgrounds2022postEE,dasBackgrounds2023preBPix,dasBackgrounds2023postBPix
from ttalps_samples_list import dasSignals2018,dasSignals2017,dasSignals2016PreVFP,dasSignals2016PostVFP
from ttalps_samples_list import dasSignals2022postEE,dasSignals2022preEE,dasSignals2023preBPix,dasSignals2023postBPix


class TTAlpsABCDConfigHelper:
  def __init__(self, years, background_skim, category, base_path, background_hist_path):
    self.years = years
    self.background_skim = background_skim
    self.category = category
    self.base_path = base_path
    self.background_hist_path = background_hist_path

  def get_background_samples(self):
    background_samples = []
    backgrounds = []

    background_input = {}
    for year in self.years:
      if year == "2016preVFP":
        background_input[year] = dasBackgrounds2016PreVFP
      elif year == "2016postVFP":
        background_input[year] = dasBackgrounds2016PostVFP
      elif year == "2017":
        background_input[year] = dasBackgrounds2017
      elif year == "2018":
        background_input[year] = dasBackgrounds2018
      elif year == "2022postEE":
        background_input[year] = dasBackgrounds2022postEE
      elif year == "2022preEE":
        background_input[year] = dasBackgrounds2022preEE
      elif year == "2023preBPix":
        background_input[year] = dasBackgrounds2023preBPix
      elif year == "2023postBPix":
        background_input[year] = dasBackgrounds2023postBPix
      else:
        raise ValueError(f"Year {year} is not supported")

    for year, dasBackgrounds in background_input.items():
      cross_sections = get_cross_sections(year)
      luminosity = get_luminosity(year)
      for name in dasBackgrounds:
        backgrounds.append(name.split("/")[-1])

        background_samples.append(
            Sample(
                name=name.split("/")[-1],
                file_path=f"{self.base_path}/{name}/{self.background_skim[0]}/{self.background_hist_path}/histograms.root",
                type=SampleType.background,
                cross_sections=cross_sections,
                luminosity=luminosity,
                year=year
            )
        )
    return background_samples, backgrounds


  def get_signal_samples(self):
    signal_samples = []
    signals = []

    signal_input = {}
    for year in self.years:
      if year == "2016preVFP":
        signal_input[year] = dasSignals2016PreVFP
      elif year == "2016postVFP":
        signal_input[year] = dasSignals2016PostVFP
      elif year == "2017":
        signal_input[year] = dasSignals2017
      elif year == "2018":
        signal_input[year] = dasSignals2018
      elif year == "2022postEE":
        signal_input[year] = dasSignals2022postEE
      elif year == "2022preEE":
        signal_input[year] = dasSignals2022preEE
      elif year == "2023preBPix":
        signal_input[year] = dasSignals2023preBPix
      elif year == "2023postBPix":
        signal_input[year] = dasSignals2023postBPix
      else:
        raise ValueError(f"Year {year} is not supported")

    for year, dasSignals in signal_input.items():
      cross_sections = get_cross_sections(year)
      luminosity = get_luminosity(year)
      for name in dasSignals:
        signal_name = name.split("/")[-1]
        signals.append(signal_name)

        signal_samples.append(
            Sample(
                name="signal_"+signal_name,
                file_path=f"{self.base_path}/{name}/{self.background_skim[0]}/{self.background_hist_path}/histograms.root",
                type=SampleType.signal,
                cross_sections=cross_sections,
                luminosity=luminosity,
                year=year
            )
        )
    return signal_samples, signals

  def get_signal_as_background_samples(self):
    background_samples = []
    backgrounds = []

    signal_inputs = {}
    for year in self.years:
      if year == "2016preVFP":
        signal_inputs[year] = dasSignals2016PreVFP
      elif year == "2016postVFP":
        signal_inputs[year] = dasSignals2016PostVFP
      elif year == "2017":
        signal_inputs[year] = dasSignals2017
      elif year == "2018":
        signal_inputs[year] = dasSignals2018
      elif year == "2022postEE":
        signal_inputs[year] = dasSignals2022postEE
      elif year == "2022preEE":
        signal_inputs[year] = dasSignals2022preEE
      elif year == "2023preBPix":
        signal_inputs[year] = dasSignals2023preBPix
      elif year == "2023postBPix":
        signal_inputs[year] = dasSignals2023postBPix
      else:
        raise ValueError(f"Year {year} is not supported")
    
    for year, signal_input in signal_inputs.items():
      for name in signal_input:
        backgrounds.append(name.split("/")[-1])
        cross_sections = get_cross_sections(year)
        luminosity = get_luminosity(year)

        background_samples.append(
            Sample(
                name=name.split("/")[-1],
                file_path=f"{self.base_path}/{name}/{self.background_skim[0]}/{self.background_hist_path}/histograms.root",
                type=SampleType.background,
                cross_sections=cross_sections,
                luminosity=luminosity,
                year=year
            )
        )
    return background_samples, backgrounds
