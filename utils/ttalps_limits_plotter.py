import ROOT
from math import log10, floor, ceil, sqrt
import os
from collections import defaultdict
from array import array

from TTAlpsLimitsPlotterHelper import TTAlpsLimitsPlotterHelper, BrazilGraph, SimpleGraph
from ttalps_cross_sections import get_theory_cross_section, get_cross_section_for_theory_coupling
from ttalps_luminosities import get_luminosity

# years = ["2018",]
years = ["2016preVFP","2016postVFP","2017","2018","2022preEE","2022postEE","2023preBPix","2023postBPix"]
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
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

cms_sublabel = "Preliminary"
# cms_sublabel = "Work in Progress"

# extra_str = ""
# extra_str = "_SR_ANv5"
# extra_str = "_SR_ANv6_regionBCD"
extra_str = "_SR_ANv10_regionABCD"

# PAT-PAT
# input_path = f"../limits/limits_{year_str}/results{extra_str}/limits_BestPFIsoDimuonVertex_logDxyPVTraj2_vs_logPt_Pat_ABCDpred.txt"

# PAT-DSA
# input_path = f"../limits/limits_{year_str}/results{extra_str}/limits_BestPFIsoDimuonVertex_logDxyPVTraj1_vs_logAbsCollinearityAngle_PatDSA_ABCDpred.txt"

# DSA-DSA
# input_path = f"../limits/limits_{year_str}/results{extra_str}/limits_BestPFIsoDimuonVertex_logAbsCollinearityAngle_vs_logPt_DSA_ABCDpred.txt"

# Combined
input_path = f"../limits/limits_{year_str}/results{extra_str}/limits_combined_noPatDSA.txt"
# input_path = f"../limits/limits_{year_str}/results{extra_str}/limits_combined.txt"
output_path = f"../limits/limits_{year_str}/plots{extra_str}/"

# input_path = f"../limits/limits_{year_str}/results{extra_str}/signal_injection_minus/limits_combined.txt"
# output_path = f"../limits/limits_{year_str}/plots{extra_str}/signal_injection_minus/"

if not os.path.exists(output_path):
  os.makedirs(output_path)

reference_coupling = 0.1  # this is the coupling we used to generate signal samples

expected_limits = False

# variable = "mass"
# variable = "ctau"
# variable = "mass_theory"  # assign lifetime according to theory and interpolate between ctau points
# variable = "mass_coupling"
# variable = "mass_signal_strength"
# variable = "ctau_signal_strength"
# variable = "theory_ctau_signal_strength"
# variable = "2d"
variable = "2d_contours"
# variable = "2d_contours_xsec"

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

include_exo21018 = False

include_mass_lifetime_cross_sections = False

if variable == "mass":

  include_mass_lifetime_cross_sections = True

  x_min = 0.35
  x_max = 60.0

  y_min = 1e-3
  y_max = 1e8
  if len(years) > 1:
    y_min = 1e-3
    y_max = 1e8

  x_title = "m_{a} [GeV]"
  scan_points = [1e-5, 1e0, 1e1, 1e2, 1e3]
  # scan_points = [1e-5, 1e0, 1e3]

if variable == "ctau":
  include_mass_lifetime_cross_sections = True

  y_min = 1e-3
  y_max = 1e7
  x_min = 1e-5
  x_max = 1e3
  x_title = "c#tau_{a} [mm]"
  scan_points = [0.35, 2.0, 12.0, 30.0, 60.0]
  resonances_ranges = ()

if variable == "mass_theory":
  do_boost = False

  x_min = 0.35
  x_max = 60.0

  y_min = 1e-2
  y_max = 1e7

  x_title = "m_{a} [GeV]"

y_title = "#sigma(pp #kern[-0.5]{#rightarrow} t#bar{t}a) #kern[-0.5]{#times} #kern[-0.5]{#font[12]{B}}(a #kern[-0.5]{#rightarrow} #kern[-0.5]{#mu#mu}) [pb]"

if variable == "mass_coupling":
  include_exo21018 = True
  x_min = 0.35
  x_max = 60.0

  y_min = 1e-4
  y_max = 1e8

  scan_points = [1e-5, 1e0, 1e1, 1e2, 1e3]
  x_title = "m_{a} [GeV]"
  y_title = "95% CL lower limit on g_{#Psi}^{2} #kern[-0.5]{#times} #kern[-0.5]{#font[12]{B}}(a #kern[-0.5]{#rightarrow} #kern[-0.5]{#mu#mu})"

if variable == "ctau_signal_strength":
  y_min = 1e-12
  y_max = 1e12
  x_min = 1e-13
  x_max = 1e3
  x_title = "c#tau_{a} [mm]"
  scan_points = [0.35, 2.0, 12.0, 30.0, 60.0]
  resonances_ranges = ()
  y_title = "95% CL upper limit on #mu"

