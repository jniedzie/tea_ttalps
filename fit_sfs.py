import ROOT
import math
from ctypes import c_double

input_path = "ttalps_get_SF_over_resonance_fraction_graphs_ANv3"
input_pattern = "graph_{}_JPsiDimuonsPatDSA_noDimuonEffSFs_noMatching_ABCD_ANv3_exp_linear_a_pt_irr_{}.root"

years = [
  "2016preVFP", "2016postVFP", "2017", "2018", "2022preEE", "2022postEE",
  "2023preBPix", "2023postBPix"
]
pt_bins = ["3", "30", "60"]
colors = {"3": ROOT.kRed, "30": ROOT.kBlue, "60": ROOT.kGreen + 2}

function_choice = "[0] + exp([1] * x)"
# function_choice = "[0] * exp([1] * x)"
# function_choice = "[0] + [1] * x"

b_start = 0.1

remove_bad_point = False


def _flatten_keys(graphs2d):
  pairs = []
  for year in sorted(graphs2d.keys()):
    for pt in sorted(graphs2d[year].keys()):
      pairs.append((year, pt))
  return pairs


def make_global_fcn_asymm_2d(graphs2d, pairs):
  graphs = [graphs2d[y][pt] for (y, pt) in pairs]
  x = c_double(0.0)
  y = c_double(0.0)

  def fcn(npar, gin, f, par, iflag):
    b = float(par[0])
    chi2 = 0.0
    fun = ROOT.TF1("temp_func", function_choice, 0, 1)
    fun.SetParameter(1, b)

    for i, graph in enumerate(graphs):
      a = float(par[1 + i])
      fun.SetParameter(0, a)

      for j in range(graph.GetN()):
        graph.GetPoint(j, x, y)
        xi = x.value
        yi = y.value

        y_hat = fun.Eval(xi)
        residual = yi - y_hat

        eyl = graph.GetErrorYlow(j)
        eyh = graph.GetErrorYhigh(j)
        err = eyh if residual >= 0.0 else eyl
        if err <= 0.0:
          continue

        pull = residual / err
        chi2 += pull * pull

    f.value = chi2

  return fcn


def fit_shared_b_2d(graphs):
  pairs = _flatten_keys(graphs)
  n_graphs = len(pairs)
  a0_list = [0.0] * n_graphs
  ROOT.TVirtualFitter.SetDefaultFitter("Minuit")

  npar = n_graphs + 1
  fitter = ROOT.TVirtualFitter.Fitter(graphs[years[0]][pt_bins[0]], npar)

  fitter.SetFCN(make_global_fcn_asymm_2d(graphs, pairs))
  fitter.SetParameter(0, "b_shared", b_start, 1e-4, 0.0, 0.0)

  for i, (year, pt) in enumerate(pairs):
    fitter.SetParameter(1 + i, f"a_{year}_{pt}", a0_list[i], 1e-3, 0.0, 0.0)

  fitter.ExecuteCommand("MIGRAD", ROOT.nullptr, 0)

  best_b = fitter.GetParameter(0)
  best_a2d = {}
  for i, (year, pt) in enumerate(pairs):
    best_a2d.setdefault(year, {})[pt] = fitter.GetParameter(1 + i)

  return best_b, best_a2d, fitter, pairs


def get_cov_matrix_from_fitter(fitter, npar):
  m = fitter.GetMinuit()
  arr = (c_double * (npar * npar))()
  m.mnemat(arr, npar)
  cov = [[0.0 for _ in range(npar)] for __ in range(npar)]
  for i in range(npar):
    for j in range(npar):
      cov[i][j] = float(arr[i * npar + j])
  return cov


def propagate_y_uncertainty(a, b, cov, idx_a, x):
  fun = ROOT.TF1("temp_func", function_choice, 0, 1)
  fun.SetParameter(0, a)
  fun.SetParameter(1, b)
  y = fun.Eval(x)

  if function_choice == "[0] + exp([1] * x)":
    dy_db = x * math.exp(b * x)
    dy_da = 1.0
  elif function_choice == "[0] * exp([1] * x)":
    dy_db = a * x * math.exp(b * x)
    dy_da = math.exp(b * x)
  elif function_choice == "[0] + [1] * x":
    dy_db = x
    dy_da = 1.0
  else:
    print("Unknown function choice for uncertainty propagation")
    return y, float('nan')

  var_b = cov[0][0]
  var_a = cov[idx_a][idx_a]
  cov_ab = cov[idx_a][0]

  var_y = dy_da**2 * var_a + dy_db**2 * var_b + 2.0 * dy_da * dy_db * cov_ab

  # Guard against tiny negative variance from numerical roundoff
  if var_y < 0.0 and var_y > -1e-12:
    var_y = 0.0

  sigma_y = math.sqrt(var_y) if var_y >= 0.0 else float('nan')
  return y, sigma_y


