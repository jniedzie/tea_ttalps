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

# do_region = "SR"
do_region = "SR_DSAChi2DCA2"
# do_region = "JPsiCR"

run_optimization = True

# SRDimuons 2018 updated October 2025, matching before dimuon selection, collinearity angle < 0.5
if do_region == "SR":
    ######### 2018 #########
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
    # min_signals = "7"
    # # min_signals = "10" # no Chi2vsDCA cut
    # max_closure = "0.40"
    # # min_n_events = "1" 
    # min_n_events = "1" # dimuon SFs
    # # min_n_events = "10" # no Chi2vsDCA cut
    ######### All years #########
    # # # PAT-PAT all muon ctaus: ABCD = 276 events
    # min_signals = "13"
    # min_n_events = "40"
    # # # PAT-DSA: ABCD = 184 events
    # min_signals = "15"
    # min_n_events = "30"
    # # # DSA-DSA: ABCD = 41 events
    min_signals = "7"
    max_closure = "0.40"
    min_n_events = "5"

if do_region == "SR_DSAChi2DCA2":
    ######### 2018 #########
    # # # 2018 PAT-PAT all muon ctaus
    # min_signals = "10"
    # max_closure = "0.40"
    # min_n_events = "15"
    # # # 2018 PAT-DSA muons all ctaus
    # min_signals = "10"
    # max_closure = "0.40"
    # min_n_events = "10"
    # # # 2018 DSA-DSA muons all ctaus:
    # min_signals = "10" 
    # max_closure = "0.40"
    # min_n_events = "10" 
    ######### All years #########
    # # # PAT-PAT: 275 events
    # min_signals = "15"
    # min_n_events = "30"
    # # # PAT-DSA: 183 events
    # min_signals = "15"
    # min_n_events = "30"
    # # # DSA-DSA: 339 events
    min_signals = "13"
    max_closure = "0.40"
    min_n_events = "30"

if do_region == "JPsiCR":
    ######### 2018 #########
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