if variable == "mass_signal_strength":
  x_min = 0.35
  x_max = 60.0

  y_min = 1e-2
  y_max = 1e8
  if len(years) > 1:
    y_min = 1e-4
    y_max = 1e9

  x_title = "m_{a} [GeV]"
  scan_points = [1e-5]
  y_title = "95% CL upper limit on #mu"

if variable == "theory_ctau_signal_strength":

  coupling_extr_case1 = True
  
  x_min = 0.35
  x_max = 60.0

  y_min = 1e-2
  y_max = 1e8
  if len(years) > 1:
    y_min = 1e-3
    y_max = 1e9

  x_title = "m_{a} [GeV]"
  scan_points = [0.35, 2.0, 12.0, 30.0, 60.0]
  y_title = "95% CL upper limit on g_{\Psi}^{2} #kern[-0.7]{#times} #kern[-0.6]{#font[12]{B}}(a #kern[-0.5]{#rightarrow} #kern[-0.5]{#mu#mu})"

if variable == "2d" or variable == "2d_contours" or variable == "2d_contours_xsec":

  include_pion_search = False
  run_coupling_limits = False

  x_min = log10(0.35)
  x_max = log10(60.0)

  # y_min = -5
  y_min = -5 if variable == "2d" else -3
  # y_max = 3 if variable == "2d" else 6
  y_max = 3 if variable == "2d" else 5

  z_min = -2.2
  z_max = 4.2
  if len(years) > 1:
    z_min = -2.4
    z_max = 4.2

  x_title = "log_{10}(m_{a} [GeV])"
  y_title = "log_{10}(c#tau_{a} [mm])"
  z_title = "log_{10}(95% CL upper limit on #sigma [pb])"

  if custom_axis:
    x_title = "m_{a} [GeV]"
    y_title = "c#tau_{a} [mm]"
    z_title = "#sigma(pp #kern[-0.5]{#rightarrow} t#bar{t}a) #kern[-0.5]{#times} #kern[-0.5]{#font[12]{B}}(a #kern[-0.5]{#rightarrow} #kern[-0.5]{#mu#mu}) [pb]"

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

def make_text(x, y, text, align=22, size=0.05, ndc=False):
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
  label_offset=0.3 if axis == "x" else 0.03

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

def draw_custom_y_log_labels(y_min_ = None, y_max_ = None):
  # option 1
  if not y_max_:
    y_max_ = y_max
  if not y_min_:
    y_min_ = y_min
  tick_values = []
  max_array = [1, 10, 100]
  if y_max_ == 5:
    max_array = [1, 10, 100, 1000, 10000]
  if y_max_ == 6:
    max_array = [1, 10, 100, 1000, 10000, 100000]
  min_array = [1000, 100, 10]
  if y_min_ == -5:
    min_array = [100000, 10000, 1000, 100, 10]
  for denom in min_array:
    tick_values += [i/denom for i in range(2, 11)]
  for nom in max_array:
    tick_values += [i*nom for i in range(2, 11)]
  
  label_values = [10**n for n in range(y_min_, y_max_+1)]

  return draw_axis_ticks_and_labels("y", tick_values, label_values)

def draw_custom_z_log_labels(z_min_ = None, z_max_ = None):

  if not z_min_:
    z_min_ = z_min
  if not z_max_:
    z_max_ = z_max

  palette = helper.graph_2d_exp.GetHistogram().GetListOfFunctions().FindObject("palette")
  palette.SetLabelSize(0)

  x1, x2 = palette.GetX1NDC(), palette.GetX2NDC()
  y1, y2 = palette.GetY1NDC(), palette.GetY2NDC()
  ndc_height = y2 - y1

  tick_min = int(floor(z_min_))
  tick_max = int(ceil(z_max_))
  label_exponents = [i for i in range(tick_min+1, tick_max)]
  label_values = [10**e for e in label_exponents]

  tick_values = []
  for ticks in range(tick_min, tick_max):
    base = 10 ** ticks
    for m in range(1, 10):
      v = m * base
      logv = log10(v)
      if z_min_ <= logv <= z_max_:
        tick_values.append((logv, v))
  tick_values.sort(key=lambda t: t[0])
  
  tick_long = 0.018
  tick_short = 0.013
  lines = []
  for logv, v in tick_values:
    z_ndc = y1 + (logv - z_min_) / (z_max_ - z_min_) * ndc_height
    tick_len = tick_long if abs(log10(v) - round(log10(v))) < 1e-8 else tick_short
    line = ROOT.TLine(x2 - tick_len, z_ndc, x2, z_ndc)
    line.SetNDC(True)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(1)
    line.DrawClone("same")
    lines.append(line)

  for exp in label_exponents:
    z_ndc = y1 +  (exp - z_min_) / (z_max_ - z_min_) * ndc_height
    if exp == 0:
      txt = "1"
    elif exp == 1:
      txt = "10"
    else:
      txt = f"10^{{{exp}}}"

    text = ROOT.TLatex()
    text.SetNDC(True)
    text.SetTextFont(42)
    text.SetTextSize(0.05)
    text.SetTextAlign(12)
    text.DrawLatex(x2*1.005, z_ndc, txt)
  
  ROOT.gPad.Modified()
  ROOT.gPad.Update()

