from Logger import info, warn, error, fatal, logger_print
from ttalps_samples_list import dasBackgrounds2016preVFP, dasBackgrounds2016postVFP, dasBackgrounds2017, dasBackgrounds2018
from ttalps_samples_list import dasBackgrounds2022preEE, dasBackgrounds2022postEE, dasBackgrounds2023preBPix, dasBackgrounds2023postBPix
from ttalps_samples_list import dasSignals2016preVFP, dasSignals2016postVFP, dasSignals2017, dasSignals2018
from ttalps_samples_list import dasSignals2022preEE, dasSignals2022postEE, dasSignals2023preBPix, dasSignals2023postBPix
from Histogram import Histogram, Histogram2D
from Sample import Sample, SampleType
from HistogramNormalizer import NormalizationType
from ABCDHelper import ABCDHelper
from ABCDPlotter import ABCDPlotter

from ttalps_luminosities import get_luminosity
from ttalps_cross_sections import get_cross_sections, get_theory_cross_section

import ROOT
import os
import re
import math
import argparse
import importlib

# years = ["2018",]
years = ["2016preVFP","2016postVFP","2017","2018","2022preEE","2022postEE","2023preBPix","2023postBPix"]

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "ABCD_ANv2")
hist_path = "histograms"

category = ""
# category = "_Pat"
# category = "_PatDSA"
# category = "_DSA"

cutFlow_name = "cutFlow"
dimuonCutFlow_name = f"dimuonCutFlow_BestPFIsoDimuonVertex"
dimuonCutFlow_name_Pat = f"dimuonCutFlow_BestPFIsoDimuonVertex_Pat"
dimuonCutFlow_name_PatDSA = f"dimuonCutFlow_BestPFIsoDimuonVertex_PatDSA"
dimuonCutFlow_name_DSA = f"dimuonCutFlow_BestPFIsoDimuonVertex_DSA"

ABCD_bin_A = {
    "_Pat": ("logAbsCollinearityAngle", "logDisplacedTrackIso04Dimuon2", (16, 14), "B"),
    "_PatDSA": ("logDxyPVTraj1", "logAbsCollinearityAngle", (31, 11), "A"), 
    "_DSA": ("logAbsCollinearityAngle", "logPt", (18, 11), "D"),
}

samples = {}
for year in years:
    samples[year] = {}
    cross_sections = get_cross_sections(year)
    luminosity = get_luminosity(year)
    backgrounds = globals()[f"dasBackgrounds{year}"]
    signals = globals()[f"dasSignals{year}"]
    for background in backgrounds:
        samples[year][background] = Sample(
            name=background.split("/")[-1],
            file_path=f"{base_path}/{background}/{skim[0]}/{hist_path}_{skim[1]}_{skim[2]}/histograms.root",
            type=SampleType.background,
            cross_sections=cross_sections,
            luminosity=luminosity,
        )
    for signal in signals:
        samples[year][signal] = Sample(
            name=signal.split("/")[-1],
            file_path=f"{base_path}/{signal}/{skim[0]}/{hist_path}_{skim[1]}_{skim[2]}/histograms.root",
            type=SampleType.signal,
            cross_sections=cross_sections,
            luminosity=luminosity,
        )

cutFlow_hist = Histogram(
    name=cutFlow_name,
    title=cutFlow_name,
    norm_type=NormalizationType.to_lumi,
)
dimuonCutFlow_hist = Histogram(
    name=dimuonCutFlow_name,
    title=dimuonCutFlow_name,
    norm_type=NormalizationType.to_lumi,
)
dimuonCutFlow_hist_Pat = Histogram(
    name=dimuonCutFlow_name_Pat,
    title=dimuonCutFlow_name_Pat,
    norm_type=NormalizationType.to_lumi,
)
dimuonCutFlow_hist_PatDSA = Histogram(
    name=dimuonCutFlow_name_PatDSA,
    title=dimuonCutFlow_name_PatDSA,
    norm_type=NormalizationType.to_lumi,
)
dimuonCutFlow_hist_DSA = Histogram(
    name=dimuonCutFlow_name_DSA,
    title=dimuonCutFlow_name_DSA,
    norm_type=NormalizationType.to_lumi,
)
ABCD_hists = {}
for category, points in ABCD_bin_A.items():
    ABCD_hists[category] = Histogram2D(
        name=f"BestPFIsoDimuonVertex_{points[0]}_vs_{points[1]}{category}",
        title=f"BestPFIsoDimuonVertex_{points[0]}_vs_{points[1]}{category}",
        norm_type=NormalizationType.to_lumi,
        x_rebin=4,
        y_rebin=4,
    )

