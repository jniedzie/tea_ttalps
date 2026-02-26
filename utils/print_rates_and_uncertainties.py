import argparse
import importlib
import os
import math
import numpy as np

from Logger import fatal, info, error, warn
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
      # print(f"Reading combined datacard: {datacard_path}")
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
                  if "/" in value:
                    kappa_down, kappa_up = map(float, value.split("/"))
                    delta_down = abs(1 - kappa_down)
                    delta_up = abs(kappa_up - 1)
                    signal_values.append(delta_down)
                    signal_values.append(delta_up)
                  else:
                    signal_values.append(float(value)-1)
                elif process == "bkg":
                  if "/" in value:
                    kappa_down, kappa_up = map(float, value.split("/"))
                    delta_down = abs(1 - kappa_down)
                    delta_up = abs(kappa_up - 1)
                    background_values.append(delta_down)
                    background_values.append(delta_up)
                  else:
                    background_values.append(float(value)-1)

            unc_category = get_unc_category(unc_name)

            if unc_name == "stat_err":
              if not unc_category+"_sig" in uncertainties[signal_sample.name]:
                uncertainties[signal_sample.name][unc_category+"_sig"] = []
                uncertainties[signal_sample.name][unc_category+"_bkg"] = []
              uncertainties[signal_sample.name][unc_category+"_sig"].extend(signal_values)
              uncertainties[signal_sample.name][unc_category+"_bkg"].extend(background_values)
            elif len(background_values) > 0:
              if not unc_category in uncertainties[signal_sample.name]:
                uncertainties[signal_sample.name][unc_category] = []
              uncertainties[signal_sample.name][unc_category].extend(signal_values)
              uncertainties[signal_sample.name][unc_category].extend(background_values)
            else:
              if not unc_category in uncertainties[signal_sample.name]:
                uncertainties[signal_sample.name][unc_category] = []
              uncertainties[signal_sample.name][unc_category].extend(signal_values)

  return rates, uncertainties


def get_min_max_uncertainty(uncertainties):
  min_uncertainty = {}
  max_uncertainty = {}

  uncertainties_per_type = {}
  for signal_name, unc_dict in uncertainties.items():
    for unc_name, unc_value in unc_dict.items():
      if unc_name not in uncertainties_per_type:
        uncertainties_per_type[unc_name] = []
      for v in unc_value:
        if v != 0.0:
          uncertainties_per_type[unc_name].append(v)

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
        if v != 0.0:
          uncertainties_per_type[unc_name].append(v)

  for unc_name, unc_values in uncertainties_per_type.items():
    min_uncertainty[unc_name] = min(unc_values)
    max_uncertainty[unc_name] = max(unc_values)

  return min_uncertainty, max_uncertainty

def get_68percert_uncertainty_range(uncertainties):
    low_68 = {}
    high_68 = {}
    mean = {}

    uncertainties_per_type = {}

    for signal_name, unc_dict in uncertainties.items():
        for unc_name, unc_value in unc_dict.items():
            if unc_name not in uncertainties_per_type:
                uncertainties_per_type[unc_name] = []
            for v in unc_value:
                if v != 0.0:
                    uncertainties_per_type[unc_name].append(v)

    for unc_name, unc_values in uncertainties_per_type.items():
        values = np.array(unc_values)
        low, high = np.percentile(values, [16, 84])
        low_68[unc_name] = low
        high_68[unc_name] = high
        mean[unc_name] = np.mean(values)

    return low_68, high_68, mean

def get_unc_category(unc_name):
  variation = ""
  if "systup" in unc_name or "systdown" in unc_name:
    variation = "_systup" if "systup" in unc_name else "_systdown"
  elif "up" in unc_name or "down" in unc_name:
    variation = "_up" if "_up" in unc_name else "_down"
  elif "Up" in unc_name or "Dn" in unc_name:
    variation = "_Up" if "Up" in unc_name else "_Dn"
  if "jecMC" in unc_name or "CMS_scale_j" in unc_name:
    return "JEC"
  if "metMC" in unc_name or "CMS_scale_met" in unc_name:
    return "MET"
  if "bTaggingMedium" in unc_name or "CMS_btag" in unc_name or "CMS_eff_b" in unc_name:
    return "bTaggingMedium"
  if variation != "" and variation in unc_name:
    base_name = unc_name.replace(variation, "")
    return base_name
  return unc_name

