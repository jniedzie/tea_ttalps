#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "EventReader.hpp"
#include "HistogramsHandler.hpp"
#include "HistogramsFiller.hpp"
#include "ExtensionsHelpers.hpp"

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
  
  if(argc == 4){
    auto &config = ConfigManager::GetInstance();
    config.SetInputPath(argv[2]);
    config.SetOutputPath(argv[3]);
  }

  auto eventReader = make_shared<EventReader>();
  auto histogramsHandler = make_shared<HistogramsHandler>();
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader);
  auto histogramsFiller = make_unique<HistogramsFiller>(histogramsHandler);

  cutFlowManager->RegisterCut("initial");

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    cutFlowManager->UpdateCutFlow("initial");
    histogramsFiller->FillDefaultVariables(event);

    auto muons = event->GetCollection("Muon");
    for(auto physObj : *muons){
      auto muon = asMuon(physObj);
      histogramsHandler->Fill("Muon_scaledPt", muon->Get("pt"), muon->GetRecoScaleFactor());
    }
  }
  
  cutFlowManager->Print();
  histogramsFiller->FillCutFlow(cutFlowManager);
  histogramsHandler->SaveHistograms();
  return 0;
}