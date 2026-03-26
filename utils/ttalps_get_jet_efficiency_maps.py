from ttalps_samples_list import dasBackgrounds2016preVFP, dasBackgrounds2016postVFP, dasBackgrounds2017, dasBackgrounds2018
from ttalps_samples_list import dasBackgrounds2022preEE, dasBackgrounds2022postEE, dasBackgrounds2023preBPix, dasBackgrounds2023postBPix
from ttalps_samples_list import dasSignals2016preVFP, dasSignals2016postVFP, dasSignals2017, dasSignals2018
from ttalps_samples_list import dasSignals2022preEE, dasSignals2022postEE, dasSignals2023preBPix, dasSignals2023postBPix

from Sample import Sample, SampleType
from HistogramNormalizer import NormalizationType
from Histogram import Histogram2D

from ttalps_luminosities import get_luminosity
from ttalps_cross_sections import get_cross_sections
from Logger import info, warn, error

import os, re, array, math, json, shutil, gzip
import ROOT
from ROOT import TFile, gROOT, gStyle, TCanvas, TLatex, TH2D, TH1D

# years = ["2017","2018",]
years = ["2016preVFP","2016postVFP","2017","2018","2022preEE","2022postEE","2023preBPix","2023postBPix"]
# years = ["2018","2022preEE","2022postEE","2023preBPix","2023postBPix"]

base_path = "/data/dust/user/lrygaard/ttalps_cms"
# skim = ("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "jetMaps_ANv3")
skim = ("skimmed_looseSemimuonic_v3_SR_noBTag_merged", "SRDimuons", "jetMaps_ANv3")
hist_path = "histograms"

signals = True
if signals:
    skim = ("skimmed_looseSemimuonic_v3_SR_noBTag", "SRDimuons", "jetMaps_ANv3")


samples = {}
for year in years:
    lumi = get_luminosity(year)
    cross_sections = get_cross_sections(year)
    samples[year] = []
    datasets = globals()[f"dasBackgrounds{year}"].keys()
    if signals:
        datasets = globals()[f"dasSignals{year}"].keys()
    for dataset in datasets:
        samples[year].append(
            Sample(
                name=dataset.split("/")[-1],
                file_path=f"{base_path}/{dataset}/{skim[0]}/{hist_path}_{skim[1]}_{skim[2]}/histograms.root",
                type=SampleType.background,
                cross_sections=cross_sections,
                luminosity=lumi,
                year=year,
            )
        )

map_variables = "pt_eta"
hadron_flavours = ["B", "C", "Q"] 
hist_all_jets_2D = Histogram2D(
    name=f"GoodMediumBtaggedJets_{map_variables}",
    title=f"GoodMediumBtaggedJets {map_variables}",
    norm_type=NormalizationType.to_lumi,
)
hist_flavours = {}
for flavour in hadron_flavours:
    hist_flavours[flavour] = Histogram2D(
    name=f"GoodMediumBtaggedJets_{flavour}_{map_variables}",
    title=f"GoodMediumBtaggedJets_{flavour} {map_variables}",
    norm_type=NormalizationType.to_lumi,
)

output_path = "../data/jet_efficiency_maps"
if not os.path.exists(output_path):
    os.makedirs(output_path)

background_groups = {
    "tt": ["TTToSemiLeptonic","TTToHadronic", "TTTo2L2Nu",],
    # "tt+ST": ["ST_tW_antitop","ST_t-channel_antitop","ST_tW_top","ST_t-channel_top",],
    # "tt+X1": ["ttHTobb"],
    # "tt+X2": ["TTZH","TTTT",],
    # "tt+X3": ["ttHToNonbb","TTZToLL", "TTZZ", "TTWJetsToLNu","TTZToQQ"],
    # # "tt+H/Z": ["ttHTobb","ttHToNonbb","TTZToQQ","TTZToLL",],
    # # "ST": ["ST_tW_antitop","ST_t-channel_antitop","ST_tW_top","ST_t-channel_top",],
    # "DY+W": ["DYJetsToMuMu_M-50","DYJetsToMuMu_M-10to50","W1JetsToLNu","W2JetsToLNu","W3JetsToLNu","W4JetsToLNu",],
    # "QCD": ["QCD_Pt-120To170","QCD_Pt-170To300","QCD_Pt-300To470","QCD_Pt-470To600","QCD_Pt-600To800","QCD_Pt-800To1000","QCD_Pt-1000",],
}

