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
#include "ArgsManager.hpp"

using namespace std;

int main(int argc, char **argv) {

  auto args = make_unique<ArgsManager>(argc, argv);
  // check if optional value "config" is present
  if (!args->GetString("config").has_value()) {
    fatal() << "No config file provided" << endl;
    exit(1);
  }

  ConfigManager::Initialize(args->GetString("config").value());
  auto &config = ConfigManager::GetInstance();
  
  if (args->GetString("input_path").has_value()) {
    config.SetInputPath(args->GetString("input_path").value());
  }
  if (args->GetString("output_trees_path").has_value()) {
    config.SetTreesOutputPath(args->GetString("output_trees_path").value());
  }
  
  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);
  auto eventProcessor = make_unique<EventProcessor>();
  auto ttAlpsCuts = make_unique<TTAlpsCuts>();
  auto ttalpsObjectsManager = make_unique<TTAlpsObjectsManager>();

  info() << "Retrieving values from config file... " << endl;

  bool applyLooseSkimming, applyTTZLikeSkimming;
  config.GetValue("applyLooseSkimming", applyLooseSkimming);
  config.GetValue("applyTTZLikeSkimming", applyTTZLikeSkimming);

  info() << "Registering cuts" << endl;

  cutFlowManager->RegisterCut("initial");
  if(applyLooseSkimming){
    cutFlowManager->RegisterCut("goldenJson");
    cutFlowManager->RegisterCut("trigger");
    cutFlowManager->RegisterCut("metFilters");
  }

  if(applyTTZLikeSkimming) ttAlpsCuts->RegisterTTZLikeCuts(cutFlowManager);

  eventProcessor->RegisterCuts(cutFlowManager);
    
  info() << "Starting events loop" << endl;

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);
    ttalpsObjectsManager->InsertMatchedLooseMuonsCollections(event);

    // map<string,float> eventWeights = asTTAlpsEvent(event)->GetEventWeights();
    // cutFlowManager->SetEventWeight(eventWeights["default"]);

    cutFlowManager->UpdateCutFlow("initial");

    

    if(applyLooseSkimming){
      if (!eventProcessor->PassesGoldenJson(event)) continue;
      cutFlowManager->UpdateCutFlow("goldenJson");

      if (!eventProcessor->PassesTriggerCuts(event)) continue;
      cutFlowManager->UpdateCutFlow("trigger");

      if (!eventProcessor->PassesMetFilters(event)) continue;
      cutFlowManager->UpdateCutFlow("metFilters");
    }

    if(applyTTZLikeSkimming){
      if(!ttAlpsCuts->PassesTTZLikeCuts(event, cutFlowManager)) continue;
    }

    if(!eventProcessor->PassesEventCuts(event, cutFlowManager)) continue;
    
    eventWriter->AddCurrentEvent("Events");
  }
  cutFlowManager->Print();
  cutFlowManager->SaveCutFlow();
  eventWriter->Save();

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}