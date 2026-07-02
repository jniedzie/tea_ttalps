from Logger import info, warn, error, fatal, logger_print
from ttalps_samples_list import dasBackgrounds2016preVFP, dasBackgrounds2016postVFP,dasBackgrounds2017, dasBackgrounds2018
from ttalps_samples_list import dasBackgrounds2022preEE, dasBackgrounds2022postEE, dasBackgrounds2023preBPix, dasBackgrounds2023postBPix
from Histogram import Histogram2D, Histogram
from Sample import Sample, SampleType
from HistogramNormalizer import NormalizationType
from ScaleFactorProducer import ScaleFactorProducer
from CorrectionWriter import CorrectionWriter

from ttalps_luminosities import get_luminosity
from ttalps_cross_sections import get_cross_sections

import ROOT
import os
import math
from ctypes import c_double
import array

# years = ["2017", ]
# years = ["2022preEE", "2022postEE",]
years = ["2016preVFP", "2016postVFP", "2017", "2018", "2022preEE", "2022postEE", "2023preBPix", "2023postBPix",]

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# category = ""
# category = "_Pat"
# category = "_PatDSA"
category = "_DSA"

skims = {
    "_Pat": ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "noDimuonEffSFs_ABCD"),
    "_PatDSA": ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuonsPatDSA", "noDimuonEffSFs_noMatching_ABCD_ANv3"),
    "_DSA": ("skimmed_looseSemimuonic_v3_SR", "JPsiDimuons", "noDimuonEffSFs_revertedMatching_ABCD", "SR"),
}
skim = skims[category]
hist_path = "histograms"

reverted_matching = True if category == "_DSA" else False

dimuon_collection = "BestDimuonVertex"

merge_to_one_bin_hists = False

# fit_function = "const"
# fit_function = "linear"
# fit_function = "exp_linear"
fit_function = "exp_linear_a"
# fit_function = "xpow"
# fit_function = "exp2"
# fit_function = "exp2_a"
# fit_function = "exp3"
# fit_function = "interp"
# fit_function = "datamc"

samples = []
year_string = ""
for year in years:
    year_string += year
    cross_sections = get_cross_sections(year)
    luminosity = get_luminosity(year)

    backgrounds = globals()[f"dasBackgrounds{year}"]
    for background in backgrounds.keys():
        samples.append(
            Sample(
                name=background.split("/")[-1],
                file_path=f"{base_path}/{background}/{skim[0]}/{hist_path}_{skim[1]}_{skim[2]}/histograms.root",
                type=SampleType.background,
                cross_sections=cross_sections,
                luminosity=luminosity,
                line_alpha=0,
                line_style=1,
                fill_alpha=0.7,
                marker_size=0,
                marker_style=0,
                year=year,
            )
        )
    year_simple = "".join(filter(str.isdigit, year))
    data = f"collision_data{year}/SingleMuon{year_simple}"
    if "2022" in year:
        data = f"collision_data{year}/Muon{year_simple}"
    if "2023" in year:
        data = f"collision_data{year}/Muon1{year_simple}"
    samples.append(
        Sample(
            name=f"data_{year}",
            file_path=f"{base_path}/{data}_{skim[0]}_{hist_path}_{skim[1]}_{skim[2]}.root",
            type=SampleType.data,
            line_style=1,
            line_alpha=1,
            fill_alpha=0,
            marker_size=0.7,
            marker_style=20,
            year=year,
        )
    )

output_graph_dir = None
# output_graph_dir = "../ttalps_get_SF_over_resonance_fraction_graphs_ANv3"
# if len(years) > 1:
#     output_graph_dir = None
# output_dir = f"../sf/sf_as_fractions/{year_string}_{skim[1]}_{skim[2]}_{fit_function}"
output_dir = f"../sf/sf_as_fractions_thesis/{year_string}_{skim[1]}_{skim[2]}_{fit_function}"
if not os.path.exists(output_dir):
  os.makedirs(output_dir)

resonant_categories = ["Resonant", "NonResonant"]

