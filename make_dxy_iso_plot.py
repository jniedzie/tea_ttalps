import ROOT
from array import array

def make_diff_plot():

    # -------------------------
    # EVEN x bins
    # -------------------------
    nx = 5
    ny = 5

    xlow, xhigh = 0.35, 80.0
    xbins = array('d', [xlow + i*(xhigh - xlow)/nx for i in range(nx+1)])

    # y bins (bottom → top)
    ybins = array('d', [0, 1, 2, 3, 4, 5])

    h = ROOT.TH2D(
        "h",
        "PAT-DSA;m_{a} [GeV];c#tau_{a}",
        nx, xbins,
        ny, ybins
    )

    # -------------------------
    # data (top row = largest ctau)
    # -------------------------
    diff = [

        # PAT-PAT 2018
        # [ 1.0,  1.0,  0.0,  0.0,  0.0],     
        # [ 0.0,  0.3,  1.0,  2.0,  2.0],
        # [ 1.0, 11.0, 20.0, 20.0, 26.0],
        # [ 5.0, 20.0, 43.0, 34.0, 39.0],
        # [ 1.8, 14.1, 38.7, 45.1, 52.5],

        # PAT-DSA 2018
        # [ 1.0,  1.0,  0.0,  5.0,  1.0],     
        # [ 8.0,  4.0,  2.0,  0.0,  3.0],
        # [15.0, 16.0, 19.0, 36.0, 21.0],
        # [17.0, 21.3, 43.5, 50.0, 46.0],
        # [11.0, 18.0, 36.0, 42.0, 13.0],
        
        # PAT-PAT All years
        # [  1,    0,     0,      1,    0],
        # [  0,    2,     1,      1,    1],
        # [  2,   11,    20,     21,   25],
        # [  5,   21,    40,     38,   39],
        # [1.4, 13.7,  34.8,   43.2,   50],

        # PAT-DSA All years
        [ 1,  0,  2,  1,  0  ],
        [ 7,  2,  0,  2,  2  ],
        [15, 16, 21, 27, 22  ],
        [19, 21, 44, 52, 56  ],
        [13, 22, 40, 46, 49  ],

    ]


    # fill normally (NO inversion)
    for i in range(ny):
        for j in range(nx):
            h.SetBinContent(j+1, i+1, diff[i][j])

    # -------------------------
    # style
    # -------------------------
    ROOT.gStyle.SetOptStat(0)

    c = ROOT.TCanvas("c", "c", 800, 600)
    c.SetRightMargin(0.15)

    h.GetZaxis().SetTitle("Efficiency difference [%]")
    h.GetZaxis().SetRangeUser(0, 100)
    h.GetZaxis().SetTitleOffset(1.20)

    h.Draw("COLZ TEXT")

    # -------------------------
    # x labels
    # -------------------------
    xlabels = ["0.35", "2", "12", "30", "60"]
    for i in range(nx):
        h.GetXaxis().SetBinLabel(i+1, xlabels[i])

    # -------------------------
    # y labels (BOTTOM → TOP = 1mm → 1m)
    # -------------------------
    ylabels = ["1nm", "1 mm", "1 cm", "10 cm", "1 m"]

    for i in range(ny):
        h.GetYaxis().SetBinLabel(i+1, ylabels[i])

    h.GetXaxis().SetTitle("m_{a} [GeV]")
    h.GetYaxis().SetTitle("c#tau_{a}")

    # c.SetGrid()
    c.SaveAs("efficiency_difference_PatDSA.pdf")


if __name__ == "__main__":
    make_diff_plot()