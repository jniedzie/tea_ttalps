import ROOT
import argparse
import importlib
import os
import math

from Logger import fatal, info, error
from limits_producer import get_datacard_file_name

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="", help="Path to the config file.")
args = parser.parse_args()


def load_uncertainties(config):
  rates = {}
  uncertainties = {}

  # loop over all signal samples and open datacard files corresponding to them
  for signal_sample in config.signal_samples:
    # when running over multiple years, we get the same signal sample name multiple times
    if signal_sample.name in rates:
      break
    uncertainties[signal_sample.name] = {}

    datacard_file_name = get_datacard_file_name(config, signal_sample)
    datacard_path = os.path.join(config.datacards_output_path, f"{datacard_file_name}.txt")

    # Check if the datacard file exists
    if not os.path.exists(datacard_path):
      error(f"Datacard file {datacard_path} does not exist.")
      continue

    get_bkg_rate = True
    if "background" in rates:
      get_bkg_rate = False

    if not config.use_combined_limits:
      with open(datacard_path, "r") as datacard_file:
        lines = datacard_file.readlines()
        read = False

        for line in lines:
          if line.startswith("rate"):
            read = True
            values = line.split()
            rates[signal_sample.name] = float(values[1])
            rates["background"] = float(values[2])

            continue

          if read:
            # Extract the values from the line
            values = line.split()

            unc_name = values[0]
            unc = float(values[2]) if values[2] != "-" else float(values[3])
            unc = unc - 1

            if unc_name == "stat_err":
              uncertainties[signal_sample.name][unc_name+"_sig"] = float(values[2]) - 1
              uncertainties[signal_sample.name][unc_name+"_bkg"] = float(values[3]) - 1
            else:
              uncertainties[signal_sample.name][unc_name] = unc

    else: 
      with open(datacard_path, "r") as datacard_file:
        lines = datacard_file.readlines()
        read = False
        processes = []

        for i, line in enumerate(lines):
          if line.startswith("rate"):
            read = True
            values = line.split()
            processes = lines[i - 2].split()
            for process, rate in zip(processes[1:], values[1:]):
              if process == "bkg" and get_bkg_rate:
                if "background" not in rates:
                  rates["background"] = []
                rates["background"].append(float(rate))
              if process == "signal":
                if signal_sample.name not in rates:
                  rates[signal_sample.name] = []
                rates[signal_sample.name].append(float(rate))
            continue

          if line.startswith("---") and read:
            continue

          if read:
            values = line.split()
            unc_name = values[0]
            signal_values = []
            background_values = []

            for i, process in enumerate(processes[1:]):
              value = values[i+2]
              if value != "-":
                if process == "signal":
                  signal_values.append(float(value)-1)
                elif process == "bkg":
                  background_values.append(float(value)-1)

            unc_category = get_unc_category(unc_name)

            if unc_name == "stat_err":
              uncertainties[signal_sample.name][unc_category+"_sig"] = signal_values
              uncertainties[signal_sample.name][unc_category+"_bkg"] = background_values
            elif len(background_values) > 0:
              uncertainties[signal_sample.name][unc_category] = signal_values
              uncertainties[signal_sample.name][unc_category] = background_values
            else:
              uncertainties[signal_sample.name][unc_category] = signal_values

  return rates, uncertainties


def get_min_max_uncertainty(uncertainties):
  min_uncertainty = {}
  max_uncertainty = {}

  uncertainties_per_type = {}
  for signal_name, unc_dict in uncertainties.items():
    for unc_name, unc_value in unc_dict.items():
      if unc_name not in uncertainties_per_type:
        uncertainties_per_type[unc_name] = []
      uncertainties_per_type[unc_name].append(unc_value)

  for unc_name, unc_values in uncertainties_per_type.items():
    min_uncertainty[unc_name] = min(unc_values)
    max_uncertainty[unc_name] = max(unc_values)

  return min_uncertainty, max_uncertainty