cuts_nice_names = {
    "0_initial": "Initial Events",
    "1_goldenJson": "Golden JSON",
    "2_trigger": "Trigger",
    "3_metFilters": "\\ptmiss Filters",
    "4_MET_pt": "\\ptmiss $>$ 30 GeV",
    "5_nLoosePATMuons": "$\\geq$ 1 Loose PAT Muon",
    "6_nGoodJets": "$\\geq$ 4 Good Jets",
    "7_nGoodMediumBtaggedJets": "$\\geq$ 1 Medium b-tagged Jets",
    "8_nano_applyHEMveto": "HEM Veto",
    "9_nano_applyJetVetoMaps": "Jet Veto Maps",
    "10_MET_pt": "\\ptmiss $>$ 50 GeV",
    "11_nTightMuons": "$\\geq$ 1 Tight PAT Muon",
    "12_nLooseMuons": "$\\geq$ 3 Loose Muons",
    "13_nLooseElectrons": "0 Loose Electrons",
    "10_BestDimuonVertex": "$\\geq$ 1 Best Dimuon Vertex",
    "10_BestDimuonVertex_Pat": "PAT-PAT Best Dimuon Vertex",
    "10_BestDimuonVertex_PatDSA": "PAT-DSA Best Dimuon Vertex",
    "10_BestDimuonVertex_DSA": "DSA-DSA Best Dimuon Vertex",
    "ABCD_SR_Pat": "PAT-PAT ABCD SR",
    "ABCD_SR_PatDSA": "PAT-DSA ABCD SR",
    "ABCD_SR_DSA": "DSA-DSA ABCD SR",
}

def getConfig(path):
  if (".py" in path):
    path = path[:-3]
  config = importlib.import_module(path)
  return config


def get_eff_str(eff):
    if eff == 0.0:
        return "0"
    if int(round(eff)) == 100:
        return "100"
    s = f"{eff:.2g}"
    if "e" in s:
        exponent = int(math.floor(math.log10(abs(eff))))
        factor = 10 ** (exponent - 1)
        rounded = round(eff / factor) * factor
        # print(f"\n---- Rounding {eff} to {rounded}\n")
        return str(rounded)
    return f"{eff:.2g}"

def extract_mass(s):
    m = re.search(r"mAlp-([0-9]+(?:p[0-9]+)?)(?=GeV)", s)
    if not m:
        return None

    mass_str = m.group(1)
    return float(mass_str.replace("p", "."))

