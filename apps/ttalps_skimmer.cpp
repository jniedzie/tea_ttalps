#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "EventReader.hpp"
#include "EventWriter.hpp"
#include "HistogramsHandler.hpp"
#include "Profiler.hpp"
#include "TTAlpsSelections.hpp"
#include "UserExtensionsHelpers.hpp"

using namespace std;

void CheckArgs(int argc, char **argv) {
  if (argc != 2 && argc != 4) {
    fatal() << "Usage: " << argv[0] << " config_path"<<endl;
    fatal() << "or"<<endl;
    fatal() << argv[0] << " config_path input_path output_path"<<endl;
    exit(1);
  }
}

int main(int argc, char **argv) {
  CheckArgs(argc, argv);
  ConfigManager::Initialize(argv[1]);
  auto &config = ConfigManager::GetInstance();
  
  if(argc == 4){
    config.SetInputPath(argv[2]);
    config.SetOutputPath(argv[3]);
  }

  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);
  auto eventProcessor = make_unique<EventProcessor>();
  auto ttAlpsSelections = make_unique<TTAlpsSelections>();

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