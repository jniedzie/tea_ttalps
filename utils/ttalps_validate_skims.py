import os
import argparse

from Logger import info, error, logger_print
from ttalps_skimmer_files_config import input_directory, output_trees_dir, samples as skimmer_samples
from ttalps_histogrammer_files_config import input_directory as hist_input_directory, samples as hist_samples
from ttalps_histogrammer_files_config import output_hists_dir, hist_path


parser = argparse.ArgumentParser(
    description="Validate TTAlps skims or histograms by comparing number of input and output files.")
parser.add_argument("--hists", action="store_true", help="Validate histograms instead of skims.")
args = parser.parse_args()

input_dir = hist_input_directory if args.hists else input_directory
output_dir = output_hists_dir if args.hists else output_trees_dir
samples = hist_samples if args.hists else skimmer_samples


def main():

  for sample in samples:
    input_sample_dir = input_dir.replace("//", f"/{sample}/")
    output_sample_dir = output_dir.replace("//", f"/{sample}/")

    n_input_files = 0
    n_output_files = 0

    if not os.path.exists(input_sample_dir):
      error(f"Input sample directory does not exist: {input_sample_dir}")
      continue

    for file in os.listdir(input_sample_dir):
      if not file.endswith(".root"):
        continue

      n_input_files += 1

    if not os.path.exists(output_sample_dir):
      error(f"Output sample directory does not exist: {output_sample_dir}")
      continue

    for file in os.listdir(output_sample_dir):
      if not file.endswith(".root"):
        continue
      
      if hist_path in file:
        continue

      n_output_files += 1

    if n_input_files == n_output_files:
      message = f"OK: {n_input_files} files"
      info(f"{sample}: {message}")
    else:
      message = f"Mismatch! Input files: {n_input_files}, Output files: {n_output_files}"
      error(f"{sample}: {message}")

  info("\n\nSummary:")
  logger_print()


if __name__ == "__main__":
  main()