def draw_legend(graphs, y_min=0.70, y_max=0.81, x_min=0.53, x_max=0.8):
  legend = ROOT.TLegend(x_min, y_min, x_max, y_max)
  legend.SetBorderSize(0)
  legend.SetFillStyle(0)
  legend.SetTextFont(42)
  legend.SetTextSize(0.04)

  for graph, title in graphs:
    legend.AddEntry(graph, title, "L")
  legend.DrawClone()


def draw_brazil_plots():

  for scan_point in scan_points:
    graph = BrazilGraph(input_path, year, x_title, y_title, x_min, x_max, y_min, y_max, True)

    theory_points = {
        0.1: [],
        1.0: [],
        # 10.0: [],
    }
    if include_mass_lifetime_cross_sections:
      theory_points[0.0] = []
    theory_graphs = {}
    colors = (ROOT.kRed, ROOT.kBlue, ROOT.kOrange+1)
    cms_red = ROOT.TColor.GetColor("#bd1f01")
    cms_green = ROOT.TColor.GetColor("#b9ac70")
    cms_orange = ROOT.TColor.GetColor("#ffa90e")
    cms_blue = ROOT.TColor.GetColor("#3f90da")

    print(f"Processing scan point: {scan_point}")

    if variable == "mass_signal_strength":
      limits = helper.get_extracted_limits_for_theory_lifetime()
    else:
      limits = helper.get_limits_for_point(variable, scan_point)

    expected_limits = {}
    for i, (x_value, r_value) in enumerate(limits.items()):
      if len(r_value) != 6:
        print(f"Invalid number of values for {x_value}: {r_value}")
        continue

      mass = x_value if "mass" in variable else scan_point
      ctau = scan_point if "mass" in variable else x_value
      scale = helper.get_scale(mass, ctau, variable)
      graph.set_point(i, x_value, r_value, scale)

      sigma_0p1 = get_theory_cross_section(mass, "2018")

      for coupling in theory_points.keys():
        if coupling == 0:
          continue
        sigma = sigma_0p1 * (coupling/0.1)**2
        key = mass if "mass" in variable else ctau
        theory_points[coupling].append((key, sigma))

      if include_mass_lifetime_cross_sections:
        sigma = get_cross_section_for_theory_coupling(mass, ctau, "Run2")
        key = mass if "mass" in variable else ctau
        theory_points[0].append((key, sigma))

    for i, (coupling, points) in enumerate(theory_points.items()):
      # leg_str = f"Theory 13 TeV, g_{{#Psi}} = {coupling}"
      leg_str = f"g_{{#Psi}} = {coupling}"
      if coupling == 0.0:
        color = cms_orange
        style = 1
        if variable == "mass":
          # leg_str = f"Theory 13 TeV, c#tau = {helper.get_ctau_label(scan_point)} mm"
          leg_str = f"c#tau_{{a}} = {helper.get_ctau_label(scan_point)}"
        if variable == "ctau":
          leg_str = f"m_{{a}} = {scan_point:.2f} GeV"
      else:
        color = cms_blue
        style = i+1
      theory_graphs[coupling] = SimpleGraph(points, leg_str, color, width=2, style=style)

    if variable == "mass_signal_strength":
      pion_graphs = helper.get_pion_graphs()
      run2_lumi_graph = helper.get_limit_graph_scaled_to_run2(limits, luminosity_run2, luminosity_run3, variable, scan_point)

    canvas = ROOT.TCanvas(f"canvas_{scan_point}", "", 800, 600)
    canvas.cd()
    canvas.SetTickx(1)
    canvas.SetTicky(1)
    canvas.SetLogx()
    canvas.SetLogy()
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)

    graph.draw()

    if variable == "mass_signal_strength":
      run2_lumi_graph.DrawClone("same")

    mask_resonances(resonances_ranges)

    legend_params = []
    if variable == "mass" or variable == "ctau":
      for theory_graph in theory_graphs.values():
        theory_graph.draw()
        legend_params.append(theory_graph.get_graph())
    if variable == "mass_coupling":
      for i, (coupling, points) in enumerate(theory_points.items()):
        # draw a dashed line at y = 1 and add it to the legend
        line = ROOT.TLine(x_min, coupling**2, x_max, coupling**2)
        line.SetLineStyle(ROOT.kDashed)
        line.SetLineColor(colors[i])
        line.SetLineWidth(2)
        line.DrawClone("same")
        legend_params.append((line, f"g_{{#Psi}} = {coupling:.1f}"))
      if include_exo21018:
        exo21018_graph = helper.get_exo21018_graph()
        exo21018_graph.SetLineColor(ROOT.kGreen+2)
        exo21018_graph.DrawClone("L same")
        graph_param = [
          (exo21018_graph, "t#bar{t}#phi, #phi#rightarrow#mu#mu,#tau#tau (EXO-21-018)"),
        ]
        draw_legend(graph_param)

    helper.draw_cms_label(cms_sublabel, 0.15)
    helper.draw_lumi_label(luminosity_run2, luminosity_run3, variable)
    if include_mass_lifetime_cross_sections:
      helper.draw_signal_label(variable, scan_point, 0.55, 0.62)
    else:
      helper.draw_signal_label(variable, scan_point)

    if "signal_strength" in variable:
      line = ROOT.TLine(x_min, 1, x_max, 1)
      line.SetLineStyle(ROOT.kDashed)
      line.SetLineColor(ROOT.kBlack)
      line.SetLineWidth(1)
      line.DrawClone("same")

    if variable == "mass_signal_strength":
      for pion_graph in pion_graphs:
        pion_graph.DrawClone("same")
        # helper.draw_pion_label()
      graph_param = [
        (run2_lumi_graph, f"Expected scaled to {luminosity_run2/1000:.0f} fb^{{-1}}"),
        (pion_graphs[0], "t#bar{t}#omega, #omega#rightarrow#pi^{-}#pi^{+}#pi^{0}, #eta BRs"),
        (pion_graphs[1], "t#bar{t}#omega, #omega#rightarrow#pi^{-}#pi^{+}#pi^{0}, #eta' BRs"),]
      draw_legend(graph_param, 0.70, 0.9, 0.52, 0.75)

    graph.draw_legend()
    tex = ROOT.TLatex(0.20, 0.83, "95% CL upper limits")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.04)
    tex.SetLineWidth(2)
    tex.DrawClone()
    if include_mass_lifetime_cross_sections:
      draw_legend(legend_params, y_min=0.66, y_max=0.82, x_min=0.55, x_max=0.72)
      tex = ROOT.TLatex(0.55, 0.83, "13 TeV theory predictions:")
      tex.SetNDC()
      tex.SetTextFont(42)
      tex.SetTextSize(0.04)
      tex.SetLineWidth(2)
      tex.DrawClone()
    else:
      draw_legend(legend_params)

    canvas.Update()
    unit = "mm" if "mass" in variable else "GeV"
    extra_str = ""
    if variable == "mass_coupling":
      extra_str = "_coupling"
    if "signal_strength" in variable:
      extra_str = "_extr_signal_strength"
    canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_{scan_point:.0e}_{unit}{extra_str}.pdf")


