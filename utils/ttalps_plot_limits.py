import ROOT
from ttalps_cross_sections import cross_sections

x_min = 1e-5 * 1e-3
x_max = 1e5 * 1e-3

y_min = 1e-3
y_max = 1e3

# output_name = "GoodBestLooseMuonsVertex_Pat_vxy"
# cross_section_limits = {
#     # converting ctau to meters
#     ("tta_mAlp-1GeV_ctau-1e-5mm",1e-5*1e-3): (0.3209,0.1714,0.2307,0.3203,0.4429,0.5819,),
#     ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (0.0206,0.0062,0.0108,0.0210,0.0394,0.0635,),
#     ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (0.0594,0.0180,0.0312,0.0591,0.1137,0.1791,),
#     ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (0.1052,0.0320,0.0554,0.1050,0.2021,0.3183,),
#     ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (4.9705,1.4945,2.6074,4.9688,9.6825,15.0668,),
#     ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (101.4040,40.0449,62.6105,101.5000,159.7600,235.3665,),
# }


# output_name = "GoodBestLooseMuonsVertex_Pat_vxySigma"
# cross_section_limits = {
# #     # converting ctau to meters
#     ("tta_mAlp-1GeV_ctau-1e-5mm",1e-5*1e-3): (0.1884,0.0709,0.1115,0.1890,0.3200,0.4970,),
#     ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (0.2750,0.1015,0.1616,0.2764,0.4680,0.7299,),
#     ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (0.9486,0.3388,0.5452,0.9531,1.6598,2.6564,),
#     ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (1.6295,0.5804,0.9422,1.6328,2.8564,4.5533,),
#     ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (59.3495,22.5449,35.5369,59.5000,98.8701,150.7992,),
#     ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (198.1594,104.6777,140.5941,198.5000,287.9089,414.9291,),
# }


# output_name = "GoodBestLooseMuonsVertex_Pat_vxySignificance"
# cross_section_limits = {
# #     # converting ctau to meters
#     ("tta_mAlp-1GeV_ctau-1e-5mm", 1e-5*1e-3): (0.4883,0.2594,0.3488,0.4883,0.6926,0.9495,),
#     ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (0.2664,0.0989,0.1566,0.2666,0.4600,0.7367,),
#     ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (0.7260,0.2498,0.4099,0.7266,1.3000,2.1667,),
#     ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (1.2783,0.4404,0.7229,1.2812,2.2925,3.8084,),
#     ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (49.9492,16.5601,28.0121,49.8750,88.4430,143.7601,),
#     ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (197.5441,86.1875,127.7422,197.0000,304.5793,452.9641,),
# }

# output_name = "GoodBestLooseMuonsVertex_PatDSA_vxy"
# cross_section_limits = {
# #     # converting ctau to meters
#     ("tta_mAlp-1GeV_ctau-1e-5mm", 1e-5*1e-3): (11.1244,5.6653,7.8531,11.1562,15.7366,20.9230,),
#     ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (7.7264,3.4814,5.0822,7.7500,11.7350,16.5878,),
#     ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (7.5893,3.1443,4.7433,7.5938,12.3763,18.6547,),
#     ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (11.2145,4.6582,7.0271,11.2500,18.1558,27.4369,),
#     ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (98.3065,49.1250,68.3145,98.2500,140.9375,190.8748,),
#     ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (163.3351,89.7773,118.3799,163.0000,224.7239,297.7494,),
# }

# output_name = "GoodBestLooseMuonsVertex_PatDSA_vxySigma"
# cross_section_limits = {
#     # converting ctau to meters
#     ("tta_mAlp-1GeV_ctau-1e-5mm", 1e-5*1e-3): (14.6575,7.2864,10.1196,14.6875,21.2445,29.3860,),
#     ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (12.4806,5.8105,8.3714,12.5000,18.6285,26.1997,),
#     ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (19.2101,8.8442,12.8038,19.1875,28.9007,41.0931,),
#     ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (28.9203,13.5645,19.4494,28.9375,43.1251,60.8275,),
#     ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (140.2884,71.6406,97.8094,140.0000,201.9431,279.7404,),
#     ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (204.6176,103.9746,142.5527,204.7500,296.1579,409.6527,),
# }

