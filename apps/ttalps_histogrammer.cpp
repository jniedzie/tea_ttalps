#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "EventReader.hpp"
#include "HistogramsHandler.hpp"
#include "TTAlpsHistogramFiller.hpp"
#include "TTAlpsObjectsManager.hpp"
#include "HistogramsFiller.hpp"
#include "UserExtensionsHelpers.hpp"
#include "ArgsManager.hpp"

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
  auto ttalpsObjectsManager = make_unique<TTAlpsObjectsManager>();

  bool runDefaultHistograms, runCustomTTAlpsHistograms, runTriggerHistograms, runPileupHistograms;
  bool runLLPNanoAODHistograms, runLLPNanoAOD2DHistograms, runMuonMatchingHistograms, runGenMuonHistograms;
  bool runLLPNanoAODVertexHistograms;
  config.GetValue("runDefaultHistograms", runDefaultHistograms);
  config.GetValue("runCustomTTAlpsHistograms", runCustomTTAlpsHistograms);
  config.GetValue("runTriggerHistograms", runTriggerHistograms);
  config.GetValue("runPileupHistograms", runPileupHistograms);
  config.GetValue("runLLPNanoAODHistograms", runLLPNanoAODHistograms);
  config.GetValue("runMuonMatchingHistograms", runMuonMatchingHistograms);
  config.GetValue("runGenMuonHistograms", runGenMuonHistograms);
  config.GetValue("runLLPNanoAODVertexHistograms", runLLPNanoAODVertexHistograms);

  if (runPileupHistograms) cutFlowManager->RegisterCut("initial");

  // check if cutflowmanager has cut "initial"
  if (!cutFlowManager->HasCut("initial")) cutFlowManager->RegisterCut("initial");
  
  info() << "Starting event loop..." << endl;
  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    if (runLLPNanoAODHistograms || runMuonMatchingHistograms || runGenMuonHistograms || runLLPNanoAODVertexHistograms) {
      ttalpsObjectsManager->InsertMatchedLooseMuonsCollections(event);
      ttalpsObjectsManager->InsertGoodLooseMuonVertexCollection(event);
    }

    if (runDefaultHistograms) {
      cutFlowManager->UpdateCutFlow("initial");
      ttalpsHistogramsFiller->FillNormCheck(event);
      ttalpsHistogramsFiller->FillDefaultVariables(event);
    }
    if (runCustomTTAlpsHistograms) {
      ttalpsHistogramsFiller->FillCustomTTAlpsVariables(event);
    }

    if (runLLPNanoAODHistograms) {
      ttalpsHistogramsFiller->FillCustomTTAlpsVariablesFromLLPNanoAOD(event);
    }
    if (runLLPNanoAOD2DHistograms) {
      ttalpsHistogramsFiller->FillCustomTTAlps2DVariablesFromLLPNanoAOD(event);      
    }
    if(runMuonMatchingHistograms){
      ttalpsObjectsManager->InsertMatchedLooseMuonEfficiencyCollections(event);
      ttalpsHistogramsFiller->FillCustomTTAlpsMuonMatchingVariables(event);
    }
    if(runGenMuonHistograms){
      ttalpsHistogramsFiller->FillCustomTTAlpsGenMuonVariables(event);
    }

    if (runTriggerHistograms) {
      auto ttAlpsEvent = asTTAlpsEvent(event);
      string ttbarCategory = ttAlpsEvent->GetTTbarEventCategory();
      ttalpsHistogramsFiller->FillTriggerVariables(event, "inclusive");
      ttalpsHistogramsFiller->FillTriggerVariables(event, ttbarCategory);
      ttalpsHistogramsFiller->FillTriggerVariablesPerTriggerSet(event, "inclusive");
      ttalpsHistogramsFiller->FillTriggerVariablesPerTriggerSet(event, ttbarCategory);
    }

    if (runPileupHistograms) {
      cutFlowManager->UpdateCutFlow("initial");
      histogramFiller->FillDefaultVariables(event);
    }
    
    if (runLLPNanoAODVertexHistograms) {
      ttalpsHistogramsFiller->FillBasicMuonVertexHistograms(event);
    }
  }

  if(runTriggerHistograms) ttalpsHistogramsFiller->FillTriggerEfficiencies();
  if(runDefaultHistograms || runPileupHistograms) histogramFiller->FillCutFlow(cutFlowManager);
  
  cutFlowManager->Print();
  histogramsHandler->SaveHistograms();

  auto &logger = Logger::GetInstance();
  logger.Print();

  return 0;
}