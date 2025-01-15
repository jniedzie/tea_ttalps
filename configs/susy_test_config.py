from ttalps_extra_collections import extraEventCollections

## specify how many events to run on (and how often to print current event number)
nEvents = -1
printEveryNevents = 1000

# specify input/output paths 
# inputFilePath = "/pnfs/desy.de/cms/tier2/store/user/lrygaard/ttalps/SingleMuon/LLPnanoAODv1_LLPminiAOD/240722_082302/0000/output_124.root"
inputFilePath = "../output_124.root"
histogramsOutputFilePath = "../susy_test_output.root"
treeOutputFilePath = "../susy_test_tree.root"

# define default histograms (can be filled automatically with HistogramsFiller, based on collection and variable names)
defaultHistParams = []

# define custom histograms (you will have to fill them in your HistogramsFiller)
histParams = []

for centralTag in ["centralJetsEq0", "centralJetsGe1"]:
  for forwardTag in ["forwardJetsEq0", "forwardJetsGe1"]:
    for bTag in ["bJetsEq0", "bJetsGe1"]:
      for muonPt in ["MuPtGe3", "MuPtGe5", "MuPtGe10", "MuPtGe15", "MuPtGe20", "MuPtGe25", "MuPtGe30"]:
        for boost in ["", "_boostGe1p0", "_boostGe1p5", "_boostGe1p7", "_boostGe2p0"]:
          histParams.append(
            (f"mInv_{centralTag}_{forwardTag}_{bTag}_{muonPt}{boost}", 100, 10, 70, ""),
          )

triggerSelection = (
    "HLT_IsoMu24",
)

eventSelections = {
    "nLooseIsoPATMuons": (2, 999999),
}

weightsBranchName = "genWeight"

eventsTreeNames = ["Events",]
specialBranchSizes = {
  "Proton_multiRP": "nProton_multiRP",
  "Proton_singleRP": "nProton_singleRP",
}
branchesToKeep = ["*"]
branchesToRemove = []