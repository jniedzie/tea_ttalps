from scale_factors_config import *
from ttalps_extra_collections import get_extra_event_collections
from ttalps_object_cuts import *
from TTAlpsHistogrammerConfigHelper import TTAlpsHistogrammerConfigHelper

year = "2018"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
extraEventCollections = get_extra_event_collections(year)
scaleFactors = get_scale_factors(year)

nEvents = -1
printEveryNevents = 10000

runDefaultHistograms = True
runLLPTriggerHistograms = False
runPileupHistograms = False

# LLPNanoAODHistograms:
#  - muonMatchingParams loose muons
#  - muonMatchingParams loose muon vertex
#  - extra muon vertex collections
runLLPNanoAODHistograms = True

runMuonMatchingHistograms = False  # TODO: this doesn't seem to work
runGenMuonHistograms = False  # can only be run on signal samples
runGenMuonVertexCollectionHistograms = False

runABCDHistograms = True

weightsBranchName = "genWeight"
eventsTreeNames = ("Events",)

specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}
# redirector = "xrootd-cms.infn.it"

pileupScaleFactorsPath = "/data/dust/user/jniedzie/ttalps_cms/pileup_scale_factors.root"
pileupScaleFactorsHistName = "pileup_scale_factors"

applyScaleFactors = {
    "muon": True,
    "muonTrigger": True,
    "pileup": True,
    "bTagging": True,
    "PUjetID": True,
}
# Extra up/down SFs: comment out all to run not include them in histograms
extraSFs = [ 
    "btagUpCorrelated", 
    "btagDownCorrelated", 
    "btagUpUncorrelated", 
    "btagDownUncorrelated", 
    "pujetIDUp", 
    "pujetIDDown"
]

# For the signal histogramming all given mathcing methods are applied separately to histograms
# More than one given method will not affect the other histograms
# Matching methods implemented are:
# "Segment" : max matching ratio (eg. 2.0f/3.0f)
# "DR" : max Delta R (eg. 0.1)
# "OuterDR" : max Delta R (eg. 0.1)
# "ProxDR" : max Delta R (eg. 0.1)
muonMatchingParams = {
    "Segment": 2.0 / 3.0,
    # "DR" : 0.1
    # "OuterDR" : 0.1
    # "ProxDR" : 0.1
}

muonVertexBaselineSelection = [
    "InvariantMassCut",
    "ChargeCut",
    "HitsInFrontOfVertexCut",
    "DPhiBetweenMuonpTAndLxyCut",
    "DCACut",
    "CollinearityAngleCut",
    "Chi2Cut"
]


# dimuonSelection and muonVertexCollection:
#  - uncomment the dimuonSelection you want to use and the muonVertexCollection will be given automatically
#  - to not use dimuonSelection and muonVertexCollection: set dimuonSelection to None
dimuonSelection = "SRDimuonVertex"
# dimuonSelection = "JPsiDimuonVertex"
# dimuonSelection = "ZDimuonVertex"
# dimuonSelection = None
muonVertexCollections = {
    "SRDimuonVertex" : ("BestPFIsoDimuonVertex", muonVertexBaselineSelection + ["PFRelIsolationCut", "BestDimuonVertex"]), 
    "JPsiDimuonVertex" : ("BestDimuonVertex", muonVertexBaselineSelection + ["BestDimuonVertex"]), 
    "ZDimuonVertex" : ("BestDimuonVertex", muonVertexBaselineSelection + ["BestDimuonVertex"]), 
}
muonVertexCollection = None
if dimuonSelection is not None:
    muonVertexCollection = muonVertexCollections[dimuonSelection]


histParams = ()
histParams2D = ()

helper = TTAlpsHistogrammerConfigHelper(muonMatchingParams, muonVertexCollection[0] if muonVertexCollection is not None else None)


defaultHistParams = helper.get_default_params()

histParams += helper.get_basic_params()
histParams += helper.get_llp_params()
histParams += helper.get_nminus1_params()
histParams += helper.get_gen_matched_params()
histParams += helper.get_gen_params()
histParams += helper.get_trigger_params()
histParams += helper.get_matching_params()

histParams2D += helper.get_2D_params()
histParams2D += helper.get_abcd_params()
histParams2D += helper.get_2D_matching_params()

extraSFsHistParams2D = helper.get_abcd_params()
