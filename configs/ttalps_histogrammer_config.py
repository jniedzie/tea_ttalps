from scale_factors_config import get_scale_factors
from ttalps_extra_collections import get_extra_event_collections
from ttalps_object_cuts import *
from TTAlpsHistogrammerConfigHelper import TTAlpsHistogrammerConfigHelper

from ttalps_histogrammer_files_config import skim, applyScaleFactors

from ttalps_skimmer_looseSemimuonic_config import eventCuts as looseEventCuts
from ttalps_skimmer_signalLike_semimuonic_config import eventCuts as signalEventCuts
# defining eventCuts as the loose eventCuts and replacing MET pt from signal eventCuts
eventCuts = {
    **looseEventCuts,
    "MET_pt": signalEventCuts["MET_pt"],
}

# year = "2016preVFP"
year = "2018"
# year = "2022postEE"
# options for year is: 2016preVFP, 2016postVFP, 2017, 2018, 2022preEE, 2022postEE, 2023preBPix, 2023postBPix
extraEventCollections = get_extra_event_collections(year)
scaleFactors = get_scale_factors(year)

nEvents = -1
printEveryNevents = 10000

# Should dimuon checks be skipped? Used for tt̄ CR, where we don't have dimuons
ignoreDimuons = False

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

runMuonMatchingHistograms = False  # TODO: this doesn't seem to work
runGenMuonHistograms = False  # can only be run on signal samples
runGenMuonVertexCollectionHistograms = False

# Create 2D histograms for ABCD background estimation
runABCDHistograms = True

# Create 2D histograms in the same way as for ABCD, but for single muon variables
runSingleMuonABCDHistograms = True

# [MC only] Create histograms with mother PIDs of dimuons entering ABCD histograms (quite heavy, turn off if not needed)
runABCDMothersHistograms = False

runGenLevelABCD = False

# [MC only] Create histograms for dimuons in the fakes region vs. non-fakes region
runFakesHistograms = False

# Create histograms for Best PAT-PAT dimuons -> DSA Best Dimuons due changed ratio
runMuonMatchingRatioEffectHistograms = False

# Apply Segment Matching on the GoodMuonVertexCollections after the dimuon selection
applySegmentMatchingAfterSelections = True

# Inlude N-1 histograms - NOTE: this will ignore the dimuon selection in order to include all N-1 dimuons properly
# Do not use for CR with dimuon selection
runNminus1Histograms = False

weightsBranchName = "genWeight"
rhoBranchName = "fixedGridRhoFastjetAll" # for jec unc.
if "22" in year or "23" in year:
    rhoBranchName = "Rho_fixedGridRhoFastjetAll"  # for jec unc. in 2022 and 2023
eventsTreeNames = ("Events",)

specialBranchSizes = {
    "Proton_multiRP": "nProton_multiRP",
    "Proton_singleRP": "nProton_singleRP",
}
# redirector = "xrootd-cms.infn.it"

pileupScaleFactorsPath = "/data/dust/user/jniedzie/ttalps_cms/pileup_scale_factors.root"
pileupScaleFactorsHistName = "pileup_scale_factors"

# For the signal histogramming all given mathcing methods are applied separately to histograms
# More than one given method will not affect the other histograms
# Matching methods implemented are:
# "Segment" : max matching ratio (eg. 2.0f/3.0f)
# "DR" : max Delta R (eg. 0.1)
# "OuterDR" : max Delta R (eg. 0.1)
# "ProxDR" : max Delta R (eg. 0.1)
muonMatchingParams = {
    "Segment": 2.0 / 3.0,
    # "Segment": 1.5,
    # "DR" : 0.1
    # "OuterDR" : 0.1
    # "ProxDR" : 0.1
}
if skim[1] == "":
    muonMatchingParams = {}

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
dimuonSelection = skim[1]
if dimuonSelection == "":
    dimuonSelection = None
    ignoreDimuons = True
elif "JPsi" in dimuonSelection or "Z" in dimuonSelection:
  runNminus1Histograms = False

muonVertexCollections = {
    "SRDimuons": ("BestPFIsoDimuonVertex", muonVertexBaselineSelection + ["PFRelIsolationCut", "BestDimuonVertex"]),
    "SRDimuonsDSAChi2DCADPhi": ("BestPFIsoDimuonVertex", muonVertexBaselineSelection + ["PFRelIsolationCut", "Chi2DCACut", "BestDimuonVertex"]),
    "AlpDimuons": ("BestPFIsoDimuonVertex", muonVertexBaselineSelection + ["PFRelIsolationCut", "BestDimuonVertex"]),
    "SRDimuonNoIso": ("BestDimuonVertex", muonVertexBaselineSelection + ["BestDimuonVertex"]),
    "JPsiDimuons": ("BestDimuonVertex", muonVertexBaselineSelection + ["BestDimuonVertex"]),
    "JPsiDimuonIso": ("BestPFIsoDimuonVertex", muonVertexBaselineSelection + ["PFRelIsolationCut", "BestDimuonVertex"]),
    "JPsiDimuonsDSAChi2DCADPhi": ("BestDimuonVertex", muonVertexBaselineSelection + ["Chi2DCACut", "BestDimuonVertex"]),
    "ZDimuons": ("BestDimuonVertex", muonVertexBaselineSelection + ["BestDimuonVertex"]),
}
muonVertexCollection = muonVertexCollections[dimuonSelection] if dimuonSelection is not None else None
# input for muonVertexCollection, options are LooseMuonsVertexSegmentMatch, LooseNonLeadingMuonsVertexSegmentMatch, LooseNonTriggerMuonsVertexSegmentMatch
muonVertexCollectionInput = skim[2]
if muonVertexCollectionInput == "":
    if muonMatchingParams != {}:
        muonVertexCollectionInput = "LooseMuonsVertexSegmentMatch"
    else:
        muonVertexCollectionInput = None

histParams = ()
histParams2D = ()
irregularHistParams = ()
irregularHistParams2D = ()

helper = TTAlpsHistogrammerConfigHelper(
    muonMatchingParams, muonVertexCollection if muonVertexCollection is not None else None, muonVertexCollectionInput)

defaultHistParams = helper.get_default_params()
histParams += helper.get_basic_params()

if runLLPNanoAODHistograms:
  histParams += helper.get_llp_params()
  irregularHistParams += helper.get_llp_irregular_params()

if runNminus1Histograms:
  histParams += helper.get_nminus1_params()

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
  histParams2D += helper.get_abcd_2Dparams(runGenLevelABCD)

if runSingleMuonABCDHistograms:
  histParams2D += helper.get_singleMuon_abcd_2Dparams()
  irregularHistParams2D += helper.get_singleMuon_abcd_irregular_2Dparams()

if runABCDMothersHistograms:
  histParams2D += helper.get_abcd_mothers_2Dparams()

if runFakesHistograms:
  histParams += helper.get_fakes_params()

if runMuonTriggerObjectsHistograms:
  histParams += helper.get_muon_trigger_objects_params()

if runMuonMatchingRatioEffectHistograms:
  histParams += helper.get_muon_matching_effect_params()

SFvariationVariables = helper.get_SF_variation_variables()
# SFvariationVariables = [] # for testing to run histogrammer faster