def draw_brazil_plots_for_theory_coupling():

  graph = BrazilGraph(input_path, year, x_title, y_title, x_min, x_max, y_min, y_max, True)

  ctau_limits_case1 = {}
  ctau_limits_case2 = {}
  coupling_over_mass_limits = {}
  over_lambda = True
  for i, scan_point in enumerate(scan_points):
    print(f"Processing scan point: {scan_point}")

    limits = helper.get_limits_for_point(variable, scan_point)
    mass = scan_point

    expected_limits = {}
    for x_value, r_value in limits.items():
      if len(r_value) != 6:
        print(f"Invalid number of values for {x_value}: {r_value}")
        continue

      ctau = x_value
      scale = helper.get_scale(mass, ctau, variable)
      expected_limits[ctau] = [r*scale for r in r_value]

    ctau_limits_case1 = helper.extract_limits_for_signal_strength1(expected_limits)
    ctau_limits_case2 = helper.find_ctau_at_r1(expected_limits)
    coupling_limits_case1 = []
    coupling_limits_case2 = []
    if not over_lambda:
      coupling_limits_case1 = [(helper.find_coupling_for_ctau(mass, False, ctau))**2 for ctau in ctau_limits_case1]
      coupling_limits_case2 = [(helper.find_coupling_for_ctau(mass, False, ctau))**2 for ctau in ctau_limits_case2]
    else: 
      coupling_limits_case1 = [helper.find_coupling_for_ctau(mass, False, ctau) for ctau in ctau_limits_case1]
      coupling_limits_case2 = [helper.find_coupling_for_ctau(mass, False, ctau) for ctau in ctau_limits_case2]
    if coupling_extr_case1:
      graph.set_point(i, mass, coupling_limits_case1, 1.0)
      coupling_over_mass_limits[mass] = coupling_limits_case1
    else:
      graph.set_point(i, mass, coupling_limits_case2, 1.0)
      coupling_over_mass_limits[mass] = coupling_limits_case2

  canvas = ROOT.TCanvas(f"canvas_{scan_point}", "", 800, 600)
  canvas.cd()
  canvas.SetLogx()
  canvas.SetLogy()
  ROOT.gPad.SetLeftMargin(0.15)
  ROOT.gPad.SetBottomMargin(0.15) 
  ROOT.gPad.SetRightMargin(0.16)

  graph.draw()

  run2_scale = (luminosity_run2 + luminosity_run3) / luminosity_run2 if luminosity_run2 != 0 else 1.0
  run2_lumi_graph = ROOT.TGraph()
  run2_lumi_graph.SetLineColor(ROOT.kViolet)
  run2_lumi_graph.SetLineWidth(2)
  run2_lumi_graph.SetLineStyle(ROOT.kDashed)
  for i, (mass, r_values) in enumerate(coupling_over_mass_limits.items()):
    run2_lumi_graph.SetPoint(i, mass, r_values[3]*run2_scale)
    print(f"{mass}, {r_values[3]*run2_scale}")
  run2_lumi_graph.DrawClone("Lsame")
  graph_params = [
    (run2_lumi_graph, f"Expected scaled to {luminosity_run2/1000:.0f} fb^{{-1}}"),
  ]

  exo21018_graph = helper.get_exo21018_graph()
  exo21018_graph.SetLineColor(ROOT.kBlue)
  exo21018_graph.DrawClone("L same")
  graph_params.append(
    (exo21018_graph, "t#bar{t}#phi, #phi#rightarrow#mu#mu (EXO-21-018)"),
  )
  draw_legend(graph_params, y_min=0.77, y_max=0.9, x_min=0.45, x_max=0.73)


  mask_resonances(resonances_ranges)

  legend_params = []
    
  helper.draw_cms_label(cms_sublabel, 0.15)
  helper.draw_lumi_label(luminosity_run2, luminosity_run3, variable)

  graph.draw_legend()
  draw_legend(legend_params)

  canvas.Update()
  case_str = "case1" if coupling_extr_case1 else "case2"
  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_extr_ctau_signal_strength_{case_str}.pdf")


