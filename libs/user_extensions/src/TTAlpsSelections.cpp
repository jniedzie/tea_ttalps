//  TTAlpsSelections.cpp
//
//  Created by Jeremi Niedziela on 16/08/2023.

#include "TTAlpsSelections.hpp"

#include "ExtensionsHelpers.hpp"
#include "TLorentzVector.h"

using namespace std;

TTAlpsSelections::TTAlpsSelections(){
  eventProcessor = make_unique<EventProcessor>();

  auto &config = ConfigManager::GetInstance();
  try {
    config.GetMap("muonMatchingParams", muonMatchingParams);
  } catch (const Exception &e) {
    warn() << "Couldn't read muonMatchingParams from config file - no muon matching methods will be applied to muon collections" << endl;
  }
  try {
    config.GetMap("muonVertexCollections", muonVertexCollections);
  } catch (const Exception &e) {
    info() << "Couldn't read muonVertexCollections from config file - no muon vertex collection selections can be made" << endl;
  }
}

void TTAlpsSelections::RegisterSignalLikeSelections(shared_ptr<CutFlowManager> cutFlowManager) {
  cutFlowManager->RegisterCut("nLooseMuonsOrDSAMuons");
}

void TTAlpsSelections::RegisterInitialDimuonCuts(shared_ptr<CutFlowManager> cutFlowManager) {
  for(auto &[collectionName, vertexCuts] : muonVertexCollections) {
    cutFlowManager->RegisterCollection(collectionName);
    cutFlowManager->RegisterCut("initial", collectionName);
  }
}

void TTAlpsSelections::RegisterDimuonSelections(shared_ptr<CutFlowManager> cutFlowManager) {
  for(auto &[collectionName, vertexCuts] : muonVertexCollections) {
    for (auto cutName : vertexCuts) {
      if(cutName == "BestDimuonVertex") continue;
      cutFlowManager->RegisterCut(cutName, collectionName);
    }
  }
}

bool TTAlpsSelections::PassesSignalLikeSelections(const shared_ptr<Event> event, shared_ptr<CutFlowManager> cutFlowManager) {
  if(muonMatchingParams.size() == 0){
    warn() << "No muon matching methods defined in config file - skipping muon matching" << endl;
    return false;
  }
  auto allMuons = make_shared<PhysicsObjects>();
  bool firstMatching = true;

  for(auto &[matchingMethod, param] : muonMatchingParams) {
    string collectionName = "LooseMuons" + matchingMethod + "Match";
    shared_ptr<PhysicsObjects> matchedMuons = event->GetCollection(collectionName);
    if(firstMatching) {
      allMuons = matchedMuons;
      firstMatching = false;
    }
    else {
      auto allMuons_new = make_shared<PhysicsObjects>();
      for(auto muon : *matchedMuons) {
        if(asNanoEvent(event)->MuonIndexExist(allMuons, muon->Get("idx"), asNanoMuon(muon)->isDSA())) {
          allMuons_new->push_back(muon);
        }
      }
      allMuons = allMuons_new;
    }
  }

  if(allMuons->size() < 3) return false;
  cutFlowManager->UpdateCutFlow("nLooseMuonsOrDSAMuons");

  return true;
}

bool TTAlpsSelections::PassesDimuonSelections(const shared_ptr<Event> event, shared_ptr<CutFlowManager> cutFlowManager) {
  bool passesSelections = true;
  for(auto &[collectionName, vertexCuts] : muonVertexCollections) {
    if(!PassesDimuonSelections(event, cutFlowManager, collectionName, vertexCuts)) passesSelections = false;
  }
  return passesSelections;
}