def get_nice_names(years):
  nice_names = {
      "abcd_nonClosure": "ABCD non-closure",
      "CMS_EXO25022_abcd": "ABCD uncertainty",
      "CMS_EXO25022_abcd_bkg": "ABCD uncertainty",
      "CMS_EXO25022_abcd_sig": "ABCD uncertainty (signal)",
      "lumi": "luminosity",
      "lumi_sig": "luminosity",
      "lumi_bkg": "luminosity",
      "stat_err_sig": "statistical (signal)",
      "stat_err_bkg": "statistical (background)",
      "JEC": "JEC",
      "MET": "MET",
      "CMS_l1_muon_prefiring": "L1 Pre-firing",
      "CMS_EXO25022_dimuonSFs_Pat_syst": "PAT-PAT Dimuon efficiency SF",
      "CMS_EXO25022_dimuonSFs_PatDSA_syst": "PAT-DSA Dimuon efficiency SF",
      "CMS_EXO25022_dimuonSFs_DSA_syst": "DSA-DSA Dimuon efficiency SF",
      # "dimuonSFs": "Dimuon efficiency SF",
      "dimuonSFs_Pat": "PAT-PAT Dimuon efficiency SF",
      "dimuonSFs_PatDSA": "PAT-DSA Dimuon efficiency SF",
      "dimuonSFs_DSA": "DSA-DSA Dimuon efficiency SF",
      "CMS_eff_m_trigger_syst": "IsoMu trigger",
      "CMS_eff_m_reco_syst": "muon reco",
      "CMS_eff_m_reco_syst_dsa": "DSA muon reco",
      "CMS_eff_m_id_syst_loose": "muon loose ID",
      "CMS_eff_m_id_syst_tight": "muon tight ID",
      "CMS_eff_m_iso_syst_loose": "muon loose Iso",
      "CMS_eff_m_iso_syst_tight": "muon tight Iso",
      "CMS_eff_m_id_syst_dsa": "DSA muon ID",
      "CMS_eff_j_PUJetID_eff": "PU jet ID",
      "CMS_btag": "b-tagging",
      "bTaggingMedium": "b-tagging",
      "CMS_pileup": "PU",
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
    nice_names[f"metMC_Regrouped_Absolute_{year}_down"] = f"MET Regrouped_Absolute_{year} SF (down)"
    nice_names[f"metMC_Regrouped_Absolute_{year}_up"] = f"MET Regrouped_Absolute_{year} SF (up)"
    nice_names[f"metMC_Regrouped_BBEC1_{year}_down"] = f"MET Regrouped_BBEC1_{year} SF (down)"
    nice_names[f"metMC_Regrouped_BBEC1_{year}_up"] = f"MET Regrouped_BBEC1_{year} SF (up)"
    nice_names[f"metMC_Regrouped_EC2_{year}_down"] = f"MET Regrouped_EC2_{year} SF (down)"
    nice_names[f"metMC_Regrouped_EC2_{year}_up"] = f"MET Regrouped_EC2_{year} SF (up)"
    nice_names[f"metMC_Regrouped_HF_{year}_down"] = f"MET Regrouped_HF_{year} SF (down)"
    nice_names[f"metMC_Regrouped_HF_{year}_up"] = f"MET Regrouped_HF_{year} SF (up)"
    nice_names[f"metMC_Regrouped_RelativeSample_{year}_down"] = f"MET Regrouped_RelativeSample_{year} SF (down)"
    nice_names[f"metMC_Regrouped_RelativeSample_{year}_up"] = f"MET Regrouped_RelativeSample_{year} SF (up)"
    if year_ in ["2022preEE", "2022postEE"]:
      year = "13p6TeV_2022"
    if year_ in ["2023preBPix", "2023postBPix"]:
      year = "13p6TeV_2023"
    nice_names[f"lumi_{year}"] = f"luminosity"
    nice_names[f"CMS_eff_j_PUJetID_eff_{year_}"] = f"PU jet ID efficiency"
    
  return nice_names

def significance_and_error(S, B, sigma_S, sigma_B, cov_SB=0.0):
  if S + B <= 0:
    return 0.0, 0.0
  Z = S / math.sqrt(S + B)
  denom = (S + B)**1.5  # (S+B)^(3/2)
  dZ_dS = (B + 0.5*S) / denom
  dZ_dB = -0.5 * S / denom

  varZ = (dZ_dS**2) * (sigma_S**2) + (dZ_dB**2) * (sigma_B**2) \
          + 2.0 * dZ_dS * dZ_dB * cov_SB
  sigma_Z = math.sqrt(max(varZ, 0.0))
  return Z, sigma_Z

def main():
  config = importlib.import_module(args.config.replace(".py", "").replace("/", "."))

  cross_sections = config.cross_sections

  rates, uncertainties = load_uncertainties(config)

  # explicitly select the first signal key, excluding "background"
  signal_name = next(
    key for key, val in uncertainties.items()
    if key != "background"
    and "stat_err_bkg" in val
    and val["stat_err_bkg"]
  )

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

    warn(f"theory_cross_section given for Run 2 now.")
    theory_cross_section = config.get_theory_cross_section(mass, "Run2")
    reference_cross_section = cross_sections[name.replace("signal_", "")]
    coupling_ref = 0.1
    coupling_target = 1.0
    signal_scale = (theory_cross_section / reference_cross_section) * (coupling_target/coupling_ref)**2

    signal_rate = 1
    signal_err = 1
    if not config.use_combined_limits:
      signal_rate = signal_scale * rate
      signal_err = uncertainties[name]["stat_err_sig"] * signal_rate
    else:
      signal_rate = sum(signal_scale * r for r in rate)
      signal_err2 = 0
      for i, r in enumerate(rate):
        stat_err = uncertainties[name]["stat_err_sig"][i] * signal_scale * r
        signal_err2 = stat_err**2
      signal_err = math.sqrt(signal_err2)

    signal_rates[(mass, ctau)] = (signal_rate, signal_err)
    signal_significance1 = signal_rate / math.sqrt(signal_rate + background_rate)
    significance, significance_err = significance_and_error(signal_rate, background_rate, signal_err, background_err)
    signal_significances[(mass, ctau)] = (significance, significance_err)

  # get a list of ctaus in increasing order:
  masses = sorted(set([mass for mass, _ in signal_rates.keys()]))
  ctaus = sorted(set([ctau for _, ctau in signal_rates.keys()]))

  # print a header line with the ctaus
  info("\n\n\t", end="")
  for ctau in ctaus:
    info(f"{ctau:.0e} mm", end="\t")
  info("")

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
        significance, err = signal_significances[(mass, ctau)]
        info(f"{significance:.2f} +/- {err:.3f}", end="\t")
      else:
        info("N/A", end="\t\t")

  min_uncertainty = {}
  max_uncertainty = {}
  if not config.use_combined_limits:
    min_uncertainty, max_uncertainty = get_min_max_uncertainty(uncertainties)
    min_68percert_uncertainty, max_68percert_uncertainty, mean_uncertainty = get_68percert_uncertainty_range(uncertainties)
  else:
    min_uncertainty, max_uncertainty = get_min_max_uncertainty(uncertainties)
    min_68percert_uncertainty, max_68percert_uncertainty, mean_uncertainty = get_68percert_uncertainty_range(uncertainties)

  info("\n\nMin/Max Uncertainties:\n")
  merged_uncertainties = {key: (min_uncertainty[key], max_uncertainty[key]) for key in min_uncertainty.keys()}
  merged_68percert_uncertainties = {key: (min_68percert_uncertainty[key], max_68percert_uncertainty[key], mean_uncertainty[key]) for key in min_68percert_uncertainty.keys()}

  # sort merged uncertainties by the average of min and max (keep it as a dictionary)
  sorted_uncertainties = {k: v for k, v in sorted(
      merged_uncertainties.items(), key=lambda item: (item[1][0] + item[1][1]) / 2, reverse=True)}
  sorted_68percert_uncertainties = {k: v for k, v in sorted(
      merged_68percert_uncertainties.items(), key=lambda item: (item[1][0] + item[1][1]) / 2, reverse=True)}

  nice_names = get_nice_names(config.years)
  max_len = max(len(nice_names[unc_name]) for unc_name in sorted_68percert_uncertainties)
  for unc_name, (min_val, max_val) in sorted_uncertainties.items():
    info(f"{nice_names[unc_name]:<{max_len}}  {min_val:.>7.4f}. {max_val:.>7.4f}".replace(".", ","))

  info("\n\nMin/Max/Mean Uncertainties in 68percert in %:\n")
  
  for unc_name, (min_val, max_val, mean_val) in sorted_68percert_uncertainties.items():
    info(f"{nice_names[unc_name]:<{max_len}}  "
          f"{min_val*100:.1f}  {max_val*100:.1f}  {mean_val*100:.1f}".replace(".", ","))

if __name__ == "__main__":
  main()
