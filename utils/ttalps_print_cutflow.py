from Logger import info, warn, error, fatal, logger_print
from ttalps_samples_list import dasBackgrounds2016preVFP, dasBackgrounds2016postVFP, dasBackgrounds2017, dasBackgrounds2018
from ttalps_samples_list import dasBackgrounds2022preEE, dasBackgrounds2022postEE, dasBackgrounds2023preBPix, dasBackgrounds2023postBPix
from ttalps_samples_list import dasData2016preVFP, dasData2016postVFP, dasData2017, dasData2018
from ttalps_samples_list import dasData2022preEE, dasData2022postEE, dasData2023preBPix, dasData2023postBPix
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
# years = ["2022preEE","2022postEE","2023preBPix","2023postBPix"]
# years = ["2016preVFP","2016postVFP","2017","2018",]
years = ["2016preVFP","2016postVFP","2017","2018","2022preEE","2022postEE","2023preBPix","2023postBPix"]

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "ABCD_ANv2")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "ABCD_ANv5")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "ANv5")
skim_bkg = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "ABCD_ANv5")
skim_data = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "ABCD_ANv10_regionABCD")
skim_sig = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "ABCD_ANv5")
# skim_sig = ("skimmed_looseSemimuonic_v3_SR", "SRDimuonsMaxDxyDz", "ANv5")
# skim_sig = ("skimmed_looseSemimuonic_v3_SR", "SRDimuonsMaxDxyDz", "ABCD_ANv5")
# skim = ("skimmed_looseSemimuonic_v3_SR_puppiMET", "SRDimuons", "ABCD_ANv5")
hist_path = "histograms"

# category = ""
category = "_Pat"
# category = "_PatDSA"
# category = "_DSA"

print_dimuon_cutflow = False

cutFlow_name = "cutFlow"
dimuonCutFlow_name = f"dimuonCutFlow_BestPFIsoDimuonVertex"
dimuonCutFlow_name_Pat = f"dimuonCutFlow_BestPFIsoDimuonVertex_Pat"
dimuonCutFlow_name_PatDSA = f"dimuonCutFlow_BestPFIsoDimuonVertex_PatDSA"
dimuonCutFlow_name_DSA = f"dimuonCutFlow_BestPFIsoDimuonVertex_DSA"
rawEventsDimuonCutFlow_name = "rawEventsDimuonCutFlow_BestPFIsoDimuonVertex"
rawEventsDimuonCutFlow_name_Pat = "rawEventsDimuonCutFlow_BestPFIsoDimuonVertex_Pat"
rawEventsDimuonCutFlow_name_PatDSA = "rawEventsDimuonCutFlow_BestPFIsoDimuonVertex_PatDSA"
rawEventsDimuonCutFlow_name_DSA = "rawEventsDimuonCutFlow_BestPFIsoDimuonVertex_DSA"


ABCD_bin_A = {
    "_Pat": ("logAbsCollinearityAngle", "logDisplacedTrackIso04Dimuon2", (16, 14), "B"),
    "_PatDSA": ("logDxyPVTraj1", "logAbsCollinearityAngle", (31, 11), "A"), 
    "_DSA": ("logAbsCollinearityAngle", "logPt", (18, 11), "D"),
}

data_str = {
    "2016preVFP": "SingleMuon2016",
    "2016postVFP": "SingleMuon2016",
    "2017": "SingleMuon2017",
    "2018": "SingleMuon2018",
    "2022preEE": "Muon2022",
    "2022postEE": "Muon2022",
    "2023preBPix": "Muon12023",
    "2023postBPix": "Muon12023",
}