def get_min_max_uncertainty_over_years(uncertainties):
  min_uncertainty = {}
  max_uncertainty = {}

  uncertainties_per_type = {}
  for signal_name, unc_dict in uncertainties.items():
    for unc_name, unc_list in unc_dict.items():
      if unc_name not in uncertainties_per_type:
        uncertainties_per_type[unc_name] = []
      for v in unc_list:
        uncertainties_per_type[unc_name].append(v)

  for unc_name, unc_values in uncertainties_per_type.items():
    min_uncertainty[unc_name] = min(unc_values)
    max_uncertainty[unc_name] = max(unc_values)

  return min_uncertainty, max_uncertainty

def get_unc_category(unc_name):
  variation = ""
  if "systup" in unc_name or "systdown" in unc_name:
    variation = "_systup" if "systup" in unc_name else "_systdown"
  elif "up" in unc_name or "down" in unc_name:
    variation = "_up" if "up" in unc_name else "_down"
  if "jecMC" in unc_name:
    return "JEC"
  if "bTaggingMedium" in unc_name:
    return "bTaggingMedium"
  if variation != "" and variation in unc_name:
    base_name = unc_name.replace(variation, "")
    return base_name
  return unc_name
  

def get_nice_names(years):
  nice_names = {
      "PUjetIDtight_down": "PU jet ID (down)",
      "PUjetIDtight_up": "PU jet ID (up)",
      "bTaggingMedium_up": "b-tagging (up)",
      "bTaggingMedium_down": "b-tagging (down)",
      "bTaggingMedium_down_correlated": "b-tagging down (uncorrelated)",
      "bTaggingMedium_down_uncorrelated": "b-tagging down (correlated)",
      "bTaggingMedium_up_correlated": "b-tagging up (uncorrelated)",
      "bTaggingMedium_up_uncorrelated": "b-tagging up (correlated)",
      "muonIDLoose_systdown": "muon ID (down)",
      "muonIDLoose_systup": "muon ID (up)",
      "muonReco_systdown": "muon reco (down)",
      "muonReco_systup": "muon reco (up)",
      "dsamuonID_syst": "DSA muon ID",
      "dsamuonReco_cosmic": "DSA muon reco",
      "muonTrigger_systdown": "IsoMu trigger (down)",
      "muonTrigger_systup": "IsoMu trigger (up)",
      "abcd_nonClosure": "ABCD non-closure",
      "abcd_unc": "ABCD uncertainty",
      "abcd_unc_bkg": "ABCD uncertainty",
      "abcd_unc_sig": "ABCD uncertainty (signal)",
      "lumi": "luminosity",
      "lumi_sig": "luminosity",
      "lumi_bkg": "luminosity",
      "stat_err_sig": "statistical (signal)",
      "stat_err_bkg": "statistical (background)",
      "dimuonEff_up": "Dimuon efficiency SF (up)",
      "dimuonEff_down": "Dimuon efficiency SF (down)",
      "dimuonRevEff_up": "Dimuon efficiency SF (up)",
      "dimuonRevEff_down": "Dimuon efficiency SF (down)",
      "DSAEff_up": "DSA Muon efficiency SF (up)",
      "DSAEff_down": "DSA Muon efficiency SF (down)",
      "jecMC_Regrouped_Absolute_down": "JEC Regrouped_Absolute SF (down)",
      "jecMC_Regrouped_Absolute_up": "JEC Regrouped_Absolute SF (up)",
      "jecMC_Regrouped_FlavorQCD_down": "JEC Regrouped_FlavorQCD SF (down)",
      "jecMC_Regrouped_FlavorQCD_up": "JEC Regrouped_FlavorQCD SF (up)",
      "jecMC_Regrouped_BBEC1_down": "JEC Regrouped_BBEC1 SF (down)",
      "jecMC_Regrouped_BBEC1_up": "JEC Regrouped_BBEC1 SF (up)",
      "jecMC_Regrouped_EC2_down": "JEC Regrouped_EC2 SF (down)",
      "jecMC_Regrouped_EC2_up": "JEC Regrouped_EC2 SF (up)",
      "jecMC_Regrouped_HF_down": "JEC Regrouped_HF SF (down)",
      "jecMC_Regrouped_HF_up": "JEC Regrouped_HF SF (up)",
      "jecMC_Regrouped_RelativeBal_down": "JEC Regrouped_RelativeBal SF (down)",
      "jecMC_Regrouped_RelativeBal_up": "JEC Regrouped_RelativeBal SF (up)",
      "jecMC_AbsoluteMPFBias_up": "JEC AbsoluteMPFBias (up)",
      "jecMC_AbsoluteMPFBias_down": "JEC AbsoluteMPFBias (down)",
      "jecMC_AbsoluteScale_up": "JEC AbsoluteScale (up)",
      "jecMC_AbsoluteScale_down": "JEC AbsoluteScale (down)",
      "jecMC_AbsoluteStat_up": "JEC AbsoluteStat (up)",
      "jecMC_AbsoluteStat_down": "JEC AbsoluteStat (down)",
      "jecMC_FlavorQCD_up": "JEC FlavorQCD (up)",
      "jecMC_FlavorQCD_down": "JEC FlavorQCD (down)",
      "jecMC_Fragmentation_up": "JEC Fragmentation (up)",
      "jecMC_Fragmentation_down": "JEC Fragmentation (down)",
      "jecMC_PileUpDataMC_up": "JEC PileUpDataMC (up)",
      "jecMC_PileUpDataMC_down": "JEC PileUpDataMC (down)",
      "jecMC_PileUpPtBB_up": "JEC PileUpPtBB (up)",
      "jecMC_PileUpPtBB_down": "JEC PileUpPtBB (down)",
      "jecMC_PileUpPtEC1_up": "JEC PileUpPtEC1 (up)",
      "jecMC_PileUpPtEC1_down": "JEC PileUpPtEC1 (down)",
      "jecMC_PileUpPtEC2_up": "JEC PileUpPtEC2 (up)",
      "jecMC_PileUpPtEC2_down": "JEC PileUpPtEC2 (down)",
      "jecMC_PileUpPtHF_up": "JEC PileUpPtHF (up)",
      "jecMC_PileUpPtHF_down": "JEC PileUpPtHF (down)",
      "jecMC_PileUpPtRef_up": "JEC PileUpPtRef (up)",
      "jecMC_PileUpPtRef_down": "JEC PileUpPtRef (down)",
      "jecMC_RelativeFSR_up": "JEC RelativeFSR (up)",
      "jecMC_RelativeFSR_down": "JEC RelativeFSR (down)",
      "jecMC_RelativeJEREC1_up": "JEC RelativeJEREC1 (up)",
      "jecMC_RelativeJEREC1_down": "JEC RelativeJEREC1 (down)",
      "jecMC_RelativeJEREC2_up": "JEC RelativeJEREC2 (up)",
      "jecMC_RelativeJEREC2_down": "JEC RelativeJEREC2 (down)",
      "jecMC_RelativeJERHF_up": "JEC RelativeJERHF (up)",
      "jecMC_RelativeJERHF_down": "JEC RelativeJERHF (down)",
      "jecMC_RelativePtBB_up": "JEC RelativePtBB (up)",
      "jecMC_RelativePtBB_down": "JEC RelativePtBB (down)",
      "jecMC_RelativePtEC1_up": "JEC RelativePtEC1 (up)",
      "jecMC_RelativePtEC1_down": "JEC RelativePtEC1 (down)",
      "jecMC_RelativePtEC2_up": "JEC RelativePtEC2 (up)",
      "jecMC_RelativePtEC2_down": "JEC RelativePtEC2 (down)",
      "jecMC_RelativePtHF_up": "JEC RelativePtHF (up)",
      "jecMC_RelativePtHF_down": "JEC RelativePtHF (down)",
      "jecMC_RelativeBal_up": "JEC RelativeBal (up)",
      "jecMC_RelativeBal_down": "JEC RelativeBal (down)",
      "jecMC_RelativeSample_up": "JEC RelativeSample (up)",
      "jecMC_RelativeSample_down": "JEC RelativeSample (down)",
      "jecMC_RelativeStatEC_up": "JEC RelativeStatEC (up)",
      "jecMC_RelativeStatEC_down": "JEC RelativeStatEC (down)",
      "jecMC_RelativeStatFSR_up": "JEC RelativeStatFSR (up)",
      "jecMC_RelativeStatFSR_down": "JEC RelativeStatFSR (down)",
      "jecMC_RelativeStatHF_up": "JEC RelativeStatHF (up)",
      "jecMC_RelativeStatHF_down": "JEC RelativeStatHF (down)",
      "jecMC_SinglePionECAL_up": "JEC SinglePionECAL (up)",
      "jecMC_SinglePionECAL_down": "JEC SinglePionECAL (down)",
      "jecMC_SinglePionHCAL_up": "JEC SinglePionHCAL (up)",
      "jecMC_SinglePionHCAL_down": "JEC SinglePionHCAL (down)",
      "jecMC_TimePtEta_up": "JEC TimePtEta (up)",
      "jecMC_TimePtEta_down": "JEC TimePtEta (down)",
      "JEC_up": "JEC (up)",
      "JEC_down": "JEC (down)",
      "JEC": "JEC",
      "DSAEff": "DSA Muon efficiency SF",
      "dimuonEff": "Dimuon efficiency SF",
      "dimuonEffRev": "Dimuon efficiency SF",
      "muonTrigger": "IsoMu trigger",
      "muonReco": "muon reco",
      "muonIDLoose": "muon ID",
      "PUjetIDtight": "PU jet ID",
      "bTaggingMedium": "b-tagging",
  }
  for year_ in years:
    year = year_
    if year_ in ["2016preVFP", "2016postVFP"]:
      year = "2016"
    nice_names[f"jecMC_Regrouped_Absolute_{year}_down"] = f"JEC Regrouped_Absolute_{year} SF (down)"
    nice_names[f"jecMC_Regrouped_Absolute_{year}_up"] = f"JEC Regrouped_Absolute_{year} SF (up)"
    nice_names[f"jecMC_Regrouped_BBEC1_{year}_down"] = f"JEC Regrouped_BBEC1_{year} SF (down)"
    nice_names[f"jecMC_Regrouped_BBEC1_{year}_up"] = f"JEC Regrouped_BBEC1_{year} SF (up)"
    nice_names[f"jecMC_Regrouped_EC2_{year}_down"] = f"JEC Regrouped_EC2_{year} SF (down)"
    nice_names[f"jecMC_Regrouped_EC2_{year}_up"] = f"JEC Regrouped_EC2_{year} SF (up)"
    nice_names[f"jecMC_Regrouped_HF_{year}_down"] = f"JEC Regrouped_HF_{year} SF (down)"
    nice_names[f"jecMC_Regrouped_HF_{year}_up"] = f"JEC Regrouped_HF_{year} SF (up)"
    nice_names[f"jecMC_Regrouped_RelativeSample_{year}_down"] = f"JEC Regrouped_RelativeSample_{year} SF (down)"
    nice_names[f"jecMC_Regrouped_RelativeSample_{year}_up"] = f"JEC Regrouped_RelativeSample_{year} SF (up)"
  return nice_names


