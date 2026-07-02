import ROOT
import math
from ABCDPlotter import ABCDPlotter
from ABCDHelper import ABCDHelper
from Styler import Styler
import importlib
import argparse
from Logger import info

import os

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="", help="Path to the config file.")
parser.add_argument("--theory", type=bool, default=False, help="Whether to use theory cross sections.")
args = parser.parse_args()

def getConfig(path):
  if (".py" in path):
    path = path[:-3]
  config = importlib.import_module(path)
  return config

y_min = 5e-1
y_max = 2e4
line_max = 1e3
category_y = 4e2

plot_abcd = False

thesis = False

# Taken from datacard so it's fraction on the yield
bkg_syst_err = {
    # "_Pat": 0.0278658154454774,
    # "_PatDSA": 0.1944346951592415,
    # "_DSA": 0.1154641409840682,
    # "_Pat": 0.034420587797399,
    # "_PatDSA": 0.4113183182760651,
    # "_DSA": 0.342956618338063,
    "_Pat": 0.0326263547808,
    "_DSA": 0.342956618338063,
}
# Using simulation true A for now becasue I don't know what else to use
bkg_obs = {
    "_Pat": (80.68, 8.98),
    "_PatDSA": (46.8, 6.85),
    "_DSA": (8.12, 2.85),
}

cms_red = ROOT.TColor.GetColor("#bd1f01")
cms_purple = ROOT.TColor.GetColor("#832db6")
cms_blue = ROOT.TColor.GetColor("#3f90da")
cms_cyan = ROOT.TColor.GetColor("#92dadd")