def weighted_efficiency(num_hist, den_hist):
    """
    Create a TGraphAsymmErrors representing efficiency for weighted histograms.
    """
    nbins = num_hist.GetNbinsX()
    x = []
    y = []
    ex_low = []
    ex_high = []
    ey_low = []
    ey_high = []

    for i in range(1, nbins+1):
        # Weighted numerator and denominator sums
        w_num = num_hist.GetBinContent(i)
        w_den = den_hist.GetBinContent(i)
        # Sum of squared weights for error propagation
        w_num2 = num_hist.GetBinError(i)**2
        w_den2 = den_hist.GetBinError(i)**2

        # Efficiency
        eff = w_num / w_den if w_den != 0 else 0
        if eff == -0.0:
            eff = 0.0

        # Weighted error (propagation)
        if w_den != 0:
            sigma_eff = math.sqrt(w_num2 / (w_den**2) + (w_num**2 * w_den2) / (w_den**4))
        else:
            sigma_eff = 0

        # Clip errors to [0,1] boundaries
        err_up = min(sigma_eff, 1 - eff)
        err_down = min(sigma_eff, eff)

        # Bin info
        bin_center = num_hist.GetBinCenter(i)
        bin_width = num_hist.GetBinWidth(i)

        # Fill arrays
        x.append(bin_center)
        y.append(eff)
        ex_low.append(bin_width/2)
        ex_high.append(bin_width/2)
        ey_low.append(err_down)
        ey_high.append(err_up)

    # Create the graph
    g = ROOT.TGraphAsymmErrors(
        len(x),
        array.array('d', x),
        array.array('d', y),
        array.array('d', ex_low),
        array.array('d', ex_high),
        array.array('d', ey_low),
        array.array('d', ey_high)
    )
    return g

def parse_sample_name(name):
    m = re.search(r"mAlp-(.*?)GeV", name).group(1)
    c = re.search(r"ctau-(.*?)mm", name).group(1)
    return m, c

