import ROOT
import math
from ABCDPlotter import ABCDPlotter
from ABCDHelper import ABCDHelper
import importlib
import argparse
from Logger import info

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="", help="Path to the config file.")
args = parser.parse_args()


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

def format_value_unc(val, unc):
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
    return f"{val_rounded:.{nd}f} #pm {unc_rounded:.{nd}f}"

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

    bkg_a, bkg_b, bkg_c, bkg_d, _, _, _, _ = abcdHelper.get_abcd(abcdPlotter.background_hist, config.abcd_point)
    prediction, prediction_err = abcdHelper.get_prediction(bkg_b, bkg_c, bkg_d, bkg_b**0.5, bkg_c**0.5, bkg_d**0.5)

    signal_yields = {}
    signal_yields_unc2 = {}
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
                    signal_yields_unc2[(mass,ctau)] = 0
                signal_yields[(mass,ctau)] += a * scale
                signal_yields_unc2[(mass,ctau)] += (a**0.5 * scale) ** 2
                info(f"{mass}, {ctau}, {year}: {a * scale:.3f} +/- {a**0.5 * scale:.3f}")
    
    h2 = ROOT.TH2D("n_signal_events", ";m_{a} [GeV];c#tau_{a} [mm]",
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
    for i, m in enumerate(config.masses):
        mass = float(m.replace("p", "."))
        h2.GetXaxis().SetBinLabel(i+1, str(mass))
    for j, c in enumerate(config.ctaus):
        ctau = ctaus_dict[c]
        h2.GetYaxis().SetBinLabel(j+1, str(ctau))
    for mass in config.masses:
        for ctau in config.ctaus:
            ix = config.masses.index(mass) + 1
            iy = config.ctaus.index(ctau) + 1
            h2.SetBinContent(ix, iy, signal_yields[(mass,ctau)])
            h2.SetBinError(ix, iy, signal_yields_unc2[(mass,ctau)]**0.5)
            info(f"{mass}, {ctau}: {signal_yields[(mass,ctau)]:.4f} +/- {signal_yields_unc2[(mass,ctau)] ** 0.5:.4f}")
    
    print_region_a_limits(config, signal)

    ROOT.gStyle.SetOptStat(0)
    # ROOT.gStyle.SetPaintTextFormat(".3f")

    c1 = ROOT.TCanvas("c1", "c1", 800, 600)
    # h2.Draw("COLZ TEXT")
    h2.Draw("COLZ")
    h2.GetXaxis().SetLabelSize(0.04)
    h2.GetYaxis().SetLabelSize(0.04)
    h2.GetZaxis().SetTitle("Number of events")

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)
    latex.SetTextSize(0.025)
    latex.SetTextFont(42)

    for ix in range(1, h2.GetNbinsX()+1):
        for iy in range(1, h2.GetNbinsY()+1):
            val = h2.GetBinContent(ix, iy)
            unc = h2.GetBinError(ix, iy)
            txt = format_value_unc(val, unc)
            x = h2.GetXaxis().GetBinCenter(ix)
            y = h2.GetYaxis().GetBinCenter(iy)
            latex.DrawLatex(x, y, txt)
    
    c1.SetRightMargin(0.15)
    c1.SaveAs(f"../plots/n_events/n_signal_events{config.category}_{config.year}.pdf")

    info(f"Background: ")
    info(f"True background in A: {bkg_a:.2f} +/- {bkg_a**0.5:.2f}")
    info(f"True background in B: {bkg_b:.2f} +/- {bkg_b**0.5:.2f}")
    info(f"True background in C: {bkg_c:.2f} +/- {bkg_c**0.5:.2f}")
    info(f"True background in D: {bkg_d:.2f} +/- {bkg_d**0.5:.2f}")
    info(f"Predicted background in A: {prediction:.2f} +/- {prediction_err:.2f}")

if __name__ == '__main__':
  main()
