import os
import glob
from copy import deepcopy
import ROOT
from array import array
import random

from ttalps_samples_list import dasBackgrounds2018
from Sample import Sample, SampleType
from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity
from ScaleFactorProducer import ScaleFactorProducer
from Histogram import Histogram
from HistogramNormalizer import NormalizationType

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)

# Loose skims
# skim = "skimmed_looseSemimuonicv1/"

# CRs and SRs
skim = "skimmed_looseSemimuonic_v2_SR"
# skim = "skimmed_looseNoBjets_lt4jets_v1_merged"

# Histograms
hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_JPsiDimuons_LooseNonLeadingMuonsVertexSegmentMatch" # all SFs
# hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_JPsiDimuons" # all SFs

# base_path = "/data/dust/user/jniedzie/ttalps_cms"
base_path = "/data/dust/user/lrygaard/ttalps_cms"

backgrounds = dasBackgrounds2018
data = "collision_data2018/SingleMuon2018"

collection = "BestDimuonVertex"
variable = "invMass"

matching_ratios = {
    "_segmentMatch0": 0.0,
    "_segmentMatch1over3": 1.0/3.0,
    "_segmentMatch3over5": 3.0/5.0,
    "": 2.0/3.0,
    "_segmentMatch3over4": 3.0/4.0,
    "_segmentMatch4over5": 4.0/5.0,
    "_segmentMatch5over6": 5.0/6.0,
    "_segmentMatch1": 1.0,
    "_segmentMatch1p5": 1.5,
}


def plot_hists(data, background, title):
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
    for bkg in background:
        bkg.SetFillStyle(1001)
        bkg.SetLineColorAlpha(ROOT.kBlack, 0.0)
        bkg.SetFillColorAlpha(ROOT.kBlue, 0.6)
    background.Draw("HIST")

    # Create an uncertainty band
    total_background = background.GetStack().Last()  # Get the total stacked histogram
    uncertainty_band = total_background.Clone("uncertainty_band")
    uncertainty_band.SetFillColorAlpha(ROOT.kGray + 3, 0.5)  # Semi-transparent gray
    uncertainty_band.SetMarkerSize(0)

    # Set the bin errors for the uncertainty band
    for bin_idx in range(1, total_background.GetNbinsX() + 1):
        bin_content = total_background.GetBinContent(bin_idx)
        bin_error = total_background.GetBinError(bin_idx)  # Total uncertainty for the bin
        uncertainty_band.SetBinContent(bin_idx, bin_content)
        uncertainty_band.SetBinError(bin_idx, bin_error)
    uncertainty_band.Draw("E2 SAME")

    # total_data = data.GetStack().Last() 
    data.SetFillStyle(1001)
    data.SetLineColorAlpha(ROOT.kBlack, 1.0)
    data.SetFillColorAlpha(ROOT.kBlue, 0.0)
    data.Draw("E1 SAME")

    max_value = max(total_background.GetMaximum(), data.GetMaximum())
    background.SetMaximum(max_value * 2)
    
    background.SetTitle(title)
    background.GetXaxis().SetTitle("Invariant Mass (GeV)")
    background.GetYaxis().SetTitle("Events")
    # background.GetXaxis().SetRangeUser(2.9, 3.0)
    canvas.Update()
    canvas.SaveAs(f"../plots/dataMCcomparisons/{title}.pdf")
    canvas.Close()


