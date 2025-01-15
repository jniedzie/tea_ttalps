from ttalps_samples_list import dasData2018, dasData2016_standard, dasData2017_standard, dasData2018_standard, dasData2022_standard, dasData2023_standard

max_files = -1

base_path = "/nfs/dust/cms/user/jniedzie/susy_test"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

sample_path = ""
dasSamples = {} 

# IsoMu24, ≥2 OS LooseIsoPATMuons, categories in number of jets 
# (GoodForwardJetsPlus/Minus, GoodCentralNonBtaggedJets, GoodMediumBtaggedJets) and boost
# skim = "minimalCuts"

# like minimalCuts, but with muon pt > 25, 18 GeV, muon |η| < 2.1
# skim = "minimalCuts_tighterMuons"

# like minimalCuts, but adding categories in muon pt
# skim = "minimalCuts_muonPtCategories"

# same as minimalCuts, but with standard NanoAOD:
# skim = "minimalCuts_standardNanoAOD"
# skim = "minimalCuts_standardNanoAOD_tighterMuons"
skim = "minimalCuts_standardNanoAOD_muonPtCategories"

# # For DAS inputs:
dataset = ""

# dbs_instance = "prod/phys03"
# dasSamples.update(dasData2018)

dbs_instance = "prod/global"
# dasSamples.update(dasData2016_standard)
# dasSamples.update(dasData2017_standard)
# dasSamples.update(dasData2018_standard)
# dasSamples.update(dasData2022_standard)
dasSamples.update(dasData2023_standard)

datasets_and_output_hists_dirs = [(v, f"{base_path}/{skim}/hists/{k}/") for k, v in dasSamples.items()]
