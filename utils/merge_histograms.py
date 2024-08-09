# from ttalps_samples_list import backgrounds2018, signals2018, data2018, signals2018_1GeV
import os

signals2018_0p35GeV = (
  "signals/tta_mAlp-0p35GeV_ctau-1e0mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e1mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e2mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e3mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e5mm",
  "signals/tta_mAlp-0p35GeV_ctau-1e-5mm",
)
signals2018_1GeV = (
  "signals/tta_mAlp-1GeV_ctau-1e0mm",
  "signals/tta_mAlp-1GeV_ctau-1e1mm",
  "signals/tta_mAlp-1GeV_ctau-1e2mm",
  "signals/tta_mAlp-1GeV_ctau-1e3mm",
  "signals/tta_mAlp-1GeV_ctau-1e5mm",
  "signals/tta_mAlp-1GeV_ctau-1e-5mm",
)
signals2018 = signals2018_0p35GeV + signals2018_1GeV
TT_backgrounds2018 = (
  "backgrounds2018/TTToSemiLeptonic",
  "backgrounds2018/TTToHadronic",
  "backgrounds2018/TTTo2L2Nu",

  "backgrounds2018/TTZToLLNuNu_M-10",
  "backgrounds2018/TTZToLL_M-1to10",

  "backgrounds2018/TTZZ",
  "backgrounds2018/TTZH",
  "backgrounds2018/TTTT",

  "backgrounds2018/TTWJetsToLNu",

  "backgrounds2018/ttHTobb",
  "backgrounds2018/ttHToNonbb",
)
ST_backgrounds2018 = ( 
  "backgrounds2018/ST_tW_antitop",
  "backgrounds2018/ST_t-channel_antitop",
  "backgrounds2018/ST_tW_top",
  "backgrounds2018/ST_t-channel_top",
)
DY_backgrounds2018 = (
  "backgrounds2018/DYJetsToMuMu_M-50",
  "backgrounds2018/DYJetsToMuMu_M-10to50",
)
V_backgrounds2018 = (
  "backgrounds2018/WJetsToLNu",
)
QCD_backgrounds2018 = (
  "backgrounds2018/QCD_Pt-15To20",
  "backgrounds2018/QCD_Pt-20To30",
  # # "backgrounds2018/QCD_Pt-30To50",
  "backgrounds2018/QCD_Pt-50To80",
  # # "backgrounds2018/QCD_Pt-80To120",
  "backgrounds2018/QCD_Pt-120To170",
  "backgrounds2018/QCD_Pt-170To300",
  "backgrounds2018/QCD_Pt-300To470",
  "backgrounds2018/QCD_Pt-470To600",
  "backgrounds2018/QCD_Pt-600To800",
  "backgrounds2018/QCD_Pt-800To1000",
  "backgrounds2018/QCD_Pt-1000",
)
backgrounds2018 = TT_backgrounds2018 + ST_backgrounds2018 + DY_backgrounds2018 + V_backgrounds2018 + QCD_backgrounds2018

def main():
  
  # base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"
  base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms"
  
  # skim=""
  # skim = "skimmed_ttbarSemimuonicCR_Met50GeV_1mediumBjets_muonIdIso_goldenJson"
  # skim = "skimmed_ttZSemimuonicCR_Met50GeV"
  # skim = "skimmed_looseSemimuonicv1"
  skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_Iso"
  # skim = "skimmed_looseSemimuonic_SRmuonic_Segmentv1_NonIso"
  
  # hist_path = "histograms"
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs"
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_InvMass_Nminus1"
  hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_Nminus1"
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_Nminus1_noInvMassCut"
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_Nminus1_JPsi"
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_NonIsoMuonsNminus2"
  # hist_path = "histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_GenLevel"
  
  # sample_paths = backgrounds2018 + signals2018_1GeV + data2018
  sample_paths = signals2018_0p35GeV
  
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
