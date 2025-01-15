#include "ConfigManager.hpp"
#include "EventReader.hpp"
#include "ExtensionsHelpers.hpp"
#include "HistogramsHandler.hpp"
#include "HistogramsFiller.hpp"
#include "ArgsManager.hpp"
#include "EventProcessor.hpp"

// If you also created a histogram filler, you can include it here
// #include "MyHistogramsFiller.hpp"

using namespace std;

void fillHistograms(shared_ptr<Event> event, shared_ptr<HistogramsHandler> histogramsHandler, string tag, float dimuon_m_inv, float dimuon_boost) {
  histogramsHandler->Fill(tag.c_str(), dimuon_m_inv, 1.0);
  if(dimuon_boost > 1.0) histogramsHandler->Fill((tag+"_boostGe1p0").c_str(), dimuon_m_inv, 1.0);
  if(dimuon_boost > 1.5) histogramsHandler->Fill((tag+"_boostGe1p5").c_str(), dimuon_m_inv, 1.0);
  if(dimuon_boost > 1.7) histogramsHandler->Fill((tag+"_boostGe1p7").c_str(), dimuon_m_inv, 1.0);
  if(dimuon_boost > 2.0) histogramsHandler->Fill((tag+"_boostGe2p0").c_str(), dimuon_m_inv, 1.0);
}

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
  if (args->GetString("output_hists_path").has_value()) {
    config.SetHistogramsOutputPath(args->GetString("output_hists_path").value());
  }
  
  auto eventReader = make_shared<EventReader>();
  auto eventWriter = make_shared<EventWriter>(eventReader);
  auto cutFlowManager = make_shared<CutFlowManager>(eventReader, eventWriter);
  auto histogramsHandler = make_shared<HistogramsHandler>();
  auto eventProcessor = make_unique<EventProcessor>();

  cutFlowManager->RegisterCut("initial");
  eventProcessor->RegisterCuts(cutFlowManager);
  cutFlowManager->RegisterCut("opposite_charge");
  cutFlowManager->RegisterCut("muons_momenta");
  cutFlowManager->RegisterCut("muons_eta");
  cutFlowManager->RegisterCut("forward_jets");
  cutFlowManager->RegisterCut("dimuon_boost");

  for (int iEvent = 0; iEvent < eventReader->GetNevents(); iEvent++) {
    auto event = eventReader->GetEvent(iEvent);

    if(!eventProcessor->PassesEventSelections(event, cutFlowManager)) continue;

    auto muon1 = asNanoMuon(event->GetCollection("LooseIsoPATMuons")->at(0));
    auto muon2 = asNanoMuon(event->GetCollection("LooseIsoPATMuons")->at(1));

    if(muon1->GetCharge() * muon2->GetCharge() > 0) continue;
    cutFlowManager->UpdateCutFlow("opposite_charge");

    // if(muon1->GetFourVector().Pt() < 25.0 || muon2->GetFourVector().Pt() < 18.0) continue;
    // cutFlowManager->UpdateCutFlow("muons_momenta");

    // if(fabs(muon1->GetFourVector().Eta()) > 2.1 || fabs(muon2->GetFourVector().Eta()) > 2.1) continue;
    // cutFlowManager->UpdateCutFlow("muons_eta");

    int nForwardJetsPlus = event->GetCollection("GoodForwardJetsPlus")->size();
    int nForwardJetsMinus = event->GetCollection("GoodForwardJetsMinus")->size();
    int nForwardJets = nForwardJetsPlus + nForwardJetsMinus;
    string forwardTag = "";
    if(nForwardJets == 0) forwardTag = "forwardJetsEq0";
    else if(nForwardJets >= 1) forwardTag = "forwardJetsGe1";

    int nCentralJets = event->GetCollection("GoodCentralNonBtaggedJets")->size();
    string centralTag = "";
    if(nCentralJets == 0) centralTag = "centralJetsEq0";
    else if(nCentralJets >= 1) centralTag = "centralJetsGe1";

    int nBtaggedJets = event->GetCollection("GoodMediumBtaggedJets")->size();
    string btaggedTag = "";
    if(nBtaggedJets == 0) btaggedTag = "bJetsEq0";
    else if(nBtaggedJets >= 1) btaggedTag = "bJetsGe1";

    string tag = "mInv_" + centralTag + "_" + forwardTag + "_" + btaggedTag;

    auto dimuon = muon1->GetFourVector() + muon2->GetFourVector();
    float dimuon_boost = dimuon.Pt() / dimuon.M();
    float dimuon_m_inv = dimuon.M();

    if(muon1->GetFourVector().Pt() > 3.0 && muon2->GetFourVector().Pt() > 3.0)    fillHistograms(event, histogramsHandler, tag+"_MuPtGe3", dimuon_m_inv, dimuon_boost);
    if(muon1->GetFourVector().Pt() > 5.0 && muon2->GetFourVector().Pt() > 5.0)    fillHistograms(event, histogramsHandler, tag+"_MuPtGe5", dimuon_m_inv, dimuon_boost);
    if(muon1->GetFourVector().Pt() > 10.0 && muon2->GetFourVector().Pt() > 10.0)  fillHistograms(event, histogramsHandler, tag+"_MuPtGe10", dimuon_m_inv, dimuon_boost);
    if(muon1->GetFourVector().Pt() > 15.0 && muon2->GetFourVector().Pt() > 15.0)  fillHistograms(event, histogramsHandler, tag+"_MuPtGe15", dimuon_m_inv, dimuon_boost);
    if(muon1->GetFourVector().Pt() > 20.0 && muon2->GetFourVector().Pt() > 20.0)  fillHistograms(event, histogramsHandler, tag+"_MuPtGe20", dimuon_m_inv, dimuon_boost);
    if(muon1->GetFourVector().Pt() > 25.0 && muon2->GetFourVector().Pt() > 25.0)  fillHistograms(event, histogramsHandler, tag+"_MuPtGe25", dimuon_m_inv, dimuon_boost);
    if(muon1->GetFourVector().Pt() > 30.0 && muon2->GetFourVector().Pt() > 30.0)  fillHistograms(event, histogramsHandler, tag+"_MuPtGe30", dimuon_m_inv, dimuon_boost);
  }

  cutFlowManager->Print();
  histogramsHandler->SaveHistograms();
  return 0;
}