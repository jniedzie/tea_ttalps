import subprocess
import ROOT


# input_path = "../TTToSemiLeptonic_2018_initial.root"
input_path = "/data/dust/group/cms/ttALPs-desy/backgrounds2018/TTToSemiLeptonic/skimmed_looseSemimuonic_v3_SR/output_0.root"

n_events = 10000

exclude_indices = (2, 6)


def main():

  file = ROOT.TFile.Open(input_path)
  tree = file.Get("Events")

  nWeights = 9  # there are 9 LHEScaleWeight variations in the LHE file

  sum_nom = 0.0
  sum_var = [0.0]*nWeights

  # here we calculate the nominal and modified sum of event weights
  for i, event in enumerate(tree):
    if i > n_events:
      break

    w = event.genWeight
    sum_nom += w

    for i in range(nWeights):
      if i in exclude_indices:
        sum_var[i] += w
      else:
        sum_var[i] += w * event.LHEScaleWeight[i]

  # we take the envelope of all uncertainties as the final uncertainty
  up = max(sum_var) - sum_nom
  down = min(sum_var) - sum_nom

  print(f"Up: {up/sum_nom:.2%}, Down: {down/sum_nom:.2%}")
  # it looks like in the SR we can expect roughtly +/- 13% uncertainty from the scale variations


if __name__ == "__main__":
  main()
