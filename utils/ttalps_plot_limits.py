import ROOT
from ttalps_cross_sections import *
from ttalps_limit_results import *

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
cross_sections = get_cross_sections(year)

y_min = 1e-3
y_max = 1e4

#########  OVER MASS  #########
x_min = 0.1
x_max = 1e2
x_title = "m_{a} [GeV]"
####  1 mm ALP  ####
output_name = "BestPFIsoDimuonVertex_PAT_LxySignificance_1e0mm_mass"
cross_section_limits = {
    ("tta_mAlp-0p35GeV_ctau-1e0mm", 0.35): signal_limits_over_lxy_significance[("tta_mAlp-0p35GeV_ctau-1e0mm", "PAT")],
    # ("tta_mAlp-1GeV_ctau-1e0mm", 1): signal_limits_over_lxy_significance[("tta_mAlp-1GeV_ctau-1e0mm", "PAT")],
    ("tta_mAlp-2GeV_ctau-1e0mm", 2): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e0mm", "PAT")],
    ("tta_mAlp-12GeV_ctau-1e0mm", 12): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e0mm", "PAT")],
    # ("tta_mAlp-30GeV_ctau-1e0mm", 30): signal_limits_over_lxy_significance[("tta_mAlp-30GeV_ctau-1e0mm", "PAT")],
    ("tta_mAlp-60GeV_ctau-1e0mm", 60): signal_limits_over_lxy_significance[("tta_mAlp-60GeV_ctau-1e0mm", "PAT")],
    # ("tta_mAlp-70GeV_ctau-1e0mm", 70): signal_limits_over_lxy_significance[("tta_mAlp-70GeV_ctau-1e0mm", "PAT")],
}
# output_name = "BestPFIsoDimuonVertex_PATDSA_LxySignificance_1e0mm_mass"
# cross_section_limits = {
#     ("tta_mAlp-0p35GeV_ctau-1e0mm", 0.35): signal_limits_over_lxy_significance[("tta_mAlp-0p35GeV_ctau-1e0mm", "PATDSA")],
#     # ("tta_mAlp-1GeV_ctau-1e0mm", 1): signal_limits_over_lxy_significance[("tta_mAlp-1GeV_ctau-1e0mm", "PATDSA")],
#     ("tta_mAlp-2GeV_ctau-1e0mm", 2): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e0mm", "PATDSA")],
#     ("tta_mAlp-12GeV_ctau-1e0mm", 12): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e0mm", "PATDSA")],
#     # ("tta_mAlp-30GeV_ctau-1e0mm", 30): signal_limits_over_lxy_significance[("tta_mAlp-30GeV_ctau-1e0mm", "PATDSA")],
#     ("tta_mAlp-60GeV_ctau-1e0mm", 60): signal_limits_over_lxy_significance[("tta_mAlp-60GeV_ctau-1e0mm", "PATDSA")],
#     # ("tta_mAlp-70GeV_ctau-1e0mm", 70): signal_limits_over_lxy_significance[("tta_mAlp-70GeV_ctau-1e0mm", "PATDSA")],
# }
# output_name = "BestPFIsoDimuonVertex_DSA_LxySignificance_1e0mm_mass"
# cross_section_limits = {
#     ("tta_mAlp-0p35GeV_ctau-1e0mm", 0.35): signal_limits_over_lxy_significance[("tta_mAlp-0p35GeV_ctau-1e0mm", "DSA")],
#     # ("tta_mAlp-1GeV_ctau-1e0mm", 1): signal_limits_over_lxy_significance[("tta_mAlp-1GeV_ctau-1e0mm", "DSA")],
#     ("tta_mAlp-2GeV_ctau-1e0mm", 2): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e0mm", "DSA")],
#     ("tta_mAlp-12GeV_ctau-1e0mm", 12): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e0mm", "DSA")],
#     # ("tta_mAlp-30GeV_ctau-1e0mm", 30): signal_limits_over_lxy_significance[("tta_mAlp-30GeV_ctau-1e0mm", "DSA")],
#     ("tta_mAlp-60GeV_ctau-1e0mm", 60): signal_limits_over_lxy_significance[("tta_mAlp-60GeV_ctau-1e0mm", "DSA")],
#     # ("tta_mAlp-70GeV_ctau-1e0mm", 70): signal_limits_over_lxy_significance[("tta_mAlp-70GeV_ctau-1e0mm", "DSA")],
# }
####  10 cm ALP  ####
# output_name = "BestPFIsoDimuonVertex_PAT_LxySignificance_1e2mm_mass"
# cross_section_limits = {
#     ("tta_mAlp-0p35GeV_ctau-1e2mm", 0.35): signal_limits_over_lxy_significance[("tta_mAlp-0p35GeV_ctau-1e2mm", "PAT")],
#     # ("tta_mAlp-1GeV_ctau-1e2mm", 1): signal_limits_over_lxy_significance[("tta_mAlp-1GeV_ctau-1e2mm", "PAT")],
#     ("tta_mAlp-2GeV_ctau-1e2mm", 2): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e2mm", "PAT")],
#     ("tta_mAlp-12GeV_ctau-1e2mm", 12): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e2mm", "PAT")],
#     # ("tta_mAlp-30GeV_ctau-1e2mm", 30): signal_limits_over_lxy_significance[("tta_mAlp-30GeV_ctau-1e2mm", "PAT")],
#     ("tta_mAlp-60GeV_ctau-1e2mm", 60): signal_limits_over_lxy_significance[("tta_mAlp-60GeV_ctau-1e2mm", "PAT")],
# }
# output_name = "BestPFIsoDimuonVertex_PATDSA_LxySignificance_1e2mm_mass"
# cross_section_limits = {
#     ("tta_mAlp-0p35GeV_ctau-1e2mm", 0.35): signal_limits_over_lxy_significance[("tta_mAlp-0p35GeV_ctau-1e2mm", "PATDSA")],
#     # ("tta_mAlp-1GeV_ctau-1e2mm", 1): signal_limits_over_lxy_significance[("tta_mAlp-1GeV_ctau-1e2mm", "PATDSA")],
#     ("tta_mAlp-2GeV_ctau-1e2mm", 2): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e2mm", "PATDSA")],
#     ("tta_mAlp-12GeV_ctau-1e2mm", 12): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e2mm", "PATDSA")],
#     # ("tta_mAlp-30GeV_ctau-1e2mm", 30): signal_limits_over_lxy_significance[("tta_mAlp-30GeV_ctau-1e2mm", "PATDSA")],
#     ("tta_mAlp-60GeV_ctau-1e2mm", 60): signal_limits_over_lxy_significance[("tta_mAlp-60GeV_ctau-1e2mm", "PATDSA")],
# }
# output_name = "BestPFIsoDimuonVertex_DSA_LxySignificance_1e2mm_mass"
# cross_section_limits = {
#     ("tta_mAlp-0p35GeV_ctau-1e2mm", 0.35): signal_limits_over_lxy_significance[("tta_mAlp-0p35GeV_ctau-1e2mm", "DSA")],
#     # ("tta_mAlp-1GeV_ctau-1e2mm", 1): signal_limits_over_lxy_significance[("tta_mAlp-1GeV_ctau-1e2mm", "DSA")],
#     ("tta_mAlp-2GeV_ctau-1e2mm", 2): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e2mm", "DSA")],
#     ("tta_mAlp-12GeV_ctau-1e2mm", 12): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e2mm", "DSA")],
#     # ("tta_mAlp-30GeV_ctau-1e2mm", 30): signal_limits_over_lxy_significance[("tta_mAlp-30GeV_ctau-1e2mm", "DSA")],
#     ("tta_mAlp-60GeV_ctau-1e2mm", 60): signal_limits_over_lxy_significance[("tta_mAlp-60GeV_ctau-1e2mm", "DSA")],
# }