samples = {}
for year in years:
    samples[year] = {}
    cross_sections = get_cross_sections(year)
    luminosity = get_luminosity(year)
    backgrounds = globals()[f"dasBackgrounds{year}"]
    das_data = globals()[f"dasData{year}"]
    signals = globals()[f"dasSignals{year}"]

    skim_path_bkg = f"{skim_bkg[0]}/{hist_path}_{skim_bkg[1]}_{skim_bkg[2]}"
    skim_path_sig = f"{skim_sig[0]}/{hist_path}_{skim_sig[1]}_{skim_sig[2]}"
    for background in backgrounds:
        samples[year][background] = Sample(
            name=background.split("/")[-1],
            file_path=f"{base_path}/{background}/{skim_path_bkg}/histograms.root",
            type=SampleType.background,
            cross_sections=cross_sections,
            luminosity=luminosity,
        )
    for signal in signals:
        samples[year][signal] = Sample(
            name=signal.split("/")[-1],
            file_path=f"{base_path}/{signal}/{skim_path_sig}/histograms.root",
            type=SampleType.signal,
            cross_sections=cross_sections,
            luminosity=luminosity,
        )
    
    samples[year]["data"] = Sample(
        name=data_str[year],
        file_path=f"{base_path}/collision_data{year}/{data_str[year]}_{skim_data[0]}_histograms_{skim_data[1]}_{skim_data[2]}.root",
        type=SampleType.data,
        cross_sections=cross_sections,
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
rawEventsDimuonCutFlow_hist = Histogram(
    name=rawEventsDimuonCutFlow_name,
    title=rawEventsDimuonCutFlow_name,
    norm_type=NormalizationType.to_lumi,
)
rawEventsDimuonCutFlow_hist_Pat = Histogram(
    name=rawEventsDimuonCutFlow_name_Pat,
    title=rawEventsDimuonCutFlow_name_Pat,
    norm_type=NormalizationType.to_lumi,
)
rawEventsDimuonCutFlow_hist_PatDSA = Histogram(
    name=rawEventsDimuonCutFlow_name_PatDSA,
    title=rawEventsDimuonCutFlow_name_PatDSA,
    norm_type=NormalizationType.to_lumi,
)
rawEventsDimuonCutFlow_hist_DSA = Histogram(
    name=rawEventsDimuonCutFlow_name_DSA,
    title=rawEventsDimuonCutFlow_name_DSA,
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
    "10_nano_MET_pt": "\\ptmiss $>$ 50 GeV",
    "11_nTightMuons": "$\\geq$ 1 Tight PAT Muon",
    "12_nLooseMuons": "$\\geq$ 3 Loose Muons",
    "13_nLooseElectrons": "0 Loose Electrons",
    "10_BestDimuonVertex": "$\\geq$ 1 Best Dimuon Vertex",
    "10_BestDimuonVertex_Pat": "PAT-PAT Best Dimuon Vertex",
    "10_BestDimuonVertex_PatDSA": "PAT-DSA Best Dimuon Vertex",
    "10_BestDimuonVertex_DSA": "DSA-DSA Best Dimuon Vertex",
    "11_maxLxy": "$\\geq$ 1 Best Dimuon Vertex",
    "11_maxLxy_Pat": "PAT-PAT Best Dimuon Vertex",
    "11_maxLxy_PatDSA": "PAT-DSA Best Dimuon Vertex",
    "11_maxLxy_DSA": "DSA-DSA Best Dimuon Vertex",
    "12_abcdRegion": "ABCD Region",
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
    dimuonCutFlows_err = {}
    dimuonCutFlows_err_Pat = {}
    dimuonCutFlows_err_PatDSA = {}
    dimuonCutFlows_err_DSA = {}
    dimuonCutFlows_eff = {}

    raw_cutFlows = {}
    raw_cutFlows_Pat = {}
    raw_cutFlows_PatDSA = {}
    raw_cutFlows_DSA = {}

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
            rawEventsDimuonCutFlow_hist.load(file)
            rawEventsDimuonCutFlow_hist_Pat.load(file)
            rawEventsDimuonCutFlow_hist_PatDSA.load(file)
            rawEventsDimuonCutFlow_hist_DSA.load(file)

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
            if sample.type != SampleType.data:
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
            if sample.type == SampleType.data:
                sample_name = f"data"
            if sample_name not in cutFlows:
                cutFlows[sample_name] = {}
            if sample_name not in dimuonCutFlows:
                dimuonCutFlows[sample_name] = {}
                dimuonCutFlows_Pat[sample_name] = {}
                dimuonCutFlows_PatDSA[sample_name] = {}
                dimuonCutFlows_DSA[sample_name] = {}
                dimuonCutFlows_err[sample_name] = {}
                dimuonCutFlows_err_Pat[sample_name] = {}
                dimuonCutFlows_err_PatDSA[sample_name] = {}
                dimuonCutFlows_err_DSA[sample_name] = {}
                
                raw_cutFlows[sample_name] = {}
                raw_cutFlows_Pat[sample_name] = {}
                raw_cutFlows_PatDSA[sample_name] = {}
                raw_cutFlows_DSA[sample_name] = {}
            for i in range(1, dimuonCutFlow_normalized.GetNbinsX() + 1):
                cut = dimuonCutFlow_normalized.GetXaxis().GetBinLabel(i)
                if cut not in dimuonCutFlows[sample_name]:
                    dimuonCutFlows[sample_name][cut] = 0.0
                    dimuonCutFlows_Pat[sample_name][cut] = 0.0
                    dimuonCutFlows_PatDSA[sample_name][cut] = 0.0
                    dimuonCutFlows_DSA[sample_name][cut] = 0.0
                    dimuonCutFlows_err[sample_name][cut] = 0.0
                    dimuonCutFlows_err_Pat[sample_name][cut] = 0.0
                    dimuonCutFlows_err_PatDSA[sample_name][cut] = 0.0
                    dimuonCutFlows_err_DSA[sample_name][cut] = 0.0
                dimuonCutFlows[sample_name][cut] += dimuonCutFlow_normalized.GetBinContent(i)
                dimuonCutFlows_Pat[sample_name][cut] += dimuonCutFlow_normalized_Pat.GetBinContent(i)
                dimuonCutFlows_PatDSA[sample_name][cut] += dimuonCutFlow_normalized_PatDSA.GetBinContent(i)
                dimuonCutFlows_DSA[sample_name][cut] += dimuonCutFlow_normalized_DSA.GetBinContent(i)                
                if rawEventsDimuonCutFlow_hist.hist.GetBinContent(i) > 0:
                    dimuonCutFlows_err[sample_name][cut] += scale * (dimuonCutFlow_hist.hist.GetBinContent(i) / math.sqrt(rawEventsDimuonCutFlow_hist.hist.GetBinContent(i)))
                if rawEventsDimuonCutFlow_hist_Pat.hist.GetBinContent(i) > 0:
                    dimuonCutFlows_err_Pat[sample_name][cut] += scale * (dimuonCutFlow_hist_Pat.hist.GetBinContent(i) / math.sqrt(rawEventsDimuonCutFlow_hist_Pat.hist.GetBinContent(i)))
                if rawEventsDimuonCutFlow_hist_PatDSA.hist.GetBinContent(i) > 0:
                    dimuonCutFlows_err_PatDSA[sample_name][cut] += scale * (dimuonCutFlow_hist_PatDSA.hist.GetBinContent(i) / math.sqrt(rawEventsDimuonCutFlow_hist_PatDSA.hist.GetBinContent(i)))
                if rawEventsDimuonCutFlow_hist_DSA.hist.GetBinContent(i) > 0:
                    dimuonCutFlows_err_DSA[sample_name][cut] += scale * (dimuonCutFlow_hist_DSA.hist.GetBinContent(i) / math.sqrt(rawEventsDimuonCutFlow_hist_DSA.hist.GetBinContent(i)))

            for i in range(1, cutFlow_normalized.GetNbinsX() + 1):
                cut = cutFlow_normalized.GetXaxis().GetBinLabel(i)
                if cut == "11_maxLxy":
                    continue
                if cut == "10_nano_MET_pt":
                    cut = "10_MET_pt"
                if cut not in cutFlows[sample_name]:
                    cutFlows[sample_name][cut] = 0.0
                cutFlows[sample_name][cut] += cutFlow_normalized.GetBinContent(i)
            dimuon_last_bin = dimuonCutFlow_normalized.GetNbinsX()
            # dimuon_cut_name = dimuonCutFlow_normalized.GetXaxis().GetBinLabel(dimuon_last_bin)
            dimuon_cut_name = "10_BestDimuonVertex"

            dimuon_cut_value = dimuonCutFlow_normalized.GetBinContent(dimuon_last_bin)
            dimuon_cut_value_Pat = dimuonCutFlow_normalized_Pat.GetBinContent(dimuon_last_bin)
            dimuon_cut_value_PatDSA = dimuonCutFlow_normalized_PatDSA.GetBinContent(dimuon_last_bin)
            dimuon_cut_value_DSA = dimuonCutFlow_normalized_DSA.GetBinContent(dimuon_last_bin)
            if dimuon_cut_name not in cutFlows[sample_name]:
                cutFlows[sample_name][dimuon_cut_name] = 0.0
                cutFlows[sample_name][f"{dimuon_cut_name}_Pat"] = 0.0
                cutFlows[sample_name][f"{dimuon_cut_name}_PatDSA"] = 0.0
                cutFlows[sample_name][f"{dimuon_cut_name}_DSA"] = 0.0
                raw_cutFlows[sample_name][dimuon_cut_name] = 0.0
                raw_cutFlows[sample_name][f"{dimuon_cut_name}_Pat"] = 0.0
                raw_cutFlows[sample_name][f"{dimuon_cut_name}_PatDSA"] = 0.0
                raw_cutFlows[sample_name][f"{dimuon_cut_name}_DSA"] = 0.0
            cutFlows[sample_name][dimuon_cut_name] += dimuon_cut_value
            cutFlows[sample_name][f"{dimuon_cut_name}_Pat"] += dimuon_cut_value_Pat
            cutFlows[sample_name][f"{dimuon_cut_name}_PatDSA"] += dimuon_cut_value_PatDSA
            cutFlows[sample_name][f"{dimuon_cut_name}_DSA"] += dimuon_cut_value_DSA
            raw_cutFlows[sample_name][dimuon_cut_name] += rawEventsDimuonCutFlow_hist.hist.GetBinContent(dimuon_last_bin)
            raw_cutFlows[sample_name][f"{dimuon_cut_name}_Pat"] += rawEventsDimuonCutFlow_hist_Pat.hist.GetBinContent(dimuon_last_bin)
            raw_cutFlows[sample_name][f"{dimuon_cut_name}_PatDSA"] += rawEventsDimuonCutFlow_hist_PatDSA.hist.GetBinContent(dimuon_last_bin)
            raw_cutFlows[sample_name][f"{dimuon_cut_name}_DSA"] += rawEventsDimuonCutFlow_hist_DSA.hist.GetBinContent(dimuon_last_bin)

    # Print cutflows
    info("Cutflow Summary:")
    cuts_bkg = cutFlows["background"].items()
    signals_to_print = {
        "tta_mAlp-0p35GeV_ctau-1e-5mm": ("$m_{a}$ = 0.35 GeV", "$c\\tau_{a}$ = 10 nm"),
        "tta_mAlp-0p35GeV_ctau-1e0mm": ("$m_{a}$ = 0.35 GeV", "$c\\tau_{a}$ = 1 mm"),
        "tta_mAlp-0p35GeV_ctau-1e1mm": ("$m_{a}$ = 0.35 GeV", "$c\\tau_{a}$ = 1 cm"),
        "tta_mAlp-0p35GeV_ctau-1e2mm": ("$m_{a}$ = 0.35 GeV", "$c\\tau_{a}$ = 10 cm"),
        "tta_mAlp-0p35GeV_ctau-1e3mm": ("$m_{a}$ = 0.35 GeV", "$c\\tau_{a}$ = 1 m"),
        "tta_mAlp-2GeV_ctau-1e-5mm": ("$m_{a}$ = 2 GeV", "$c\\tau_{a}$ = 10 nm"),
        "tta_mAlp-2GeV_ctau-1e0mm": ("$m_{a}$ = 2 GeV", "$c\\tau_{a}$ = 1 mm"),
        "tta_mAlp-2GeV_ctau-1e1mm": ("$m_{a}$ = 2 GeV", "$c\\tau_{a}$ = 1 cm"),
        "tta_mAlp-2GeV_ctau-1e2mm": ("$m_{a}$ = 2 GeV", "$c\\tau_{a}$ = 10 cm"),
        "tta_mAlp-2GeV_ctau-1e3mm": ("$m_{a}$ = 2 GeV", "$c\\tau_{a}$ = 1 m"),

        "tta_mAlp-12GeV_ctau-1e-5mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 10 nm"),
        "tta_mAlp-12GeV_ctau-1e0mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 1 mm"),
        "tta_mAlp-12GeV_ctau-1e1mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 1 cm"),
        "tta_mAlp-12GeV_ctau-1e2mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 10 cm"),
        "tta_mAlp-12GeV_ctau-1e3mm": ("$m_{a}$ = 12 GeV", "$c\\tau_{a}$ = 1 m"),

        "tta_mAlp-30GeV_ctau-1e-5mm": ("$m_{a}$ = 30 GeV", "$c\\tau_{a}$ = 10 nm"),
        "tta_mAlp-30GeV_ctau-1e0mm": ("$m_{a}$ = 30 GeV", "$c\\tau_{a}$ = 1 mm"),
        "tta_mAlp-30GeV_ctau-1e1mm": ("$m_{a}$ = 30 GeV", "$c\\tau_{a}$ = 1 cm"),
        "tta_mAlp-30GeV_ctau-1e2mm": ("$m_{a}$ = 30 GeV", "$c\\tau_{a}$ = 10 cm"),
        "tta_mAlp-30GeV_ctau-1e3mm": ("$m_{a}$ = 30 GeV", "$c\\tau_{a}$ = 1 m"),
        "tta_mAlp-60GeV_ctau-1e-5mm": ("$m_{a}$ = 60 GeV", "$c\\tau_{a}$ = 10 nm"),
        "tta_mAlp-60GeV_ctau-1e0mm": ("$m_{a}$ = 60 GeV", "$c\\tau_{a}$ = 1 mm"),
        "tta_mAlp-60GeV_ctau-1e1mm": ("$m_{a}$ = 60 GeV", "$c\\tau_{a}$ = 1 cm"),
        "tta_mAlp-60GeV_ctau-1e2mm": ("$m_{a}$ = 60 GeV", "$c\\tau_{a}$ = 10 cm"),
        "tta_mAlp-60GeV_ctau-1e3mm": ("$m_{a}$ = 60 GeV", "$c\\tau_{a}$ = 1 m"),
    }

    print("Raw cutflows for signals:")
    print(f"signal \tAll categories \t PAT-PAT \t PAT-DSA \t DSA-DSA")
    for signal_name, signal_nice_name in signals_to_print.items():
        if signal_name not in raw_cutFlows:
            continue
        print(f"{signal_name}: \t", end="")
        for cut in raw_cutFlows[signal_name].keys():
            print(f"{raw_cutFlows[signal_name][cut]:.0f} \t", end="")
        print()

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

        value_data = cutFlows["data"][cut] if "data" in cutFlows and cut in cutFlows["data"] else 0.0
        eff_data_rel = 100.0
        eff_data_abs = 100.0
        if i != 0:
            previous_cut = list(cutFlows["data"].keys())[i - 1]
            if cutFlows["data"][previous_cut] > 0:
                eff_data_rel = 100.0 * value_data / cutFlows["data"][previous_cut]
            eff_data_abs = 100.0 * value_data / cutFlows["data"][initial_bkg_cut]
        
        info(f"\t\t{cut_nice_name} & {value_data:.1e} & {get_eff_str(eff_data_rel)} & {eff_data_abs:.1e} & {value_bkg:.1e} & {get_eff_str(eff_bkg_rel)} & {eff_bkg_abs:.1e}", end="")
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

    dimuon_cut_rel_i = 0
    if print_dimuon_cutflow:
        dimuoncuts_Pat = dimuonCutFlows_Pat[list(signals_to_print.keys())[0]].items()
        dimuoncuts_PatDSA = dimuonCutFlows_PatDSA[list(signals_to_print.keys())[0]].items()
        dimuoncuts_DSA = dimuonCutFlows_DSA[list(signals_to_print.keys())[0]].items()
        info("\n\nDetailed Dimuon Cutflow Summary:")
        info("PAT-PAT:")
        info("signal \t\t N_events \t eff_rel [\\%] \t eff_abs [\\%]")
        for i, (cut, values) in enumerate(dimuoncuts_Pat):
            info(f"-- {cut} --")
            for signal_name in signals_to_print:
                if signal_name not in dimuonCutFlows_Pat:
                    continue
                value_signal = dimuonCutFlows_Pat[signal_name][cut]
                err_signal = dimuonCutFlows_err_Pat[signal_name][cut]
                eff_signal_rel = 100.0
                eff_signal_rel_err = 0.0
                eff_signal_abs = 100.0
                if i != 0:
                    previous_cut = list(dimuonCutFlows_Pat[signal_name].keys())[i - 1]
                    if dimuon_cut_rel_i != 0:
                        previous_cut = list(dimuonCutFlows_Pat[signal_name].keys())[dimuon_cut_rel_i]
                    if dimuonCutFlows_Pat[signal_name][previous_cut] > 0:
                        previous_value = dimuonCutFlows_Pat[signal_name][previous_cut]
                        previous_err = dimuonCutFlows_err_Pat[signal_name][previous_cut]
                        eff_signal_rel = 100.0 * value_signal / previous_value
                        eff_signal_rel_err = eff_signal_rel * math.sqrt((err_signal / value_signal) ** 2 + (previous_err / previous_value) ** 2)
                    eff_signal_abs = 100.0 * value_signal / cutFlows[signal_name][initial_signal_cut]
                info(f"{signal_name}: \t {get_eff_str(value_signal)} +/- {get_eff_str(err_signal)} \t {get_eff_str(eff_signal_rel)} +/- {get_eff_str(eff_signal_rel_err)} % \t {get_eff_str(eff_signal_abs)} %")
        