def main():

    config = getConfig(args.config)
    config.normalize_signal = False

    categories = ["_Pat", "_DSA"]
    # categories = ["_Pat", "_PatDSA", "_DSA"]

    bkg_a = {}
    bkg_b = {}
    bkg_c = {}
    bkg_d = {}
    prediction = {}
    obs_a = {}

    signal_yields_a = {}
    signal_yields_b = {}
    signal_yields_c = {}
    signal_yields_d = {}

    all_years = config.years

    for category in categories:
        config.category = category
        config.variable_1 = config.optimal_parameters[(category, config.do_region)][0]
        config.variable_2 = config.optimal_parameters[(category, config.do_region)][1]
        config.abcd_point = config.optimal_parameters[(category, config.do_region)][2]
        config.signal_bin = config.optimal_parameters[(category, config.do_region)][3]
        config.years = all_years

        abcdPlotter = ABCDPlotter(config, args)
        abcdHelper = ABCDHelper(config, args)

        output_path = f"../plots/yields/{config.do_region}_{config.year}_noPatDSA"
        if thesis:
            output_path = f"../plots/yields_thesis/{config.do_region}_{config.year}_noPatDSA"
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        bkg_a_, bkg_b_, bkg_c_, bkg_d_, _, _, _, _ = abcdHelper.get_abcd(abcdPlotter.background_hist, config.abcd_point)
        prediction_, prediction_err_ = abcdHelper.get_prediction(bkg_b_, bkg_c_, bkg_d_, bkg_b_**0.5, bkg_c_**0.5, bkg_d_**0.5)
        print(f"{category=}, {bkg_a_=}, {bkg_b_=}, {bkg_c_=}, {bkg_d_=}, {prediction_=}")

        bkg_a[category] = bkg_a_
        bkg_b[category] = bkg_b_
        bkg_c[category] = bkg_c_
        bkg_d[category] = bkg_d_

        obs_a[category] = (bkg_a_, bkg_a_**0.5)

        prediction[category] = (prediction_, prediction_err_)

        signal_yields_a[category] = {}
        signal_yields_b[category] = {}
        signal_yields_c[category] = {}
        signal_yields_d[category] = {}    
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
                    if (mass, ctau) not in signal_yields_a[category]:
                        signal_yields_a[category][(mass,ctau)] = [0,0]
                        signal_yields_b[category][(mass,ctau)] = [0,0]
                        signal_yields_c[category][(mass,ctau)] = [0,0]
                        signal_yields_d[category][(mass,ctau)] = [0,0]
                    signal_yields_a[category][(mass,ctau)][0] += a * scale
                    signal_yields_a[category][(mass,ctau)][1] += (a**0.5 * scale) ** 2
                    signal_yields_b[category][(mass,ctau)][0] += b * scale
                    signal_yields_b[category][(mass,ctau)][1] += (b**0.5 * scale) ** 2
                    signal_yields_c[category][(mass,ctau)][0] += c * scale
                    signal_yields_c[category][(mass,ctau)][1] += (c**0.5 * scale) ** 2
                    signal_yields_d[category][(mass,ctau)][0] += d * scale
                    signal_yields_d[category][(mass,ctau)][1] += (d**0.5 * scale) ** 2


    n_bins_base = 4 if plot_abcd else 1 
    
    n_categories = len(categories)
    n_bins = n_bins_base * n_categories
    print(f"n_bins: {n_bins}")

    signal = ("12","1e1")
    signal2 = ("12","1e3")

    category_strs = {
        "_Pat": "TMS-TMS",
        "_PatDSA": "TMS-STA",
        "_DSA": "STA-STA",
    }

    if thesis:
        category_strs = {
            "_Pat": "PAT-PAT",
            "_PatDSA": "PAT-DSA",
            "_DSA": "DSA-DSA",
        }

    h_bkg = ROOT.TH1D("h_grouped_bkg", "",
                      n_bins, 0.5, n_bins + 0.5)
    h_obs = ROOT.TH1D("h_grouped_obs", "",
                      n_bins, 0.5, n_bins + 0.5)
    h_pred = ROOT.TH1D("h_grouped_pred", "",
                      n_bins, 0.5, n_bins + 0.5)
    h_sig = ROOT.TH1D("h_grouped_sig", "",
                      n_bins, 0.5, n_bins + 0.5)
    h_sig2 = ROOT.TH1D("h_grouped_sig2", "",
                      n_bins, 0.5, n_bins + 0.5)

    for i, category in enumerate(categories):
        idx_base = n_bins_base * i + 1
        h_bkg.SetBinContent(idx_base, bkg_a[category])
        h_bkg.SetBinError(idx_base, bkg_a[category]**0.5 + bkg_a[category]*bkg_syst_err[category])
        
        h_sig.SetBinContent(idx_base, signal_yields_a[category][signal][0])
        h_sig.SetBinError(idx_base, signal_yields_a[category][signal][1]**0.5)
        h_sig2.SetBinContent(idx_base, signal_yields_a[category][signal2][0])
        h_sig2.SetBinError(idx_base, signal_yields_a[category][signal2][1]**0.5)

        print(f"-- {category}: {bkg_a[category]}, {prediction[category][0]}, {signal_yields_a[category][signal][0]} +/- {signal_yields_a[category][signal][1]**0.5}, {signal_yields_a[category][signal2][0]} +/- {signal_yields_a[category][signal2][1]**0.5}")

        if not plot_abcd:
            h_pred.SetBinContent(idx_base, prediction[category][0])
            h_pred.SetBinError(idx_base, prediction[category][1] + prediction[category][0] * bkg_syst_err[category])
            print(f"obs_a[category][0] = {obs_a[category][0]}")
            h_obs.SetBinContent(idx_base, obs_a[category][0])
            h_obs.SetBinError(idx_base, obs_a[category][1])
            category_str = category_strs[category]
            h_pred.GetXaxis().SetBinLabel(idx_base, category_str)
        else:
            h_bkg.SetBinContent(idx_base+1, bkg_b[category])
            h_bkg.SetBinError(idx_base+1, bkg_b[category]**0.5)
            h_bkg.SetBinContent(idx_base+2, bkg_c[category])
            h_bkg.SetBinError(idx_base+2, bkg_c[category]**0.5)
            h_bkg.SetBinContent(idx_base+3, bkg_d[category])
            h_bkg.SetBinError(idx_base+3, bkg_d[category]**0.5)
            h_bkg.GetXaxis().SetBinLabel(idx_base, "A")
            h_bkg.GetXaxis().SetBinLabel(idx_base+1, "B")
            h_bkg.GetXaxis().SetBinLabel(idx_base+2, "C")
            h_bkg.GetXaxis().SetBinLabel(idx_base+3, "D")
            
            h_sig.SetBinContent(idx_base+1, signal_yields_b[category][signal][0])
            h_sig.SetBinError(idx_base+1, signal_yields_b[category][signal][1]**0.5)
            h_sig.SetBinContent(idx_base+2, signal_yields_c[category][signal][0])
            h_sig.SetBinError(idx_base+2, signal_yields_c[category][signal][1]**0.5)
            h_sig.SetBinContent(idx_base+3, signal_yields_d[category][signal][0])
            h_sig.SetBinError(idx_base+3, signal_yields_d[category][signal][1]**0.5)

    h_pred.SetFillColor(cms_blue)
    h_pred.SetFillStyle(1001)
    h_pred.SetLineColor(cms_blue)
    h_pred.SetLineWidth(1)

    h_pred.SetMinimum(y_min)
    h_pred.SetMaximum(y_max)
    h_pred.GetYaxis().SetTitle("Events")
    h_pred.GetYaxis().SetTitleSize(0.05)
    h_pred.GetXaxis().SetTitleSize(0.05)
    h_pred.GetYaxis().SetNdivisions(210)
    
    h_pred.GetXaxis().SetLabelSize(0)
    if plot_abcd:
        h_pred.GetXaxis().SetLabelSize(0.07)
    h_pred.GetYaxis().SetLabelSize(0.05)

    h_obs.SetFillStyle(0) 
    h_obs.SetLineColor(ROOT.kBlack)
    h_obs.SetLineWidth(2)
    h_obs.SetMarkerStyle(20)
    h_obs.SetMarkerSize(1.1)

    h_sig.SetFillStyle(0) 
    h_sig.SetLineColor(cms_red)
    h_sig.SetLineWidth(2)
    h_sig.SetMarkerSize(0.0)
    h_sig.SetMarkerColor(cms_red)
    h_sig2.SetFillStyle(0) 
    h_sig2.SetLineColor(cms_purple)
    h_sig2.SetLineWidth(2)
    # h_sig2.SetLineStyle(ROOT.kDashed)
    h_sig2.SetMarkerSize(0.0)
    h_sig2.SetMarkerColor(cms_purple)

    h_pred_err = h_pred.Clone()
    h_pred_err.SetFillColorAlpha(ROOT.kBlack, 0.3)
    h_pred_err.SetLineColor(ROOT.kBlack)
    h_pred_err.SetFillStyle(3244)
    h_pred_err.SetMarkerSize(0.0)

    h_sig_err = h_sig.Clone()
    h_sig_err.SetLineColor(cms_red)
    h_sig_err.SetMarkerSize(0.0)
    h_sig_err.SetMarkerColor(cms_red)
    h_sig2_err = h_sig2.Clone()
    h_sig2_err.SetLineColor(cms_purple)
    h_sig2_err.SetMarkerSize(0.0)
    h_sig2_err.SetMarkerColor(cms_purple)
    # h_sig2_err.SetLineStyle(ROOT.kDashed)

    c = ROOT.TCanvas("c_grouped_1d", "Grouped 4x3 1D", 800, 700)
    c.Divide(1, 2)
    c.GetPad(1).SetPad(0, 0.25, 1, 1)
    c.GetPad(1).SetLogy()
    c.GetPad(1).SetTickx(1)
    c.GetPad(1).SetTicky(1)
    c.GetPad(1).SetLeftMargin(0.14)
    c.GetPad(1).SetRightMargin(0.05)
    if not plot_abcd:
        c.GetPad(1).SetBottomMargin(0.02)
    c.GetPad(2).SetPad(0, 0, 1, 0.25)
    c.GetPad(2).SetLeftMargin(0.14)
    c.GetPad(2).SetRightMargin(0.05)
    c.GetPad(2).SetTopMargin(0)
    c.GetPad(2).SetBottomMargin(0.3)

    c.cd(1)
    ROOT.gStyle.SetOptStat(0)

    h_pred.Draw("HIST")
    h_pred_err.Draw("E2 SAME")
    h_sig.Draw("HIST ][ SAME")
    h_sig2.Draw("HIST ][ SAME")
    h_sig_err.Draw("E SAME")
    h_sig2_err.Draw("E SAME")
    if not plot_abcd:
        h_obs.Draw("e same")

    # Legend (simple)
    leg = ROOT.TLegend(0.43, 0.60, 0.87, 0.86)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.04)
    leg.AddEntry(h_obs, "Data", "pe")
    leg.AddEntry(h_pred, "Background", "f")
    leg.AddEntry(h_pred_err, "Background stat. + syst. uncertainty", "f")
    leg.AddEntry(h_sig, "m_{a} = 12 GeV, c#tau_{a} = 1 cm", "l")
    leg.AddEntry(h_sig2, "m_{a} = 12 GeV, c#tau_{a} = 1 m", "l")
    leg.Draw()

    luminosity_run2 = 138
    luminosity_run3 = 62
    lumi_text = f"#scale[0.8]{{{luminosity_run2} fb^{{-1}} (13 TeV), {luminosity_run3:.0f} fb^{{-1}} (13.6 TeV)}}"
    tex = ROOT.TLatex(0.58, 0.92, lumi_text)
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.DrawClone()

    tex = ROOT.TLatex(0.14, 0.92, "#bf{CMS}#it{ Preliminary}")
    if thesis:
        tex = ROOT.TLatex(0.14, 0.92, "#bf{CMS}#it{ Work in Progress}")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.DrawClone()

    if plot_abcd:
        line_pos_x = h_pred.GetXaxis().GetBinLowEdge(5)
        line1 = ROOT.TLine(line_pos_x, y_min, line_pos_x, line_max)
        line1.SetLineColor(ROOT.kBlack)
        line1.SetLineWidth(2)
        line1.Draw()
        line_pos_x = h_pred.GetXaxis().GetBinLowEdge(9)
        line2 = ROOT.TLine(line_pos_x, y_min, line_pos_x, line_max)
        line2.SetLineColor(ROOT.kBlack)
        line2.SetLineWidth(2)
        line2.Draw()

        tex_pos_x = h_pred.GetXaxis().GetBinLowEdge(2)
        tex2 = ROOT.TLatex(tex_pos_x, category_y, "TMS-TMS")
        tex2.SetTextFont(42)
        tex2.SetTextSize(0.045)
        tex2.DrawClone()
        tex_pos_x = h_pred.GetXaxis().GetBinLowEdge(6)
        tex2 = ROOT.TLatex(tex_pos_x, category_y, "TMS-STA")
        tex2.SetTextFont(42)
        tex2.SetTextSize(0.045)
        tex2.DrawClone()
        tex_pos_x = h_pred.GetXaxis().GetBinLowEdge(10)
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

    if not plot_abcd:
        c.cd(2)

        h_ratio = h_obs.Clone("ratio_pred_bkg")
        h_ratio.Add(h_pred, -1)
        h_ratio.Divide(h_pred)

        h_ratio.Draw("p e0")
        h_ratio.SetMinimum(-2.5)
        h_ratio.SetMaximum(2.5)
        h_ratio.GetYaxis().SetTitle("#frac{Data-Bkg.}{Bkg.}")
        h_ratio.GetYaxis().SetTitleSize(0.15)
        h_ratio.GetYaxis().SetLabelSize(0.15)
        h_ratio.GetYaxis().SetTitleOffset(0.30)
        h_ratio.GetYaxis().CenterTitle()
        h_ratio.GetYaxis().SetNdivisions(404)

        h_ratio.GetXaxis().SetBinLabel(1, category_strs["_Pat"])
        # h_ratio.GetXaxis().SetBinLabel(2, "TMS-STA")
        # h_ratio.GetXaxis().SetBinLabel(3, "STA-STA")
        h_ratio.GetXaxis().SetBinLabel(2, category_strs["_DSA"])
        h_ratio.GetXaxis().SetLabelOffset(0.02)
        h_ratio.GetXaxis().SetLabelFont(42)
        h_ratio.GetXaxis().SetLabelSize(0.20)
        # h_ratio.GetXaxis().SetTitle("Dimuon category")
        h_ratio.GetXaxis().SetTitleOffset(1.20)
        h_ratio.GetXaxis().SetTitleSize(0.16)

        h_pred_ratio_err = h_pred_err.Clone("bkg_err_ratio")
        print(f"h_pred_err.GetNbinsX(): {h_pred_err.GetNbinsX()}")
        print(f"h_pred_ratio_err.GetNbinsX(): {h_pred_ratio_err.GetNbinsX()}")
        for i in range(1, h_pred_ratio_err.GetNbinsX() + 1):
            bkg = h_pred_err.GetBinContent(i)
            err = h_pred_err.GetBinError(i)
            rel_err = err / bkg
            err = h_pred_err.GetBinError(i)
            h_pred_ratio_err.SetBinContent(i, 0.0)
            h_pred_ratio_err.SetBinError(i, rel_err)
        h_pred_ratio_err.Draw("E2 SAME")

        # plot.SetTitle("" if is_ratio else hist.title)
        # plot.GetXaxis().SetLimits(hist.x_min, hist.x_max)
        # h_ratio.GetXaxis().SetTitle(hist.x_label)
        # plot.GetXaxis().SetTitleOffset(1.0 if is_ratio else 1.7)
        # plot.GetYaxis().SetTitleSize(self.labelFontSize)
        # plot.GetYaxis().SetTitleOffset(1.5)

        x_min = h_ratio.GetXaxis().GetBinLowEdge(1)
        x_max = h_ratio.GetXaxis().GetBinLowEdge(3)
        line = ROOT.TLine(x_min, 0, x_max, 0)
        line.SetLineColor(ROOT.kBlack)
        line.SetLineStyle(ROOT.kDashed)

        line.Draw()

        c.Update()


    extra_str = ""
    if plot_abcd:
        extra_str = "_adcd"
    print(f"Saving plot {output_path}/SR_yields{extra_str}_cmscolors_unblinded.pdf")
    c.SaveAs(f"{output_path}/SR_yields{extra_str}_cmscolors_unblinded.pdf")

if __name__ == '__main__':
  main()
