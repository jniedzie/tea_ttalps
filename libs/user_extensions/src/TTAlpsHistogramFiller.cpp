#include "TTAlpsHistogramFiller.hpp"

#include "ConfigManager.hpp"
#include "ExtensionsHelpers.hpp"
#include "UserExtensionsHelpers.hpp"
#include "TTAlpsSelections.hpp"

using namespace std;

TTAlpsHistogramFiller::TTAlpsHistogramFiller(shared_ptr<HistogramsHandler> histogramsHandler_) : histogramsHandler(histogramsHandler_) {
  eventProcessor = make_unique<EventProcessor>();
  nanoEventProcessor = make_unique<NanoEventProcessor>();
  auto &config = ConfigManager::GetInstance();

  try {
    config.GetMap("triggerSets", triggerSets);
    for (auto it = triggerSets.begin(); it != triggerSets.end(); ++it) triggerNames.push_back(it->first);
  } catch (const Exception &e) {
    warn() << "Couldn't read triggerSets from config file ";
    warn() << "(which may be fine if you're not trying to apply trigger selection)" << endl;
  }

  try {
    config.GetHistogramsParams(defaultHistVariables, "defaultHistParams");
  } catch (const Exception &e) {
    warn() << "Couldn't read defaultHistParams from config file - no default histograms will be included" << endl;
  }
  try {
    config.GetHistogramsParams(ttalpsHistVariables, "histParams");
  } catch (const Exception &e) {
    warn() << "Couldn't read histParams from config file - no custom ttalps histograms will be included" << endl;
  }
}

TTAlpsHistogramFiller::~TTAlpsHistogramFiller() {}

float TTAlpsHistogramFiller::GetEventWeight(const shared_ptr<Event> event) {

  auto nanoEvent = asNanoEvent(event);

  float genWeight = nanoEventProcessor->GetGenWeight(nanoEvent);
  // change to "pileup" to use jsonPOG LUM values, or "custom" to use our own pileup distribution
  float pileupSF = nanoEventProcessor->GetPileupScaleFactor(nanoEvent, "custom"); 
  float muonTriggerSF = nanoEventProcessor->GetMuonTriggerScaleFactor(nanoEvent, "muonTriggerIsoMu24");

  return genWeight * pileupSF * muonTriggerSF;
}

bool TTAlpsHistogramFiller::EndsWithTriggerName(string name) {
  string lastPart = name.substr(name.rfind("_") + 1);
  return find(triggerNames.begin(), triggerNames.end(), lastPart) != triggerNames.end();
}

float TTAlpsHistogramFiller::GetObjectWeight(const shared_ptr<PhysicsObject> object, string collectionName) {
  float weight = 1.0;
  if (collectionName == "TightMuons") {
    weight *= asNanoMuon(object)->GetScaleFactor("muonIDTight", "muonIsoTight", "muonReco");
  } else if (collectionName == "LooseMuons") {
    weight *= asNanoMuon(object)->GetScaleFactor("muonIDLoose", "muonIsoLoose", "muonReco");
  } else if (collectionName == "GoodTightBtaggedJets") {
    weight *= asNanoJet(object)->GetBtaggingScaleFactor("bTaggingTight");
  } else if (collectionName == "GoodMediumBtaggedJets") {
    weight *= asNanoJet(object)->GetBtaggingScaleFactor("bTaggingMedium");
  } else if (collectionName == "LooseMuonsDRMatch" || collectionName == "LooseMuonsOuterDRMatch" || collectionName == "LooseMuonsSegmentMatch") {
    weight *= asNanoMuon(object)->GetScaleFactor("muonIDLoose", "muonIsoLoose", "muonReco");
  }
  return weight;
}

void TTAlpsHistogramFiller::FillDefaultVariables(const shared_ptr<Event> event) {
  float eventWeight = GetEventWeight(event);
  
  for (auto &[title, params] : defaultHistVariables) {
    string collectionName = params.collection;
    string branchName = params.variable;

    float value;
    

    if (collectionName == "Event") {
      if (branchName[0] == 'n') {
        auto collection = event->GetCollection(branchName.substr(1));
        value = collection->size();
      } else {
        value = event->GetAsFloat(branchName);
      }
      histogramsHandler->Fill(title, value, eventWeight);
    } else {
      auto collection = event->GetCollection(collectionName);
      for (auto object : *collection) {
        value = object->GetAsFloat(branchName);
        float objectWeight = GetObjectWeight(object, collectionName);
        histogramsHandler->Fill(title, value, eventWeight * objectWeight);
      }
    }
  }
}

