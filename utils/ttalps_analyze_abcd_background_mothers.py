from Logger import info, warn, error, fatal, logger_print
from ttalps_samples_list import dasBackgrounds2018, dasBackgrounds2017, dasBackgrounds2016preVFP, dasSignals2018
from Histogram import Histogram2D, Histogram
from Sample import Sample, SampleType
from HistogramNormalizer import NormalizationType

from ttalps_luminosities import get_luminosity
from ttalps_cross_sections import get_cross_sections

import ROOT
import os
import math
from ctypes import c_double

year = "2018"
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "genInfo")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "ABCD_genInfo_ANv2")
skim = ("skimmed_looseSemimuonic_v3_SR", "SSDimuons", "genInfo_v3")
# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "genInfo_v3")
# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "noDimuonEffSFs_revertedMatching_ABCD", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "noDimuonEffSFs_revertedMatching_ABCD", "SR")
# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuonsPatDSA", "noDimuonEffSFs_noMatching_ABCD")
# skim = ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "noDimuonEffSFs_ABCD")
# skim = ("skimmed_3muCR_merged", "JPsiDimuons", "noDimuonEffSFs_ABCD")
hist_path = "histograms"

signals = False
reverted_matching = False
# cut_on_y = -2.0
# cut_on_x = 0.0
cut_on_y = None
cut_on_x = None
output_dir = f"../plots/backgroundMothers_{year}_{skim[1]}_{skim[2]}"
if signals:
  output_dir = f"../plots/signalMothers_{year}_{skim[1]}_{skim[2]}"
if not os.path.exists(output_dir):
  os.makedirs(output_dir)

backgrounds = globals()[f"dasBackgrounds{year}"].keys()
dimuon_collection = "BestDimuonVertex"
# dimuon_collection = "BestPFIsoDimuonVertex"
if signals or "SRDimuons" in skim[1] or "SSDimuons" in skim[1]:
  backgrounds = dasSignals2018.keys()
  dimuon_collection = "BestPFIsoDimuonVertex"


# category = ""
category = "_Pat"
# category = "_PatDSA"
# category = "_DSA"

do_mother_ids = False

samples = []
for background in backgrounds:
  samples.append(
      Sample(
          name=background.split("/")[-1],
          file_path=f"{base_path}/{background}/{skim[0]}/{hist_path}_{skim[1]}_{skim[2]}/histograms.root",
          type=SampleType.background,
          cross_sections=cross_sections,
      )
  )

flip_hists = {
  # category: (flip_horizontally, flip_vertically)
    "_Pat": (True,True),
    "_PatDSA": (False,False),
    "_DSA": (True,True),
}

flip_hist = flip_hists[category]

rebin_hist = {
    "_Pat": (20, 20),
    "_PatDSA": (20, 20),
    "_DSA": (20, 20),
    "": (4, 4),
}

resonant_categories = ["FromALP", "Resonant", "NonResonant"]
# mother_categories = ["X", "W", "tau", "B", "D", "d", "u", "s", "c", "b", "t", "e", "mu",
                    #  "g", "gamma", "Z", "rho", "pi0", "omega", "K0", "phi", "upsilon", "JPsi", "other"]
mother_categories = ["X", "W", "tau", "B", "D", "q", "l", "g", "gamma", "Z", "lightMeson", "JPsi", "other"]
# mother_categories = []

colors = [ROOT.kGreen+2, ROOT.kRed, ROOT.kOrange+1, ROOT.kMagenta+1, ROOT.kPink+1, ROOT.kCyan+1, ROOT.kViolet+1, ROOT.kTeal+1,
          ROOT.kYellow+1, ROOT.kAzure+1, ROOT.kGreen+3, ROOT.kMagenta+3, ROOT.kRed+3, ROOT.kOrange+3, ROOT.kBlue+3, ROOT.kBlue-3, ROOT.kBlack]
