import ROOT
import math
import re
import os
from ttalps_samples_list import dasSignals2018
from Histogram import Histogram
from HistogramNormalizer import NormalizationType
from Sample import Sample, SampleType
from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity

year = "2018"
base_path = "/data/dust/user/lrygaard/ttalps_cms"

skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "SRDimuons", "withLeadingTightMuon_genInfo")
hist_path = f"histograms_dimuonEffSFs_{skim[1]}_{skim[2]}"

cross_sections = get_cross_sections(year)
luminosity = get_luminosity(year)
samples = []
for signal in dasSignals2018.keys():
    samples.append(
        Sample(
            name=signal.split("/")[-1],
            file_path=f"{base_path}/{signal}/{skim[0]}/{hist_path}/histograms.root",
            type=SampleType.signal,
            cross_sections=cross_sections,
            luminosity=luminosity,
            line_alpha=0,
            line_style=1,
            fill_alpha=0.7,
            marker_size=0,
            marker_style=0,
            year=year,
        )
    )

# leading_from_alp = "TightMuonsSegmentMatchFromALP_hmu_hasLeadingMuon"
# leading_from_w = "TightMuonsSegmentMatchFromW_hmu_hasLeadingMuon"
leading_from_alp = "TightMuonsSegmentMatchFromALP_hasLeadingMuon"
leading_from_w = "TightMuonsSegmentMatchFromW_hasLeadingMuon"
hist_from_alp = Histogram(
    name=leading_from_alp,
    title=leading_from_alp,
    norm_type=NormalizationType.to_lumi,
)
hist_from_w = Histogram(
    name=leading_from_w,
    title=leading_from_w,
    norm_type=NormalizationType.to_lumi,
)

def get_ratio_and_uncertainties(hist):
    n_leading = hist.GetBinContent(2)
    n_leading_err = hist.GetBinError(2)
    n_nonleading = hist.GetBinContent(1)
    n_nonleading_err = hist.GetBinError(1)
    n_tot = n_leading + n_nonleading
    r = n_leading / n_tot

    sigma_r = math.sqrt(
        ((n_nonleading / n_tot**2)**2) * n_leading_err**2 +
        ((n_leading / n_tot**2)**2) * n_nonleading_err**2
    )

    if (n_leading_err > 0 or n_nonleading_err > 0):
        # Effective total counts (accounts for weights)
        n_eff = (n_tot)**2 / (n_leading_err**2 + n_nonleading_err**2) if (n_leading_err**2 + n_nonleading_err**2) > 0 else 0
        k_eff = r * n_eff

        if n_eff > 0:
            low = ROOT.TEfficiency.ClopperPearson(int(round(n_eff)), int(round(k_eff)), 0.683, False)
            high = ROOT.TEfficiency.ClopperPearson(int(round(n_eff)), int(round(k_eff)), 0.683, True)
            err_low = r - low
            err_high = high - r
        else:
            err_low = err_high = sigma_r
    else:
        err_low = err_high = sigma_r
    return r, err_low, err_high

ratios_leading_from_alp = {}
ratios_leading_from_w = {}
for sample in samples:
    print(f"Sample: {sample.name}")
    match = re.search(r"mAlp-([\d\.p]+)GeV_ctau-([\deE\-\+]+)mm", sample.name)
    mass_str, ctau_str = match.groups()
    mass = float(mass_str.replace("p", "."))  # handle '0p35' style
    ctau = float(ctau_str)
    print(mass, ctau)

    root_file = ROOT.TFile.Open(sample.file_path, "READ")
    hist_from_alp.load(root_file)
    hist_from_w.load(root_file)

    hist_from_alp.setup(sample)
    hist_from_w.setup(sample)

    cut_flow = root_file.Get("cutFlow")
    sample.initial_weight_sum = cut_flow.GetBinContent(1)
    scale = sample.cross_section * sample.luminosity / sample.initial_weight_sum
    hist_from_alp.hist.Scale(scale)
    hist_from_w.hist.Scale(scale)

    r_alp, r_low_alp, r_high_alp = get_ratio_and_uncertainties(hist_from_alp.hist)    
    r_w, r_low_w, r_high_w = get_ratio_and_uncertainties(hist_from_w.hist)    
    
    print(f"Ratio leading tight muon from ALP: {r_alp:.3f} + {r_high_alp:.3f} - {r_low_alp:.3f}")
    print(f"Ratio leading tight muon from W: {r_w:.3f} + {r_high_w:.3f} - {r_low_w:.3f}")

    ratios_leading_from_alp[(mass,ctau)] = r_alp
    ratios_leading_from_w[(mass,ctau)] = r_w


masses = sorted(set(m for m, c in ratios_leading_from_alp.keys()))
cta_values = sorted(set(c for m, c in ratios_leading_from_alp.keys()))
h2 = ROOT.TH2D("ratios_leading_from_alp", "Fraction of events with leading muon from ALP;m_{a} [GeV];c#tau_{a} [mm]",
               len(masses), 0, len(masses),
               len(cta_values), 0, len(cta_values))
h2_w = ROOT.TH2D("ratios_leading_from_w", "Fraction of events with leading muon from W;m_{a} [GeV];c#tau_{a} [mm]",
               len(masses), 0, len(masses),
               len(cta_values), 0, len(cta_values))
