import ROOT
import math
from ABCDPlotter import ABCDPlotter
from ABCDHelper import ABCDHelper
import importlib
import argparse
from Logger import info

import os

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="", help="Path to the config file.")
parser.add_argument("--theory", type=bool, default=False, help="Whether to use theory cross sections.")
args = parser.parse_args()

# z_max = None
## For cross section = 0.01
# z_max= {
#     "_Pat": 18,
#     "_PatDSA": 4,
#     "_DSA": 7,
# }
## For coupling = 1.0
z_max= {
    "_Pat": 500,
    "_PatDSA": 45,
    "_DSA": 160,
}

syst_unc = {}
syst_unc["_Pat"] = None
syst_unc["_PatDSA"] = None
syst_unc["_DSA"] = None

## datacards_SR_ANv6_regionBCD
# syst_unc["_Pat"] = {
# 	("0p35", "1e-5"):	(0.1277,0.1268),
# 	("0p35", "1e0"):	(0.6653,0.6655),
# 	("0p35", "1e1"):	(0.7803,0.7806),
# 	("0p35", "1e2"):	(0.7961,0.7965),
# 	("0p35", "1e3"):	(0.7438,0.7444),
# 	("2", "1e-5"):	(0.1886,0.1731),
# 	("2", "1e0"):	(0.3200,0.3208),
# 	("2", "1e1"):	(0.7729,0.7733),
# 	("2", "1e2"):	(0.8648,0.8652),
# 	("2", "1e3"):	(0.8723,0.8723),
# 	("12", "1e-5"):	(0.1268,0.1274),
# 	("12", "1e0"):	(0.1044,0.1074),
# 	("12", "1e1"):	(0.5899,0.5903),
# 	("12", "1e2"):	(0.9092,0.9096),
# 	("12", "1e3"):	(0.9118,0.9126),
# 	("30", "1e-5"):	(0.2255,0.2228),
# 	("30", "1e0"):	(0.1015,0.1032),
# 	("30", "1e1"):	(0.3939,0.3946),
# 	("30", "1e2"):	(0.7866,0.7870),
# 	("30", "1e3"):	(0.9018,0.9028),
# 	("60", "1e-5"):	(0.1357,0.1346),
# 	("60", "1e0"):	(0.1036,0.1063),
# 	("60", "1e1"):	(0.3135,0.3149),
# 	("60", "1e2"):	(0.6989,0.6994),
# 	("60", "1e3"):	(0.8473,0.8483),
# }
# syst_unc["_PatDSA"] = {
# 	("0p35", "1e-5"):	(0.1138,0.1281),
# 	("0p35", "1e0"):	(0.1293,0.1256),
# 	("0p35", "1e1"):	(0.1833,0.1853),
# 	("0p35", "1e2"):	(0.2166,0.2164),
# 	("0p35", "1e3"):	(0.1658,0.1727),
# 	("2", "1e-5"):	(0.1242,0.1204),
# 	("2", "1e0"):	(0.1103,0.1102),
# 	("2", "1e1"):	(0.1966,0.1947),
# 	("2", "1e2"):	(0.2385,0.2411),
# 	("2", "1e3"):	(0.2500,0.2537),
# 	("12", "1e-5"):	(0.1545,0.1464),
# 	("12", "1e0"):	(0.0947,0.0993),
# 	("12", "1e1"):	(0.2383,0.2383),
# 	("12", "1e2"):	(0.4508,0.4508),
# 	("12", "1e3"):	(0.4238,0.4225),
# 	("30", "1e-5"):	(0.1140,0.1096),
# 	("30", "1e0"):	(0.1188,0.1256),
# 	("30", "1e1"):	(0.2879,0.2875),
# 	("30", "1e2"):	(0.5293,0.5298),
# 	("30", "1e3"):	(0.4829,0.4829),
# 	("60", "1e-5"):	(0.2478,0.3927),
# 	("60", "1e0"):	(0.1221,0.1321),
# 	("60", "1e1"):	(0.2515,0.2503),
# 	("60", "1e2"):	(0.5688,0.5688),
# 	("60", "1e3"):	(0.5137,0.5135),
# }
# syst_unc["_DSA"] = {
# 	("0p35", "1e-5"):	(0.2715,0.3167),
# 	("0p35", "1e0"):	(0.1776,0.2279),
# 	("0p35", "1e1"):	(0.1655,0.2052),
# 	("0p35", "1e2"):	(0.1827,0.2082),
# 	("0p35", "1e3"):	(0.1755,0.1961),
# 	("2", "1e-5"):	(0.2005,0.2846),
# 	("2", "1e0"):	(0.2545,0.3742),
# 	("2", "1e1"):	(0.1784,0.2305),
# 	("2", "1e2"):	(0.1962,0.2264),
# 	("2", "1e3"):	(0.2393,0.2554),
# 	("12", "1e-5"):	(0.2461,0.3055),
# 	("12", "1e0"):	(0.2237,0.2608),
# 	("12", "1e1"):	(0.1754,0.2294),
# 	("12", "1e2"):	(0.1645,0.2110),
# 	("12", "1e3"):	(0.3249,0.3809),
# 	("30", "1e-5"):	(0.2375,0.2736),
# 	("30", "1e0"):	(0.1899,0.2352),
# 	("30", "1e1"):	(0.1554,0.2148),
# 	("30", "1e2"):	(0.1529,0.2044),
# 	("30", "1e3"):	(0.3100,0.3760),
# 	("60", "1e-5"):	(0.4219,0.3957),
# 	("60", "1e0"):	(0.3976,0.3592),
# 	("60", "1e1"):	(0.2275,0.3027),
# 	("60", "1e2"):	(0.1555,0.2079),
# 	("60", "1e3"):	(0.2794,0.3566),
# }