def main():
  files = {}
  graphs = {}
  fits = {}

  canvas = ROOT.TCanvas("c1", "c1", 800, 600)
  canvas.Divide(3, 3)

  ROOT.gStyle.SetTitleY(1.005)

  for year in years:
    graphs[year] = {}
    files[year] = {}
    fits[year] = {}

    for pt_bin in pt_bins:

      file_name = input_pattern.format(year, pt_bin)
      files[year][pt_bin] = ROOT.TFile.Open(f"{input_path}/{file_name}")
      graphs[year][pt_bin] = files[year][pt_bin].Get("Graph")

      graphs[year][pt_bin].SetMarkerStyle(20)
      graphs[year][pt_bin].SetMarkerSize(0.7)
      graphs[year][pt_bin].SetMarkerColor(colors[pt_bin])
      graphs[year][pt_bin].SetLineColor(colors[pt_bin])
      graphs[year][pt_bin].SetTitle(f"{year}")
      
      if remove_bad_point:
        graphs[year][pt_bin].RemovePoint(9)

  # fit with shared b
  best_b, best_a2d, fitter, pairs = fit_shared_b_2d(graphs)

  legends = {}
  for j, year in enumerate(years):
    canvas.cd(j + 1)
    canvas.GetPad(j +1).SetTopMargin(0.14)
    canvas.GetPad(j +1).SetBottomMargin(0.13)
    canvas.GetPad(j +1).SetLeftMargin(0.14)
    canvas.GetPad(j +1).SetTickx(1)
    canvas.GetPad(j +1).SetTicky(1)
    legends[year] = ROOT.TLegend(0.55, 0.65, 0.85, 0.83)
    legend = legends[year]
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    for pt_bin in pt_bins:
      graph = graphs[year][pt_bin]

      fits[year][pt_bin] = ROOT.TF1(
        "fit_{}_{}".format(year, pt_bin), function_choice, 0, 1
      )
      fits[year][pt_bin].SetParameter(0, best_a2d[year][pt_bin])
      fits[year][pt_bin].SetParameter(1, best_b)

      fits[year][pt_bin].SetLineColor(colors[pt_bin])

      if pt_bin == "3":
        graph.Draw("AP")
        graph.GetXaxis().SetTitle("f_{R}")
        graph.GetXaxis().SetTitleSize(0.06)
        graph.GetXaxis().SetLabelSize(0.06)
        graph.GetYaxis().SetTitle("Correction (Data/MC)")
        graph.GetYaxis().SetTitleSize(0.06)
        graph.GetYaxis().SetLabelSize(0.06)
        graph.GetXaxis().SetNdivisions(505)
        graph.GetYaxis().SetNdivisions(505)

      else:
        graph.Draw("P SAME")

      legend.AddEntry(
        graph, f"p_{{T}} = {pt_bin} GeV", "l"
      )

      # set x and y range
      graph.GetXaxis().SetLimits(0, 1.0)
      graph.GetYaxis().SetRangeUser(0.0, 6.0)
      
      fits[year][pt_bin].Draw("SAME")
    
    legend.Draw()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    top = canvas.GetPad(j +1).GetTopMargin()
    right = canvas.GetPad(j +1).GetRightMargin()
    left = canvas.GetPad(j +1).GetLeftMargin()
    bottom = canvas.GetPad(j +1).GetBottomMargin()

    latex.SetTextSize(0.4*top)
    lumi = f"{59830. / 1000.0:.1f} fb^{{-1}}"
    # lumiText = lumi + " (13 TeV)"
    lumiText = "138 fb^{-1} (13 TeV), 62 fb^{-1} (13.6 TeV)"
    latex.DrawLatex(1-right, 1-top+0.02, lumiText)

    latex = ROOT.TLatex()
    posX_ = left + 0.045*(1-left-right) - 0.13
    posY_ = 5.7
    latex.SetTextFont(61)
    latex.SetTextSize(0.45*top)
    latex.SetTextAlign(13)
    latex.DrawLatex(posX_, posY_, "CMS")

    latex = ROOT.TLatex()
    latex.SetTextFont(52)
    latex.SetTextAlign(13)
    extraTextSize = 0.76 * 0.45*top
    latex.SetTextSize(0.76*0.45*top)
    # latex.DrawLatex(posX_, posY_ - 0.1 , "Simulation Preliminary")
    latex.DrawLatex(posX_, posY_ - 0.6 , "Work in Progress")
    # latex.DrawLatex(posX_, posY_ - 0.2 , "Preliminary")
    # latex.DrawLatex(posX_, posY_ - 0.1 , "Internal")

  chi2 = fitter.GetMinuit().fAmin
  pairs = _flatten_keys(graphs)  # same order you used for params
  npar = 1 + len(pairs)
  npoints = sum(graphs[y][pt].GetN() for (y, pt) in pairs)
  ndof = npoints - npar
  chi2_red = chi2 / ndof
  cov = get_cov_matrix_from_fitter(fitter, npar)

  print("\nFit results:")
  print(f"chi2/ndof = {chi2_red:.6g}")
  print(f"{'Year':<15} {'Pt Bin':<7} {'Fit(0.0)':<18} {'Fit(1.0)':<18}")

  for ip, (year, pt) in enumerate(pairs):
    fit_0, err_0 = propagate_y_uncertainty(
      best_a2d[year][pt], best_b, cov, ip + 1, 0.0
    )
    fit_1, err_1 = propagate_y_uncertainty(
      best_a2d[year][pt], best_b, cov, ip + 1, 1.0
    )
    col0 = f"{fit_0:.2f} ± {err_0:.2f}"
    col1 = f"{fit_1:.2f} ± {err_1:.2f}"
    print(f"{year:<15} {pt:<7} {col0:<18} {col1:<18}")

  canvas.SaveAs("fitted_corrections_thesis.pdf")


if __name__ == "__main__":
  main()