bool TTAlpsSelections::PassesDimuonSelections(const shared_ptr<Event> event, shared_ptr<CutFlowManager> cutFlowManager, string collectionName, vector<string> vertexCuts) {
  std::unique_ptr<TTAlpsDimuonSelections> ttAlpsDimuonSelections = make_unique<TTAlpsDimuonSelections>();

  shared_ptr<PhysicsObjects> dimuons = event->GetCollection("BaseDimuonVertices");
    
  cutFlowManager->UpdateCutFlow("initial", collectionName);

  auto baseDimuons = make_shared<PhysicsObjects>();
  for (const auto& dimuon : *dimuons) {
      baseDimuons->push_back(std::make_shared<PhysicsObject>(*dimuon));
  }
  // auto goodDimuons = make_shared<PhysicsObjects>();

  for(auto cutName : vertexCuts) {
    if(cutName == "BestDimuonVertex") continue;
    auto goodDimuons = make_shared<PhysicsObjects>();
    for (auto dimuon : *baseDimuons) {
      if(ttAlpsDimuonSelections->PassesCut(asNanoDimuonVertex(dimuon, event), cutName)) {
        goodDimuons->push_back(dimuon);
      }
    }
    if(goodDimuons->size() < 1) return false;
    cutFlowManager->UpdateCutFlow(cutName, collectionName);
    baseDimuons = make_shared<PhysicsObjects>();
    for (const auto& dimuon : *goodDimuons) {
      baseDimuons->push_back(dimuon);
    }
  }
  return true;
}

bool TTAlpsSelections::PassesSingleMuonTrigger(const shared_ptr<Event> event) {
  string triggerName = "HLT_IsoMu24";
  bool passes = false;
  try {
    passes = event->Get(triggerName);
  } catch (Exception &) {
    if (find(triggerWarningsPrinted.begin(), triggerWarningsPrinted.end(), triggerName) == triggerWarningsPrinted.end()) {
      warn() << "Trigger not present: " << triggerName << endl;
      triggerWarningsPrinted.push_back(triggerName);
    }
  }
  if(passes) return true;
  return passes;
}

bool TTAlpsSelections::PassesDoubleMuonTrigger(const shared_ptr<Event> event) {
  vector<string> triggerNames = {"HLT_DoubleL2Mu23NoVtx_2Cha","HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed"};
  bool passes = false;
  for (auto &triggerName : triggerNames) {
    passes = false;
    try {
      passes = event->Get(triggerName);
    } catch (Exception &) {
      if (find(triggerWarningsPrinted.begin(), triggerWarningsPrinted.end(), triggerName) == triggerWarningsPrinted.end()) {
        warn() << "Trigger not present: " << triggerName << endl;
        triggerWarningsPrinted.push_back(triggerName);
      }
    }
    if (passes) return true;
  }
  return passes;
}

void TTAlpsSelections::RegisterSingleLeptonSelections(shared_ptr<CutFlowManager> cutFlowManager) {
  cutFlowManager->RegisterCut("nAdditionalLooseMuons");
}

bool TTAlpsSelections::PassesSingleLeptonSelections(const shared_ptr<Event> event, shared_ptr<CutFlowManager> cutFlowManager) {
  int nLooseMuons = event->GetCollection("LooseIsoPATMuons")->size();
  if (nLooseMuons > 1) return false;

  int nTightMuons = event->GetCollection("TightMuons")->size();
  if (nTightMuons != 1) return false;

  if (nLooseMuons == 1) {
    auto tightMuon = event->GetCollection("TightMuons")->at(0);
    auto looseMuon = event->GetCollection("LooseIsoPATMuons")->at(0);
    if (looseMuon != tightMuon) return false;
  }
  if(cutFlowManager) cutFlowManager->UpdateCutFlow("nAdditionalLooseMuons");

  return true;
}

void TTAlpsSelections::RegisterTTZLikeSelections(shared_ptr<CutFlowManager> cutFlowManager) {
  cutFlowManager->RegisterCut("inZpeak");
}