## datacards_years_combined_noDimuonSFs_SR_ANv6
# syst_unc["_Pat"] = {
# 	("0p35", "1e-5"):	(0.1011,0.1012),
# 	("0p35", "1e0"):	(0.6642,0.6642),
# 	("0p35", "1e1"):	(0.7798,0.7800),
# 	("0p35", "1e2"):	(0.7948,0.7946),
# 	("0p35", "1e3"):	(0.7422,0.7426),
# 	("2", "1e-5"):	(0.1410,0.1284),
# 	("2", "1e0"):	(0.3165,0.3167),
# 	("2", "1e1"):	(0.7719,0.7721),
# 	("2", "1e2"):	(0.8631,0.8631),
# 	("2", "1e3"):	(0.8706,0.8704),
# 	("12", "1e-5"):	(0.1054,0.0837),
# 	("12", "1e0"):	(0.0972,0.0970),
# 	("12", "1e1"):	(0.5880,0.5877),
# 	("12", "1e2"):	(0.9077,0.9077),
# 	("12", "1e3"):	(0.9086,0.9085),
# 	("30", "1e-5"):	(0.1411,0.1333),
# 	("30", "1e0"):	(0.0926,0.0900),
# 	("30", "1e1"):	(0.3912,0.3909),
# 	("30", "1e2"):	(0.7847,0.7848),
# 	("30", "1e3"):	(0.8981,0.8981),
# 	("60", "1e-5"):	(0.1301,0.1113),
# 	("60", "1e0"):	(0.0917,0.0934),
# 	("60", "1e1"):	(0.3092,0.3092),
# 	("60", "1e2"):	(0.6967,0.6967),
# 	("60", "1e3"):	(0.8434,0.8434),
# }
# syst_unc["_PatDSA"] = {
# 	("0p35", "1e-5"):	(0.1001,0.1027),
# 	("0p35", "1e0"):	(0.1078,0.1002),
# 	("0p35", "1e1"):	(0.1778,0.1836),
# 	("0p35", "1e2"):	(0.2097,0.2077),
# 	("0p35", "1e3"):	(0.1557,0.1605),
# 	("2", "1e-5"):	(0.0992,0.0924),
# 	("2", "1e0"):	(0.0920,0.0971),
# 	("2", "1e1"):	(0.1837,0.1837),
# 	("2", "1e2"):	(0.2298,0.2347),
# 	("2", "1e3"):	(0.2426,0.2462),
# 	("12", "1e-5"):	(0.1215,0.1330),
# 	("12", "1e0"):	(0.0958,0.1062),
# 	("12", "1e1"):	(0.2278,0.2289),
# 	("12", "1e2"):	(0.4461,0.4460),
# 	("12", "1e3"):	(0.4154,0.4144),
# 	("30", "1e-5"):	(0.0982,0.0924),
# 	("30", "1e0"):	(0.0888,0.0841),
# 	("30", "1e1"):	(0.2806,0.2812),
# 	("30", "1e2"):	(0.5242,0.5243),
# 	("30", "1e3"):	(0.4717,0.4717),
# 	("60", "1e-5"):	(0.2908,0.4517),
# 	("60", "1e0"):	(0.1269,0.1439),
# 	("60", "1e1"):	(0.2337,0.2311),
# 	("60", "1e2"):	(0.5637,0.5636),
# 	("60", "1e3"):	(0.5025,0.5027),
# }
# syst_unc["_DSA"] = {
# 	("0p35", "1e-5"):	(0.2199,0.2519),
# 	("0p35", "1e0"):	(0.0818,0.0738),
# 	("0p35", "1e1"):	(0.0993,0.0989),
# 	("0p35", "1e2"):	(0.1406,0.1440),
# 	("0p35", "1e3"):	(0.1291,0.1292),
# 	("2", "1e-5"):	(0.0855,0.0924),
# 	("2", "1e0"):	(0.1220,0.1263),
# 	("2", "1e1"):	(0.0848,0.0790),
# 	("2", "1e2"):	(0.1435,0.1430),
# 	("2", "1e3"):	(0.2091,0.2090),
# 	("12", "1e-5"):	(0.1955,0.2399),
# 	("12", "1e0"):	(0.0875,0.0826),
# 	("12", "1e1"):	(0.0826,0.0725),
# 	("12", "1e2"):	(0.0915,0.0920),
# 	("12", "1e3"):	(0.2465,0.2465),
# 	("30", "1e-5"):	(0.3203,0.3879),
# 	("30", "1e0"):	(0.1418,0.1522),
# 	("30", "1e1"):	(0.0699,0.0651),
# 	("30", "1e2"):	(0.0683,0.0693),
# 	("30", "1e3"):	(0.2364,0.2358),
# 	("60", "1e-5"):	(0.3583,0.3208),
# 	("60", "1e0"):	(0.3226,0.2119),
# 	("60", "1e1"):	(0.1494,0.1478),
# 	("60", "1e2"):	(0.0712,0.0732),
# 	("60", "1e3"):	(0.1916,0.1922),
# }

