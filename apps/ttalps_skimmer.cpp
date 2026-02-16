#include "ArgsManager.hpp"
#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "EventReader.hpp"
#include "EventWriter.hpp"
#include "HistogramsHandler.hpp"
#include "Profiler.hpp"
#include "TTAlpsCuts.hpp"
#include "TTAlpsObjectsManager.hpp"
#include "UserExtensionsHelpers.hpp"
#include "NanoEventProcessor.hpp"

using namespace std;

int main(int argc, char **argv) {
  vector<string> requiredArgs = {"config"};
  vector<string> optionalArgs = {"input_path", "output_trees_path"};
  auto args = make_unique<ArgsManager>(argc, argv, requiredArgs, optionalArgs);
  ConfigManager::Initialize(args);
  
  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);
  auto eventProcessor = make_unique<EventProcessor>();
  auto nanoEventProcessor = make_unique<NanoEventProcessor>();
  auto ttAlpsCuts = make_unique<TTAlpsCuts>();
  auto ttalpsObjectsManager = make_unique<TTAlpsObjectsManager>();

  info() << "Retrieving values from config file... " << endl;
  
  bool applyLooseSkimming, applyTTZLikeSkimming;

  auto &config = ConfigManager::GetInstance();
  config.GetValue("applyLooseSkimming", applyLooseSkimming);
  config.GetValue("applyTTZLikeSkimming", applyTTZLikeSkimming);

  info() << "Registering cuts" << endl;

  cutFlowManager->RegisterCut("initial");
  if (applyLooseSkimming) {
    cutFlowManager->RegisterCut("goldenJson");
    cutFlowManager->RegisterCut("trigger");
    cutFlowManager->RegisterCut("metFilters");
  }

  if (applyTTZLikeSkimming) ttAlpsCuts->RegisterTTZLikeCuts(cutFlowManager);

  eventProcessor->RegisterCuts(cutFlowManager);

  info() << "Starting events loop" << endl;

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);
    ttalpsObjectsManager->InsertMatchedLooseMuonsCollections(event);

    cutFlowManager->UpdateCutFlow("initial");

    if (applyLooseSkimming) {
      if (!eventProcessor->PassesGoldenJson(event)) continue;
      cutFlowManager->UpdateCutFlow("goldenJson");

      if (!eventProcessor->PassesTriggerCuts(event)) continue;
      cutFlowManager->UpdateCutFlow("trigger");

      if (!eventProcessor->PassesMetFilters(event)) continue;
      cutFlowManager->UpdateCutFlow("metFilters");
    }

    if (applyTTZLikeSkimming) {
      if (!ttAlpsCuts->PassesTTZLikeCuts(event, cutFlowManager)) continue;
    }

    auto nanoEvent = asNanoEvent(event);
    if (!nanoEventProcessor->PassesEventCuts(nanoEvent, cutFlowManager)) continue;

    eventWriter->AddCurrentEvent("Events");
  }
  cutFlowManager->Print();
  cutFlowManager->SaveCutFlow();
  eventWriter->Save();

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}