if __name__ == "__main__":
    main()

# Initial Events                & 4.0e+09 & 100   & 1.0e+02  & 1.5e+12 & 100   & 1.0e+02 & 830 & 100 & 100 & 830 & 100 & 100 & 830 & 100 & 100 \\
# Golden JSON                   & 4.0e+09 & 100   & 1.0e+02  & 1.5e+12 & 100   & 1.0e+02 & 830 & 100 & 100 & 830 & 100 & 100 & 830 & 100 & 100 \\
# Trigger                       & 2.5e+09 & 63    & 6.3e+01  & 2.2e+09 & 0.15  & 1.5e-01 & 600 & 72 & 72 & 460 & 56 & 56 & 120 & 15 & 15 \\
# \ptmiss Filters               & 2.5e+09 & 100   & 6.3e+01  & 2.2e+09 & 100   & 1.5e-01 & 600 & 100 & 72 & 460 & 100 & 56 & 120 & 100 & 15 \\
# $\ptmiss > 30\GeV$            & 1.7e+09 & 66    & 4.2e+01  & 1.4e+09 & 64    & 9.3e-02 & 460 & 78 & 56 & 360 & 79 & 44 & 110 & 92 & 14 \\
# $\geq$ 1 Loose PAT Muon       & 1.6e+09 & 99    & 4.1e+01  & 1.4e+09 & 100   & 9.3e-02 & 460 & 100 & 56 & 360 & 100 & 44 & 110 & 100 & 14 \\
# $\geq$ 4 Good Jets            & 1.8e+07 & 1.1   & 4.6e-01  & 1.8e+07 & 1.3   & 1.2e-03 & 280 & 59 & 33 & 200 & 55 & 24 & 48 & 42 & 5.7 \\
# $\geq$ 1 Medium b-tagged Jets & 1.1e+07 & 61    & 2.8e-01  & 1.2e+07 & 67    & 8.3e-04 & 250 & 90 & 30 & 180 & 91 & 22 & 44 & 92 & 5.2 \\
# HEM Veto                      & 1.1e+07 & 98    & 2.7e-01  & 1.2e+07 & 97    & 8.1e-04 & 240 & 97 & 29 & 180 & 97 & 21 & 43 & 97 & 5.1 \\
# Jet Veto Maps                 & 1.1e+07 & 98    & 2.7e-01  & 1.2e+07 & 97    & 7.8e-04 & 230 & 96 & 28 & 170 & 96 & 20 & 41 & 97 & 4.9 \\
# $\ptmiss > 50\GeV$            & 7.0e+06 & 66    & 1.8e-01  & 7.5e+06 & 65    & 5.1e-04 & 150 & 66 & 18 & 110 & 67 & 14 & 36 & 88 & 4.3 \\
# $\geq$ 1 Tight PAT Muon       & 4.4e+06 & 62    & 1.1e-01  & 4.8e+06 & 64    & 3.2e-04 & 130 & 87 & 16 & 66 & 58 & 8 & 28 & 78 & 3.4 \\
# $\geq$ 3 Loose Muons          & 1.8e+06 & 41    & 4.5e-02  & 2.1e+06 & 44    & 1.4e-04 & 130 & 95 & 15 & 62 & 94 & 7.4 & 18 & 65 & 2.2 \\
# 0 Loose Electrons             & 1.7e+06 & 93    & 4.2e-02  & 1.9e+06 & 93    & 1.3e-04 & 100 & 80 & 12 & 51 & 83 & 6.2 & 17 & 92 & 2 \\
# $\geq$ 1 Best Dimuon          & 6.9e+02 & 0.051 & 1.7e-05  & 8.1e+02 & 0.042 & 5.5e-08 & 2.2 & 2.2 & 0.27 & 4.6 & 9 & 0.55 & 1.2 & 7.1 & 0.14 \\
# PAT-PAT Best Dimuon           & 6.6e+02 & 95    & 1.7e-05  & 6.2e+02 & 76    & 4.2e-08 & 2.0 & 91 & 0.24 & 4.3 & 93 & 0.52 & 0.21 & 18 & 0.026 \\
# PAT-PAT SR bin A              & 8.6e+01 & 13    & 2.2e-06  & 3.9e+01 & 6.3   & 2.6e-09 & 0.12 & 6.0 & 0.014 & 3.7 & 86 & 0.45 & 0.17 & 81 & 0.020 \\ \hline
# DSA-DSA Best Dimuon           & 3.2e+01 & 4.6   & 8.0e-07  & 2.2e+01 & 2.7   & 1.5e-09 & 0.011 & 0.51 & 0.0014 & 0.095 & 2 & 0.011 & 0.91 & 76 & 0.11 \\
# DSA-DSA SR bin A              & 1.6e+01 & 50    & 4.0e-07  & 8.6e+00 & 20    & 5.7e-10 & 0.0053 & 48 & 0.00064 & 0.085 & 89 & 0.010 & 0.85 & 93 & 0.10