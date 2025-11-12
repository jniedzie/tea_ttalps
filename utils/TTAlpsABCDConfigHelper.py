from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity
from Sample import Sample, SampleType
from ttalps_samples_list import dasBackgrounds2018,dasSignals2018
from ttalps_samples_list import dasBackgrounds2017,dasSignals2017
from ttalps_samples_list import dasBackgrounds2016preVFP,dasSignals2016preVFP
from ttalps_samples_list import dasBackgrounds2016postVFP,dasSignals2016postVFP
from ttalps_samples_list import dasBackgrounds2022preEE,dasSignals2022preEE
from ttalps_samples_list import dasBackgrounds2022postEE,dasSignals2022postEE
from ttalps_samples_list import dasBackgrounds2023preBPix,dasSignals2023preBPix
from ttalps_samples_list import dasBackgrounds2023postBPix,dasSignals2023postBPix

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
      background_input[year] = globals()[f"dasBackgrounds{year}"]

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
      signal_input[year] = globals()[f"dasSignals{year}"]
      
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
      signal_inputs[year] = globals()[f"dasSignals{year}"]
    
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
