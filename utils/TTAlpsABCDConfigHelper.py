from ttalps_cross_sections import get_cross_sections
from Sample import Sample, SampleType
from ttalps_samples_list import dasSignals2018, dasSignals2018_30GeV, dasBackgrounds2018


class TTAlpsABCDConfigHelper:
  def __init__(self, year, skim, base_path, hist_path):
    self.year = year
    self.skim = skim
    self.base_path = base_path
    self.hist_path = hist_path
    self.cross_sections = get_cross_sections(year)

  def get_background_params(self, backgrounds):
    background_params = []
    for b in backgrounds:
      for k, v in self.cross_sections.items():
        if b in k:
          background_params.append((b, v))
          break

    return background_params

  def get_background_samples(self, backgrounds_to_exclude):
    background_samples = []
    backgrounds = []
    
    for name in dasBackgrounds2018:
      skip = False
      for exclude in backgrounds_to_exclude:
        if exclude in name:
          skip = True
          break

      if skip:
        continue

      backgrounds.append(name.split("/")[-1])

      background_samples.append(
          Sample(
              name=name.split("/")[-1],
              file_path=f"{self.base_path}/{name}/{self.skim[0]}/{self.hist_path}/histograms.root",
              type=SampleType.background,
              cross_sections=self.cross_sections,
          )
      )
    return background_samples, backgrounds
