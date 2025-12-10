import ROOT
from math import log10, floor, ceil
import os

from TTAlpsLimitsPlotterHelper import TTAlpsLimitsPlotterHelper, BrazilGraph, SimpleGraph
from ttalps_cross_sections import get_theory_cross_section
from ttalps_luminosities import get_luminosity

# years = ["2023postBPix",]
years = ["2016preVFP","2016postVFP","2017","2018","2022preEE","2022postEE","2023preBPix","2023postBPix"]

# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
# cross_sections = get_cross_sections(year)
luminosity_run2 = 0
luminosity_run3 = 0
year = years[0]
year_str = ""
for year_ in years:
  if "2016" in year_ or "2017" in year_ or "2018" in year_:
    luminosity_run2 += get_luminosity(year_)
  if "2022" in year_ or "2023" in year_:
    luminosity_run3 += get_luminosity(year_)
  year_str += year_

# extra_str = ""
extra_str = "_SR"

# PAT-PAT
# input_path = f"../limits/limits_{year_str}/results{extra_str}/limits_BestPFIsoDimuonVertex_logAbsCollinearityAngle_vs_logLeadingPt_Pat_ABCDpred.txt"

# PAT-DSA
# input_path = f"../limits/limits_{year_str}/results{extra_str}/limits_BestPFIsoDimuonVertex_logDxyPVTraj1_vs_logLeadingPt_PatDSA_ABCDpred.txt"

# DSA-DSA
# input_path = f"../limits/limits_{year_str}/results{extra_str}/limits_BestPFIsoDimuonVertex_logPt_vs_logInvMass_DSA_ABCDpred.txt"

# Combined
input_path = f"../limits/limits_{year_str}/results{extra_str}/limits_combined_DSA.txt"

output_path = f"../limits/limits_{year_str}/plots{extra_str}_test/"

if not os.path.exists(output_path):
  os.makedirs(output_path)

reference_coupling = 0.1  # this is the coupling we used to generate signal samples

expected_limits = True

# variable = "mass"
# variable = "ctau"
# variable = "mass_theory"  # assign lifetime according to theory and interpolate between ctau points
variable = "2d"

custom_axis = True

resonances_ranges = (
    # (0.43, 0.49),  # K_s
    # (0.52, 0.58),  # eta
    # (0.73, 0.84),  # rho/omega
    # (0.96, 1.08),  # phi
    # (2.9, 3.3),  # J/Psi
    # (3.5, 3.86),  # Psi(2S)
    (2.4, 3.9),  # J/Psi + Psi(2S)
    # (8.99, 9.87),  # Upsilon(1S)
    # (9.61, 10.39),  # Upsilon(2S)
    # (9.87, 10.77),  # Upsilon(3S)
)

if variable == "mass":
  x_min = 0.35
  x_max = 60.0

  y_min = 1e-2
  y_max = 1e6
  if len(years) > 1:
    y_min = 1e-4
    y_max = 1e5

  x_title = "m_{a} [GeV]"
  scan_points = [1e-5, 1e0, 1e1, 1e2, 1e3]
  # scan_points = [1e-5, 1e0, 1e3]

if variable == "ctau":
  y_min = 1e-3
  y_max = 1e6
  x_min = 1e-5
  x_max = 1e3
  x_title = "c#tau_{a} [mm]"
  scan_points = [0.35, 2.0, 12.0, 30.0, 60.0]
  resonances_ranges = ()

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
  if len(years) > 1:
    z_min = -3.4
    z_max = 1.6

  x_title = "log_{10}(m_{a} [GeV])"
  y_title = "log_{10}(c#tau_{a} [mm])"
  z_title = "log_{10}(95% CL lower limit on #sigma [pb])"

  # z_title = "log_{10}(95% CL lower limit on signal strength r)"
  if custom_axis:
    x_title = "m_{a} [GeV]"
    y_title = "c#tau_{a} [mm]"
    z_title = "95% CL lower limit on #sigma [pb]"

  # cross-section limit

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

def mask_resonances_2d(ranges):
  for x_min, x_max in ranges:
    print(f"{x_min}-{x_max}")
    # create a white box to mask the resonances
    box = ROOT.TBox(log10(x_min), y_min, log10(x_max), y_max)
    box.SetFillColor(ROOT.kWhite)
    box.SetFillStyle(1001)
    box.SetLineColor(ROOT.kWhite)
    box.SetLineWidth(0)
    box.DrawClone("same")

def make_line(x1, y1, x2, y2, ndc=False, width=1, color=ROOT.kBlack):
  line = ROOT.TLine(x1, y1, x2, y2)
  if ndc:
      line.SetNDC(True)
  line.SetLineColor(color)
  line.SetLineWidth(width)
  line.DrawClone("same")
  return line

def make_text(x, y, text, align=22, size=0.04, ndc=False):
  t = ROOT.TLatex(x, y, text)
  if ndc:
      t.SetNDC(True)
  t.SetTextFont(42)
  t.SetTextAlign(align)
  t.SetTextSize(size)
  t.DrawClone("same")
  return t