def getConfig(path):
  if (".py" in path):
    path = path[:-3]
  config = importlib.import_module(path)
  return config

def print_region_a_limits(config, hist):
    x_cut = hist.GetXaxis().GetBinLowEdge(config.abcd_point[0])
    y_cut = hist.GetYaxis().GetBinLowEdge(config.abcd_point[1])
    info(f"Region A limits for points ({config.abcd_point[0]},{config.abcd_point[1]}):")
    x_variable = config.variable_2
    y_variable = config.variable_1
    if config.signal_bin == "B" or config.signal_bin == "D":
        y_variable = f"- {y_variable}"
    if config.signal_bin == "C" or config.signal_bin == "D":
        x_variable = f"- {x_variable}"
    info(f"  {x_variable} < {x_cut}")
    info(f"  {y_variable} ≥ {y_cut}")
    x_req = "<"
    y_req = "≥"
    if "-" in x_variable:
        x_variable = x_variable.replace("- ", "")
        x_req = ">"
        x_cut = x_cut*(-1)
    if "-" in y_variable:
        y_variable = y_variable.replace("- ", "")
        y_req = " ≤"
        y_cut = y_cut*(-1)
    info(f"  {x_variable} {x_req} {x_cut:.3f}")
    info(f"  {y_variable} {y_req} {y_cut:.3f}")
    if "log" in x_variable:
        x_variable = x_variable.replace("log", "")
        x_cut = 10 ** x_cut
    if "log" in y_variable:
        y_variable = y_variable.replace("log", "")
        y_cut = 10 ** y_cut
    info(f"  {x_variable} {x_req} {x_cut:.3f}")
    info(f"  {y_variable} {y_req} {y_cut:.3f}")

