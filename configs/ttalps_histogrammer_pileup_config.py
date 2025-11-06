from scale_factors_config import get_scale_factors
from ttalps_histogrammer_files_config import year

scaleFactors = get_scale_factors(year)

nEvents = -1

runDefaultHistograms = False
runTriggerHistograms = False
runPileupHistograms = True
runMuonMatchingHistograms = False
runGenMuonHistograms = False

weightsBranchName = "genWeight"

pileupScaleFactorsPath = "../data/pileup/pileup_scale_factors.root"
pileupScaleFactorsHistName = "pileup_scale_factors"

applyScaleFactors = {
    "muon": False,
    "muonTrigger": False,
    "pileup": False,
}

defaultHistParams = (
    #  collection             variable               bins    xmin    xmax    dir
    ("Event", "PV_npvs", 300, 0, 300, ""),
    ("Event", "PV_npvsGood", 300, 0, 300, ""),
)