bool TTAlpsSelections::PassesTTZLikeSelections(const shared_ptr<Event> event, shared_ptr<CutFlowManager> cutFlowManager) {
  auto looseMuons = event->GetCollection("LooseIsoPATMuons");
  
  double zMass = 91.1876; // GeV
  double smallestDifferenceToZmass = 999999;
  double maxDistanceFromZ = 30;

  for(int iMuon1=0; iMuon1 < looseMuons->size(); iMuon1++){
    auto muon1 = asNanoMuon(looseMuons->at(iMuon1))->GetFourVector();
    
    for(int iMuon2=iMuon1+1; iMuon2 < looseMuons->size(); iMuon2++){
      auto muon2 = asNanoMuon(looseMuons->at(iMuon2))->GetFourVector();
      double diMuonMass = (muon1 + muon2).M();

      if(fabs(diMuonMass-zMass) < smallestDifferenceToZmass){
        smallestDifferenceToZmass = fabs(diMuonMass-zMass);
      }
    }
    if(smallestDifferenceToZmass < maxDistanceFromZ) break;
  }
  if(smallestDifferenceToZmass > maxDistanceFromZ) return false;
  if(cutFlowManager) cutFlowManager->UpdateCutFlow("inZpeak");

  return true;
}

bool TTAlpsSelections::PassesDileptonSelections(const shared_ptr<Event> event) {
  int muonsPt30 = 0;
  int electronsPt30;
  int jetsBtagged = 0;

  uint nMuons = event->Get("nMuon");
  auto muons = event->GetCollection("Muon");
  for (int i = 0; i < nMuons; i++) {
    float muonPt = muons->at(i)->Get("pt");
    float muonEta = muons->at(i)->Get("eta");
    if (muonPt > 30 && abs(muonEta) < 2.4) muonsPt30++;
  }
  uint nElectrons = event->Get("nElectron");
  auto electrons = event->GetCollection("Electron");
  for (int i = 0; i < nElectrons; i++) {
    float electronPt = electrons->at(i)->Get("pt");
    float electronEta = electrons->at(i)->Get("eta");
    if (electronPt > 30 && abs(electronEta) < 2.4) electronsPt30++;
  }
  uint nJets = event->Get("nJet");
  auto jets = event->GetCollection("Jet");
  for (int i = 0; i < nJets; i++) {
    float jetPt = jets->at(i)->Get("pt");
    float jet_eta = jets->at(i)->Get("eta");
    float jet_btagDeepB = jets->at(i)->Get("btagDeepB");
    if (jetPt > 30 && abs(jet_eta) < 2.4 && jet_btagDeepB > 0.5) jetsBtagged++;
  }

  if ((muonsPt30 + electronsPt30) < 2) return false;
  float metPt = event->Get("MET_pt");
  if (metPt <= 30) return false;
  if (jetsBtagged < 2) return false;
  return true;
}

bool TTAlpsSelections::PassesHadronSelections(const shared_ptr<Event> event) {
  int jetsBtagged = 0;
  int jetsPt30;

  uint nJets = event->Get("nJet");
  auto jets = event->GetCollection("Jet");
  for (int i = 0; i < nJets; i++) {
    float jetPt = jets->at(i)->Get("pt");
    float jetEta = jets->at(i)->Get("eta");
    float jetBtagDeepB = jets->at(i)->Get("btagDeepB");
    if (jetPt > 30 && abs(jetEta) < 2.4) {
      jetsPt30++;
      if (jetBtagDeepB > 0.5) jetsBtagged++;
    }
  }

  if (jetsBtagged < 2) return false;
  if (jetsPt30 < 6) return false;
  return true;
}

void TTAlpsSelections::PrintDimuonCutFlow(shared_ptr<CutFlowManager> cutFlowManager) {
  info() << "Dimuon cut flow for all muonVertexCollections" << endl;
  for(auto &[collectionName, vertexCuts] : muonVertexCollections) {
    info() << "CutFlow for dimuon collection " << collectionName << endl;
    cutFlowManager->Print(collectionName);
  }
}
    