import ROOT
from math import log10

from ttalps_cross_sections import get_cross_sections
from TTAlpsLimitsPlotterHelper import TTAlpsLimitsPlotterHelper, BrazilGraph


year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)

# input_path = "../datacards/limits_BestPFIsoDimuonVertex_Pat_LxySignificance.txt"
# input_path = "../datacards/limits_BestPFIsoDimuonVertex_logLxySignificance_vs_log3Dangle_Pat_ABCDreal.txt"

input_path = "../limits/results/limits_BestPFIsoDimuonVertex_logLxySignificance_vs_log3Dangle_Pat_ABCDpred.txt"
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_dPhi_vs_logDxyPVTraj1_PatDSA_ABCDpred.txt"
# input_path = "../limits/results/limits_BestPFIsoDimuonVertex_logLxy_vs_log3Dangle_DSA_ABCDpred.txt"


output_path = "../limits/plots/"

luminosity = 59830.  # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

reference_coupling = 0.1  # this is the coupling we used to generate signal samples

variable = "mass"
# variable = "ctau"
# variable = "mass_theory"  # assign lifetime according to theory and interpolate between ctau points
# variable = "2d"

if variable == "mass":
  x_min = 0.35
  x_max = 60.0

  y_min = 1e-3
  y_max = 1e6

  x_title = "m_{a} [GeV]"
  scan_points = [1e-5, 1e0, 1e1, 1e2, 1e3]

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

y_title = "95% CL lower limit on g_{#Psi}"

if variable == "2d":

  x_min = log10(0.35)
  x_max = log10(60.0)

  y_min = -5
  y_max = 3

  z_min = -1.2
  z_max = 3

  x_title = "log_{10}(m_{a} [GeV])"
  y_title = "log_{10}(c#tau_{a} [mm])"
  z_title = "log_{10}(95% CL lower limit on signal strength r)"
  scan_points = [0.35, 1.0, 2.0, 12.0, 30.0, 60.0]


helper = TTAlpsLimitsPlotterHelper(input_path)
input_file_name = input_path.split("/")[-1]


def draw_brazil_plots():
  graph = BrazilGraph(input_path, x_title, y_title, x_min, x_max, y_min, y_max)

  for scan_point in scan_points:
    limits = helper.get_limits_for_point(variable, scan_point)
    print(limits)

    for i, (x_value, r_value) in enumerate(limits.items()):
      if len(r_value) != 6:
        print(f"Invalid number of values for {x_value}: {r_value}")
        continue

      # scale = cross_sections[name]  # TODO: implement cross section limits
      scale = reference_coupling
      graph.set_point(i, x_value, r_value, scale)

    canvas = ROOT.TCanvas(f"canvas_{scan_point}", "", 800, 600)
    canvas.cd()
    canvas.SetLogx()
    canvas.SetLogy()
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)

    graph.draw()
    graph.draw_legend()
    helper.draw_cms_label()
    helper.draw_lumi_label(luminosity)
    helper.draw_signal_label(variable, scan_point)
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
  helper.get_2d_graph(scale, expected=False)

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
