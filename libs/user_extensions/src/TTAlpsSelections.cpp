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
}

void TTAlpsSelections::RegisterSignalLikeSelections(shared_ptr<CutFlowManager> cutFlowManager) {
  cutFlowManager->RegisterCut("nLooseMuonsOrDSAMuons");
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
        if(asNanoEvent(event)->MuonIndexExist(allMuons, muon->Get("idx"), asNanoMuon(muon)->isDSAMuon())) {
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

void TTAlpsSelections::RegisterSingleLeptonSelections(shared_ptr<CutFlowManager> cutFlowManager) {
  cutFlowManager->RegisterCut("nAdditionalLooseMuons");
}

bool TTAlpsSelections::PassesSingleLeptonSelections(const shared_ptr<Event> event, shared_ptr<CutFlowManager> cutFlowManager) {
  int nLooseMuons = event->GetCollection("LooseMuons")->size();
  if (nLooseMuons > 1) return false;

  int nTightMuons = event->GetCollection("TightMuons")->size();
  if (nTightMuons != 1) return false;

  if (nLooseMuons == 1) {
    auto tightMuon = event->GetCollection("TightMuons")->at(0);
    auto looseMuon = event->GetCollection("LooseMuons")->at(0);
    if (looseMuon != tightMuon) return false;
  }
  if(cutFlowManager) cutFlowManager->UpdateCutFlow("nAdditionalLooseMuons");

  return true;
}

void TTAlpsSelections::RegisterTTZLikeSelections(shared_ptr<CutFlowManager> cutFlowManager) {
  cutFlowManager->RegisterCut("inZpeak");
}

bool TTAlpsSelections::PassesTTZLikeSelections(const shared_ptr<Event> event, shared_ptr<CutFlowManager> cutFlowManager) {
  auto looseMuons = event->GetCollection("LooseMuons");
  
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
