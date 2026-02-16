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
  vector<string> requiredArgs = {"config"};
  vector<string> optionalArgs = {"input_path", "output_hists_path"};
  auto args = make_unique<ArgsManager>(argc, argv, requiredArgs, optionalArgs);
  ConfigManager::Initialize(args);

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
  bool runMuonTriggerObjectsHistograms;
  bool runABCDHistograms, runSingleMuonABCDHistograms, runABCDMothersHistograms, runFakesHistograms;
  bool ignoreDimuons, runNminus1Histograms;
  bool runGenLevelResonancesABCD, runGenLevelMothersABCD, runRevertedMatching, noWeights;

  auto &config = ConfigManager::GetInstance();

  config.GetValue("runDefaultHistograms", runDefaultHistograms);
  config.GetValue("runLLPTriggerHistograms", runLLPTriggerHistograms);
  config.GetValue("runLLPNanoAODHistograms", runLLPNanoAODHistograms);
  config.GetValue("runMuonMatchingHistograms", runMuonMatchingHistograms);
  config.GetValue("runGenMuonHistograms", runGenMuonHistograms);
  config.GetValue("runGenMuonVertexCollectionHistograms", runGenMuonVertexCollectionHistograms);
  config.GetValue("runABCDHistograms", runABCDHistograms);
  config.GetValue("runSingleMuonABCDHistograms", runSingleMuonABCDHistograms);
  config.GetValue("runMuonTriggerObjectsHistograms", runMuonTriggerObjectsHistograms);
  config.GetValue("runABCDMothersHistograms", runABCDMothersHistograms);
  config.GetValue("runFakesHistograms", runFakesHistograms);
  config.GetValue("ignoreDimuons", ignoreDimuons);
  config.GetValue("runNminus1Histograms", runNminus1Histograms);
  config.GetValue("runGenLevelResonancesABCD", runGenLevelResonancesABCD);
  config.GetValue("runGenLevelMothersABCD", runGenLevelMothersABCD);
  config.GetValue("runRevertedMatching", runRevertedMatching);
  config.GetValue("noWeights", noWeights);

  cutFlowManager->RegisterCut("initial");

  auto categories = {"", "Pat", "PatDSA", "DSA"};

  for (string category : categories) {
    ttAlpsCuts->RegisterInitialDimuonCuts(cutFlowManager, category);
    ttAlpsCuts->RegisterDimuonCuts(cutFlowManager, category);
  }

  info() << "Starting event loop..." << endl;
  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);
    ttalpsObjectsManager->InsertMuonTriggerCollections(event);
    ttalpsObjectsManager->InsertMatchedLooseMuonsCollections(event);
    ttalpsObjectsManager->InsertNonLeadingLooseMuonsCollections(event);
    ttalpsObjectsManager->InsertRevertedMatchedMuonsCollections(event);
    if (!ignoreDimuons) {
      ttalpsObjectsManager->InsertMuonVertexCollection(event);
      ttalpsObjectsManager->InsertBaseLooseMuonVertexCollection(event);
      ttalpsObjectsManager->InsertNminus1VertexCollections(event);
      if (runRevertedMatching) {
        ttalpsObjectsManager->InsertRevertedMatchedDSAMuonVertexCollection(event);
      }
    }
    map<string, float> eventWeights = {{"default", 1.0}};
    if (!noWeights) {
      eventWeights = asTTAlpsEvent(event)->GetEventWeights();
    }
    histogramsHandler->SetEventWeights(eventWeights);
    
    cutFlowManager->SetEventWeight(eventWeights["default"]);
    if (!ignoreDimuons && !runNminus1Histograms) {
      bool passesDimuonCuts = false;
      for (string category : categories) {
        passesDimuonCuts |= ttAlpsCuts->PassesDimuonCuts(event, cutFlowManager, category);
      }
      if (!passesDimuonCuts) continue;
    }
    if (runDefaultHistograms) {
      cutFlowManager->UpdateCutFlow("initial");
      ttalpsHistogramsFiller->FillNormCheck();
      ttalpsHistogramsFiller->FillDataCheck(event);
      ttalpsHistogramsFiller->FillDefaultVariables(event);
    }
    if (runLLPNanoAODHistograms) {
      ttalpsHistogramsFiller->FillCustomTTAlpsVariablesForLooseMuons(event, runRevertedMatching);
      if (!ignoreDimuons) {
        ttalpsHistogramsFiller->FillCustomTTAlpsVariablesForMuonVertexCollections(event, runNminus1Histograms, runRevertedMatching);
      }
    }
    if (runMuonTriggerObjectsHistograms) {
      ttalpsHistogramsFiller->FillMuonTriggerObjectsHistograms(event);
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
      if (ttAlpsCuts->PassesSingleMuonTrigger(event) || ttAlpsCuts->PassesDoubleMuonTrigger(event)) {
        ttalpsHistogramsFiller->FillTriggerStudyHistograms(event, "SingleorDoubleMuonTrigger");
      }
    }
    if (runABCDHistograms) {
      ttalpsHistogramsFiller->FillABCDHistograms(event, runGenLevelResonancesABCD, runGenLevelMothersABCD);
    }
    if (runSingleMuonABCDHistograms) {
      ttalpsHistogramsFiller->FillSingleMuonABCDHistograms(event);
    }
    if (runABCDMothersHistograms) {
      ttalpsHistogramsFiller->FillABCDMothersHistograms(event, runFakesHistograms);
    }
    if (runFakesHistograms) {
      ttalpsHistogramsFiller->FillFakesHistograms(event);
    }
  }

  if (runDefaultHistograms) {
    histogramFiller->FillCutFlow(cutFlowManager);
    for (string category : categories) {
      ttalpsHistogramsFiller->FillDimuonCutFlows(cutFlowManager, category);
    }
  }
  cutFlowManager->Print();
  histogramsHandler->SaveHistograms();

  ttAlpsCuts->PrintDimuonCutFlow(cutFlowManager);

  auto &logger = Logger::GetInstance();
  logger.Print();

  info() << "\nAll done, exitting" << endl;
  _exit(0);
  return 0;
}