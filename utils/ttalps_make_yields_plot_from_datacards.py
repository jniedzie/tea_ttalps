import ROOT
import math
from ABCDPlotter import ABCDPlotter
from ABCDHelper import ABCDHelper
from Styler import Styler
import importlib
import argparse
from Logger import info, error

import os

# parser = argparse.ArgumentParser()
# parser.add_argument("--config", type=str, default="", help="Path to the config file.")
# parser.add_argument("--theory", type=bool, default=False, help="Whether to use theory cross sections.")
# args = parser.parse_args()

# def getConfig(path):
#   if (".py" in path):
#     path = path[:-3]
#   config = importlib.import_module(path)
#   return config

y_min = 5e-4
y_max = 1e5
line_max = 1e3
category_y = 4e2

limits_path = "../limits/limits_2016preVFP2016postVFP201720182022preEE2022postEE2023preBPix2023postBPix"
datacard_path = "datacards_years_combined_dxydzIso_SR_ANv5"
input_path = f"{limits_path}/{datacard_path}"
card_pattern = "combined_datacard_{}_{}{}.txt"

output_path = f"../plots/yields_datacard/{datacard_path}"

signals = [
    ("12","1e1"),
    ("12","1e3"),
]

def main():

    # config = getConfig(args.config)
    # config.normalize_signal = False

    if not os.path.exists(input_path):
        error(f"Input path {input_path} does not exist!")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    categories = ["_Pat", "_PatDSA", "_DSA"]

    bkg_a = {}
    bkg_b = {}
    bkg_c = {}
    bkg_d = {}
    prediction = {}

    observation = {}
    stat_err_bck = {}
    abcd_err_bkg = {}

    signal_rates = {}
    stat_err_signal = {}
    bkg_rates = {}

    for category in categories:
        # config.category = category
        # config.variable_1 = config.optimal_parameters[(category, config.do_region)][0]
        # config.variable_2 = config.optimal_parameters[(category, config.do_region)][1]
        # config.abcd_point = config.optimal_parameters[(category, config.do_region)][2]
        # config.signal_bin = config.optimal_parameters[(category, config.do_region)][3]

        # abcdPlotter = ABCDPlotter(config, args)
        # abcdHelper = ABCDHelper(config, args)

        signal_rates[category] = {}
        stat_err_signal[category] = {}

        for signal in signals:
            mass = signal[0]
            ctau = signal[1]
            datacard = input_path + "/" + card_pattern.format(mass, ctau, category)

            with open(datacard, "r") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith("observation"):
                        if category in observation:
                            continue
                        parts = stripped.split()
                        if len(parts) >= 2:
                            observation[category] = int(parts[1])
                        continue
                    if stripped.startswith("stat_err_bck"):
                        if category in stat_err_bck:
                            continue
                        parts = stripped.split()
                        if len(parts) >= 3:
                            stat_err_bck[category] = float(parts[-1])-1
                        continue
                    if stripped.startswith("CMS_EXO25022_abcd"):
                        if category in abcd_err_bkg:
                            continue
                        parts = stripped.split()
                        if len(parts) >= 3:
                            abcd_err_bkg[category] = float(parts[-1])-1
                        continue
                        
                    if stripped.startswith("rate"):
                        parts = stripped.split()
                        if len(parts) >= 3:
                            signal_rates[category][(mass,ctau)] = float(parts[1])
                            if category in bkg_rates:
                                continue
                            bkg_rates[category] = float(parts[2])
                        continue
                    if stripped.startswith("stat_err_signal"):
                        parts = stripped.split()
                        if len(parts) >= 3:
                            stat_err_signal[category][(mass,ctau)] = float(parts[2])-1.
                        continue
                    
                        

        # bkg_a_, bkg_b_, bkg_c_, bkg_d_, _, _, _, _ = abcdHelper.get_abcd(abcdPlotter.background_hist, config.abcd_point)
        # prediction_, prediction_err_ = abcdHelper.get_prediction(bkg_b_, bkg_c_, bkg_d_, bkg_b_**0.5, bkg_c_**0.5, bkg_d_**0.5)

        # bkg_a[category] = bkg_a_
        # bkg_b[category] = bkg_b_
        # bkg_c[category] = bkg_c_
        # bkg_d[category] = bkg_d_

        # prediction[category] = (prediction_, prediction_err_)

        # signal_yields_a[category] = {}
        # signal_yields_b[category] = {}
        # signal_yields_c[category] = {}
        # signal_yields_d[category] = {}    
        # all_years = config.years
        # for year in all_years:
        #     config.years = [year,]
        #     abcdPlotter = ABCDPlotter(config, args)
        #     abcdHelper = ABCDHelper(config, args)

        #     for mass in config.masses:
        #         for ctau in config.ctaus:
        #             scale = abcdPlotter.signal_scales[(mass,ctau,year)]
        #             signal = abcdPlotter.signal_hists[(mass, ctau)]
        #             a, b, c, d, _, _, _, _ = abcdHelper.get_abcd(signal, config.abcd_point)
        #             if (mass, ctau) not in signal_yields_a:
        #                 signal_yields_a[category][(mass,ctau)] = [0,0]
        #                 signal_yields_b[category][(mass,ctau)] = [0,0]
        #                 signal_yields_c[category][(mass,ctau)] = [0,0]
        #                 signal_yields_d[category][(mass,ctau)] = [0,0]
        #             signal_yields_a[category][(mass,ctau)][0] += a * scale
        #             signal_yields_a[category][(mass,ctau)][1] += (a**0.5 * scale) ** 2
        #             signal_yields_b[category][(mass,ctau)][0] += b * scale
        #             signal_yields_b[category][(mass,ctau)][1] += (b**0.5 * scale) ** 2
        #             signal_yields_c[category][(mass,ctau)][0] += c * scale
        #             signal_yields_c[category][(mass,ctau)][1] += (c**0.5 * scale) ** 2
        #             signal_yields_d[category][(mass,ctau)][0] += d * scale
        #             signal_yields_d[category][(mass,ctau)][1] += (d**0.5 * scale) ** 2


    # styler = Styler()

    n_bins_base = 1 
    
    n_categories = len(categories)
    n_bins = n_bins_base * n_categories

    signal = signals[0]
    signal2 = signals[1]

    category_strs = {
        "_Pat": "TMS-TMS",
        "_PatDSA": "TMS-STA",
        "_DSA": "STA-STA",
    }

    h_bkg = ROOT.TH1D("h_grouped_bkg", "",
                      n_bins, 0.5, n_bins + 0.5)
    h_obs = ROOT.TH1D("h_grouped_pred", "",
                      3, 0.5, 3 + 0.5)
    h_sig = ROOT.TH1D("h_grouped_sig", "",
                      n_bins, 0.5, n_bins + 0.5)
    h_sig2 = ROOT.TH1D("h_grouped_sig2", "",
                      n_bins, 0.5, n_bins + 0.5)

    for i, category in enumerate(categories):
        idx_base = n_bins_base * i + 1
        h_bkg.SetBinContent(idx_base, bkg_rates[category])
        h_bkg.SetBinError(idx_base, stat_err_bck[category]*bkg_rates[category] + abcd_err_bkg[category]*bkg_rates[category])

        h_sig.SetBinContent(idx_base, signal_rates[category][signal])
        h_sig.SetBinError(idx_base, stat_err_signal[category][signal]*signal_rates[category][signal])
        h_sig2.SetBinContent(idx_base, signal_rates[category][signal2])
        h_sig2.SetBinError(idx_base, stat_err_signal[category][signal2]*signal_rates[category][signal2])

        h_obs.SetBinContent(idx_base, observation[category])
        h_obs.SetBinError(idx_base, observation[category]**0.5)
        category_str = category_strs[category]
        h_bkg.GetXaxis().SetBinLabel(idx_base, category_str)
        

    h_bkg.SetFillColor(ROOT.kAzure+6)
    h_bkg.SetFillStyle(1001)
    h_bkg.SetLineColor(ROOT.kAzure+6)
    h_bkg.SetLineWidth(1)

    h_bkg.SetMinimum(y_min)
    h_bkg.SetMaximum(y_max)
    h_bkg.GetYaxis().SetTitle("Events")
    h_bkg.GetYaxis().SetTitleSize(0.05)
    h_bkg.GetXaxis().SetTitleSize(0.05)
    h_bkg.GetYaxis().SetNdivisions(210)
    
    h_bkg.GetXaxis().SetLabelSize(0)
    h_bkg.GetXaxis().SetLabelSize(0.07)
    h_bkg.GetYaxis().SetLabelSize(0.05)

    h_obs.SetFillStyle(0) 
    h_obs.SetLineColor(ROOT.kBlack)
    h_obs.SetLineWidth(2)
    h_obs.SetMarkerStyle(20)
    h_obs.SetMarkerSize(0.7)

    h_sig.SetFillStyle(0) 
    h_sig.SetLineColor(ROOT.kBlue)
    h_sig.SetLineWidth(2)
    h_sig.SetMarkerSize(0.0)
    h_sig.SetMarkerColor(ROOT.kBlue)
    h_sig2.SetFillStyle(0) 
    h_sig2.SetLineColor(ROOT.kGreen+2)
    h_sig2.SetLineWidth(2)
    # h_sig2.SetLineStyle(ROOT.kDashed)
    h_sig2.SetMarkerSize(0.0)
    h_sig2.SetMarkerColor(ROOT.kGreen+2)

    h_bkg_err = h_bkg.Clone()
    h_bkg_err.SetFillColorAlpha(ROOT.kBlack, 0.3)
    h_bkg_err.SetLineColor(ROOT.kBlack)
    h_bkg_err.SetFillStyle(3244)
    h_bkg_err.SetMarkerSize(0.0)

    h_sig_err = h_sig.Clone()
    h_sig_err.SetLineColor(ROOT.kBlue)
    h_sig_err.SetMarkerSize(0.0)
    h_sig_err.SetMarkerColor(ROOT.kBlue)
    h_sig2_err = h_sig2.Clone()
    h_sig2_err.SetLineColor(ROOT.kGreen+2)
    h_sig2_err.SetMarkerSize(0.0)
    h_sig2_err.SetMarkerColor(ROOT.kGreen+2)
    # h_sig2_err.SetLineStyle(ROOT.kDashed)

    c = ROOT.TCanvas("c_grouped_1d", "Grouped 4x3 1D", 800, 700)
    c.Divide(1, 2)
    c.GetPad(1).SetPad(0, 0.25, 1, 1)
    c.GetPad(1).SetLogy()
    c.GetPad(1).SetTickx(1)
    c.GetPad(1).SetTicky(1)
    c.GetPad(1).SetLeftMargin(0.14)
    c.GetPad(1).SetRightMargin(0.05)
    c.GetPad(1).SetBottomMargin(0.02)
    c.GetPad(2).SetPad(0, 0, 1, 0.25)
    c.GetPad(2).SetLeftMargin(0.14)
    c.GetPad(2).SetRightMargin(0.05)
    c.GetPad(2).SetTopMargin(0)
    # c.GetPad(2).SetBottomMargin(0.45)

    c.cd(1)
    ROOT.gStyle.SetOptStat(0)

    h_bkg.Draw("HIST")
    h_bkg_err.Draw("E2 SAME")
    h_sig.Draw("HIST ][ SAME")
    h_sig2.Draw("HIST ][ SAME")
    h_sig_err.Draw("E SAME")
    h_sig2_err.Draw("E SAME")
    h_obs.Draw("e same")

    # Legend (simple)
    leg = ROOT.TLegend(0.45, 0.60, 0.87, 0.86)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.04)
    leg.AddEntry(h_obs, "Data", "pe")
    leg.AddEntry(h_bkg, "Background", "f")
    leg.AddEntry(h_bkg_err, "Background stat. + syst. uncertainty", "f")
    leg.AddEntry(h_sig, "m_{a} = 12 GeV, c#tau_{a} = 1 cm", "l")
    leg.AddEntry(h_sig2, "m_{a} = 12 GeV, c#tau_{a} = 1 m", "l")
    leg.Draw()

    luminosity_run2 = 138
    luminosity_run3 = 62
    lumi_text = f"#scale[0.8]{{{luminosity_run2} fb^{{-1}} (13 TeV), {luminosity_run3:.0f} fb^{{-1}} (13.6 TeV)}}"
    tex = ROOT.TLatex(0.61, 0.92, lumi_text)
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.DrawClone()

    tex = ROOT.TLatex(0.14, 0.92, "#bf{CMS} #it{Preliminary}")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.DrawClone()

    line_pos_x = h_bkg.GetXaxis().GetBinLowEdge(5)
    line1 = ROOT.TLine(line_pos_x, y_min, line_pos_x, line_max)
    line1.SetLineColor(ROOT.kBlack)
    line1.SetLineWidth(2)
    line1.Draw()
    line_pos_x = h_bkg.GetXaxis().GetBinLowEdge(9)
    line2 = ROOT.TLine(line_pos_x, y_min, line_pos_x, line_max)
    line2.SetLineColor(ROOT.kBlack)
    line2.SetLineWidth(2)
    line2.Draw()

    tex_pos_x = h_bkg.GetXaxis().GetBinLowEdge(2)
    tex2 = ROOT.TLatex(tex_pos_x, category_y, "TMS-TMS")
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.045)
    tex2.DrawClone()
    tex_pos_x = h_bkg.GetXaxis().GetBinLowEdge(6)
    tex2 = ROOT.TLatex(tex_pos_x, category_y, "TMS-STA")
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.045)
    tex2.DrawClone()
    tex_pos_x = h_bkg.GetXaxis().GetBinLowEdge(10)
    tex2 = ROOT.TLatex(tex_pos_x, category_y, "STA-STA")
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.045)
    tex2.DrawClone()

    # for i in range(1, n_bins + 1):
    #     y = h_sig.GetBinContent(i)
    #     err = h_sig.GetBinError(i)
    #     if err > 0:
    #         x = h_sig.GetXaxis().GetBinCenter(i)
    #         print(f"y: {y}, err: {err}, x: {x}")
    #         L = ROOT.TLine(x, y - err, x, y + err)
    #         L.SetLineColor(ROOT.kBlue)
    #         L.SetLineWidth(2)
    #         L.Draw()
    
    ROOT.gErrorIgnoreLevel = ROOT.kError

    c.Update()

    c.cd(2)

    h_ratio = h_obs.Clone("ratio_obs_bkg")
    h_ratio.Add(h_bkg, -1)
    h_ratio.Divide(h_bkg)

    h_ratio.Draw("p e0")
    h_ratio.SetMinimum(-1.5)
    h_ratio.SetMaximum(1.5)
    h_ratio.GetYaxis().SetTitle("#frac{Data-Bkg.}{Bkg.}")
    h_ratio.GetYaxis().SetTitleSize(0.12)
    h_ratio.GetYaxis().SetLabelSize(0.15)
    h_ratio.GetYaxis().SetTitleOffset(0.40)
    h_ratio.GetYaxis().CenterTitle()
    h_ratio.GetYaxis().SetNdivisions(404)

    h_ratio.GetXaxis().SetBinLabel(1, "TMS-TMS")
    h_ratio.GetXaxis().SetBinLabel(2, "TMS-STA")
    h_ratio.GetXaxis().SetBinLabel(3, "STA-STA")
    h_ratio.GetXaxis().SetLabelOffset(0.02)
    h_ratio.GetXaxis().SetLabelFont(42)
    h_ratio.GetXaxis().SetLabelSize(0.20)
    # h_ratio.GetXaxis().SetTitle("Dimuon category")
    h_ratio.GetXaxis().SetTitleOffset(1.20)
    h_ratio.GetXaxis().SetTitleSize(0.16)

    h_bkg_ratio_err = h_bkg_err.Clone("bkg_err_ratio")
    for i in range(1, h_bkg_ratio_err.GetNbinsX() + 1):
        bkg = h_bkg.GetBinContent(i)
        err = h_bkg_err.GetBinError(i)
        rel_err = err / bkg
        err = h_bkg_err.GetBinError(i)
        h_bkg_ratio_err.SetBinContent(i, 0.0)
        h_bkg_ratio_err.SetBinError(i, rel_err)
    h_bkg_ratio_err.Draw("E2 SAME")

    # plot.SetTitle("" if is_ratio else hist.title)
    # plot.GetXaxis().SetLimits(hist.x_min, hist.x_max)
    # h_ratio.GetXaxis().SetTitle(hist.x_label)
    # plot.GetXaxis().SetTitleOffset(1.0 if is_ratio else 1.7)
    # plot.GetYaxis().SetTitleSize(self.labelFontSize)
    # plot.GetYaxis().SetTitleOffset(1.5)

    x_min = h_ratio.GetXaxis().GetBinLowEdge(1)
    x_max = h_ratio.GetXaxis().GetBinLowEdge(4)
    line = ROOT.TLine(x_min, 0, x_max, 0)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineStyle(ROOT.kDashed)

    line.Draw()

    c.Update()


    extra_str = ""
    c.SaveAs(f"{output_path}/SR_yields{extra_str}.pdf")

if __name__ == '__main__':
  main()
