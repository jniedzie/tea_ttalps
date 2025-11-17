import ROOT
import os
import sys
from Logger import info, error

count_initial = True


def count_events_and_size_in_files(directory):
  print("Starting to loop over files")
  total_events = 0
  total_size_bytes = 0
  total_good_files = 0
  total_files = 0

  # Loop through files in the specified directory
  for root, _, files in os.walk(directory):
    for file in files:
      if not file.endswith(".root"):
        continue

      total_files += 1

      file_path = os.path.join(root, file)
      info(f"Processing file: {file_path}")
      try:
        root_file = ROOT.TFile(file_path)
      except Exception:
        error(f"Couldn't open file: {file_path}")
        continue

      # Check if the file can be opened
      if not root_file.IsOpen():
        error(f"Unable to open file: {file_path}")
        continue

      # Check if the "Events" tree exists in the file
      events_tree = root_file.Get("Events")
      if not events_tree:
        error(f"No 'Events' tree found in file: {file_path}")
        continue

      if count_initial:
        hist_initial = root_file.Get("CutFlow/0_initial")
        n_events = hist_initial.GetBinContent(1)
      else:
        n_events = events_tree.GetEntries()

      total_events += n_events

      # Get the file size in bytes
      file_size_bytes = os.path.getsize(file_path)
      total_size_bytes += file_size_bytes
      total_good_files += 1
      root_file.Close()

  return total_events, total_size_bytes, total_good_files, total_files


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python count_events_and_size.py /path/to/your/directory")
    sys.exit(1)

  directory_path = sys.argv[1]
  total_events, total_size_bytes, total_good_files, total_files = count_events_and_size_in_files(directory_path)
  info(f"Total number of events in {total_good_files} .root files (total files: {total_files}): {total_events}")
  info(f"Total size of *.root files in '{directory_path}': {total_size_bytes/1024/1024/1024} GB")
  size = os.popen(f"du -h {directory_path}").read()
  info(f"Size: {size}")
