max_files = -1

# skim = "skimmed_looseSemimuonic"
# skim = "skimmed_looseSemimuonic_new"
# skim = "skimmed_looseSemimuonic_SRmuonic"
# skim = "skimmed_looseSemimuonic_SRmuonic_DR"
# skim = "skimmed_looseSemimuonic_SRmuonic_OuterDR"
skim = "skimmed_looseSemimuonic_SRmuonic_Segment"
# skim = "LLPNanoAOD"

# base_path = "/nfs/dust/cms/user/jniedzie/ttalps_cms"
base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms"

applyScaleFactors = {
  "muon": True,
  "muonTrigger": True,
  "pileup": True,
  "bTagging": True,
}

samples = (
  # Backgrounds
  # "backgrounds2018/TTToSemiLeptonic",
  # "backgrounds2018/TTToHadronic",
  # "backgrounds2018/TTTo2L2Nu",

  # "backgrounds2018/TTZToLLNuNu_M-10",
  # "backgrounds2018/TTZToLL_M-1to10",
  
  # "backgrounds2018/ST_tW_antitop",
  # "backgrounds2018/ST_t-channel_antitop",
  # "backgrounds2018/ST_tW_top",
  # "backgrounds2018/ST_t-channel_top",
  
  # "backgrounds2018/DYJetsToMuMu_M-50",
  # "backgrounds2018/DYJetsToMuMu_M-10to50",
    
  # "backgrounds2018/ttWJets",
  # "backgrounds2018/TTWJetsToLNu",
  # "backgrounds2018/WJetsToLNu",
  
  # "backgrounds2018/ttHToMuMu",
  # # "backgrounds2018/ttHTobb",
  # "backgrounds2018/ttHToNonbb",
  
  # # "backgrounds2018/TTZZ",
  # "backgrounds2018/TTZH",
  # "backgrounds2018/TTTT",
  
  # # QCD (LLPnanoAOD mu enhanced)
  # "backgrounds2018/QCD_Pt-15To20",
  # "backgrounds2018/QCD_Pt-20To30",
  # "backgrounds2018/QCD_Pt-30To50",
  # "backgrounds2018/QCD_Pt-50To80",
  # "backgrounds2018/QCD_Pt-80To120",
  # "backgrounds2018/QCD_Pt-120To170",
  # "backgrounds2018/QCD_Pt-170To300",
  # "backgrounds2018/QCD_Pt-300To470",
  # "backgrounds2018/QCD_Pt-470To600",
  # "backgrounds2018/QCD_Pt-600To800",
  "backgrounds2018/QCD_Pt-800To1000",
  "backgrounds2018/QCD_Pt-1000",

  # # Data
  # "collision_data2018/SingleMuon2018A",
  # "collision_data2018/SingleMuon2018B",
  # "collision_data2018/SingleMuon2018C",
  # "collision_data2018/SingleMuon2018D",
  
  # Signal
  # "signals/tta_mAlp-0p35GeV_ctau-1e0mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e1mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e2mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e3mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e5mm",
  # "signals/tta_mAlp-0p35GeV_ctau-1e-5mm",
)

# this has to be here, otherwise the script will not work:
sample_path = ""
input_directory = f"{base_path}/{sample_path}/{skim}/"

output_dir = f"{input_directory}/histograms"

for name, apply in applyScaleFactors.items():
  if not apply:
    continue
  
  output_dir += f"_{name}SFs"
  
output_dir += "/"
