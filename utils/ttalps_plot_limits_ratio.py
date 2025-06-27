import ROOT
import re
import math

def parse_file(filepath):
    data = {}
    with open(filepath, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            key, value_str = line.strip().split(':')
            values = eval(value_str.strip())  # Parse the list
            data[key.strip()] = [float(v) for v in values]
    return data

# Extract mAlp and ctau as floats
def parse_key(key):
    match = re.search(r'mAlp-(\d+p?\d*)GeV_ctau-(\d+e[+-]?\d*)mm', key)
    if match:
        mAlp = float(match.group(1).replace('p', '.'))
        ctau = float(match.group(2))
        return mAlp, ctau
    else:
        return None, None

def parse_combined_key(key):
    match = re.search(r'mass_(\d+p?\d*)_ctau_(\d+e[+-]?\d*)', key)
    if match:
        mAlp = float(match.group(1).replace('p', '.'))
        ctau = float(match.group(2))
        return mAlp, ctau
    else:
        return None, None


base_path = "../limits/"

# old matching / new matching:
# file_path1 = "results_oldMatching_JPsiSFs"
# file_path2 = "results_newMatching_JPsiSFminBkg3"
# filename1 = "limits_BestPFIsoDimuonVertex_logAbsCollinearityAngle_vs_logPt_Pat_ABCDpred"
# filename2 = "limits_BestSegmentMatchedPFIsoDimuonVertex_logAbsCollinearityAngle_vs_logPt_Pat_ABCDpred"
# filename1 = "limits_BestPFIsoDimuonVertex_outerDR_vs_leadingPt_PatDSA_ABCDpred"
# filename2 = "limits_BestSegmentMatchedPFIsoDimuonVertex_absPtLxyDPhi2_vs_logDxyPVTraj1_PatDSA_ABCDpred"
# filename1 = "limits_BestPFIsoDimuonVertex_logLeadingPt_vs_dPhi_DSA_ABCDpred"
# filename2 = "limits_BestSegmentMatchedPFIsoDimuonVertex_logLxy_vs_outerDR_DSA_ABCDpred"
# filename1 = "limits_combined_oldMatching_JPsiSFs"
# filename2 = "limits_combined_newMatching_JPsiSFminBkg3"

# Without JEC / with JEC:
file_path1 = "results_newMatching_dimuonEff_jec"
file_path2 = "results_newMatching_dimuonEff"
# filename1 = "limits_BestPFIsoDimuonVertex_logAbsCollinearityAngle_vs_pt_Pat_ABCDpred"
# filename2 = "limits_BestPFIsoDimuonVertex_logAbsCollinearityAngle_vs_pt_Pat_ABCDpred"
filename1 = "limits_BestPFIsoDimuonVertex_log3Dangle_vs_logDxyPVTraj1_PatDSA_ABCDpred"
filename2 = "limits_BestPFIsoDimuonVertex_log3Dangle_vs_logDxyPVTraj1_PatDSA_ABCDpred"
# filename1 = "limits_BestPFIsoDimuonVertex_logLxy_vs_outerDR_DSA_ABCDpred"
# filename2 = "limits_BestPFIsoDimuonVertex_logLxy_vs_outerDR_DSA_ABCDpred"


output_path = "../limits/plots/ratios_jec/"

file1_data = parse_file(f"{base_path}/{file_path1}/{filename1}.txt")
file2_data = parse_file(f"{base_path}/{file_path2}/{filename2}.txt")

mAlps = set()
ctaus = set()
ratios = {}

for key in file1_data:
    print("key: ", key)
    if key not in file2_data:
        continue

    mAlp = None 
    ctau = None
    if "combined" in filename1:
        mAlp, ctau = parse_combined_key(key)
    else:
        mAlp, ctau = parse_key(key)
    if mAlp is None or ctau is None:
        continue

    mAlps.add(mAlp)
    ctaus.add(ctau)

    vals1 = file1_data[key]
    vals2 = file2_data[key]
    if len(vals1) != len(vals2):
        continue

    median1 = float(vals1[0])
    median2 = float(vals2[0])        
    ratio = median1 / median2 if median2 != 0 else 0
    ratios[(mAlp, ctau)] = ratio

# Prepare sorted bins
mAlps = sorted(list(mAlps))
ctaus = sorted(list(ctaus))

h2 = ROOT.TH2F("ratio", "Average Value Ratio; m_{a} [GeV]; c#tau [mm]", len(mAlps), 0, len(mAlps), len(ctaus), 0, len(ctaus))
ROOT.gStyle.SetPaintTextFormat("0.2f")
h2.SetMarkerSize(1.6) 

# Label axes
for i, m in enumerate(mAlps):
    h2.GetXaxis().SetBinLabel(i+1, f"{m:.2f}")
for j, c in enumerate(ctaus):
    h2.GetYaxis().SetBinLabel(j+1, f"{c:.0e}")

# Set z-axis title
h2.GetZaxis().SetTitle("Ratio")

# Fill histogram
for (m, c), r in ratios.items():
    xbin = mAlps.index(m) + 1
    ybin = ctaus.index(c) + 1
    h2.SetBinContent(xbin, ybin, r)

# h2.SetMinimum(0.4)
# h2.SetMaximum(1.0)

# Draw
canvas = ROOT.TCanvas("c1", "Ratio Plot", 800, 600)
canvas.SetRightMargin(0.15)
h2.SetStats(False)
h2.Draw("COLZ TEXT")
output_name = f"{output_path}ratio_{filename1}_{filename2}.pdf"
canvas.SaveAs(output_name)