mother_naming = {
    # ("other", "e", "mu", "g", "gamma", "d", "u", "s", "c", "b", "t"): "Other",
    ("other", "q", "l", "g",): "Other",
    ("gamma",): "Photons",
    ("Z",): "Z",
    ("X",): "Pileup",
    ("B", "D",): "B/D mesons",
    ("W", "tau",): "SS NonResonant",
    ("lightMeson", "JPsi"): "Light flavoured mesons",
    # ("NonResonant","W","tau"): ("NonResonant",ROOT.kBlue+3),
    # ("NonResonantX",): ("NonResonant Pileup",ROOT.kOrange+1),
    # ("pi0",): ("#pi_{0}",ROOT.kCyan+1),
    # ("omega",): ("#omega",ROOT.kMagenta+3),
    # ("K0",): ("K0",ROOT.kRed+3),
    # ("phi",): ("#phi",ROOT.kOrange+3),
    # ("upsilon",): ("#Upsilon",ROOT.kTeal+1),
    # ("JPsi",): ("J/#Psi",ROOT.kBlue-3),
    # ("g",): ("gluon",ROOT.kCyan+1),
    # ("gamma",): ("photon",ROOT.kViolet+1),
    # ("Z",): ("Z",ROOT.kTeal+1),
    # ("W",): ("W",ROOT.kYellow+1),
    # ("d","u","s","c","b","t",): ("other",ROOT.kBlue),
}


# PAT-DSA
legend_settings_Pat = {
    ("B/D mesonsB/D mesons",): ("B/D meson + B/D meson", ROOT.kAzure+1),
    # ("SS NonResonantZ",): ("SS NonResonant + Z", ROOT.kPink+1),
    ("PileupPileup", "PileupSS NonResonant", "B/D mesonsPileup", "OtherPileup", "Light flavoured mesonsPileup", "PileupZ", "PileupPhotons"): ("Pileup + Pileup/X", ROOT.kGreen+1),
    ("B/D mesonsSS NonResonant",): ("B/D meson + W/#tau", ROOT.kBlue+1),
    ("OtherSS NonResonant", "Light flavoured mesonsSS NonResonant", "SS NonResonantZ", "SS NonResonantSS NonResonant",): ("W/#tau + W/#tau/X", ROOT.kPink+1),
    # (,): ("B/D + X", ROOT.kBlue+1),
    # ("B/D mesonsSS NonResonant",): ("SS NonResonant + B/D meson", ROOT.kMagenta+1),
    ("OtherOther", "Light flavoured mesonsLight flavoured mesons", "Light flavoured mesonsOther", "B/D mesonsOther", "B/D mesonsLight flavoured mesons", "B/D mesonsZ",
     "ZZ", "Light flavoured mesonsZ", "OtherZ", "OtherPhotons", "B/D mesonsPhotons", "Light flavoured mesonsPhotons", ): ("Other", ROOT.kRed),
    ("PhotonsPhotons", ): ("#gamma + #gamma", ROOT.kMagenta),
}
# PAT-DSA
legend_settings_PatDSA = {
    ("B/D mesonsB/D mesons",): ("B/D meson + B/D meson", ROOT.kAzure+1),
    # ("B/D mesonsPileup",): ("B/D meson + Pileup", ROOT.kRed+3),
    # ("PileupSS NonResonant",): ("SS NonResonant + Pileup", ROOT.kYellow+1),
    ("SS NonResonantSS NonResonant",): ("W/#tau + W/#tau", ROOT.kOrange+1),
    ("B/D mesonsSS NonResonant",): ("B/D meson + W/#tau", ROOT.kBlue+1),
    # (,): ("W/#tau + X", ROOT.kMagenta+1),
    # (): ("B/D + X", ROOT.kBlue+1),
    ("PileupPileup", "PileupSS NonResonant", "B/D mesonsPileup", "OtherPileup", "Light flavoured mesonsPileup", "PileupZ"): ("Pileup + Pileup/X", ROOT.kGreen+1),
    ("OtherOther", "OtherPileup", "Light flavoured mesonsLight flavoured mesons", "OtherSS NonResonant", "Light flavoured mesonsSS NonResonant", "SS NonResonantZ",
     "Light flavoured mesonsOther", "ZZ", "B/D mesonsZ", "Light flavoured mesonsZ", "OtherZ", "B/D mesonsOther", "B/D mesonsLight flavoured mesons",): ("Other", ROOT.kRed),
}
legend_settings_DSA = {
    ("B/D mesonsB/D mesons",): ("B/D meson + B/D meson", ROOT.kAzure+1),
    # ("SS NonResonantZ",): ("SS NonResonant + Z", ROOT.kPink+1),
    ("PileupPileup", "PileupSS NonResonant", "B/D mesonsPileup", "OtherPileup", "Light flavoured mesonsPileup", "PileupZ", "PhotonsPileup"): ("Pileup + Pileup/X", ROOT.kGreen+1),
    ("B/D mesonsSS NonResonant",): ("B/D meson + W/#tau", ROOT.kBlue+1),
    ("OtherSS NonResonant", "Light flavoured mesonsSS NonResonant", "SS NonResonantZ", "SS NonResonantSS NonResonant", "PhotonsSS NonResonant",): ("W/#tau + W/#tau/X", ROOT.kPink+1),
    # (,): ("B/D + X", ROOT.kBlue+1),
    # ("B/D mesonsSS NonResonant",): ("SS NonResonant + B/D meson", ROOT.kMagenta+1),
    ("OtherOther", "Light flavoured mesonsLight flavoured mesons", "Light flavoured mesonsOther", "B/D mesonsOther", "B/D mesonsLight flavoured mesons", "B/D mesonsZ",
     "ZZ", "Light flavoured mesonsZ", "OtherZ", "OtherPhotons", "B/D mesonsPhotons", "Light flavoured mesonsPhotons", ): ("Other", ROOT.kRed),
    ("PhotonsPhotons", "PhotonsZ"): ("#gamma + #gamma/X", ROOT.kMagenta),
}
legend_settings = legend_settings_Pat
if category == "_PatDSA":
  legend_settings = legend_settings_PatDSA
