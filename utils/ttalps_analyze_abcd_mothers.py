from Logger import info, warn, error, fatal, logger_print

import ROOT
import os

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_DSAmuPtGt20", "_SRDimuons")
# skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR_muPtGt20", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2", "_SRDimuons")
# skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2_muPtGt10", "_SRDimuons")
skim = ("skimmed_looseSemimuonic_v2_SR_muEtaLt1p2_muPtGt7", "_SRDimuons")

hist_base_name = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"

# process = "backgrounds2018/TTTo2L2Nu"
# process = "backgrounds2018/TTToSemiLeptonic"
# process = "backgrounds2018/ST_tW_antitop"
# process = "backgrounds2018/ST_t-channel_antitop"
# process = "backgrounds2018/ST_tW_top"
# process = "backgrounds2018/ST_t-channel_top"

# process = "signals/tta_mAlp-1GeV_ctau-1e-5mm"
# process = "signals/tta_mAlp-1GeV_ctau-1e0mm"
# process = "signals/tta_mAlp-1GeV_ctau-1e3mm"
process = "signals/tta_mAlp-12GeV_ctau-1e0mm"

input_path = f"{base_path}/{process}/{skim[0]}/{hist_base_name}{skim[1]}/histograms.root"


# variants = ["", "_lowBlob", "_centralBlob", "_rightBlob", "_lowLine", "_rightLine"]
# variants = [""]

variants = ["", "_mysteriousBlob"]

# min_fraction_to_show = 0.15
min_fraction_to_show = 0.0

code_to_name = {
    -1: "d~",
    1: "d",
    -2: "u~",
    2: "u",
    -4: "c~",
    4: "c",
    -5: "b~",
    5: "b",
    -6: "t~",
    6: "t",
    -13: "mu+",
    13: "mu-",
    -15: "tau+",
    15: "tau-",
    -21: "g",
    21: "g",
    22: "gamma",
    -23: "Z~",
    23: "Z",
    -24: "W-",
    24: "W+",
    
    113: "rho",
    223: "omega",
    333: "phi",
    
    -521: "B-",
    521: "B+",
    -511: "B0~",
    511: "B0",
    -411: "D-",
    411: "D+",
    -421: "D0~",
    421: "D0",
    -431: "D_s-",
    431: "D_s+",
    -443: "J/#psi",
    443: "J/#psi",
    -531: "B_s0~",
    531: "B_s0",

    90: "X_{PAT}",  # no gen matching reco
    91: "X_{DSA}",
    
    54: "ALP",
}


def symmetrize_hist(hist):
  for i in range(1, hist.GetNbinsX() + 1):
    for j in range(i + 1, hist.GetNbinsY() + 1):
      hist.SetBinContent(
          j, i,
          hist.GetBinContent(i, j) + hist.GetBinContent(j, i)
      )
      hist.SetBinContent(i, j, 0, 0)


def hist_to_dict(hist):

  result = {}

  if not isinstance(hist, ROOT.TH2):
    return result

  for i in range(1, hist.GetNbinsX() + 1):
    for j in range(1, hist.GetNbinsY() + 1):
      if hist.GetBinContent(i, j) == 0:
        continue

      x = int(hist.GetXaxis().GetBinLowEdge(i))
      y = int(hist.GetYaxis().GetBinLowEdge(j))

      result[(x, y)] = hist.GetBinContent(i, j)

  return result


def merge_identical(results):
  # merge entries where keys have the same value, but are swapped
  new_results = {}

  for key, value in results.items():
    if (key[1], key[0]) in new_results:
      new_results[(key[1], key[0])] += value
    else:
      new_results[key] = value

  return new_results


def merge_charge_conjugate(results):
  # merge entries where keys have the same values, but both with opposite sign. They may be swapped.

  new_results = {}

  for key, value in results.items():
    if (-key[0], -key[1]) in new_results:
      new_results[(-key[0], -key[1])] += value
    elif (-key[1], -key[0]) in new_results:
      new_results[(-key[1], -key[0])] += value
    else:
      new_results[key] = value

  return new_results


