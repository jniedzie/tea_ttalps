#include "ArgsManager.hpp"
#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "EventReader.hpp"
#include "HistogramsFiller.hpp"
#include "HistogramsHandler.hpp"
#include "TTAlpsHistogramFiller.hpp"
#include "TTAlpsObjectsManager.hpp"
#include "UserExtensionsHelpers.hpp"

using namespace std;

int main(int argc, char **argv) {
  auto args = make_unique<ArgsManager>(argc, argv);
  if (!args->GetString("config").has_value()) {
    fatal() << "No config file provided" << endl;
    exit(1);
  }

  ConfigManager::Initialize(args->GetString("config").value());
  auto &config = ConfigManager::GetInstance();

  if (args->GetString("input_path").has_value()) {
    config.SetInputPath(args->GetString("input_path").value());
  }
  if (args->GetString("output_path").has_value()) {
    config.SetHistogramsOutputPath(args->GetString("output_path").value());
  }
  if (args->GetString("output_hists_path").has_value()) {
    config.SetHistogramsOutputPath(args->GetString("output_hists_path").value());
  }
  if (args->GetString("output_trees_path").has_value()) {
    config.SetTreesOutputPath(args->GetString("output_trees_path").value());
  }

  info() << "Creating objects..." << endl;
  auto eventReader = make_shared<EventReader>();
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader);
  auto histogramsHandler = make_shared<HistogramsHandler>();
  auto histogramFiller = make_unique<HistogramsFiller>(histogramsHandler);
  auto ttalpsHistogramsFiller = make_unique<TTAlpsHistogramFiller>(histogramsHandler);
  auto ttAlpsCuts = make_unique<TTAlpsCuts>();
  auto ttalpsObjectsManager = make_unique<TTAlpsObjectsManager>();

  bool runDefaultHistograms, runLLPTriggerHistograms;
  bool runLLPNanoAODHistograms, runMuonMatchingHistograms, runGenMuonHistograms, runGenMuonVertexCollectionHistograms;
  bool runABCDHistograms;
  config.GetValue("runDefaultHistograms", runDefaultHistograms);
  config.GetValue("runLLPTriggerHistograms", runLLPTriggerHistograms);
  config.GetValue("runLLPNanoAODHistograms", runLLPNanoAODHistograms);
  config.GetValue("runMuonMatchingHistograms", runMuonMatchingHistograms);
  config.GetValue("runGenMuonHistograms", runGenMuonHistograms);
  config.GetValue("runGenMuonVertexCollectionHistograms", runGenMuonVertexCollectionHistograms);
  config.GetValue("runABCDHistograms", runABCDHistograms);

  cutFlowManager->RegisterCut("initial");

  auto categories = {"", "Pat", "PatDSA", "DSA"};

  for (string category : categories) {
    ttAlpsCuts->RegisterInitialDimuonCuts(cutFlowManager, category);
    ttAlpsCuts->RegisterDimuonCuts(cutFlowManager, category);
  }

  info() << "Starting event loop..." << endl;
  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    ttalpsObjectsManager->InsertMatchedLooseMuonsCollections(event);
    ttalpsObjectsManager->InsertMuonVertexCollection(event);
    ttalpsObjectsManager->InsertNminus1VertexCollections(event);
    ttalpsObjectsManager->InsertBaseLooseMuonVertexCollection(event);

    map<string,float> eventWeights = asTTAlpsEvent(event)->GetEventWeights();
    histogramsHandler->SetEventWeights(eventWeights);
    cutFlowManager->SetEventWeight(eventWeights["systematic"]);

    bool passesDimuonCuts = false;
    for (string category : categories) {
      passesDimuonCuts |= ttAlpsCuts->PassesDimuonCuts(event, cutFlowManager, category);
    }
    if (!passesDimuonCuts) continue;
    
    if (runDefaultHistograms) {
      cutFlowManager->UpdateCutFlow("initial");
      ttalpsHistogramsFiller->FillNormCheck(event);
      ttalpsHistogramsFiller->FillDataCheck(event);
      ttalpsHistogramsFiller->FillDefaultVariables(event);
    }
    if (runLLPNanoAODHistograms) {
      ttalpsHistogramsFiller->FillCustomTTAlpsVariablesForLooseMuons(event);
      ttalpsHistogramsFiller->FillCustomTTAlpsVariablesForMuonVertexCollections(event);
    }

    if (runMuonMatchingHistograms) {
      ttalpsObjectsManager->InsertMatchedLooseMuonEfficiencyCollections(event);
      ttalpsHistogramsFiller->FillCustomTTAlpsMuonMatchingVariables(event);
    }
    if (runGenMuonHistograms) {
      ttalpsHistogramsFiller->FillCustomTTAlpsGenMuonVariables(event);
    }
    if (runGenMuonVertexCollectionHistograms) {
      ttalpsHistogramsFiller->FillCustomTTAlpsGenMuonVertexCollectionsVariables(event);
    }

    if (runLLPTriggerHistograms) {
      ttalpsHistogramsFiller->FillTriggerStudyHistograms(event, "NoExtraTrigger");
      
      if (ttAlpsCuts->PassesSingleMuonTrigger(event)) {
        ttalpsHistogramsFiller->FillTriggerStudyHistograms(event, "SingleMuonTrigger");
      }
      if (ttAlpsCuts->PassesDoubleMuonTrigger(event)) {
        ttalpsHistogramsFiller->FillTriggerStudyHistograms(event, "DoubleMuonTrigger");
      }
    }
    if (runABCDHistograms) {
      ttalpsHistogramsFiller->FillABCDHistograms(event);
    }
  }

  if (runDefaultHistograms) {
    histogramFiller->FillCutFlow(cutFlowManager);
  }
  if (runDefaultHistograms) {
    for (string category : categories) {
      ttalpsHistogramsFiller->FillDimuonCutFlows(cutFlowManager, category);
    }
  }
  cutFlowManager->Print();
  histogramsHandler->SaveHistograms();

  ttAlpsCuts->PrintDimuonCutFlow(cutFlowManager);

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}