def format_value_unc(val, unc, syst_up=None, syst_down=None):
    if unc <= 0:
        return f"{val:.2f} ± 0"

    exponent = math.floor(math.log10(abs(unc)))
    unc_rounded = round(unc, -exponent)
    
    nd = max(0, -int(math.floor(math.log10(abs(unc_rounded)))))
    # nd = max(0, -exponent)
    # unc_rounded = round(unc, nd)
    val_rounded = round(val, nd)
    if val_rounded == 0 and val != 0:
        nd += 1
        val_rounded = round(val, nd)
        unc_rounded = round(unc, nd)
    
    if syst_up is not None and syst_down is not None:
        nd_syst = nd
        while (
            round(syst_up, nd_syst) == 0
            or round(syst_down, nd_syst) == 0
        ) and nd_syst < 10:
            nd_syst += 1
        syst_up_rounded = round(syst_up, nd_syst)
        syst_down_rounded = round(syst_down, nd_syst)
        return f"{val_rounded:.{nd}f} #pm{unc_rounded:.{nd}f} (stat) ^{{+{syst_up_rounded:.{nd_syst}f}}}_{{-{syst_down_rounded:.{nd_syst}f}}} (syst)"
    
    return f"{val_rounded:.{nd}f} #pm {unc_rounded:.{nd}f}"

def format_value_unc_latex(val, unc, syst_up=None, syst_down=None):
    if unc <= 0:
        return f"{val:.2f} ± 0"

    exponent = math.floor(math.log10(abs(unc)))
    unc_rounded = round(unc, -exponent)
    # if syst_up is not None and syst_down is not None:
    #     syst_up_rounded = round(syst_up, -exponent)
    #     syst_down_rounded = round(syst_down, -exponent)
    nd = max(0, -int(math.floor(math.log10(abs(unc_rounded)))))
    # nd = max(0, -exponent)
    # unc_rounded = round(unc, nd)
    val_rounded = round(val, nd)
    if val_rounded == 0 and val != 0:
        nd += 1
        val_rounded = round(val, nd)
        unc_rounded = round(unc, nd)
    
    if syst_up is not None and syst_down is not None:
        nd_syst = nd
        while (
            round(syst_up, nd_syst) == 0
            or round(syst_down, nd_syst) == 0
        ) and nd_syst < 10:
            nd_syst += 1
        syst_up_rounded = round(syst_up, nd_syst)
        syst_down_rounded = round(syst_down, nd_syst)
    
        return f"{val_rounded:.{nd}f} $\pm$ {unc_rounded:.{nd}f} (stat) $^{{+{syst_up_rounded:.{nd_syst}f}}}_{{-{syst_down_rounded:.{nd_syst}f}}}$ (syst)"
    
    return f"{val_rounded:.{nd}f} $\pm$ {unc_rounded:.{nd}f}"

def extract_mass(s):
    m = re.search(r"mAlp-([0-9]+(?:p[0-9]+)?)(?=GeV)", s)
    if not m:
        return None
    mass_str = m.group(1)
    return float(mass_str.replace("p", "."))

ctaus_dict = {
    "1e-5": "1 nm",
    "1e0": "1 mm",
    "1e1": "1 cm",
    "1e2": "10 cm",
    "1e3": "1 m",
}