resonance_variables_ = {
    "_Pat": [
        "eta_irr2",
        "eta_irr2_logPtlt1p2",
        "eta_irr2_logPtlt1p1",
        "eta_irr2_logPtlt1p0",
        "eta_irr2_logPtgt1p2",
        "eta_irr2_logPtgt1p4",
    ],
    "_PatDSA": [
        "",
        "_logDRlt-1_logDxySig2gt0",
        "_logDRlt-0p8_logDxySig2gt0p2",
        "_logDRlt-1p2_logDxySig2gt-0p2",
        "_logDRgt-1_logDxySig2lt0",
        "_logDRgt-1p5_logDxySig2lt0p5",
        "_logDRgt-2_logDxySig2lt1",

        "_logDRgt-1p2_logDxySig2lt-0p2",
        "_logDRlt-0p5_logDxySig2lt-0p2",
        "_logDRgt-1_logDxySig2gt0",
        "_logDRgt-2_logDxySig2gt0",

        # "eta_irr2_logPtlt1p2",
        # "eta_irr2_logPtlt1p1",
        # "eta_irr2_logPtlt1p0",
        # "eta_irr2_logPtgt1p2",
        # "eta_irr2_logPtgt1p4",
        # "eta_irr2_logDxySig1gt0p2_logDxySig2gt0p2",
        # "eta_irr2_logDxySig1gt0p1_logDxySig2gt0p1",
        # "eta_irr2_logDxySig1gt0_logDxySig2gt0",
        # "eta_irr2_logDxySig1gt-0p1_logDxySig2gt-0p1",
        # "eta_irr2_logDxySig1lt0p1_logDxySig2lt0p1",
    ],
    "_DSA": [
        "eta_irr2",
        "eta_irr2_logDxySig1gt0p2_logDxySig2gt0p2",
        "eta_irr2_logDxySig1gt0p1_logDxySig2gt0p1",
        "eta_irr2_logDxySig1gt0_logDxySig2gt0",
        "eta_irr2_logDxySig1gt-0p1_logDxySig2gt-0p1",
        "eta_irr2_logDxySig1lt0p1_logDxySig2lt0p1",
    ],
}
resonance_variables = resonance_variables_[category]

y_axis_ranges = {
    "_Pat": (0,2),
    "_PatDSA": (0,3),
    "_DSA": (0, 3.5),
}
y_axis_range = y_axis_ranges[category]

resonant_str = "Resonant"

# sf_bin_variable = "pt_irr"
sf_bin_variable = "eta_irr"

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta, ROOT.kOrange+7, ROOT.kCyan+2]


def sf_and_err_lin(x, res):
    """
    Returns (SF, SF_up, SF_down) at given x
    using full covariance propagation.
    """

    SF = res["p0"] + res["p1"] * x

    err = math.sqrt(
        res["p0_err"]**2
        + (x * res["p1_err"])**2
        + 2.0 * x * res["cov01"]
    )

    SF_up = SF + err
    SF_down = SF - err

    return SF, SF_up, SF_down

def sf_and_err_exp_lin(x, res):
    z = res["p0"] + res["p1"] * x
    SF = math.exp(z)

    var_z = (
        res["p0_err"]**2
        + (x * res["p1_err"])**2
        + 2.0 * x * res["cov01"]
    )

    err = SF * math.sqrt(var_z)

    return SF, SF + err, SF - err

def sf_and_err_exp_lin_a(x, res):
    z = res["p0"] - 1.20*x
    SF = math.exp(z)

    err = SF * res["p0_err"]

    return SF, SF + err, SF - err

def sf_and_err_exp3(x, res):
    c, A, k = res["c"], res["A"], res["k"]

    e = math.exp(-k * x)
    SF = c + A * e

    # derivatives
    dc = 1.0
    dA = e
    dk = -A * x * e

    cov = res["cov"]

    var = (
        dc*dc * cov(0,0)
        + dA*dA * cov(1,1)
        + dk*dk * cov(2,2)
        + 2*dc*dA * cov(0,1)
        + 2*dc*dk * cov(0,2)
        + 2*dA*dk * cov(1,2)
    )

    err = math.sqrt(var)

    return SF, SF + err, SF - err

def sf_and_err_exp2(x, res):
    p0 = res["p0"]
    p1 = res["p1"]

    SF = p0 + math.exp(p1 * x)

    var = (
        res["p0_err"]**2
        + (x * math.exp(p1 * x) * res["p1_err"])**2
        + 2.0 * x * math.exp(p1 * x) * res["cov01"]
    )

    err = math.sqrt(var)

    return SF, SF + err, SF - err

