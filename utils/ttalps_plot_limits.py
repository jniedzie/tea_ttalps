import ROOT
from ttalps_cross_sections import cross_sections


cross_section_limits = {
    # converting ctau to meters
    ("signal_tta_mAlp-0p35GeV_ctau-1e0mm", 1e0*1e-3): (0.0907, 0.0270, 0.0479, 0.0908, 0.1726, 0.2754, ),
    ("signal_tta_mAlp-0p35GeV_ctau-1e1mm", 1e1*1e-3): (0.1848, 0.0557, 0.0981, 0.1851, 0.3473, 0.5611, ),
    ("signal_tta_mAlp-0p35GeV_ctau-1e2mm", 1e2*1e-3): (0.7399, 0.2319, 0.3994, 0.7422, 1.3753, 2.2500, ),
    ("signal_tta_mAlp-0p35GeV_ctau-1e3mm", 1e3*1e-3): (39.5189, 13.2695, 20.8518, 39.5000, 79.4920, 119.7964, ),
    ("signal_tta_mAlp-0p35GeV_ctau-1e5mm", 1e5*1e-3): (39.3475, 13.2275, 20.7858, 39.3750, 79.2404, 119.4173, ),
}



def main():
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

    for i, (name, ctau) in enumerate(cross_section_limits):
        
        scale = cross_sections[name]
        limits = cross_section_limits[(name, ctau)]
        
        obs_graph.SetPoint(i, ctau, limits[0]*scale)
        exp_graph.SetPoint(i, ctau, limits[3]*scale)

        exp_graph_1sigma.SetPoint(i, ctau, limits[3]*scale)
        exp_graph_1sigma.SetPointError(i, 0, 0, (limits[3] - limits[2])*scale, (limits[4] - limits[3])*scale)

        exp_graph_2sigma.SetPoint(i, ctau, limits[3]*scale)
        exp_graph_2sigma.SetPointError(i, 0, 0, (limits[3] - limits[1])*scale, (limits[5] - limits[3])*scale)

    canvas = ROOT.TCanvas("canvas", "", 800, 600)
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

    exp_graph_2sigma.GetXaxis().SetTitle("c#tau [m]")
    exp_graph_2sigma.GetYaxis().SetTitle(
        "#sigma_{pp #rightarrow a #rightarrow #mu #mu} [pb]")

    # exp_graph_2sigma.GetXaxis().SetMoreLogLabels()

    # set x and y axes limits
    exp_graph_2sigma.GetXaxis().SetLimits(1e-3, 1e2)
    # exp_graph_2sigma.SetMaximum(4000)
    # exp_graph_2sigma.SetMinimum(0.4)

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

    tex2 = ROOT.TLatex(0.60, 0.92, "#scale[0.8]{pp, 60 fb^{-1} (#sqrt{s_{NN}} = 13 TeV)}")
    tex2.SetNDC()
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.045)
    tex2.SetLineWidth(2)
    tex2.Draw()

    canvas.Update()
    canvas.SaveAs("../plots/limits_cross_section.pdf")
    canvas.SaveAs("../plots/limits_cross_section.C")
    

if __name__ == "__main__":
    main()