if category == "_DSA":
  legend_settings = legend_settings_DSA

legend_positions = {
    "_Pat": (0.2, 0.68, 0.45, 0.89),
    "_PatDSA": (0.2, 0.68, 0.45, 0.89),
    "_DSA": (0.2, 0.68, 0.45, 0.89),
    "": (0.2, 0.68, 0.45, 0.89),
}

resonance_colors = {
    "NonResonant": ROOT.kRed+1,
    "Resonant": ROOT.kBlue+1,
    "FalseResonant": ROOT.kGreen+1,
    "FromALP": ROOT.kGreen+1,
}

abcd_variables = {
    "_Pat": ("logAbsCollinearityAngle", "logPt"),
    "_PatDSA": ("logDxyPVTraj1", "logAbsCollinearityAngle"),
    "_DSA": ("logAbsCollinearityAngle", "logPt"),
}
variable_to_str = {
    "logLeadingPt": "log leading p_{T} [GeV]",
    "logPt": "log p_{T} [GeV]",
    "logAbsCollinearityAngle": "log |#Delta#Phi_{coll}|",
    "logDxyPVTrajSig1": "log d_{xy}^{#mu1} / #sigma_{dxy}^{#mu1}",
    "logDxyPVTrajSig2": "log d_{xy}^{#mu2} / #sigma_{dxy}^{#mu2}",
    "logDxyPVTraj1": "log d_{xy}^{#mu1} [cm]",
    "logInvMass": "log m_{#mu#mu} [GeV]",
    "outerDR": "outer #DeltaR",
    "logOuterDR": "log Outer #DeltaR",
    "log3Dangle": "log 3D angle",
    "logLxy": "log L_{xy} [cm]",
    "logNormChi2": "logNormChi2",
    "logDca": "logDca",
    "absPtLxyDPhi1": "absPtLxyDPhi1",
    "absCollinearityAngle": "absCollinearityAngle",
}
abcd_variable = abcd_variables[category]


def get_color(category_name):
  for names, settings in legend_settings.items():
    for name in names:
      if category_name == name:
        return settings[1]
  warn(f"Warning: No color found for category {category_name}, returning kGray")
  return ROOT.kGray


def get_category_name(mother_category):
  for categories, name in mother_naming.items():
    for category in categories:
      if mother_category == category:
        return name
  warn(f"Warning: No category name found for mother category {mother_category}, returning 'Other'")
  return "Other"


def get_legend_name(category_name):
  for names, settings in legend_settings.items():
    for name in names:
      if category_name == name:
        return settings[0]
  warn(f"Warning: No legend name found for category {category_name}, returning 'Other'")
  return "Other"


def merge_histograms(histograms, n_events_per_category):
  merged_histograms = {}
  # for mother_category, hist_list in histograms.items():
  count = 0
  for mother_category, n_events in n_events_per_category.items():
    hist_list = histograms[mother_category]
    if mother_category not in merged_histograms:
      merged_histograms[mother_category] = hist_list[0].Clone()
      merged_histograms[mother_category].SetDirectory(0)
    for i in range(1, len(hist_list)):
      merged_histograms[mother_category].Add(hist_list[i])
  return merged_histograms


