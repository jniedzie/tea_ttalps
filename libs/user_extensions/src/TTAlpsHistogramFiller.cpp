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
  bool nonIso = false;
  try {
    config.GetValue("useNonIsolatedLooseMuons", nonIso);
  } catch (const Exception &e) {
    info() << "Couldn't read useNonIsolatedLooseMuons from config file - will use isolated LooseMuons collection with isolation cuts" << endl;
  }
  useNonIsolatedLooseMuons = nonIso;
  try {
    config.GetVector("muonVertexCollectionNames", muonVertexCollectionNames);
  } catch (const Exception &e) {
    info() << "Couldn't read muonVertexCollectionNames from config file - no muon vertex collection histograms will be filled" << endl;
  }
  try {
    config.GetMap("muonVertexCollections", muonVertexCollections);
  } catch (const Exception &e) {
    info() << "Couldn't read muonVertexCollections from config file - no dimuon cutflows will be filled" << endl;
  }
  try {
    config.GetVector("muonVertexNminus1Collections", muonVertexNminus1Collections);
  } catch (const Exception &e) {
    info() << "Couldn't read muonVertexNminus1Collections from config file - no N-1 muon vertex collection histograms will be filled" << endl;
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
    histogramsHandler->Fill(collectionName+"_absDxyPVTraj", abs(float(object->Get("dxyPVTraj"))), weight);
    histogramsHandler->Fill(collectionName+"_dxyPVTrajErr",    object->Get("dxyPVTrajErr"), weight * muonWeight);
    float dxyPVTrajSig = abs(float(object->Get("dxyPVTraj")) / float(object->Get("dxyPVTrajErr")));
    histogramsHandler->Fill(collectionName+"_dxyPVTrajSig",    abs(float(dxyPVTrajSig)), weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_ip3DPVSigned",    object->Get("ip3DPVSigned"), weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_ip3DPVSignedErr", object->Get("ip3DPVSignedErr"), weight * muonWeight);
    float ip3DPVSignedSig = float(object->Get("ip3DPVSigned")) / float(object->Get("ip3DPVSignedErr"));
    histogramsHandler->Fill(collectionName+"_ip3DPVSignedSig", abs(float(ip3DPVSignedSig)), weight * muonWeight);

    int isPATMuon = 0;
    int isTightMuon = 0;
    if(!asNanoMuon(object)->isDSA()) {
      histogramsHandler->Fill(collectionName+"_pfRelIso04all", object->Get("pfRelIso04_all"), weight * muonWeight);
      histogramsHandler->Fill(collectionName+"_tkRelIso", object->Get("tkRelIso"), weight * muonWeight);
      isPATMuon = 1;
      if(asNanoMuon(object)->isTight()) isTightMuon = 1;
    }
    histogramsHandler->Fill(collectionName+"_isPAT", isPATMuon, weight * muonWeight);
    histogramsHandler->Fill(collectionName+"_isTight", isTightMuon, weight * muonWeight);
  }
}

void TTAlpsHistogramFiller::FillLooseMuonsHistograms(const shared_ptr<Event> event, string collectionName) {
  float weight = GetEventWeight(event);
  
  auto objectCollection = event->GetCollection(collectionName);
  FillLooseMuonsHistograms(objectCollection, collectionName, weight);
}

