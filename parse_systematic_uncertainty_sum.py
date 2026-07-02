import math

def parse_uncertainty_asymmetric(value):
    """
    Convert lnN value to (down, up) relative uncertainties.
    """
    if "/" in value:
        down, up = value.split("/")
        down = float(down)
        up = float(up)

        unc_down = abs(1.0 - down)
        unc_up = abs(up - 1.0)

    else:
        val = float(value)
        unc_down = abs(1.0 - val)
        unc_up = abs(val - 1.0)

    return unc_down, unc_up


def extract_signal_systematics(datacard_path, skip_dimuon_sfs=False):
    down_uncs = []
    up_uncs = []

    with open(datacard_path, "r") as f:
        for line in f:
            line = line.strip()

            if not line.startswith("CMS"):
                continue

            if skip_dimuon_sfs and "dimuonSF" in line:
                continue
            if skip_dimuon_sfs and "Lxy" in line:
                continue

            parts = line.split()

            if len(parts) < 4:
                continue

            _, unc_type, sig_val, bkg_val = parts[:4]

            if unc_type != "lnN":
                continue

            if sig_val == "-":
                continue

            try:
                unc_down, unc_up = parse_uncertainty_asymmetric(sig_val)
                down_uncs.append(unc_down)
                up_uncs.append(unc_up)
            except ValueError:
                print(f"Warning: could not parse {sig_val}")

    return down_uncs, up_uncs


def combine_quadrature(values):
    return math.sqrt(sum(v**2 for v in values))


if __name__ == "__main__":
    datacard_path = "limits/limits_2016preVFP2016postVFP201720182022preEE2022postEE2023preBPix2023postBPix/datacards_years_combined_noDimuonSFs_SR_ANv6"
    # datacard_path = "limits/limits_2016preVFP2016postVFP201720182022preEE2022postEE2023preBPix2023postBPix/datacards_years_combined_dxydzIso_SR_ANv5"
    # datacard_path = "limits/limits_2016preVFP2016postVFP201720182022preEE2022postEE2023preBPix2023postBPix/datacards_SR_ANv6_regionBCD"
    card_pattern = "combined_datacard_{}_{}{}.txt"

    skip_dimuon_sfs = "noDimuonSFs" in datacard_path

    categories = ["_Pat", "_PatDSA", "_DSA"]
    masses = ["0p35", "2", "12", "30", "60"]
    ctaus = ["1e-5", "1e0", "1e1", "1e2", "1e3"]

    for category in categories:
        print(f"\nsyst_unc[\"{category}\"] = {{")
        for mass in masses:
            for ctau in ctaus:
                card_path = f"{datacard_path}/{card_pattern.format(mass, ctau, category)}"

                down_uncs, up_uncs = extract_signal_systematics(card_path, skip_dimuon_sfs)

                total_down = combine_quadrature(down_uncs)
                total_up = combine_quadrature(up_uncs)

                print(f"\t(\"{mass}\", \"{ctau}\"):\t({total_down:.4f},{total_up:.4f}),")
        print("}")