def sf_and_err_exp2_a(x, res):
    p0 = res["p0"]
    SF = p0 + math.exp(-7.7 * x)
    err = res["p0_err"]

    return SF, SF + err, SF - err


def sf_and_err_xpow(x, res):
    p0 = res["p0"]
    p1 = res["p1"]

    SF = p0 + x**p1

    d_p0 = 1.0
    d_p1 = (x**p1) * math.log(x)

    var = (
        (d_p0 * res["p0_err"])**2
        + (d_p1 * res["p1_err"])**2
        + 2.0 * d_p0 * d_p1 * res["cov01"]
    )

    err = math.sqrt(var)

    return SF, SF + err, SF - err


def sf_and_err_interp(x, res):
    """
    Returns (SF, SF_up, SF_down) for
    SF = ([0]*x + [1]*(1-x)) / ([2]*x + [3]*(1-x))
    using full covariance propagation.
    """

    p0 = res["p0"]
    p1 = res["p1"]
    p2 = res["p2"]
    p3 = res["p3"]
    cov = res["cov"]   # full covariance matrix

    N = p0 * x + p1 * (1.0 - x)
    D = p2 * x + p3 * (1.0 - x)

    SF = N / D

    # derivatives
    d_p0 =  x / D
    d_p1 = (1.0 - x) / D
    d_p2 = -N * x / D**2
    d_p3 = -N * (1.0 - x) / D**2

    grads = [d_p0, d_p1, d_p2, d_p3]

    # variance = g^T C g
    var = 0.0
    for i in range(4):
        for j in range(4):
            var += grads[i] * cov(i, j) * grads[j]

    err = math.sqrt(var)

    return SF, SF + err, SF - err


def sf_and_err_datamc(x, res):
    p0 = res["p0"]
    p1 = res["p1"]
    D = res["D"]
    M = res["MC"]

    N = p0 * x + (D - p0) * (1 - x)
    Dn = p1 * x + (M - p1) * (1 - x)

    SF = N / Dn

    # derivatives for error propagation
    d_p0 = (x - (1 - x)) / Dn   # ∂N/∂p0 / Dn
    d_p1 = -N * (x - (1 - x)) / Dn**2

    cov = res["cov"]

    var = d_p0**2 * cov(0,0) + d_p1**2 * cov(1,1) + 2*d_p0*d_p1*cov(0,1)
    err = math.sqrt(var)

    return SF, SF + err, SF - err


