import argparse
import importlib
import os

from limits_producer import run_commands_with_condor, run_commands_in_parallel
from Logger import fatal, info, error, logger_print

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="", help="Path to the config file.")
parser.add_argument("--condor", action="store_true", help="Run in condor mode.")
args = parser.parse_args()


masses = ["0p35", "2", "12", "30", "60"]
ctaus = ["1e-5", "1e0", "1e1", "1e2", "1e3"]

# masses = ["0p35"]
# ctaus = ["1e-5"]

card_pattern_Pat = "datacard_BestPFIsoDimuonVertex_logAbsCollinearityAngle_vs_logPt_Pat_signal_tta_mAlp-{}GeV_ctau-{}mm_ABCDpred.txt"
card_pattern_PatDSA = "datacard_BestPFIsoDimuonVertex_dPhi_vs_logDxyPVTraj1_PatDSA_signal_tta_mAlp-{}GeV_ctau-{}mm_ABCDpred.txt"
card_pattern_DSA = "datacard_BestPFIsoDimuonVertex_logLeadingPt_vs_dPhi_DSA_signal_tta_mAlp-{}GeV_ctau-{}mm_ABCDpred.txt"

skip_cards_preparation = True


def run_combine(config):
  base_command = (
      f'cd {config.combine_path}; '
      f'cmssw-el7 --no-home --command-to-run \"cmsenv; '
      f'cd {config.datacards_output_path};'
  )
  commands = []
  for mass in masses:
    for ctau in ctaus:

      combined_card_path = f"{config.datacards_output_path}/combined_datacard_{mass}_{ctau}.txt"

      if not skip_cards_preparation:
        datacard_Pat = config.datacards_output_path + "/" + card_pattern_Pat.format(mass, ctau)
        datacard_PatDSA = config.datacards_output_path + "/" + card_pattern_PatDSA.format(mass, ctau)
        datacard_DSA = config.datacards_output_path + "/" + card_pattern_DSA.format(mass, ctau)

        combine_cards_command = f"combineCards.py {datacard_Pat} {datacard_PatDSA} {datacard_DSA} > {combined_card_path}"
        combine_cards_command = f'{base_command} {combine_cards_command}\"'

        os.system(combine_cards_command)

      combine_output_path = combined_card_path.replace('.txt', '.log')

      command = f'{base_command} combine -M AsymptoticLimits {combined_card_path} > {combine_output_path} \"'
      commands.append(command)

  if args.condor:
    info("Running commands with condor...")
    run_commands_with_condor(commands)
  else:
    info("Running commands in parallel...")
    run_commands_in_parallel(commands)


def get_limits(config):
  limits_per_process = {}

  for mass in masses:
    for ctau in ctaus:
      combine_output_path = f"combined_datacard_{mass}_{ctau}.log"

      try:
        with open(f"{config.datacards_output_path}/{combine_output_path}", "r") as combine_output_file:
          combine_output = combine_output_file.read()
          r_values = [line.split("r < ")[1].strip() for line in combine_output.split("\n") if "r < " in line]
          limits_per_process[f"mass_{mass}_ctau_{ctau}"] = r_values
      except FileNotFoundError:
        error(f"File {combine_output_path} not found.")
        continue

  return limits_per_process


def save_limits(config):
  limits_per_process = get_limits(config)

  file_path = "limits_combined.txt"
  info(f"Saving limits to {file_path}")

  if not os.path.exists(os.path.dirname(config.results_output_path)):
    os.makedirs(os.path.dirname(config.results_output_path))

  with open(f"{config.results_output_path}/{file_path}", "w") as limits_file:
    for signal_name, limits in limits_per_process.items():
      limits_file.write(f"{signal_name}: {limits}\n")
      info(f"{signal_name}: {limits}")


def main():
  config = importlib.import_module(args.config.replace(".py", "").replace("/", "."))

  run_combine(config)

  save_limits(config)

  logger_print()


if __name__ == "__main__":
  main()
