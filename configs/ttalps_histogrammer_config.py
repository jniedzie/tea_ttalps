from scale_factors_config import get_scale_factors
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

# Histograms for Muon Trigger Objects
runMuonTriggerObjectsHistograms = False
# Histograms for "BestDimuonVertex" excluding trigger matched muon and leading tight muon
# Needed for BestNonLeadingDimuonVertex ABCD histograms
runNonLeadingVertexCollection = True

runMuonMatchingHistograms = False  # TODO: this doesn't seem to work
runGenMuonHistograms = False  # can only be run on signal samples
runGenMuonVertexCollectionHistograms = False

# Create 2D histograms for ABCD background estimation
runABCDHistograms = True

# [MC only] Create histograms with mother PIDs of dimuons entering ABCD histograms (quite heavy, turn off if not needed)
runABCDMothersHistograms = False

# [MC only] Create histograms for dimuons in the fakes region vs. non-fakes region
runFakesHistograms = False

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
    "SRDimuonVertex": ("BestPFIsoDimuonVertex", muonVertexBaselineSelection + ["PFRelIsolationCut", "BestDimuonVertex"]),
    "JPsiDimuonVertex": ("BestDimuonVertex", muonVertexBaselineSelection + ["BestDimuonVertex"]),
    "ZDimuonVertex": ("BestDimuonVertex", muonVertexBaselineSelection + ["BestDimuonVertex"]),
}
muonVertexCollection = None
if dimuonSelection is not None:
  muonVertexCollection = muonVertexCollections[dimuonSelection]


histParams = ()
histParams2D = ()

helper = TTAlpsHistogrammerConfigHelper(
    muonMatchingParams, muonVertexCollection if muonVertexCollection is not None else None)

defaultHistParams = helper.get_default_params()
histParams += helper.get_basic_params()

if runLLPNanoAODHistograms:
  histParams += helper.get_llp_params()

if runGenMuonVertexCollectionHistograms:
  histParams += helper.get_gen_vertex_params()
if runGenMuonHistograms:
  histParams += helper.get_gen_params()
  histParams += helper.get_gen_matched_params()

if runLLPTriggerHistograms:
  histParams += helper.get_trigger_params()
if runMuonMatchingHistograms:
  histParams += helper.get_matching_params()
  histParams2D += helper.get_2D_matching_params()

if runABCDHistograms:
  histParams += helper.get_abcd_1Dparams()
  histParams2D += helper.get_abcd_2Dparams()

if runABCDMothersHistograms:
  histParams2D += helper.get_abcd_mothers_2Dparams()

if runFakesHistograms:
  histParams += helper.get_fakes_params()

if runMuonTriggerObjectsHistograms:
    histParams += helper.get_muon_trigger_objects_params()
if runNonLeadingVertexCollection:
    histParams += helper.get_nontrigger_muon_vertex_params()

SFvariationVariables = helper.get_SF_variation_variables()