def main():
    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)

    for year in years:
        year_output_path = f"{output_path}/{year}"
        if not os.path.exists(year_output_path):
            os.makedirs(year_output_path)
        
        hist_grid = {}
        hist_grid_1D = {}
        hist_flavour_sums = {}
        hist_all_jets_sum = None
        for sample in samples[year]:

            info(f"Processing sample: {sample.name} from {sample.file_path}")
            mass = ""
            catu = ""
            if signals:
                mass, ctau = parse_sample_name(sample.name)
                hist_grid[(mass, ctau)] = {}
                hist_grid_1D[(mass, ctau)] = {}
            else:
                hist_grid[sample.name] = {}
                hist_grid_1D[sample.name] = {}

            file = TFile(sample.file_path, "READ")
            cut_flow = file.Get("cutFlow")
            sample.initial_weight_sum = cut_flow.GetBinContent(1)

            hist_all_jets_2D.load(file)
            if hist_all_jets_2D.hist is None:
                continue                

            hist_all_jets_2D.hist.Scale(sample.cross_section * sample.luminosity / sample.initial_weight_sum)
            hist_all_jets_2D.hist.Sumw2()
            nx = hist_all_jets_2D.hist.GetNbinsX() 
            x_edges = array.array('d', [hist_all_jets_2D.hist.GetXaxis().GetBinLowEdge(i+1) for i in range(nx)])
            x_edges.append(hist_all_jets_2D.hist.GetXaxis().GetBinUpEdge(nx))
            hist_all_jets_1D = TH1D(
                f"All jets 1D {sample.name}", 
                f"All jets 1D {sample.name}", 
                nx, x_edges,
            )
            for x_idx in range(1, nx+1):
                hist_all_jets_1D.SetBinContent(x_idx, hist_all_jets_2D.hist.GetBinContent(x_idx, 1))
                hist_all_jets_1D.SetBinError(x_idx, hist_all_jets_2D.hist.GetBinError(x_idx, 1))

            if signals:
                if hist_all_jets_sum is None:
                    hist_all_jets_sum = hist_all_jets_1D.Clone("hist_all_jets_sum")
                    hist_all_jets_sum.SetDirectory(0)
                else: 
                    hist_all_jets_sum.Add(hist_all_jets_1D)

            for flavour in hadron_flavours:
                hist = hist_flavours[flavour]
                hist.load(file)
                if hist.hist is None:
                    continue

                hist.hist.Scale(sample.cross_section * sample.luminosity / sample.initial_weight_sum)
                hist_1D = TH1D(
                    f"Hist 1D {sample.name} {flavour}", 
                    f"Hist 1D {sample.name} {flavour}", 
                    nx, x_edges,
                )
                for x_idx in range(1, nx+1):
                    hist_1D.SetBinContent(x_idx, hist.hist.GetBinContent(x_idx, 1))
                    hist_1D.SetBinError(x_idx, hist.hist.GetBinError(x_idx, 1))

                hist_ratio = hist.hist.Clone(f"{flavour} ratio {year} {sample.name}")
                hist_ratio.Sumw2()
                hist_ratio.SetDirectory(0)
                hist_ratio.Divide(hist_all_jets_2D.hist)
                hist_ratio.SetMinimum(0)
                hist_ratio.SetMaximum(1)
    
                hist_ratio_1D = weighted_efficiency(hist_1D, hist_all_jets_1D)

                info(f"Saving jet effiency map: {year_output_path}/{sample.name}_{flavour}_efficiency.root")
                hist_ratio.SaveAs(f"{year_output_path}/{sample.name}_{flavour}_efficiency.root")
                hist.hist.SaveAs(f"{year_output_path}/{sample.name}_{flavour}_efficiency.root")

                if signals:
                    hist_grid[(mass,ctau)][flavour] = hist_ratio
                    hist_grid_1D[(mass,ctau)][flavour] = hist_ratio_1D
                else:
                    hist_grid[sample.name][flavour] = hist_ratio
                    hist_grid_1D[sample.name][flavour] = hist_ratio_1D
            
                if signals:
                    if flavour not in hist_flavour_sums:
                        hist_flavour_sums[flavour] = hist_1D.Clone(f"{flavour}_sum")
                        hist_flavour_sums[flavour].SetDirectory(0)
                    else:
                        hist_flavour_sums[flavour].Add(hist_1D)
            
            file.Close()
        
        # assuming y (eta) only has one bin:
        first_hist = next(iter(hist_grid.values()))['B']
        ny = first_hist.GetNbinsY() 
        if ny > 1:
            continue
        nx = first_hist.GetNbinsX() 
        x_edges = array.array('d', [first_hist.GetXaxis().GetBinLowEdge(i+1) for i in range(nx)])
        x_edges.append(first_hist.GetXaxis().GetBinUpEdge(nx))
        print(f"x_edges:")
        print(x_edges)
        xmin = first_hist.GetXaxis().GetXmin()
        xmax = first_hist.GetXaxis().GetXmax()

        colors = [ROOT.kBlue+1, ROOT.kGreen+1, ROOT.kRed+1, ROOT.kGreen+3, ROOT.kRed+3, ROOT.kOrange+1, ROOT.kMagenta+1, ROOT.kAzure+1, ROOT.kPink+1]
        if signals:
            ## json efficiencies for all signals combined
            file_path = f"{output_path}/{year}_jetTagging_efficiency.json"
            if os.path.exists(file_path):
                with open(file_path) as f:
                    correction_file = json.load(f)
            else:
                correction_file = {
                    "schema_version": 2,
                    "corrections": []
                }
            
            for flavour in hadron_flavours:
                g = weighted_efficiency(hist_flavour_sums[flavour], hist_all_jets_sum)
                n = g.GetN()
                edges = []
                values = []
                for i in range(n):
                    x = g.GetX()[i]
                    y = g.GetY()[i]

                    ex_low = g.GetEXlow()[i]
                    ex_high = g.GetEXhigh()[i]

                    pt_low = x - ex_low
                    pt_high = x + ex_high

                    if i == 0:
                        edges.append(float(pt_low))
                    edges.append(float(pt_high))

                    values.append(float(y))
                
                signal_entry = {
                    "key": "tta",
                    "value": {
                        "nodetype": "binning",
                        "input": "pt",
                        "edges": edges,
                        "content": values,
                        "flow": "clamp"
                    }
                }
                correction_name = f"efficiency_{flavour}"
                correction_found = False
                for corr in correction_file["corrections"]:
                    if corr["name"] == correction_name:
                        corr["data"]["content"].append(signal_entry)
                        correction_found = True
                        break
                
                if not correction_found:
                    correction_file["corrections"].append({
                        "name": correction_name,
                        "description": f"{flavour} efficiency vs pt",
                        "version": 1,
                        "inputs": [
                            {"name": "sample", "type": "string"},
                            {"name": "pt", "type": "real"}
                        ],
                        "output": {"name": "eff", "type": "real"},
                        "data": {
                            "nodetype": "category",
                            "input": "sample",
                            "content": [signal_entry]
                        }
                    })
                                    
                with open(file_path, "w") as f:
                    json.dump(correction_file, f, indent=2)

                gz_path = file_path + ".gz"
                with open(file_path, "rb") as f_in:
                    with gzip.open(gz_path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)

            ## Plotting
            ROOT.gStyle.SetOptTitle(1)
            ROOT.gStyle.SetTitleSize(0.06, "t")
            masses = ["0p35", "2", "12", "30", "60"]
            ctaus  = ["1e-5", "1e0", "1e1", "1e2", "1e3"]
            for flavour in hadron_flavours:
                canvas = TCanvas(f"c_mass_{flavour}", "", 2000, 4000)
                canvas.Divide(1, 5)

                hists1D = []
                legends = []
                for i, mass in enumerate(masses):
                    first_plot = True
                    legend = ROOT.TLegend(0.15, 0.65, 0.6, 0.9)
                    if flavour == "B":
                        legend = ROOT.TLegend(0.15, 0.2, 0.6, 0.45)
                    legend.SetBorderSize(0)
                    legend.SetFillStyle(0)
                    legend.SetTextFont(42)
                    legend.SetTextSize(0.04)
                    canvas.cd(i+1)
                    ROOT.gPad.SetBottomMargin(0.13)
                    ROOT.gPad.SetLeftMargin(0.13)
                    for j, ctau in enumerate(ctaus):
                        hist = hist_grid[(mass, ctau)][flavour]
                        if hist:
                            hist1D = hist_grid_1D[(mass, ctau)][flavour]
                            hist1D.SetLineColor(colors[j])
                            hist1D.SetMarkerStyle(20)
                            hist1D.SetMarkerColor(colors[j])
                            hist1D.SetMarkerSize(1)
                            hist1D.SetMinimum(0)
                            hist1D.SetMaximum(1.1)
                            if first_plot:
                                hist1D.Draw("AP")
                                first_plot = False
                                hist1D.GetXaxis().SetTitle("Jet p_{T} [GeV]")
                                hist1D.GetYaxis().SetTitle("Jet tagging effiency")
                                hist1D.GetXaxis().SetLabelSize(0.06)
                                hist1D.GetYaxis().SetLabelSize(0.06)
                                hist1D.GetXaxis().SetTitleSize(0.06)
                                hist1D.GetYaxis().SetTitleSize(0.06)
                                hist1D.SetTitle(f"ALP mass {mass} GeV")
                            else:
                                hist1D.Draw("P same")
                            hists1D.append(hist1D)
                            legend.AddEntry(hist1D, f"c#tau = {ctau} mm")
                            legends.append(legend)
                            
                    legend.Draw()
                
                info(f"Saving {year_output_path}/{flavour}_signal_mass_grid.pdf")
                canvas.SaveAs(f"{year_output_path}/{flavour}_signal_mass_grid.pdf")
                canvas.Close()

                canvas = TCanvas(f"c_ctau_{flavour}", "", 24000, 80000)
                canvas.Divide(1, 5)

                hists1D = []
                legends = []
                for i, ctau in enumerate(ctaus):
                    first_plot = True
                    legend = ROOT.TLegend(0.10, 0.70, 0.6, 0.9)
                    if flavour == "B":
                        legend = ROOT.TLegend(0.10, 0.15, 0.6, 0.4)
                    legend.SetBorderSize(0)
                    legend.SetFillStyle(0)
                    legend.SetTextFont(42)
                    legend.SetTextSize(0.06)
                    canvas.cd(i+1)
                    ROOT.gPad.SetBottomMargin(0.1)
                    ROOT.gPad.SetLeftMargin(0.1)
                    for j, mass in enumerate(masses):
                        hist = hist_grid[(mass, ctau)][flavour]
                        if hist:
                            hist1D = hist_grid_1D[(mass, ctau)][flavour]
                            hist1D.SetLineColor(colors[j])
                            hist1D.SetLineWidth(1)
                            hist1D.SetMinimum(0)
                            hist1D.SetMaximum(1.1)
                            hist1D.SetTitle(f"ALP ctau {ctau} GeV")
                            if first_plot:
                                hist1D.GetXaxis().SetTitle("Jet p_{T} [GeV]")
                                hist1D.GetYaxis().SetTitle("Jet tagging effiency")
                                hist1D.GetXaxis().SetLabelSize(0.06)
                                hist1D.GetYaxis().SetLabelSize(0.06)
                                hist1D.GetXaxis().SetTitleSize(0.06)
                                hist1D.GetYaxis().SetTitleSize(0.06)
                                hist1D.Draw("AP")
                                first_plot = False
                            else:
                                hist1D.Draw("P same")
                            hists1D.append(hist1D)
                            legend.SetTextSize(0.04)
                            legend.AddEntry(hist1D, f"m_{{a}} = {mass}")
                            legends.append(legend)
                            
                        legend.Draw()
                
                info(f"Saving {year_output_path}/{flavour}_signal_ctau_grid.pdf")
                canvas.SaveAs(f"{year_output_path}/{flavour}_signal_ctau_grid.pdf")
                canvas.Close()
                
        else:
            ROOT.gStyle.SetOptTitle(1)
            ## Saving efficiencies
            corrections = []
            for flavour in hadron_flavours:
                category_content = []

                for sample in samples[year]:
                    if not hist_grid_1D[sample.name]:
                        continue
                    if not flavour in hist_grid_1D[sample.name]:
                        continue
                    g = hist_grid_1D[sample.name][flavour]
                    n = g.GetN()
                    edges = []
                    values = []
                    for i in range(n):
                        x = g.GetX()[i]
                        y = g.GetY()[i]

                        ex_low = g.GetEXlow()[i]
                        ex_high = g.GetEXhigh()[i]

                        pt_low = x - ex_low
                        pt_high = x + ex_high

                        if i == 0:
                            edges.append(float(pt_low))
                        edges.append(float(pt_high))

                        values.append(float(y))
                    
                    category_content.append({
                        "key": sample.name,
                        "value": {
                            "nodetype": "binning",
                            "input": "pt",
                            "edges": edges,
                            "content": values,
                            "flow": "clamp"
                        }
                    })
                    
                corrections.append({
                    "name": f"efficiency_{flavour}",
                    "description": f"{flavour} efficiency vs pt",
                    "version": 1,
                    "inputs": [
                        {"name": "sample", "type": "string"},
                        {"name": "pt", "type": "real"}
                    ],
                    "output": {"name": "eff", "type": "real"},
                    "data": {
                        "nodetype": "category",
                        "input": "sample",
                        "content": category_content
                    }
                })
            
            correction_file = {
                "schema_version": 2,
                "corrections": corrections
            }
                
            with open(f"{output_path}/{year}_jetTagging_efficiency.json", "w") as f:
                json.dump(correction_file, f, indent=2)

            ## Plotting
            n_samples = len(hist_grid)
            hists1D = {}
            for flavour in hadron_flavours:
                hists1D[flavour] = {}
                for group in background_groups:
                    hists1D[flavour][group] = {}
                hists1D[flavour]["other"] = {}
            
            for name, flavour_dict in hist_grid.items():
                group = next((g for g, samples in background_groups.items() if name in samples), "other")
                if group != "other":
                    for flavour, hist in flavour_dict.items():
                        hist1D = hist_grid_1D[name][flavour]
                        hists1D[flavour][group][name] = hist1D

            legends = []
            for flavour, group_dict in hists1D.items():
                n_groups = len(group_dict)
                n_others = len(group_dict["other"])
                if n_others == 0:
                    n_groups -= 1
                for group, hist_dict in group_dict.items():
                    if len(hist_dict) == 0:
                        n_groups -= 1
                canvas = TCanvas(f"c_summary_{flavour}", "", 1200, 800)
                canvas.Divide(1, n_groups)

                title = f"{flavour} jets efficiencies"
                if flavour == "Q":
                    title = f"Light jets efficiencies"
                
                i_pad = 0
                for group, hist_dict in group_dict.items():
                    
                    if len(hist_dict) == 0:
                        continue

                    canvas.cd(i_pad + 1)
                    ROOT.gPad.SetBottomMargin(0.15)
                    ROOT.gPad.SetLeftMargin(0.15)
                    hists = list(hist_dict.items())


                    # legend = ROOT.TLegend(0.65, 0.65, 0.88, 0.88)
                    legend = ROOT.TLegend(0.60, 0.20, 0.88, 0.40)
                    
                    n_samples = len(hists)

                    for i in range(0, n_samples):

                        name, hist = hists[i]

                        i_c = i
                        if i > len(colors):
                            i_c = len(colors) + i
                        color = colors[i_c]
                        hist.SetLineColor(color)

                        drawopt = "P same"
                        if i == 0:
                            drawopt = "AP"
                            hist.GetXaxis().SetTitle("Jet p_{T} [GeV]")
                            hist.GetYaxis().SetTitle("Jet tagging effiency")
                            hist.GetXaxis().SetTitleSize(0.06)
                            hist.GetXaxis().SetLabelSize(0.06)
                            hist.GetYaxis().SetTitleSize(0.06)
                            hist.GetYaxis().SetLabelSize(0.06)
                            hist.SetTitle(title)
                        hist.Draw(drawopt)

                        legend.AddEntry(hist, name, "l")

                    legend.SetTextSize(0.04)
                    legend.Draw()
                    legends.append(legend)

                    i_pad += 1


                for i, (name, hist) in enumerate(hist_dict.items()):
                    if i % 5 == 0:
                        current_pad = pad_it
                        pad_it += 1

                    canvas.cd(current_pad)

                    hist.SetLineColor(colors[i % 5])
                    hist.Draw("hist" if i % 5 == 0 else "hist same")
                canvas.SaveAs(f"{year_output_path}/{flavour}_summary_efficiency.pdf")
    
if __name__ == "__main__":
  main()
