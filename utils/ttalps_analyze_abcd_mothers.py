import ROOT
import os

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"

skim = ("skimmed_loose_lt3bjets_lt4jets_v1_bbCR", "_SRDimuons")
hist_base_name = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"

input_path = f"{base_path}/backgrounds2018/TTTo2L2Nu/{skim[0]}/{hist_base_name}{skim[1]}/histograms.root"
# input_path = f"{base_path}/backgrounds2018/TTTo2L2Nu/{skim[0]}/{hist_base_name}{skim[1]}/output_850.root"


# variants = ["", "_lowBlob", "_centralBlob", "_rightBlob", "_lowLine", "_rightLine"]
variants = [""]

min_fraction_to_show = 0.05
# min_fraction_to_show = 0.0

code_to_name = {
    -1: "d~",
    1: "d",
    -13: "mu+",
    13: "mu-",
    -15: "tau+",
    15: "tau-",
    22: "gamma",
    -24: "W-",
    24: "W+",
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
    -531: "B_s0~",
    531: "B_s0",

    90: "X_{PAT}",  # no gen matching reco
    91: "X_{DSA}",
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
    hist = file.Get(hist_name + variant)
    results = hist_to_dict(hist)

    results = merge_identical(results)
    results = merge_charge_conjugate(results)
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    sum_all = sum([value for _, value in results])
  
    print(f"\n\nvariant {variant}")
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


if __name__ == "__main__":
  main()
