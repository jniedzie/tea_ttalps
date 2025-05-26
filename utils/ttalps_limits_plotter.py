import ROOT
from math import log10

from TTAlpsLimitsPlotterHelper import TTAlpsLimitsPlotterHelper, BrazilGraph, SimpleGraph
from ttalps_cross_sections import get_theory_cross_section

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix

# PAT-PAT
input_path = "../limits/results/limits_BestPFIsoDimuonVertex_logAbsCollinearityAngle_vs_logPt_Pat_ABCDpred.txt"
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_invMass_vs_logDeltaSquaredIso03_Pat_ABCDpred.txt"
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_logAbsCollinearityAngle_vs_logLeadingPt_Pat_ABCDpred.txt"

# PAT-DSA
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_dPhi_vs_logDxyPVTraj1_PatDSA_ABCDpred.txt"
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_logLxy_vs_outerDR_PatDSA_ABCDpred.txt"
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_outerDR_vs_logAbsPtLxyDPhi1_PatDSA_ABCDpred.txt"

# DSA-DSA
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_logLeadingPt_vs_dPhi_DSA_ABCDpred.txt"
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_logLeadingPt_vs_dEta_DSA_ABCDpred.txt"
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_logLxySignificance_vs_outerDR_DSA_ABCDpred.txt"

# Combined
# input_path = "../limits/results/limits_combined.txt"

output_path = "../limits/plots/"

luminosity = 59830.  # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

reference_coupling = 0.1  # this is the coupling we used to generate signal samples

# variable = "mass"
# variable = "ctau"
# variable = "mass_theory"  # assign lifetime according to theory and interpolate between ctau points
variable = "2d"

if variable == "mass":
  x_min = 0.35
  x_max = 60.0

  y_min = 1e-2
  y_max = 1e6

  x_title = "m_{a} [GeV]"
  # scan_points = [1e-5, 1e0, 1e1, 1e2, 1e3]
  scan_points = [1e-5, 1e0, 1e3]

if variable == "ctau":
  y_min = 1e-3
  y_max = 1e6
  x_min = 1e-5
  x_max = 1e3
  x_title = "c#tau_{a} [mm]"
  scan_points = [0.35, 1.0, 2.0, 12.0, 30.0, 60.0]

if variable == "mass_theory":
  do_boost = True

  x_min = 0.35
  x_max = 60.0

  y_min = 1e-3
  y_max = 1e6

  x_title = "m_{a} [GeV]"

# y_title = "95% CL lower limit on g_{#Psi}"
# cross-section limit
y_title = "95% CL lower limit on #sigma [pb]"

if variable == "2d":

  x_min = log10(0.35)
  x_max = log10(60.0)

  y_min = -5
  y_max = 3

  z_min = -2.2
  z_max = 2

  x_title = "log_{10}(m_{a} [GeV])"
  y_title = "log_{10}(c#tau_{a} [mm])"
  # z_title = "log_{10}(95% CL lower limit on signal strength r)"

  # cross-section limit
  z_title = "log_{10}(95% CL lower limit on #sigma [pb])"

  scan_points = [0.35, 1.0, 2.0, 12.0, 30.0, 60.0]


helper = TTAlpsLimitsPlotterHelper(input_path, year)
input_file_name = input_path.split("/")[-1]


def mask_resonances(ranges):
  for x_min, x_max in ranges:
    # create a white box to mask the resonances
    box = ROOT.TBox(x_min, 1.1*y_min, x_max, 0.9*y_max)
    box.SetFillColor(ROOT.kWhite)
    box.SetFillStyle(1001)
    box.SetLineColor(ROOT.kWhite)
    box.SetLineWidth(0)
    box.DrawClone("same")


def draw_legend(graphs):
  legend = ROOT.TLegend(0.60, 0.60, 0.9, 0.75)
  legend.SetBorderSize(0)
  legend.SetFillStyle(0)
  legend.SetTextFont(42)
  legend.SetTextSize(0.04)

  for graph, title in graphs:
    legend.AddEntry(graph, title, "L")
  legend.DrawClone()


