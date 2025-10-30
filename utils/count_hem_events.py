import glob
import ROOT

input_pattern = "/data/dust/user/jniedzie/ttalps_cms/collision_data2018/SingleMuon2018*/skimmed_looseSemimuonic_v2_ttbarCR/*.root"
run_number_threshold = 319077


def count_events_in_root_files(input_pattern, run_number_threshold):
  total_events = 0
  events_above_threshold = 0

  # Loop over all ROOT files matching the input pattern
  for file_path in glob.glob(input_pattern):
    root_file = ROOT.TFile.Open(file_path)
    if not root_file or root_file.IsZombie():
      print(f"Error opening file: {file_path}")
      continue

    tree = root_file.Get("Events")
    if not tree:
      print(f"No tree found in file: {file_path}")
      root_file.Close()
      continue

    for event in tree:
      total_events += 1
      if event.run >= run_number_threshold:
        events_above_threshold += 1

    root_file.Close()

  # Calculate the fraction
  fraction_above_threshold = (events_above_threshold / total_events) if total_events > 0 else 0

  # Print the results
  print(f"Total events: {total_events}")
  print(f"Events with run number above {run_number_threshold}: {events_above_threshold}")
  print(f"Fraction of events above threshold: {fraction_above_threshold:.4f}")


if __name__ == "__main__":
  count_events_in_root_files(input_pattern, run_number_threshold)