void TTAlpsHistogramFiller::FillTriggerEfficiencies() {
  TH1D *hist_tmp;

  for (auto &[name, hist] : histogramsHandler->GetHistograms1D()) {
    if (!EndsWithTriggerName(name)) continue;
    string nameWithoutTrigger = name.substr(0, name.rfind("_"));
    string newName = name + "_eff";
    hist_tmp = (TH1D *)histogramsHandler->GetHistogram1D(name)->Clone(newName.c_str());
    hist_tmp->Divide(hist_tmp, histogramsHandler->GetHistogram1D(nameWithoutTrigger), 1, 1, "B");
    histogramsHandler->SetHistogram1D(newName, hist_tmp);
  }
}

void TTAlpsHistogramFiller::FillTriggerVariables(const shared_ptr<Event> event, string prefix, string suffix) {
  if (prefix != "") prefix = prefix + "_";
  if (suffix != "") suffix = "_" + suffix;

  auto nanoEvent = asNanoEvent(event);

  float weight = nanoEventProcessor->GetGenWeight(nanoEvent);

  histogramsHandler->Fill(prefix + "muonMaxPt" + suffix, eventProcessor->GetMaxPt(event, "Muon"), weight);
  histogramsHandler->Fill(prefix + "eleMaxPt" + suffix, eventProcessor->GetMaxPt(event, "Electron"), weight);
  histogramsHandler->Fill(prefix + "jetMaxPt" + suffix, eventProcessor->GetMaxPt(event, "Jet"), weight);
  histogramsHandler->Fill(prefix + "jetHt" + suffix, eventProcessor->GetHt(event, "Jet"), weight);
}

void TTAlpsHistogramFiller::FillTriggerVariablesPerTriggerSet(const shared_ptr<Event> event, string ttbarCategory) {
  auto ttAlpsSelections = make_unique<TTAlpsSelections>();

  bool passesSingleLepton = ttAlpsSelections->PassesSingleLeptonSelections(event);
  bool passesDilepton = ttAlpsSelections->PassesDileptonSelections(event);
  bool passesHadron = ttAlpsSelections->PassesHadronSelections(event);

  for (auto &[triggerSetName, triggerSet] : triggerSets) {
    bool passesTrigger = false;

    for (auto &triggerName : triggerSet) {
      passesTrigger = event->Get(triggerName);
      if (passesTrigger) break;
    }
    if (!passesTrigger) continue;

    FillTriggerVariables(event, ttbarCategory, triggerSetName);
    if (passesSingleLepton) FillTriggerVariables(event, ttbarCategory, triggerSetName + "_singleLepton");
    if (passesDilepton) FillTriggerVariables(event, ttbarCategory, triggerSetName + "_dilepton");
    if (passesHadron) FillTriggerVariables(event, ttbarCategory, triggerSetName + "_hadron");
  }
}

void TTAlpsHistogramFiller::FillNormCheck(const shared_ptr<Event> event) {
  float weight = nanoEventProcessor->GetGenWeight(asNanoEvent(event));
  histogramsHandler->Fill("Event_normCheck", 0.5, weight);
}

void TTAlpsHistogramFiller::FillLeadingPt(const shared_ptr<Event> event, string histName, const HistogramParams &params) {
  auto maxPtObject = eventProcessor->GetMaxPtObject(event, params.collection);
  if (!maxPtObject) return;

  float weight = GetEventWeight(event);
  weight *= GetObjectWeight(maxPtObject, params.collection);
  histogramsHandler->Fill(histName, maxPtObject->Get("pt"), weight);
}

void TTAlpsHistogramFiller::FillAllSubLeadingPt(const shared_ptr<Event> event, string histName, const HistogramParams &params) {
  float maxPt = eventProcessor->GetMaxPt(event, params.collection);

  auto collection = event->GetCollection(params.collection);
  float weight = GetEventWeight(event);

  for (auto object : *collection) {
    float pt = object->Get("pt");
    if (pt == maxPt) continue;
    histogramsHandler->Fill(histName, pt, weight * GetObjectWeight(object, params.collection));
  }
}

void TTAlpsHistogramFiller::FillDimuonHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);
  string collectionName = "LooseMuons";

  auto looseMuons = event->GetCollection(collectionName);
  for (int iMuon1 = 0; iMuon1 < looseMuons->size(); iMuon1++) {
    auto obj1 = looseMuons->at(iMuon1);
    auto muon1 = asNanoMuon(obj1);
    float muon1SF = GetObjectWeight(obj1, collectionName);
    TLorentzVector muon1vector = muon1->GetFourVector();

    for (int iMuon2 = iMuon1 + 1; iMuon2 < looseMuons->size(); iMuon2++) {
      auto obj2 = looseMuons->at(iMuon2);
      auto muon2 = asNanoMuon(obj2);
      float muon2SF = GetObjectWeight(obj2, collectionName);
      TLorentzVector muon2vector = muon2->GetFourVector();
      histogramsHandler->Fill("LooseMuons_dimuonMinv", (muon1vector + muon2vector).M(), weight * muon1SF * muon2SF);
    }
  }
}

