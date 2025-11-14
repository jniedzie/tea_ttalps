import ROOT
from array import array

beam_spot_sigma_z = 3.9  # in cm


def main():
  canvas = ROOT.TCanvas("canvas", "Delta Z Distribution", 800, 400)
  canvas.Divide(2, 1)

  # Left panel
  canvas.cd(1)
  gauss = ROOT.TF1("gauss", "gaus", -20, 20)
  gauss.SetParameters(1, 0, beam_spot_sigma_z)  # amplitude, mean, sigma
  gauss.SetTitle(f"Gaussian Distribution (sigma={beam_spot_sigma_z:.1f} cm);z (cm);Density")
  gauss.Draw()

  # Right panel
  canvas.cd(2)
  ROOT.gPad.SetLogx()

  nBins = 20
  log_bins = []
  for i in range(nBins + 1):
    log_bins.append(10 ** (-5 + i * (8 / nBins)))

  deltaZHist = ROOT.TH1F("deltaZ", "|z| distribution;#Delta z (cm);Entries", nBins, array('d', log_bins))
  deltaZHist.SetLineColor(ROOT.kRed)
  deltaZHist.SetFillColorAlpha(ROOT.kRed, 0.3)

  nEntries = 1000
  for _ in range(nEntries):
    x1 = gauss.GetRandom()
    x2 = gauss.GetRandom()
    deltaZ = abs(x1 - x2)
    deltaZHist.Fill(deltaZ)

  deltaZHist.Draw("hist")

  canvas.Update()
  canvas.SaveAs("../plots/gauss_test.pdf")


if __name__ == "__main__":
  main()
