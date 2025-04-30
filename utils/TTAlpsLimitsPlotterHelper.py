import re
import ROOT
import physics
from math import pi, log10

from Logger import error
from ttalps_cross_sections import get_cross_sections, get_theory_cross_section


class TTAlpsLimitsPlotterHelper:
  def __init__(self, input_path, year):
    self.data = {}
    self.input_path = input_path

    self.__load_limits()
    self.cross_sections = get_cross_sections(year)
    self.reference_coupling = 0.1
    self.target_coupling = 1.0

  def __load_limits(self):

    pattern = re.compile(r"signal_tta_mAlp-(\d+p?\d*)GeV_ctau-(\S+)mm: \[(.*?)\]")
    pattern_alt = re.compile(r"mass_(\d+p?\d*)_ctau_([-\deEpP\.]+): \[(.*?)\]")

    with open(self.input_path, 'r') as f:
      for line in f:
        match = pattern.match(line.strip())

        if not match:
          match = pattern_alt.match(line.strip())

        if match:
          mass_str, ctau_str, values_str = match.groups()
          mass = float(mass_str.replace('p', '.'))
          ctau = float(ctau_str)
          values = list(map(float, values_str.replace("'", "").split(', ')))
          self.data[(mass, ctau)] = values

  def get_ctau_label(self, ctau):
    exponent = int(round(ROOT.TMath.Log10(ctau)))
    label = f"10^{{{exponent}}}"
    return label

  def get_central_graph(self, expected=False):
    graph = ROOT.TGraph()
    graph.SetLineColor(ROOT.kBlack)
    graph.SetLineWidth(2)
    graph.SetLineStyle(2 if expected else 1)
    return graph

  def get_band_graph(self, x_title="", y_title="", two_sigma=False):
    graph = ROOT.TGraphAsymmErrors()
    graph.SetLineWidth(0)
    graph.SetFillColorAlpha(ROOT.kYellow+1 if two_sigma else ROOT.kGreen+1, 1.0)
    graph.GetXaxis().SetTitleSize(0.05)
    graph.GetYaxis().SetTitleSize(0.05)
    graph.GetXaxis().SetLabelSize(0.04)
    graph.GetYaxis().SetLabelSize(0.04)
    graph.GetXaxis().SetTitleOffset(1.1)
    graph.GetYaxis().SetTitleOffset(1.1)
    graph.GetXaxis().SetTitle(x_title)
    graph.GetYaxis().SetTitle(y_title)

    return graph

  def get_pion_graph(self):
    pion_limits_points = [
        # mass (GeV), coupling (g)
        (0.5, 0.2262295081967213),
        (2, 1.2721311475409836),
        (4, 0.8950819672131147),
    ]

    graph = ROOT.TGraph()
    graph.SetLineColor(ROOT.kRed)
    graph.SetLineWidth(2)
    graph.SetLineStyle(1)

    for i, (mass, coupling) in enumerate(pion_limits_points):
      graph.SetPoint(i, mass, coupling)

    return graph

  def get_limits_for_point(self, variable, scan_point):
    limits = {}
    for (m, ct), values in self.data.items():
      if variable == "mass" and ct == scan_point:
        limits[m] = values
      if variable == "ctau" and m == scan_point:
        limits[ct] = values

    return limits

  def get_scale(self, mass, ctau):

    mass_string = f"{mass:.2f}" if mass < 1.0 else f"{mass:.0f}"
    mass_string = mass_string.replace(".", "p")

    ctau_string = f"{ctau:.0e}"
    ctau_string = ctau_string.replace("+0", "").replace("-0", "-")

    signal_name = f"tta_mAlp-{mass_string}GeV_ctau-{ctau_string}mm"

    sigma_ref = self.cross_sections[signal_name]
    
    # fot limits on coupling - work in progress
    # sigma_theory_0p1 = get_theory_cross_section(mass)
    # scale = sigma_ref/sigma_theory_0p1 * self.reference_coupling / self.target_coupling
    # scale = self.reference_coupling * sigma_ref

    # for limit on cross_section:
    scale = sigma_ref

    return scale

  def get_2d_graph(self, expected=False):
    self.graph_2d_exp = ROOT.TGraph2D()
    self.graph_2d_exp.SetTitle("")
    self.graph_2d_exp.SetLineColor(ROOT.kBlack)
    self.graph_2d_exp.SetLineWidth(2)
    self.graph_2d_exp.SetLineStyle(2)
    self.graph_2d_exp.SetMarkerStyle(20)
    self.graph_2d_exp.SetMarkerSize(0.5)

    for (m, ct), values in self.data.items():
      self.graph_2d_exp.SetPoint(
          self.graph_2d_exp.GetN(),
          log10(m),
          log10(ct),
          log10(self.get_scale(m, ct) * values[3 if expected else 0])
      )

    return self.graph_2d_exp

  def draw_2d_graph(self, x_title, y_title, z_title, x_min, x_max, y_min, y_max, z_min, z_max):
    self.graph_2d_exp.SetNpx(500)
    self.graph_2d_exp.SetNpy(500)

    self.graph_2d_exp.DrawClone("COLZ")

    # work in progress:
    # sigma_theory_0p1 = get_theory_cross_section(mass)

    # contour = self.graph_2d_exp.GetHistogram().Clone("contour")
    # contour.SetContour(1)  # We need 2 levels: below and above 1.0
    # contour.SetContourLevel(0, log10(1.0))

    # contour_0p2 = self.graph_2d_exp.GetHistogram().Clone("contour")
    # contour_0p2.SetContour(1)  # We need 2 levels: below and above 1.0
    # contour_0p2.SetContourLevel(0, log10(0.2))

    self.graph_2d_exp.GetHistogram().GetXaxis().SetTitle(x_title)
    self.graph_2d_exp.GetHistogram().GetYaxis().SetTitle(y_title)
    self.graph_2d_exp.GetHistogram().GetZaxis().SetTitle(z_title)

    self.graph_2d_exp.GetHistogram().GetXaxis().SetRangeUser(x_min, x_max)
    self.graph_2d_exp.GetHistogram().GetYaxis().SetRangeUser(y_min, y_max)
    self.graph_2d_exp.GetHistogram().GetZaxis().SetRangeUser(z_min, z_max)

    self.graph_2d_exp.GetHistogram().DrawClone("COLZ")

    # work in progress:
    # Overlay the contour line
    # contour.SetLineColor(ROOT.kRed)
    # contour_0p2.SetLineColor(ROOT.kYellow+1)

    # # fill contour with hashing
    # contour.SetFillStyle(3013)
    # contour.SetFillColorAlpha(ROOT.kRed, 0.5)

    # contour.DrawClone("CONT3 SAME")
    # contour_0p2.DrawClone("CONT3 SAME")

  def draw_pion_label(self):
    tex = ROOT.TLatex(0.60, 0.80, "tt+a, a #rightarrow #pi's")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.SetLineWidth(2)
    tex.SetTextColor(ROOT.kRed)
    tex.DrawClone()

  def draw_cms_label(self):
    tex = ROOT.TLatex(0.15, 0.92, "#bf{CMS} #it{Preliminary}")
    # tex = ROOT.TLatex(0.15, 0.92, "#bf{CMS}")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.SetLineWidth(2)
    tex.DrawClone()

  def draw_lumi_label(self, luminosity):
    tex = ROOT.TLatex(0.60, 0.92, f"#scale[0.8]{{pp, {luminosity/1000:.0f} fb^{{-1}} (#sqrt{{s}} = 13 TeV)}}")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.SetLineWidth(2)
    tex.DrawClone()

  def draw_signal_label(self, variable, scan_point):
    # add a label describing which signal we're looking at
    if variable == "mass":
      signal_label = f"#scale[0.8]{{c#tau = {self.get_ctau_label(scan_point)} mm}}"
    if variable == "ctau":
      signal_label = f"#scale[0.8]{{m_a = {scan_point:.2f} GeV}}"

    tex = ROOT.TLatex(0.60, 0.85, signal_label)
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.SetLineWidth(2)
    tex.DrawClone()

  def find_lifetime_for_mass(self, mass, boost, coupling=0.1, Lambda=4*pi*1000):
    ctau = physics.ctaua(mass, coupling, coupling, Lambda)  # in cm

    if boost:
      boost = 1 / mass
      if mass < 3:
        boost *= 223
      elif mass < 20:
        boost *= 230
      elif mass < 30:
        boost *= 240
      elif mass < 50:
        boost *= 260
      else:
        boost *= 296

      ctau *= boost

    ctau *= 10  # cm -> mm

    return ctau

  def get_limits_for_theory_lifetime(self, boost):

    mass_vs_ctau = {}

    for (m, ct), values in self.data.items():
      if m not in mass_vs_ctau:
        theory_ct = self.find_lifetime_for_mass(m, boost)
        mass_vs_ctau[m] = theory_ct

    limits = {}

    for mass, ctau in mass_vs_ctau.items():
      print(f"mass: {mass}, ctau: {ctau}")

      values = {}
      for (m, ct), v in self.data.items():
        if m == mass:
          values[ct] = v

      interpolated_values = self.interpolate_values(values, ctau)
      limits[mass] = interpolated_values

    return limits

  def interpolate_values(self, values, target_ctau):

    # find smallest ctau in values
    min_ctau = min(values.keys())
    max_ctau = max(values.keys())

    if target_ctau < min_ctau:
      error(f"Target ctau {target_ctau} is smaller than minimum ctau {min_ctau}")
      return values[min_ctau]

    if target_ctau > max_ctau:
      error(f"Target ctau {target_ctau} is larger than maximum ctau {max_ctau}")
      return values[max_ctau]

    # find the closest ctaus above and below the target, without knowing the order
    lower_ctau = None
    upper_ctau = None
    for ctau in values.keys():
      if ctau < target_ctau:
        if lower_ctau is None or ctau > lower_ctau:
          lower_ctau = ctau
      elif ctau > target_ctau:
        if upper_ctau is None or ctau < upper_ctau:
          upper_ctau = ctau

    lower_values = values[lower_ctau]
    upper_values = values[upper_ctau]

    # interpolate the values
    interpolated_values = []

    for i in range(len(lower_values)):
      lower_value = lower_values[i]
      upper_value = upper_values[i]

      interpolated_value = lower_value + (upper_value - lower_value) * \
          (target_ctau - lower_ctau) / (upper_ctau - lower_ctau)
      interpolated_values.append(interpolated_value)

    return interpolated_values


