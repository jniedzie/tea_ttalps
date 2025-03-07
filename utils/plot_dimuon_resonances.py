import ROOT

topMargin = 0.06
bottomMargin = 0.3
leftMargin = 0.16
rightMargin = 0.15
ROOT.gStyle.SetPadTopMargin(topMargin)
ROOT.gStyle.SetPadBottomMargin(bottomMargin)
ROOT.gStyle.SetPadLeftMargin(leftMargin)
ROOT.gStyle.SetPadRightMargin(rightMargin)

ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetCanvasColor(ROOT.kWhite)

ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(ROOT.kWhite)
ROOT.gStyle.SetPadGridX(False)
ROOT.gStyle.SetPadGridY(False)
ROOT.gStyle.SetGridColor(0)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridWidth(1)

ROOT.gStyle.SetFrameBorderMode(0)
ROOT.gStyle.SetFrameBorderSize(1)
ROOT.gStyle.SetFrameFillColor(0)
ROOT.gStyle.SetFrameFillStyle(0)
ROOT.gStyle.SetFrameLineColor(1)
ROOT.gStyle.SetFrameLineStyle(1)
ROOT.gStyle.SetFrameLineWidth(1)

ROOT.gStyle.SetHistLineColor(1)
ROOT.gStyle.SetHistLineStyle(0)
ROOT.gStyle.SetHistLineWidth(1)

ROOT.gStyle.SetEndErrorSize(2)

ROOT.gStyle.SetOptFit(1)
ROOT.gStyle.SetFitFormat("5.4g")
ROOT.gStyle.SetFuncColor(2)
ROOT.gStyle.SetFuncStyle(1)
ROOT.gStyle.SetFuncWidth(1)

ROOT.gStyle.SetOptDate(0)
ROOT.gStyle.SetOptFile(0)

ROOT.gStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
ROOT.gStyle.SetStatColor(ROOT.kWhite)
ROOT.gStyle.SetStatFont(42)
ROOT.gStyle.SetStatFontSize(0.025)
ROOT.gStyle.SetStatTextColor(1)
ROOT.gStyle.SetStatFormat("6.4g")
ROOT.gStyle.SetStatBorderSize(1)
ROOT.gStyle.SetStatH(0.1)
ROOT.gStyle.SetStatW(0.15)

ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetTitleFont(42)
ROOT.gStyle.SetTitleColor(1)
ROOT.gStyle.SetTitleTextColor(1)
ROOT.gStyle.SetTitleFillColor(10)
ROOT.gStyle.SetTitleFontSize(0.05)

ROOT.gStyle.SetTitleColor(1, "XYZ")
ROOT.gStyle.SetTitleFont(42, "XYZ")
ROOT.gStyle.SetTitleSize(0.06, "XYZ")
ROOT.gStyle.SetTitleXOffset(0.9)
ROOT.gStyle.SetTitleYOffset(1.25)

ROOT.gStyle.SetLabelColor(1, "XYZ")
ROOT.gStyle.SetLabelFont(42, "XYZ")
ROOT.gStyle.SetLabelOffset(0.007, "XYZ")
ROOT.gStyle.SetLabelSize(0.05, "XYZ")

ROOT.gStyle.SetAxisColor(1, "XYZ")
ROOT.gStyle.SetStripDecimals(True)
ROOT.gStyle.SetTickLength(0.03, "XYZ")
ROOT.gStyle.SetNdivisions(510, "XYZ")
ROOT.gStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
ROOT.gStyle.SetPadTickY(1)

ROOT.gStyle.SetOptLogx(0)
ROOT.gStyle.SetOptLogy(1)
ROOT.gStyle.SetOptLogz(0)

ROOT.gStyle.SetPaperSize(20.,20.)

# Open the ROOT file (assuming all histograms are stored in the same file)
signal_samples = {
    "tta_mAlp-2GeV_ctau-1e0mm" : "m_{a} = 2 GeV, c#tau_{a} = 1 mm",
    "tta_mAlp-2GeV_ctau-1e2mm" : "m_{a} = 2 GeV, c#tau_{a} = 10 cm",
    "tta_mAlp-12GeV_ctau-1e0mm" : "m_{a} = 12 GeV, c#tau_{a} = 1 mm",
}