def draw_brazil_plot_for_theory_lifetime():
  graph = BrazilGraph(input_path, year, x_title, y_title, x_min, x_max, y_min, y_max)

  limits = helper.get_limits_for_theory_lifetime(do_boost)
  print(limits)

  for i, (x_value, r_value) in enumerate(limits.items()):
    if len(r_value) != 6:
      print(f"Invalid number of values for {x_value}: {r_value}")
      continue

    target_coupling = 1.0
    scale = (target_coupling / reference_coupling ) ** 2

    graph.set_point(i, x_value, r_value, scale)

  pion_graphs = helper.get_pion_graphs()

  canvas = ROOT.TCanvas("canvas_theory", "", 800, 600)
  canvas.cd()
  canvas.SetLogx()
  canvas.SetLogy()
  ROOT.gPad.SetLeftMargin(0.15)
  ROOT.gPad.SetBottomMargin(0.15)

  graph.draw()
  graph.draw_legend()
  helper.draw_cms_label(cms_sublabel)
  helper.draw_lumi_label(luminosity_run2, luminosity_run3)

  for pion_graph in pion_graphs:
    pion_graph.DrawClone("same")
  graph_param = [
    (pion_graphs[0], "t#bar{t}#omega, #omega#rightarrow#pi^{-}#pi^{+}#pi^{0}, #eta BRs"),
    (pion_graphs[1], "t#bar{t}#omega, #omega#rightarrow#pi^{-}#pi^{+}#pi^{0}, #eta' BRs"),]
  draw_legend(graph_param)

  canvas.Update()
  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_theory.pdf")


def draw_brazil_plot_for_coupling():
  graph = BrazilGraph(input_path, year, x_title, y_title, x_min, x_max, y_min, y_max)

  limits = helper.get_limits_for_coupling()
  for i, (x_value, r_value) in enumerate(limits.items()):
    if len(r_value) != 6:
      print(f"Invalid number of values for {x_value}: {r_value}")
      continue

    scale = 1
    graph.set_point(i, x_value, r_value, scale)

  canvas = ROOT.TCanvas("canvas_coupling", "", 800, 600)
  canvas.cd()
  canvas.SetLogx()
  canvas.SetLogy()
  ROOT.gPad.SetLeftMargin(0.15)
  ROOT.gPad.SetBottomMargin(0.15)

  graph.draw()
  graph.draw_legend()
  helper.draw_cms_label(cms_sublabel)
  helper.draw_lumi_label(luminosity_run2, luminosity_run3)

  canvas.Update()
  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_coupling.pdf")