void TTAlpsHistogramFiller::FillDiumonClosestToZhistgrams(const shared_ptr<Event> event) {
  auto looseMuons = event->GetCollection("LooseMuons");
  if (looseMuons->size() < 2) {
    warn() << "Not enough muons in event to fill dimuon histograms" << endl;
    return;
  }

  string collectionName = "LooseMuons";

  float weight = GetEventWeight(event);
  auto [muon1, muon2] = nanoEventProcessor->GetMuonPairClosestToZ(asNanoEvent(event), collectionName);

  TLorentzVector muon1fourVector = muon1->GetFourVector();
  TLorentzVector muon2fourVector = muon2->GetFourVector();

  float massClosestToZ = (muon1fourVector + muon2fourVector).M();
  float deltaRclosestToZ = muon1fourVector.DeltaR(muon2fourVector);
  float deltaEtaclosestToZ = fabs(muon1fourVector.Eta() - muon2fourVector.Eta());
  float deltaPhiclosestToZ = muon1fourVector.DeltaPhi(muon2fourVector);
  float muon1SF = GetObjectWeight(muon1->GetPhysicsObject(), collectionName);
  float muon2SF = GetObjectWeight(muon2->GetPhysicsObject(), collectionName);

  histogramsHandler->Fill(collectionName + "_dimuonMinvClosestToZ", massClosestToZ, weight * muon1SF * muon2SF);
  histogramsHandler->Fill(collectionName + "_dimuonDeltaRclosestToZ", deltaRclosestToZ, weight * muon1SF * muon2SF);
  histogramsHandler->Fill(collectionName + "_dimuonDeltaEtaclosestToZ", deltaEtaclosestToZ, weight * muon1SF * muon2SF);
  histogramsHandler->Fill(collectionName + "_dimuonDeltaPhiclosestToZ", deltaPhiclosestToZ, weight * muon1SF * muon2SF);
}

void TTAlpsHistogramFiller::FillMuonMetHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  string collectionName = "TightMuons";
  if(event->GetCollection(collectionName)->size() > 0) {
    auto leadingMuonObj = eventProcessor->GetMaxPtObject(event, collectionName);

    auto leadingTightMuon = asNanoMuon(leadingMuonObj);
    float leadingMuonSF = GetObjectWeight(leadingMuonObj, collectionName);

    TLorentzVector leadingMuonVector = leadingTightMuon->GetFourVector();
    TLorentzVector metVector = asNanoEvent(event)->GetMetFourVector();

    histogramsHandler->Fill(collectionName + "_deltaPhiMuonMET", metVector.DeltaPhi(leadingMuonVector), weight * leadingMuonSF);
    histogramsHandler->Fill(collectionName + "_minvMuonMET", (leadingMuonVector + metVector).M(), weight * leadingMuonSF);
  }
}

void TTAlpsHistogramFiller::FillJetHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);
  auto bJets = event->GetCollection("GoodTightBtaggedJets");
  auto jets = event->GetCollection("GoodNonTightBtaggedJets");

  for (auto bJet : *bJets) {
    TLorentzVector bJetVector = asNanoJet(bJet)->GetFourVector();
    float bjetWeight = GetObjectWeight(bJet, "GoodTightBtaggedJets");

    for (int iJet = 0; iJet < jets->size(); iJet++) {
      TLorentzVector jet1vector = asNanoJet(jets->at(iJet))->GetFourVector();

      for (int jJet = iJet + 1; jJet < jets->size(); jJet++) {
        TLorentzVector jet2vector = asNanoJet(jets->at(jJet))->GetFourVector();
        histogramsHandler->Fill("GoodJets_minvBjet2jets", (bJetVector + jet1vector + jet2vector).M(), weight * bjetWeight);
      }
    }
  }
}

