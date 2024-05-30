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
  try {
    config.GetMap("muonMatchingParams",muonMatchingParams);
  } catch (const Exception &e) {
    warn() << "Couldn't read muonMatchingParams from config file - no muon matching methods will be applied to muon collections" << endl;
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
        value = event->GetCollection(branchName.substr(1))->size();
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
  if (event->GetCollection("LooseMuons")->size() < 2) {
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

  auto leadingMuonObj = eventProcessor->GetMaxPtObject(event, collectionName);
  if(!leadingMuonObj) return;
  
  auto leadingTightMuon = asNanoMuon(leadingMuonObj);
  float leadingMuonSF = GetObjectWeight(leadingMuonObj, collectionName);

  TLorentzVector leadingMuonVector = leadingTightMuon->GetFourVector();
  TLorentzVector metVector = asNanoEvent(event)->GetMetFourVector();

  histogramsHandler->Fill(collectionName + "_deltaPhiMuonMET", metVector.DeltaPhi(leadingMuonVector), weight * leadingMuonSF);
  histogramsHandler->Fill(collectionName + "_minvMuonMET", (leadingMuonVector + metVector).M(), weight * leadingMuonSF);
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
  
  float size = objectCollection->size();
  histogramsHandler->Fill("Event_n"+collectionName, objectCollection->size(), weight);

  for(auto object : *objectCollection){
    float muonWeight = GetObjectWeight(object, "LooseMuons");

    histogramsHandler->Fill(collectionName+"_pt", object->Get("pt"), weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_eta", object->Get("eta"), weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_phi", object->Get("phi"), weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_dxy", object->Get("dxy"), weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_dxyPVTraj",       object->Get("dxyPVTraj"),       weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_dxyPVTrajErr",    object->Get("dxyPVTrajErr"),    weight * muonWeight);
    float dxyPVTrajSig = float(object->Get("dxyPVTraj")) / float(object->Get("dxyPVTrajErr"));
    histogramsHandler->Fill(collectionName+"_dxyPVTrajSig",    abs(float(dxyPVTrajSig)),                   weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_ip3DPVSigned",    object->Get("ip3DPVSigned"),    weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_ip3DPVSignedErr", object->Get("ip3DPVSignedErr"), weight * muonWeight);
    float ip3DPVSignedSig = float(object->Get("ip3DPVSigned")) / float(object->Get("ip3DPVSignedErr"));
    histogramsHandler->Fill(collectionName+"_ip3DPVSignedSig", abs(float(ip3DPVSignedSig)),                weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_dz",      object->Get("dz"),      weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_dzPV",    object->Get("dzPV"),    weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_dzPVErr", object->Get("dzPVErr"), weight * muonWeight);
    float dzPVSig = float(object->Get("dzPV")) / float(object->Get("dzPVErr"));
    histogramsHandler->Fill(collectionName+"_dzPVSig", dzPVSig,                weight * muonWeight);
  }
}

void TTAlpsHistogramFiller::FillLooseMuonsHistograms(const shared_ptr<Event> event, string collectionName) {
  float weight = GetEventWeight(event);
  
  auto objectCollection = event->GetCollection(collectionName);
  FillLooseMuonsHistograms(objectCollection, collectionName, weight);
}

void TTAlpsHistogramFiller::FillMuonVertexHistograms(const shared_ptr<Event> event, const shared_ptr<Collection<shared_ptr<PhysicsObject> >> vertexCollection, string vertexName) {
  float weight = GetEventWeight(event);
  // float weight = 1.;
    
  histogramsHandler->Fill("Event_n"+vertexName, vertexCollection->size(), weight);
  int nPatDSA = 0;
  int nPat = 0;
  int nDSA = 0;
  for(auto vertex : *vertexCollection){
    auto dimuonVertex = asNanoDimuonVertex(vertex,event);
    shared_ptr<PhysicsObject> muon1  = dimuonVertex->Muon1();
    shared_ptr<PhysicsObject> muon2  = dimuonVertex->Muon2();
    float muonWeight1 = GetObjectWeight(muon1, "LooseMuons");
    float muonWeight2 = GetObjectWeight(muon2, "LooseMuons");
    // float muonWeight1 = 1.;
    // float muonWeight2 = 1.;
    
    histogramsHandler->Fill(vertexName+"_chi2", dimuonVertex->Get("chi2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_ndof", dimuonVertex->Get("ndof"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_normChi2", dimuonVertex->Get("normChi2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxy", dimuonVertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxySigma", dimuonVertex->Get("vxySigma"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxySignificance", float(dimuonVertex->Get("vxy"))/float(dimuonVertex->Get("vxySigma")), weight * muonWeight1 * muonWeight2);
    if (float(dimuonVertex->Get("vxySigma")) == 0) histogramsHandler->Fill(vertexName+"_vxySignificanceV2", float(dimuonVertex->Get("vxy"))/float(dimuonVertex->Get("vxySigma")), weight * muonWeight1 * muonWeight2);
    else histogramsHandler->Fill(vertexName+"_vxySignificanceV2", -1, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxyz", dimuonVertex->Get("vxyz"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxyzSigma", dimuonVertex->Get("vxyzSigma"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxyzSignificance", float(dimuonVertex->Get("vxyz"))/float(dimuonVertex->Get("vxyzSigma")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vx", dimuonVertex->Get("vx"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vy", dimuonVertex->Get("vy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vz", dimuonVertex->Get("vz"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxErr", dimuonVertex->Get("vxErr"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxSignificance", float(dimuonVertex->Get("vx"))/float(dimuonVertex->Get("vxErr")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vyErr", dimuonVertex->Get("vyErr"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vySignificance", float(dimuonVertex->Get("vy"))/float(dimuonVertex->Get("vyErr")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vzErr", dimuonVertex->Get("vzErr"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vzSignificance", float(dimuonVertex->Get("vz"))/float(dimuonVertex->Get("vzErr")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_dR", dimuonVertex->Get("dR"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_proxDR", dimuonVertex->Get("dRprox"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_outerDR", dimuonVertex->GetOuterDeltaR(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_originalMuonIdx1", dimuonVertex->Get("originalMuonIdx1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_originalMuonIdx2", dimuonVertex->Get("originalMuonIdx2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_isDSAMuon1", dimuonVertex->Get("isDSAMuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_isDSAMuon2", dimuonVertex->Get("isDSAMuon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso03Dimuon1", dimuonVertex->Get("displacedTrackIso03Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso04Dimuon1", dimuonVertex->Get("displacedTrackIso04Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso03Dimuon2", dimuonVertex->Get("displacedTrackIso03Dimuon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso04Dimuon2", dimuonVertex->Get("displacedTrackIso04Dimuon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso03Muon1", dimuonVertex->Get("displacedTrackIso03Muon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso04Muon1", dimuonVertex->Get("displacedTrackIso04Muon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso03Muon2", dimuonVertex->Get("displacedTrackIso03Muon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_displacedTrackIso04Muon2", dimuonVertex->Get("displacedTrackIso04Muon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_chargeProduct", dimuonVertex->GetDimuonChargeProduct(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_hitsInFrontOfVert1", dimuonVertex->Get("hitsInFrontOfVert1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_hitsInFrontOfVert2", dimuonVertex->Get("hitsInFrontOfVert2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_hitsInFrontOfVertSum", float(dimuonVertex->Get("hitsInFrontOfVert1"))+float(dimuonVertex->Get("hitsInFrontOfVert2")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_maxHitsInFrontOfVert", max(float(dimuonVertex->Get("hitsInFrontOfVert1")),float(dimuonVertex->Get("hitsInFrontOfVert2"))), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_missHitsAfterVert1", dimuonVertex->Get("missHitsAfterVert1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_missHitsAfterVert2", dimuonVertex->Get("missHitsAfterVert2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_missHitsAfterVertSum", float(dimuonVertex->Get("missHitsAfterVert1"))+float(dimuonVertex->Get("missHitsAfterVert2")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_maxMissHitsAfterVert", max(float(dimuonVertex->Get("missHitsAfterVert1")),float(dimuonVertex->Get("missHitsAfterVert2"))), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_dca", dimuonVertex->Get("dca"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_dcaStatus", dimuonVertex->Get("dcaStatus"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_collinearityAngle", dimuonVertex->GetCollinearityAngle(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_absCollinearityAngle", abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_deltaPixelHits", dimuonVertex->GetDeltaPixelHits(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_lxyFromPV", dimuonVertex->GetLxyFromPV(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_lxyFromPVvxyDiff", abs(float(dimuonVertex->GetLxyFromPV())-float(dimuonVertex->Get("vxy"))), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_invMass", dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_pt", dimuonVertex->GetDimuonPt(), weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_invMass_absCollinearityAngle", dimuonVertex->GetInvariantMass(), abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);

    string category = dimuonVertex->GetVertexCategory();
    histogramsHandler->Fill(vertexName+"_"+category+"_chi2", dimuonVertex->Get("chi2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_ndof", dimuonVertex->Get("ndof"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_normChi2", dimuonVertex->Get("normChi2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxy", dimuonVertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxySigma", dimuonVertex->Get("vxySigma"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxySignificance", float(dimuonVertex->Get("vxy"))/float(dimuonVertex->Get("vxySigma")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vx", dimuonVertex->Get("vx"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vy", dimuonVertex->Get("vy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vz", dimuonVertex->Get("vz"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxyz", dimuonVertex->Get("vxyz"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxyzSigma", dimuonVertex->Get("vxyzSigma"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxyzSignificance", float(dimuonVertex->Get("vxyz"))/float(dimuonVertex->Get("vxyzSigma")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dR", dimuonVertex->Get("dR"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_proxDR", dimuonVertex->Get("dRprox"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDR", dimuonVertex->GetOuterDeltaR(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_hitsInFrontOfVert1", dimuonVertex->Get("hitsInFrontOfVert1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_hitsInFrontOfVert2", dimuonVertex->Get("hitsInFrontOfVert2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_hitsInFrontOfVertSum", float(dimuonVertex->Get("hitsInFrontOfVert1"))+float(dimuonVertex->Get("hitsInFrontOfVert2")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_maxHitsInFrontOfVert", max(float(dimuonVertex->Get("hitsInFrontOfVert1")),float(dimuonVertex->Get("hitsInFrontOfVert2"))), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_missHitsAfterVert1", dimuonVertex->Get("missHitsAfterVert1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_missHitsAfterVert2", dimuonVertex->Get("missHitsAfterVert2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_missHitsAfterVertSum", float(dimuonVertex->Get("missHitsAfterVert1"))+float(dimuonVertex->Get("missHitsAfterVert2")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_maxMissHitsAfterVert", max(float(dimuonVertex->Get("missHitsAfterVert1")),float(dimuonVertex->Get("missHitsAfterVert2"))), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dca", dimuonVertex->Get("dca"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dcaStatus", dimuonVertex->Get("dcaStatus"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_collinearityAngle", dimuonVertex->GetCollinearityAngle(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_absCollinearityAngle", abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);
    if(dimuonVertex->GetDeltaPixelHits() > -5) histogramsHandler->Fill(vertexName+"_"+category+"_absPATPtLxyDPhi", abs(dimuonVertex->GetPATpTLxyDPhi()), weight * muonWeight1 * muonWeight2);
    else histogramsHandler->Fill(vertexName+"_"+category+"_absPATPtLxyDPhi", -1, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_deltaPixelHits", dimuonVertex->GetDeltaPixelHits(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_lxyFromPV", dimuonVertex->GetLxyFromPV(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_invMass", dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_pt", dimuonVertex->GetDimuonPt(), weight * muonWeight1 * muonWeight2);
    float nPixelHits1, nPixelHits2, nTrackerLayers1, nTrackerLayers2;
    if(category=="Pat") {
      nPixelHits1 = dimuonVertex->Muon1()->Get("trkNumPixelHits");
      nPixelHits2 = dimuonVertex->Muon2()->Get("trkNumPixelHits");
      nTrackerLayers1 = dimuonVertex->Muon1()->Get("trkNumTrkLayers");
      nTrackerLayers2 = dimuonVertex->Muon2()->Get("trkNumTrkLayers");
    }
    if(category=="PatDSA") {
      nPixelHits1 = dimuonVertex->Muon1()->Get("trkNumPixelHits");
      nPixelHits2 = 0;
      nTrackerLayers1 = dimuonVertex->Muon1()->Get("trkNumTrkLayers");
      nTrackerLayers2 = 0;
    }
    if(category=="DSA") {
      nPixelHits1 = 0;
      nPixelHits2 = 0;
      nTrackerLayers1 = 0;
      nTrackerLayers2 = 0;
    }
    histogramsHandler->Fill(vertexName+"_"+category+"_nPixelHits1", nPixelHits1, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_nPixelHits2", nPixelHits2, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_nTrackerLayers1", nTrackerLayers1, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_nTrackerLayers2", nTrackerLayers2, weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_"+category+"_Lxy_nTrackerLayers1", dimuonVertex->GetLxyFromPV(), nTrackerLayers1, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_Lxy_nTrackerLayers2", dimuonVertex->GetLxyFromPV(), nTrackerLayers2, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_Lxy_maxTrackerLayers", dimuonVertex->GetLxyFromPV(), max(nTrackerLayers1,nTrackerLayers2), weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_"+category+"_invMass_absCollinearityAngle", dimuonVertex->GetInvariantMass(), abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);

    if(category=="PatDSA") nPatDSA++;
    if(category=="Pat") nPat++;
    if(category=="DSA") nDSA++;

    if(vertexName == "GoodBestLooseMuonsVertexTight") {
      std::cout << "GoodBestLooseMuonsVertexTight" << std::endl;
      std::cout << "proxDR: " << (float)dimuonVertex->Get("dRprox") << std::endl;
    }
  }
  histogramsHandler->Fill("Event_n"+vertexName+"_PatDSA", nPatDSA, weight);
  histogramsHandler->Fill("Event_n"+vertexName+"_Pat", nPat, weight);
  histogramsHandler->Fill("Event_n"+vertexName+"_DSA", nDSA, weight);
}

void TTAlpsHistogramFiller::FillMuonVertexHistograms(const shared_ptr<Event> event, string vertexName) {
  auto vertexCollection = event->GetCollection(vertexName);
  FillMuonVertexHistograms(event, vertexCollection, vertexName);
}


void TTAlpsHistogramFiller::FillMuonMinDeltaRHistograms(const shared_ptr<Event> event, const shared_ptr<Collection<shared_ptr<PhysicsObject> >> muonCollection, string collectionName) {
  float weight = GetEventWeight(event);
  
  float minDeltaR = 999;
  float minDeltaRSF1 = 1;
  float minDeltaRSF2 = 1;
  float minOuterDeltaR = 999;
  float minOuterDeltaRSF1 = 1;
  float minOuterDeltaRSF2 = 1;
  float minProxDeltaR = 999;
  float minProxDeltaRSF1 = 1;
  float minProxDeltaRSF2 = 1;
  for (int iMuon1 = 0; iMuon1 < muonCollection->size(); iMuon1++) {
    auto muon1 = muonCollection->at(iMuon1);
    auto muon1SF = GetObjectWeight(muon1, collectionName);
    TLorentzVector muon1Vector = asNanoMuon(muon1)->GetFourVector();

    for (int iMuon2 = iMuon1 + 1; iMuon2 < muonCollection->size(); iMuon2++) {
      auto muon2 = muonCollection->at(iMuon2);
      auto muon2SF = GetObjectWeight(muon2, collectionName);
      TLorentzVector muon2Vector = asNanoMuon(muon2)->GetFourVector();

      if(muon1Vector.DeltaR(muon2Vector) < minDeltaR) {
        minDeltaR = float(muon1Vector.DeltaR(muon2Vector));
        minDeltaRSF1 = muon1SF;
        minDeltaRSF2 = muon2SF;
      }
      if(asNanoMuon(muon1)->OuterDeltaRtoMuon(asNanoMuon(muon2)) < minOuterDeltaR) {
        minOuterDeltaR = asNanoMuon(muon1)->OuterDeltaRtoMuon(asNanoMuon(muon2));
        minOuterDeltaRSF1 = muon1SF;
        minOuterDeltaRSF2 = muon2SF;
      }
      
      auto vertex = asNanoEvent(event)->GetVertexForDimuon(muon1, muon2);
      if(vertex->size() > 0) {
        if(float(vertex->at(0)->Get("dRprox")) < minProxDeltaR) {
          minProxDeltaR = vertex->at(0)->Get("dRprox");
          minProxDeltaRSF1 = muon1SF;
          minProxDeltaRSF2 = muon2SF;
        }
      }
    }
  }
  histogramsHandler->Fill(collectionName + "_minDeltaR", minDeltaR, weight * minDeltaRSF1 * minDeltaRSF2);
  histogramsHandler->Fill(collectionName + "_minOuterDeltaR", minOuterDeltaR, weight * minOuterDeltaRSF1 * minOuterDeltaRSF2);
  histogramsHandler->Fill(collectionName + "_minProxDeltaR", minProxDeltaR, weight * minProxDeltaRSF1 * minProxDeltaRSF2);
}

void TTAlpsHistogramFiller::FillMuonMinDeltaRHistograms(const shared_ptr<Event> event, string collectionName) {
  auto muonCollection = event->GetCollection(collectionName);
  if(muonCollection->size() < 2) return;
  FillMuonMinDeltaRHistograms(event, muonCollection, collectionName);
}

void TTAlpsHistogramFiller::FillMuonVertexCorrelationHistograms(const shared_ptr<Event> event, string vertexName) {
  auto vertexCollection = event->GetCollection(vertexName);
  float weight = GetEventWeight(event);
  // float weight = 1.;
  
  for (auto vertex : *vertexCollection) {
    float muonWeight1 = GetObjectWeight(asNanoDimuonVertex(vertex,event)->Muon1(), "LooseMuons");
    float muonWeight2 = GetObjectWeight(asNanoDimuonVertex(vertex,event)->Muon2(), "LooseMuons");
    // float muonWeight1 = 1.;
    // float muonWeight2 = 1.;

    float vxySignificance = float(vertex->Get("vxy"))/float(vertex->Get("vxySigma"));
    float vxyzSignificance = float(vertex->Get("vxyz"))/float(vertex->Get("vxyzSigma"));
    
    histogramsHandler->Fill(vertexName+"_normChi2_ndof", vertex->Get("normChi2"), vertex->Get("ndof"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxySigma_vxy", vertex->Get("vxySigma"), vertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxyzSigma_vxyz", vertex->Get("vxyzSigma"), vertex->Get("vxyz"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxySigma_vxySignificance", vertex->Get("vxySigma"), vxySignificance, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxyzSigma_vxyzSignificance", vertex->Get("vxyzSigma"), vxyzSignificance, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxySignificance_vxy", vxySignificance, vertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxyzSignificance_vxyz", vxyzSignificance, vertex->Get("vxyz"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vxErr_vx", vertex->Get("vxErr"), vertex->Get("vx"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vyErr_vy", vertex->Get("vyErr"), vertex->Get("vy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_vzErr_vz", vertex->Get("vzErr"), vertex->Get("vz"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_normChi2_vxy", vertex->Get("normChi2"), vertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_normChi2_vxyz", vertex->Get("normChi2"), vertex->Get("vxyz"), weight * muonWeight1 * muonWeight2);
  }
}

void TTAlpsHistogramFiller::FillAllLooseMuonsHistograms(const shared_ptr<Event> event){
  float weight = GetEventWeight(event);

  for(auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    FillLooseMuonsHistograms(event, muonCollectionName);
    FillMuonMinDeltaRHistograms(event, muonCollectionName);
    auto DSAmuonCollection = asNanoEvent(event)->GetDSAMuonsFromCollection(muonCollectionName);
    auto PATmuonCollection = asNanoEvent(event)->GetPATMuonsFromCollection(muonCollectionName);
    string DSAmuonCollectionName = "LooseDSAMuons" + matchingMethod + "Match";
    string PATmuonCollectionName = "LoosePATMuons" + matchingMethod + "Match";
    FillLooseMuonsHistograms(DSAmuonCollection, DSAmuonCollectionName, weight);
    FillLooseMuonsHistograms(PATmuonCollection, PATmuonCollectionName, weight);
    string muonVertexCollectionName = "LooseMuonsVertex" + matchingMethod + "Match";
    FillMuonVertexHistograms(event,muonVertexCollectionName);
  }

  FillMuonVertexHistograms(event,"MaskedLooseMuonsVertex");
  FillMuonVertexHistograms(event,"GoodLooseMuonsVertex");
  FillMuonVertexHistograms(event,"GoodLooseMuonsVertexTight");
  FillMuonVertexHistograms(event,"GoodMaskedLooseMuonsVertex");
  FillMuonVertexHistograms(event,"BestLooseMuonsVertex");
  FillMuonVertexHistograms(event,"SecondBestLooseMuonsVertex");
  FillMuonVertexHistograms(event,"GoodBestLooseMuonsVertex");
  FillMuonVertexHistograms(event,"GoodSecondBestLooseMuonsVertex");
  FillMuonVertexHistograms(event,"GoodBestLooseMuonsVertexTight");
  FillMuonVertexHistograms(event,"GoodSecondBestLooseMuonsVertexTight");

  FillMuonVertexCorrelationHistograms(event, "GoodLooseMuonsVertex");
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
}

void TTAlpsHistogramFiller::FillCustomTTAlpsGenMuonVariables(const shared_ptr<Event> event) {
  FillGenMuonsFromALPsHistograms(event);
  FillLooseMuonsFromALPsHistograms(event);
  FillGenALPsHistograms(event);
}

void TTAlpsHistogramFiller::FillCustomTTAlpsMuonMatchingVariables(const shared_ptr<Event> event) {
  FillMatchingHistograms(event, "LooseMuons", "LooseDSAMuons");
}

void TTAlpsHistogramFiller::FillGenALPsHistograms(const shared_ptr<Event> event) {
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
    auto ALPfourvector = asNanoGenParticle(genALP)->GetFourVector(asNanoGenParticle(genALP)->GetMass());
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

void TTAlpsHistogramFiller::FillDimuonHistograms(const shared_ptr<PhysicsObject> muon1, const shared_ptr<PhysicsObject> muon2, string collectionName, float weight, bool genLevel) {
  TLorentzVector muon1fourVector;
  TLorentzVector muon2fourVector;
  float muon1Weight = 1;
  float muon2Weight = 1;
  if(genLevel) {
    muon1fourVector = asNanoGenParticle(muon1)->GetFourVector(0.105);
    muon2fourVector = asNanoGenParticle(muon2)->GetFourVector(0.105);
  } else {
    muon1fourVector = asNanoMuon(muon1)->GetFourVector();
    muon2fourVector = asNanoMuon(muon2)->GetFourVector();
    muon1Weight = GetObjectWeight(muon1, "LooseMuons");
    muon2Weight = GetObjectWeight(muon2, "LooseMuons");
  }
  histogramsHandler->Fill(collectionName+"_invMass", (muon1fourVector+muon2fourVector).M(), weight * muon1Weight * muon2Weight);
  histogramsHandler->Fill(collectionName+"_deltaR", muon1fourVector.DeltaR(muon2fourVector), weight * muon1Weight * muon2Weight);
  histogramsHandler->Fill(collectionName+"_deltaEta", muon1fourVector.Eta()-muon2fourVector.Eta(), weight * muon1Weight * muon2Weight);
  histogramsHandler->Fill(collectionName+"_deltaPhi", muon1fourVector.DeltaPhi(muon2fourVector), weight * muon1Weight * muon2Weight);
  if(!genLevel){
    float outerDeltaR = asNanoMuon(muon1)->OuterDeltaRtoMuon(asNanoMuon(muon2));
    histogramsHandler->Fill(collectionName+"_outerDeltaR", outerDeltaR, weight * muon1Weight * muon2Weight);
  }
}

void TTAlpsHistogramFiller::FillGenMuonMinDR(const shared_ptr<PhysicsObject> genMuon, const shared_ptr<Collection<shared_ptr<PhysicsObject> >> muonCollection, string muonCollectionName, float weight) {
  float muonMass = 0.105;
  TLorentzVector genMuonFourVector = asNanoGenParticle(genMuon)->GetFourVector(muonMass);
  float deltaRmin = 9999.;
  float muonWeight = 1;
  for ( auto muon : *muonCollection ) {
    TLorentzVector muonFourVector = asNanoMuon(muon)->GetFourVector();
    if(genMuonFourVector.DeltaR(muonFourVector) < deltaRmin) {
      deltaRmin = genMuonFourVector.DeltaR(muonFourVector);
      muonWeight = GetObjectWeight(muon, "LooseMuons");
    }
  }
  if(deltaRmin < 9999.) histogramsHandler->Fill("GenMuonFromALP_"+muonCollectionName+"MinDR", deltaRmin, weight*muonWeight);
}

void TTAlpsHistogramFiller::FillGenMuonsFromALPsHistograms(const shared_ptr<Event> event) {
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
    TLorentzVector genMuon1fourVector = asNanoGenParticle(genMuon)->GetFourVector(0.105);

    int pdgId = genMuon->Get("pdgId");
    histogramsHandler->Fill("GenMuonFromALP_pdgId",  pdgId,                  weight);
    histogramsHandler->Fill("GenMuonFromALP_pt",     genMuon->Get("pt"),     weight);
    histogramsHandler->Fill("GenMuonFromALP_mass",   genMuon->Get("mass"),   weight);
    histogramsHandler->Fill("GenMuonFromALP_eta",    genMuon->Get("eta"),    weight);
    histogramsHandler->Fill("GenMuonFromALP_phi",    genMuon->Get("phi"),    weight);
    float vx = genMuon->Get("vx");
    float vy = genMuon->Get("vy");
    float vz = genMuon->Get("vz");
    float vxy = sqrt(vx*vx + vy*vy);
    float vxyz = sqrt(vx*vx + vy*vy + vz*vz);
    histogramsHandler->Fill("GenMuonFromALP_vx",     vx,                     weight);
    histogramsHandler->Fill("GenMuonFromALP_vy",     vy,                     weight);
    histogramsHandler->Fill("GenMuonFromALP_vz",     vz,                     weight);
    histogramsHandler->Fill("GenMuonFromALP_vxy",    vxy,                    weight);
    histogramsHandler->Fill("GenMuonFromALP_vxyz",   vxyz,                   weight);
    float boost = float(genMuon->Get("pt")) / float(genMuon->Get("mass"));
    histogramsHandler->Fill("GenMuonFromALP_boost", boost, weight);

    float dxy = asNanoGenParticle(genMuon)->GetDxy(pv_x, pv_y);
    histogramsHandler->Fill("GenMuonFromALP_dxy", dxy, weight);

    for (int j = i+1; j<genMuonsFromALP->size(); j++)
    {
      if(j==i) continue;
      auto genMuon2 = genMuonsFromALP->at(j);
      TLorentzVector genMuon2fourVector = asNanoGenParticle(genMuon2)->GetFourVector(0.105);

      FillDimuonHistograms(genMuon, genMuon2, "GenDimuonFromALP", weight, true);
      nGenDimuons++;
    }
    int motherIndex = asNanoGenParticle(genMuon)->GetMotherIndex();
    if(motherIndex<0) continue;
    auto genALP = asNanoGenParticle(genParticles->at(motherIndex));
    auto ALPfourvector = genALP->GetFourVector(genALP->GetMass());
    float ALPboost_pT = float(genALP->GetPt()) / float(genALP->GetMass());
    float ALPboost_p = ALPfourvector.P() / float(genALP->GetMass());
    float ALPboost_T = float(genALP->GetPt()) / ALPfourvector.Mt();
    histogramsHandler->Fill("GenMuonFromALP_vxyALPboostpT", vxy/ALPboost_pT, weight);
    histogramsHandler->Fill("GenMuonFromALP_vxyALPboostT", vxy/ALPboost_T, weight);
    histogramsHandler->Fill("GenMuonFromALP_vxyzALPboostp", vxyz/ALPboost_p, weight);
  }
  histogramsHandler->Fill("Event_nGenDimuonFromALP", nGenDimuons, weight);
}

void TTAlpsHistogramFiller::FillLooseMuonsFromALPsHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  auto genMuonsFromALP = asTTAlpsEvent(event)->GetGenMuonsFromALP();

  auto loosePATMuons = event->GetCollection("LooseMuons");
  auto looseDSAMuons = event->GetCollection("LooseDSAMuons");

  for(auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    auto looseMatchedMuons = event->GetCollection(muonCollectionName);
    for ( auto genMuon : *genMuonsFromALP ) {
      FillGenMuonMinDR(genMuon, looseMatchedMuons, muonCollectionName, weight);
      auto looseMatchedMuonsFromALP = asTTAlpsEvent(event)->GetMuonsMatchedToGenMuonsFromALP(looseMatchedMuons);

      string muonFromALPsCollectionName = "LooseMuonsFromALP"+matchingMethod+"Match";
      FillLooseMuonsHistograms(looseMatchedMuonsFromALP,muonFromALPsCollectionName,weight);
      FillMuonMinDeltaRHistograms(event, looseMatchedMuonsFromALP, muonFromALPsCollectionName);

      if(looseMatchedMuonsFromALP->size() > 1) {
        FillDimuonHistograms(looseMatchedMuonsFromALP->at(0), looseMatchedMuonsFromALP->at(1), muonFromALPsCollectionName, weight, false);
        auto dimuonVertex = asNanoEvent(event)->GetVertexForDimuon(looseMatchedMuonsFromALP->at(0),looseMatchedMuonsFromALP->at(1));
        string muonFromALPsVertexCollectionName = muonFromALPsCollectionName+"Vertex";
        if(dimuonVertex->size() > 0) FillMuonVertexHistograms(event,dimuonVertex,muonFromALPsVertexCollectionName);
      }
    }

  }
  for ( auto genMuon : *genMuonsFromALP ) {
    FillGenMuonMinDR(genMuon, loosePATMuons, "LoosePATMuons", weight);
    FillGenMuonMinDR(genMuon, looseDSAMuons, "LooseDSAMuons", weight);
  }
}

void TTAlpsHistogramFiller::FillMatchedMuonHistograms(const shared_ptr<PhysicsObject> muon, string muonCollectionName, float weight) {
  histogramsHandler->Fill(muonCollectionName+"_pt", muon->Get("pt"), weight);
  histogramsHandler->Fill(muonCollectionName+"_eta", muon->Get("eta"), weight);
  histogramsHandler->Fill(muonCollectionName+"_phi", muon->Get("phi"), weight);
  histogramsHandler->Fill(muonCollectionName+"_dxy", muon->Get("dxy"), weight);
  histogramsHandler->Fill(muonCollectionName+"_dxyPVTraj", muon->Get("dxyPVTraj"), weight);
  float dxyPVTrajSig = abs(float(muon->Get("dxyPVTraj")) / float(muon->Get("dxyPVTrajErr")));
  histogramsHandler->Fill(muonCollectionName+"_dxyPVTrajSig", dxyPVTrajSig, weight);
  histogramsHandler->Fill(muonCollectionName+"_ip3DPVSigned", muon->Get("ip3DPVSigned"), weight);
  float ip3DPVSignedSig = abs(float(muon->Get("ip3DPVSigned")) / float(muon->Get("ip3DPVSignedErr")));
  histogramsHandler->Fill(muonCollectionName+"_ip3DPVSignedSig", ip3DPVSignedSig, weight);
  histogramsHandler->Fill(muonCollectionName+"_dzPV",            muon->Get("dzPV"),    weight);
  float dzPVSig = float(muon->Get("dzPV")) / float(muon->Get("dzPVErr"));
  histogramsHandler->Fill(muonCollectionName+"_dzPVSig", dzPVSig, weight);
}

void TTAlpsHistogramFiller::FillMatchingHistograms(const shared_ptr<Event> event, string patMuonCollection, string dsaMuonCollection) {
  float weight = GetEventWeight(event);

  auto looseMuons = event->GetCollection(patMuonCollection);
  auto looseDsaMuons = event->GetCollection(dsaMuonCollection);

  float matchingMinDeltaR = 0.1;

  // Segment-based matching
  float nSegmentMatched = 0;
  float nSegmentDRMatched = 0;
  float nSegmentOuterDRMatched = 0;
  for(auto dsaMuon : *looseDsaMuons){
    
    float muonWeight = GetObjectWeight(dsaMuon, "LooseMuons");
    float nSegments = dsaMuon->Get("nSegments");
    float minRatio = float(2)/float(3);

    histogramsHandler->Fill(dsaMuonCollection+"_nDTHits", dsaMuon->Get("trkNumDTHits"), weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_nCSCHits", dsaMuon->Get("trkNumCSCHits"), weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_nDTplusCSCHits", float(dsaMuon->Get("trkNumDTHits"))+float(dsaMuon->Get("trkNumCSCHits")), weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_nSegments", nSegments, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch1", dsaMuon->Get("muonMatch1"), weight * muonWeight);
    float ratio1 = float(dsaMuon->Get("muonMatch1")) / nSegments;
    histogramsHandler->Fill(dsaMuonCollection+"_matchRatio1", ratio1, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch2", dsaMuon->Get("muonMatch2"), weight * muonWeight);
    float ratio2 = float(dsaMuon->Get("muonMatch2")) / nSegments;
    histogramsHandler->Fill(dsaMuonCollection+"_matchRatio2", ratio2, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch3", dsaMuon->Get("muonMatch3"), weight * muonWeight);
    float ratio3 = float(dsaMuon->Get("muonMatch3")) / nSegments;
    histogramsHandler->Fill(dsaMuonCollection+"_matchRatio3", ratio3, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch1_nSegments", dsaMuon->Get("muonMatch1"), nSegments, weight*muonWeight*muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch2_nSegments", dsaMuon->Get("muonMatch2"), nSegments, weight*muonWeight*muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch3_nSegments", dsaMuon->Get("muonMatch3"), nSegments, weight*muonWeight*muonWeight);

    float matchFound = false;
    float muon_idx = -1;
    float maxMatches = -1;
    float ratio = -1;
    for(int i=1; i<=5; i++) {
      float ratio_tmp = asNanoMuon(dsaMuon)->GetMatchesForNthBestMatch(i) / nSegments;
      if(!matchFound && ratio_tmp >= minRatio) {
        if(asNanoEvent(event)->PATMuonIndexExist(looseMuons, asNanoMuon(dsaMuon)->GetMatchIdxForNthBestMatch(i))) {
          matchFound = true;
          muon_idx = asNanoMuon(dsaMuon)->GetMatchIdxForNthBestMatch(i);
          maxMatches = asNanoMuon(dsaMuon)->GetMatchesForNthBestMatch(i);
          ratio = ratio_tmp;
        }
      }
    }
    if(matchFound) {
      nSegmentMatched++;
      pair<float,int> dsaGenMinDR = asNanoEvent(event)->GetDeltaRandIndexOfClosestGenMuon(dsaMuon);
      float dsaMinDR = dsaGenMinDR.first;
      float dsaMinDR_genidx = dsaGenMinDR.second;
      auto muon = asNanoEvent(event)->GetPATMuonWithIndex(muon_idx, patMuonCollection);
      pair<float,int> patGenMinDR = asNanoEvent(event)->GetDeltaRandIndexOfClosestGenMuon(muon); 
      float patMinDR = patGenMinDR.first;
      float patMinDR_genidx = patGenMinDR.second;
      float muonWeight = GetObjectWeight(muon, "LooseMuons");
      float dsaMuonWeight = GetObjectWeight(dsaMuon, "LooseMuons");

      histogramsHandler->Fill("SegmentMatch"+dsaMuonCollection+"_genMinDR", dsaMinDR, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch"+dsaMuonCollection+"_genMinDRidx", dsaMinDR_genidx, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_genMinDR", patMinDR, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_genMinDRidx", patMinDR_genidx, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_"+dsaMuonCollection+"_genMinDR", patMinDR, dsaMinDR, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_"+dsaMuonCollection+"_genMinDRidx", patMinDR_genidx, dsaMinDR_genidx, weight * muonWeight);
      
      FillMatchedMuonHistograms(muon, "SegmentMatch"+patMuonCollection, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_nSegments", nSegments, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_matchingRatio", ratio, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_maxMatches", maxMatches, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_muonMatchIdx", muon_idx, weight * muonWeight);

      FillMatchedMuonHistograms(muon, "SegmentMatch"+dsaMuonCollection, weight * dsaMuonWeight);

      histogramsHandler->Fill("SegmentMatch"+dsaMuonCollection+"_eta_outerEta", dsaMuon->Get("eta"), dsaMuon->Get("outerEta"), weight*dsaMuonWeight*dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch"+dsaMuonCollection+"_phi_outerPhi", dsaMuon->Get("phi"), dsaMuon->Get("outerPhi"), weight*dsaMuonWeight*dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_eta_outerEta", muon->Get("eta"), muon->Get("outerEta"), weight*muonWeight*muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_phi_outerPhi", muon->Get("phi"), muon->Get("outerPhi"), weight*muonWeight*muonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_"+dsaMuonCollection+"_eta", muon->Get("eta"), dsaMuon->Get("eta"), weight*muonWeight*dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_"+dsaMuonCollection+"_phi", muon->Get("phi"), dsaMuon->Get("phi"), weight*muonWeight*dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_"+dsaMuonCollection+"_outerEta", muon->Get("outerEta"), dsaMuon->Get("outerEta"), weight*muonWeight*dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch"+patMuonCollection+"_"+dsaMuonCollection+"_outerPhi", muon->Get("outerPhi"), dsaMuon->Get("outerPhi"), weight*muonWeight*dsaMuonWeight);

      // Segment-based + DR matching
      auto dsaMuonP4 = asNanoMuon(dsaMuon)->GetFourVector();
      auto muonP4 = asNanoMuon(muon)->GetFourVector();
      if(muonP4.DeltaR(dsaMuonP4) < matchingMinDeltaR) {
        nSegmentDRMatched++;
        FillMatchedMuonHistograms(muon, "SegmentDRMatch"+patMuonCollection, weight * muonWeight);
        histogramsHandler->Fill("SegmentDRMatch"+patMuonCollection+"_nSegments", nSegments, weight * muonWeight);
        histogramsHandler->Fill("SegmentDRMatch"+patMuonCollection+"_matchingRatio", ratio, weight * muonWeight);
        histogramsHandler->Fill("SegmentDRMatch"+patMuonCollection+"_maxMatches", maxMatches, weight * muonWeight);
        histogramsHandler->Fill("SegmentDRMatch"+patMuonCollection+"_muonMatchIdx", muon_idx, weight * muonWeight);
      }

      // Segment-based + Outer DR matching
      float eta1 = dsaMuon->Get("outerEta");
      float phi1 = dsaMuon->Get("outerPhi");
      float eta2 = muon->Get("outerEta");
      float phi2 = muon->Get("outerPhi");
      if(asNanoEvent(event)->DeltaR(eta1, phi1, eta2, phi2) < matchingMinDeltaR) {
        nSegmentOuterDRMatched++;
        FillMatchedMuonHistograms(muon, "SegmentOuterDRMatch"+patMuonCollection, weight * muonWeight);
        histogramsHandler->Fill("SegmentOuterDRMatch"+patMuonCollection+"_nSegments", nSegments, weight * muonWeight);
        histogramsHandler->Fill("SegmentOuterDRMatch"+patMuonCollection+"_matchingRatio", ratio, weight * muonWeight);
        histogramsHandler->Fill("SegmentOuterDRMatch"+patMuonCollection+"_maxMatches", maxMatches, weight * muonWeight);
        histogramsHandler->Fill("SegmentOuterDRMatch"+patMuonCollection+"_muonMatchIdx", muon_idx, weight * muonWeight);
      }
    }
  }
  histogramsHandler->Fill("Event_nSegmentMatch"+patMuonCollection, nSegmentMatched, weight);
  histogramsHandler->Fill("Event_nSegmentMatch"+dsaMuonCollection, nSegmentMatched, weight);
  histogramsHandler->Fill("Event_nSegmentDRMatch"+patMuonCollection, nSegmentDRMatched, weight);
  histogramsHandler->Fill("Event_nSegmentOuterDRMatch"+patMuonCollection, nSegmentOuterDRMatched, weight);

  // Delta R matching values
  for(auto dsaMuon : *looseDsaMuons){
    auto dsaMuonP4 = asNanoMuon(dsaMuon)->GetFourVector();
    float dsaMuonWeight = GetObjectWeight(dsaMuon, "LooseMuons");

    for(auto patMuon : *looseMuons){
      float patMuonWeight = GetObjectWeight(patMuon, "LooseMuons");
      auto patMuonP4 = asNanoMuon(patMuon)->GetFourVector();
      float outerDeltaR = asNanoMuon(dsaMuon)->OuterDeltaRtoMuon(asNanoMuon(patMuon));
      float deltaR = dsaMuonP4.DeltaR(patMuonP4);
      histogramsHandler->Fill(dsaMuonCollection+"_PATDR", deltaR, weight*dsaMuonWeight*patMuonWeight);
      histogramsHandler->Fill(dsaMuonCollection+"_PATOuterDR", outerDeltaR, weight*dsaMuonWeight*patMuonWeight);

      auto vertex = asNanoEvent(event)->GetVertexForDimuon(dsaMuon,patMuon);
      if(vertex->size() > 0) {
        float proxDR = vertex->at(0)->Get("dRprox");
        histogramsHandler->Fill(dsaMuonCollection+"_PATProxDR", proxDR, weight*dsaMuonWeight*patMuonWeight);
      }
    }
  }
}