def main():
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetLineScalePS(1.0)
    ROOT.gStyle.SetOptStat(0)
    cutFlows = {}
    cutFlows_eff = {}
    dimuonCutFlows = {}
    dimuonCutFlows_Pat = {}
    dimuonCutFlows_PatDSA = {}
    dimuonCutFlows_DSA = {}
    dimuonCutFlows_eff = {}

    for year, samples_ in samples.items():
        # config.years = [year,]
        for sample_name, sample in samples_.items():
            print(f"Processing year {year} with samples: {sample_name}")

            file = ROOT.TFile(sample.file_path)

            if file is None or file.IsZombie():
                fatal(f"File {sample.file_path} not found or corrupted.")
                continue

            cutFlow_hist.load(file)
            dimuonCutFlow_hist.load(file)
            dimuonCutFlow_hist_Pat.load(file)
            dimuonCutFlow_hist_PatDSA.load(file)
            dimuonCutFlow_hist_DSA.load(file)

            initial_weight = cutFlow_hist.hist.GetBinContent(1)
            if initial_weight <= 0:
                warn(f"Initial weight for sample {sample.name} is non-positive ({initial_weight}). Skipping.")
                continue

            cross_section = sample.cross_section
            if sample.type == SampleType.signal:
                # cross_section = 0.01 
                mass = extract_mass(sample.name)
                cross_section = get_theory_cross_section(mass, year)
            scale = cross_section * sample.luminosity / initial_weight
            cutFlow_normalized = cutFlow_hist.hist.Clone(f"{sample.name}_cutFlow_normalized")
            cutFlow_normalized.Scale(scale)
            dimuonCutFlow_normalized = dimuonCutFlow_hist.hist.Clone(f"{sample.name}_dimuonCutFlow_normalized")
            dimuonCutFlow_normalized.Scale(scale)
            dimuonCutFlow_normalized_Pat = dimuonCutFlow_hist_Pat.hist.Clone(f"{sample.name}_dimuonCutFlow_normalized_Pat")
            dimuonCutFlow_normalized_Pat.Scale(scale)
            dimuonCutFlow_normalized_PatDSA = dimuonCutFlow_hist_PatDSA.hist.Clone(f"{sample.name}_dimuonCutFlow_normalized_PatDSA")
            dimuonCutFlow_normalized_PatDSA.Scale(scale)
            dimuonCutFlow_normalized_DSA = dimuonCutFlow_hist_DSA.hist.Clone(f"{sample.name}_dimuonCutFlow_normalized_DSA")
            dimuonCutFlow_normalized_DSA.Scale(scale)

            sample_name = sample.name
            if sample.type == SampleType.background:
                sample_name = f"background"
            if sample_name not in cutFlows:
                cutFlows[sample_name] = {}
            if sample_name not in dimuonCutFlows:
                dimuonCutFlows[sample_name] = {}
                dimuonCutFlows_Pat[sample_name] = {}
                dimuonCutFlows_PatDSA[sample_name] = {}
                dimuonCutFlows_DSA[sample_name] = {}
            for i in range(1, dimuonCutFlow_normalized.GetNbinsX() + 1):
                cut = dimuonCutFlow_normalized.GetXaxis().GetBinLabel(i)
                if cut not in dimuonCutFlows[sample_name]:
                    dimuonCutFlows[sample_name][cut] = 0.0
                    dimuonCutFlows_Pat[sample_name][cut] = 0.0
                    dimuonCutFlows_PatDSA[sample_name][cut] = 0.0
                    dimuonCutFlows_DSA[sample_name][cut] = 0.0
                dimuonCutFlows[sample_name][cut] += dimuonCutFlow_normalized.GetBinContent(i)
                dimuonCutFlows_Pat[sample_name][cut] += dimuonCutFlow_normalized_Pat.GetBinContent(i)
                dimuonCutFlows_PatDSA[sample_name][cut] += dimuonCutFlow_normalized_PatDSA.GetBinContent(i)
                dimuonCutFlows_DSA[sample_name][cut] += dimuonCutFlow_normalized_DSA.GetBinContent(i)

            for i in range(1, cutFlow_normalized.GetNbinsX() + 1):
                cut = cutFlow_normalized.GetXaxis().GetBinLabel(i)
                if cut not in cutFlows[sample_name]:
                    cutFlows[sample_name][cut] = 0.0
                cutFlows[sample_name][cut] += cutFlow_normalized.GetBinContent(i)
            dimuon_last_bin = dimuonCutFlow_normalized.GetNbinsX()
            dimuon_cut_name = dimuonCutFlow_normalized.GetXaxis().GetBinLabel(dimuon_last_bin)
            dimuon_cut_value = dimuonCutFlow_normalized.GetBinContent(dimuon_last_bin)
            dimuon_cut_value_Pat = dimuonCutFlow_normalized_Pat.GetBinContent(dimuon_last_bin)
            dimuon_cut_value_PatDSA = dimuonCutFlow_normalized_PatDSA.GetBinContent(dimuon_last_bin)
            dimuon_cut_value_DSA = dimuonCutFlow_normalized_DSA.GetBinContent(dimuon_last_bin)
            if dimuon_cut_name not in cutFlows[sample_name]:
                cutFlows[sample_name][dimuon_cut_name] = 0.0
                cutFlows[sample_name][f"{dimuon_cut_name}_Pat"] = 0.0
                cutFlows[sample_name][f"{dimuon_cut_name}_PatDSA"] = 0.0
                cutFlows[sample_name][f"{dimuon_cut_name}_DSA"] = 0.0
            cutFlows[sample_name][dimuon_cut_name] += dimuon_cut_value
            cutFlows[sample_name][f"{dimuon_cut_name}_Pat"] += dimuon_cut_value_Pat
            cutFlows[sample_name][f"{dimuon_cut_name}_PatDSA"] += dimuon_cut_value_PatDSA
            cutFlows[sample_name][f"{dimuon_cut_name}_DSA"] += dimuon_cut_value_DSA

    # Print cutflows
    info("Cutflow Summary:")
    cuts_bkg = cutFlows["background"].items()
    signals_to_print = {
        "tta_mAlp-12GeV_ctau-1e-5mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 10 nm"),
        # "tta_mAlp-12GeV_ctau-1e1mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 1 mm"),
        "tta_mAlp-12GeV_ctau-1e1mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 1 cm"),
        # "tta_mAlp-12GeV_ctau-1e2mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 10 cm"),
        "tta_mAlp-12GeV_ctau-1e3mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 1 m"),
    }

    info("\\begin{table}[hbtp]")
    info("\t\centering\n\t\\topcaption{}\n\t\\begin{tabular}{l | r r r ", end="")
    for _ in signals_to_print:
        info("| r r r ", end="")
    info("}")
    info("\t\tSelection criterion & \multicolumn{3}{|c}{Background}", end="")
    for signal_name, signal_nice_name in signals_to_print.items():
        info(f" & \multicolumn{{3}}{{|c}}{{{signal_nice_name[0]}}}", end="")
    info(" \\\\ \n \t\t& & &", end="")
    for signal_name, signal_nice_name in signals_to_print.items():
        info(f" & \multicolumn{{3}}{{|c}}{{{signal_nice_name[1]}}}", end="")
    info(" \\\\")
    info("\t\t& $N_{events}$ & $\epsilon_{rel}$ [\\%] & $\epsilon_{abs}$ [\\%]",end="")
    for i in range(len(signals_to_print)):
        info(" & $N_{events}$ & $\epsilon_{rel}$ [\\%] & $\epsilon_{abs}$ [\\%]", end="")
    info("\\\\ \\hline")
    initial_bkg_cut = list(cutFlows["background"].keys())[0]
    dimuon_cut_rel_i = 0
    for i, (cut, value_bkg) in enumerate(cuts_bkg):
        if "_Pat" in cut and "DSA" not in cut:
            info("\hline")
            dimuon_cut_rel_i = i-1
        cut_nice_name = cuts_nice_names[cut] if cut in cuts_nice_names else cut
        eff_bkg_rel = 100.0
        eff_bkg_abs = 100.0
        if i != 0:
            previous_cut = list(cutFlows["background"].keys())[i - 1]
            if dimuon_cut_rel_i != 0:
                previous_cut = list(cutFlows["background"].keys())[dimuon_cut_rel_i]
            if cutFlows["background"][previous_cut] > 0:
                eff_bkg_rel = 100.0 * value_bkg / cutFlows["background"][previous_cut]
            eff_bkg_abs = 100.0 * value_bkg / cutFlows["background"][initial_bkg_cut]

        info(f"\t\t{cut_nice_name} & {value_bkg:.1e} & {get_eff_str(eff_bkg_rel)} & {eff_bkg_abs:.1e}", end="")
        for signal_name in signals_to_print:
            if signal_name not in cutFlows:
                continue
            initial_signal_cut = list(cutFlows[signal_name].keys())[0]
            value_signal = cutFlows[signal_name][cut]
            eff_signal_rel = 100.0
            eff_signal_abs = 100.0
            if i != 0:
                previous_cut = list(cutFlows[signal_name].keys())[i - 1]
                if dimuon_cut_rel_i != 0:
                    previous_cut = list(cutFlows[signal_name].keys())[dimuon_cut_rel_i]
                if cutFlows[signal_name][previous_cut] > 0:
                    eff_signal_rel = 100.0 * value_signal / cutFlows[signal_name][previous_cut]
                eff_signal_abs = 100.0 * value_signal / cutFlows[signal_name][initial_signal_cut]
            info(f" & {get_eff_str(value_signal)} & {get_eff_str(eff_signal_rel)} & {get_eff_str(eff_signal_abs)}", end="")
        info(" \\\\")
    info("\t\\end{tabular}")
    info("\t\\label{tab:cutflow}")
    info("\end{table}")

if __name__ == "__main__":
    main()