def draw_2d_plot():

  helper.get_2d_graph(expected=expected_limits)

  plot_name = "2d_expected" if expected_limits else "2d_observed"

  canvas = ROOT.TCanvas(f"canvas_{plot_name}", "", 800, 600)
  canvas.cd()
  ROOT.gPad.SetLeftMargin(0.11)
  ROOT.gPad.SetBottomMargin(0.15) 
  ROOT.gPad.SetRightMargin(0.16)

  helper.draw_2d_graph(x_title, y_title, z_title, x_min, x_max, y_min, y_max, z_min, z_max, custom_axis)

  mask_resonances_2d(resonances_ranges)

  ROOT.gPad.RedrawAxis()

  if custom_axis:
    draw_custom_x_log_labels()
    draw_custom_y_log_labels()
    
  helper.draw_cms_label(cms_sublabel)
  helper.draw_lumi_label(luminosity_run2, luminosity_run3)
  
  canvas.Update()

  if custom_axis:
    draw_custom_z_log_labels()

  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_{plot_name}.pdf")
  

def draw_2d_plot_with_contours():
  helper.get_2d_graph(expected=expected_limits)
  helper.get_theory_2d_graph()
  helper.get_expected_theory_ratio_graph()

  ROOT.gStyle.SetCanvasBorderMode(1)
  ROOT.gStyle.SetPadBorderMode(1)
  ROOT.gStyle.SetFrameBorderMode(1)

  plot_name = "2d_contours_expected" if expected_limits else "2d_contours_observed"

  canvas = ROOT.TCanvas(f"canvas_{plot_name}", "", 800, 700)
  canvas.cd()
  ROOT.gPad.SetLeftMargin(0.12)
  ROOT.gPad.SetBottomMargin(0.15) 
  ROOT.gPad.SetRightMargin(0.17)

  helper.draw_2d_graph(x_title, y_title, z_title, x_min, x_max, y_min, y_max, z_min, z_max, custom_axis)
  helper.draw_missing_points(custom_axis)
  canvas.RedrawAxis()

  canvas.cd()
  canvas.Modified()
  canvas.Update()

  if custom_axis:
    draw_custom_z_log_labels()
  
  canvas.Update()

  theory_name = "2d_contours_theory"
  canvas_theory = ROOT.TCanvas(f"canvas_{theory_name}", "", 800, 700)
  canvas_theory.cd()
  ROOT.gPad.SetLeftMargin(0.11)
  ROOT.gPad.SetBottomMargin(0.15) 
  ROOT.gPad.SetRightMargin(0.16)

  helper.draw_2d_theory_graph(x_title, y_title, z_title, x_min, x_max, y_min, 3, -13, 4, custom_axis)
  
  ROOT.gPad.RedrawAxis()
  if custom_axis:
    draw_custom_x_log_labels()
    draw_custom_y_log_labels(y_min, y_max)
  helper.draw_cms_label(cms_sublabel)
  helper.draw_lumi_label(luminosity_run2, luminosity_run3)
  canvas_theory.Update()
  if custom_axis:
    draw_custom_z_log_labels(-13, 4)
  canvas_theory.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_{theory_name}.pdf")

  ratio_name = "2d_contours_expected_theory_ratio"
  canvas_ratios = ROOT.TCanvas(f"canvas_{ratio_name}", "", 800, 700)
  canvas_ratios.cd()
  ROOT.gPad.SetLeftMargin(0.11)
  ROOT.gPad.SetBottomMargin(0.15) 
  ROOT.gPad.SetRightMargin(0.16)

  helper.draw_2d_theory_ratio_graphs(canvas_ratios, x_title, y_title, z_title, x_min, x_max, y_min, 3, -4, 11, custom_axis)
  
  ROOT.gPad.RedrawAxis()
  if custom_axis:
    draw_custom_x_log_labels()
    draw_custom_y_log_labels(y_min, y_max)
  helper.draw_cms_label(cms_sublabel)
  helper.draw_lumi_label(luminosity_run2, luminosity_run3)
  canvas_ratios.Update()
  if custom_axis:
    draw_custom_z_log_labels(-4, 11)
  helper.draw_2d_theory_contour_graph(canvas_ratios, x_min, x_max, y_min, y_max, expected_limits, run_coupling_limits)
  canvas_ratios.Update()
  canvas_ratios.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_{ratio_name}.pdf")

  canvas.cd()
  helper.draw_2d_theory_contour_graph(canvas, x_min, x_max, y_min, y_max)
  mask_resonances_2d(resonances_ranges)

  if include_pion_search:
    helper.draw_pion_mass_lifetime_2d_graphs()

  box = ROOT.TBox(x_min, 3, x_max, y_max)
  box.SetFillColor(ROOT.kWhite)
  box.SetFillStyle(1001)
  box.SetLineColor(ROOT.kBlack)
  box.SetLineWidth(1)
  box.DrawClone("same")

  if custom_axis:
    draw_custom_x_log_labels()
    draw_custom_y_log_labels(y_min, y_max)
    
  helper.draw_cms_label(cms_sublabel, 0.12, subpad=False)
  helper.draw_lumi_label(luminosity_run2, luminosity_run3, "2d", subpad=False)
  canvas.Modified()
  canvas.Update()
  leg_x_min = 0.17 if not include_pion_search else 0.14
  leg_x_max = 0.85 if not include_pion_search else 0.69
  legend = ROOT.TLegend(leg_x_min, 0.71, leg_x_max, 0.83)
  legend.SetFillStyle(0)
  legend.SetBorderSize(0)
  legend.SetTextSize(0.04)
  legend.SetNColumns(2)

  for idx, g in enumerate(helper.contour_graphs):
    print(idx, g.GetName() if g else "None", g.GetN() if g else "N/A")

  legend.AddEntry(0, "", "")
  legend.AddEntry(helper.contour_graphs[3], "Expected", "l")
  legend.AddEntry(0, "", "")
  legend.AddEntry(helper.contour_graphs[2], "Expected #kern[-0.5]{#pm} 1 s.d.", "l")
  legend.AddEntry(helper.contour_graphs[0], "Observed", "l")
  legend.AddEntry(helper.contour_graphs[1], "Expected #kern[-0.5]{#pm} 2 s.d.", "l")
  legend.Draw()

  if include_pion_search:
    legend2 = ROOT.TLegend(0.65, 0.75, 0.85, 0.87)
    legend2.SetFillStyle(0)
    legend2.SetBorderSize(0)
    legend2.SetTextSize(0.04)
    legend2.AddEntry(0, "", "")
    legend2.AddEntry(helper.eta_exclusion_2d_graph, "#eta BRs", "l")
    legend2.AddEntry(helper.etaprime_exclusion_2d_graph, "#eta' BRs", "l")
    legend2.Draw()
    tex = ROOT.TLatex(0.65, 0.84, "EXO-25-021:")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.04)
    tex.SetLineWidth(2)
    tex.DrawClone()

  
  tex = ROOT.TLatex(leg_x_min+0.01, 0.84, "95% CL upper limits")
  tex.SetNDC()
  tex.SetTextFont(42)
  tex.SetTextSize(0.04)
  tex.SetLineWidth(2)
  tex.DrawClone()
  tex = ROOT.TLatex(leg_x_min+0.01, 0.80, "pp #kern[-0.5]{#rightarrow} t#bar{t}a, a #kern[-0.5]{#rightarrow} #kern[-0.5]{#mu#mu}")
  tex.SetNDC()
  tex.SetTextFont(42)
  tex.SetTextSize(0.04)
  tex.SetLineWidth(2)
  tex.DrawClone()
  tex = ROOT.TLatex(leg_x_min+0.01, 0.76, "#font[12]{B}(a #kern[-0.5]{#rightarrow} #kern[-0.5]{#mu#mu}) = 1")
  tex.SetNDC()
  tex.SetTextFont(42)
  tex.SetTextSize(0.04)
  tex.SetLineWidth(2)
  tex.DrawClone()
  line = ROOT.TLine(x_min, 3, x_max, 3)
  line.SetLineColor(ROOT.kBlack)
  line.SetLineWidth(1)
  line.DrawClone("same")

  canvas.Modified()
  canvas.Update()
  pion_name = "" if not include_pion_search else "_pion"
  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_{plot_name}{pion_name}.pdf")