def plot_sf_with_variations(fit_results, x_min, x_max, n_points=200, canvas_name="c_sf_variations"):
    c = ROOT.TCanvas(canvas_name, "", 900, 700)
    c.SetGrid()

    # leg = ROOT.TLegend(0.15, 0.60, 0.45, 0.88)
    leg = ROOT.TLegend(0.35, 0.65, 0.88, 0.88)
    leg.SetBorderSize(0)

    first = True
    all_objects = []

    for i, pt in enumerate(sorted(fit_results.keys())):
        res = fit_results[pt]
        col = colors[i % len(colors)]

        gr_c, gr_u, gr_d = ROOT.TGraph(), ROOT.TGraph(), ROOT.TGraph()
        all_objects.extend([gr_c, gr_u, gr_d, leg])

        gr_c.SetLineColor(col)
        gr_u.SetLineColor(col)
        gr_d.SetLineColor(col)

        gr_c.SetLineWidth(3)
        gr_u.SetLineWidth(2)
        gr_d.SetLineWidth(2)

        gr_u.SetLineStyle(2)
        gr_d.SetLineStyle(2)

        for j in range(n_points):
            x = x_min + j * (x_max - x_min) / (n_points - 1)
            if fit_function == "const":
                SF = res["p0"]
                SF_up = res["p0"] + res["p0_err"]
                SF_down = res["p0"] - res["p0_err"]
            if fit_function == "linear":
                SF, SF_up, SF_down = sf_and_err_lin(x, res)
            if fit_function == "exp_linear":
                SF, SF_up, SF_down = sf_and_err_exp_lin(x, res)
            if fit_function == "exp_linear_a":
                SF, SF_up, SF_down = sf_and_err_exp_lin_a(x, res)
            if fit_function == "exp2":
                SF, SF_up, SF_down = sf_and_err_exp2(x, res)
            if fit_function == "exp2_a":
                SF, SF_up, SF_down = sf_and_err_exp2_a(x, res)
            if fit_function == "xpow":
                SF, SF_up, SF_down = sf_and_err_xpow(x, res)
            if fit_function == "exp3":
                SF, SF_up, SF_down = sf_and_err_exp3(x, res)
            if fit_function == "interp":
                SF, SF_up, SF_down = sf_and_err_interp(x, res)
            if fit_function == "datamc":
                SF, SF_up, SF_down = sf_and_err_datamc(x, res)
            gr_c.SetPoint(j, x, SF)
            gr_u.SetPoint(j, x, SF_up)
            gr_d.SetPoint(j, x, SF_down)

        draw_opt = "AL" if first else "L"
        gr_c.Draw(draw_opt)
        gr_u.Draw("L SAME")
        gr_d.Draw("L SAME")

        if first:
            gr_c.GetXaxis().SetTitle("Resonant fraction x")
            gr_c.GetYaxis().SetTitle("Correction")
            gr_c.GetYaxis().SetRangeUser(y_axis_range[0],y_axis_range[1])
            first = False

        if fit_function == "const":
            p0 = res["p0"]
            eq_text = f"{p0:.2f} +/- {p0:.2f}"
        if fit_function == "linear":
            p0 = res["p0"]
            p1 = res["p1"]
            eq_text = f"{p0:.2f} + {p1:.2f} * x"
        if fit_function == "exp_linear":
            p0 = res["p0"]
            p1 = res["p1"]
            eq_text = f"exp({p0:.2f} + {p1:.2f} * x)"
        if fit_function == "exp_linear_a":
            p0 = res["p0"]
            eq_text = f"exp({p0:.2f} - 1.20 * x)"
        if fit_function == "exp2":
            p0, p1 = res["p0"], res["p1"]
            eq_text = f"{p0:.2f} + exp({p1:.2f} * x)"
        if fit_function == "exp2_a":
            p0 = res["p0"]
            eq_text = f"{p0:.2f} + exp(-7.7 * x)"
        if fit_function == "xpow":
            p0, p1 = res["p0"], res["p1"]
            eq_text = f"{p0:.2f} + x ^ {p1:.2f})"
        if fit_function == "exp3":
            c_, A, k = res["c"], res["A"], res["k"]
            eq_text = f"{c_:.2f} + {A:.2f} * exp(-{k:.2f} * x)"
        if fit_function == "interp":
            p0 = res["p0"]
            p1 = res["p1"]
            p2 = res["p2"]
            p3 = res["p3"]
            eq_text = f"({p0:.2f} * x + {p1:.2f} * (1 - x)) / ({p2:.2f} * x + {p3:.2f} * (1 - x))"
        if fit_function == "datamc":
            p0 = res["p0"]
            p1 = res["p1"]
            D = res["D"]
            M = res["MC"]
            eq_text = f"({p0:.2f} * x + ({D:0.1f} - {p0:.2f}) * (1 - x)) / ({p1:.2f} * x + ({M:.2f} - {p1:.2f}) * (1 - x))"
        chi2ndf = res["chi2"] / res["ndf"]
        # leg_text = f"p_{{T}} = {pt}: SF(x) = {eq_text}, #Chi^{{2}}/ndf = {chi2ndf:.2f}"
        leg_text = f"p_{{T}} = {pt}: SF(x) = {eq_text}"
        leg.AddEntry(gr_c, leg_text, "l")

    leg.Draw()
    c.Update()
    return c, all_objects

