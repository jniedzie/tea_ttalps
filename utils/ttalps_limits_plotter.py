import ROOT
from ttalps_cross_sections import get_cross_sections
import re

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)

input_path = "../datacards/limits_BestPFIsoDimuonVertex_Pat_LxySignificance.txt"

luminosity = 59830.  # recommended lumi from https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2

coupling_scale = 0.1

# variable = "mass"
variable = "ctau"

if variable == "mass":
  y_min = 1e-1
  y_max = 1e6
  x_min = 0.1
  x_max = 1e2
  x_title = "m_{a} [GeV]"
  scan_points = [1e-5, 1e0, 1e1, 1e2, 1e3]

if variable == "ctau":
  y_min = 1e-1
  y_max = 1e6
  x_min = 1e-5
  x_max = 1e3
  x_title = "c#tau_{a} [mm]"
  scan_points = [0.35, 1.0, 2.0, 12.0, 30.0, 60.0]

y_title = "95% CL lower limit on g_{#Psi}"


def load_limits(input_path):
  data = {}
  pattern = re.compile(r"signal_tta_mAlp-(\d+p?\d*)GeV_ctau-(\S+)mm: \[(.*?)\]")

  with open(input_path, 'r') as f:
    for line in f:
      match = pattern.match(line.strip())
      if match:
        mass_str, ctau_str, values_str = match.groups()
        mass = float(mass_str.replace('p', '.'))
        ctau = float(ctau_str)
        values = list(map(float, values_str.replace("'", "").split(', ')))
        data[(mass, ctau)] = values

  return data


def get_ctau_label(ctau):
  exponent = int(round(ROOT.TMath.Log10(ctau)))
  label = f"10^{{{exponent}}}"
  return label


def main():
  data = load_limits(input_path)

  for key, value in data.items():
    print(f"{key}: {value}")

  ROOT.gROOT.SetBatch(True)

  obs_graph = ROOT.TGraph()
  obs_graph.SetLineColor(ROOT.kBlack)
  obs_graph.SetLineWidth(2)
  obs_graph.SetLineStyle(1)

  exp_graph = ROOT.TGraphAsymmErrors()
  exp_graph.SetLineColor(ROOT.kBlack)
  exp_graph.SetLineWidth(2)
  exp_graph.SetLineStyle(2)

  exp_graph_1sigma = ROOT.TGraphAsymmErrors()
  exp_graph_1sigma.SetLineWidth(0)
  exp_graph_1sigma.SetFillColorAlpha(ROOT.kGreen+1, 1.0)

  exp_graph_2sigma = ROOT.TGraphAsymmErrors()
  exp_graph_2sigma.SetLineWidth(0)
  exp_graph_2sigma.SetFillColorAlpha(ROOT.kYellow+1, 1.0)

  for scan_point in scan_points:

    limits = {}
    for (m, ct), values in data.items():
      if variable == "mass" and ct == scan_point:
        limits[m] = values
      if variable == "ctau" and m == scan_point:
        limits[ct] = values

    print(limits)

    for i, (x_value, r_value) in enumerate(limits.items()):

      # scale = cross_sections[name]  # TODO: implement cross section limits
      scale = coupling_scale

      obs_graph.SetPoint(i, x_value, r_value[0]*scale)
      exp_graph.SetPoint(i, x_value, r_value[3]*scale)

      exp_graph_1sigma.SetPoint(i, x_value, r_value[3]*scale)
      exp_graph_1sigma.SetPointError(i, 0, 0, (r_value[3] - r_value[2])*scale, (r_value[4] - r_value[3])*scale)

      exp_graph_2sigma.SetPoint(i, x_value, r_value[3]*scale)
      exp_graph_2sigma.SetPointError(i, 0, 0, (r_value[3] - r_value[1])*scale, (r_value[5] - r_value[3])*scale)

    canvas = ROOT.TCanvas(f"canvas_{scan_point}", "", 800, 600)
    canvas.cd()
    canvas.SetLogx()
    canvas.SetLogy()

    exp_graph_2sigma.Draw("A3")
    exp_graph_1sigma.Draw("3same")
    exp_graph.Draw("Lsame")
    obs_graph.Draw("Lsame")

    exp_graph_2sigma.GetXaxis().SetTitleSize(0.05)
    exp_graph_2sigma.GetYaxis().SetTitleSize(0.05)
    exp_graph_2sigma.GetXaxis().SetLabelSize(0.04)
    exp_graph_2sigma.GetYaxis().SetLabelSize(0.04)
    exp_graph_2sigma.GetXaxis().SetTitleOffset(1.1)
    exp_graph_2sigma.GetYaxis().SetTitleOffset(1.1)

    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)

    exp_graph_2sigma.GetXaxis().SetTitle(x_title)
    exp_graph_2sigma.GetYaxis().SetTitle(y_title)

    # exp_graph_2sigma.GetXaxis().SetMoreLogLabels()

    # set x and y axes limits
    exp_graph_2sigma.GetXaxis().SetLimits(x_min, x_max)
    exp_graph_2sigma.SetMinimum(y_min)
    exp_graph_2sigma.SetMaximum(y_max)

    legend = ROOT.TLegend(0.20, 0.65, 0.45, 0.9)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.AddEntry(obs_graph, "Observed", "L")
    legend.AddEntry(exp_graph, "Expected", "L")
    legend.AddEntry(exp_graph_1sigma, "Expected #pm 1 #sigma", "F")
    legend.AddEntry(exp_graph_2sigma, "Expected #pm 2 #sigma", "F")
    legend.Draw()

    tex = ROOT.TLatex(0.15, 0.92, "#bf{CMS} #it{Preliminary}")
    # tex = ROOT.TLatex(0.15, 0.92, "#bf{CMS}")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.SetLineWidth(2)
    tex.Draw()

    tex2 = ROOT.TLatex(0.60, 0.92, f"#scale[0.8]{{pp, {luminosity/1000:.0f} fb^{{-1}} (#sqrt{{s}} = 13 TeV)}}")
    tex2.SetNDC()
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.045)
    tex2.SetLineWidth(2)
    tex2.Draw()

    # add a label describing which signal we're looking at
    if variable == "mass":
      signal_label = f"#scale[0.8]{{c#tau = {get_ctau_label(scan_point)} mm}}"
    if variable == "ctau":
      signal_label = f"#scale[0.8]{{m_a = {scan_point:.2f} GeV}}"

    tex3 = ROOT.TLatex(0.60, 0.85, signal_label)
    tex3.SetNDC()
    tex3.SetTextFont(42)
    tex3.SetTextSize(0.045)
    tex3.SetLineWidth(2)
    tex3.Draw()

    canvas.Update()
    
    unit = "mm" if variable == "mass" else "GeV"
    
    canvas.SaveAs(f"../plots/{input_path.replace('.txt', '.pdf')}_{scan_point:.0e}_{unit}.pdf")


if __name__ == "__main__":
  main()