def setup_legend(legend, merged_histograms, n_events_per_category):
  legend.Clear()
  legend_entries = []
  n_tot = get_total_events(n_events_per_category)
  for mother_category, n_events in n_events_per_category.items():
    if mother_category == "Other":
      continue  # we want to have other last in the legend
    faction_of_events = n_events_per_category[mother_category] / n_tot * 100 if n_tot > 0 else 0
    if n_events_per_category[mother_category] > 0:
      text = f"{mother_category} ({faction_of_events:.2f}%)"
    if mother_category not in legend_entries:
      hist = merged_histograms[mother_category]
      legend.AddEntry(hist, text, "f")
      legend_entries.append(mother_category)
  faction_of_events = n_events_per_category["Other"] / n_tot * 100 if n_tot > 0 else 0
  if n_events_per_category["Other"] > 0:
    text = f"Other ({faction_of_events:.2f}%)"
  if "Other" not in legend_entries:
    legend.AddEntry(merged_histograms["Other"], text, "f")
  return legend


def setup_resonance_legend(legend, merged_histograms, n_events_per_category):
  legend.Clear()
  legend_entries = []
  n_tot = get_total_events(n_events_per_category)
  for mother_category, n_events in n_events_per_category.items():
    faction_of_events = n_events_per_category[mother_category] / n_tot * 100 if n_tot > 0 else 0
    if n_events_per_category[mother_category] > 0:
      text = f"{mother_category} ({faction_of_events:.2f}%)"
    if mother_category not in legend_entries:
      hist = merged_histograms[mother_category]
      legend.AddEntry(hist, text, "f")
      legend_entries.append(mother_category)
  return legend


def get_total_events(n_events_per_category):
  total_events = 0
  for mother_category, n_events in n_events_per_category.items():
    total_events += n_events
  return total_events


def print_events_per_category(n_events_per_category):
  n_tot = get_total_events(n_events_per_category)
  n_events_per_category_sorted = dict(sorted(n_events_per_category.items(), key=lambda item: item[1], reverse=True))
  for mother_category, n_events in n_events_per_category_sorted.items():
    if n_events > 0:
      info(f"{mother_category}: \t {n_events:.2f} events \t ({n_events/n_tot*100:.2f}%)")

  info(f"Total: \t {n_tot} events")

# WIP - I haven't made this work


def flip_hist_horizontally(hist):
  # The method changes the x-axis from X to -X. The range of the axis will
  # be changed from (a, b) to (-b, -a), and the value on the x-axis will be changed
  # from x to -x. The y-axis will not be changed.

  if hist is None:
    return None

  flipped_hist = ROOT.TH2F(hist.GetName() + f"_flipped_{ROOT.gRandom.Rndm()}", hist.GetTitle(),
                           hist.GetNbinsX(), -hist.GetXaxis().GetXmax(), -hist.GetXaxis().GetXmin(),
                           hist.GetNbinsY(), hist.GetYaxis().GetXmin(), hist.GetYaxis().GetXmax())

  for i in range(1, hist.GetNbinsX() + 1):
    for j in range(1, hist.GetNbinsY() + 1):
      flipped_hist.SetBinContent(hist.GetNbinsX()+1-i, j, hist.GetBinContent(i, j))
      flipped_hist.SetBinError(hist.GetNbinsX()+1-i, j, hist.GetBinError(i, j))

  flipped_hist.GetXaxis().SetTitle("-")
  flipped_hist.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())

  return flipped_hist

# WIP - I haven't made this work