def draw_sf_points(resonant_fractions, scale_factors, pt_bin, pt_bin_i, marker_style=20, color=ROOT.kBlack):
    """
    Draw the original SF points with asymmetric errors for a given pt_bin.
    
    Returns the TGraphAsymmErrors object.
    """
    x_vals, y_vals = [], []
    x_unc_up, x_unc_down = [], []
    y_unc_up, y_unc_down = [], []

    for variable in resonant_fractions.keys():
        x = resonant_fractions[variable][pt_bin]
        # x = resonant_fractions[variable]
        sf_dict = list(scale_factors[variable].values())
        SF, SF_up, SF_down = sf_dict[pt_bin_i]
        if not SF or not SF_up or not SF_down:
            warn(f"No SF found for fraction {x} in pt bin {pt_bin}.")
            continue
        x_vals.append(x)
        y_vals.append(SF)
        x_unc_up.append(0)
        x_unc_down.append(0)
        y_unc_up.append(SF_up - SF)
        y_unc_down.append(SF - SF_down)

    gr_points = ROOT.TGraphAsymmErrors(
        len(x_vals),
        array.array("d", x_vals),
        array.array("d", y_vals),
        array.array("d", x_unc_down),
        array.array("d", x_unc_up),
        array.array("d", y_unc_down),
        array.array("d", y_unc_up)
    )

    gr_points.SetMarkerStyle(marker_style)
    gr_points.SetMarkerColor(color)
    gr_points.SetLineColor(color)
    
    gr_points.Draw("P SAME")  # draw points on existing canvas
    return gr_points

import ROOT

def merge_to_single_bin(hist):
    # Create a new 1-bin histogram
    merged = ROOT.TH1D(
        f"{hist.GetName()}_merged",
        hist.GetTitle(),
        1, 0, 1
    )

    total = 0.0
    err2 = 0.0

    for i in range(1, hist.GetNbinsX() + 1):
        c = hist.GetBinContent(i)
        e = hist.GetBinError(i)

        total += c
        err2 += e * e  # sum in quadrature

    merged.SetBinContent(1, total)
    merged.SetBinError(1, err2**0.5)

    return merged


