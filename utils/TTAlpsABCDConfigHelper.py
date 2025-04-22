from ttalps_cross_sections import get_cross_sections
from Sample import Sample, SampleType
from ttalps_samples_list import dasSignals2018, dasSignals2018_30GeV, dasBackgrounds2018
from Logger import fatal


class TTAlpsABCDConfigHelper:
  def __init__(self, year, skim, category, base_path, hist_path):
    self.year = year
    self.skim = skim
    self.category = category
    self.base_path = base_path
    self.hist_path = hist_path
    self.cross_sections = get_cross_sections(year)

    if category == "_Pat":
      self.backgrounds_to_exclude = [
          # "TTToSemiLeptonic",
          # "TTToHadronic",
          "TTTo2L2Nu",
          # "TTZToLLNuNu_M-10",
          # "TTZToLL_M-1to10",
          # "TTWJetsToLNu",
          # "ttHTobb",
          # "ttHToNonbb",
          # "TTZZ",
          # "TTZH",
          # "TTTT",
          # "ST_tW_antitop",
          # "ST_t-channel_antitop",
          # "ST_tW_top",
          # "ST_t-channel_top",
          # "DYJetsToMuMu_M-50",
          # "DYJetsToMuMu_M-10to50",
          # "WJetsToLNu",
          "QCD_Pt-15To20",
          "QCD_Pt-20To30",
          "QCD_Pt-30To50",
          "QCD_Pt-50To80",
          "QCD_Pt-80To120",
          "QCD_Pt-120To170",
          "QCD_Pt-170To300",
          # "QCD_Pt-300To470",
          # "QCD_Pt-470To600",
          # "QCD_Pt-600To800",
          # "QCD_Pt-800To1000",
          # "QCD_Pt-1000",
      ]
    elif category == "_PatDSA":
      self.backgrounds_to_exclude = [
          # "TTToSemiLeptonic",
          # "TTToHadronic",
          "TTTo2L2Nu",
          # "TTZToLLNuNu_M-10",
          # "TTZToLL_M-1to10",
          # "TTWJetsToLNu",
          # "ttHTobb",
          # "ttHToNonbb",
          # "TTZZ",
          # "TTZH",
          # "TTTT",
          # "ST_tW_antitop",
          # "ST_t-channel_antitop",
          # "ST_tW_top",
          # "ST_t-channel_top",
          # "DYJetsToMuMu_M-50",
          # "DYJetsToMuMu_M-10to50",
          # "WJetsToLNu",
          # "QCD_Pt-15To20",
          # "QCD_Pt-20To30",
          # "QCD_Pt-30To50",
          # "QCD_Pt-50To80",
          # "QCD_Pt-80To120",
          # "QCD_Pt-120To170",
          # "QCD_Pt-170To300",
          # "QCD_Pt-300To470",
          # "QCD_Pt-470To600",
          # "QCD_Pt-600To800",
          # "QCD_Pt-800To1000",
          # "QCD_Pt-1000",
      ]
    elif category == "_DSA":
      self.backgrounds_to_exclude = [
          # "TTToSemiLeptonic",
          # "TTToHadronic",
          # "TTTo2L2Nu",
          # "TTZToLLNuNu_M-10",
          # "TTZToLL_M-1to10",
          # "TTWJetsToLNu",
          # "ttHTobb",
          # "ttHToNonbb",
          # "TTZZ",
          # "TTZH",
          # "TTTT",
          # "ST_tW_antitop",
          # "ST_t-channel_antitop",
          # "ST_tW_top",
          # "ST_t-channel_top",
          # "DYJetsToMuMu_M-50",
          # "DYJetsToMuMu_M-10to50",
          "WJetsToLNu",
          "QCD_Pt-15To20",
          "QCD_Pt-20To30",
          "QCD_Pt-30To50",
          "QCD_Pt-50To80",
          "QCD_Pt-80To120",
          "QCD_Pt-120To170",
          "QCD_Pt-170To300",
          # "QCD_Pt-300To470",
          # "QCD_Pt-470To600",
          # "QCD_Pt-600To800",
          # "QCD_Pt-800To1000",
          # "QCD_Pt-1000",
      ]
    else:
      fatal(
          f"Category {category} not recognized. Please use one of the following: _Pat, _PatDSA, _DSA"
      )
      exit(0)

  def get_background_params(self, backgrounds):
    background_params = []
    for b in backgrounds:
      for k, v in self.cross_sections.items():
        if b in k:
          background_params.append((b, v))
          break

    return background_params

  def get_background_samples(self):
    background_samples = []
    backgrounds = []

    for name in dasBackgrounds2018:
      skip = False
      for exclude in self.backgrounds_to_exclude:
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