void TTAlpsHistogramFiller::FillLooseMuonsHistograms(const shared_ptr<Collection<shared_ptr<PhysicsObject> >> objectCollection, string collectionName, float weight) {
  histogramsHandler->Fill("Event_n"+collectionName, objectCollection->size(), weight);

  for(auto object : *objectCollection){
    float muonWeight = GetObjectWeight(object, collectionName);
    histogramsHandler->Fill(collectionName+"_pt", object->Get("pt"), weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_eta", object->Get("eta"), weight * muonWeight);

    try {
      histogramsHandler->Fill(collectionName+"_dxy", object->Get("dxy"), weight * muonWeight);
      histogramsHandler->Fill(collectionName+"_dz", object->Get("dz"), weight * muonWeight);
    } catch (const Exception &e) {
      try {
        histogramsHandler->Fill(collectionName+"_dxy", object->Get("dxyPV"), weight * muonWeight);
        histogramsHandler->Fill(collectionName+"_dz", object->Get("dzPV"), weight * muonWeight);
      } catch (const Exception &e) {
        warn() << "dxy, dxyPV, dz and dzPV couldn't be found for muon." << endl;
      }
    }
  }
}

void TTAlpsHistogramFiller::FillMuonVertexHistograms(const shared_ptr<Event> event, const shared_ptr<Collection<shared_ptr<PhysicsObject> >> vertexCollection, string vertexName) {
  float weight = GetEventWeight(event);
  
  histogramsHandler->Fill("Event_n"+vertexName, vertexCollection->size(), weight);

  for(auto vertex : *vertexCollection){
    pair<shared_ptr<PhysicsObject>,shared_ptr<PhysicsObject>> muons = asNanoEvent(event)->GetLooseMuonsInVertex(vertex);
    float muonWeight1 = GetObjectWeight(muons.first, "LooseMuons");
    float muonWeight2 = GetObjectWeight(muons.second, "LooseMuons");
    
    histogramsHandler->Fill(vertexName+"_chi2", vertex->Get("chi2"), weight);
    histogramsHandler->Fill(vertexName+"_vxy", vertex->Get("vxy"), weight);
    histogramsHandler->Fill(vertexName+"_vxySigma", vertex->Get("vxySigma"), weight);
    // float vxyz = sqrt(float(vertex->Get("vx"))*float(vertex->Get("vx")) + float(vertex->Get("vy"))*float(vertex->Get("vy")) + float(vertex->Get("vz"))*float(vertex->Get("vz")));
    // histogramsHandler->Fill(vertexName+"_vxyz", vxyz, weight);
    histogramsHandler->Fill(vertexName+"_vz", vertex->Get("vz"), weight);
    histogramsHandler->Fill(vertexName+"_dR", vertex->Get("dR"), weight);
    histogramsHandler->Fill(vertexName+"_idx1", vertex->Get("idx1"), weight);
    histogramsHandler->Fill(vertexName+"_idx2", vertex->Get("idx2"), weight);
    histogramsHandler->Fill(vertexName+"_isDSAMuon1", vertex->Get("isDSAMuon1"), weight);
    histogramsHandler->Fill(vertexName+"_isDSAMuon2", vertex->Get("isDSAMuon2"), weight);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso03Dimuon1", vertex->Get("displacedTrackIso03Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso04Dimuon1", vertex->Get("displacedTrackIso04Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso03Dimuon2", vertex->Get("displacedTrackIso03Dimuon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso04Dimuon2", vertex->Get("displacedTrackIso04Dimuon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso03Muon1", vertex->Get("displacedTrackIso03Muon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso04Muon1", vertex->Get("displacedTrackIso04Muon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso03Muon2", vertex->Get("displacedTrackIso03Muon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso04Muon2", vertex->Get("displacedTrackIso04Muon2"), weight * muonWeight1 * muonWeight2);
  }
}

void TTAlpsHistogramFiller::FillHasMatchHistograms(const shared_ptr<Collection<shared_ptr<PhysicsObject> >> muonCollectionRef, const shared_ptr<Collection<shared_ptr<PhysicsObject> >> muonCollectionCheck, string branchName, float weight) {

  for(auto muonRef : *muonCollectionRef) {
    float muonRef_idx = muonRef->Get("idx");
    int indexFound = 0;
    for(auto muonCheck : *muonCollectionCheck) {
      float muonCheck_idx = muonCheck->Get("idx");
      if(muonRef_idx == muonCheck_idx) {
        indexFound = 1;
        break;
      }
    }
    float muonWeight = GetObjectWeight(muonRef, "LooseMuons");
    histogramsHandler->Fill(branchName, indexFound, weight * muonWeight);
  }
}

void TTAlpsHistogramFiller::FillAllLooseMuonsHistograms(const shared_ptr<Event> event){
  float weight = GetEventWeight(event);

  auto looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons(0.01);
  auto looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons(0.01);
  auto looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons();

  FillLooseMuonsHistograms(looseMuonsDRMatch,"LooseMuonsDRMatch",weight);
  FillLooseMuonsHistograms(looseMuonsOuterDRMatch,"LooseMuonsOuterDRMatch",weight);
  FillLooseMuonsHistograms(looseMuonsSegmentMatch,"LooseMuonsSegmentMatch",weight);

  auto looseMuonsVertexDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsDRMatch);
  auto looseMuonsVertexOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsOuterDRMatch);
  auto looseMuonsVertexSegmentMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentMatch);
  FillMuonVertexHistograms(event,looseMuonsVertexDRMatch,"LooseMuonsVertexDRMatch");
  FillMuonVertexHistograms(event,looseMuonsVertexOuterDRMatch,"LooseMuonsVertexOuterDRMatch");
  FillMuonVertexHistograms(event,looseMuonsVertexSegmentMatch,"LooseMuonsVertexSegmentMatch");

  FillHasMatchHistograms(looseMuonsDRMatch, looseMuonsOuterDRMatch, "LooseMuonsDRMatch_hasOuterDRMatch", weight);
  FillHasMatchHistograms(looseMuonsDRMatch, looseMuonsSegmentMatch, "LooseMuonsDRMatch_hasSegmentMatch", weight);
  FillHasMatchHistograms(looseMuonsOuterDRMatch, looseMuonsDRMatch, "LooseMuonsOuterDRMatch_hasDRMatch", weight);
  FillHasMatchHistograms(looseMuonsOuterDRMatch, looseMuonsSegmentMatch, "LooseMuonsOuterDRMatch_hasSegmentMatch", weight);
  FillHasMatchHistograms(looseMuonsSegmentMatch, looseMuonsDRMatch, "LooseMuonsSegmentMatch_hasDRMatch", weight);
  FillHasMatchHistograms(looseMuonsSegmentMatch, looseMuonsOuterDRMatch, "LooseMuonsSegmentMatch_hasOuterDRMatch", weight);

  auto looseMuonsSegmentDRMatch = make_shared<PhysicsObjects>();
  for(auto muon : *looseMuonsSegmentMatch){
    float muon_idx = muon->Get("idx");
    if(asNanoEvent(event)->IndexExist(looseMuonsDRMatch,muon_idx,asNanoMuon(muon)->isDSAMuon())) {
      looseMuonsSegmentDRMatch->push_back(muon);
    }
  }
  FillLooseMuonsHistograms(looseMuonsSegmentDRMatch,"LooseMuonsSegmentDRMatch",weight);
  auto looseMuonsVertexSegmentDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentDRMatch);
  FillMuonVertexHistograms(event,looseMuonsVertexSegmentDRMatch,"LooseMuonsVertexSegmentDRMatch");
  FillHasMatchHistograms(looseMuonsSegmentDRMatch, looseMuonsDRMatch,      "LooseMuonsSegmentDRMatch_hasDRMatch", weight);
  FillHasMatchHistograms(looseMuonsSegmentDRMatch, looseMuonsOuterDRMatch, "LooseMuonsSegmentDRMatch_hasOuterDRMatch", weight);
  FillHasMatchHistograms(looseMuonsSegmentDRMatch, looseMuonsSegmentMatch, "LooseMuonsSegmentDRMatch_hasSegmentMatch", weight);
  auto looseMuonsSegmentOuterDRMatch = make_shared<PhysicsObjects>();
  for(auto muon : *looseMuonsSegmentMatch){
    float muon_idx = muon->Get("idx");
    if(asNanoEvent(event)->IndexExist(looseMuonsOuterDRMatch,muon_idx,asNanoMuon(muon)->isDSAMuon())) {
      looseMuonsSegmentOuterDRMatch->push_back(muon);
    }
  }
  FillLooseMuonsHistograms(looseMuonsSegmentOuterDRMatch,"LooseMuonsSegmentOuterDRMatch",weight);
  auto looseMuonsVertexSegmentOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentOuterDRMatch);
  FillMuonVertexHistograms(event,looseMuonsVertexSegmentOuterDRMatch,"LooseMuonsVertexSegmentOuterDRMatch");
  FillHasMatchHistograms(looseMuonsSegmentOuterDRMatch, looseMuonsDRMatch,      "LooseMuonsSegmentOuterDRMatch_hasDRMatch", weight);
  FillHasMatchHistograms(looseMuonsSegmentOuterDRMatch, looseMuonsOuterDRMatch, "LooseMuonsSegmentOuterDRMatch_hasOuterDRMatch", weight);
  FillHasMatchHistograms(looseMuonsSegmentOuterDRMatch, looseMuonsSegmentMatch, "LooseMuonsSegmentOuterDRMatch_hasSegmentMatch", weight);
}

