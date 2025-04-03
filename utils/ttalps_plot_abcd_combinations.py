import subprocess
import importlib

base_config_path = "ttalps_abcd_config.py"

variables = (
    "logLxy",
    "logLxySignificance",
    "logAbsCollinearityAngle",
    "log3Dangle",
    "outerDR",
    "maxHitsInFrontOfVert",
    "absPtLxyDPhi1",
    "absPtLxyDPhi2",
    "invMass",
    "logInvMass",
    "pt",
    "eta",
    "dEta",
    "dPhi",
    "nSegments",
    "logDisplacedTrackIso03Dimuon1",
    "logDisplacedTrackIso04Dimuon1",
    "logDisplacedTrackIso03Dimuon2",
    "logDisplacedTrackIso04Dimuon2",
    "leadingPt",
    "logDxyPVTraj1",
    "logDxyPVTraj2",
    "logDxyPVTrajSig1",
    "logDxyPVTrajSig2",
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
    for j in range(len(variables)):
      if i == j:
        continue
      config_path = f"tmp_ttalps_abcd_config_{variables[i]}_{variables[j]}{category}.py"

      with open(base_config_path, "r") as base_config_file:
        base_config = base_config_file.read()

      with open(config_path, "w") as config_file:
        config_file.write(base_config)
        config_file.write(f"\nvariable_1 = \"{variables[i]}\"\n")
        config_file.write(f"variable_2 = \"{variables[j]}\"\n")

      print(f"Created config file: {config_path}")

      command = f"plot_abcd_hists.py {config_path}"
      commands_to_run.append(command)

  # Create the commands list file for condor
  with open("cmds.txt", "w") as f:
    for i, cmd in enumerate(commands_to_run):
      f.write(f'{cmd}\n')

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
  initialdir = .
  getenv = True
  queue cmd from cmds.txt
  ''')

  # Submit the jobs
  subprocess.run(["condor_submit", submit_file], check=True)

  # cleanup
  # os.system("rm cmds.txt")
  # os.system("rm submit_jobs.sub")
  # os.system("rm tmp_ttalps_abcd_config_*.py")


if __name__ == "__main__":
  main()
