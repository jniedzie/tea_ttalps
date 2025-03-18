from ttalps_samples_list import *
from ttalps_cross_sections import get_cross_sections
from ttalps_plotting_styles import samples_params, samples_styles

import ROOT
from Logger import error, info
from Sample import Sample, SampleType
from Legend import Legend

from collections import defaultdict


class TTAlpsPlotterConfigHelper:
  def __init__(self, year, base_path, skim, hist_path, data_to_include, backgrounds_to_exclude, signals_to_include, legend_pos_and_size):

    self.year = year
    self.cross_sections = get_cross_sections(year)
    self.base_path = base_path
    self.skim = skim
    self.hist_path = hist_path
    self.data_to_include = data_to_include
    self.backgrounds_to_exclude = backgrounds_to_exclude
    self.signals_to_include = signals_to_include
    self.legend_pos_and_size = legend_pos_and_size

    self.custom_stacks_order = []
    self.custom_stacks_order_reversed = False

  def add_samples(self, sample_type, samples):
    if sample_type == SampleType.background and self.year == "2018":
      dataset = dasBackgrounds2018
    elif sample_type == SampleType.background and self.year == "2023":
      dataset = dasBackgrounds2023preBPix
    elif sample_type == SampleType.signal and self.year == "2018":
      dataset = dasSignals2018
    elif sample_type == SampleType.data and (self.year == "2018" or self.year == "2023"):
      dataset = self.data_to_include
    else:
      error(f"Unknown combination of sample: {sample_type} and year {self.year}")

    for sample_name in dataset:
      short_name = sample_name.split("/")[-1]

      if sample_type == SampleType.background and self.__exclude_background(short_name):
        continue

      if sample_type == SampleType.signal and short_name not in self.signals_to_include:
        continue

      long_name = self.__get_long_name(short_name)

      if sample_type == SampleType.data:
        long_name = short_name

      params = self.__get_params_for_sample(long_name)
      if params is None:
        continue

      file_path = f"{self.base_path}/{sample_name}/{self.skim}/{self.hist_path}/histograms.root"

      if sample_type == SampleType.data:
        file_path = f"{self.base_path}/collision_data2018/{sample_name}_{self.skim}_{self.hist_path}.root"

      info(f"Adding sample {long_name} of type {sample_type} with file path {file_path}")

      samples.append(
          Sample(
              name=long_name,
              file_path=file_path,
              type=sample_type,
              cross_sections=self.cross_sections,
              line_alpha=samples_styles[sample_type]["line_alpha"],
              line_style=samples_styles[sample_type]["line_style"],
              fill_alpha=samples_styles[sample_type]["fill_alpha"],
              marker_size=samples_styles[sample_type]["marker_size"],
              marker_style=samples_styles[sample_type]["marker_style"],
              marker_color=params["color"],
              fill_color=params["color"],
              line_color=params["color"],
              legend_description=params["legend_title"],
              custom_legend=self.__get_legend(
                  params["legend_column"],
                  params["legend_row"],
                  samples_styles[sample_type]["legend_style"]
              ),
          )
      )

  def get_custom_stacks_order(self, samples):

    # Group samples by short names in samples_params
    sample_groups = defaultdict(list)
    for sample in samples:
      for param in samples_params:
        if param in sample.name:
          sample_groups[param].append(sample)
          break  # Stop after first match to avoid duplicate mappings

    # Create the final ordered list
    ordered_samples = []
    for param in samples_params:
      ordered_samples.extend(sample_groups[param])

    samples = ordered_samples

    custom_stacks_order = [sample.name for sample in samples]
    custom_stacks_order.reverse()
    return custom_stacks_order

  def __get_long_name(self, short_name):
    long_name = None

    for sample_name in self.cross_sections.keys():
      if short_name in sample_name:
        long_name = sample_name
        break

    return long_name

  def __get_params_for_sample(self, long_name):
    for key, params in samples_params.items():
      if key in long_name:
        return params
    error(f"No sample parameters found for sample {long_name}")
    return None

  def __exclude_background(self, background_name):
    for background_to_exclude in self.backgrounds_to_exclude:
      if background_name in background_to_exclude:
        return True

    return False

  def __get_legend(self, column, row, style="f"):
    legend = Legend(
        self.legend_pos_and_size[0]-(column+1)*self.legend_pos_and_size[2],
        self.legend_pos_and_size[1]-(row+1)*self.legend_pos_and_size[3],
        self.legend_pos_and_size[0]-(column)*self.legend_pos_and_size[2],
        self.legend_pos_and_size[1]-(row)*self.legend_pos_and_size[3],
        style
    )

    return legend