def main():

    data_MC_ratios = {}
    data_MC_ratios_uncertainty_up = {}
    data_MC_ratios_uncertainty_down = {}
    data_yields = {}
    background_yields = {}

    sfProducer = ScaleFactorProducer()
    sfProducer.setLuminosity(luminosity)

    for ratio_name, ratio in matching_ratios.items():
        print(f"--- {ratio_name} ---")

        for category in ("", "Pat", "PatDSA", "DSA"):
            if ratio_name == "_segmentMatch0" and category != "Pat":
                continue
            hist_name = f"{collection}_{category}_{variable}"
            if category == "":
                hist_name = f"{collection}_{variable}"
            histogram = Histogram(
                name=hist_name,
                title=hist_name,
                norm_type=NormalizationType.to_lumi,
                x_min=3.0,
                x_max=3.2
            )

            samples = []
            for background in backgrounds.keys():
                samples.append(
                    Sample(
                        name=background.split("/")[-1],
                        file_path=os.path.join(base_path, background, f"{skim}{ratio_name}", hist_path, "histograms.root"),
                        type=SampleType.background,
                        cross_sections=cross_sections,
                    )
                )
            samples.append(
                Sample(
                    name=data,
                    file_path=os.path.join(base_path, f"{data}_{skim}{ratio_name}_{hist_path}.root"),
                    type=SampleType.data,
                )
            )
            sfProducer.setSamples(samples)

            background_stack = sfProducer.getBackgroundStack(histogram)
            data_hist = sfProducer.getDataHist(histogram)
            plot_hists(data_hist, background_stack, f"{ratio_name}_{hist_name}_{category}")
            
            data_yield, data_uncertainty_down, data_uncertainty_up = sfProducer.getYieldAndAsymmetricUncertainties(data_hist)
            background_yield, background_uncertainty_down, background_uncertainty_up = sfProducer.getYieldAndAsymmetricUncertainties(background_stack.GetStack().Last())
            print(f"Data yields: {data_yield:.5f} pm {data_uncertainty_down:.5f} (down) pm {data_uncertainty_up:.5f} (up)")
            print(f"Background yields: {background_yield:.5f} pm {background_uncertainty_down:.5f} (down) pm {background_uncertainty_up:.5f} (up)")

            ratio,ratio_uncertainty_down,ratio_uncertainty_up = sfProducer.getDataMCRatio(data_yield, data_uncertainty_down, data_uncertainty_up, background_yield, background_uncertainty_down, background_uncertainty_up)

            print(f"Data / MC ratio: {ratio:.5f} pm {ratio_uncertainty_down:.5f} (down) pm {ratio_uncertainty_up:.5f} (up)")
            data_MC_ratios[ratio_name,category] = ratio
            data_MC_ratios_uncertainty_up[ratio_name,category] = ratio_uncertainty_up
            data_MC_ratios_uncertainty_down[ratio_name,category] = ratio_uncertainty_down
            data_yields[ratio_name,category] = [data_yield,data_uncertainty_up,data_uncertainty_down]
            background_yields[ratio_name,category] = [background_yield,background_uncertainty_up,background_uncertainty_down]
            

    # Loop over categories
    for category in ("Pat", "PatDSA", "DSA"):
        min_ratios = []
        ratios = []
        uncertainties_up = []
        uncertainties_down = []
        
        for ratio_name, minRatio in matching_ratios.items():
            if ratio_name == "_segmentMatch0" and category != "Pat":
                continue
            min_ratios.append(minRatio)
            ratios.append(data_MC_ratios[ratio_name,category])
            uncertainties_up.append(data_MC_ratios_uncertainty_up[ratio_name,category])
            uncertainties_down.append(data_MC_ratios_uncertainty_down[ratio_name,category])
            
        # Create TGraphAsymmErrors for plotting
        graph = ROOT.TGraphAsymmErrors(len(min_ratios))
        
        for i in range(len(min_ratios)):
            graph.SetPoint(i, min_ratios[i], ratios[i])
            graph.SetPointError(i, 0, 0, uncertainties_down[i], uncertainties_up[i])

        # Fit a line to the data (Linear fit)
        linear_fit_func = ROOT.TF1("linear_fit_func", "[0]*x + [1]", min(min_ratios), max(min_ratios))
        linear_fit_result = graph.Fit(linear_fit_func, "0SME")
        constant_fit_func = ROOT.TF1("linear_fit_func", "[0]", min(min_ratios), max(min_ratios))
        constant_fit_result = graph.Fit(constant_fit_func, "0SME")

        linear_err_low_0 = linear_fit_result.LowerError(0)
        linear_err_high_0 = linear_fit_result.UpperError(0)
        linear_err_low_1 = linear_fit_result.LowerError(1)
        linear_err_high_1 = linear_fit_result.UpperError(1)
        constant_err_low_0 = constant_fit_result.LowerError(0)
        constant_err_high_0 = constant_fit_result.UpperError(0)

        # Create a canvas to draw on
        canvas = ROOT.TCanvas(f"canvas_{category}", f"Data/MC Ratios for {category}", 800, 600)
        graph.SetTitle(f"Data/MC Ratios for {category}")
        graph.GetXaxis().SetTitle('Min Ratio Required')
        graph.GetYaxis().SetTitle('Data / MC Ratio')

        # Customize graph appearance
        graph.SetMarkerStyle(20)  # Circle markers
        graph.SetMarkerColor(ROOT.kBlack)  # Blue markers
        graph.SetLineColor(ROOT.kBlack)  # Line color (same as markers)
        graph.GetYaxis().SetRangeUser(0, 4.0)
        graph.GetXaxis().SetLimits(0, 1.6)
        
        # Draw the graph with errors
        graph.Draw("AP")  # "A" for axis, "P" for points

        # Plot the fit line (the function)
        linear_fit_func.SetLineColor(ROOT.kGreen+2)  # Set the fit line color to green
        linear_fit_func.Draw("SAME")  # "SAME" to draw on top of the graph
        constant_fit_func.SetLineColor(ROOT.kBlue+2)  # Set the fit line color to green
        constant_fit_func.Draw("SAME")  # "SAME" to draw on top of the graph

        # Draw a horizontal line at y = 1.0 (ideal ratio)
        hline = ROOT.TLine(min(min_ratios), 1.0, max(min_ratios), 1.0)
        hline.SetLineColor(ROOT.kBlack)
        hline.SetLineStyle(2)  # Dashed line
        hline.Draw("SAME")

        # Add the fit label as text on the plot
        linear_fit_label = f"Fit: y = ({linear_fit_result.Parameter(0):.2f} - {linear_err_low_0:.2f} + {linear_err_high_0:.2f}) x + ({linear_fit_result.Parameter(1):.2f} - {linear_err_low_1:.2f} + {linear_err_high_1:.2f})"
        constant_fit_label = f"Fit: y = ({constant_fit_result.Parameter(0):.2f} - {constant_err_low_0:.2f} + {constant_err_high_0:.2f})"

        # Add legend
        legend = ROOT.TLegend(0.5, 0.75, 0.9, 0.9)
        legend.AddEntry(graph, "Data/MC Ratio", "p")
        legend.AddEntry(linear_fit_func, linear_fit_label, "l")
        legend.AddEntry(constant_fit_func, constant_fit_label, "l")
        legend.AddEntry(hline, "Ideal Ratio (1.0)", "l")
        legend.Draw()

        # Set grid and adjust layout
        canvas.SetGrid(True)
        canvas.Update()

        # Save and show the plot
        canvas.SaveAs(f"../plots/dataMCcomparisons/data_MC_ratios_plot_{category}.png")
        canvas.Draw()

        # Clear the canvas for next category
        canvas.Clear()



if __name__ == '__main__':
  main()