class BrazilGraph:
  def __init__(self, input_path, year, x_title, y_title, x_min, x_max, y_min, y_max, show_obs=False):
    self.helper = TTAlpsLimitsPlotterHelper(input_path, year)

    self.obs_graph = self.helper.get_central_graph()
    self.exp_graph = self.helper.get_central_graph(expected=True)
    self.exp_graph_1sigma = self.helper.get_band_graph()
    self.exp_graph_2sigma = self.helper.get_band_graph(x_title, y_title, two_sigma=True)

    self.show_obs = show_obs

    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max

  def set_point(self, i, x_value, r_value, scale):
    self.obs_graph.SetPoint(i, x_value, r_value[0]*scale)
    self.exp_graph.SetPoint(i, x_value, r_value[3]*scale)

    self.exp_graph_1sigma.SetPoint(i, x_value, r_value[3]*scale)
    self.exp_graph_1sigma.SetPointError(i, 0, 0, (r_value[3] - r_value[2])*scale, (r_value[4] - r_value[3])*scale)

    self.exp_graph_2sigma.SetPoint(i, x_value, r_value[3]*scale)
    self.exp_graph_2sigma.SetPointError(i, 0, 0, (r_value[3] - r_value[1])*scale, (r_value[5] - r_value[3])*scale)

  def draw(self):
    self.exp_graph_2sigma.Draw("A3")
    self.exp_graph_1sigma.Draw("3same")
    self.exp_graph.Draw("Lsame")
    if self.show_obs:
      self.obs_graph.Draw("Lsame")

    self.exp_graph_2sigma.GetXaxis().SetLimits(self.x_min, self.x_max)
    self.exp_graph_2sigma.SetMinimum(self.y_min)
    self.exp_graph_2sigma.SetMaximum(self.y_max)

  def draw_legend(self):
    legend = ROOT.TLegend(0.20, 0.65, 0.45, 0.9)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    if self.show_obs:
      legend.AddEntry(self.obs_graph, "Observed", "L")
    legend.AddEntry(self.exp_graph, "Expected", "L")
    legend.AddEntry(self.exp_graph_1sigma, "Expected #pm 1 #sigma", "F")
    legend.AddEntry(self.exp_graph_2sigma, "Expected #pm 2 #sigma", "F")
    legend.DrawClone()


class SimpleGraph:
  def __init__(self, points, title, color):
    self.graph = ROOT.TGraph()
    self.title = title
    self.graph.SetLineColor(color)

    for x, y in points:
      self.graph.SetPoint(self.graph.GetN(), x, y)

  def get_graph(self):
    return self.graph, self.title

  def draw(self):
    self.graph.DrawClone("Lsame")