void TTAlpsHistogramFiller::FillCustomTTAlpsVariables(const shared_ptr<Event> event) {
  for (auto &[histName, params] : ttalpsHistVariables) {
    if (params.variable == "subleadingPt") {
      FillAllSubLeadingPt(event, histName, params);
    } else if (params.variable == "leadingPt") {
      FillLeadingPt(event, histName, params);
    }
  }
  FillDimuonHistograms(event);
  FillDiumonClosestToZhistgrams(event);
  FillMuonMetHistograms(event);
  FillJetHistograms(event);
}

void TTAlpsHistogramFiller::FillCustomTTAlpsVariablesFromLLPNanoAOD(const shared_ptr<Event> event) {
  FillAllLooseMuonsHistograms(event);
  FillGenMuonsFromALPs(event);
  FillLooseMuonsFromALPs(event);
  FillGenALPs(event);
}

void TTAlpsHistogramFiller::FillGenALPs(const std::shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  auto pv_x = event->GetAsFloat("PV_x");
  auto pv_y = event->GetAsFloat("PV_y");

  auto ttalpsEvent = asTTAlpsEvent(event);
  auto genALPs = ttalpsEvent->GetGenALPs();

  histogramsHandler->Fill("Event_nGenALP", genALPs->size(), weight);

  for (int i=0; i<genALPs->size(); i++)
  {    
    auto genALP = genALPs->at(i);
    int pdgId = genALP->Get("pdgId");
    auto ALPfourvector = asNanoGenParticle(genALP)->GetFourVector();
    histogramsHandler->Fill("GenALP_pdgId", pdgId,                weight);
    histogramsHandler->Fill("GenALP_pt",    genALP->Get("pt"),    weight);
    histogramsHandler->Fill("GenALP_mass",  genALP->Get("mass"),  weight);
    histogramsHandler->Fill("GenALP_massT", ALPfourvector.Mt(),   weight);
    histogramsHandler->Fill("GenALP_eta",   genALP->Get("eta"),   weight);
    histogramsHandler->Fill("GenALP_phi",   genALP->Get("phi"),   weight);
    float vx = genALP->Get("vx");
    float vy = genALP->Get("vy");
    float vz = genALP->Get("vz");
    float vxy = sqrt(vx*vx + vy*vy);
    float vxyz = sqrt(vx*vx + vy*vy + vz*vz);
    histogramsHandler->Fill("GenALP_vx",    vx,                    weight);
    histogramsHandler->Fill("GenALP_vy",    vy,                    weight);
    histogramsHandler->Fill("GenALP_vz",    genALP->Get("vz"),     weight);
    histogramsHandler->Fill("GenALP_vxy",   vxy,                   weight);
    histogramsHandler->Fill("GenALP_vxyz",  vxyz,                  weight);
    float boost_pT = float(genALP->Get("pt")) / float(genALP->Get("mass"));
    float boost_p = ALPfourvector.P() / float(genALP->Get("mass"));
    float boost_T = float(genALP->Get("pt")) / ALPfourvector.Mt();
    histogramsHandler->Fill("GenALP_boost_pT", boost_pT,           weight);
    histogramsHandler->Fill("GenALP_boost_p",  boost_p,            weight);
    histogramsHandler->Fill("GenALP_boost_T",  boost_T,            weight);

    float dxy = asNanoGenParticle(genALP)->GetDxy(pv_x, pv_y);
    histogramsHandler->Fill("GenALP_dxy", dxy,         weight);
  }
}

