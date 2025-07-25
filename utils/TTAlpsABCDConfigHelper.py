from ttalps_cross_sections import get_cross_sections
from Sample import Sample, SampleType
from ttalps_samples_list import dasBackgrounds2018, dasSignals2018, dasBackgrounds2022postEE, dasSignals2022postEE


class TTAlpsABCDConfigHelper:
  def __init__(self, year, background_skim, category, base_path, background_hist_path):
    self.year = year
    self.background_skim = background_skim
    self.category = category
    self.base_path = base_path
    self.background_hist_path = background_hist_path
    self.cross_sections = get_cross_sections(year)

  def get_background_params(self, backgrounds):
    background_params = []
    for b in backgrounds:
      for k, v in self.cross_sections.items():
        if b in k:
          background_params.append((b, v))
          break

    return background_params

  def get_background_samples(self, year="2018"):
    background_samples = []
    backgrounds = []

    background_input = dasBackgrounds2018
    if year == "2022postEE":
      background_input = dasBackgrounds2022postEE

    for name in background_input:
      backgrounds.append(name.split("/")[-1])

      background_samples.append(
          Sample(
              name=name.split("/")[-1],
              file_path=f"{self.base_path}/{name}/{self.background_skim[0]}/{self.background_hist_path}/histograms.root",
              type=SampleType.background,
              cross_sections=self.cross_sections,
          )
      )
    return background_samples, backgrounds

  def get_signal_as_background_samples(self, year="2018"):
    background_samples = []
    backgrounds = []

    signal_input = dasSignals2018
    if year == "2022postEE":
      signal_input = dasSignals2022postEE
    
    for name in signal_input:
      backgrounds.append(name.split("/")[-1])

      background_samples.append(
          Sample(
              name=name.split("/")[-1],
              file_path=f"{self.base_path}/{name}/{self.background_skim[0]}/{self.background_hist_path}/histograms.root",
              type=SampleType.background,
              cross_sections=self.cross_sections,
          )
      )
    return background_samples, backgrounds
