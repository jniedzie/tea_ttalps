import ROOT
from copy import deepcopy
from ttalps_samples_list import dasBackgrounds2018
from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity
from Sample import Sample, SampleType
from Histogram import Histogram, Histogram2D
from HistogramNormalizer import NormalizationType

year = "2018"
base_path = "/data/dust/user/lrygaard/ttalps_cms"
skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "JPsiDimuonsDSAChi2DCADPhi", "LooseNonLeadingPATMuonsVertex_revertedMatching")
hist_path = f"histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_jecSFs"

samples = dasBackgrounds2018.keys()

background_samples = []
cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)
for sample in samples:
    background_samples.append(
        Sample(
            name=sample.split("/")[-1],
            file_path=f"{base_path}/{sample}/{skim[0]}/{hist_path}_{skim[1]}_{skim[2]}/histograms.root",
            type=SampleType.background,
            cross_sections=cross_sections,
            luminosity=luminosity,
        )
    )

variable = "BestDimuonVertex_DSA_invMass"
histogram = Histogram(
    name=variable,
    title="histogram",
    norm_type=NormalizationType.to_lumi,
    rebin=10,
)
cutflow_histogram = Histogram(
    name="cutFlow",
    title="cutFlow",
    norm_type=NormalizationType.to_lumi,
)

stack = ROOT.THStack("stack", "stack")
for sample in background_samples:
    root_file = ROOT.TFile.Open(sample.file_path, "READ")
    histogram.load(root_file)
    if not histogram.isGood():
        print(f"Error: Unable to load the histogram {histogram.name} from file: {sample.file_path}")
        root_file.Close()
        continue

    histogram.setup(sample)

    if histogram.hist.GetEntries() < 3:
        continue

    cross_section = sample.cross_section
    cutflow_histogram.load(root_file)
    if not cutflow_histogram.isGood():
        print(f"Error: Unable to load the histogram {cutflow_histogram.name} from file: {sample.file_path}")
        continue
    initial_weight_sum = cutflow_histogram.hist.GetBinContent(1)
    scale = luminosity*cross_section/initial_weight_sum
    histogram.hist.Scale(scale)

    stack.Add(deepcopy(histogram.hist))

hist_combined = stack.GetStack().Last()

hist_cut = hist_combined.Clone("histogram_cut")
invMass_max = 10
for i in range(1, hist_cut.GetNbinsX() + 1):
    if hist_cut.GetBinCenter(i) >= invMass_max:
        hist_cut.SetBinContent(i, 0)
        hist_cut.SetBinError(i, 0)

gaus = ROOT.TF1("gaus", "gaus", hist_cut.GetXaxis().GetXmin(), 10)
hist_cut.Fit(gaus, "R")
mean = gaus.GetParameter(1)
sigma = gaus.GetParameter(2)
print(f"Mean = {mean:.3f}, StdDev = {sigma:.3f}")

c = ROOT.TCanvas("c", "Canvas", 800, 600)
c.SetLogy()

hist_cut.SetStats(0)
hist_cut.SetMinimum(1e-3)
hist_cut.SetMaximum(1e5)
hist_cut.GetXaxis().SetRangeUser(0, 10)
hist_cut.SetFillColorAlpha(ROOT.kBlue, 0.)
hist_cut.SetFillColorAlpha(ROOT.kBlue, 0.4)
hist_cut.Draw("hist")
gaus.SetLineColor(ROOT.kBlack)
gaus.Draw("SAME")

latex = ROOT.TLatex()
ymin = 0
ymax = 0.9 * hist_cut.GetMaximum()
lines = []
def add_line(x, color, style):
    l = ROOT.TLine(x, ymin, x, ymax)
    l.SetLineColor(color)
    l.SetLineStyle(style)
    l.SetLineWidth(2)
    l.Draw()
    lines.append(l)
    latex.SetTextSize(0.03)
    latex.SetTextColor(color)
    latex.DrawLatex(x-0.1, ymax*1.1, f"{x:.1f}")

add_line(mean, ROOT.kRed, 1)
add_line(mean - sigma, ROOT.kGreen, 1)
add_line(mean + sigma, ROOT.kGreen, 1)
add_line(mean - 2*sigma, ROOT.kOrange, 1)
add_line(mean + 2*sigma, ROOT.kOrange, 1)

latex.SetNDC()
# Add text with mean and std
latex.SetTextSize(0.04)
latex.SetTextColor(ROOT.kBlack)
latex.DrawLatex(0.6, 0.85, f"Mean = {mean:.3f}")
latex.DrawLatex(0.6, 0.80, f"Sigma = {sigma:.3f}")

c.SaveAs("../hist_with_fit.png")
