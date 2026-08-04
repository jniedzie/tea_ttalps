import re
import ROOT
import physics
from math import pi, log10, floor, ceil, sqrt
import array
import ctypes
from collections import defaultdict
from scipy.optimize import brentq
import numpy as np
from scipy.ndimage import uniform_filter1d

from Logger import error, warn
from ttalps_cross_sections import get_cross_sections, get_theory_cross_section, get_cross_section_scales, get_cross_section_for_theory_coupling


class TTAlpsLimitsPlotterHelper:
  def __init__(self, input_path, year):
    self.data = {}
    self.input_path = input_path

    self.__load_limits()
    self.cross_sections = get_cross_sections(year)
    self.reference_coupling = 0.1
    self.target_coupling = 1.0
    self.missing_points = []

    self.theory_lifetimes_for_coupling1p0 = {
      0.35: 0.1327277591964898, 
      2: 0.0038540172431162684, 
      12: 9.357205773942406e-09, 
      30: 2.753518824189904e-09, 
      60: 1.292235496234161e-09
    }

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
          if values_str != "":
            values = list(map(float, values_str.replace("'", "").split(', ')))
          else:
            values = []
          self.data[(mass, ctau)] = values

  def get_ctau_label(self, ctau):
    labels = {
      1e-5: "10 nm",
      1e0: "1 mm",
      1e1: "1 cm",
      1e2: "10 cm",
      1e3: "1 m",
    }
    # exponent = int(round(ROOT.TMath.Log10(ctau)))
    # label = f"10^{{{exponent}}}"
    return labels[ctau]

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

  def get_exo21018_graph(self):
    coupling_limits = {
      15.0: 0.0037017,
      15.5: 0.0035153,
      16.0: 0.0051587,
      16.5: 0.0025269,
      17.0: 0.0025644,
      17.5: 0.0029029,
      18.0: 0.0030174,
      18.5: 0.0038216,
      19.0: 0.0042739,
      19.5: 0.0037116,
      20.0: 0.0030868,
      20.5: 0.0046723,
      21.0: 0.0041074,
      21.5: 0.0017149,
      22.0: 0.0024004,
      22.5: 0.0042661,
      23.0: 0.0053544,
      23.5: 0.0072175,
      24.0: 0.0059043,
      24.5: 0.0036559,
      25.0: 0.0028737,
      25.5: 0.0020106,
      26.0: 0.002358,
      26.5: 0.0033718,
      27.0: 0.0042617,
      27.5: 0.0024807,
      28.0: 0.0017901,
      28.5: 0.0024166,
      29.0: 0.0027431,
      29.5: 0.0035219,
      30.0: 0.0030153,
      30.5: 0.0028974,
      31.0: 0.0031295,
      31.5: 0.003978,
      32.0: 0.0042664,
      32.5: 0.0029895,
      33.0: 0.0030195,
      33.5: 0.0022422,
      34.0: 0.0022203,
      34.5: 0.0024249,
      35.0: 0.0024831,
      35.5: 0.0031115,
      36.0: 0.0028899,
      36.5: 0.0024703,
      37.0: 0.0022962,
      37.5: 0.0018753,
      38.0: 0.0019203,
      38.5: 0.0017209,
      39.0: 0.0020612,
      39.5: 0.0021191,
      40.0: 0.0019945,
      40.5: 0.0018932,
      41.0: 0.0020409,
      41.5: 0.0022351,
      42.0: 0.0019341,
      42.5: 0.0025024,
      43.0: 0.0025802,
      43.5: 0.0023542,
      44.0: 0.0024162,
      44.5: 0.0022353,
      45.0: 0.002275,
      45.5: 0.0023348,
      46.0: 0.0029825,
      46.5: 0.0031132,
      47.0: 0.0032038,
      47.5: 0.0029442,
      48.0: 0.0025693,
      48.5: 0.0025039,
      49.0: 0.0021604,
      49.5: 0.0026547,
      50.0: 0.0047564,
      50.5: 0.0045926,
      51.0: 0.0089459,
      51.5: 0.0074443,
      52.0: 0.0076749,
      52.5: 0.0075276,
      53.0: 0.00577,
      53.5: 0.0069219,
      54.0: 0.0050376,
      54.5: 0.0057734,
      55.0: 0.0050137,
      55.5: 0.0046349,
      56.0: 0.0039359,
      56.5: 0.0041126,
      57.0: 0.003878,
      57.5: 0.004691,
      58.0: 0.0053457,
      58.5: 0.00627,
      59.0: 0.0073927,
      59.5: 0.0081154,
      60.0: 0.0098574,
    }
    # coupling_limits = {
    #   15: 15.4,
    #   20: 11.6,
    #   25: 9.0,
    #   30: 6.4,
    #   40: 3.1,
    #   50: 2.3,
    #   60: 2.1,
    # }
    graph = ROOT.TGraph()
    graph.SetLineColor(ROOT.kGreen+2)
    graph.SetLineWidth(2)
    graph.SetLineStyle(1)
    for i, (mass, coupling) in enumerate(coupling_limits.items()):
      graph.SetPoint(i, mass, coupling)
    return graph

  def draw_pion_mass_lifetime_2d_graphs(self, y_min = -5):

    lumi_scale = 138 / (138+62)
    # eta BRs: 27%
    pion_limits_r_points_eta = [
        # mass (GeV), signal strengh, lifetime [mm], theoretical cross sections [pb]
        (0.5,  0.04,  8.172e-02,  0.504),
        (0.75, 0.20,  5.144e-02,  0.508),
        (1,    0.65,  3.787e-02,  0.523),
        (1.5,  3.38,  6.387e-03,  0.536),
        (2,    10.8,  3.854e-03,  0.534),
        (3,    3.1,   3.820e-05,  0.533),
        (4,    2.2,   1.566e-05,  0.529),
    ]
    pion_limits_scaled_eta = [
      (m, r*0.27*lumi_scale, ct, xs)
      for m, r, ct, xs in pion_limits_r_points_eta
    ]
    # etaprime BRs: 69%
    pion_limits_r_points_etaprime = [
        # mass (GeV), signal strengh, lifetime [mm], theoretical cross sections [pb]
        (0.85, 0.01,  4.496e-02,  0.502),
        (1,    0.05,  3.787e-02,  0.523),
        (1.5,  0.24,  6.387e-03,  0.536),
        (2,    0.37,  3.854e-03,  0.534),
        (3,    0.52,  3.820e-05,  0.533),
        (4,    0.28,  1.566e-05,  0.529),
    ]
    pion_limits_scaled_etaprime = [
      (m, r*0.69*lumi_scale, ct, xs)
      for m, r, ct, xs in pion_limits_r_points_etaprime
    ]

    eta_masses = np.array([p[0] for p in pion_limits_scaled_eta])
    eta_rs     = np.array([p[1] for p in pion_limits_scaled_eta])
    eta_ctaus  = np.array([p[2] for p in pion_limits_scaled_eta])
    eta_boundary_points_mass = []
    eta_boundary_points_ctau = []

    etaprime_masses = np.array([p[0] for p in pion_limits_scaled_etaprime])
    etaprime_rs     = np.array([p[1] for p in pion_limits_scaled_etaprime])
    etaprime_ctaus  = np.array([p[2] for p in pion_limits_scaled_etaprime])
    etaprime_boundary_points_mass = []
    etaprime_boundary_points_ctau = []

    for i in range(len(eta_rs) - 1):
      if (eta_rs[i] - 1) * (eta_rs[i+1] - 1) < 0:  # sign change -> crossing
        # log-interpolate in mass and ctau
        frac = (1 - eta_rs[i]) / (eta_rs[i+1] - eta_rs[i])  # linear in r
        m_cross = eta_masses[i] + frac * (eta_masses[i+1] - eta_masses[i])
        ct_cross = np.exp(
            np.log(eta_ctaus[i]) + frac * (np.log(eta_ctaus[i+1]) - np.log(eta_ctaus[i]))
        )
        eta_boundary_points_mass.append(m_cross)
        eta_boundary_points_ctau.append(ct_cross)
    
    for i in range(len(etaprime_rs) - 1):
      if (etaprime_rs[i] - 1) * (etaprime_rs[i+1] - 1) < 0:  # sign change -> crossing
        # log-interpolate in mass and ctau
        frac = (1 - etaprime_rs[i]) / (etaprime_rs[i+1] - etaprime_rs[i])  # linear in r
        m_cross = etaprime_masses[i] + frac * (etaprime_masses[i+1] - etaprime_masses[i])
        ct_cross = np.exp(
            np.log(etaprime_ctaus[i]) + frac * (np.log(etaprime_ctaus[i+1]) - np.log(etaprime_ctaus[i]))
        )
        etaprime_boundary_points_mass.append(m_cross)
        etaprime_boundary_points_ctau.append(ct_cross)

    # Mark excluded segment (r < 1)
    eta_excl = [(m, ct) for m, r, ct, xs in pion_limits_scaled_eta if r < 1]
    eta_excl_with_boundary = eta_excl + list(zip(eta_boundary_points_mass, eta_boundary_points_ctau))
    eta_excl_with_boundary.sort()
    eta_m_first, eta_ct_first = eta_excl_with_boundary[0]
    eta_m_last, eta_ct_last = eta_excl_with_boundary[-1]
    eta_excl_closed = [(eta_m_first, 10**y_min)] + eta_excl_with_boundary + [(eta_m_last, 10**y_min)]

    etaprime_excl = [(m, ct) for m, r, ct, xs in pion_limits_scaled_etaprime if r < 1]
    etaprime_excl_with_boundary = etaprime_excl + list(zip(etaprime_boundary_points_mass, etaprime_boundary_points_ctau))
    etaprime_excl_with_boundary.sort()
    etaprime_m_first, etaprime_ct_first = etaprime_excl_with_boundary[0]
    etaprime_m_last, etaprime_ct_last = etaprime_excl_with_boundary[-1]
    etaprime_excl_closed = [(etaprime_m_first, 10**y_min)] + etaprime_excl_with_boundary + [(etaprime_m_last, 10**y_min)]

    self.eta_exclusion_2d_graph = ROOT.TGraph(len(eta_excl_closed))
    self.etaprime_exclusion_2d_graph = ROOT.TGraph(len(etaprime_excl_closed))
    for i, (m, ct) in enumerate(eta_excl_closed):
        self.eta_exclusion_2d_graph.SetPoint(i, log10(m), log10(ct))
    self.eta_exclusion_2d_graph.SetLineStyle(1)
    self.eta_exclusion_2d_graph.SetLineWidth(2)
    self.eta_exclusion_2d_graph.SetLineColor(ROOT.kBlue)
    self.eta_exclusion_2d_graph.Draw("L SAME")
    for i, (m, ct) in enumerate(etaprime_excl_closed):
        self.etaprime_exclusion_2d_graph.SetPoint(i, log10(m), log10(ct))
    self.etaprime_exclusion_2d_graph.SetLineStyle(2)
    self.etaprime_exclusion_2d_graph.SetLineWidth(2)
    self.etaprime_exclusion_2d_graph.SetLineColor(ROOT.kBlue)
    self.etaprime_exclusion_2d_graph.Draw("L SAME")

  def get_pion_graphs(self):
    
    # eta BRs: 27%
    pion_limits_r_points_eta = [
        # mass (GeV), signal strengh, lifetime [mm], theoretical cross sections [pb]
        (0.5,  0.04,  8.172e-02,  0.504),
        (0.75, 0.20,  5.144e-02,  0.508),
        (1,    0.65,  3.787e-02,  0.523),
        (1.5,  3.38,  6.387e-03,  0.536),
        (2,    10.8,  3.854e-03,  0.534),
        (3,    3.1,   3.820e-05,  0.533),
        (4,    2.2,   1.566e-05,  0.529),
    ]
    # etaprime BRs: 69%
    pion_limits_r_points_etaprime = [
        # mass (GeV), signal strengh, lifetime [mm], theoretical cross sections [pb]
        (0.85, 0.01,  4.496e-02,  0.502),
        (1,    0.05,  3.787e-02,  0.523),
        (1.5,  0.24,  6.387e-03,  0.536),
        (2,    0.37,  3.854e-03,  0.534),
        (3,    0.52,  3.820e-05,  0.533),
        (4,    0.28,  1.566e-05,  0.529),
    ]
  
    graphs = []
    graph_eta = ROOT.TGraph()
    graph_eta.SetLineColor(ROOT.kRed)
    graph_eta.SetLineWidth(2)
    graph_eta.SetLineStyle(1)
    graph_etaprime = ROOT.TGraph()
    graph_etaprime.SetLineColor(ROOT.kBlue)
    graph_etaprime.SetLineWidth(2)
    graph_etaprime.SetLineStyle(1)

    for i, (mass, value) in enumerate(pion_limits_r_points_eta):
      graph_eta.SetPoint(i, mass, value)

    for i, (mass, value) in enumerate(pion_limits_r_points_etaprime):
      graph_etaprime.SetPoint(i, mass, value)

    return [graph_eta, graph_etaprime]

  def get_limits_for_point(self, variable, scan_point):
    limits = {}
    for (m, ct), values in self.data.items():
      if "mass" in variable and ct == scan_point:
        limits[m] = values
      elif m == scan_point:
        limits[ct] = values

    return limits

  def get_extracted_limits_for_theory_lifetime(self):
    limits = {}

    mass_list = defaultdict(list)

    for (m, ct), values in self.data.items():
        mass_list[m].append(
            (float(ct), [float(v) for v in values])
        )

    for m, ct_values in mass_list.items():
        ct_values.sort(key=lambda x: x[0])

        lifetime = self.theory_lifetimes_for_coupling1p0[m]

        if lifetime <= ct_values[0][0]:
            limits[m] = ct_values[0][1]
            continue

        if lifetime >= ct_values[-1][0]:
            limits[m] = ct_values[-1][1]
            continue

        for i in range(len(ct_values) - 1):
            ct1, values1 = ct_values[i]
            ct2, values2 = ct_values[i + 1]

            if ct1 <= lifetime <= ct2:
                # interpolate in log(ct)
                x1 = log10(ct1)
                x2 = log10(ct2)
                x  = log10(lifetime)
                frac = (x - x1) / (x2 - x1)

                limits[m] = [
                    values1[j] + frac * (values2[j] - values1[j])
                    for j in range(len(values1))
                ]
                break

    return limits

  def get_scale(self, mass, ctau, variable):

    mass_string = f"{mass:.2f}" if mass < 1.0 else f"{mass:.0f}"
    mass_string = mass_string.replace(".", "p")

    ctau_string = f"{ctau:.0e}"
    ctau_string = ctau_string.replace("+0", "").replace("-0", "-")

    signal_name = f"tta_mAlp-{mass_string}GeV_ctau-{ctau_string}mm"

    if "signal_strength" in variable:
      scale_ref = get_cross_section_scales(mass, ctau)
      return scale_ref

    sigma_ref = self.cross_sections[signal_name]
    
    # fot limits on coupling - work in progress
    if variable == "mass_coupling":
      sigma_theory_0p1 = get_theory_cross_section(mass, "Run2")
      scale = self.reference_coupling**2 * sigma_ref / sigma_theory_0p1

    else:
      scale = sigma_ref

    return scale

  def get_nan_invalid_points(self):
    masses = sorted(set(m for (m, ct) in self.data.keys()))
    ctaus = sorted(set(ct for (m, ct) in self.data.keys()))
    nan_points = []

    nan_corner_point = (-1,-1)
    nan_corner_mass_idx = -1
    nan_corner_ctau_idx = -1
    if (masses[len(masses)-1],ctaus[0]) in self.missing_points:
      nan_corner_point = (masses[len(masses)-1], ctaus[0])
      nan_corner_mass_idx = len(masses)-1
      nan_corner_ctau_idx = 0

    if (masses[0],ctaus[0]) in self.missing_points:
      nan_points.append((masses[0], ctaus[0]))

    for (m1, ct1) in self.missing_points:
      mass_neighbour = False
      ctau_neighbour = False
      m_idx1 = masses.index(m1)
      ct_idx1 = ctaus.index(ct1)
      if (m1, ct1) == nan_corner_point:
        nan_points.append((m1, ct1))
        continue
      if m1 == nan_corner_point[0] and abs(ct_idx1 - nan_corner_ctau_idx) == 1:
        nan_points.append((m1, ct1))
        continue
      if ct1 == nan_corner_point[1] and abs(m_idx1 - nan_corner_mass_idx) == 1:
          nan_points.append((m1, ct1))
          continue
      
      for (m2, ct2) in self.missing_points:
        if (m1, ct1) == (m2, ct2):
          continue
        if (m2, ct2) in nan_points:
          continue
        m_idx2 = masses.index(m2)
        ct_idx2 = ctaus.index(ct2)
        if m1 == m2 and abs(ct_idx1 - ct_idx2) == 1:
            ctau_neighbour == True
        if ct1 == ct2 and abs(m_idx1 - m_idx2) == 1:
            mass_neighbour == True
      
      if mass_neighbour and ctau_neighbour:
        nan_points.append((m1, ct1))

    print(f"nan_points:")
    for (m,ct) in nan_points:
      print(f"{m=}, {ct}")
    return nan_points

  def get_2d_graph(self, expected=False):
    self.graph_2d_data = []
    n_values = len(next(iter(self.data.values())))
    for i in range(0, n_values):
      graph = ROOT.TGraph2D()
      graph.SetTitle("")
      graph.SetLineColor(ROOT.kBlack)
      graph.SetLineWidth(2)
      graph.SetLineStyle(2)
      graph.SetMarkerStyle(20)
      graph.SetMarkerSize(0.5)
      self.graph_2d_data.append(graph)

    for (m, ct), values in self.data.items():
      if len(values) < 4:
          warn(f"Point ({m}, {ct}) is missing - skipping")
          self.missing_points.append((m, ct))
          continue
      else:
        for i in range(0, n_values):
          point = log10(self.get_scale(m, ct, "2d") * values[i])
          # point = log10(self.get_scale(m, ct, "2d") * values[3 if expected else 0])

          self.graph_2d_data[i].SetPoint(
              self.graph_2d_data[i].GetN(),
              log10(m),
              log10(ct),
              point
          )
    
    self.graph_2d_exp = self.graph_2d_data[3 if expected else 0]
    nan_points = self.get_nan_invalid_points()
    for (m, ct) in nan_points:
      point = float('nan')
      self.graph_2d_exp.SetPoint(
          self.graph_2d_exp.GetN(),
          log10(m),
          log10(ct),
          point
      )

    return self.graph_2d_exp

  def draw_2d_graph(self, x_title, y_title, z_title, x_min, x_max, y_min, y_max, z_min, z_max, custom_axis=False):
    self.graph_2d_exp.SetNpx(500)
    self.graph_2d_exp.SetNpy(500)

    hframe = ROOT.TH2D(
        "hframe", "",
        500, x_min, x_max,
        500, y_min, y_max
    )
    hframe.SetStats(0)

    self.graph_2d_exp.SetHistogram(hframe)
    self.graph_2d_exp.Draw("COLZ")

    self.graph_2d_exp.GetHistogram().GetXaxis().SetTitle(x_title)
    self.graph_2d_exp.GetHistogram().GetYaxis().SetTitle(y_title)
    self.graph_2d_exp.GetHistogram().GetZaxis().SetTitle(z_title)

    self.graph_2d_exp.GetHistogram().GetXaxis().SetTitleSize(0.05)
    self.graph_2d_exp.GetHistogram().GetYaxis().SetTitleSize(0.05)
    self.graph_2d_exp.GetHistogram().GetZaxis().SetTitleSize(0.05)

    self.graph_2d_exp.GetHistogram().GetXaxis().SetRangeUser(x_min, x_max)
    self.graph_2d_exp.GetHistogram().GetXaxis().SetRangeUser(x_min, x_max)
    self.graph_2d_exp.GetHistogram().GetYaxis().SetRangeUser(y_min, y_max)
    self.graph_2d_exp.GetHistogram().GetZaxis().SetRangeUser(z_min, z_max)

    if custom_axis:
      self.graph_2d_exp.GetHistogram().GetXaxis().SetLabelSize(0)
      self.graph_2d_exp.GetHistogram().GetYaxis().SetLabelSize(0)
      self.graph_2d_exp.GetHistogram().GetXaxis().SetTickLength(0)
      self.graph_2d_exp.GetHistogram().GetYaxis().SetTickLength(0)
      self.graph_2d_exp.GetHistogram().GetZaxis().SetTickLength(0)
      self.graph_2d_exp.GetHistogram().GetYaxis().SetTitleOffset(1.2)
      self.graph_2d_exp.GetHistogram().GetZaxis().SetTitleOffset(1.15)

  def draw_missing_points(self, custom_axis=False):
    if len(self.missing_points) == 0:
      return

    # Draw red X over missing points
    self.missing_graph = ROOT.TGraph(len(self.missing_points))
    for i, (m, ct) in enumerate(self.missing_points):
      self.missing_graph.SetPoint(i, log10(m), log10(ct))

    self.missing_graph.SetMarkerColor(ROOT.kRed)
    self.missing_graph.SetMarkerStyle(70)
    self.missing_graph.SetMarkerSize(3.0)

    self.missing_graph.Draw("P SAME")
    if custom_axis:
      self.missing_graph.GetXaxis().SetLabelSize(0)
      self.missing_graph.GetYaxis().SetLabelSize(0)
      self.missing_graph.GetXaxis().SetTickLength(0)
      self.missing_graph.GetYaxis().SetTickLength(0)


  def get_theory_2d_graph(self):
    self.graph_2d_theory = ROOT.TGraph2D()
    self.graph_2d_theory.SetTitle("")
    self.graph_2d_theory.SetLineColor(ROOT.kBlack)
    self.graph_2d_theory.SetLineWidth(2)
    self.graph_2d_theory.SetLineStyle(2)
    self.graph_2d_theory.SetMarkerStyle(20)
    self.graph_2d_theory.SetMarkerSize(0.5)

    for (m, ct) in self.data.keys():
      point = log10(get_cross_section_for_theory_coupling(m, ct, "Run2"))

      self.graph_2d_theory.SetPoint(
          self.graph_2d_theory.GetN(),
          log10(m),
          log10(ct),
          point
      )

    return self.graph_2d_theory

  def draw_2d_theory_graph(self, x_title, y_title, z_title, x_min, x_max, y_min, y_max, z_min, z_max, custom_axis=False):
    self.graph_2d_theory.SetNpx(500)
    self.graph_2d_theory.SetNpy(500)

    self.graph_2d_theory.Draw("COLZ")

    self.graph_2d_theory.GetHistogram().GetXaxis().SetTitle(x_title)
    self.graph_2d_theory.GetHistogram().GetYaxis().SetTitle(y_title)
    self.graph_2d_theory.GetHistogram().GetZaxis().SetTitle(z_title)

    self.graph_2d_theory.GetHistogram().GetXaxis().SetTitleSize(0.05)
    self.graph_2d_theory.GetHistogram().GetYaxis().SetTitleSize(0.05)
    self.graph_2d_theory.GetHistogram().GetZaxis().SetTitleSize(0.05)

    self.graph_2d_theory.GetHistogram().GetXaxis().SetRangeUser(x_min, x_max)
    self.graph_2d_theory.GetHistogram().GetXaxis().SetRangeUser(x_min, x_max)
    self.graph_2d_theory.GetHistogram().GetYaxis().SetRangeUser(y_min, y_max)
    self.graph_2d_theory.GetHistogram().GetZaxis().SetRangeUser(z_min, z_max)

    if custom_axis:
      self.graph_2d_theory.GetHistogram().GetXaxis().SetLabelSize(0)
      self.graph_2d_theory.GetHistogram().GetYaxis().SetLabelSize(0)
      self.graph_2d_theory.GetHistogram().GetZaxis().SetLabelSize(0)
      self.graph_2d_theory.GetHistogram().GetXaxis().SetTickLength(0)
      self.graph_2d_theory.GetHistogram().GetYaxis().SetTickLength(0)
      self.graph_2d_theory.GetHistogram().GetZaxis().SetTickLength(0)
      self.graph_2d_theory.GetHistogram().GetYaxis().SetTitleOffset(1.1)
      self.graph_2d_theory.GetHistogram().GetZaxis().SetTitleOffset(1.1)

    # Change the underflow color to gray
    gray_color = ROOT.TColor.GetColor(0.65, 0.65, 0.65)
    n_colors = ROOT.gStyle.GetNumberOfColors()
    colors = array.array('i', [ROOT.gStyle.GetColorPalette(i) for i in range(n_colors)])
    ROOT.gROOT.GetColor(colors[0]).SetRGB(0.65, 0.65, 0.65)

  def get_expected_theory_ratio_graph(self, expected = True):
    if not self.graph_2d_exp or not self.graph_2d_theory or not self.graph_2d_data:
      warn("Expected ot thero graph not defined - ratio cannot be computed!")
      return
    
    self.graph_2d_data_theory_ratios = []
    n_values = len(self.graph_2d_data)
    for i in range(0, n_values):
      graph = ROOT.TGraph2D()
      graph.SetTitle("")
      graph.SetLineColor(ROOT.kBlack)
      graph.SetLineWidth(2)
      graph.SetLineStyle(2)
      graph.SetMarkerStyle(20)
      graph.SetMarkerSize(0.5)

      for j in range(self.graph_2d_data[i].GetN()):
        x = self.graph_2d_data[i].GetX()[j]
        y = self.graph_2d_data[i].GetY()[j]
        z_exp = 10**self.graph_2d_data[i].GetZ()[j]
        z_theory = 10**self.graph_2d_theory.Interpolate(x, y)
        
        if z_theory != 0:
            graph.SetPoint(j, x, y, log10(z_exp / z_theory))
      
      self.graph_2d_data_theory_ratios.append(graph)
      
    self.graph_2d_exp_theory_ratio = self.graph_2d_data_theory_ratios[3 if expected else 0]
    return self.graph_2d_exp_theory_ratio

  def draw_2d_theory_ratio_graphs(self, canvas, x_title, y_title, z_title, x_min, x_max, y_min, y_max, z_min, z_max, custom_axis=False):
    n_values = len(self.graph_2d_data_theory_ratios)
    for i in range(0, n_values):
      canvas.cd()
      graph = self.graph_2d_data_theory_ratios[i]
      graph.SetNpx(500)
      graph.SetNpy(500)

      graph.Draw("COLZ")

      graph.GetHistogram().GetXaxis().SetTitle(x_title)
      graph.GetHistogram().GetYaxis().SetTitle(y_title)
      graph.GetHistogram().GetZaxis().SetTitle(z_title)

      graph.GetHistogram().GetXaxis().SetTitleSize(0.05)
      graph.GetHistogram().GetYaxis().SetTitleSize(0.05)
      graph.GetHistogram().GetZaxis().SetTitleSize(0.05)

      graph.GetHistogram().GetXaxis().SetRangeUser(x_min, x_max)
      graph.GetHistogram().GetXaxis().SetRangeUser(x_min, x_max)
      graph.GetHistogram().GetYaxis().SetRangeUser(y_min, y_max)
      graph.GetHistogram().GetZaxis().SetRangeUser(z_min, z_max)

      if custom_axis:
        graph.GetHistogram().GetXaxis().SetLabelSize(0)
        graph.GetHistogram().GetYaxis().SetLabelSize(0)
        graph.GetHistogram().GetZaxis().SetLabelSize(0)
        graph.GetHistogram().GetXaxis().SetTickLength(0)
        graph.GetHistogram().GetYaxis().SetTickLength(0)
        graph.GetHistogram().GetZaxis().SetTickLength(0)
        graph.GetHistogram().GetYaxis().SetTitleOffset(1.1)
        graph.GetHistogram().GetZaxis().SetTitleOffset(1.1)
      
      self.graph_2d_data_theory_ratios[i] = graph
    
    self.graph_2d_data_theory_ratios[3].Draw("COLZ")

  def draw_2d_theory_contour_graph(self, canvas, x_min, x_max, y_min, y_max, expected = True, coupling_graphs = False):
    self.hist_contours = []
    self.contour_graphs = []
    n_values = len(self.graph_2d_data_theory_ratios)
    # obs, -2sigma, -1sigma, exp, +1sigma, +2sigma
    contour_line_styles = [1, 3, 2, 1, 2, 3]

    temp_canvas = ROOT.TCanvas("temp_contour", "", 800, 600)

    for i in range(0, n_values):
      n_pts = self.graph_2d_data_theory_ratios[i].GetN()
      contour_color = ROOT.kBlack if i==0 else ROOT.kRed

      temp_canvas.cd()
      hist_contour = self.graph_2d_data_theory_ratios[i].GetHistogram().Clone(f"hist_contour_ratio_{i}")
      contour_level = array.array('d', [0.0])
      hist_contour.SetContour(1, contour_level)
      hist_contour.Draw("CONT LIST")
      temp_canvas.Update()

      contours = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
      if not contours:
          continue
      contours_list = contours.At(0)  # first (only) contour level
      if not contours_list:
          continue

      for j in range(contours_list.GetSize()):
          graph = contours_list.At(j)
          if not graph:
              continue
          graph_clone = graph.Clone(f"contour_graph_{i}_{j}")

          graph_clone.SetLineColor(contour_color)
          graph_clone.SetLineWidth(2)
          graph_clone.SetLineStyle(contour_line_styles[i])
          ROOT.SetOwnership(graph_clone, False)
          self.contour_graphs.append(graph_clone)
        
      self.hist_contours.append(hist_contour)

    canvas.cd()
    for graph in self.contour_graphs:
      graph.Draw("L same")

    self.contour_coupling_points = []
    x, y = ctypes.c_double(0), ctypes.c_double(0)
    if coupling_graphs:
      for graph in self.contour_graphs:
        points = []
        for k in range(graph.GetN()):
          graph.GetPoint(k, x, y)
          if x == 0 and y == 0:
            continue
          m = 10**x.value
          ctau = 10**y.value
          ctt = self.derive_ctt(m, ctau, boost=False)
          points.append((x.value, ctt))
        self.contour_coupling_points.append(points)
      
    temp_canvas.Close()

    
  def draw_pion_label(self):
    tex = ROOT.TLatex(0.60, 0.80, "tt+a, a #rightarrow #pi's")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.SetLineWidth(2)
    tex.SetTextColor(ROOT.kRed)
    tex.DrawClone()

  def draw_cms_label(self, subtext = "Preliminary", x = 0.11, subpad = False):
    tex = ROOT.TLatex(x, 0.92, f"#bf{{CMS}}#it{{ {subtext}}}")
    textsize = 0.042
    if subpad:
      tex = ROOT.TLatex(0.15, 0.80, f"#bf{{CMS}}#it{{ {subtext}}}")
      textsize = 0.18
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(textsize)
    tex.SetLineWidth(2)
    tex.DrawClone()

  def draw_lumi_label(self, luminosity_run2, luminosity_run3, variable="", subpad = False):
    lumi_text = ""
    lumi_text_xmin = 0.60
    if luminosity_run2 != 0 and luminosity_run3 == 0:
      lumi_text = f"#scale[0.8]{{{luminosity_run2/1000:.0f} fb^{{-1}} (13 TeV)}}"
    elif luminosity_run2 == 0 and luminosity_run3 != 0:
      lumi_text = f"#scale[0.8]{{{luminosity_run3/1000:.0f} fb^{{-1}} (13.6 TeV)}}"
    else:
      lumi_text = f"#scale[0.8]{{{luminosity_run2/1000:.0f} fb^{{-1}} (13 TeV), {luminosity_run3/1000:.0f} fb^{{-1}} (13.6 TeV)}}"
      lumi_text_xmin = 0.49
      # lumi_text_xmin = 0.42
    if variable == "mass" or variable == "ctau" or variable == "mass_coupling":
      lumi_text_xmin += 0.12
    tex = ROOT.TLatex(lumi_text_xmin, 0.92, lumi_text)
    textsize = 0.042
    if subpad:
      tex = ROOT.TLatex(lumi_text_xmin-0.01, 0.80, lumi_text)
      textsize = 0.2
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(textsize)
    tex.SetLineWidth(2)
    tex.DrawClone()

  def draw_signal_label(self, variable, scan_point, x = 0.60, y = 0.85):
    if variable == "mass_signal_strength":
      return
    if "mass" in variable:
      signal_label = f"#scale[0.8]{{c#tau_{{a}} = {self.get_ctau_label(scan_point)}}}"
    else:
      signal_label = f"#scale[0.8]{{m_{{a}} = {scan_point:.2f} GeV}}"

    tex = ROOT.TLatex(x, y, signal_label)
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.SetLineWidth(2)
    tex.DrawClone()

  def find_lifetime_for_mass(self, mass, boost, coupling=0.1, Lambda=4*pi*1000):
    ctau = physics.ctaua(mass, coupling/2, coupling/2, Lambda)  # in cm

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

  def reference_ctau(self, mass, boost=True, Lambda=4*pi*1000):
      return self.find_lifetime_for_mass(mass=mass, coupling=1.0, boost=boost, Lambda=Lambda)

  def derive_ctt(self, mass, ctau_target, boost=True, Lambda=4*pi*1000):
      ctau_ref = self.reference_ctau(mass, boost, Lambda)
      return sqrt(ctau_ref / ctau_target)


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
        scale = self.get_scale(m, ct)
        if m == mass:
          values[ct] = [v_ * scale for v_ in v]

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


  def get_limits_for_coupling(self):

    xsec_limits = {}
    for (m, ct), values in self.data.items():
        if m not in xsec_limits:
            xsec_limits[m] = {}
        scale = self.get_scale(m, ct)
        xsec_limits[m][ct] = [v_ * scale for v_ in values]

    for m, ctau_dict in xsec_limits.items():

      pairs = sorted(ctau_dict.items())
      ctau_vals = [ct for ct, _ in pairs]

      log_ctau = array.array('d', [log10(ct) for ct in ctau_vals])
      n_points = len(pairs[0][1])
      interpolators = {}
      interpolators[m] = {
        "ctau_min": min(ctau_vals),
        "ctau_max": max(ctau_vals),
        "graphs": []
      }

      for i in range(n_points):
        sigma_vals = [max(vals[i], 1e-300) for _, vals in pairs]
        log_sigma = array.array('d', [log10(sigma) for sigma in sigma_vals])
        graph = ROOT.TGraph(len(log_ctau), log_ctau, log_sigma)
        interpolators[m]["graphs"].append(graph)

      g_ref = 0.1
      g_values = [10**(-5 + i * (6.0/2000.0)) for i in range(2000)]
      
      results = {}
      for m, info in interpolators.items():
        results[m] = []
        ctau_ref = self.find_lifetime_for_mass(m, boost=False, coupling=g_ref)
        xsec_ref = get_theory_cross_section(m, "Run2")
        ctau_min = info["ctau_min"]
        ctau_max = info["ctau_max"]
        for graph in info["graphs"]:
          scan = []
          for g in g_values:
            ctau_g = ctau_ref * (g_ref / g)**2
            if ctau_g < ctau_min or ctau_g > ctau_max:
              continue
            
            xsec_g = xsec_ref * (g / g_ref)**2

            log_sigma_limit = graph.Eval(log10(ctau_g))
            sigma_limit = 10**log_sigma_limit

            ratio = xsec_g / sigma_limit
            excluded = (ratio >= 1.0)
            scan.append({
              "g": g,
              "ctau": ctau_g,
              "xsec_theory": xsec_g,
              "xsec_limit": sigma_limit,
              "ratio": ratio,
              "excluded": excluded,
            })
          results[m].append(scan)

      coupling2_limits = {}
      for m, scans in results.items():
        coupling2_limits[m] = []
        for scan in scans:
          excluded_points = [p["g"]**2 for p in scan if p["excluded"]]
          if len(excluded_points) == 0:
            coupling2_limits[m].append(None)
          else:
            coupling2_limits[m].append(min(excluded_points))
    return coupling2_limits

  def get_limit_graph_scaled_to_run2(self, limits, luminosity_run2, luminosity_run3, variable, scan_point):

    run2_scale = sqrt((luminosity_run2 + luminosity_run3) / luminosity_run2) if luminosity_run2 != 0 else 1.0
    print(f"Run 2 scale factor: {run2_scale:.3f}")
    graph = ROOT.TGraph()
    graph.SetLineColor(ROOT.kViolet)
    graph.SetLineWidth(2)
    graph.SetLineStyle(ROOT.kDashed)

    for i, (x_value, r_value) in enumerate(limits.items()):
        if len(r_value) != 6:
          continue

        mass = x_value if "mass" in variable else scan_point
        ctau = scan_point if "mass" in variable else x_value
        scale = self.get_scale(mass, ctau, variable)
        scale *= run2_scale
        graph.SetPoint(i, x_value, r_value[3]*scale)
    return graph
  
  def extract_limits_for_signal_strength1(self, expected_limits):
    gr = ROOT.TGraph()
    n_bands = 6
    x_crosses = []
    for band in range(n_bands):
      gr = ROOT.TGraph()
      for i, (ctau, r_values) in enumerate(sorted(expected_limits.items())):
        gr.SetPoint(i, ctau, r_values[band])
        # gr.SetPoint(i, log10(ctau), r_values[band])
      
      n = gr.GetN()
      found = False
      for i in range(n - 1):
        x1 = ctypes.c_double(0.0)
        y1 = ctypes.c_double(0.0)
        x2 = ctypes.c_double(0.0)
        y2 = ctypes.c_double(0.0)

        gr.GetPoint(i, x1, y1)
        gr.GetPoint(i + 1, x2, y2)

        r1 = y1.value
        r2 = y2.value
        ct1 = x1.value
        ct2 = x2.value
        if (r1 - 1.0) * (r2 - 1.0) <= 0:
          x_cross = ct1 + (1.0 - r1) * (ct2 - ct1) / (r2 - r1)
          x_crosses.append(x_cross)
          found = True
          break

      if not found:
        # try extrapolation using last two points
        x1 = ctypes.c_double(0.0)
        y1 = ctypes.c_double(0.0)
        x2 = ctypes.c_double(0.0)
        y2 = ctypes.c_double(0.0)

        gr.GetPoint(n - 2, x1, y1)
        gr.GetPoint(n - 1, x2, y2)

        r1, r2 = y1.value, y2.value
        ct1, ct2 = x1.value, x2.value

        if r1 != r2:
          x_cross = ct1 + (1.0 - r1) * (ct2 - ct1) / (r2 - r1)
          x_crosses.append(x_cross)
        else:
          x_crosses.append(ct2)
    
    return x_crosses


  def find_ctau_at_r1(self, expected_limits, band_labels=None, mass_label=""):
    ctaus = sorted(expected_limits.keys())
    n_bands = len(next(iter(expected_limits.values())))
    
    if band_labels is None:
        band_labels = [f"band[{i}]" for i in range(n_bands)]
    
    log_ctaus = np.array([np.log10(ct) for ct in ctaus], dtype=float)
    
    ctau_crossings = []
    
    for band_idx in range(n_bands):
        label = band_labels[band_idx]
        r_values = np.array([expected_limits[ct][band_idx] for ct in ctaus], dtype=float)
        log_r    = np.log10(r_values)
        
        r_lo = r_values[0]
        r_hi = r_values[-1]
        
        # Case 1: r=1 is within the data range — interpolate as before
        if min(r_lo, r_hi) <= 1.0 <= max(r_lo, r_hi):
          # Find the two bracketing points
          for i in range(len(log_ctaus) - 1):
              if min(log_r[i], log_r[i+1]) <= 0.0 <= max(log_r[i], log_r[i+1]):
                  # Linear interpolation in log-log space between these two points
                  slope = (log_r[i+1] - log_r[i]) / (log_ctaus[i+1] - log_ctaus[i])
                  intercept = log_r[i] - slope * log_ctaus[i]
                  log_ctau_cross = -intercept / slope
                  break
        
        # Case 2: all r > 1, crossing is below ctau range — extrapolate leftward
        elif r_lo > 1.0:
            # Use all points for a log-log linear fit (more robust than 2-point slope)
            coeffs = np.polyfit(log_ctaus, log_r, 1)
            slope, intercept = coeffs
            
            # Sanity check: slope should be positive (r increases with ctau)
            if slope <= 0:
                print(f"[WARNING] mass={mass_label}, {label}: "
                      f"non-physical slope={slope:.3f} in extrapolation, skipping")
                ctau_crossings.append(None)
                continue
            
            log_ctau_cross = -intercept / slope
            print(f"[EXTRAPOLATED LEFT] mass={mass_label}, {label}: "
                  f"global slope={slope:.3f}, intercept={intercept:.3f}")
        
        # Case 3: all r < 1, crossing is above ctau range — extrapolate rightward
        elif r_hi < 1.0:
            slope = (log_r[-1] - log_r[-2]) / (log_ctaus[-1] - log_ctaus[-2])
            intercept = log_r[-1] - slope * log_ctaus[-1]
            log_ctau_cross = -intercept / slope
            print(f"[EXTRAPOLATED RIGHT] mass={mass_label}, {label}: "
                  f"using slope={slope:.3f} from last 2 points")
        
        else:
            print(f"[WARNING] mass={mass_label}, {label}: unexpected r range, skipping")
            ctau_crossings.append(None)
            continue
        
        ctau_at_r1 = 10**log_ctau_cross
        ctau_crossings.append(ctau_at_r1)
    
    return ctau_crossings

  def extract_limits_for_signal_strength1(self, expected_limits):
    n_bands = 6
    ctau_crosses = []

    points = sorted(expected_limits.items())

    ctaus = [p[0] for p in points]
    ctau_min = min(ctaus)
    ctau_max = max(ctaus)

    for band in range(n_bands):
      gr = ROOT.TGraph()
      for i, (ctau, r_values) in enumerate(points):
        gr.SetPoint(i, ctau, r_values[band])

      spline = ROOT.TSpline3(f"spline_band_{band}", gr)

      def f(ctau):
        return spline.Eval(ctau) - 1.0

      found = False
      for i in range(len(ctaus) - 1):
        c1 = ctaus[i]
        c2 = ctaus[i + 1]

        f1 = f(c1)
        f2 = f(c2)

        if f1 * f2 <= 0:
          ctau_cross = brentq(f, c1, c2)
          ctau_crosses.append(ctau_cross)
          found = True
          break

      if not found:
        r_low = spline.Eval(ctau_min)
        r_high = spline.Eval(ctau_max)

        if r_low > 1:
            c1, c2 = ctaus[0], ctaus[1]
        elif r_high < 1:
            c1, c2 = ctaus[-2], ctaus[-1]
        else:
            print(f"Warning: band {band}: no crossing found")
            ctau_crosses.append(None)
            continue

        r1 = spline.Eval(c1)
        r2 = spline.Eval(c2)
        if r1 != r2:
            log_c1, log_c2 = log10(c1), log10(c2)
            log_cross = log_c1 + (1 - r1) * (log_c2 - log_c1) / (r2 - r1)
            ctau_cross = 10 ** log_cross
        else:
            ctau_cross = c2
        ctau_crosses.append(ctau_cross)

    return ctau_crosses


  def find_coupling_for_ctau(self, mass, boost, ctau_target,
                           cmin=1e-12, cmax=1e25):
    def f(c):
        return self.find_lifetime_for_mass(mass, boost, c) - ctau_target
    
    fmin = f(cmin)
    fmax = f(cmax)
    if fmin * fmax > 0:
        raise ValueError(f"No root in coupling range — expand bounds fmin = {fmin}, fmax = {fmax}, ctau_target = {ctau_target}")

    return brentq(f, cmin, cmax)

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
    y_min = 0.70 if not self.show_obs else 0.61
    legend = ROOT.TLegend(0.19, y_min, 0.39, 0.82)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    if self.show_obs:
      legend.AddEntry(self.obs_graph, "Observed", "L")
    legend.AddEntry(self.exp_graph, "Expected", "L")
    legend.AddEntry(self.exp_graph_1sigma, "Expected #pm 1 s.d.", "F")
    legend.AddEntry(self.exp_graph_2sigma, "Expected #pm 2 s.d.", "F")
    legend.DrawClone()


class SimpleGraph:
  def __init__(self, points, title, color, width = 2, style = 1):
    self.graph = ROOT.TGraph()
    self.title = title
    self.graph.SetLineColor(color)
    self.graph.SetLineWidth(width)
    self.graph.SetLineStyle(style)

    points = sorted(points, key=lambda p: p[0])
    points = [(float(x), float(y)) for x, y in points]

    for i, (x, y) in enumerate(points):
      self.graph.SetPoint(i, x, y)

  def get_graph(self):
    return self.graph, self.title

  def draw(self):
    self.graph.DrawClone("Lsame")