def main():
  config = importlib.import_module(args.config.replace(".py", "").replace("/", "."))

  cross_sections = config.cross_sections

  rates, uncertainties = load_uncertainties(config)

  # explicitly select the first signal key, excluding "background"
  signal_name = next(key for key in uncertainties.keys() if key != "background")
  
  

  background_rate_ = rates.pop("background")
  background_rate = 1
  background_err = 1
  if not config.use_combined_limits:
    background_rate = background_rate_[signal_name]
    background_err = uncertainties[signal_name]["stat_err_bkg"] * background_rate
  else:
    background_rate = sum(r for r in background_rate_)
    background_err2 = 0
    for i, r in enumerate(background_rate_):
      stat_err = uncertainties[signal_name]["stat_err_bkg"][i] * r
      background_err2 += stat_err**2
    background_err = math.sqrt(background_err2)

  info(f"\n\nBackground Rate: {background_rate:.1f} +/- {background_err:.1f}")

  signal_rates = {}
  signal_significances = {}

  for name, rate in rates.items():
    mass = name.split("_")[2]
    mass = mass.split("-")[1]
    mass = mass.replace("p", ".").replace("GeV", "")
    mass = float(mass)

    ctau = name.split("_")[3]

    ctau = ctau.replace("mm", "").replace("ctau-", "")
    ctau = float(ctau)

    theory_cross_section = config.get_theory_cross_section(mass)
    reference_cross_section = cross_sections[signal_name.replace("signal_", "")]
    coupling_ref = 0.1
    coupling_target = 1.0
    signal_scale = (theory_cross_section / reference_cross_section) * (coupling_target/coupling_ref)**2 

    signal_rate = 1
    signal_err = 1
    if not config.use_combined_limits:
      signal_rate = signal_scale * rate
      signal_err = uncertainties[signal_name]["stat_err_sig"] * signal_rate
    else:
      signal_rate = sum(signal_scale * r for r in rate)
      signal_err2 = 0
      for i, r in enumerate(rate):
        stat_err = uncertainties[signal_name]["stat_err_sig"][i] * signal_scale * r
        signal_err2 = stat_err**2
      signal_err = math.sqrt(signal_err2)

    signal_rates[(mass, ctau)] = (signal_rate, signal_err)
    signal_significances[(mass, ctau)] = signal_rate / math.sqrt(signal_rate + background_rate)

  # get a list of ctaus in increasing order:
  masses = sorted(set([mass for mass, _ in signal_rates.keys()]))
  ctaus = sorted(set([ctau for _, ctau in signal_rates.keys()]))
  
  # print a header line with the ctaus
  info("\n\n\t", end="")
  for ctau in ctaus:
    info(f"{ctau:.0e} mm", end="\t")
  info()
  
  # print the signal rates for each mass
  for mass in masses:
    info(f"\n{mass:.2f} GeV:\t", end="")
    for ctau in ctaus:
      if (mass, ctau) in signal_rates:
        rate, err = signal_rates[(mass, ctau)]
        info(f"{rate:.2f} +/- {err:.3f}", end="\t")
      else:
        info("N/A", end="\t\t")

  # print the signal significance for each mass
  info("\n\nSignal Significances:\n")
  info("\t\t", end="")
  for ctau in ctaus:
    info(f"{ctau:.0e} mm", end="\t")
  for mass in masses:
    info(f"\n{mass:.2f} GeV:\t", end="")
    for ctau in ctaus:
      if (mass, ctau) in signal_significances:
        significance = signal_significances[(mass, ctau)]
        info(f"{significance:.2f}", end="\t\t")
      else:
        info("N/A", end="\t\t")


  min_uncertainty = {}
  max_uncertainty = {}
  if not config.use_combined_limits:
    min_uncertainty, max_uncertainty = get_min_max_uncertainty(uncertainties)
  else:
    min_uncertainty, max_uncertainty = get_min_max_uncertainty_over_years(uncertainties)

  info("\n\nMin/Max Uncertainties:\n")
  merged_uncertainties = {key: (min_uncertainty[key], max_uncertainty[key]) for key in min_uncertainty.keys()}

  # sort merged uncertainties by the average of min and max (keep it as a dictionary)
  sorted_uncertainties = {k: v for k, v in sorted(
      merged_uncertainties.items(), key=lambda item: (item[1][0] + item[1][1]) / 2, reverse=True)}

  nice_names = get_nice_names(config.years)
  for unc_name, (min, max) in sorted_uncertainties.items():
    info(f"{nice_names[unc_name]}\t{min:.4f}\t{max:.4f}".replace(".", ","))


if __name__ == "__main__":
  main()