def draw_2d_plot_with_constant_xsec_contours():
  helper.get_2d_graph(expected=expected_limits)
  helper.get_theory_2d_graph()
  helper.get_expected_theory_ratio_graph()

  ROOT.gStyle.SetCanvasBorderMode(1)
  ROOT.gStyle.SetPadBorderMode(1)
  ROOT.gStyle.SetFrameBorderMode(1)

  plot_name = "2d_contours_xsec_expected" if expected_limits else "2d_contours_xsec_observed"

  canvas = ROOT.TCanvas(f"canvas_{plot_name}", "", 800, 600)
  canvas.cd()
  ROOT.gPad.SetLeftMargin(0.11)
  ROOT.gPad.SetBottomMargin(0.15) 
  ROOT.gPad.SetRightMargin(0.16)

  helper.draw_2d_graph(x_title, y_title, z_title, x_min, x_max, y_min, y_max, z_min, z_max, custom_axis)
  helper.draw_missing_points(custom_axis)
  canvas.RedrawAxis()

  canvas.Modified()
  canvas.Update()

  if custom_axis:
    draw_custom_z_log_labels()
  
  canvas.Update()

  hist_2d = helper.graph_2d_exp.GetHistogram()
  hist_2d_contours = hist_2d.Clone("hist_2d_contours")

  contour_levels = [log10(0.01), log10(0.1), log10(1.0), log10(10.0)]
  labels = ["10 fb", "0.1 pb", "1 pb", "10 pb"]
  
  cms_red = ROOT.TColor.GetColor("#bd1f01")
  cms_green = ROOT.TColor.GetColor("#2ca02c") 
  cms_orange = ROOT.TColor.GetColor("#ffa90e")
  cms_blue = ROOT.TColor.GetColor("#5790fc")
  colors = [cms_green, cms_blue, cms_orange, cms_red]
  was_batch = ROOT.gROOT.IsBatch()
  ROOT.gROOT.SetBatch(True)

  graphs_per_level = {}
  _keepalive = []
  for level, label, color in zip(contour_levels, labels, colors):
      hist_clone = hist_2d.Clone(f"hist_2d_contour_{label.replace(' ', '_').replace('.', 'p')}")
      hist_clone.SetContour(1, array('d', [level]))
      _keepalive.append(hist_clone)

      c_extract = ROOT.TCanvas("c_extract_tmp", "c_extract_tmp")
      hist_clone.Draw("CONT Z LIST")
      c_extract.Update()
      _keepalive.append(c_extract)

      contours = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
      level_list = contours.At(0)  # only one level now, always index 0
      graphs = []
      for j in range(level_list.GetSize()):
        g_orig = level_list.At(j)
        g_clone = g_orig.Clone()
        _keepalive.append(g_clone)
        graphs.append(g_clone)

      graphs_per_level[label] = (graphs, color)

  ROOT.gROOT.SetBatch(was_batch) 
  canvas.cd()

  legend = ROOT.TLegend(0.50, 0.75, 0.85, 0.87)
  legend.SetFillStyle(0)
  legend.SetBorderSize(0)
  legend.SetTextSize(0.04)
  for label, (graphs, color) in graphs_per_level.items():
    for g in graphs:
        g.SetLineColor(color)
        g.SetLineWidth(2)
        g.Draw("L SAME")
    if len(graphs) > 0:
        legend.AddEntry(graphs[0], f"#sigma = {label}", "l")

  mask_resonances_2d(resonances_ranges)

  box = ROOT.TBox(x_min, 3, x_max, y_max)
  box.SetFillColor(ROOT.kWhite)
  box.SetFillStyle(1001)
  box.SetLineColor(ROOT.kBlack)
  box.SetLineWidth(1)
  box.DrawClone("same")

  if custom_axis:
    draw_custom_x_log_labels()
    draw_custom_y_log_labels()
    
  helper.draw_cms_label(cms_sublabel, subpad=False)
  helper.draw_lumi_label(luminosity_run2, luminosity_run3, "2d", subpad=False)

  legend.Draw()
  canvas.Modified()
  canvas.Update()

  leg_x_min = 0.17 if not include_pion_search else 0.14
  leg_x_max = 0.85 if not include_pion_search else 0.69
  tex = ROOT.TLatex(leg_x_min+0.01, 0.84, "pp #kern[-0.5]{#rightarrow} t#bar{t}a, a #kern[-0.5]{#rightarrow} #kern[-0.5]{#mu#mu}")
  tex.SetNDC()
  tex.SetTextFont(42)
  tex.SetTextSize(0.04)
  tex.SetLineWidth(2)
  tex.DrawClone()
  tex = ROOT.TLatex(leg_x_min+0.01, 0.80, "#font[12]{B}(a #kern[-0.5]{#rightarrow} #kern[-0.5]{#mu#mu}) = 1")
  tex.SetNDC()
  tex.SetTextFont(42)
  tex.SetTextSize(0.04)
  tex.SetLineWidth(2)
  tex.DrawClone()
  line = ROOT.TLine(x_min, 3, x_max, 3)
  line.SetLineColor(ROOT.kBlack)
  line.SetLineWidth(1)
  line.DrawClone("same")

  canvas.Modified()
  canvas.Update()
  canvas.SaveAs(f"{output_path}/{input_file_name.replace('.txt', '')}_{plot_name}.pdf")

def main():
  ROOT.gROOT.SetBatch(True)

  if variable == "mass" or variable == "ctau" or variable == "mass_coupling" or variable == "mass_signal_strength" or variable == "ctau_signal_strength":
    draw_brazil_plots()
  elif variable == "mass_theory":
    draw_brazil_plot_for_theory_lifetime()
  elif variable == "theory_ctau_signal_strength":
    draw_brazil_plots_for_theory_coupling()
  elif variable == "2d":
    draw_2d_plot()
  elif variable == "2d_contours":
    draw_2d_plot_with_contours()
  elif variable == "2d_contours_xsec":
    draw_2d_plot_with_constant_xsec_contours()


if __name__ == "__main__":
  main()