def main():
  file = ROOT.TFile(input_path)

  hist_name = "BestPFIsoDimuonVertex_motherPid1_vs_motherPid2"

  for variant in variants:
    print(f"\n\nvariant {variant}")

    hist = file.Get(hist_name + variant)
    results = hist_to_dict(hist)

    results = merge_identical(results)
    results = merge_charge_conjugate(results)
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    has_negative = False
    for key, value in results:
      if value < 0:
        has_negative = True
        break

    if has_negative:
      error("Negative values found")

    sum_all = sum([value for _, value in results])

    for key, value in results:
      if value/sum_all < min_fraction_to_show:
        continue

      if key[0] in code_to_name:
        part0 = code_to_name[key[0]]
      else:
        print(f"Unknown code: {key[0]}")
        part0 = str(key[0])

      if key[1] in code_to_name:
        part1 = code_to_name[key[1]]
      else:
        print(f"Unknown code: {key[1]}")
        part1 = str(key[1])

      print(f"{part0} {part1}: {value/sum_all:.2f}")

  # deltaR_name = "logDeltaR"
  rebin = 1

  deltaR_name = "deltaR"
  rebin = 20

  hist_deltaR_OS = file.Get(f"BestPFIsoDimuonVertex_{deltaR_name}_OS")
  hist_deltaR_WW = file.Get(f"BestPFIsoDimuonVertex_{deltaR_name}_WW")
  hist_deltaR_Wtau = file.Get(f"BestPFIsoDimuonVertex_{deltaR_name}_Wtau")

  if hist_deltaR_OS is None or not isinstance(hist_deltaR_OS, ROOT.TH1D):
    error(f"{hist_deltaR_OS} not found in file {input_path}")
    logger_print()
    return

  if hist_deltaR_WW is None or not isinstance(hist_deltaR_WW, ROOT.TH1D):
    error(f"{hist_deltaR_WW} not found in file {input_path}")
    logger_print()
    return

  if hist_deltaR_Wtau is None or not isinstance(hist_deltaR_Wtau, ROOT.TH1D):
    error(f"{hist_deltaR_Wtau} not found in file {input_path}")
    logger_print()
    return

  canvas = ROOT.TCanvas("canvas", "canvas", 800, 800)

  ROOT.gStyle.SetOptStat(0)

  hist_deltaR_OS.SetLineColor(ROOT.kBlack)
  hist_deltaR_WW.SetLineColor(ROOT.kRed)
  hist_deltaR_Wtau.SetLineColor(ROOT.kBlue)

  hist_deltaR_OS.Scale(1/hist_deltaR_OS.Integral())
  hist_deltaR_WW.Scale(1/hist_deltaR_WW.Integral())
  hist_deltaR_Wtau.Scale(1/hist_deltaR_Wtau.Integral())

  hist_deltaR_OS.Rebin(rebin)
  hist_deltaR_WW.Rebin(rebin)
  hist_deltaR_Wtau.Rebin(rebin)
  hist_deltaR_OS.Scale(1/rebin)
  hist_deltaR_WW.Scale(1/rebin)
  hist_deltaR_Wtau.Scale(1/rebin)

  hist_deltaR_OS.Draw()
  hist_deltaR_WW.Draw("same")
  hist_deltaR_Wtau.Draw("same")

  hist_deltaR_OS.GetXaxis().SetRangeUser(0, 2*3.1415)
  hist_deltaR_OS.GetYaxis().SetRangeUser(0, 0.03)
  hist_deltaR_OS.GetXaxis().SetTitle("#Delta R_{#mu#mu}")

  legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)
  legend.AddEntry(hist_deltaR_WW, "WW (SS)", "l")
  legend.AddEntry(hist_deltaR_Wtau, "W#tau (OS)", "l")
  legend.AddEntry(hist_deltaR_OS, "everything else", "l")
  legend.Draw()

  canvas.SaveAs("../plots/deltaR_OS_vs_SS.pdf")

  logger_print()


if __name__ == "__main__":
  main()
