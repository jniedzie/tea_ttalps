from ttalps_samples_list import backgrounds2018, signals2018, data2018, signals2018_1GeV
import os

def main():
  
  # base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"
  base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms"
  
  # skim=""
  # skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso_goldenJson"
  # skim = "skimmed_ttZSemimuonicCR_Met50GeV"

  # skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_Iso"
  # skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"

  skim = "skimmed_looseSemimuonicv1"
  
  # hist_path = "histograms"
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
  hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons"
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons_Unweighted"
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_JPsiDimuons"
  
  # sample_paths = backgrounds2018 + signals2018_1GeV + data2018
  sample_paths = signals2018_70GeV
  
  for sample_path in sample_paths:
    print(f"{sample_path=}")
    
    input_path = f"{sample_path}/{skim}/{hist_path}/*.root"
    
    if "collision_data" in input_path:
      output_path = f"collision_data2018/SingleMuon2018_{skim}_{hist_path}.root"
    else:
      output_path = input_path.replace("*.root", "histograms.root")
    
    print(f"{output_path=}")
    
    os.system(f"rm {base_path}/{output_path}")
    os.system(f"hadd -f -j -k {base_path}/{output_path} {base_path}/{input_path}")

if __name__ == "__main__":
  main()
