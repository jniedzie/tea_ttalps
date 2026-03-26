import ROOT
import os

from Logger import info

# year = "2023preBPix"
year = "2016preVFP2016postVFP201720182022preEE2022postEE2023preBPix2023postBPix"
categories = ["Pat", "PatDSA", "DSA"]

Lxy_region = "SR_maxLxy_ANv3"

output_path = f"../plots/n_events/{Lxy_region}_{year}"
if not os.path.exists(output_path):
    os.makedirs(output_path)

ctau_string_to_float = {
    "1 nm": 1e-5,
    "1 mm": 1.0,
    "1 cm": 10.0,
    "10 cm": 100.0,
    "1 m": 1000.0,
}
ctau_string_to_exp_name = {
    "1 nm": "1e-5",
    "1 mm": "1e0",
    "1 cm": "1e1",
    "10 cm": "1e2",
    "1 m": "1e3",
}

def format_value_unc(val, unc):
    if unc <= 0:
        return f"{val:.2f} ± 0"

    exponent = math.floor(math.log10(abs(unc)))
    unc_rounded = round(unc, -exponent)
    nd = max(0, -int(math.floor(math.log10(abs(unc_rounded)))))
    # nd = max(0, -exponent)
    # unc_rounded = round(unc, nd)
    val_rounded = round(val, nd)
    if val_rounded == 0 and val != 0:
        nd += 1
        val_rounded = round(val, nd)
        unc_rounded = round(unc, nd)
    # return f"{val_rounded:.{nd}f} #pm {unc_rounded:.{nd}f}"
    return f"{val_rounded:.{nd}f}"

for category in categories:

    info(f"\n--- {category}:")
    # Open input files
    f_base = ROOT.TFile.Open(f"../signal_lxy_uncertainty/input_root_files/n_signal_events_{category}_{year}_SR_ANv3.root")
    f_cut  = ROOT.TFile.Open(f"../signal_lxy_uncertainty/input_root_files/n_signal_events_{category}_{year}_{Lxy_region}.root")

    # Get histograms
    h_base = f_base.Get("n_signal_events")
    h_cut  = f_cut.Get("n_signal_events")

    if not h_base:
        raise RuntimeError("Histogram 'n_signal_events' not found")

    # Clone base histogram to preserve binning, labels, titles
    h_eff = h_base.Clone(f"n_signal_events_efficiency_{category}_{year}")
    title = "PAT-PAT"
    if category == "PatDSA":
        title = "PAT-DSA"
    if category == "DSA":
        title = "DSA-DSA"
    h_eff.SetTitle(title)
    h_eff.Reset()

    nx = h_base.GetNbinsX()
    ny = h_base.GetNbinsY()

    # Compute efficiency bin-by-bin
    for ix in range(1, nx+1):
        for iy in range(1, ny+1):

            base = h_base.GetBinContent(ix, iy)
            cut  = h_cut.GetBinContent(ix, iy)

            if base != 0:
                if base == cut:
                    eff = 1.0
                    eff_prc = 1e-9
                else:
                    eff = 1.0 + (base - cut) / base
                    eff_prc = 100 * (base - cut) / base
            else:
                eff = 1.0
                eff_prc = 1e-9
            
            h_eff.SetBinContent(ix, iy, eff_prc)
            mass_str = h_base.GetXaxis().GetBinLabel(ix)
            ctau_str = h_base.GetYaxis().GetBinLabel(iy)
            mass = float(mass_str)
            ctau = ctau_string_to_float[ctau_str]
            mass_str.replace(".","p",1)
            ctau_str_exp = ctau_string_to_exp_name[ctau_str]
            info(f"\"tta_mAlp-{mass_str}GeV_ctau-{ctau_str_exp}mm\": {eff},")

    ROOT.gStyle.SetOptStat(0)

    c1 = ROOT.TCanvas("c1", "c1", 800, 600)
    h_eff.SetMinimum(1e-9)

    h_eff.Draw("COLZ")
    h_eff.GetXaxis().SetLabelSize(0.04)
    h_eff.GetYaxis().SetLabelSize(0.04)
    
    h_eff.GetZaxis().SetTitle("Efficiency [%]")

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)
    latex.SetTextSize(0.025)
    latex.SetTextFont(42)

    for ix in range(1, h_eff.GetNbinsX()+1):
        for iy in range(1, h_eff.GetNbinsY()+1):
            val = h_eff.GetBinContent(ix, iy)
            unc = h_eff.GetBinError(ix, iy)
            txt = f"{val:.1f}"
            x = h_eff.GetXaxis().GetBinCenter(ix)
            y = h_eff.GetYaxis().GetBinCenter(iy)
            latex.DrawLatex(x, y, txt)
    
    c1.SetRightMargin(0.15)
    c1.SaveAs(f"{output_path}/n_signal_events_Lxy_efficiency_{category}_{year}.pdf")

    # Save to new ROOT file
    out = ROOT.TFile(f"../signal_lxy_uncertainty/output_root_files/n_signal_events_efficiency_{category}_{year}.root", "RECREATE")
    h_eff.Write()
    out.Close()

    print(f"Efficiency histogram saved to signal_lxy_uncertainty/output_root_files/n_signal_events_efficiency_{category}_{year}.root")
