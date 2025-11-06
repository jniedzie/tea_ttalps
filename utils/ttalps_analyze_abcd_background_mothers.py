from Logger import info, warn, error, fatal, logger_print
from ttalps_samples_list import dasBackgrounds2018
from Histogram import Histogram2D, Histogram
from Sample import Sample, SampleType
from HistogramNormalizer import NormalizationType

from ttalps_luminosities import get_luminosity
from ttalps_cross_sections import get_cross_sections

import ROOT
import os

year = "2018"
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "SRDimuonsDSAChi2DCADPhi",
        "LooseNonLeadingMuonsVertexSegmentMatch_genABCD")
hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_dimuonEffSFs_DSAEffSFs_jecSFs"


backgrounds = dasBackgrounds2018.keys()
# backgrounds = ["backgrounds2018/QCD_Pt-1000"]

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

rebin_hist = {
    "_Pat": (20, 20),
    "_PatDSA": (20, 20),
    "_DSA": (20, 20),
}

resonant_categories = ["FromALP", "Resonant", "NonResonant"]
mother_categories = ["X", "W", "tau", "B", "D", "d", "u", "s", "c", "b", "t", "e", "mu",
                     "g", "gamma", "Z", "rho", "pi0", "omega", "K0", "phi", "upsilon", "JPsi", "other"]

colors = [ROOT.kGreen+2, ROOT.kRed, ROOT.kOrange+1, ROOT.kMagenta+1, ROOT.kPink+1, ROOT.kCyan+1, ROOT.kViolet+1, ROOT.kTeal+1,
          ROOT.kYellow+1, ROOT.kAzure+1, ROOT.kGreen+3, ROOT.kMagenta+3, ROOT.kRed+3, ROOT.kOrange+3, ROOT.kBlue+3, ROOT.kBlue-3, ROOT.kBlack]
mother_naming = {
    ("other", "e", "mu", "g", "gamma", "d", "u", "s", "c", "b", "t"): "Other",
    ("Z",): "Z",
    ("X",): "Pileup",
    ("B", "D",): "B/D mesons",
    ("W", "tau",): "SS NonResonant",
    ("pi0", "rho", "omega", "K0", "phi", "upsilon", "JPsi"): "Light flavoured mesons",
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
    ("B/D mesonsB/D mesons",): ("B/D + B/D", ROOT.kAzure+1),
    # ("SS NonResonantZ",): ("SS NonResonant + Z", ROOT.kPink+1),
    ("PileupPileup", "PileupSS NonResonant", "B/D mesonsPileup", "OtherPileup", "Light flavoured mesonsPileup", "PileupZ"): ("Pileup + Pileup/X", ROOT.kGreen+1),
    ("SS NonResonantSS NonResonant",): ("W/#tau + W/#tau", ROOT.kOrange+1),
    ("B/D mesonsSS NonResonant",): ("B/D + W/#tau", ROOT.kBlue+1),
    ("OtherSS NonResonant", "Light flavoured mesonsSS NonResonant", "SS NonResonantZ",): ("W/#tau + X", ROOT.kPink+1),
    # (,): ("B/D + X", ROOT.kBlue+1),
    # ("B/D mesonsSS NonResonant",): ("SS NonResonant + B/D meson", ROOT.kMagenta+1),
    ("OtherOther", "Light flavoured mesonsLight flavoured mesons", "Light flavoured mesonsOther", "B/D mesonsOther", "B/D mesonsLight flavoured mesons", "B/D mesonsZ",
     "ZZ", "Light flavoured mesonsZ", "OtherZ"): ("Other", ROOT.kRed),

}
# PAT-DSA
legend_settings_PatDSA = {
    ("B/D mesonsB/D mesons",): ("B/D + B/D", ROOT.kAzure+1),
    # ("B/D mesonsPileup",): ("B/D meson + Pileup", ROOT.kRed+3),
    # ("PileupSS NonResonant",): ("SS NonResonant + Pileup", ROOT.kYellow+1),
    ("SS NonResonantSS NonResonant",): ("W/#tau + W/#tau", ROOT.kOrange+1),
    ("B/D mesonsSS NonResonant",): ("B/D + W/#tau", ROOT.kBlue+1),
    # (,): ("W/#tau + X", ROOT.kMagenta+1),
    # (): ("B/D + X", ROOT.kBlue+1),
    ("PileupPileup", "PileupSS NonResonant", "B/D mesonsPileup", "OtherPileup", "Light flavoured mesonsPileup", "PileupZ"): ("Pileup + Pileup/X", ROOT.kGreen+1),
    ("OtherOther", "OtherPileup", "Light flavoured mesonsLight flavoured mesons", "OtherSS NonResonant", "Light flavoured mesonsSS NonResonant", "SS NonResonantZ",
     "Light flavoured mesonsOther", "ZZ", "B/D mesonsZ", "Light flavoured mesonsZ", "OtherZ", "B/D mesonsOther", "B/D mesonsLight flavoured mesons",): ("Other", ROOT.kRed),
}
# DSA-DSA
legend_settings_DSA = {
    ("B/D mesonsB/D mesons",): ("B/D + B/D", ROOT.kAzure+1),
    # ("B mesonsSS NonResonant","B mesonsOther","B mesonsLight flavoured mesons",): ("B mesons + Other", ROOT.kBlue+1),
    # ("D mesonsSS NonResonant","D mesonsOther","D mesonsLight flavoured mesons",): ("D mesons + Other", ROOT.kBlue+1),
    # ("B/D mesonsOther","B/D mesonsLight flavoured mesons",): ("B/D + X", ROOT.kBlue+1),
    ("B/D mesonsSS NonResonant",): ("B/D + W/#tau", ROOT.kBlue+1),
    # ("B/D mesonsSS NonResonant",): ("SS NonResonant + B/D meson", ROOT.kMagenta+1),
    # ("B/D mesonsPileup",): ("B/D meson + Pileup", ROOT.kRed+2),
    ("PileupPileup", "PileupSS NonResonant", "OtherPileup", "Light flavoured mesonsPileup", "B/D mesonsPileup",): ("Pileup + Pileup/X", ROOT.kGreen+2),
    ("SS NonResonantSS NonResonant",): ("W/#tau + W/#tau", ROOT.kOrange+1),
    ("OtherOther", "OtherSS NonResonant", "Light flavoured mesonsSS NonResonant", "B/D mesonsOther", "B/D mesonsLight flavoured mesons"
     "Light flavoured mesonsLight flavoured mesons", "Light flavoured mesonsOther", "SS NonResonantZ", "PileupZ", "ZZ", "B/D mesonsZ",
     "Light flavoured mesonsZ", "OtherZ",): ("Other", ROOT.kRed),
}
legend_settings = legend_settings_Pat
if category == "_PatDSA":
  legend_settings = legend_settings_PatDSA
