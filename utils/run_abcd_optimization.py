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

do_region = "SR"
# do_region = "JPsiCR"

run_optimization = True

# SRDimuons updated October 2025, matching before dimuon selection, collinearity angle < 0.5
if do_region == "SR":
    # # # 2018 PAT-PAT all muon ctaus
    # min_signals = "10"
    # max_closure = "0.40"
    # min_n_events = "15"
    # # # 2018 PAT-DSA muons all ctaus
    # min_signals = "5"
    # min_signals = "7" # dimuonEff SFs
    # max_closure = "0.40"
    # min_n_events = "10"
    # # # 2018 DSA-DSA muons all ctaus:
    min_signals = "7"
    max_closure = "0.40"
    min_n_events = "1"
    # min_n_events = "3" # dimuonEff SFs


if do_region == "JPsiCR":
    # # # 2018 PAT-PAT all muon ctaus
    # min_signals = "10"
    # max_closure = "0.40"
    # min_n_events = "20"
    # # # 2018 PAT-DSA muons all ctaus
    # min_signals = "7"
    # max_closure = "0.40"
    # min_n_events = "3"
    # # # 2018 DSA-DSA muons all ctaus:
    min_signals = "7"
    max_closure = "0.40"
    min_n_events = "1"

if not run_optimization:
    # for plotting:
    min_signals = "0"
    max_overlap = "0.8"
    max_error = "5.0"
    max_signal_contamination = "0.80"
    max_closure = "0.80"

run_script = "ttalps_plot_abcd_combinations.py"
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