def draw_axis_ticks_and_labels(axis, tick_values, label_values):
  logs = [log10(v) for v in tick_values]
  log_labels = [log10(v) for v in label_values]
  texts = []
  lines = []

  tick_long=0.3 if axis == "x" else 0.07
  tick_short=0.2 if axis == "x" else 0.04
  label_offset=0.2 if axis == "x" else 0.03

  # axis line
  if axis == "x":
    lines.append(make_line(x_min, y_min, x_max, y_min))
    lines.append(make_line(x_min, y_max, x_max, y_max))
  else:
    lines.append(make_line(x_min, y_min, x_min, y_max))
    lines.append(make_line(x_max, y_min, x_max, y_max))
  
  # tick marks
  for logv, linear_v in zip(logs, tick_values):
    height = tick_long if linear_v in label_values else tick_short
    if axis == "x":
        lines.append(make_line(logv, y_min, logv, y_min + height))
        lines.append(make_line(logv, y_max - height, logv, y_max))
    else:
        lines.append(make_line(x_min, logv, x_min + height, logv))
        lines.append(make_line(x_max - height, logv, x_max, logv))

  # axis labels
  for logv, linear_v in zip(log_labels, label_values):
    if axis == "x":
      texts.append(make_text(logv, y_min - label_offset, f"{linear_v:g}", align=22))
    else:
      if logv == 0:
        label = "1"
      elif linear_v == 10:
        label = "10"
      else:
        exponent = int(logv)
        label = f"10^{{{exponent}}}"
      texts.append(make_text(x_min - 0.03, logv, label, align=32))

  return lines, texts
  
def draw_custom_x_log_labels():
  # option 1
  # tick_values = [0.35, 2, 12, 30, 60]
  # label_values = [0.35, 2, 12, 30, 60]
  # option 2
  tick_values = (
    [i/10 for i in range(4, 11)] +
    list(range(2, 11)) +
    list(range(20, 61, 10))
  )
  label_values = [1.0, 10,]

  return draw_axis_ticks_and_labels("x", tick_values, label_values)

def draw_custom_y_log_labels():
  # option 1
  tick_values = []
  for denom in [100000, 10000, 1000, 100, 10]:
    tick_values += [i/denom for i in range(2, 11)]
  for nom in [1, 10, 100]:
    tick_values += [i*nom for i in range(2, 11)]
  
  label_values = [10**n for n in range(y_min, y_max+1)]

  return draw_axis_ticks_and_labels("y", tick_values, label_values)

def draw_custom_z_log_labels():

  palette = helper.graph_2d_exp.GetHistogram().GetListOfFunctions().FindObject("palette")
  palette.SetLabelSize(0)

  x1, x2 = palette.GetX1NDC(), palette.GetX2NDC()
  y1, y2 = palette.GetY1NDC(), palette.GetY2NDC()
  ndc_height = y2 - y1

  tick_min = int(floor(z_min))
  tick_max = int(ceil(z_max))
  label_exponents = [i for i in range(tick_min+1, tick_max)]
  label_values = [10**e for e in label_exponents]

  tick_values = []
  for ticks in range(tick_min, tick_max):
    base = 10 ** ticks
    for m in range(1, 10):
      v = m * base
      logv = log10(v)
      if z_min <= logv <= z_max:
        tick_values.append((logv, v))
  tick_values.sort(key=lambda t: t[0])
  
  tick_long = 0.018
  tick_short = 0.013
  lines = []
  for logv, v in tick_values:
    z_ndc = y1 + (logv - z_min) / (z_max - z_min) * ndc_height
    tick_len = tick_long if abs(log10(v) - round(log10(v))) < 1e-8 else tick_short
    line = ROOT.TLine(x2 - tick_len, z_ndc, x2, z_ndc)
    line.SetNDC(True)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(1)
    line.DrawClone("same")
    lines.append(line)

  for exp in label_exponents:
    z_ndc = y1 +  (exp - z_min) / (z_max - z_min) * ndc_height
    if exp == 0:
      txt = "1"
    elif exp == 1:
      txt = "10"
    else:
      txt = f"10^{{{exp}}}"

    text = ROOT.TLatex()
    text.SetNDC(True)
    text.SetTextFont(42)
    text.SetTextSize(0.04)
    text.SetTextAlign(12)
    text.DrawLatex(x2*1.005, z_ndc, txt)
  
  ROOT.gPad.Modified()
  ROOT.gPad.Update()

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
        key = mass if variable == "mass" else ctau
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

    mask_resonances(resonances_ranges)

    legend_params = []
    if variable == "mass":
      for theory_graph in theory_graphs.values():
        theory_graph.draw()
        legend_params.append(theory_graph.get_graph())

    helper.draw_cms_label()
    helper.draw_lumi_label(luminosity_run2, luminosity_run3)
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
  helper.draw_lumi_label(luminosity_run2, luminosity_run3)

  pion_graph.DrawClone("same")
  helper.draw_pion_label()

  canvas.Update()
  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_theory.pdf")


def draw_2d_plot():

  # scale = cross_sections[name]  # TODO: implement cross section limits
  scale = reference_coupling
  helper.get_2d_graph(expected=expected_limits)

  plot_name = "2d_expected" if expected_limits else "2d_observed"

  canvas = ROOT.TCanvas(f"canvas_{plot_name}", "", 800, 600)
  canvas.cd()
  # canvas.SetLogx()
  # canvas.SetLogy()
  # canvas.SetLogz()
  ROOT.gPad.SetLeftMargin(0.15)
  ROOT.gPad.SetBottomMargin(0.15) 
  ROOT.gPad.SetRightMargin(0.15)

  helper.draw_2d_graph(x_title, y_title, z_title, x_min, x_max, y_min, y_max, z_min, z_max, custom_axis)

  mask_resonances_2d(resonances_ranges)

  ROOT.gPad.RedrawAxis()

  if custom_axis:
    draw_custom_x_log_labels()
    draw_custom_y_log_labels()
    
  helper.draw_cms_label()
  helper.draw_lumi_label(luminosity_run2, luminosity_run3)

  canvas.Update()

  if custom_axis:
    draw_custom_z_log_labels()

  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_{plot_name}.pdf")


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
