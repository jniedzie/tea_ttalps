import subprocess

# Default optimization flags:
max_correlation = "1.0"
min_signals = "0"
max_overlap = "0.3"
max_error = "1.0"
max_closure = "0.20"
min_n_events = "20"
max_signal_contamination = "0.20"

do_region = "SRnewMatching"
# do_region = "JPsiCRnewMatching"

# new matching with dimuonEff for min 3 bkg events
if do_region == "SRnewMatching":
    min_signals = "10"
    # for plotting:
    min_signals = "0"
    max_overlap = "0.8"
    max_error = "5.0"
    max_signal_contamination = "0.80"
    max_closure = "0.80"

if do_region == "JPsiCRnewMatching":
    min_signals = "5"
    # min_n_events = "10" # PAT, PATDSA category
    min_n_events = "5" # DSA category


run_script = "ttalps_plot_abcd_combinations.py"
# run_script = "abcd_plotter.py"
config = "ttalps_abcd_config.py"
condor = False

command = [
    "python", run_script,
    "--config", config,
    "--max_correlation", max_correlation,
    "--min_signals", min_signals,
    "--max_overlap", max_overlap,
    "--max_error", max_error,
    "--max_closure", max_closure,
    "--min_n_events", min_n_events,
    "--max_signal_contamination", max_signal_contamination
]
if condor:
    command += ["--condor"]


print(f"Running command {command}")
subprocess.run(command, text=True)
print("Done")