void TTAlpsHistogramFiller::FillGenMuonsFromALPs(const std::shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  auto pv_x = event->GetAsFloat("PV_x");
  auto pv_y = event->GetAsFloat("PV_y");

  auto genMuonsFromALP = asTTAlpsEvent(event)->GetGenMuonsFromALP();
  auto genParticles = event->GetCollection("GenPart");

  histogramsHandler->Fill("Event_nGenMuonFromALP", genMuonsFromALP->size(), weight);

  int nGenDimuons = 0;

  for (int i=0; i<genMuonsFromALP->size(); i++)
  {    
    auto genMuon = genMuonsFromALP->at(i);
    TLorentzVector genMuon1fourVector = asNanoGenParticle(genMuon)->GetFourVector();

    int pdgId = genMuon->Get("pdgId");
    histogramsHandler->Fill("GenMuonFromALP_pdgId", pdgId,                 weight);
    histogramsHandler->Fill("GenMuonFromALP_pt",    genMuon->Get("pt"),    weight);
    histogramsHandler->Fill("GenMuonFromALP_mass",  genMuon->Get("mass"),  weight);
    histogramsHandler->Fill("GenMuonFromALP_eta",   genMuon->Get("eta"),   weight);
    histogramsHandler->Fill("GenMuonFromALP_phi",   genMuon->Get("phi"),   weight);
    float vx = genMuon->Get("vx");
    float vy = genMuon->Get("vy");
    float vz = genMuon->Get("vz");
    float vxy = sqrt(vx*vx + vy*vy);
    float vxyz = sqrt(vx*vx + vy*vy + vz*vz);
    histogramsHandler->Fill("GenMuonFromALP_vx",    vx,                    weight);
    histogramsHandler->Fill("GenMuonFromALP_vy",    vy,                    weight);
    histogramsHandler->Fill("GenMuonFromALP_vz",    vz,                    weight);
    histogramsHandler->Fill("GenMuonFromALP_vxy",   vxy,                   weight);
    histogramsHandler->Fill("GenMuonFromALP_vxyz",  vxyz,                  weight);
    float boost = float(genMuon->Get("pt")) / float(genMuon->Get("mass"));
    histogramsHandler->Fill("GenMuonFromALP_boost", boost,         weight);

    float dxy = asNanoGenParticle(genMuon)->GetDxy(pv_x, pv_y);
    histogramsHandler->Fill("GenMuonFromALP_dxy", dxy,         weight);

    for (int j = i+1; j<genMuonsFromALP->size(); j++)
    {
      if(j==i) continue;
      auto genMuon2 = genMuonsFromALP->at(j);
      TLorentzVector genMuon2fourVector = asNanoGenParticle(genMuon2)->GetFourVector();

      histogramsHandler->Fill("GenDimuonFromALP_invMass", (genMuon1fourVector+genMuon2fourVector).M(), weight);
      histogramsHandler->Fill("GenDimuonFromALP_DR", genMuon1fourVector.DeltaR(genMuon2fourVector), weight);
      histogramsHandler->Fill("GenDimuonFromALP_Dphi", genMuon1fourVector.DeltaPhi(genMuon2fourVector), weight);
      nGenDimuons++;

      if((genMuon1fourVector+genMuon2fourVector).M() < 0.28) {
        int pdgId2 = genMuon2->Get("pdgId");
        histogramsHandler->Fill("GenDimuonFromALP_pdgId", pdgId2,                 weight);
        histogramsHandler->Fill("GenDimuonFromALP_pt",    genMuon2->Get("pt"),    weight);
        histogramsHandler->Fill("GenDimuonFromALP_mass",  genMuon2->Get("mass"),  weight);
        histogramsHandler->Fill("GenDimuonFromALP_eta",   genMuon2->Get("eta"),   weight);
        histogramsHandler->Fill("GenDimuonFromALP_phi",   genMuon2->Get("phi"),   weight);
      }
    }
    int motherIndex = asNanoGenParticle(genMuon)->GetMotherIndex();
    if(motherIndex<0) continue;
    auto genALP = asNanoGenParticle(genParticles->at(motherIndex));
    auto ALPfourvector = genALP->GetFourVector();
    float ALPboost_pT = float(genALP->GetPt()) / float(genALP->GetMass());
    float ALPboost_p = ALPfourvector.P() / float(genALP->GetMass());
    float ALPboost_T = float(genALP->GetPt()) / ALPfourvector.Mt();
    histogramsHandler->Fill("GenMuonFromALP_vxyALPboostpT", vxy/ALPboost_pT, weight);
    histogramsHandler->Fill("GenMuonFromALP_vxyALPboostT", vxy/ALPboost_T, weight);
    histogramsHandler->Fill("GenMuonFromALP_vxyzALPboostp", vxyz/ALPboost_p, weight);
  }
  histogramsHandler->Fill("Event_nGenDimuonFromALP", nGenDimuons, weight);
}

