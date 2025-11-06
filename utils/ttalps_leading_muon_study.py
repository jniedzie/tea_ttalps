import ROOT
import math
import re
from ttalps_samples_list import dasSignals2018
from Histogram import Histogram
from HistogramNormalizer import NormalizationType
from Sample import Sample, SampleType
from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity

year = "2018"
base_path = "/data/dust/user/lrygaard/ttalps_cms"

skim = ("skimmed_looseSemimuonic_v2_SR_segmentMatch1p5", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch_genInfo")
hist_path = f"histograms_muonSFs_dsamuonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_dimuonEffSFs_jecSFs_L1PreFiringWeightSFs_{skim[1]}_{skim[2]}"

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

leading_from_alp = "TightMuonsSegmentMatchFromALP_hmu_hasLeadingMuon"
leading_from_w = "TightMuonsSegmentMatchFromW_hmu_hasLeadingMuon"
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

    n_from_alp_with_leading_muon = hist_from_alp.hist.GetBinContent(2)
    n_from_alp_without_leading_muon = hist_from_alp.hist.GetBinContent(1)
    n_from_alp_tot = hist_from_alp.hist.GetBinContent(1) + hist_from_alp.hist.GetBinContent(2)
    r_from_alp_with_leading_muon = n_from_alp_with_leading_muon / n_from_alp_tot
    r_from_alp_with_leading_muon_unc = math.sqrt(n_from_alp_with_leading_muon*n_from_alp_without_leading_muon/(n_from_alp_tot**3))
    print(f"Ratio leading tight muon from ALP: {r_from_alp_with_leading_muon:.3f} +- {r_from_alp_with_leading_muon_unc:.3f}")

    n_from_w_with_leading_muon = hist_from_w.hist.GetBinContent(2)
    n_from_w_without_leading_muon = hist_from_w.hist.GetBinContent(1)
    n_from_w_tot = hist_from_w.hist.GetBinContent(1) + hist_from_w.hist.GetBinContent(2)
    r_from_w_with_leading_muon = n_from_w_with_leading_muon / n_from_w_tot
    r_from_w_with_leading_muon_unc = math.sqrt(n_from_w_with_leading_muon*n_from_w_without_leading_muon/(n_from_w_tot**3))
    print(f"Ratio leading tight muon from W: {r_from_w_with_leading_muon:.3f} +- {r_from_w_with_leading_muon_unc:.3f}")

    print(f"n_from_alp_tot: {n_from_alp_tot:.2f} - n_from_w_tot: {n_from_w_tot:.2f}")
    print(f"n_from_alp_with_leading_muon: {n_from_alp_with_leading_muon:.2f} - n_from_w_with_leading_muon: {n_from_w_with_leading_muon:.2f}")

    ratios_leading_from_alp[(mass,ctau)] = r_from_alp_with_leading_muon
    ratios_leading_from_w[(mass,ctau)] = r_from_w_with_leading_muon


masses = sorted(set(m for m, c in ratios_leading_from_alp.keys()))
cta_values = sorted(set(c for m, c in ratios_leading_from_alp.keys()))
h2 = ROOT.TH2D("ratios_leading_from_alp", ";m_{a} [GeV];c#tau [mm]",
               len(masses), 0, len(masses),
               len(cta_values), 0, len(cta_values))
h2_w = ROOT.TH2D("ratios_leading_from_w", ";m_{a} [GeV];c#tau [mm]",
               len(masses), 0, len(masses),
               len(cta_values), 0, len(cta_values))
for i, m in enumerate(masses):
    h2.GetXaxis().SetBinLabel(i+1, str(m))
    h2_w.GetXaxis().SetBinLabel(i+1, str(m))
for j, c in enumerate(cta_values):
    h2.GetYaxis().SetBinLabel(j+1, str(c))
    h2_w.GetYaxis().SetBinLabel(j+1, str(c))

# ✅ Loop directly over the map
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

c = ROOT.TCanvas("c", "c", 800, 600)
h2.Draw("COLZ TEXT")
c.SetRightMargin(0.15)
c.SaveAs("../ratios_leading_from_alp.pdf")

c_w = ROOT.TCanvas("c_w", "c_w", 800, 600)
h2_w.Draw("COLZ TEXT")
c_w.SetRightMargin(0.15)
c_w.SaveAs("../ratios_leading_from_w.pdf")


