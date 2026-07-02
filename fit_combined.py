import ROOT

input_path = "ttalps_get_SF_over_resonance_fraction_graphs_ANv3/graph_2016preVFP2016postVFP201720182022preEE2022postEE2023preBPix2023postBPix_JPsiDimuonsPatDSA_noDimuonEffSFs_noMatching_ABCD_ANv3_exp_linear_a_eta_irr_-3.root"

functions = [
  ("[0] + exp([1] * x)", ROOT.kRed + 1),
  ("[0] * exp([1] * x)", ROOT.kBlue + 1),
  ("[0] + [1] * x", ROOT.kGreen + 2),
]

topMargin = 0.06
bottomMargin = 0.3
leftMargin = 0.16
rightMargin = 0.15

def main():
  file = ROOT.TFile.Open(input_path)
  graph = file.Get("Graph")

  canvas = ROOT.TCanvas("c1", "c1", 800, 600)
  canvas.SetBottomMargin(0.13)
  canvas.SetLeftMargin(0.11)

  canvas.SetTickx(1)
  canvas.SetTicky(1)

  # remove 5th point from the graph
  # graph.RemovePoint(9)

  graph.SetMarkerStyle(20)
  graph.SetMarkerColor(ROOT.kBlack)

  graph.Draw("AP")
  graph.GetXaxis().SetLimits(0, 1.0)
  graph.GetYaxis().SetRangeUser(0, 2.5)

  graph.SetTitle("")
  graph.GetXaxis().SetTitle("f_{R}")
  graph.GetXaxis().SetLabelSize(0.05)
  graph.GetXaxis().SetTitleSize(0.05)
  graph.GetYaxis().SetTitle("Corrections (Data/MC)")
  graph.GetYaxis().SetLabelSize(0.05)
  graph.GetYaxis().SetTitleSize(0.05)
  graph.GetYaxis().SetTitleOffset(0.98)

  legend = ROOT.TLegend(0.37, 0.68, 0.87, 0.87)
  legend.SetBorderSize(0)
  legend.SetFillStyle(0)

  for function, color in functions:
    fit_func = ROOT.TF1("fit_func", function, 0, 1)
    fit_func.SetParameters(1.0, -10.0)
    fitter = graph.Fit(fit_func, "S")

    # get chi2/ndf
    chi2 = fitter.Get().Chi2()
    ndf = fitter.Get().Ndf()
    chi2_red = chi2 / ndf

    fit_func.SetLineColor(color)
    fit_func.Draw("same")
    legend.AddEntry(
      fit_func, f"{function}, #chi^{{2}}/NDF = {chi2_red:.2f}", "l"
    )

  legend.Draw()

  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAngle(0)
  latex.SetTextColor(ROOT.kBlack)
  latex.SetTextFont(42)
  latex.SetTextAlign(31)
  top = canvas.GetTopMargin()
  right = canvas.GetRightMargin()
  latex.SetTextSize(0.4*top)
  lumi = f"{59830. / 1000.0:.1f} fb^{{-1}}"
  # lumiText = lumi + " (13 TeV)"
  lumiText = "138 fb^{-1} (13 TeV), 62 fb^{-1} (13.6 TeV)"
  latex.DrawLatex(1-right, 1-top+0.02, lumiText)

  left = canvas.GetLeftMargin()
  bottom = canvas.GetBottomMargin()
  posX_ = left + 0.045*(1-left-right) - 0.11
  posY_ = 1-top - 0.070*(1-bottom) + 1.55
  latex = ROOT.TLatex()
  latex.SetTextFont(61)
  latex.SetTextSize(0.55*top)
  latex.SetTextAlign(13)
  latex.DrawLatex(posX_, posY_, "CMS")

  latex = ROOT.TLatex()
  latex.SetTextFont(52)
  latex.SetTextAlign(13)
  extraTextSize = 0.76 * 0.55*top
  latex.SetTextSize(0.76*0.55*top)
  # latex.DrawLatex(posX_, posY_ - 0.1 , "Simulation Preliminary")
  latex.DrawLatex(posX_, posY_ - 0.2 , "Work in Progress")
  # latex.DrawLatex(posX_, posY_ - 0.2 , "Preliminary")
  # latex.DrawLatex(posX_, posY_ - 0.1 , "Internal")

  canvas.Update()
  canvas.SaveAs("fit_combined_corrections_thesis.pdf")


if __name__ == "__main__":
  main()
