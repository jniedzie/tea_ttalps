from scale_factors_config import *

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
scaleFactors = get_scale_factors(year)

nEvents = -1
printEveryNevents = 10000

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
  "muonTriggerIsoMu24": False,
  "pileup": False,
}

defaultHistParams = (
#  collection             variable               bins    xmin    xmax    dir
  ("Event"             , "PV_npvs"              , 300   , 0     , 300   , ""  ),
  ("Event"             , "PV_npvsGood"          , 300   , 0     , 300   , ""  ),
)
