import subprocess
import argparse

parser = argparse.ArgumentParser(description="My program")
parser.add_argument("--condor",action="store_true", help="Run on condor")
args = parser.parse_args()

# Default optimization flags:
max_correlation = "1.0"
min_signals = "0"
max_overlap = "0.3"
max_error = "1.0"
max_closure = "0.20"
min_n_events = "20"
max_signal_contamination = "0.20"

do_region = "SR_ANv2"
# do_region = "JPsiCR_ANv2"

run_optimization = True

if do_region == "SR_ANv2":
    max_closure = "100.0"
    ######### All years #########   
    # # # PAT-PAT: 616 events
    # min_signals = "8"
    # min_n_events = "40"
    # # # PAT-DSA: ABCD 
    min_signals = "7"
    min_n_events = "15"
    # # # DSA-DSA: ABCD
    # min_signals = "7"
    # min_n_events = "3"

if do_region == "JPsiCR_ANv2":
    max_closure = "10"
    ######### All years MC #########
    # # PAT-PAT: 2078 events
    min_n_events = "100"
    min_signals = "7"
    # # # 2018 PAT-DSA : 1446 events
    # min_n_events = "100"
    # min_signals = "7"
    # # # 2018 DSA-DSA: 662 events
    # min_n_events = "50"
    # min_signals = "7"

if not run_optimization:
    min_signals = "0"
    min_n_events = "0"
    max_closure = "1.0"

run_script = "ttalps_plot_abcd_combinations.py" if run_optimization else "abcd_plotter.py"
config = "ttalps_abcd_config.py"

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
if args.condor:
    command += ["--condor"]


print(f"Running command {command}")
subprocess.run(command, text=True)
print("Done")
