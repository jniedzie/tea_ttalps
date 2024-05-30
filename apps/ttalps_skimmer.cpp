#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "EventReader.hpp"
#include "EventWriter.hpp"
#include "HistogramsHandler.hpp"
#include "Profiler.hpp"
#include "TTAlpsSelections.hpp"
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
  auto ttAlpsSelections = make_unique<TTAlpsSelections>();
  auto ttalpsObjectsManager = make_unique<TTAlpsObjectsManager>();

  info() << "Retrieving values from config file... " << endl;

  bool applyLooseSkimming, applyTTbarLikeSkimming, applySignalLikeSkimming, applyTTZLikeSkimming;
  config.GetValue("applyLooseSkimming", applyLooseSkimming);
  config.GetValue("applyTTbarLikeSkimming", applyTTbarLikeSkimming);
  config.GetValue("applySignalLikeSkimming", applySignalLikeSkimming);
  config.GetValue("applyTTZLikeSkimming", applyTTZLikeSkimming);

  info() << "Registering cuts" << endl;

  cutFlowManager->RegisterCut("initial");
  if(applyLooseSkimming){
    cutFlowManager->RegisterCut("goldenJson");
    cutFlowManager->RegisterCut("trigger");
    cutFlowManager->RegisterCut("metFilters");
  }

  if(applyTTbarLikeSkimming) ttAlpsSelections->RegisterSingleLeptonSelections(cutFlowManager);
  if(applyTTZLikeSkimming) ttAlpsSelections->RegisterTTZLikeSelections(cutFlowManager);
  if(applySignalLikeSkimming) ttAlpsSelections->RegisterSignalLikeSelections(cutFlowManager);

  eventProcessor->RegisterCuts(cutFlowManager);
    
  info() << "Starting events loop" << endl;

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    cutFlowManager->UpdateCutFlow("initial");


    if(applyLooseSkimming){
      if (!eventProcessor->PassesGoldenJson(event)) continue;
      cutFlowManager->UpdateCutFlow("goldenJson");

      if (!eventProcessor->PassesTriggerSelections(event)) continue;
      cutFlowManager->UpdateCutFlow("trigger");

      if (!eventProcessor->PassesMetFilters(event)) continue;
      cutFlowManager->UpdateCutFlow("metFilters");
    }


    if(applyTTbarLikeSkimming){
      if(!ttAlpsSelections->PassesSingleLeptonSelections(event, cutFlowManager)) continue;
    }


    if(applySignalLikeSkimming){
      ttalpsObjectsManager->InsertMatchedLooseMuonsCollections(event);
      if(!ttAlpsSelections->PassesSignalLikeSelections(event, cutFlowManager)) continue;
    }
    if(applyTTZLikeSkimming){
      if(!ttAlpsSelections->PassesTTZLikeSelections(event, cutFlowManager)) continue;
    }

    if(!eventProcessor->PassesEventSelections(event, cutFlowManager)) continue;
    
    eventWriter->AddCurrentEvent("Events");
  }
  cutFlowManager->Print();
  cutFlowManager->SaveCutFlow();
  eventWriter->Save();

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}