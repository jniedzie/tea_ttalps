import ROOT
import argparse
import importlib
import os

from Logger import fatal, info, error
from limits_producer import get_datacard_file_name

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="", help="Path to the config file.")
args = parser.parse_args()


def load_uncertainties(config):
  uncertainties = {}

  # loop over all signal samples and open datacard files corresponding to them
  for signal_sample in config.signal_samples:
    info(f"\n\nSignal: {signal_sample.name}")
    uncertainties[signal_sample.name] = {}

    datacard_file_name = get_datacard_file_name(config, signal_sample)
    datacard_path = os.path.join(config.datacards_output_path, f"{datacard_file_name}.txt")

    # Check if the datacard file exists
    if not os.path.exists(datacard_path):
      error(f"Datacard file {datacard_path} does not exist.")
      continue

    with open(datacard_path, "r") as datacard_file:
      lines = datacard_file.readlines()
      read = False

      for line in lines:
        if line.startswith("rate"):
          read = True
          continue

        if read:
          # Extract the values from the line
          values = line.split()

          unc_name = values[0]
          unc = float(values[2]) if values[2] != "-" else float(values[3])
          unc = unc - 1

          if unc_name == "stat_err":
            uncertainties[signal_sample.name][unc_name+"_sig"] = float(values[2]) - 1
            uncertainties[signal_sample.name][unc_name+"_bkg"] = float(values[3]) - 1
          else:
            uncertainties[signal_sample.name][unc_name] = unc

  return uncertainties


def get_min_max_uncertainty(uncertainties):
  min_uncertainty = {}
  max_uncertainty = {}

  uncertainties_per_type = {}
  for signal_name, unc_dict in uncertainties.items():
    for unc_name, unc_value in unc_dict.items():
      if unc_name not in uncertainties_per_type:
        uncertainties_per_type[unc_name] = []
      uncertainties_per_type[unc_name].append(unc_value)

  for unc_name, unc_values in uncertainties_per_type.items():
    min_uncertainty[unc_name] = min(unc_values)
    max_uncertainty[unc_name] = max(unc_values)

  return min_uncertainty, max_uncertainty


def main():
  config = importlib.import_module(args.config.replace(".py", "").replace("/", "."))

  uncertainties = load_uncertainties(config)

  for signal_name, unc_dict in uncertainties.items():
    info(f"\n\nSignal: {signal_name}")

    for unc_name, unc_value in unc_dict.items():
      info(f"{unc_name}: {unc_value*100:.1f}%")

  min_uncertainty, max_uncertainty = get_min_max_uncertainty(uncertainties)

  info("\n\nMin/Max Uncertainties:")
  for unc_name, unc_value in min_uncertainty.items():
    info(f"{unc_name}: {unc_value:.4f} -- {max_uncertainty[unc_name]:.4f}")


if __name__ == "__main__":
  main()