def main():
    resonant_fractions = {}
    resonant_events = {}
    nonresonant_events = {}
    n_tot_events = {}


    sfProducer = ScaleFactorProducer()
    sfProducer.setSamples(samples)
    # if category == "_Pat":
    #     sfProducer.setCorrectedPtBins()
    correctionWriter = CorrectionWriter()
    scale_factors = {}
    ratio_hist = {}
    ratio_unc_hist_up = {}
    ratio_unc_hist_down = {}

    data_events = {}
    mc_events = {}

    for variable in resonance_variables:

        hist_name = f"{dimuon_collection}{category}_{sf_bin_variable}{variable}"
        if reverted_matching:
            hist_name = f"{dimuon_collection}{category}_revertedMatching_{sf_bin_variable}_{variable}"

        histogram1D = Histogram(
            name=hist_name,
            title=hist_name,
            norm_type=NormalizationType.to_lumi,
        )
        print(f"hist_name: {hist_name}")
        data_histogram = sfProducer.getDataHistogram1D(histogram1D)
        background_histogram = sfProducer.getBackgroundHistogram1D(histogram1D)
        data_hist = data_histogram.hist
        background_hist = background_histogram.hist
        if merge_to_one_bin_hists:
            data_hist = merge_to_single_bin(data_histogram.hist)
            data_histogram.hist = data_hist
            background_hist = merge_to_single_bin(background_histogram.hist)
            background_histogram.hist = background_hist
        scale_factors[variable] = sfProducer.getDataMCRatios1D(data_histogram, background_histogram)
        ratio_hist[variable],ratio_unc_hist_up[variable],ratio_unc_hist_down[variable]  = sfProducer.getDataMCRatioHists1D(data_histogram, background_histogram)

        print(f"{scale_factors[variable].keys()=}")
        pt_bins_ = list(scale_factors[variable].keys())
        print(f"{pt_bins_=}")
        resonant_hist_name = f"{dimuon_collection}{resonant_str}{category}_{sf_bin_variable}{variable}"
        if reverted_matching:
            resonant_hist_name = f"{dimuon_collection}{resonant_str}{category}_revertedMatching_{sf_bin_variable}_{variable}"
        nonresonant_hist_name = f"{dimuon_collection}Non{resonant_str}{category}_{sf_bin_variable}{variable}"
        if reverted_matching:
            nonresonant_hist_name = f"{dimuon_collection}Non{resonant_str}{category}_revertedMatching_{sf_bin_variable}{variable}"

        print(f"{resonant_hist_name=}")
        resonant_histogram1D = Histogram(
            name=resonant_hist_name,
            title=resonant_hist_name,
            norm_type=NormalizationType.to_lumi,
        )
        nonresonant_histogram1D = Histogram(
            name=nonresonant_hist_name,
            title=nonresonant_hist_name,
            norm_type=NormalizationType.to_lumi,
        )

        resonant_events[variable] = {}
        nonresonant_events[variable] = {}
        n_tot_events[variable] = {}
        resonant_fractions[variable] = {}
        resonant_background_histogram = sfProducer.getBackgroundHistogram1D(resonant_histogram1D)
        nonresonant_background_histogram = sfProducer.getBackgroundHistogram1D(nonresonant_histogram1D)
        resonant_background_hist = resonant_background_histogram.hist
        nonresonant_background_hist = nonresonant_background_histogram.hist
        if merge_to_one_bin_hists:
            resonant_background_hist = merge_to_single_bin(resonant_background_histogram.hist)
            background_hist = merge_to_single_bin(background_histogram.hist)
        for i in range(1, background_hist.GetNbinsX()+1):
            resonant_events[variable][pt_bins_[i-1]] = resonant_background_hist.GetBinContent(i)
            nonresonant_events[variable][pt_bins_[i-1]] = nonresonant_background_hist.GetBinContent(i)
            n_tot_events[variable][pt_bins_[i-1]] = resonant_background_hist.GetBinContent(i) + nonresonant_background_hist.GetBinContent(i)
            resonant_fractions[variable][pt_bins_[i-1]] = resonant_background_hist.GetBinContent(i)/n_tot_events[variable][pt_bins_[i-1]] if n_tot_events[variable][pt_bins_[i-1]] != 0.0 else 0.0

    variable0 = resonance_variables[0]
    pt_bins = scale_factors[variable0].keys()
    fit_results = {}

    for i, pt_bin in enumerate(pt_bins):
        x_vals, y_vals = [], []
        x_unc_up, x_unc_down = [], []
        y_unc_up, y_unc_down = [], []

        for variable in resonance_variables:
            x = resonant_fractions[variable][pt_bin]
            # x = resonant_fractions[variable]
            sf_dict = list(scale_factors[variable].values())
            SF, SF_up, SF_down = sf_dict[i]
            if not SF or not SF_up or not SF_down:
                warn(f"No SF found for fraction {x} in pt bin {pt_bin}.")
                continue
            x_vals.append(x)
            y_vals.append(SF)
            x_unc_up.append(0)
            x_unc_down.append(0)
            y_unc_up.append(SF_up - SF)
            y_unc_down.append(SF - SF_down)
    
        gr = ROOT.TGraphAsymmErrors(
            len(x_vals),
            array.array("d", x_vals),
            array.array("d", y_vals),
            array.array("d", x_unc_up),
            array.array("d", x_unc_down),
            array.array("d", y_unc_up),
            array.array("d", y_unc_down),
        )

        if output_graph_dir:
            gr.SaveAs(f"{output_graph_dir}/graph_{year_string}_{skim[1]}_{skim[2]}_{fit_function}_{sf_bin_variable}_{str(int(pt_bin))}.root")

        gr.SetName(f"gr_pt_{pt_bin}")
        gr.SetMarkerStyle(20)

        # Constant function
        if fit_function == "const":
            f = ROOT.TF1(f"f_pt_{pt_bin}", "[0]",
                        min(x_vals), max(x_vals))
            f.SetParameters(1.0)
        
        # Linear function
        if fit_function == "linear":
            f = ROOT.TF1(f"f_pt_{pt_bin}", "[0] + [1]*x",
                        min(x_vals), max(x_vals))
            f.SetParameters(1.0, 0.0)

        # y = exp(a + bx):
        if fit_function == "exp_linear":
            b = -1.20
            f = ROOT.TF1(
                f"f_pt_{pt_bin}",
                "exp([0] + [1]*x)",
                min(x_vals),
                max(x_vals),
            )
            f.SetParameters(0.5, -0.5)
            # f.SetParLimits(0, -1.5, 1.2) # 0.22-3.32 for x=0
            f.SetParLimits(1, -100.0, 0.2) # negative slope
        
        if fit_function == "exp_linear_a":
            f = ROOT.TF1(
                f"f_pt_{pt_bin}",
                "exp([0] - 1.20*x)",
                min(x_vals),
                max(x_vals),
            )
            f.SetParameters(0.5)
        
        if fit_function == "exp2":
            f = ROOT.TF1(
                f"f_pt_{pt_bin}",
                "[0] + exp([1]*x)",
                min(x_vals),
                max(x_vals),
            )
            f.SetParameters(0.2, -0.5)
            # f.SetParLimits(1, -100.0, 0.2)
        
        if fit_function == "exp2_a":
            f = ROOT.TF1(
                f"f_pt_{pt_bin}",
                "[0] + exp(-7.7*x)",
                min(x_vals),
                max(x_vals),
            )
            f.SetParameters(1.0)
        
        if fit_function == "xpow":
            f = ROOT.TF1(
                f"f_pt_{pt_bin}",
                "[0] + pow(x,[1])",
                min(x_vals),
                max(x_vals),
            )
            f.SetParameters(1.2, -0.5)
            f.SetParLimits(1, -100.0, 0.2)

        if fit_function == "exp3":
            f = ROOT.TF1(
                f"f_pt_{pt_bin}",
                "[0] + [1]*exp(-[2]*x)",
                min(x_vals),
                max(x_vals),
            )
            f.SetParameters(0.5, 1.0, 1.0)

        if fit_function == "interp":
            f = ROOT.TF1(
                "f_interp",
                "([0]*x + [1]*(1-x)) / ([2]*x + [3]*(1-x))",
                min(x_vals),
                max(x_vals),
            )
            f.SetParameters(1.0, 1.5, 1.0, 1.0)
            f.SetParLimits(2, 1e-3, 10.0)
            f.SetParLimits(3, 1e-3, 10.0)
        
        if fit_function == "datamc":
            data = float(data_events[pt_bin])
            mc = float(mc_events[pt_bin])
            f = ROOT.TF1(
                "f_datamc",
                f"([0]*x + ({data}-[0])*(1-x)) / ([1]*x + ({mc}-[1])*(1-x))",
                min(x_vals),
                max(x_vals),
            )
            f.SetParameters(1.0, 1.5)
            f.SetParLimits(1, 1e-3, mc - 1e-3)

        fit_result = gr.Fit(f, "S")

        cov = fit_result.GetCovarianceMatrix()

        if fit_function == "const" or fit_function == "exp_linear_a" or fit_function == "exp2_a":
            fit_results[pt_bin] = {
                "p0": f.GetParameter(0),
                "p0_err": f.GetParError(0),
                "cov01": cov(0, 1),
                "chi2": f.GetChisquare(),
                "ndf": f.GetNDF(),
            }
        if fit_function == "linear" or fit_function == "exp_linear" or fit_function == "exp2" or fit_function == "xpow":
            fit_results[pt_bin] = {
                "p0": f.GetParameter(0),
                "p0_err": f.GetParError(0),
                "p1": f.GetParameter(1),
                "p1_err": f.GetParError(1),
                "cov01": cov(0, 1),
                "chi2": f.GetChisquare(),
                "ndf": f.GetNDF(),
            }
        if fit_function == "exp3":
            fit_results[pt_bin] = {
                "c": f.GetParameter(0),
                "c_err": f.GetParError(0),
                "A": f.GetParameter(1),
                "A_err": f.GetParError(1),
                "k": f.GetParameter(2),
                "k_err": f.GetParError(2),
                "cov": cov,
                "chi2": f.GetChisquare(),
                "ndf": f.GetNDF(),
            }
        if fit_function == "interp":
            fit_results[pt_bin] = {
                "p0": f.GetParameter(0),
                "p0_err": f.GetParError(0),
                "p1": f.GetParameter(1),
                "p1_err": f.GetParError(1),
                "p2": f.GetParameter(2),
                "p2_err": f.GetParError(2),
                "p3": f.GetParameter(3),
                "p3_err": f.GetParError(3),
                "cov": cov,
                "chi2": f.GetChisquare(),
                "ndf": f.GetNDF(),
            }
        if fit_function == "datamc":
            fit_results[pt_bin] = {
                "p0": f.GetParameter(0),
                "p0_err": f.GetParError(0),
                "p1": f.GetParameter(1),
                "p1_err": f.GetParError(1),
                "cov": cov,
                "chi2": f.GetChisquare(),
                "ndf": f.GetNDF(),
                "D": float(data_events[pt_bin]),
                "MC": float(mc_events[pt_bin]),
            }
        
        print()
        print(f"---- pT bin: {pt_bin}:")
        print(f"chi2: {f.GetChisquare()}")
        print(f"ndf: {f.GetNDF()}")
        if f.GetNDF() > 0:
            print(f"chi2/ndf: {f.GetChisquare()/f.GetNDF()}")
        print(f"prob: {f.GetProb()}")
    
    c, all_objects = plot_sf_with_variations(fit_results, x_min=0.0, x_max=1.0)
    for i, pt_bin in enumerate(pt_bins):
        gr_points = draw_sf_points(resonant_fractions, scale_factors, pt_bin, i, color=colors[i])
        all_objects.append(gr_points)
        if fit_function == "const":
            SF_0 = SF_1 = fit_results[pt_bin]["p0"]
            SF_up_0 = SF_up_1 = fit_results[pt_bin]["p0"] + fit_results[pt_bin]["p0_err"]
            SF_down_0 = SF_down_1 = fit_results[pt_bin]["p0"] - fit_results[pt_bin]["p0_err"]
        if fit_function == "linear":
            SF_0, SF_up_0, SF_down_0 = sf_and_err_lin(0.0, fit_results[pt_bin])
            SF_1, SF_up_1, SF_down_1 = sf_and_err_lin(1.0, fit_results[pt_bin])
        if fit_function == "exp_linear":
            SF_0, SF_up_0, SF_down_0 = sf_and_err_exp_lin(0.0, fit_results[pt_bin])
            SF_1, SF_up_1, SF_down_1 = sf_and_err_exp_lin(1.0, fit_results[pt_bin])
        if fit_function == "exp_linear_a":
            SF_0, SF_up_0, SF_down_0 = sf_and_err_exp_lin_a(0.0, fit_results[pt_bin])
            SF_1, SF_up_1, SF_down_1 = sf_and_err_exp_lin_a(1.0, fit_results[pt_bin])
        if fit_function == "exp2":
            SF_0, SF_up_0, SF_down_0 = sf_and_err_exp2(0.0, fit_results[pt_bin])
            SF_1, SF_up_1, SF_down_1 = sf_and_err_exp2(1.0, fit_results[pt_bin])
        if fit_function == "exp2_a":
            SF_0, SF_up_0, SF_down_0 = sf_and_err_exp2_a(0.0, fit_results[pt_bin])
            SF_1, SF_up_1, SF_down_1 = sf_and_err_exp2_a(1.0, fit_results[pt_bin])
        if fit_function == "xpow":
            SF_0, SF_up_0, SF_down_0 = sf_and_err_xpow(0.0, fit_results[pt_bin])
            SF_1, SF_up_1, SF_down_1 = sf_and_err_xpow(1.0, fit_results[pt_bin])
        if fit_function == "exp3":
            SF_0, SF_up_0, SF_down_0 = sf_and_err_exp3(0.0, fit_results[pt_bin])
            SF_1, SF_up_1, SF_down_1 = sf_and_err_exp3(1.0, fit_results[pt_bin])
        if fit_function == "interp":
            SF_0, SF_up_0, SF_down_0 = sf_and_err_interp(0.0, fit_results[pt_bin])
            SF_1, SF_up_1, SF_down_1 = sf_and_err_interp(1.0, fit_results[pt_bin])
        if fit_function == "datamc":
            SF_0, SF_up_0, SF_down_0 = sf_and_err_datamc(0.0, fit_results[pt_bin])
            SF_1, SF_up_1, SF_down_1 = sf_and_err_datamc(1.0, fit_results[pt_bin])
        print(f"SFs for pT: {pt_bin}")
        print(f"x=0.0: nom: {SF_0}, up: {SF_up_0} down: {SF_down_0}")
        print(f"x=1.0: nom: {SF_1}, up: {SF_up_1} down: {SF_down_1}")
        print(f"x=0.0: {SF_0} + {SF_up_0-SF_0} - {SF_0-SF_down_0}")
        print(f"x=1.0: {SF_1} + {SF_up_1-SF_1} - {SF_1-SF_down_1}")


    c.SaveAs(f"{output_dir}/corrections_thesis_{sf_bin_variable}.pdf")


if __name__ == "__main__":
    main()