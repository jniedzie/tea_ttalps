from ttalps_samples_list import backgrounds2018, signals2018, data2018, signals2018_1GeV
import os

def main():
  
  # base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"
  base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms"
  
  # For signal like skim: SR and J/Psi CR with no isolation requirement on the loose muons
  skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"

  # For signal like skim with Dimuon triggers for LLP trigger study
  # skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso_LLPtrigger"

  # Loose semimuonic skim
  # skim = "skimmed_looseSemimuonicv1"

  # Loose semimuonic skim with Dimuon triggers for LLP trigger study
  # skim = "skimmed_looseSemimuonicv1_LLPtrigger"
  
  # Default settings
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
  # SR dimuon cuts applied
  hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_SRDimuons"
  # JPsi dimuon cuts applied
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_JPsiDimuons"
  
  # sample_paths = backgrounds2018 + signals2018_1GeV + data2018
  sample_paths = signals2018_1GeV
  
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
