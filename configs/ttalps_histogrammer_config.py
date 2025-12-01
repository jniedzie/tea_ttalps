from scale_factors_config import get_scale_factors
from ttalps_extra_collections import get_extra_event_collections
from ttalps_object_cuts import *
from TTAlpsHistogrammerConfigHelper import TTAlpsHistogrammerConfigHelper

from ttalps_histogrammer_files_config import skim, applyScaleFactors, year

from ttalps_skimmer_looseSemimuonic_config import eventCuts as looseEventCuts
from ttalps_skimmer_signalLike_semimuonic_config import eventCuts as signalEventCuts
# defining eventCuts as the loose eventCuts and replacing MET pt from signal eventCuts
eventCuts = {
    **looseEventCuts,
    "MET_pt": signalEventCuts["MET_pt"],

    # The first value is whether to apply the cut, the second is the fraction of events in data with run>=319077.
    # To measure the second number, you can use the `utils/count_hem_events.py` script.
    "nano_applyHEMveto": (True, 0.6294),

    # Only the first argument matters
    "nano_applyJetVetoMaps": (True, False),
}

extraEventCollections = get_extra_event_collections(year)
scaleFactors = get_scale_factors(year)

nEvents = -1

# Should dimuon checks be skipped? Used for tt̄ CR, where we don't have dimuons
ignoreDimuons = False

runDefaultHistograms = True
runLLPTriggerHistograms = False
runPileupHistograms = False

# LLPNanoAODHistograms:
#  - muonMatchingParams loose muons
#  - muonMatchingParams loose muon vertex
#  - extra muon vertex collections
#  - tracker maps
runLLPNanoAODHistograms = True

# Histograms for Muon Trigger Objects
runMuonTriggerObjectsHistograms = False

runMuonMatchingHistograms = False  # TODO: this doesn't seem to work
runGenMuonHistograms = False  # can only be run on signal samples
runGenMuonVertexCollectionHistograms = False

# Create 2D histograms for ABCD background estimation
runABCDHistograms = False

# [MC only] Create ABCD histograms for gen-level mother information - only workd with runABCDHistograms = True
# resonances: FromALP, Resonant, NonResonant, FalseResonant
runGenLevelResonancesABCD = False
# mothers: particle PID based categories (takes more memory and time)
runGenLevelMothersABCD = False

# Create 2D histograms in the same way as for ABCD, but for single muon variables
runSingleMuonABCDHistograms = False

# [MC only] Create histograms with mother PIDs of dimuons entering ABCD histograms (quite heavy, turn off if not needed)
runABCDMothersHistograms = False

# [MC only] Create histograms for dimuons in the fakes region vs. non-fakes region
runFakesHistograms = False

# Apply Segment Matching on the GoodMuonVertexCollections after the dimuon selection
applySegmentMatchingAfterSelections = False

# Inlude N-1 histograms - NOTE: this will ignore the dimuon selection in order to include all N-1 dimuons properly
# Do not use for CR with dimuon selection
runNminus1Histograms = False

# Revert matching such that we use DSA matched that have been matched to PAT muons
runRevertedMatching = False

# Run without applying any events weights - for producing efficiency plots with correct uncertainties
noWeights = False

weightsBranchName = "genWeight"
rhoBranchName = "fixedGridRhoFastjetAll"  # for jec unc.
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

muonVertexBaselineSelection = [
    "InvariantMassCut",
    "ChargeCut",
    # "HitsInFrontOfVertexCut",
    # "DPhiBetweenMuonpTAndLxyCut",
    "DCACut",
    "CollinearityAngleCut",
    "Chi2Cut",
    "Chi2DCACut",
    # "Cos3DAngleCut",
]


# dimuonSelection and muonVertexCollection:
#  - uncomment the dimuonSelection you want to use and the muonVertexCollection will be given automatically
#  - to not use dimuonSelection and muonVertexCollection: set dimuonSelection to None
dimuonSelection = skim[1]
if dimuonSelection == "":
  dimuonSelection = None
  ignoreDimuons = True

muonVertexCollections = {
    "SRDimuons": ("BestPFIsoDimuonVertex", muonVertexBaselineSelection + ["PFRelIsolationCut", "BestDimuonVertex"]),
    "SRDimuonsNoChi2": ("BestPFIsoDimuonVertex", muonVertexBaselineSelection + ["PFRelIsolationCut", "BestDimuonVertex"]),
    "JPsiDimuons": ("BestDimuonVertex", muonVertexBaselineSelection + ["BestDimuonVertex"]),
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
    muonMatchingParams, muonVertexCollection if muonVertexCollection is not None else None, muonVertexCollectionInput, runRevertedMatching)

defaultHistParams = helper.get_default_params()
histParams += helper.get_basic_params()

if runLLPNanoAODHistograms:
  histParams += helper.get_llp_params()
  irregularHistParams += helper.get_llp_irregular_params()
  histParams2D += helper.get_llp_2d_params()

if runNminus1Histograms:
  histParams += helper.get_nminus1_params()
  histParams2D += helper.get_nminus1_params2D()

if runGenMuonVertexCollectionHistograms:
  histParams += helper.get_gen_vertex_params()
if runGenMuonHistograms:
  histParams += helper.get_gen_params()
  histParams += helper.get_gen_matched_params()
  irregularHistParams += helper.get_gen_matched_irregular_params()

if runLLPTriggerHistograms:
  histParams += helper.get_trigger_params()

if runMuonMatchingHistograms:
  histParams += helper.get_matching_params()
  histParams2D += helper.get_2D_matching_params()

if runABCDHistograms:
  histParams += helper.get_abcd_1Dparams(runGenLevelResonancesABCD, runGenLevelMothersABCD)
  histParams2D += helper.get_abcd_2Dparams(runGenLevelResonancesABCD, runGenLevelMothersABCD)

if runSingleMuonABCDHistograms:
  histParams2D += helper.get_singleMuon_abcd_2Dparams()
  irregularHistParams2D += helper.get_singleMuon_abcd_irregular_2Dparams()

if runABCDMothersHistograms:
  histParams2D += helper.get_abcd_mothers_2Dparams()

if runFakesHistograms:
  histParams += helper.get_fakes_params()

if runMuonTriggerObjectsHistograms:
  histParams += helper.get_muon_trigger_objects_params()

SFvariationVariables = helper.get_SF_variation_variables()
if runGenLevelResonancesABCD or runABCDMothersHistograms or runNminus1Histograms or runRevertedMatching:
  SFvariationVariables = [] # to run histogrammer faster and take up less dust space