# output_name = "GoodBestLooseMuonsVertex_PatDSA_vxySignificance"
# cross_section_limits = {
#     # converting ctau to meters
#     ("tta_mAlp-1GeV_ctau-1e-5mm", 1e-5*1e-3): (11.6362,6.4028,8.4835,11.6250,15.8417,20.6426,),
#     ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (10.6865,5.7195,7.6989,10.6875,14.7346,19.2451,),
#     ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (14.5155,6.8831,9.8228,14.5625,21.0637,28.5917,),
#     ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (23.4188,11.8701,16.3642,23.3750,32.9719,43.8386,),
#     ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (111.5216,62.2832,81.8930,111.5000,151.9444,197.9912,),
#     ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (159.0917,88.6768,116.5966,158.7500,216.3334,283.9745,),
# }

# output_name = "GoodBestLooseMuonsVertex_DSA_vxy"
# cross_section_limits = {
#     # converting ctau to meters
#     ("tta_mAlp-1GeV_ctau-1e-5mm", 1e-5*1e-3): (13.0653,6.8374,9.2691,13.0625,18.2693,24.3864,),
#     ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (10.9287,5.7251,7.7612,10.9375,15.3408,20.5904,),
#     ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (3.3955,1.6688,2.3280,3.3906,5.0260,7.1108,),
#     ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (4.2173,2.0435,2.8592,4.2188,6.2535,8.8990,),
#     ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (21.3198,8.6582,13.3047,21.3125,34.2253,51.6671,),
#     ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (95.2802,43.1602,63.1008,95.2500,141.1901,196.2794,),
# }

# output_name = "GoodBestLooseMuonsVertex_DSA_vxySigma"
# cross_section_limits = {
#     # converting ctau to meters
#     ("tta_mAlp-1GeV_ctau-1e-5mm", 1e-5*1e-3): (24.2557,12.3145,16.8835,24.2500,35.0761,48.8202,),
#     ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (21.7377,10.9285,15.0472,21.6875,31.6289,44.0966,),
#     ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (14.5997,7.0840,9.9119,14.6250,21.8537,31.3076,),
#     ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (19.7662,9.7207,13.4817,19.7500,29.3544,41.7073,),
#     ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (104.6960,53.0664,72.3540,104.5000,152.8188,214.6752,),
#     ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (214.9112,112.5391,151.7624,215.0000,310.1269,429.6013,),
# }

# output_name = "GoodBestLooseMuonsVertex_DSA_vxySignificance"
# cross_section_limits = {
#     # converting ctau to meters
#     ("tta_mAlp-1GeV_ctau-1e-5mm", 1e-5*1e-3): (12.3831,6.8816,9.0828,12.4062,16.9064,22.0299,),
#     ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (9.8210,5.2129,7.0096,9.8125,13.7238,18.3190,),
#     ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (2.9218,1.5180,2.0554,2.9219,4.1914,5.7498,),
#     ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (3.4823,1.7966,2.4559,3.4844,4.9705,6.7942,),
#     ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (19.5230,10.2070,13.6919,19.5000,28.3610,40.0827,),
#     ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (97.0200,49.6367,67.7680,97.0000,139.1444,188.4463,),
# }

output_name = "GoodBestLooseMuonsVertex_combined_vxy"
cross_section_limits = {
    # converting ctau to meters
    ("tta_mAlp-1GeV_ctau-1e-5mm", 1e-5*1e-3): (0.2318,0.1230,0.1653,0.2314,0.3246,0.4357,),
    ("tta_mAlp-1GeV_ctau-1e0mm", 1e0*1e-3): (0.0205,0.0062,0.0108,0.0210,0.0394,0.0635,),
    ("tta_mAlp-1GeV_ctau-1e1mm", 1e1*1e-3): (0.0591,0.0180,0.0312,0.0591,0.1132,0.1791,),
    ("tta_mAlp-1GeV_ctau-1e2mm", 1e2*1e-3): (0.1045,0.0318,0.0551,0.1045,0.2003,0.3168,),
    ("tta_mAlp-1GeV_ctau-1e3mm", 1e3*1e-3): (4.3650,1.3501,2.3426,4.3750,8.2464,13.2642,),
    ("tta_mAlp-1GeV_ctau-1e5mm", 1e5*1e-3): (67.5304,25.5762,40.9701,67.5000,107.8587,156.5582,),
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

    tex2 = ROOT.TLatex(0.60, 0.92, "#scale[0.8]{pp, 60 fb^{-1} (#sqrt{s_{NN}} = 13 TeV)}")
    tex2.SetNDC()
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.045)
    tex2.SetLineWidth(2)
    tex2.Draw()

    canvas.Update()
    canvas.SaveAs(f"../plots/limits_cross_section_{output_name}.pdf")
    

if __name__ == "__main__":
    main()