for i, m in enumerate(masses):
    h2.GetXaxis().SetBinLabel(i+1, str(m))
    h2_w.GetXaxis().SetBinLabel(i+1, str(m))
for j, c in enumerate(cta_values):
    h2.GetYaxis().SetBinLabel(j+1, str(c))
    h2_w.GetYaxis().SetBinLabel(j+1, str(c))

for (mass, ctau), ratio in ratios_leading_from_alp.items():
    ix = masses.index(mass) + 1
    iy = cta_values.index(ctau) + 1
    if ratio == 0.0:
        ratio = 0.0000000001
    h2.SetBinContent(ix, iy, ratio)
    h2_w.SetBinContent(ix, iy, ratios_leading_from_w[(mass,ctau)])

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat(".3f")

h2.SetMinimum(0)
h2_w.SetMinimum(0)

if not os.path.exists("../plots/leading_muon_study"):
    os.makedirs("../plots/leading_muon_study")

c = ROOT.TCanvas("c", "c", 800, 600)
h2.Draw("COLZ TEXT")
c.SetRightMargin(0.15)
c.SaveAs("../plots/leading_muon_study/ratios_leading_from_alp.pdf")

c_w = ROOT.TCanvas("c_w", "c_w", 800, 600)
h2_w.Draw("COLZ TEXT")
c_w.SetRightMargin(0.15)
c_w.SaveAs("../plots/leading_muon_study/ratios_leading_from_w.pdf")

significance_excluding_leading_muon = {}
significance_excluding_leading_muon[0.35] = (4.1, 5.63, 4.37, 1.21, 0.22)
significance_excluding_leading_muon[2] = (2.05, 5.64, 6.18, 4.97, 1.35)
significance_excluding_leading_muon[12] = (0.96, 5.25, 7.61, 12.68, 8.76)
significance_excluding_leading_muon[30] = (0.67, 2.97, 7.58, 12.28, 12.45)
significance_excluding_leading_muon[60] = (0.33, 2.97, 6.43, 9.47, 11.30)
significance_including_leading_muon = {}
significance_including_leading_muon[0.35] = (12.39, 6.11, 1.73, 0.31, 0.05)
significance_including_leading_muon[2] = (5.22, 12.53, 4.65, 1.62, 0.31)
significance_including_leading_muon[12] = (2.74, 15.47, 8.36, 5.93, 2.96)
significance_including_leading_muon[30] = (1.54, 15.42, 9.02, 5.83, 5.09)
significance_including_leading_muon[60] = (0.73, 12.88, 8.16, 4.24, 4.38)

h2_sig_excluding_leading = ROOT.TH2D("sig_excluding_leading", "Signal siginificance without leading muon;m_{a} [GeV];c#tau_{a} [mm]; S / #sqrt{S+B}",
               len(masses), 0, len(masses),
               len(cta_values), 0, len(cta_values))
h2_sig_including_leading = ROOT.TH2D("sig_including_leading", "Signal siginificance with leading muon;m_{a} [GeV];c#tau_{a} [mm]; S / #sqrt{S+B}",
               len(masses), 0, len(masses),
               len(cta_values), 0, len(cta_values))
h2_sig_excluding_over_including_leading = ROOT.TH2D("sig_excluding_over_including_leading", "Signal siginificance ratio of excluding / including leading tight muon;m_{a} [GeV];c#tau_{a} [mm]; Ratio",
               len(masses), 0, len(masses),
               len(cta_values), 0, len(cta_values))
for i, m in enumerate(masses):
    h2_sig_excluding_leading.GetXaxis().SetBinLabel(i+1, str(m))
    h2_sig_including_leading.GetXaxis().SetBinLabel(i+1, str(m))
for j, c in enumerate(cta_values):
    h2_sig_excluding_leading.GetYaxis().SetBinLabel(j+1, str(c))
    h2_sig_including_leading.GetYaxis().SetBinLabel(j+1, str(c))

for i, m in enumerate(masses):
    for j, c in enumerate(cta_values):
        sig_excl = significance_excluding_leading_muon[m][j]
        sig_incl = significance_including_leading_muon[m][j]
        h2_sig_excluding_leading.SetBinContent(i+1, j+1, sig_excl)
        h2_sig_including_leading.SetBinContent(i+1, j+1, sig_incl)
        h2_sig_excluding_over_including_leading.SetBinContent(i+1, j+1, sig_excl/sig_incl if sig_incl != 0 else 0)

c1 = ROOT.TCanvas("c1", "c1", 800, 600)
h2_sig_excluding_leading.Draw("COLZ TEXT")
c1.SetRightMargin(0.15)
c1.SaveAs("../plots/leading_muon_study/significance_excluding_leading_muon.pdf")

c2 = ROOT.TCanvas("c2", "c2", 800, 600)
h2_sig_including_leading.Draw("COLZ TEXT")
c2.SetRightMargin(0.15)
c2.SaveAs("../plots/leading_muon_study/significance_including_leading_muon.pdf")

c3 = ROOT.TCanvas("c3", "c3", 800, 600)
h2_sig_excluding_over_including_leading.Draw("COLZ TEXT")
c3.SetRightMargin(0.15)
c3.SaveAs("../plots/leading_muon_study/significance_excluding_over_including_leading_muon.pdf")