void TTAlpsHistogramFiller::FillMuonVertexHistograms(const shared_ptr<Event> event, const shared_ptr<Collection<shared_ptr<PhysicsObject> >> vertexCollection, string vertexName) {
  float weight = GetEventWeight(event);
    
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

    string category = dimuonVertex->GetVertexCategory();

    histogramsHandler->Fill(vertexName+"_"+category+"_normChi2", dimuonVertex->Get("normChi2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_Lxy", dimuonVertex->GetLxyFromPV(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxy", dimuonVertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxySigma", dimuonVertex->Get("vxySigma"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxySignificance", float(dimuonVertex->Get("vxy"))/float(dimuonVertex->Get("vxySigma")), weight * muonWeight1 * muonWeight2);
    if(float(dimuonVertex->Get("vxySigma"))!=0) histogramsHandler->Fill(vertexName+"_"+category+"_vxySignificanceV2", float(dimuonVertex->Get("vxy"))/float(dimuonVertex->Get("vxySigma")), weight * muonWeight1 * muonWeight2);
    else histogramsHandler->Fill(vertexName+"_"+category+"_vxySignificanceV2", float(dimuonVertex->Get("vxy")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dR", dimuonVertex->Get("dR"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_proxDR", dimuonVertex->Get("dRprox"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDR", dimuonVertex->GetOuterDeltaR(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_maxHitsInFrontOfVert", max(float(dimuonVertex->Get("hitsInFrontOfVert1")),float(dimuonVertex->Get("hitsInFrontOfVert2"))), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_sumHitsInFrontOfVert", float(dimuonVertex->Get("hitsInFrontOfVert1"))+float(dimuonVertex->Get("hitsInFrontOfVert2")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_maxMissHitsAfterVert", max(float(dimuonVertex->Get("missHitsAfterVert1")),float(dimuonVertex->Get("missHitsAfterVert2"))), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_hitsInFrontOfVert1", dimuonVertex->Get("hitsInFrontOfVert1"), weight * muonWeight1);
    histogramsHandler->Fill(vertexName+"_"+category+"_hitsInFrontOfVert2", dimuonVertex->Get("hitsInFrontOfVert2"), weight * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dca", dimuonVertex->Get("dca"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_absCollinearityAngle", abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_absPtLxyDPhi1", abs(dimuonVertex->GetDPhiBetweenMuonpTAndLxy(1)), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_absPtLxyDPhi2", abs(dimuonVertex->GetDPhiBetweenMuonpTAndLxy(2)), weight * muonWeight1 * muonWeight2);
    // histogramsHandler->Fill(vertexName+"_"+category+"_absPtPtMissDPhi", abs(dimuonVertex->GetDPhiBetweenDimuonpTAndPtMiss(asNanoEvent(event)->GetMetFourVector())), weight * muonWeight1 * muonWeight2);
    // if(dimuonVertex->GetDeltaPixelHits() > -5) histogramsHandler->Fill(vertexName+"_"+category+"_deltaPixelHits", dimuonVertex->GetDeltaPixelHits(), weight * muonWeight1 * muonWeight2);
    // else histogramsHandler->Fill(vertexName+"_"+category+"_deltaPixelHits", -1, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_invMass", dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_pt", dimuonVertex->GetDimuonPt(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dEta", abs((float)muon1->Get("eta")-(float)muon2->Get("eta")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDEta", abs((float)muon1->Get("outerEta")-(float)muon2->Get("outerEta")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dPhi", abs((float)muon1->Get("phi")-(float)muon2->Get("phi")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDPhi", abs((float)muon1->Get("outerPhi")-(float)muon2->Get("outerPhi")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_chargeProduct", dimuonVertex->GetDimuonChargeProduct(), weight * muonWeight1 * muonWeight2);
    // if(dimuonVertex->GetDimuonChargeProduct() < 0) histogramsHandler->Fill(vertexName+"_"+category+"_OSinvMass", dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    // else histogramsHandler->Fill(vertexName+"_"+category+"_SSinvMass", dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    // float nTrackerLayers1 = 0; 
    // float nTrackerLayers2 = 0;
    // float nSegments1 = 0;
    // float nSegments2 = 0;
    // if(category=="Pat") {
    //   nTrackerLayers1 = muon1->Get("trkNumTrkLayers");
    //   nTrackerLayers2 = muon2->Get("trkNumTrkLayers");
    // }
    // if(category=="PatDSA") {
    //   nTrackerLayers1 = muon1->Get("trkNumTrkLayers");
    //   nSegments2 = muon2->Get("nSegments");
    // }
    // if(category=="DSA") {
    //   nSegments1 = muon1->Get("nSegments");
    //   nSegments2 = muon2->Get("nSegments");
    // }
    // histogramsHandler->Fill(vertexName+"_"+category+"_nTrackerLayers1", nTrackerLayers1, weight * muonWeight1 * muonWeight2);
    // histogramsHandler->Fill(vertexName+"_"+category+"_nTrackerLayers2", nTrackerLayers2, weight * muonWeight1 * muonWeight2);
    // histogramsHandler->Fill(vertexName+"_"+category+"_nSegments1", nSegments1, weight * muonWeight1 * muonWeight2);
    // histogramsHandler->Fill(vertexName+"_"+category+"_nSegments2", nSegments2, weight * muonWeight1 * muonWeight2);
    // histogramsHandler->Fill(vertexName+"_"+category+"_nSegmentsSum", nSegments1+nSegments2, weight * muonWeight1 * muonWeight2);

    // Isolations:
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso03Dimuon1", dimuonVertex->Get("displacedTrackIso03Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso04Dimuon1", dimuonVertex->Get("displacedTrackIso04Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso03Dimuon2", dimuonVertex->Get("displacedTrackIso03Dimuon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso04Dimuon2", dimuonVertex->Get("displacedTrackIso04Dimuon2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso03Muon1", dimuonVertex->Get("displacedTrackIso03Muon1"), weight * muonWeight1);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso04Muon1", dimuonVertex->Get("displacedTrackIso04Muon1"), weight * muonWeight1);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso03Muon2", dimuonVertex->Get("displacedTrackIso03Muon2"), weight * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso04Muon2", dimuonVertex->Get("displacedTrackIso04Muon2"), weight * muonWeight2);
    float pfRelIso04_all1 = 0;
    float pfRelIso04_all2 = 0;
    float tkRelIsoMuon1 = 0;
    float tkRelIsoMuon2 = 0;
    if(category=="Pat") {
      pfRelIso04_all1 = muon1->Get("pfRelIso04_all");
      pfRelIso04_all2 = muon2->Get("pfRelIso04_all");
      tkRelIsoMuon1 = muon1->Get("tkRelIso");
      tkRelIsoMuon2 = muon2->Get("tkRelIso");
    }
    if(category=="PatDSA") {
      pfRelIso04_all1 = muon1->Get("pfRelIso04_all");
      tkRelIsoMuon1 = muon1->Get("tkRelIso");
    }
    histogramsHandler->Fill(vertexName+"_"+category+"_pfRelIso04all1", pfRelIso04_all1, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_pfRelIso04all2", pfRelIso04_all2, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_tkRelIsoMuon1", tkRelIsoMuon1, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_tkRelIsoMuon2", tkRelIsoMuon2, weight * muonWeight1 * muonWeight2);

    // Muons in vertex variables:
    histogramsHandler->Fill(vertexName+"_"+category+"_leadingPt", max((float)muon1->Get("pt"),(float)muon2->Get("pt")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_subleadingPt", min((float)muon1->Get("pt"),(float)muon2->Get("pt")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dxyPVTraj1", muon1->Get("dxyPVTraj"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dxyPVTraj2", muon2->Get("dxyPVTraj"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_minDxyPVTraj", min((float)muon1->Get("dxyPVTraj"),(float)muon2->Get("dxyPVTraj")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_maxDxyPVTraj", max((float)muon1->Get("dxyPVTraj"),(float)muon2->Get("dxyPVTraj")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dxyPVTrajSig1", (float)muon1->Get("dxyPVTraj")/(float)muon1->Get("dxyPVTrajErr"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dxyPVTrajSig2", (float)muon2->Get("dxyPVTraj")/(float)muon2->Get("dxyPVTrajErr"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_minDxyPVTrajSig", min((float)muon1->Get("dxyPVTraj")/(float)muon1->Get("dxyPVTrajErr"),(float)muon2->Get("dxyPVTraj")/(float)muon2->Get("dxyPVTrajErr")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_maxDxyPVTrajSig", max((float)muon1->Get("dxyPVTraj")/(float)muon1->Get("dxyPVTrajErr"),(float)muon2->Get("dxyPVTraj")/(float)muon2->Get("dxyPVTrajErr")), weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_normChi2", dimuonVertex->Get("normChi2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_Lxy", dimuonVertex->GetLxyFromPV(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_dca", dimuonVertex->Get("dca"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_absCollinearityAngle", abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_invMass", dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_chargeProduct", dimuonVertex->GetDimuonChargeProduct(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_pt", dimuonVertex->GetDimuonPt(), weight * muonWeight1 * muonWeight2);

    if(category=="PatDSA") nPatDSA++;
    if(category=="Pat") nPat++;
    if(category=="DSA") nDSA++;

  }
  histogramsHandler->Fill("Event_n"+vertexName+"_PatDSA", nPatDSA, weight);
  histogramsHandler->Fill("Event_n"+vertexName+"_Pat", nPat, weight);
  histogramsHandler->Fill("Event_n"+vertexName+"_DSA", nDSA, weight);
}

void TTAlpsHistogramFiller::FillBasicMuonVertexHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  auto vertexCollection = event->GetCollection("GoodBestLooseMuonsVertex");
  
  for(auto vertex : *vertexCollection){
    auto dimuonVertex = asNanoDimuonVertex(vertex,event);
    shared_ptr<PhysicsObject> muon1  = dimuonVertex->Muon1();
    shared_ptr<PhysicsObject> muon2  = dimuonVertex->Muon2();
    float muonWeight1 = GetObjectWeight(muon1, "LooseMuons");
    float muonWeight2 = GetObjectWeight(muon2, "LooseMuons");
    
    string category = dimuonVertex->GetVertexCategory();
    
    histogramsHandler->Fill("GoodBestLooseMuonsVertex_"+category+"_normChi2", dimuonVertex->Get("normChi2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill("GoodBestLooseMuonsVertex_"+category+"_vxy", dimuonVertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill("GoodBestLooseMuonsVertex_"+category+"_vxySigma", dimuonVertex->Get("vxySigma"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill("GoodBestLooseMuonsVertex_"+category+"_vxySignificance", float(dimuonVertex->Get("vxy"))/float(dimuonVertex->Get("vxySigma")), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill("GoodBestLooseMuonsVertex_"+category+"_dca", dimuonVertex->Get("dca"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill("GoodBestLooseMuonsVertex_"+category+"_collinearityAngle", dimuonVertex->GetCollinearityAngle(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill("GoodBestLooseMuonsVertex_"+category+"_invMass", dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2); 
  }
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
      if(vertex) {
        if(float(vertex->Get("dRprox")) < minProxDeltaR) {
          minProxDeltaR = vertex->Get("dRprox");
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
    auto dimuonVertex = asNanoDimuonVertex(vertex,event);
    float muonWeight1 = GetObjectWeight(dimuonVertex->Muon1(), "LooseMuons");
    float muonWeight2 = GetObjectWeight(dimuonVertex->Muon2(), "LooseMuons");
    // float muonWeight1 = 1.;
    // float muonWeight2 = 1.;

    float vxySignificance = float(dimuonVertex->Get("vxy"))/float(dimuonVertex->Get("vxySigma"));
    float vxyzSignificance = float(dimuonVertex->Get("vxyz"))/float(dimuonVertex->Get("vxyzSigma"));

    string category = dimuonVertex->GetVertexCategory();
    
    histogramsHandler->Fill(vertexName+"_"+category+"_vxySigma_vxy", dimuonVertex->Get("vxySigma"), dimuonVertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxySigma_vxySignificance", dimuonVertex->Get("vxySigma"), vxySignificance, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_vxySignificance_vxy", vxySignificance, dimuonVertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_normChi2_vxy", dimuonVertex->Get("normChi2"), dimuonVertex->Get("vxy"), weight * muonWeight1 * muonWeight2);
  
    float nTrackerLayers1 = 0; 
    float nTrackerLayers2 = 0;
    if(category=="Pat") {
      nTrackerLayers1 = dimuonVertex->Muon1()->Get("trkNumTrkLayers");
      nTrackerLayers2 = dimuonVertex->Muon2()->Get("trkNumTrkLayers");
    }
    if(category=="PatDSA") nTrackerLayers1 = dimuonVertex->Muon1()->Get("trkNumTrkLayers");
    histogramsHandler->Fill(vertexName+"_"+category+"_Lxy_nTrackerLayers1", dimuonVertex->GetLxyFromPV(), nTrackerLayers1, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_Lxy_nTrackerLayers2", dimuonVertex->GetLxyFromPV(), nTrackerLayers2, weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_Lxy_maxTrackerLayers", dimuonVertex->GetLxyFromPV(), max(nTrackerLayers1,nTrackerLayers2), weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_"+category+"_absCollinearityAngle_invMass", abs(dimuonVertex->GetCollinearityAngle()), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_chargeProduct_invMass", dimuonVertex->GetDimuonChargeProduct(), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dEta_invMass", abs((float)dimuonVertex->Muon1()->Get("eta")-(float)dimuonVertex->Muon2()->Get("eta")), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDEta_invMass", abs((float)dimuonVertex->Muon1()->Get("outerEta")-(float)dimuonVertex->Muon2()->Get("outerEta")), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dR_invMass", dimuonVertex->Get("dR"), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDR_invMass", dimuonVertex->GetOuterDeltaR(), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso03Dimuon1_invMass", dimuonVertex->Get("displacedTrackIso03Dimuon1"), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso03Dimuon2_invMass", dimuonVertex->Get("displacedTrackIso03Dimuon2"), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso04Dimuon1_invMass", dimuonVertex->Get("displacedTrackIso04Dimuon1"), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_displacedTrackIso04Dimuon2_invMass", dimuonVertex->Get("displacedTrackIso04Dimuon2"), dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_"+category+"_dEta_displacedTrackIso03Dimuon1", abs((float)dimuonVertex->Muon1()->Get("eta")-(float)dimuonVertex->Muon2()->Get("eta")), dimuonVertex->Get("displacedTrackIso03Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDEta_displacedTrackIso03Dimuon1", abs((float)dimuonVertex->Muon1()->Get("outerEta")-(float)dimuonVertex->Muon2()->Get("outerEta")), dimuonVertex->Get("displacedTrackIso03Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dR_displacedTrackIso03Dimuon1", dimuonVertex->Get("dR"), dimuonVertex->Get("displacedTrackIso03Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDR_displacedTrackIso03Dimuon1", dimuonVertex->GetOuterDeltaR(), dimuonVertex->Get("displacedTrackIso03Dimuon1"), weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_"+category+"_dEta_absCollinearityAngle", abs((float)dimuonVertex->Muon1()->Get("eta")-(float)dimuonVertex->Muon2()->Get("eta")), abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDEta_absCollinearityAngle", abs((float)dimuonVertex->Muon1()->Get("outerEta")-(float)dimuonVertex->Muon2()->Get("outerEta")), abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_dR_absCollinearityAngle", dimuonVertex->Get("dR"), abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_outerDR_absCollinearityAngle", dimuonVertex->GetOuterDeltaR(), abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_proxDR_absCollinearityAngle", dimuonVertex->Get("dRprox"), abs(dimuonVertex->GetCollinearityAngle()), weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_"+category+"_absCollinearityAngle_displacedTrackIso03Dimuon1", abs(dimuonVertex->GetCollinearityAngle()), dimuonVertex->Get("displacedTrackIso03Dimuon1"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_absCollinearityAngle_Lxy", abs(dimuonVertex->GetCollinearityAngle()), dimuonVertex->GetLxyFromPV(), weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_"+category+"_absCollinearityAngle_normChi2", abs(dimuonVertex->GetCollinearityAngle()), dimuonVertex->Get("normChi2"), weight * muonWeight1 * muonWeight2);
    histogramsHandler->Fill(vertexName+"_"+category+"_absCollinearityAngle_chargeProduct", abs(dimuonVertex->GetCollinearityAngle()), dimuonVertex->GetDimuonChargeProduct(), weight * muonWeight1 * muonWeight2);

    histogramsHandler->Fill(vertexName+"_"+category+"_dca_normChi2", dimuonVertex->Get("dca"), dimuonVertex->Get("normChi2"), weight * muonWeight1 * muonWeight2);
  }
}

void TTAlpsHistogramFiller::FillDimuonHistograms(const shared_ptr<PhysicsObject> muon1, const shared_ptr<PhysicsObject> muon2, string collectionName, const shared_ptr<Event> event, bool genLevel) {
  float weight = GetEventWeight(event);
  
  auto pv_x = event->GetAsFloat("PV_x");
  auto pv_y = event->GetAsFloat("PV_y");
  auto pv_z = event->GetAsFloat("PV_z");

  TLorentzVector muon1fourVector;
  TLorentzVector muon2fourVector;
  float muon1Weight = 1;
  float muon2Weight = 1;
  float muonMass = 0.105;
  if(genLevel) {
    muon1fourVector = asNanoGenParticle(muon1)->GetFourVector(muonMass);
    muon2fourVector = asNanoGenParticle(muon2)->GetFourVector(muonMass);
  } else {
    muon1fourVector = asNanoMuon(muon1)->GetFourVector();
    muon2fourVector = asNanoMuon(muon2)->GetFourVector();
    muon1Weight = GetObjectWeight(muon1, "LooseMuons");
    muon2Weight = GetObjectWeight(muon2, "LooseMuons");
  }
  histogramsHandler->Fill(collectionName+"_invMass", (muon1fourVector+muon2fourVector).M(), weight * muon1Weight * muon2Weight);
  histogramsHandler->Fill(collectionName+"_deltaR", muon1fourVector.DeltaR(muon2fourVector), weight * muon1Weight * muon2Weight);
  if(!genLevel){
    float outerDeltaR = asNanoMuon(muon1)->OuterDeltaRtoMuon(asNanoMuon(muon2));
    histogramsHandler->Fill(collectionName+"_outerDeltaR", outerDeltaR, weight * muon1Weight * muon2Weight);
  }
  else {
    float Lx1 = (float)muon1->Get("vx") - pv_x;
    float Ly1 = (float)muon1->Get("vy") - pv_y;
    float Lz1 = (float)muon1->Get("vz") - pv_z;
    float Lxy1 = sqrt(Lx1*Lx1 + Ly1*Ly1);
    TVector3 Lxyz1(Lx1, Ly1, Lz1);
    histogramsHandler->Fill(collectionName+"_Lxy", Lxy1, weight);

    auto genParticles = event->GetCollection("GenPart");
    int motherIndex = asNanoGenParticle(muon1)->GetMotherIndex();
    auto genMother = asNanoGenParticle(genParticles->at(motherIndex));
    auto motherFourvector = genMother->GetFourVector(genMother->GetMass());
    float boost = float(genMother->GetPt()) / float(genMother->GetMass());
    // float boost_3D = motherFourvector.P() / float(genMother->GetMass());
    float boost_T = float(genMother->GetPt()) / motherFourvector.Mt();
    histogramsHandler->Fill(collectionName+"_properLxy",  Lxy1/boost, weight);

    TVector3 ptVector(muon1fourVector.Px()+muon2fourVector.Px(), muon1fourVector.Py()+muon2fourVector.Py(), muon1fourVector.Pz()+muon2fourVector.Pz());
    float absCollinearityAngle = ptVector.DeltaPhi(Lxyz1);
    histogramsHandler->Fill(collectionName+"_absCollinearityAngle", absCollinearityAngle, weight);
    
    TVector3 pt1Vector(muon1fourVector.Px(), muon1fourVector.Py(), muon1fourVector.Pz());
    TVector3 pt2Vector(muon2fourVector.Px(), muon2fourVector.Py(), muon2fourVector.Pz());
    float ptLxyDPhi1 = pt1Vector.DeltaPhi(Lxyz1);
    float ptLxyDPhi2 = pt2Vector.DeltaPhi(Lxyz1);
    histogramsHandler->Fill(collectionName+"_absPtLxyDPhi1", abs(ptLxyDPhi1), weight);
    histogramsHandler->Fill(collectionName+"_absPtLxyDPhi2", abs(ptLxyDPhi2), weight);
  }
}

/// Custom TTAlps Histograms - old reminent naming should probably be changed

void TTAlpsHistogramFiller::FillCustomTTAlpsVariables(const shared_ptr<Event> event) {
  for (auto &[histName, params] : ttalpsHistVariables) {
    if (params.variable == "subleadingPt") {
      FillAllSubLeadingPt(event, histName, params);
    } else if (params.variable == "leadingPt") {
      FillLeadingPt(event, histName, params);
    }
  }
  // FillDimuonHistograms(event);
  // FillDiumonClosestToZhistgrams(event);
  FillMuonMetHistograms(event);
  FillJetHistograms(event);
}

/// LLPnanoAOD Loose Muons and Loose Muon Vertex Histograms

void TTAlpsHistogramFiller::FillCustomTTAlpsVariablesFromLLPNanoAOD(const shared_ptr<Event> event) {
  FillLLPnanoAODLooseMuonsHistograms(event);
  FillLLPnanoAODLooseMuonsVertexHistograms(event);
  FillLLPnanoAODLooseMuonsNminus1VertexHistograms(event);
}

void TTAlpsHistogramFiller::FillLLPnanoAODLooseMuonsHistograms(const shared_ptr<Event> event){
  float weight = GetEventWeight(event);

  // FillLooseMuonsHistograms(event, "LooseMuons");
  // FillLooseMuonsHistograms(event, "LooseNonIsoMuons");
  // FillLooseMuonsHistograms(event, "LooseDSAMuons");

  for(auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    FillLooseMuonsHistograms(event, muonCollectionName);
    // FillMuonMinDeltaRHistograms(event, muonCollectionName);
    // auto DSAmuonCollection = asNanoEvent(event)->GetDSAMuonsFromCollection(muonCollectionName);
    // auto PATmuonCollection = asNanoEvent(event)->GetPATMuonsFromCollection(muonCollectionName);
    // string DSAmuonCollectionName = "LooseDSAMuons" + matchingMethod + "Match";
    // string PATmuonCollectionName = "LoosePATMuons" + matchingMethod + "Match";
    // FillLooseMuonsHistograms(DSAmuonCollection, DSAmuonCollectionName, weight);
    // FillLooseMuonsHistograms(PATmuonCollection, PATmuonCollectionName, weight);
  }
}

void TTAlpsHistogramFiller::FillLLPnanoAODLooseMuonsVertexHistograms(const shared_ptr<Event> event){
  float weight = GetEventWeight(event);

  for(auto &[matchingMethod, param] : muonMatchingParams) {
    string muonVertexCollectionName = "LooseMuonsVertex" + matchingMethod + "Match";
    FillMuonVertexHistograms(event,muonVertexCollectionName);
  }

  for(auto collectionName : muonVertexCollectionNames) {
    FillMuonVertexHistograms(event, collectionName);
  }

  // FillMuonVertexHistograms(event, "MaskedDimuonVertices");
  // FillMuonVertexHistograms(event, "GoodDimuonVertices");
  // FillMuonVertexHistograms(event, "GoodIsoDimuonVertices");
  // FillMuonVertexHistograms(event, "GoodIsoMaskedDimuonVertices");
  // FillMuonVertexHistograms(event, "GoodIsoMaskedDRDimuonVertices");
  // FillMuonVertexHistograms(event, "GoodMaskedDimuonVertices");
  // FillMuonVertexHistograms(event, "BestIsoDimuonVertex");
  // FillMuonVertexHistograms(event, "BestIsoMaskedDimuonVertex");
  // FillMuonVertexHistograms(event, "BestIsoMaskedDRDimuonVertex");
  // FillMuonVertexHistograms(event, "BestMaskedDimuonVertex");
}

void TTAlpsHistogramFiller::FillLLPnanoAODLooseMuonsNminus1VertexHistograms(const shared_ptr<Event> event){
  for(auto collectionName : muonVertexNminus1Collections) {
    FillMuonVertexHistograms(event, collectionName);
  }
}

/// LLPnanoAOD Muon Vertex 2D Histograms

void TTAlpsHistogramFiller::FillCustomTTAlps2DVariablesFromLLPNanoAOD(const shared_ptr<Event> event) {
  
  for(auto collectionName : muonVertexCollectionNames) {
    FillMuonVertexCorrelationHistograms(event, collectionName);
  }
}

/// Gen Muon Histograms

void TTAlpsHistogramFiller::FillCustomTTAlpsGenMuonVariables(const shared_ptr<Event> event) {
  FillGenALPsHistograms(event);
  FillGenMuonsFromALPsHistograms(event);
  FillGenMuonsNotFromALPsHistograms(event);
  FillLooseMuonsFromALPsHistograms(event);
  FillLooseMuonsNotFromALPsHistograms(event);
  FillLooseMuonsFromWsHistograms(event);
}

void TTAlpsHistogramFiller::FillGenALPsHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  auto genALPs = asTTAlpsEvent(event)->GetGenALPs();

  histogramsHandler->Fill("Event_nGenALP", genALPs->size(), weight);

  for (int i=0; i<genALPs->size(); i++) {    
    auto genALP = genALPs->at(i);
    int pdgId = genALP->Get("pdgId");
    histogramsHandler->Fill("GenALP_pdgId", pdgId, weight);
    histogramsHandler->Fill("GenALP_pt",    genALP->Get("pt"),    weight);
    histogramsHandler->Fill("GenALP_mass",  genALP->Get("mass"),  weight);
    histogramsHandler->Fill("GenALP_eta",   genALP->Get("eta"),   weight);
    histogramsHandler->Fill("GenALP_phi",   genALP->Get("phi"),   weight);
  }
}

void TTAlpsHistogramFiller::FillGenMuonMinDR(const shared_ptr<PhysicsObject> genMuon, const shared_ptr<Collection<shared_ptr<PhysicsObject> >> muonCollection, string genMuonCollectionName, string looseMuonCollectionName, float weight) {
  float muonMass = 0.105;
  TLorentzVector genMuonFourVector = asNanoGenParticle(genMuon)->GetFourVector(muonMass);
  float deltaRmin = 9999.;
  float muonWeightDR = 1;
  float deltaPhimin = 9999.;
  float muonWeightDPhi = 1;
  float deltaEtamin = 9999.;
  float muonWeightDEta = 1;
  for ( auto muon : *muonCollection ) {
    TLorentzVector muonFourVector = asNanoMuon(muon)->GetFourVector();
    if(genMuonFourVector.DeltaR(muonFourVector) < deltaRmin) {
      deltaRmin = genMuonFourVector.DeltaR(muonFourVector);
      muonWeightDR = GetObjectWeight(muon, "LooseMuons");
    }
    if(genMuonFourVector.DeltaPhi(muonFourVector) < deltaPhimin) {
      deltaPhimin = genMuonFourVector.DeltaPhi(muonFourVector);
      muonWeightDPhi = GetObjectWeight(muon, "LooseMuons");
    }
    float dEta = abs(genMuonFourVector.Eta() - muonFourVector.Eta());
    if(dEta < deltaEtamin) {
      deltaEtamin = dEta;
      muonWeightDEta = GetObjectWeight(muon, "LooseMuons");
    }
  }
  if(deltaRmin < 9999.) histogramsHandler->Fill(genMuonCollectionName+"_"+looseMuonCollectionName+"MinDR", deltaRmin, weight*muonWeightDR);
  if(deltaPhimin < 9999.) histogramsHandler->Fill(genMuonCollectionName+"_"+looseMuonCollectionName+"MinDPhi", deltaPhimin, weight*muonWeightDPhi);
  if(deltaEtamin < 9999.) histogramsHandler->Fill(genMuonCollectionName+"_"+looseMuonCollectionName+"MinDEta", deltaEtamin, weight *muonWeightDEta);
}

void TTAlpsHistogramFiller::FillGenMuonMinDR(const shared_ptr<PhysicsObject> genMuon, const shared_ptr<PhysicsObject> looseMuon, string genMuonCollectionName, string looseMuonCollectionName, float weight) {
  float muonMass = 0.105;
  TLorentzVector genMuonFourVector = asNanoGenParticle(genMuon)->GetFourVector(muonMass);
  TLorentzVector muonFourVector = asNanoMuon(looseMuon)->GetFourVector();
  float deltaRmin = genMuonFourVector.DeltaR(muonFourVector);
  float deltaPhimin = genMuonFourVector.DeltaPhi(muonFourVector);
  float deltaEtamin = abs(genMuonFourVector.Eta() - muonFourVector.Eta());
  float muonWeight = GetObjectWeight(looseMuon, "LooseMuons");
  histogramsHandler->Fill(genMuonCollectionName+"_"+looseMuonCollectionName+"MinDR", deltaRmin, weight*muonWeight);
  histogramsHandler->Fill(genMuonCollectionName+"_"+looseMuonCollectionName+"MinDPhi", deltaPhimin, weight*muonWeight);
  histogramsHandler->Fill(genMuonCollectionName+"_"+looseMuonCollectionName+"MinDEta", deltaEtamin, weight*muonWeight);
}

void TTAlpsHistogramFiller::FillGenMuonsFromALPsHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);
  float muonMass = 0.105;
  auto pv_x = event->GetAsFloat("PV_x");
  auto pv_y = event->GetAsFloat("PV_y");
  auto pv_z = event->GetAsFloat("PV_z");

  auto genMuonsFromALP = asTTAlpsEvent(event)->GetGenMuonsFromALP();
  auto genMuonsFromALPindices = asTTAlpsEvent(event)->GetGenMuonIndicesFromALP();
  string muonCollectionName = "LooseMuonsSegmentMatch";
  auto looseMatchedMuons = event->GetCollection(muonCollectionName);      
  auto looseMatchedMuonsFromALP = asTTAlpsEvent(event)->GetMuonsMatchedToGenMuonsFromALP(looseMatchedMuons);
  auto genParticles = event->GetCollection("GenPart");

  if(asTTAlpsEvent(event)->IsALPDecayWithinCMS()) return;

  histogramsHandler->Fill("Event_nGenMuonFromALP", genMuonsFromALP->size(), weight);
  if(genMuonsFromALP->size() > 1) {
    histogramsHandler->Fill("GenMuonFromALP_index1", genMuonsFromALPindices.at(0), weight);
    histogramsHandler->Fill("GenMuonFromALP_index2", genMuonsFromALPindices.at(1), weight);
  }
  int nGenDimuons = 0;

  for (int i=0; i<genMuonsFromALP->size(); i++)
  {    
    auto genMuon = genMuonsFromALP->at(i);
    TLorentzVector genMuon1fourVector = asNanoGenParticle(genMuon)->GetFourVector(muonMass);

    int pdgId = genMuon->Get("pdgId");
    histogramsHandler->Fill("GenMuonFromALP_pdgId",  pdgId,                  weight);
    histogramsHandler->Fill("GenMuonFromALP_pt",     genMuon->Get("pt"),     weight);
    histogramsHandler->Fill("GenMuonFromALP_mass",   genMuon->Get("mass"),   weight);
    histogramsHandler->Fill("GenMuonFromALP_eta",    genMuon->Get("eta"),    weight);
    histogramsHandler->Fill("GenMuonFromALP_phi",    genMuon->Get("phi"),    weight);
    float Lx = (float)genMuon->Get("vx") - pv_x;
    float Ly = (float)genMuon->Get("vy") - pv_y;
    float Lz = (float)genMuon->Get("vz") - pv_z;
    float Lxy = sqrt(Lx*Lx + Ly*Ly);
    float Lxyz = sqrt(Lx*Lx + Ly*Ly + Lz*Lz);
    histogramsHandler->Fill("GenMuonFromALP_Lxy",    Lxy,    weight);
    histogramsHandler->Fill("GenMuonFromALP_Lxyz",   Lxyz,   weight);

    float dxy = asNanoGenParticle(genMuon)->GetDxy(pv_x, pv_y);
    histogramsHandler->Fill("GenMuonFromALP_dxy", dxy, weight);

    int motherIndex = asNanoGenParticle(genMuon)->GetMotherIndex();
    auto genALP = asNanoGenParticle(genParticles->at(motherIndex));
    auto ALPfourvector = genALP->GetFourVector(genALP->GetMass());
    float ALPboost = float(genALP->GetPt()) / float(genALP->GetMass());
    float ALPboost_3D = ALPfourvector.P() / float(genALP->GetMass());
    float ALPboost_T = float(genALP->GetPt()) / ALPfourvector.Mt();
    histogramsHandler->Fill("GenMuonFromALP_properLxy",  Lxy/ALPboost, weight);
    histogramsHandler->Fill("GenMuonFromALP_properLxyT", Lxy/ALPboost_T, weight);
    histogramsHandler->Fill("GenMuonFromALP_properLxyz", Lxyz/ALPboost_3D, weight);

    auto motherIDs = asTTAlpsEvent(event)->GetFiveFirstMotherIDsOfParticle(genMuon);
    for(int j=0; j<motherIDs.size(); j++) {
      histogramsHandler->Fill("GenMuonFromALP_motherID"+to_string(j+1), motherIDs[j], weight);
    }
    for (int j = i+1; j<genMuonsFromALP->size(); j++)
    {
      if(j==i) continue;
      auto genMuon2 = genMuonsFromALP->at(j);
      TLorentzVector genMuon2fourVector = asNanoGenParticle(genMuon2)->GetFourVector(muonMass);
      FillDimuonHistograms(genMuon, genMuon2, "GenDimuonFromALP", event, true);
      nGenDimuons++;

      TVector3 ptVector(genMuon1fourVector.Px()+genMuon2fourVector.Px(), genMuon1fourVector.Py()+genMuon2fourVector.Py(), genMuon1fourVector.Pz()+genMuon2fourVector.Pz());
      TVector3 LxyzVector(Lx, Ly, Lz);
      float absCollinearityAngle = ptVector.DeltaPhi(LxyzVector);
      if(absCollinearityAngle > 2) FillDimuonHistograms(genMuon, genMuon2, "GenDimuonFromALPmindPhi2", event, true);
    }
  }
  histogramsHandler->Fill("Event_nGenDimuonFromALP", nGenDimuons, weight);  
}

void TTAlpsHistogramFiller::FillLooseMuonsFromALPsHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);
  float muonMass = 0.105;

  auto pv_x = event->GetAsFloat("PV_x");
  auto pv_y = event->GetAsFloat("PV_y");
  auto pv_z = event->GetAsFloat("PV_z");

  auto genMuonsFromALP = asTTAlpsEvent(event)->GetGenMuonsFromALP();
  auto genParticles = event->GetCollection("GenPart");

  if(asTTAlpsEvent(event)->IsALPDecayWithinCMS()) return;

  string category = asTTAlpsEvent(event)->GetTTbarEventCategory();
  bool hmuCategory = category == "hmu";

  for(auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    auto looseMatchedMuons = event->GetCollection(muonCollectionName);      
    auto tightMatchedMuons = asTTAlpsEvent(event)->GetTightMuonsInCollection(looseMatchedMuons);
    auto looseMatchedMuonsFromALP = asTTAlpsEvent(event)->GetMuonsMatchedToGenMuonsFromALP(looseMatchedMuons);
    auto tightMatchedMuonsFromALP = asTTAlpsEvent(event)->GetTightMuonsInCollection(looseMatchedMuonsFromALP);

    string muonFromALPsCollectionName = "LooseMuonsFromALP"+matchingMethod+"Match";
    string tightMuonFromALPsCollectionName = "TightMuonsFromALP"+matchingMethod+"Match";
    histogramsHandler->Fill("Event_n"+tightMuonFromALPsCollectionName, tightMatchedMuonsFromALP->size(), weight);
    if(hmuCategory) histogramsHandler->Fill("Event_n"+tightMuonFromALPsCollectionName+"_hmu", tightMatchedMuonsFromALP->size(), weight);

    if(looseMatchedMuonsFromALP->size() == 2) {
      float muon1Weight = GetObjectWeight(looseMatchedMuonsFromALP->at(0), "LooseMuons");
      float muon2Weight = GetObjectWeight(looseMatchedMuonsFromALP->at(1), "LooseMuons");
      FillLooseMuonsHistograms(looseMatchedMuonsFromALP,muonFromALPsCollectionName,weight);
      FillMuonMinDeltaRHistograms(event, looseMatchedMuonsFromALP, muonFromALPsCollectionName);
      FillGenMuonMinDR(genMuonsFromALP->at(0), looseMatchedMuonsFromALP->at(0), "GenMuonFromALP", "RecoMatch1", weight);
      FillGenMuonMinDR(genMuonsFromALP->at(1), looseMatchedMuonsFromALP->at(1), "GenMuonFromALP", "RecoMatch2", weight);
      FillDimuonHistograms(looseMatchedMuonsFromALP->at(0), looseMatchedMuonsFromALP->at(1), muonFromALPsCollectionName, event, false);
      
      for(int j=0; j<tightMatchedMuonsFromALP->size(); j++) {
        float muonWeight = GetObjectWeight(tightMatchedMuonsFromALP->at(j), "LooseMuons");
        
        histogramsHandler->Fill(tightMuonFromALPsCollectionName+"_index", tightMatchedMuonsFromALP->at(j)->Get("idx"), weight * muonWeight);
        histogramsHandler->Fill(tightMuonFromALPsCollectionName+"_pt", tightMatchedMuonsFromALP->at(j)->Get("pt"), weight * muonWeight);
        if(hmuCategory) {
          histogramsHandler->Fill(tightMuonFromALPsCollectionName+"_hmu_index", tightMatchedMuonsFromALP->at(j)->Get("idx"), weight * muonWeight);
          histogramsHandler->Fill(tightMuonFromALPsCollectionName+"_hmu_pt", tightMatchedMuonsFromALP->at(j)->Get("pt"), weight * muonWeight);
        }
      }
      
      auto dimuonVertex = asNanoEvent(event)->GetVertexForDimuon(looseMatchedMuonsFromALP->at(0),looseMatchedMuonsFromALP->at(1));
      string muonFromALPsVertexCollectionName = muonFromALPsCollectionName+"Vertex";
      if(dimuonVertex) {
        auto dimuonVertexCollection = make_shared<Collection<shared_ptr<PhysicsObject>>>();
        dimuonVertexCollection->push_back(dimuonVertex);
        FillMuonVertexHistograms(event,dimuonVertexCollection,muonFromALPsVertexCollectionName);
        auto nanoDimuonVertex = asNanoDimuonVertex(dimuonVertex,event);        
        float etaSum = abs((float)looseMatchedMuonsFromALP->at(0)->Get("eta")) + abs((float)looseMatchedMuonsFromALP->at(1)->Get("eta"));
        histogramsHandler->Fill(muonFromALPsVertexCollectionName+"_etaSum", etaSum, weight * muon1Weight * muon2Weight);

        float absCollinearityAngle = abs(nanoDimuonVertex->GetCollinearityAngle());
        if(absCollinearityAngle > 2) {
          muonFromALPsCollectionName = "LooseMuonsFromALPmindPhi2"+matchingMethod+"Match";
          muonFromALPsVertexCollectionName = muonFromALPsCollectionName+"Vertex";
          FillLooseMuonsHistograms(looseMatchedMuonsFromALP,muonFromALPsCollectionName,weight);
          FillDimuonHistograms(looseMatchedMuonsFromALP->at(0), looseMatchedMuonsFromALP->at(1), muonFromALPsCollectionName, event, false);
          FillMuonVertexHistograms(event,dimuonVertexCollection,muonFromALPsVertexCollectionName);
          histogramsHandler->Fill(muonFromALPsVertexCollectionName+"_etaSum", etaSum, weight * muon1Weight * muon2Weight);
        }
        else {
          string muonFromALPsCollectionNamedPhi = "LooseMuonsFromALPmaxdPhi2"+matchingMethod+"Match";
          string muonFromALPsVertexCollectionNamedPhi = muonFromALPsCollectionNamedPhi+"Vertex";
          histogramsHandler->Fill(muonFromALPsVertexCollectionNamedPhi+"_etaSum", etaSum, weight * muon1Weight * muon2Weight);
        }
        auto Lxyz = nanoDimuonVertex->GetLxyzFromPV();
        if(abs(Lxyz.X()) < 0.1) {
          int motherIndex = asNanoGenParticle(genMuonsFromALP->at(0))->GetMotherIndex();
          auto ALP = genParticles->at(motherIndex);
          float recoAngle = asTTAlpsEvent(event)->GetPhiAngleBetweenMuonsAndALP(looseMatchedMuonsFromALP->at(0), looseMatchedMuonsFromALP->at(1), ALP, true);
          float genAngle = asTTAlpsEvent(event)->GetPhiAngleBetweenMuonsAndALP(genMuonsFromALP->at(0), genMuonsFromALP->at(1), ALP, false);
          muonFromALPsVertexCollectionName = "LooseMuonsFromALP"+matchingMethod+"MatchVertex";
          histogramsHandler->Fill(muonFromALPsVertexCollectionName+"_genPlaneAngle", abs(genAngle), weight);
          histogramsHandler->Fill(muonFromALPsVertexCollectionName+"_recoPlaneAngle", abs(recoAngle), weight * muon1Weight * muon2Weight);
          if (absCollinearityAngle > 2) {
            muonFromALPsVertexCollectionName = "LooseMuonsFromALPmindPhi2"+matchingMethod+"MatchVertex";
            histogramsHandler->Fill(muonFromALPsVertexCollectionName+"_genPlaneAngle", abs(genAngle), weight);
            histogramsHandler->Fill(muonFromALPsVertexCollectionName+"_recoPlaneAngle", abs(recoAngle), weight * muon1Weight * muon2Weight);
          }
          else {
            muonFromALPsVertexCollectionName = "LooseMuonsFromALPmaxdPhi2"+matchingMethod+"MatchVertex";
            histogramsHandler->Fill(muonFromALPsVertexCollectionName+"_genPlaneAngle", abs(genAngle), weight);
            histogramsHandler->Fill(muonFromALPsVertexCollectionName+"_recoPlaneAngle", abs(recoAngle), weight * muon1Weight * muon2Weight);
          }
        }
      }
    }

    for ( auto looseMuon : *looseMatchedMuonsFromALP ) {
      float muonWeight = GetObjectWeight(looseMuon, "LooseMuons");
      float deltaRmin = 9999.0;
      TLorentzVector looseMuonFourVector = asNanoMuon(looseMuon)->GetFourVector();
      for ( auto genMuon : *genMuonsFromALP ) {
        TLorentzVector genMuonFourVector = asNanoGenParticle(genMuon)->GetFourVector(muonMass);
        if(genMuonFourVector.DeltaR(looseMuonFourVector) < deltaRmin) deltaRmin = genMuonFourVector.DeltaR(looseMuonFourVector);
      }
      histogramsHandler->Fill(muonFromALPsCollectionName+"_genMuonMinDR", deltaRmin, weight*muonWeight);
    }
    for ( auto genMuon : *genMuonsFromALP ) {
      FillGenMuonMinDR(genMuon, looseMatchedMuons, "GenMuonFromALP", muonCollectionName, weight);
    }
    int leadingLooseMuonFromALP = 0;
    if(asTTAlpsEvent(event)->IsLeadingMuonInCollection(looseMatchedMuonsFromALP, looseMatchedMuons)) leadingLooseMuonFromALP = 1;
    muonFromALPsCollectionName = "LooseMuonsFromALP"+matchingMethod+"Match";
    histogramsHandler->Fill(muonFromALPsCollectionName+"_hasLeadingMuon", leadingLooseMuonFromALP, weight);
    if(hmuCategory) {
      histogramsHandler->Fill(muonFromALPsCollectionName+"_hmu_hasLeadingMuon", leadingLooseMuonFromALP, weight);
    }
    
    int leadingTightMuonFromALP = 0;
    if(tightMatchedMuons->size() > 0 && tightMatchedMuonsFromALP->size() > 0) {
      if(asTTAlpsEvent(event)->IsLeadingMuonInCollection(tightMatchedMuonsFromALP, tightMatchedMuons)) leadingTightMuonFromALP = 1;
    }
    histogramsHandler->Fill(tightMuonFromALPsCollectionName+"_hasLeadingMuon", leadingTightMuonFromALP, weight);
    if(hmuCategory) histogramsHandler->Fill(tightMuonFromALPsCollectionName+"_hmu_hasLeadingMuon", leadingTightMuonFromALP, weight);
  }
}

void TTAlpsHistogramFiller::FillGenMuonsNotFromALPsHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);
  float muonMass = 0.105;

  string muonCollectionName = "LooseMuonsSegmentMatch";
  auto looseMatchedMuons = event->GetCollection(muonCollectionName);      
  auto genMuonsNotFromALP = asTTAlpsEvent(event)->GetGenMuonsNotFromALP();
  auto genDimuonsNotFromALP = asTTAlpsEvent(event)->GetGenDimuonsNotFromALP();

  if(asTTAlpsEvent(event)->IsALPDecayWithinCMS()) return;
  
  histogramsHandler->Fill("Event_nGenMuonNotFromALP", genMuonsNotFromALP->size(), weight);
  histogramsHandler->Fill("Event_nGenDimuonNotFromALP", genDimuonsNotFromALP->size(), weight);

  for (int i=0; i<genDimuonsNotFromALP->size(); i++){
    auto genMuon1 = genDimuonsNotFromALP->at(i).first;
    auto genMuon2 = genDimuonsNotFromALP->at(i).second;
    FillDimuonHistograms(genMuon1, genMuon2, "GenDimuonNotFromALP", event, true);
    auto motherIDs1 = asTTAlpsEvent(event)->GetFiveFirstMotherIDsOfParticle(genMuon1);
    auto motherIDs2 = asTTAlpsEvent(event)->GetFiveFirstMotherIDsOfParticle(genMuon2);
    for(int j=0; j<motherIDs1.size(); j++) {
      histogramsHandler->Fill("GenDimuonNotFromALP_motherID1"+to_string(j+1), motherIDs1[j], weight);
      histogramsHandler->Fill("GenDimuonNotFromALP_motherID2"+to_string(j+1), motherIDs2[j], weight);
    }
  }
  for (int i=0; i<genMuonsNotFromALP->size(); i++){
    auto genMuon1 = genMuonsNotFromALP->at(i);
    auto motherIDs1 = asTTAlpsEvent(event)->GetFiveFirstMotherIDsOfParticle(genMuon1);
    for(int j=0; j<motherIDs1.size(); j++) {
      histogramsHandler->Fill("GenMuonNotFromALP_motherID"+to_string(j+1), motherIDs1[j], weight);
    }
    for (int j=i+1; j<genMuonsNotFromALP->size(); j++){
      if(j==i) continue;
      auto genMuon2 = genMuonsNotFromALP->at(j);
      FillDimuonHistograms(genMuon1, genMuon2, "GenMuonNotFromALP", event, true);
    }
  }
}

void TTAlpsHistogramFiller::FillLooseMuonsNotFromALPsHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  if(asTTAlpsEvent(event)->IsALPDecayWithinCMS()) return;

  for(auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    auto looseMatchedMuons = event->GetCollection(muonCollectionName);      
    auto looseMatchedMuonsFromALP = asTTAlpsEvent(event)->GetMuonsMatchedToGenMuonsFromALP(looseMatchedMuons);
    auto looseMatchedMuonsNotFromALP = asTTAlpsEvent(event)->GetMuonsMatchedToGenMuonsNotFromALP(looseMatchedMuons); 
    auto looseMatchedDimuonsNotFromALP = asTTAlpsEvent(event)->GetMuonsMatchedToGenDimuonsNotFromALP(looseMatchedMuons); 
    auto looseMatchedDimuonsVertexNotFromALP = asNanoEvent(event)->GetVerticesForDimuons(looseMatchedDimuonsNotFromALP);

    auto looseMatchedResonantDimuons = looseMatchedDimuonsNotFromALP;
    auto looseMatchedDimuonsFromALP = make_shared<vector<pair<shared_ptr<PhysicsObject>,shared_ptr<PhysicsObject>>>>();
    if(looseMatchedMuonsFromALP->size() > 1) looseMatchedResonantDimuons->push_back(make_pair(looseMatchedMuonsFromALP->at(0),looseMatchedMuonsFromALP->at(1)));
    auto looseMatchedResonantDimuonsVertex= asNanoEvent(event)->GetVerticesForDimuons(looseMatchedResonantDimuons);
    auto looseMatchedNonResonantMuons = asTTAlpsEvent(event)->GetRemainingNonResonantMuons(looseMatchedMuons, looseMatchedResonantDimuons);
    auto looseMatchedNonResonantMuonsVertex = asNanoEvent(event)->GetVerticesForMuons(looseMatchedNonResonantMuons);

    string muonNotFromALPsCollectionName = "LooseMuonsNotFromALP"+matchingMethod+"Match";
    string muonNotFromALPsVertexCollectionName = "LooseMuonsNotFromALP"+matchingMethod+"MatchVertex";
    string dimuonNotFromALPsVertexCollectionName = "LooseDimuonsNotFromALP"+matchingMethod+"MatchVertex";
    FillLooseMuonsHistograms(looseMatchedMuonsNotFromALP,muonNotFromALPsCollectionName,weight);
    auto looseMatchedMuonsVerticesNotFromALP = asNanoEvent(event)->GetVerticesForMuons(looseMatchedMuonsNotFromALP);
    FillMuonVertexHistograms(event,looseMatchedMuonsVerticesNotFromALP,muonNotFromALPsVertexCollectionName);
    FillMuonVertexHistograms(event,looseMatchedDimuonsVertexNotFromALP,dimuonNotFromALPsVertexCollectionName);
  
    string nonresonantDimuonVertexCollectionName = "LooseNonResonantDimuons"+matchingMethod+"MatchVertex";
    FillMuonVertexHistograms(event,looseMatchedNonResonantMuonsVertex,nonresonantDimuonVertexCollectionName);
  }
}

void TTAlpsHistogramFiller::FillLooseMuonsFromWsHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);
  float muonMass = 0.105;

  auto genMuonsFromW = asTTAlpsEvent(event)->GetGenMuonsFromW();
  auto genMuonsFromW_indices = asTTAlpsEvent(event)->GetGenMuonIndicesFromW();
  auto genParticles = event->GetCollection("GenPart");
  histogramsHandler->Fill("Event_nGenMuonFromW", genMuonsFromW->size(), weight);
  if(genMuonsFromW_indices.size() > 0) {
    histogramsHandler->Fill("GenMuonFromW_index1", genMuonsFromW_indices.at(0), weight);
    if(genMuonsFromW_indices.size() > 1) {
      histogramsHandler->Fill("GenMuonFromW_index2", genMuonsFromW_indices.at(1), weight);
      if(genMuonsFromW_indices.size() > 2) histogramsHandler->Fill("GenMuonFromW_index3", genMuonsFromW_indices.at(2), weight);
    }
  }

  string category = asTTAlpsEvent(event)->GetTTbarEventCategory();
  bool hmuCategory = category == "hmu";

  for(auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    auto looseMatchedMuons = event->GetCollection(muonCollectionName);
    auto tightMatchedMuons = asTTAlpsEvent(event)->GetTightMuonsInCollection(looseMatchedMuons);

    auto looseMatchedMuonsFromW = asTTAlpsEvent(event)->GetLooseMuonsMatchedToGenMuons(genMuonsFromW, looseMatchedMuons, 0.01);
    auto tightMatchedMuonsFromW = asTTAlpsEvent(event)->GetTightMuonsInCollection(looseMatchedMuonsFromW);

    string muonFromWsCollectionName = "LooseMuonsFromW"+matchingMethod+"Match";
    string tightMuonFromWsCollectionName = "TightMuonsFromW"+matchingMethod+"Match";

    histogramsHandler->Fill("Event_n"+tightMuonFromWsCollectionName, tightMatchedMuonsFromW->size(), weight);
    if(hmuCategory) histogramsHandler->Fill("Event_n"+tightMuonFromWsCollectionName+"_hmu", tightMatchedMuonsFromW->size(), weight);

    int leadingLooseMuonFromW = 0;
    int leadingTightMuonFromW = 0;
    if(looseMatchedMuonsFromW->size() > 0) {
      FillLooseMuonsHistograms(looseMatchedMuonsFromW,muonFromWsCollectionName,weight);
      FillMuonMinDeltaRHistograms(event, looseMatchedMuonsFromW, muonFromWsCollectionName);
      FillGenMuonMinDR(genMuonsFromW->at(0), looseMatchedMuonsFromW->at(0), "GenMuonFromW", "RecoMatch1", weight);
      if(looseMatchedMuonsFromW->size() > 1) FillGenMuonMinDR(genMuonsFromW->at(1), looseMatchedMuonsFromW->at(1), "GenMuonFromW", "RecoMatch2", weight);
    
      if(asTTAlpsEvent(event)->IsLeadingMuonInCollection(looseMatchedMuonsFromW, looseMatchedMuons)) leadingLooseMuonFromW = 1;
      if(tightMatchedMuons->size() > 0 && tightMatchedMuonsFromW->size() > 0) {
        if(asTTAlpsEvent(event)->IsLeadingMuonInCollection(tightMatchedMuonsFromW, tightMatchedMuons)) leadingTightMuonFromW = 1;
        for(int j=0; j<tightMatchedMuonsFromW->size(); j++) {
          float muonWeight = GetObjectWeight(tightMatchedMuonsFromW->at(j), "LooseMuons");
          
          histogramsHandler->Fill(tightMuonFromWsCollectionName+"_index", tightMatchedMuonsFromW->at(j)->Get("idx"), weight * muonWeight);
          histogramsHandler->Fill(tightMuonFromWsCollectionName+"_pt", tightMatchedMuonsFromW->at(j)->Get("pt"), weight * muonWeight);
          if(hmuCategory) {
            histogramsHandler->Fill(tightMuonFromWsCollectionName+"_hmu_index", tightMatchedMuonsFromW->at(j)->Get("idx"), weight * muonWeight);
            histogramsHandler->Fill(tightMuonFromWsCollectionName+"_hmu_pt", tightMatchedMuonsFromW->at(j)->Get("pt"), weight * muonWeight);
          }
        }
      }
    }
    histogramsHandler->Fill(muonFromWsCollectionName+"_hasLeadingMuon", leadingLooseMuonFromW, weight);
    histogramsHandler->Fill(tightMuonFromWsCollectionName+"_hasLeadingMuon", leadingTightMuonFromW, weight);
    if(hmuCategory) {
      histogramsHandler->Fill(muonFromWsCollectionName+"_hmu_hasLeadingMuon", leadingLooseMuonFromW, weight);
      histogramsHandler->Fill(tightMuonFromWsCollectionName+"_hmu_hasLeadingMuon", leadingTightMuonFromW, weight);
    }
  }
}

/// Muon Matching Histograms

void TTAlpsHistogramFiller::FillCustomTTAlpsMuonMatchingVariables(const shared_ptr<Event> event) {
  FillMatchingHistograms(event, "LooseMuons", "LooseDSAMuons");
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

    histogramsHandler->Fill(dsaMuonCollection+"_nSegments", nSegments, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch1", dsaMuon->Get("muonMatch1"), weight * muonWeight);
    float ratio1 = float(dsaMuon->Get("muonMatch1")) / nSegments;
    histogramsHandler->Fill(dsaMuonCollection+"_matchRatio1", ratio1, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch2", dsaMuon->Get("muonMatch2"), weight * muonWeight);
    float ratio2 = float(dsaMuon->Get("muonMatch2")) / nSegments;
    histogramsHandler->Fill(dsaMuonCollection+"_matchRatio2", ratio2, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch1_nSegments", dsaMuon->Get("muonMatch1"), nSegments, weight*muonWeight*muonWeight);
    histogramsHandler->Fill(dsaMuonCollection+"_muonMatch2_nSegments", dsaMuon->Get("muonMatch2"), nSegments, weight*muonWeight*muonWeight);

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
      if(vertex) {
        float proxDR = vertex->Get("dRprox");
        histogramsHandler->Fill(dsaMuonCollection+"_PATProxDR", proxDR, weight*dsaMuonWeight*patMuonWeight);
      }
    }
  }
}

void TTAlpsHistogramFiller::FillMatchedMuonHistograms(const shared_ptr<PhysicsObject> muon, string muonCollectionName, float weight) {
  histogramsHandler->Fill(muonCollectionName+"_pt", muon->Get("pt"), weight);
  histogramsHandler->Fill(muonCollectionName+"_eta", muon->Get("eta"), weight);
  histogramsHandler->Fill(muonCollectionName+"_phi", muon->Get("phi"), weight);
  histogramsHandler->Fill(muonCollectionName+"_dxyPVTraj", muon->Get("dxyPVTraj"), weight);
  float dxyPVTrajSig = abs(float(muon->Get("dxyPVTraj")) / float(muon->Get("dxyPVTrajErr")));
  histogramsHandler->Fill(muonCollectionName+"_dxyPVTrajSig", dxyPVTrajSig, weight);
  histogramsHandler->Fill(muonCollectionName+"_ip3DPVSigned", muon->Get("ip3DPVSigned"), weight);
  float ip3DPVSignedSig = abs(float(muon->Get("ip3DPVSigned")) / float(muon->Get("ip3DPVSignedErr")));
  histogramsHandler->Fill(muonCollectionName+"_ip3DPVSignedSig", ip3DPVSignedSig, weight);
}

void TTAlpsHistogramFiller::FillDimuonCutFlows(const shared_ptr<CutFlowManager> cutFlowManager) {
  for(auto &[collectionName, vertexCuts] : muonVertexCollections) {
    int cutFlowLength = cutFlowManager->GetCutFlow(collectionName).size();
    string cutFlowName = "dimuonCutFlow_"+collectionName;
    string rawEventsCutFlowName = "rawEventsDimuonCutFlow_"+collectionName;
    auto cutFlowHist = new TH1D(cutFlowName.c_str(), cutFlowName.c_str(), cutFlowLength, 0, cutFlowLength);
    auto rawEventsCutFlowHist = new TH1D(rawEventsCutFlowName.c_str(), rawEventsCutFlowName.c_str(), cutFlowLength, 0, cutFlowLength);

    map<int, pair<string, float>> sortedWeightsAfterCuts;
    map<int, pair<string, float>> sortedRawEventsAfterCuts;
    auto cutFlow = cutFlowManager->GetCutFlow(collectionName);
    auto rawEventsCutFlow = cutFlowManager->GetRawEventsCutFlow(collectionName);
    for (auto& [cutName, sumOfWeights] : cutFlowManager->GetCutFlow(collectionName)) {
      string number = cutName.substr(0, cutName.find("_"));
      int index = stoi(number);
      sortedWeightsAfterCuts[index] = {cutName, sumOfWeights};
      sortedRawEventsAfterCuts[index] = {cutName, rawEventsCutFlow[cutName]};
    }

    int bin = 1;
    for (auto& [index, values] : sortedWeightsAfterCuts) {
      cutFlowHist->SetBinContent(bin, get<1>(values));
      rawEventsCutFlowHist->SetBinContent(bin, get<1>(sortedRawEventsAfterCuts[index]));
      cutFlowHist->GetXaxis()->SetBinLabel(bin, get<0>(values).c_str());
      rawEventsCutFlowHist->GetXaxis()->SetBinLabel(bin, get<0>(sortedRawEventsAfterCuts[index]).c_str());
      bin++;
    }
    histogramsHandler->SetHistogram1D(cutFlowName.c_str(), cutFlowHist);
    histogramsHandler->SetHistogram1D(rawEventsCutFlowName.c_str(), rawEventsCutFlowHist);
  }
}