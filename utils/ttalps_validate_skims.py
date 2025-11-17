import os

from Logger import info, error
from ttalps_skimmer_files_config import input_directory, output_trees_dir, samples


def main():

  for sample in samples:
    input_sample_dir = input_directory.replace("//", f"/{sample}/")
    output_sample_dir = output_trees_dir.replace("//", f"/{sample}/")

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

      n_output_files += 1

    if n_input_files == n_output_files:
      message = f"OK: {n_input_files} files"
    else:
      message = f"Mismatch! Input files: {n_input_files}, Output files: {n_output_files}"

    info(f"{sample}: {message}")


if __name__ == "__main__":
  main()