if category == "_DSA":
  legend_settings = legend_settings_DSA

legend_positions = {
    "_Pat": (0.12, 0.12, 0.4, 0.35),
    "_PatDSA": (0.6, 0.12, 0.89, 0.35),
    "_DSA": (0.12, 0.12, 0.35, 0.35),
}

resonance_colors = {
    "NonResonant": ROOT.kRed+1,
    "Resonant": ROOT.kBlue+1,
    "FalseResonant": ROOT.kGreen+1,
}

abcd_variables = {
    "_Pat": ("logAbsCollinearityAngle", "logLeadingPt"),
    "_PatDSA": ("logDxyPVTrajSig1", "outerDR"),
    "_DSA": ("logLxy", "log3Dangle"),
}
variable_to_str = {
    "logLeadingPt": "log leading p_{T} [GeV]",
    "logAbsCollinearityAngle": "log |#Delta#Phi_{coll}|",
    "logDxyPVTrajSig1": "log d_{xy}^{#mu1} / #sigma_{dxy}^{#mu1}",
    "outerDR": "outer #DeltaR",
    "log3Dangle": "log 3D angle",
    "logLxy": "log L_{xy} [cm]",
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
      merged_histograms[mother_category].Reset()
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


def main():
  ROOT.gROOT.SetBatch(True)

  legend = ROOT.TLegend(legend_positions[category][0], legend_positions[category]
                        [1], legend_positions[category][2], legend_positions[category][3])
  legend.SetBorderSize(0)
  legend.SetFillStyle(0)
  legend.SetTextSize(0.03)
  legend2 = ROOT.TLegend(legend_positions[category][0], legend_positions[category]
                         [1], legend_positions[category][2], legend_positions[category][3])
  legend2.SetBorderSize(0)
  legend2.SetFillStyle(0)
  legend2.SetTextSize(0.03)
  legend3 = ROOT.TLegend(legend_positions[category][0], legend_positions[category]
                         [1], legend_positions[category][2], legend_positions[category][3])
  legend3.SetBorderSize(0)
  legend3.SetFillStyle(0)
  legend3.SetTextSize(0.03)

  background_histograms = {}
  resonance_histograms = {}
  resonance_motherid1_histograms = {}
  n_events_per_category = {}
  n_events_per_resonance = {}
  n_events_per_resonance_motherid1 = {}

  for sample in samples:

    info(f"Processing sample: {sample.name} from {sample.file_path}")
    file = ROOT.TFile(sample.file_path, "READ")
    cut_flow = file.Get("cutFlow")
    sample.initial_weight_sum = cut_flow.GetBinContent(1)

    processed_categories = []

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
        hist_name = f"BestPFIsoDimuonVertex_{abcd_variable[0]}_vs_{abcd_variable[1]}_{mother1_category}{mother2_category}{category}"
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
      hist_name = f"BestPFIsoDimuonVertex{resonance}_{abcd_variable[0]}_vs_{abcd_variable[1]}{category}"
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

      hist.hist.Rebin2D(hist.x_rebin, hist.y_rebin)
      hist.hist.Scale(sample.cross_section * luminosity / sample.initial_weight_sum)

      # if category == "_Pat":
      #   flipped_hist = flip_hist_horizontally(hist.hist)
      #   flipped_hist = flip_hist_vertically(flipped_hist)
      #   hist.hist = flipped_hist

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
      n_events = cloned_hist.Integral(0, cloned_hist.GetNbinsX()+1,
                                      0, cloned_hist.GetNbinsY()+1)
      n_events_per_resonance[resonance] += n_events

      if resonance == "Resonant" and do_mother_ids:
        hist_motherPdgId1 = Histogram(
            name=f"BestPFIsoDimuonVertex{resonance}{category}_motherPdgId1",
            title=f"{resonance} mother PDG ID",
            norm_type=NormalizationType.to_lumi,
        )
        print(f"hist_motherPdgId1 name: {hist_motherPdgId1.name}")
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

  n_events_per_category_sorted = dict(sorted(n_events_per_category.items(), key=lambda item: item[1], reverse=True))
  merged_histograms = merge_histograms(background_histograms, n_events_per_category_sorted)

  legend = setup_legend(legend, merged_histograms, n_events_per_category_sorted)
  canvas = ROOT.TCanvas("canvas", "Background Sources", 800, 600)
  # draw 2D stack as box
  histograms_iter = iter(n_events_per_category_sorted.items())
  first_name, first_n_events = next(histograms_iter)
  first_hist = merged_histograms[first_name]
  # set x axis range from xmin to xmax
  # first_hist.GetXaxis().SetRangeUser(0, 8)
  # first_hist.GetYaxis().SetRangeUser(-5, 3)
  first_hist.Draw("BOX")
  for name, n_events in histograms_iter:
    hist = merged_histograms[name]
    hist.Draw("BOX SAME")
  first_hist.SetStats(0)
  first_hist.GetXaxis().SetTitle(variable_to_str[abcd_variable[1]])
  first_hist.GetYaxis().SetTitle(variable_to_str[abcd_variable[0]])
  category_str = category.replace("_", " ").strip()
  first_hist.SetTitle(f"Background sources for {category_str} dimuons")
  legend.Draw()
  canvas.Update()
  canvas.SaveAs(f"../plots/backgroundMothers2018/background_sources{category}.png")
  info(f"Saved background sources to ../plots/backgroundMothers2018/background_sources{category}.png")

  print_events_per_category(n_events_per_category)

  # Resonance plot:
  n_events_per_resonance_sorted = dict(sorted(n_events_per_resonance.items(), key=lambda item: item[1], reverse=True))
  merged_resonance_histograms = merge_histograms(resonance_histograms, n_events_per_resonance_sorted)

  legend2 = setup_resonance_legend(legend2, merged_resonance_histograms, n_events_per_resonance_sorted)
  canvas2 = ROOT.TCanvas("canvas2", "Background Resonances", 800, 600)
  histograms_iter = iter(n_events_per_resonance_sorted.items())
  first_name, first_n_events = next(histograms_iter)
  first_hist = merged_resonance_histograms[first_name]
  first_hist.Draw("BOX")
  for name, n_events in histograms_iter:
    hist = merged_resonance_histograms[name]
    hist.Draw("BOX SAME")
  first_hist.SetStats(0)
  first_hist.GetXaxis().SetTitle(variable_to_str[abcd_variable[1]])
  first_hist.GetYaxis().SetTitle(variable_to_str[abcd_variable[0]])
  first_hist.SetTitle(f"Background resonances for {category_str} dimuons")
  legend2.Draw()
  canvas2.Update()
  canvas2.SaveAs(f"../plots/backgroundMothers2018/background_resonances{category}.png")
  info(f"Saved background resonances to ../plots/backgroundMothers2018/background_resonances{category}.png")

  print_events_per_category(n_events_per_resonance)

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
    canvas3.SaveAs(f"../plots/backgroundMothers2018/background_resonances_motherIDs{category}.png")
    info(f"Saved background resonances to ../plots/backgroundMothers2018/background_resonances_motherIDs{category}.png")


if __name__ == "__main__":
  main()