for signal_sample in signal_samples.keys():
    filename=f"/data/dust/user/lrygaard/ttalps_cms/signals/{signal_sample}/skimmed_looseSemimuonic_v2_SR/histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons/histograms.root"

    file = ROOT.TFile.Open(filename)

    # create an empty hist
    hist0 = ROOT.TH1F("hist0", "hist0", 100, 0, 3.15)

    variables ={
    #   name    xaxis   xmin   xmax   rebin
        "Pat_pfRelIso04all1" : ("#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )", 0, 1, 1),
        "Pat_pfRelIso04all2" : ("#mu_{2} I_{PF}^{rel} ( #Delta R < 0.4 )", 0, 1, 1),
        "PatDSA_pfRelIso04all1" : ("#mu_{1} I_{PF}^{rel} ( #Delta R < 0.4 )", 0, 1, 1),
        "Pat_Lxy" : ("L_{xy} [cm]", 0, 60, 1),
        "PatDSA_Lxy" : ("L_{xy} [cm]", 0, 400, 10),
        "DSA_Lxy" : ("L_{xy} [cm]", 0, 500, 10),
        "Pat_LxySignificance" : ("L_{xy} significance [cm]", 0, 100, 1),
        "PatDSA_LxySignificance" : ("L_{xy} significance [cm]", 0, 100, 1),
        "DSA_LxySignificance" : ("L_{xy} significance [cm]", 0, 50, 1),
        "Pat_LxySigma" : ("#sigma_{Lxy}", 0, 20, 20),
        "PatDSA_LxySigma" : ("#sigma_{Lxy}", 0, 100, 100),
        "DSA_LxySigma" : ("#sigma_{Lxy}", 0, 100, 100),
    }

    collections = ["LooseMuonsFromALPSegmentMatchVertex", "LooseDimuonsNotFromALPSegmentMatchVertex", "LooseNonResonantDimuonsSegmentMatchVertex"]
    # collections = ["GoodPFIsoDimuonVertexFromALP", "GoodPFIsoDimuonVertexResonancesNotFromALP", "GoodPFIsoDimuonVertexNonresonancesNotFromALP"]

    # loop over variables map:
    for variable in variables.keys():
        # Retrieve histograms from the file
        print(f"Plotting {variable} for {signal_sample}")
        hist_fromALP_Pat1 = file.Get(f"{collections[0]}_{variable}")
        hist_resonantNoFromALP_Pat1 = file.Get(f"{collections[1]}_{variable}")
        hist_nonresonantNoFromALP_Pat1 = file.Get(f"{collections[2]}_{variable}")

        factor = variables[variable][3]  # Rebinning factor
        hist_fromALP_Pat1 = hist_fromALP_Pat1.Rebin(factor)
        hist_resonantNoFromALP_Pat1 = hist_resonantNoFromALP_Pat1.Rebin(factor)
        hist_nonresonantNoFromALP_Pat1 = hist_nonresonantNoFromALP_Pat1.Rebin(factor)
        # hist_nonresonantNoFromALP_Pat1.Scale(1./factor)
        # hist_resonantNoFromALP_Pat1.Scale(1./factor)
        # hist_nonresonantNoFromALP_Pat1.Scale(1./factor)

        if hist_fromALP_Pat1.Integral() > 0:
            hist_fromALP_Pat1.Scale(1./hist_fromALP_Pat1.Integral())
        if hist_resonantNoFromALP_Pat1.Integral() > 0:
            hist_resonantNoFromALP_Pat1.Scale(1./hist_resonantNoFromALP_Pat1.Integral())
        if hist_nonresonantNoFromALP_Pat1.Integral() > 0:
            hist_nonresonantNoFromALP_Pat1.Scale(1./hist_nonresonantNoFromALP_Pat1.Integral())

        # Set up a canvas to draw the plots
        canvas = ROOT.TCanvas("canvas", "Multihists", 800, 600)
        canvas.Divide(1, 1)  # Create one pad if none exist
        pad = canvas.GetPad(1)
        canvas.SetLeftMargin(leftMargin)
        canvas.SetBottomMargin(bottomMargin)
        canvas.SetRightMargin(rightMargin)
        canvas.SetTopMargin(topMargin)
        canvas.SetTickx(0)
        canvas.SetTicky(0)
        canvas.SetBottomMargin(0.2)
        canvas.SetTopMargin(topMargin + 0.03)

        pad.cd()
        # Set marker style and color for each plot
        hist_fromALP_Pat1.SetLineColor(ROOT.kBlue)
        hist_fromALP_Pat1.SetMarkerColor(ROOT.kBlue)
        hist_fromALP_Pat1.SetMarkerStyle(20)

        hist_resonantNoFromALP_Pat1.SetLineColor(ROOT.kGreen+1)
        hist_resonantNoFromALP_Pat1.SetMarkerColor(ROOT.kGreen+1)
        hist_resonantNoFromALP_Pat1.SetMarkerStyle(20)

        hist_nonresonantNoFromALP_Pat1.SetLineColor(ROOT.kOrange+1)
        hist_nonresonantNoFromALP_Pat1.SetMarkerColor(ROOT.kOrange+1)
        hist_nonresonantNoFromALP_Pat1.SetMarkerStyle(20)

        # canvas.GetPad(1).SetLogy()

        # # Now set the axis titles AFTER drawing the efficiency objects
        hist0.GetXaxis().SetTitle(variables[variable][0])
        hist0.GetYaxis().SetTitle("Fraction of events (2018)")
        hist0.GetXaxis().SetTitleSize(0.04)
        hist0.GetXaxis().SetLabelSize(0.04)
        hist0.GetXaxis().SetTitleOffset(1.7)
        hist0.GetYaxis().SetTitleSize(0.05)
        hist0.GetYaxis().SetLabelSize(0.06)
        hist0.GetYaxis().SetTitleOffset(1.5)
        hist0.SetMaximum(1e2)
        hist0.SetMinimum(1e-6)
        hist0.GetXaxis().SetLimits(variables[variable][1], variables[variable][2])

        # Draw the TEfficiency objects on the same canvas
        hist0.Draw("hist")  # Draw the first efficiency with axis
        hist_fromALP_Pat1.Draw("hist SAME")  # Draw the first efficiency with axis
        hist_resonantNoFromALP_Pat1.Draw("hist SAME")  # Draw others on the same canvas
        hist_nonresonantNoFromALP_Pat1.Draw("hist SAME")

        canvas.Update()

        # Add a legend to describe the plots
        legend = ROOT.TLegend(0.42, 0.76, 0.85, 0.85)
        legend.AddEntry(hist_fromALP_Pat1, "Dimuons from ALPs", "l")
        legend.AddEntry(hist_resonantNoFromALP_Pat1, "Dimuons not from ALPs", "l")
        legend.AddEntry(hist_nonresonantNoFromALP_Pat1, "Non-resonant dimuons", "l")
        legend.SetBorderSize(0)
        # legend.SetFillColor(0)
        # legend.SetFillStyle(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
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
        lumiText = lumi + " (13 TeV)"
        latex.DrawLatex(1-right, 1-top+0.04, lumiText)

        xmax = variables[variable][2]
        posX_ = 0.05*xmax
        bottom = canvas.GetBottomMargin()
        posY_ = 1-top - 0.070*(1-bottom) + 40
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
        latex.DrawLatex(posX_, posY_ - 30 , "Preliminary")

        latex = ROOT.TLatex()
        latex.SetTextFont(42)
        latex.SetTextAlign(13)
        extraTextSize = 0.76 * 0.55*top
        latex.SetTextSize(0.76*0.55*top)
        posX_ = 0.42*xmax
        latex.DrawLatex(posX_, posY_, signal_samples[signal_sample])
        posY_ = 6*top
        category_ = ""
        if "PatDSA" in variable:
            category_ = "PAT-DSA"
        elif "Pat" in variable:
            category_ = "PAT-PAT"
        elif "DSA" in variable:
            category_ = "DSA-DSA"
        latex.DrawLatex(posX_, posY_, category_)

        # Redraw the axes
        # make sure plot border is on top of everything else
        pad.GetFrame().SetLineWidth(2)
        pad.GetFrame().SetBorderSize(2)
        pad.GetFrame().SetBorderMode(0)
        pad.GetFrame().SetFillColor(0)
        pad.GetFrame().SetFillStyle(0)
        pad.RedrawAxis()
        canvas.RedrawAxis()

        # Update and save the canvas
        canvas.Update()
        ROOT.gSystem.mkdir("../plots/dimuon_resonances", True)
        canvas.SaveAs(f"../plots/dimuon_resonances/{collections[0]}_{variable}_{signal_sample}.png")

        # Keep the canvas open in interactive mode
        canvas.Draw()