void TTAlpsHistogramFiller::FillLooseMuonsFromALPs(const std::shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  auto genMuonsFromALP = asTTAlpsEvent(event)->GetGenMuonsFromALP();

  auto looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons(0.01);
  auto looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons(0.01);
  auto looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons();

  for ( auto genMuon : *genMuonsFromALP ) {
    TLorentzVector genMuonFourVector = asNanoGenParticle(genMuon)->GetFourVector();
    float deltaRmin = 9999.;
    for ( auto looseMuon : *looseMuonsDRMatch ) {
      TLorentzVector looseMuonFourVector = asNanoMuon(looseMuon)->GetFourVector();
      if(genMuonFourVector.DeltaR(looseMuonFourVector) < deltaRmin) deltaRmin = genMuonFourVector.DeltaR(looseMuonFourVector);
    }
    if(deltaRmin < 9999.) histogramsHandler->Fill("GenMuonFromALP_looseMuonsDRMatchMinDR", deltaRmin, weight);
    deltaRmin = 9999.;
    for ( auto looseMuon : *looseMuonsOuterDRMatch ) {
      TLorentzVector looseMuonFourVector = asNanoMuon(looseMuon)->GetFourVector();
      if(genMuonFourVector.DeltaR(looseMuonFourVector) < deltaRmin) deltaRmin = genMuonFourVector.DeltaR(looseMuonFourVector);
    }
    if(deltaRmin < 9999.) histogramsHandler->Fill("GenMuonFromALP_looseMuonsOuterDRMatchMinDR", deltaRmin, weight);
    deltaRmin = 9999.;
    for ( auto looseMuon : *looseMuonsSegmentMatch ) {
      TLorentzVector looseMuonFourVector = asNanoMuon(looseMuon)->GetFourVector();
      if(genMuonFourVector.DeltaR(looseMuonFourVector) < deltaRmin) deltaRmin = genMuonFourVector.DeltaR(looseMuonFourVector);
    }
    if(deltaRmin < 9999.) histogramsHandler->Fill("GenMuonFromALP_looseMuonsSegmentMatchMinDR", deltaRmin, weight);
  }

  auto ttalpsEvent = asTTAlpsEvent(event);
  // auto muonsFromALPDRMatch = ttalpsEvent->GetMuonsFromALP(looseMuonsDRMatch);
  // auto muonsFromALPOuterDRMatch = ttalpsEvent->GetMuonsFromALP(looseMuonsOuterDRMatch);
  auto muonsFromALPSegmentMatch0p2 = ttalpsEvent->GetMuonsFromALP(looseMuonsSegmentMatch, 0.2);
  auto muonsFromALPSegmentMatch0p5 = ttalpsEvent->GetMuonsFromALP(looseMuonsSegmentMatch, 0.5);
  // FillLooseMuonsHistograms(muonsFromALPDRMatch,"LooseMuonsFromALPDRMatch",weight);
  // FillLooseMuonsHistograms(muonsFromALPOuterDRMatch,"LooseMuonsFromALPOuterDRMatch",weight);
  FillLooseMuonsHistograms(muonsFromALPSegmentMatch0p2,"LooseMuonsFromALPSegmentMatch0p2",weight);
  FillLooseMuonsHistograms(muonsFromALPSegmentMatch0p5,"LooseMuonsFromALPSegmentMatch0p5",weight);

  if(muonsFromALPSegmentMatch0p2->size() > 1) {
    TLorentzVector muon1fourVector = asNanoGenParticle(muonsFromALPSegmentMatch0p2->at(0))->GetFourVector();
    TLorentzVector muon2fourVector = asNanoGenParticle(muonsFromALPSegmentMatch0p2->at(1))->GetFourVector();
    float muonWeight1 = GetObjectWeight(muonsFromALPSegmentMatch0p2->at(0), "LooseMuons");
    float muonWeight2 = GetObjectWeight(muonsFromALPSegmentMatch0p2->at(1), "LooseMuons");
    histogramsHandler->Fill("LooseMuonsFromALPSegmentMatch0p2_invMass", (muon1fourVector+muon2fourVector).M(), weight * muonWeight1 * muonWeight2);
    auto muonsFromALPVertexSegmentMatch0p2 = asNanoEvent(event)->GetVertexForDimuon(muonsFromALPSegmentMatch0p2->at(0),muonsFromALPSegmentMatch0p2->at(1));
    FillMuonVertexHistograms(event,muonsFromALPVertexSegmentMatch0p2,"LooseMuonsFromALPVertexSegmentMatch0p2");
  }
  if(muonsFromALPSegmentMatch0p5->size() > 1) {
    TLorentzVector muon1fourVector = asNanoGenParticle(muonsFromALPSegmentMatch0p5->at(0))->GetFourVector();
    TLorentzVector muon2fourVector = asNanoGenParticle(muonsFromALPSegmentMatch0p5->at(1))->GetFourVector();
    float muonWeight1 = GetObjectWeight(muonsFromALPSegmentMatch0p5->at(0), "LooseMuons");
    float muonWeight2 = GetObjectWeight(muonsFromALPSegmentMatch0p5->at(1), "LooseMuons");
    histogramsHandler->Fill("LooseMuonsFromALPSegmentMatch0p5_invMass", (muon1fourVector+muon2fourVector).M(), weight * muonWeight1 * muonWeight2);
    auto muonsFromALPVertexSegmentMatch0p5 = asNanoEvent(event)->GetVertexForDimuon(muonsFromALPSegmentMatch0p5->at(0),muonsFromALPSegmentMatch0p5->at(1));
    FillMuonVertexHistograms(event,muonsFromALPVertexSegmentMatch0p5,"LooseMuonsFromALPVertexSegmentMatch0p5");
  }
}