#########  OVER CTAU  #########
# x_min = 1e-5 * 1e-3
# x_max = 1e5 * 1e-3
# x_title = "c#tau [m]"
####  2 GeV ALP  ####
# output_name = "BestPFIsoDimuonVertex_PAT_LxySignificance_2GeV_ctau"
# cross_section_limits = {
#     ("tta_mAlp-2GeV_ctau-1e-5mm", 1e-5*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e-5mm", "PAT")],
#     ("tta_mAlp-2GeV_ctau-1e0mm", 1e0*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e0mm", "PAT")],
#     ("tta_mAlp-2GeV_ctau-1e1mm", 1e1*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e1mm", "PAT")],
#     ("tta_mAlp-2GeV_ctau-1e2mm", 1e2*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e2mm", "PAT")],
#     ("tta_mAlp-2GeV_ctau-1e3mm", 1e3*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e3mm", "PAT")],
# }
# output_name = "BestPFIsoDimuonVertex_PATDSA_LxySignificance_2GeV_ctau"
# cross_section_limits = {
#     ("tta_mAlp-2GeV_ctau-1e-5mm", 1e-5*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e-5mm", "PATDSA")],
#     ("tta_mAlp-2GeV_ctau-1e0mm", 1e0*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e0mm", "PATDSA")],
#     ("tta_mAlp-2GeV_ctau-1e1mm", 1e1*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e1mm", "PATDSA")],
#     ("tta_mAlp-2GeV_ctau-1e2mm", 1e2*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e2mm", "PATDSA")],
#     ("tta_mAlp-2GeV_ctau-1e3mm", 1e3*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e3mm", "PATDSA")],
# }
# output_name = "BestPFIsoDimuonVertex_DSA_LxySignificance_2GeV_ctau"
# cross_section_limits = {
#     ("tta_mAlp-2GeV_ctau-1e-5mm", 1e-5*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e-5mm", "DSA")],
#     ("tta_mAlp-2GeV_ctau-1e0mm", 1e0*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e0mm", "DSA")],
#     ("tta_mAlp-2GeV_ctau-1e1mm", 1e1*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e1mm", "DSA")],
#     ("tta_mAlp-2GeV_ctau-1e2mm", 1e2*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e2mm", "DSA")],
#     ("tta_mAlp-2GeV_ctau-1e3mm", 1e3*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-2GeV_ctau-1e3mm", "DSA")],
# }
####  12 GeV ALP  ####
# output_name = "BestPFIsoDimuonVertex_PAT_LxySignificance_12GeV_ctau"
# cross_section_limits = {
#     ("tta_mAlp-12GeV_ctau-1e0mm", 1e0*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e0mm", "PAT")],
#     ("tta_mAlp-12GeV_ctau-1e1mm", 1e1*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e1mm", "PAT")],
#     ("tta_mAlp-12GeV_ctau-1e2mm", 1e2*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e2mm", "PAT")],
# }
# output_name = "BestPFIsoDimuonVertex_PATDSA_LxySignificance_12GeV_ctau"
# cross_section_limits = {
#     ("tta_mAlp-12GeV_ctau-1e0mm", 1e0*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e0mm", "PATDSA")],
#     ("tta_mAlp-12GeV_ctau-1e1mm", 1e1*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e1mm", "PATDSA")],
#     ("tta_mAlp-12GeV_ctau-1e2mm", 1e2*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e2mm", "PATDSA")],
# }
# output_name = "BestPFIsoDimuonVertex_DSA_LxySignificance_12GeV_ctau"
# # cross_section_limits = {
#     ("tta_mAlp-12GeV_ctau-1e0mm", 1e0*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e0mm", "DSA")],
#     ("tta_mAlp-12GeV_ctau-1e1mm", 1e1*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e1mm", "DSA")],
#     ("tta_mAlp-12GeV_ctau-1e2mm", 1e2*1e-3): signal_limits_over_lxy_significance[("tta_mAlp-12GeV_ctau-1e2mm", "DSA")],
# }


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

    exp_graph_2sigma.GetXaxis().SetTitle(x_title)
    exp_graph_2sigma.GetYaxis().SetTitle(
        "#sigma_{pp #rightarrow a #rightarrow #mu #mu} [pb]")

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

    tex2 = ROOT.TLatex(0.60, 0.92, "#scale[0.8]{pp, 60 fb^{-1} (#sqrt{s} = 13 TeV)}")
    tex2.SetNDC()
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.045)
    tex2.SetLineWidth(2)
    tex2.Draw()

    canvas.Update()
    canvas.SaveAs(f"../plots/limits_cross_section_{output_name}.pdf")
    

if __name__ == "__main__":
    main()