def main():

    config = getConfig(args.config)
    config.normalize_signal = True

    abcdPlotter = ABCDPlotter(config, args)
    abcdHelper = ABCDHelper(config, args)

    output_path = f"../plots/n_events_test/{config.do_region}_{config.year}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    bkg_a, bkg_b, bkg_c, bkg_d, _, _, _, _ = abcdHelper.get_abcd(abcdPlotter.background_hist, config.abcd_point)
    prediction, prediction_err = abcdHelper.get_prediction(bkg_b, bkg_c, bkg_d, bkg_b**0.5, bkg_c**0.5, bkg_d**0.5)

    signal_yields = {}
    signal_yields_tot = {}
    signal_yields_unc2 = {}
    signal_yields_tot_unc2 = {}
    all_years = config.years
    for year in all_years:
        config.years = [year,]
        abcdPlotter = ABCDPlotter(config, args)
        abcdHelper = ABCDHelper(config, args)

        for mass in config.masses:
            for ctau in config.ctaus:
                scale = abcdPlotter.signal_scales[(mass,ctau,year)]
                signal = abcdPlotter.signal_hists[(mass, ctau)]
                a, b, c, d, _, _, _, _ = abcdHelper.get_abcd(signal, config.abcd_point)
                if (mass, ctau) not in signal_yields:
                    signal_yields[(mass,ctau)] = 0
                    signal_yields_tot[(mass,ctau)] = 0
                    signal_yields_unc2[(mass,ctau)] = 0
                    signal_yields_tot_unc2[(mass,ctau)] = 0
                signal_yields[(mass,ctau)] += a * scale
                signal_yields_tot[(mass,ctau)] += (a+b+c+d) * scale
                signal_yields_unc2[(mass,ctau)] += (a**0.5 * scale) ** 2
                signal_yields_tot_unc2[(mass,ctau)] += ((a+b+c+d)**0.5 * scale) ** 2
                # info(f"{mass}, {ctau}, {year}: {signal.GetEntries()}, {a}, {scale}, {a * scale:.3f} +/- {a**0.5 * scale:.3f}")
    
    h2 = ROOT.TH2D("n_signal_events", ";m_{a} [GeV];c#tau_{a}",
               len(config.masses), 0, len(config.masses),
               len(config.ctaus), 0, len(config.ctaus))
    h2_tot = ROOT.TH2D("n_signal_events_tot", ";m_{a} [GeV];c#tau_{a}",
               len(config.masses), 0, len(config.masses),
               len(config.ctaus), 0, len(config.ctaus))
    h2_eff = ROOT.TH2D("n_signal_events_eff", ";m_{a} [GeV];c#tau_{a}",
               len(config.masses), 0, len(config.masses),
               len(config.ctaus), 0, len(config.ctaus))
    h2_sig = ROOT.TH2D("signal_significance", ";m_{a} [GeV];c#tau_{a}",
               len(config.masses), 0, len(config.masses),
               len(config.ctaus), 0, len(config.ctaus))
    title = ""
    if config.category == "_Pat":
        title = "PAT-PAT"
    if config.category == "_PatDSA":
        title = "PAT-DSA"
    if config.category == "_DSA":
        title = "DSA-DSA"
    h2.SetTitle(title)
    h2_tot.SetTitle(title)
    h2_eff.SetTitle(title)
    h2_sig.SetTitle(title)
    for i, m in enumerate(config.masses):
        mass = float(m.replace("p", "."))
        h2.GetXaxis().SetBinLabel(i+1, str(mass))
        h2_tot.GetXaxis().SetBinLabel(i+1, str(mass))
        h2_eff.GetXaxis().SetBinLabel(i+1, str(mass))
        h2_sig.GetXaxis().SetBinLabel(i+1, str(mass))
    for j, c in enumerate(config.ctaus):
        ctau = ctaus_dict[c]
        h2.GetYaxis().SetBinLabel(j+1, str(ctau))
        h2_tot.GetYaxis().SetBinLabel(j+1, str(ctau))
        h2_eff.GetYaxis().SetBinLabel(j+1, str(ctau))
        h2_sig.GetYaxis().SetBinLabel(j+1, str(ctau))
    for mass in config.masses:
        for ctau in config.ctaus:
            ix = config.masses.index(mass) + 1
            iy = config.ctaus.index(ctau) + 1
            h2.SetBinContent(ix, iy, signal_yields[(mass,ctau)])
            h2.SetBinError(ix, iy, signal_yields_unc2[(mass,ctau)]**0.5)
            h2_tot.SetBinContent(ix, iy, signal_yields_tot[(mass,ctau)])
            h2_tot.SetBinError(ix, iy, signal_yields_tot_unc2[(mass,ctau)]**0.5)
            h2_eff.SetBinContent(ix, iy, signal_yields[(mass,ctau)] / signal_yields_tot[(mass,ctau)] if signal_yields_tot[(mass,ctau)] > 0 else 0)
            h2_eff.SetBinError(ix, iy, 0)  # ignoring uncertainty on efficiency for now
            h2_sig.SetBinContent(ix, iy, signal_yields[(mass,ctau)] / math.sqrt(prediction) if prediction > 0 else 0)
            h2_sig.SetBinError(ix, iy, signal_yields[(mass,ctau)] / math.sqrt(prediction) * math.sqrt((signal_yields_unc2[(mass,ctau)] / signal_yields[(mass,ctau)]**2) + (0.5 * prediction_err / prediction)**2) if signal_yields[(mass,ctau)] > 0 and prediction > 0 else 0)
            info(f"{mass}, {ctau}: {signal_yields[(mass,ctau)]:.4f} +/- {signal_yields_unc2[(mass,ctau)] ** 0.5:.4f}")
            # info(f"\tTotal: {signal_yields_tot[(mass,ctau)]:.4f} +/- {signal_yields_tot_unc2[(mass,ctau)] ** 0.5:.4f}")

    print_region_a_limits(config, signal)

    h2.SaveAs(f"../signal_lxy_uncertainty/input_root_files/n_signal_events{config.category}_{config.year}_{config.do_region}.root")

    ROOT.gStyle.SetOptStat(0)
    # ROOT.gStyle.SetPaintTextFormat(".3f")

    c1 = ROOT.TCanvas("c1", "c1", 900, 600)
    c1.SetBottomMargin(0.15)

    # h2.Draw("COLZ TEXT")
    h2.SetTitle("")
    h2.Draw("COLZ")
    h2.GetXaxis().SetLabelSize(0.065)
    h2.GetYaxis().SetLabelSize(0.065)
    h2.GetZaxis().SetLabelSize(0.045)
    h2.GetZaxis().SetTitle("Number of events")
    h2.GetZaxis().SetTitleOffset(1.1)
    h2.GetYaxis().SetTitleOffset(1.2)
    h2.GetXaxis().SetTitleOffset(1.1)
    h2.GetXaxis().SetTitleSize(0.05)
    h2.GetYaxis().SetTitleSize(0.05)
    h2.GetZaxis().SetTitleSize(0.05)
    if z_max is not None:
        print(f"------- z_max: {z_max[config.category]} -------")
        h2.GetZaxis().SetRangeUser(0, z_max[config.category])

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)
    latex.SetTextSize(0.038)
    latex.SetTextFont(42)

    txts = {}
    for ix in range(1, h2.GetNbinsX()+1):
        # info(f"{config.masses[ix-1]}", end="")
        for iy in range(1, h2.GetNbinsY()+1):
            val = h2.GetBinContent(ix, iy)
            unc = h2.GetBinError(ix, iy)
            if val == 0:
                continue
            if syst_unc[config.category] is not None:
                syst = syst_unc[config.category][(config.masses[ix-1], config.ctaus[iy-1])]
                syst_up = val * syst[0]
                syst_down = val * syst[1]
                txt = format_value_unc(val, unc, syst_up, syst_down)
                txt_latex = format_value_unc_latex(val, unc, syst_up, syst_down)
            else:
                txt = format_value_unc(val, unc)
                txt_latex = format_value_unc_latex(val, unc)

            txts[(config.masses[ix-1], config.ctaus[iy-1])] = txt_latex

            x = h2.GetXaxis().GetBinCenter(ix)
            y = h2.GetYaxis().GetBinCenter(iy)
            latex.DrawLatex(x, y, txt)
    
    ctau_strs = {
        "1e-5": "1\\unit{nm}",
        "1e0": "1\\mm",
        "1e1": "1\\cm",
        "1e2": "10\\cm",
        "1e3": "1\\unit{m}",
    }

    # for ctau in config.ctaus:
    #     ctau_str = ctau_strs[ctau]
    #     info(f"\\multirow{2}{{*}}{{{ctau_str}}}", end="")
    #     # info(f" ", end="")
    #     for mass in config.masses:
    #         info(f" & {txts[(mass, ctau)]}", end="")
    #     info(" \\\\")
    #     # info(" \\\\ \\hline")

    tex = ROOT.TLatex(0.12, 0.92, "#bf{CMS}#it{ Simulation Work in Progress}")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.042)
    tex.SetLineWidth(2)
    tex.DrawClone()

    lumi_text = ""
    lumi_text_xmin = 0.68
    if config.luminosity_sum_run2 != 0 and config.luminosity_sum_run3 == 0:
      lumi_text = f"#scale[0.8]{{{config.luminosity_sum_run2/1000:.0f} fb^{{-1}} (13 TeV)}}"
    elif config.luminosity_sum_run2 == 0 and config.luminosity_sum_run3 != 0:
      lumi_text = f"#scale[0.8]{{{config.luminosity_sum_run3/1000:.0f} fb^{{-1}} (13.6 TeV)}}"
    else:
      lumi_text = f"#scale[0.8]{{{config.luminosity_sum_run2/1000:.0f} fb^{{-1}} (13 TeV), {config.luminosity_sum_run3/1000:.0f} fb^{{-1}} (13.6 TeV)}}"
      lumi_text_xmin = 0.52
    
    tex = ROOT.TLatex(lumi_text_xmin, 0.92, lumi_text)
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.042)
    tex.SetLineWidth(2)
    tex.DrawClone()

    c1.SetRightMargin(0.16)
    c1.SetLeftMargin(0.12)
    c1.SaveAs(f"{output_path}/n_signal_events{config.category}_{config.year}.pdf")

    c2 = ROOT.TCanvas("c2", "c2", 800, 600)
    # h2_tot.Draw("COLZ TEXT")
    h2_tot.Draw("COLZ")
    h2_tot.GetXaxis().SetLabelSize(0.04)
    h2_tot.GetYaxis().SetLabelSize(0.04)
    h2_tot.GetZaxis().SetTitle("Number of events")

    for ix in range(1, h2_tot.GetNbinsX()+1):
        for iy in range(1, h2_tot.GetNbinsY()+1):
            val = h2_tot.GetBinContent(ix, iy)
            unc = h2_tot.GetBinError(ix, iy)
            txt = format_value_unc(val, unc)
            x = h2_tot.GetXaxis().GetBinCenter(ix)
            y = h2_tot.GetYaxis().GetBinCenter(iy)
            latex.DrawLatex(x, y, txt)

    c2.SetRightMargin(0.15)
    c2.SaveAs(f"{output_path}/n_signal_events_tot{config.category}_{config.year}.pdf")

    c3 = ROOT.TCanvas("c3", "c3", 800, 600)
    h2_eff.Draw("COLZ")
    h2_eff.GetXaxis().SetLabelSize(0.04)
    h2_eff.GetYaxis().SetLabelSize(0.04)
    h2_eff.GetZaxis().SetTitle("Selection efficiency")
    h2_eff.GetZaxis().SetRangeUser(0,1)
    for ix in range(1, h2_eff.GetNbinsX()+1):
        for iy in range(1, h2_eff.GetNbinsY()+1):
            val = h2_eff.GetBinContent(ix, iy)
            txt = f"{val:.2f}"
            x = h2_eff.GetXaxis().GetBinCenter(ix)
            y = h2_eff.GetYaxis().GetBinCenter(iy)
            latex.DrawLatex(x, y, txt)
    c3.SetRightMargin(0.15)
    c3.SaveAs(f"{output_path}/n_signal_events_eff{config.category}_{config.year}.pdf")

    c4 = ROOT.TCanvas("c4", "c4", 800, 600)
    # h2.Draw("COLZ TEXT")
    h2_sig.Draw("COLZ")
    h2_sig.GetXaxis().SetLabelSize(0.04)
    h2_sig.GetYaxis().SetLabelSize(0.04)
    h2_sig.GetZaxis().SetTitle("Signal significance (S/sqrt(B))")
    h2_sig.GetZaxis().SetRangeUser(0,1)

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)
    latex.SetTextSize(0.025)
    latex.SetTextFont(42)

    for ix in range(1, h2_sig.GetNbinsX()+1):
        for iy in range(1, h2_sig.GetNbinsY()+1):
            val = h2_sig.GetBinContent(ix, iy)
            # print(f"Significance for mass {config.masses[ix-1]} and ctau {config.ctaus[iy-1]}: {val:.7f}")
            unc = h2_sig.GetBinError(ix, iy)
            if val == 0:
                continue
            txt = format_value_unc(val, unc)
            x = h2_sig.GetXaxis().GetBinCenter(ix)
            y = h2_sig.GetYaxis().GetBinCenter(iy)
            latex.DrawLatex(x, y, txt)
    
    c4.SetRightMargin(0.15)
    c4.SaveAs(f"{output_path}/signal_significance{config.category}_{config.year}.pdf")

    info(f"Background: ")
    info(f"True background in A: {bkg_a:.2f} +/- {bkg_a**0.5:.2f}")
    info(f"True background in B: {bkg_b:.2f} +/- {bkg_b**0.5:.2f}")
    info(f"True background in C: {bkg_c:.2f} +/- {bkg_c**0.5:.2f}")
    info(f"True background in D: {bkg_d:.2f} +/- {bkg_d**0.5:.2f}")
    info(f"Predicted background in A: {prediction:.2f} +/- {prediction_err:.2f}")

if __name__ == '__main__':
  main()