def flip_hist_vertically(hist):
  # The method changes the y-axis from Y to -Y. The range of the axis will
  # be changed from (a, b) to (-b, -a), and the value on the y-axis will be changed
  # from y to -y. The x-axis will not be changed.

  if hist is None:
    return None

  flipped_hist = ROOT.TH2F(hist.GetName() + f"_flipped_{ROOT.gRandom.Rndm()}", hist.GetTitle(),
                           hist.GetNbinsX(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax(),
                           hist.GetNbinsY(), -hist.GetYaxis().GetXmax(), -hist.GetYaxis().GetXmin())

  for i in range(1, hist.GetNbinsX() + 1):
    for j in range(1, hist.GetNbinsY() + 1):
      flipped_hist.SetBinContent(i, hist.GetNbinsY()+1-j, hist.GetBinContent(i, j))
      flipped_hist.SetBinError(i,  hist.GetNbinsY()+1-j, hist.GetBinError(i, j))

  flipped_hist.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
  flipped_hist.GetYaxis().SetTitle("-")
  flipped_hist.SetFillColorAlpha(hist.GetFillColor(), 0.5)

  return flipped_hist

def format_value_unc(val, unc):
  if unc <= 0:
      return f"{val:.2f} ± 0"

  exponent = math.floor(math.log10(abs(unc)))
  unc_rounded = round(unc, -exponent)
  nd = max(0, -int(math.floor(math.log10(abs(unc_rounded)))))
  val_rounded = round(val, nd)
  if val_rounded == 0 and val != 0:
      nd += 1
      val_rounded = round(val, nd)
      unc_rounded = round(unc, nd)
  return f"{val_rounded:.{nd}f} #pm {unc_rounded:.{nd}f}"

def main():
  ROOT.gROOT.SetBatch(True)

  legend = ROOT.TLegend(legend_positions[category][0], legend_positions[category]
                        [1], legend_positions[category][2], legend_positions[category][3])
  legend.SetBorderSize(0)
  legend.SetFillStyle(0)
  legend.SetTextSize(0.022)
  legend2 = ROOT.TLegend(legend_positions[category][0], legend_positions[category]
                         [1], legend_positions[category][2], legend_positions[category][3])
  legend2.SetBorderSize(0)
  legend2.SetFillStyle(0)
  legend2.SetTextSize(0.022)
  legend3 = ROOT.TLegend(legend_positions[category][0], legend_positions[category]
                         [1], legend_positions[category][2], legend_positions[category][3])
  legend3.SetBorderSize(0)
  legend3.SetFillStyle(0)
  legend3.SetTextSize(0.022)

  background_histograms = {}
  resonance_histograms = {}
  resonance_motherid1_histograms = {}
  n_events_per_category = {}
  n_events_per_resonance = {}
  n_events_per_resonance_motherid1 = {}
  n_events_per_resonance_and_sample = {}

  for sample in samples:

    info(f"Processing sample: {sample.name} from {sample.file_path}")
    file = ROOT.TFile(sample.file_path, "READ")
    cut_flow = file.Get("cutFlow")
    sample.initial_weight_sum = cut_flow.GetBinContent(1)

    processed_categories = []
    n_events_per_resonance_and_sample[sample.name] = {}

    for mother1_category_ in mother_categories:
      same_category_included = False
      for mother2_category_ in mother_categories:
        categories_sorted = sorted([mother1_category_, mother2_category_])
        mother1_category = categories_sorted[0]
        mother2_category = categories_sorted[1]
        category_name1 = get_category_name(mother1_category)
        category_name2 = get_category_name(mother2_category)
        category_name_sorted = sorted([category_name1, category_name2])
        category_name = f"{category_name_sorted[0]}{category_name_sorted[1]}"
        legend_name = get_legend_name(category_name)
        if f"{mother1_category}{mother2_category}" in processed_categories:
          continue  # avoiding eg. including both pi0K0 and K0pi0
        processed_categories.append(f"{mother1_category}{mother2_category}")
        hist_name = f"{dimuon_collection}_{abcd_variable[0]}_vs_{abcd_variable[1]}_{mother1_category}{mother2_category}{category}"
        if reverted_matching:
          hist_name = f"{dimuon_collection}_revertedMatching_{abcd_variable[0]}_vs_{abcd_variable[1]}_{mother1_category}{mother2_category}{category}"
        hist = Histogram2D(
            name=hist_name,
            title=f"{category_name} {abcd_variable[0]} vs {abcd_variable[1]}",
            norm_type=NormalizationType.to_lumi,
            x_rebin=rebin_hist[category][0],
            y_rebin=rebin_hist[category][1],
        )
        hist.load(file)

        if hist.hist is None or hist.hist.GetEntries() == 0:
          # warn(f"{hist_name} has no entries")
          continue

        # hist.setup()
        hist.hist.Rebin2D(hist.x_rebin, hist.y_rebin)
        hist.hist.Scale(sample.cross_section * luminosity / sample.initial_weight_sum)

        if flip_hist[0]:  # flip horizontally
          flipped_hist = flip_hist_horizontally(hist.hist)
          hist.hist = flipped_hist
        if flip_hist[1]:  # flip vertically
          flipped_hist = flip_hist_vertically(hist.hist)
          hist.hist = flipped_hist

        hist.hist.SetFillStyle(1001)
        color = get_color(category_name)
        hist.hist.SetFillColorAlpha(color, 0.4)
        hist.hist.SetLineColorAlpha(color, 0)

        cloned_hist = hist.hist.Clone()
        cloned_hist.SetDirectory(0)

        if legend_name not in background_histograms:
          background_histograms[legend_name] = [cloned_hist]
        else:
          if background_histograms[legend_name] is None:
            background_histograms[legend_name] = [cloned_hist]
          else:
            background_histograms[legend_name].append(cloned_hist)

        if legend_name not in n_events_per_category:
          n_events_per_category[legend_name] = 0
        n_events = cloned_hist.Integral(0, cloned_hist.GetNbinsX()+1,
                                        0, cloned_hist.GetNbinsY()+1)
        n_events_per_category[legend_name] += n_events

    for resonance in resonant_categories:
      hist_name = f"{dimuon_collection}{resonance}_{abcd_variable[0]}_vs_{abcd_variable[1]}{category}"
      if reverted_matching:
        hist_name = f"{dimuon_collection}{resonance}_revertedMatching_{abcd_variable[0]}_vs_{abcd_variable[1]}{category}"
      hist = Histogram2D(
          name=hist_name,
          title=f"{resonance} {abcd_variable[0]} vs {abcd_variable[1]}",
          norm_type=NormalizationType.to_lumi,
          x_rebin=rebin_hist[category][0],
          y_rebin=rebin_hist[category][1],
      )
      hist.load(file)
      if hist.hist is None or hist.hist.GetEntries() == 0:
        warn(f"{hist_name} has no entries")
        continue

      if (cut_on_y != None):
        ybin_cut = hist.hist.GetYaxis().FindBin(cut_on_y)
        for ix in range(1, hist.hist.GetNbinsX() + 1):
          for iy in range(1, ybin_cut):
          # for iy in range(ybin_cut, hist.hist.GetNbinsY() + 1):
            hist.hist.SetBinContent(ix, iy, 0.0)
            hist.hist.SetBinError(ix, iy, 0.0)
      if (cut_on_x != None):
        xbin_cut = hist.hist.GetXaxis().FindBin(cut_on_x)
        # for ix in range(xbin_cut, hist.hist.GetNbinsX() + 1):
        for ix in range(1, xbin_cut):
          for iy in range(1, hist.hist.GetNbinsY() + 1):
            hist.hist.SetBinContent(ix, iy, 0.0)
            hist.hist.SetBinError(ix, iy, 0.0)
      
      
      hist.hist.Rebin2D(hist.x_rebin, hist.y_rebin)
      hist.hist.Scale(sample.cross_section * luminosity / sample.initial_weight_sum)

      if flip_hist[0]:  # flip horizontally
        flipped_hist = flip_hist_horizontally(hist.hist)
        hist.hist = flipped_hist
      if flip_hist[1]:  # flip vertically
        flipped_hist = flip_hist_vertically(hist.hist)
        hist.hist = flipped_hist

      hist.hist.SetFillStyle(1001)
      color = resonance_colors[resonance]
      hist.hist.SetFillColorAlpha(color, 0.4)
      hist.hist.SetLineColorAlpha(color, 0)

      cloned_hist = hist.hist.Clone()
      cloned_hist.SetDirectory(0)

      if resonance not in resonance_histograms or resonance_histograms is None:
        resonance_histograms[resonance] = [cloned_hist]
      else:
        resonance_histograms[resonance].append(cloned_hist)

      if resonance not in n_events_per_resonance:
        n_events_per_resonance[resonance] = 0
      n_events_unc = c_double(0.0)
      n_events = cloned_hist.IntegralAndError(0, cloned_hist.GetNbinsX()+1,
                                      0, cloned_hist.GetNbinsY()+1, n_events_unc)
      n_events_per_resonance[resonance] += n_events
      n_events_per_resonance_and_sample[sample.name][resonance] = (n_events, n_events_unc.value)

      if resonance == "Resonant" and do_mother_ids:
        hist_motherPdgId1 = Histogram(
            name=f"BestPFIsoDimuonVertex{resonance}{category}_motherPdgId1",
            title=f"{resonance} mother PDG ID",
            norm_type=NormalizationType.to_lumi,
        )
        hist_motherPdgId1.load(file)
        if hist_motherPdgId1.hist is None or hist_motherPdgId1.hist.GetEntries() == 0:
          warn(f"{hist_motherPdgId1.name} has no entries")
          continue
        hist_motherPdgId1.hist.Scale(sample.cross_section * luminosity / sample.initial_weight_sum)
        hist_motherPdgId1.hist.SetLineColorAlpha(color, 1)
        cloned_hist_motherPdgId1 = hist_motherPdgId1.hist.Clone()
        cloned_hist_motherPdgId1.SetDirectory(0)

        if resonance not in resonance_motherid1_histograms or resonance_motherid1_histograms is None:
          resonance_motherid1_histograms[resonance] = [cloned_hist_motherPdgId1]
        else:
          resonance_motherid1_histograms[resonance].append(cloned_hist_motherPdgId1)
        if resonance not in n_events_per_resonance_motherid1:
          n_events_per_resonance_motherid1[resonance] = 0
        n_events = cloned_hist_motherPdgId1.Integral(0, cloned_hist_motherPdgId1.GetNbinsX()+1)
        n_events_per_resonance_motherid1[resonance] += n_events

    file.Close()

  
  x_prefix = ""
  # x_prefix = "-"
  y_prefix = ""
  if flip_hist[0]:
    x_prefix = "-"
  if flip_hist[1]:
    y_prefix = "-"

  category_str = ""
  if category == "_Pat":
    category_str = "PAT-PAT"
  if category == "_PatDSA":
    category_str = "PAT-DSA"
  if category == "_DSA":
    category_str = "DSA-DSA"

  if mother_categories != []:
    n_events_per_category_sorted = dict(sorted(n_events_per_category.items(), key=lambda item: item[1], reverse=True))
    merged_histograms = merge_histograms(background_histograms, n_events_per_category_sorted)

    legend = setup_legend(legend, merged_histograms, n_events_per_category_sorted)

    canvas = ROOT.TCanvas("canvas", "Background Sources", 800, 800)
    canvas.SetLeftMargin(0.15)
    # draw 2D stack as box
    histograms_iter = iter(n_events_per_category_sorted.items())
    first_name, first_n_events = next(histograms_iter)
    first_hist = merged_histograms[first_name]
    first_hist.Draw("BOX")
    for name, n_events in histograms_iter:
      hist = merged_histograms[name]
      hist.Draw("BOX SAME")
    first_hist.SetStats(0)
    abcd_variable1_str = abcd_variable[1]
    abcd_variable0_str = abcd_variable[0]
    if abcd_variable[1] in variable_to_str:
      abcd_variable1_str = variable_to_str[abcd_variable[1]]
    if abcd_variable[0] in variable_to_str:
      abcd_variable0_str = variable_to_str[abcd_variable[0]]

    first_hist.GetYaxis().SetTitle(y_prefix+abcd_variable0_str)
    first_hist.GetXaxis().SetTitle(x_prefix+abcd_variable1_str)
    
    first_hist.SetTitle(f"Background sources for {category_str} dimuons")
    legend.Draw()
    canvas.Update()
    canvas.SaveAs(f"{output_dir}/background_sources{category}.pdf")
    info(f"Saved background sources to {output_dir}/background_sources{category}.pdf")

    print_events_per_category(n_events_per_category)

  # Resonance plot:
  n_events_per_resonance_sorted = dict(sorted(n_events_per_resonance.items(), key=lambda item: item[1], reverse=True))
  merged_resonance_histograms = merge_histograms(resonance_histograms, n_events_per_resonance_sorted)

  legend2 = setup_resonance_legend(legend2, merged_resonance_histograms, n_events_per_resonance_sorted)
  canvas2 = ROOT.TCanvas("canvas2", "Background Resonances", 800, 800)
  canvas2.SetLeftMargin(0.15)
  histograms_iter = iter(n_events_per_resonance_sorted.items())
  first_name, first_n_events = next(histograms_iter)
  first_hist = merged_resonance_histograms[first_name]
  first_hist.Draw("BOX")
  for name, n_events in histograms_iter:
    hist = merged_resonance_histograms[name]
    hist.Draw("BOX SAME")
  first_hist.SetStats(0)

  abcd_variable1_str = abcd_variable[1]
  abcd_variable0_str = abcd_variable[0]
  if abcd_variable[1] in variable_to_str:
    abcd_variable1_str = variable_to_str[abcd_variable[1]]
  if abcd_variable[0] in variable_to_str:
    abcd_variable0_str = variable_to_str[abcd_variable[0]]

  first_hist.GetYaxis().SetTitle(y_prefix+abcd_variable0_str)
  first_hist.GetXaxis().SetTitle(x_prefix+abcd_variable1_str)
  first_hist.SetTitle(f"Background resonances for {category_str} dimuons")
  legend2.Draw()
  canvas2.Update()
  if not signals:
    canvas2.SaveAs(f"{output_dir}/background_resonances{category}.pdf")
    info(f"Saved background resonances to {output_dir}/background_resonances{category}.pdf")

  print_events_per_category(n_events_per_resonance)

  if signals:
    h2_resonant = ROOT.TH2D("", "", 5, 0, 5, 5, 0, 5)
    h2_all = ROOT.TH2D("all", "all", 5, 0, 5, 5, 0, 5)
    masses = ["0p35", "2", "12", "30", "60"]
    ctaus = ["1e-5", "1e0", "1e1", "1e2", "1e3"]
    for i, mass in enumerate(masses):
      mass_ = float(mass.replace("p", "."))
      h2_resonant.GetXaxis().SetBinLabel(i+1, str(mass_))
      for j, ctau in enumerate(ctaus):
        sample_name = f"tta_mAlp-{mass}GeV_ctau-{ctau}mm"
        if "FromALP" not in n_events_per_resonance_and_sample[sample_name]:
          continue
        n_resonant, n_resonant_unc = n_events_per_resonance_and_sample[sample_name]["FromALP"]
        n_nonresonant, n_nonresonant_unc = n_events_per_resonance_and_sample[sample_name]["NonResonant"]
        n_all = n_resonant+n_nonresonant
        n_all_unc = math.sqrt(n_resonant_unc**2 + n_nonresonant_unc**2)
        h2_resonant.SetBinContent(i+1, j+1, n_resonant)
        h2_resonant.SetBinError(i+1, j+1, n_resonant_unc)
        h2_all.SetBinContent(i+1, j+1, n_all)
        h2_all.SetBinError(i+1, j+1, n_all_unc)
    for j, ctau in enumerate(ctaus):
      h2_resonant.GetYaxis().SetBinLabel(j+1, str(ctau))

    h2_resonant.Divide(h2_all)
    h2_resonant.SaveAs("../signal_resonances.root")

    ROOT.gStyle.SetOptStat(0)
    c1 = ROOT.TCanvas("c1", "c1", 800, 600)
    h2_resonant.Draw("COLZ")
    h2_resonant.GetXaxis().SetLabelSize(0.04)
    h2_resonant.GetYaxis().SetLabelSize(0.04)
    h2_resonant.GetXaxis().SetTitle("ALP mass [GeV]")
    h2_resonant.GetYaxis().SetTitle("ALP c#tau [mm]")
    h2_resonant.GetZaxis().SetTitle("Fraction of dimuons from ALPs")

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)
    latex.SetTextSize(0.025)
    latex.SetTextFont(42)

    for ix in range(1, h2_resonant.GetNbinsX()+1):
        for iy in range(1, h2_resonant.GetNbinsY()+1):
            val = h2_resonant.GetBinContent(ix, iy)
            if val == 0.0:
              continue
            unc = h2_resonant.GetBinError(ix, iy)
            txt = format_value_unc(val, unc)
            x = h2_resonant.GetXaxis().GetBinCenter(ix)
            y = h2_resonant.GetYaxis().GetBinCenter(iy)
            latex.DrawLatex(x, y, txt)
    
    c1.SetRightMargin(0.15)
    c1.SaveAs(f"{output_dir}/signal_resonances{category}.pdf")
    info(f"Saved signal resonances to {output_dir}/signal_resonances{category}.pdf")
    

  if do_mother_ids:
    n_events_per_resonance_motherid1_sorted = dict(
        sorted(n_events_per_resonance_motherid1.items(), key=lambda item: item[1], reverse=True))
    merged_resonance_motherid1_histograms = merge_histograms(
        resonance_motherid1_histograms, n_events_per_resonance_motherid1_sorted)

    legend3 = setup_resonance_legend(legend3, merged_resonance_motherid1_histograms,
                                     n_events_per_resonance_motherid1_sorted)
    canvas3 = ROOT.TCanvas("canvas3", "Background Resonances MohterID", 800, 600)
    histograms_iter = iter(n_events_per_resonance_motherid1_sorted.items())
    first_name, first_n_events = next(histograms_iter)
    first_hist = merged_resonance_motherid1_histograms[first_name]
    first_hist.Draw("hist")
    for name, n_events in histograms_iter:
      hist = merged_resonance_motherid1_histograms[name]
      hist.Draw("hist SAME")
    first_hist.SetStats(0)
    first_hist.GetXaxis().SetTitle(variable_to_str[abcd_variable[1]])
    first_hist.GetYaxis().SetTitle("#Events")
    first_hist.SetTitle(f"Background resonances mother IDs for {category_str} dimuons")
    legend3.Draw()
    canvas3.Update()
    canvas3.SaveAs(f"{output_dir}/background_resonances_motherIDs{category}.pdf")
    info(f"Saved background resonances to {output_dir}/background_resonances_motherIDs{category}.pdf")


if __name__ == "__main__":
  main()
