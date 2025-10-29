import argparse
import importlib
import os
import subprocess

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

### Old matching:
# card_pattern_Pat = "datacard_BestPFIsoDimuonVertex_logAbsCollinearityAngle_vs_logLeadingPt_Pat_signal_tta_mAlp-{}GeV_ctau-{}mm_ABCDpred.txt"
# card_pattern_PatDSA = "datacard_BestPFIsoDimuonVertex_logDxyPVTraj1_vs_logOuterDR_PatDSA_signal_tta_mAlp-{}GeV_ctau-{}mm_ABCDpred.txt"
# card_pattern_DSA = "datacard_BestPFIsoDimuonVertex_logDxyPVTrajSig2_vs_logPt_DSA_signal_tta_mAlp-{}GeV_ctau-{}mm_ABCDpred.txt"

card_pattern_Pat = "combined_datacard_{}_{}_Pat.txt"
card_pattern_PatDSA = "combined_datacard_{}_{}_PatDSA.txt"
card_pattern_DSA = "combined_datacard_{}_{}_DSA.txt"

combine_dimuon_categories = True
skip_cards_preparation = False


def run_combine(config):
  
  years = config.years
  year_str = config.year_str

  base_command = (
      f'cd {config.combine_path}; '
      f'cmssw-el7 --no-home --command-to-run \"cmsenv; '
      f'cd {config.datacards_output_path};'
  )
  # Test cmssw-el7
  test_command = f"{base_command} echo \"\""
  if subprocess.run(test_command, shell=True).returncode != 0:
      base_command = (
      f'cd {config.combine_path}; '
      f'cmssw-el9 --no-home --command-to-run \"cmsenv; '
      f'cd {config.datacards_output_path};'
  )
  commands = []
  for mass in masses:
    for ctau in ctaus:

      combined_card_path = f"{config.datacards_output_path}/combined_datacard_{mass}_{ctau}.txt"
      if not combine_dimuon_categories:
        combined_card_path = f"{config.datacards_output_path}/combined_datacard_{mass}_{ctau}{config.category}.txt"

      if not skip_cards_preparation:
        if combine_dimuon_categories:
          datacard_Pat = config.datacards_output_path + "/" + card_pattern_Pat.format(mass, ctau)
          datacard_PatDSA = config.datacards_output_path + "/" + card_pattern_PatDSA.format(mass, ctau)
          datacard_DSA = config.datacards_output_path + "/" + card_pattern_DSA.format(mass, ctau)

          combine_cards_command = f"combineCards.py {datacard_Pat} {datacard_PatDSA} {datacard_DSA} > {combined_card_path}"
          combine_cards_command = f'{base_command} {combine_cards_command}\"'

          os.system(combine_cards_command)
        else:
          if len(years) > 1:
            info(f"combining datacards over years {years}")
            card_pattern = card_pattern_Pat
            if config.category == "_PatDSA":
              card_pattern = card_pattern_PatDSA
            if config.category == "_DSA":
              card_pattern = card_pattern_DSA

            datacards = ""
            for year in years:
              datacard_output_path = config.datacards_output_path.replace(year_str, year)
              datacard = datacard_output_path + "/" + card_pattern.format(mass, ctau)
              datacards += datacard+" "
            combine_cards_command = f"combineCards.py {datacards} > {combined_card_path}"
            combine_cards_command = f'{base_command} {combine_cards_command}\"'

            os.system(combine_cards_command)
          else:
            error(f"Combine limits set to combine over years but multiple years are not defined.")
              

      combine_output_path = combined_card_path.replace('.txt', '.log')

      command = f'{base_command} combine -M AsymptoticLimits {combined_card_path} > {combine_output_path} \"'
      commands.append(command)

  if args.condor:
    info("Running commands with condor...")
    run_commands_with_condor(commands)
  else:
    info("Running commands in parallel...")
    run_commands_in_parallel(commands)


def get_limits(config, combine_dimuon_categories):
  limits_per_process = {}

  for mass in masses:
    for ctau in ctaus:
      combine_output_path = f"combined_datacard_{mass}_{ctau}.log"
      if not combine_dimuon_categories:
        combine_output_path = f"combined_datacard_{mass}_{ctau}{config.category}.log"

      try:
        with open(f"{config.datacards_output_path}/{combine_output_path}", "r") as combine_output_file:
          combine_output = combine_output_file.read()
          r_values = [line.split("r < ")[1].strip() for line in combine_output.split("\n") if "r < " in line]
          limits_per_process[f"mass_{mass}_ctau_{ctau}"] = r_values
      except FileNotFoundError:
        error(f"File {combine_output_path} not found.")
        continue

  return limits_per_process


def save_limits(config, combine_dimuon_categories):
  limits_per_process = get_limits(config, combine_dimuon_categories)

  file_path = "limits_combined.txt"
  if not combine_dimuon_categories:
    file_path = f"limits_combined{config.category}.txt"
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

  save_limits(config, combine_dimuon_categories)

  logger_print()


if __name__ == "__main__":
  main()
