import subprocess
import importlib
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="", help="Path to the config file.")
parser.add_argument("--condor", action="store_true", help="Run in condor mode.")
parser.add_argument("--max_correlation", type=float, default=1.0, help="Max correlation for the background histograms.")
parser.add_argument("--min_signals", type=int, default=0, help="Min number of ""good"" signals.")
parser.add_argument("--max_overlap", type=float, default=0.3, help="Max overlap between background and signal.")
parser.add_argument("--max_error", type=float, default=1.0, help="Max allowed error expressed in number of sigmas.")
parser.add_argument("--max_closure", type=float, default=0.20, help="Max allowed closure.")
parser.add_argument("--min_n_events", type=int, default=20, help="Min number of events in any of the ABCD bins.")
parser.add_argument("--max_signal_contamination", type=float, default=0.20, help="Max allowed signal contamination in any of the ABCD bins.")
args = parser.parse_args()

base_config_path = args.config

variables = (
    # # displacement
    "logLxy",
    "logLxySignificance",
    "logDxyPVTraj1",
    "logDxyPVTraj2",
    "logDxyPVTrajSig1",
    "logDxyPVTrajSig2",
    # # Angle
    "logAbsCollinearityAngle",
    "3Dangle",
    "log3Dangle",
    "cos3Dangle",
    "logCos3Dangle",
    "outerDR",
    "logOuterDR",
    "absPtLxyDPhi1",
    "absPtLxyDPhi2",
    "logAbsPtLxyDPhi1",
    "logAbsPtLxyDPhi2",
    "pt",
    "logPt",
    "leadingPt",
    "logLeadingPt",
    "eta",
    "dEta",
    "dPhi",
    # # Inv mass
    "invMass",
    "logInvMass",
    # # Vertex quality
    "nSegments",
    "normChi2",
    "logNormChi2",
    "dca",
    "logDca",
    "maxHitsInFrontOfVert",
    # # Isolation
    "logDisplacedTrackIso03Dimuon1",
    "logDisplacedTrackIso04Dimuon1",
    "logDisplacedTrackIso03Dimuon2",
    "logDisplacedTrackIso04Dimuon2",
    "deltaIso03",
    "deltaIso04",
    "logDeltaIso03",
    "logDeltaIso04",
    "deltaSquaredIso03",
    "deltaSquaredIso04",
    "logDeltaSquaredIso03",
    "logDeltaSquaredIso04",
)


def run(cmd):
  return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def main():

  commands_to_run = []

  config = importlib.import_module(base_config_path.replace(".py", "").replace("/", "."))

  category = config.category

  for i in range(len(variables)):
    for j in range(i+1, len(variables)):
      config_path = f"tmp_ttalps_abcd_config_{variables[i]}_{variables[j]}{category}.py"

      with open(base_config_path, "r") as base_config_file:
        base_config = base_config_file.read()

      with open(config_path, "w") as config_file:
        config_file.write(base_config)
        config_file.write(f"\nvariable_1 = \"{variables[i]}\"\n")
        config_file.write(f"variable_2 = \"{variables[j]}\"\n")

      print(f"Created config file: {config_path}")

      command = (
          f"abcd_plotter.py --config {config_path} "
          f"--max_error {args.max_error} "
          f"--max_closure {args.max_closure} "
          f"--min_n_events {args.min_n_events} "
          f"--max_signal_contamination {args.max_signal_contamination} "
          f"--max_correlation {args.max_correlation} "
          f"--min_signals {args.min_signals} "
          f"--max_overlap {args.max_overlap}"
      )
      commands_to_run.append(command)

  # Create the commands list file for condor
  with open("cmds.txt", "w") as f:
    for i, cmd in enumerate(commands_to_run):
      f.write(f'{cmd}\n')

  if args.condor:
    # Create the submit file
    submit_file = "submit_jobs.sub"
    with open(submit_file, "w") as f:
      f.write('''\
    universe   = vanilla
    executable = /usr/bin/python3
    arguments  = $(cmd)
    output     = /dev/null
    error      = /dev/null
    log        = /dev/null
    # output     = ./output/$(ClusterId).$(ProcId).out
    # error      = ./error/$(ClusterId).$(ProcId).err
    # log        = ./log/$(ClusterId).log
    request_cpus = 1
    request_memory = 512MB
    # request_memory = 8000MB
    initialdir = .
    getenv = True
    queue cmd from cmds.txt
    ''')

    # Submit the jobs
    subprocess.run(["condor_submit", submit_file], check=True)
  else:
    for cmd in commands_to_run:
      print(f"Running command: {cmd}")
      os.system(f"python {cmd}")
      

  # cleanup
  # os.system("rm cmds.txt")
  # os.system("rm submit_jobs.sub")
  # os.system("rm tmp_ttalps_abcd_config_*.py")


if __name__ == "__main__":
  main()