def draw_brazil_plots():

  for scan_point in scan_points:
    graph = BrazilGraph(input_path, year, x_title, y_title, x_min, x_max, y_min, y_max)

    theory_points = {
        # 0.1: [],
        1.0: [],
        # 10.0: [],
    }
    theory_graphs = {}
    colors = (ROOT.kRed, ROOT.kOrange+1, ROOT.kBlue)

    limits = helper.get_limits_for_point(variable, scan_point)

    for i, (x_value, r_value) in enumerate(limits.items()):
      if len(r_value) != 6:
        print(f"Invalid number of values for {x_value}: {r_value}")
        continue

      mass = x_value if variable == "mass" else scan_point
      ctau = scan_point if variable == "mass" else x_value
      scale = helper.get_scale(mass, ctau)
      graph.set_point(i, x_value, r_value, scale)

      sigma_0p1 = get_theory_cross_section(mass)

      for coupling in theory_points.keys():
        sigma = sigma_0p1 * (coupling/0.1)**2
        theory_points[coupling].append((mass, sigma))

    for i, (coupling, points) in enumerate(theory_points.items()):
      theory_graphs[coupling] = SimpleGraph(points, f"Theory, g_{{#Psi}} = {coupling}", colors[i])

    canvas = ROOT.TCanvas(f"canvas_{scan_point}", "", 800, 600)
    canvas.cd()
    canvas.SetLogx()
    canvas.SetLogy()
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)

    graph.draw()

    mask_resonances((
        (0.43, 0.49),  # K_s
        (0.52, 0.58),  # eta
        (0.73, 0.84),  # rho/omega
        (0.96, 1.08),  # phi
        (2.9, 3.3),  # J/Psi
        (3.5, 3.86),  # Psi(2S)
        (8.99, 9.87),  # Upsilon(1S)
        (9.61, 10.39),  # Upsilon(2S)
        (9.87, 10.77),  # Upsilon(3S)
    ))

    legend_params = []
    for theory_graph in theory_graphs.values():
      theory_graph.draw()
      legend_params.append(theory_graph.get_graph())

    helper.draw_cms_label()
    helper.draw_lumi_label(luminosity)
    helper.draw_signal_label(variable, scan_point)

    graph.draw_legend()
    draw_legend(legend_params)

    canvas.Update()
    unit = "mm" if variable == "mass" else "GeV"
    canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_{scan_point:.0e}_{unit}.pdf")


def draw_brazil_plot_for_theory_lifetime():
  graph = BrazilGraph(input_path, x_title, y_title, x_min, x_max, y_min, y_max)

  limits = helper.get_limits_for_theory_lifetime(do_boost)
  print(limits)

  for i, (x_value, r_value) in enumerate(limits.items()):
    if len(r_value) != 6:
      print(f"Invalid number of values for {x_value}: {r_value}")
      continue

    # scale = cross_sections[name]  # TODO: implement cross section limits
    scale = reference_coupling
    graph.set_point(i, x_value, r_value, scale)

  pion_graph = helper.get_pion_graph()

  canvas = ROOT.TCanvas("canvas_theory", "", 800, 600)
  canvas.cd()
  canvas.SetLogx()
  canvas.SetLogy()
  ROOT.gPad.SetLeftMargin(0.15)
  ROOT.gPad.SetBottomMargin(0.15)

  graph.draw()
  graph.draw_legend()
  helper.draw_cms_label()
  helper.draw_lumi_label(luminosity)

  pion_graph.DrawClone("same")
  helper.draw_pion_label()

  canvas.Update()
  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_theory.pdf")


def draw_2d_plot():

  # scale = cross_sections[name]  # TODO: implement cross section limits
  scale = reference_coupling
  helper.get_2d_graph(expected=False)

  canvas = ROOT.TCanvas("canvas_2d_expected", "", 800, 600)
  canvas.cd()
  # canvas.SetLogx()
  # canvas.SetLogy()
  # canvas.SetLogz()
  ROOT.gPad.SetLeftMargin(0.15)
  ROOT.gPad.SetBottomMargin(0.15)
  ROOT.gPad.SetRightMargin(0.15)

  helper.draw_2d_graph(x_title, y_title, z_title, x_min, x_max, y_min, y_max, z_min, z_max)

  helper.draw_cms_label()
  helper.draw_lumi_label(luminosity)

  canvas.Update()
  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_2d_expected.pdf")


def main():
  ROOT.gROOT.SetBatch(True)

  if variable == "mass" or variable == "ctau":
    draw_brazil_plots()
  elif variable == "mass_theory":
    draw_brazil_plot_for_theory_lifetime()
  elif variable == "2d":
    draw_2d_plot()


if __name__ == "__main__":
  main()
