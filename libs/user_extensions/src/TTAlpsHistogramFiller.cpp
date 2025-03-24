#include "TTAlpsHistogramFiller.hpp"

#include "ConfigManager.hpp"
#include "ExtensionsHelpers.hpp"
#include "TTAlpsCuts.hpp"
#include "UserExtensionsHelpers.hpp"

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
    config.GetMap("muonMatchingParams", muonMatchingParams);
  } catch (const Exception &e) {
    warn() << "Couldn't read muonMatchingParams from config file - no muon matching methods will be applied to muon collections" << endl;
  }
  try {
    config.GetPair("muonVertexCollection", muonVertexCollection);
  } catch (const Exception &e) {
    info() << "Couldn't read muonVertexCollection from config file - no muon vertex collection histograms will be filled" << endl;
  }
  try {
    config.GetValue("year", year);
  } catch (const Exception &e) {
    info() << "Couldn't read year from config file - will assume year 2018" << endl;
    year = "2018";
  }
}

TTAlpsHistogramFiller::~TTAlpsHistogramFiller() {}

/// --------- Help Functions--------- ///

float TTAlpsHistogramFiller::GetEventWeight(const shared_ptr<Event> event) {
  auto nanoEvent = asNanoEvent(event);

  float genWeight = nanoEventProcessor->GetGenWeight(nanoEvent);
  // change to "pileup" to use jsonPOG LUM values, or "custom" to use our own pileup distribution
  float pileupSF;
  if (year == "2018") {
    pileupSF = nanoEventProcessor->GetPileupScaleFactor(nanoEvent, "custom");  // TODO: do we want to use custom for all years?
  } else {
    pileupSF = nanoEventProcessor->GetPileupScaleFactor(nanoEvent, "pileup");
  }
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
    weight *= asNanoMuon(object)->GetScaleFactor("muonIDTight", "muonIsoTight", "muonReco", year);
  } else if (collectionName.rfind("LooseMuons", 0) == 0) {
    weight *= asNanoMuon(object)->GetScaleFactor("muonIDLoose", "muonIsoLoose", "muonReco", year);
  } else if (collectionName == "LoosePATMuons") {
    weight *= asNanoMuon(object)->GetScaleFactor("muonIDLoose", "muonIsoLoose", "muonReco", year);
  } else if (collectionName == "GoodTightBtaggedJets") {
    weight *= asNanoJet(object)->GetBtaggingScaleFactor("bTaggingTight");
  } else if (collectionName == "GoodMediumBtaggedJets") {
    weight *= asNanoJet(object)->GetBtaggingScaleFactor("bTaggingMedium");
  } else if (collectionName == "GoodJets") {
    weight *= asNanoJet(object)->GetPUJetIDScaleFactor("PUjetIDtight");
  } else {
    fatal() << "Unknown collection name " << collectionName << " in GetObjectWeight" << endl;
    exit(1);
  }

  return weight;
}

/// --------- Default Histograms --------- ///
/// ----- flag: runDefaultHistograms ----- ///

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
        value = event->GetAs<float>(branchName);
      }
      histogramsHandler->Fill(title, value, eventWeight);
    } else {
      auto collection = event->GetCollection(collectionName);
      if (branchName == "leadingPt") {
        auto object = eventProcessor->GetMaxPtObject(event, collectionName);
        if (!object) continue;
        value = object->GetAs<float>("pt");
        float objectWeight = GetObjectWeight(object, collectionName);
        histogramsHandler->Fill(title, value, eventWeight * objectWeight);
      }
      else if (branchName == "subleadingPt") {
        auto object = eventProcessor->GetSubleadingPtObject(event, collectionName);
        if (!object) continue;
        value = object->GetAs<float>("pt");
        float objectWeight = GetObjectWeight(object, collectionName);
        histogramsHandler->Fill(title, value, eventWeight * objectWeight);
      }
      else {
        for (auto object : *collection) {
          value = object->GetAs<float>(branchName);
          float objectWeight = GetObjectWeight(object, collectionName);
          histogramsHandler->Fill(title, value, eventWeight * objectWeight);
        }
      }
    }
  }
}

/// --------- NormCheck Histogram --------- ///

void TTAlpsHistogramFiller::FillNormCheck(const shared_ptr<Event> event) {
  float weight = nanoEventProcessor->GetGenWeight(asNanoEvent(event));
  histogramsHandler->Fill("Event_normCheck", 0.5, weight);
}

/// --------- LooseMuons Histograms --------- ///
/// ----- flag: runLLPNanoAODHistograms ----- ///

void TTAlpsHistogramFiller::FillCustomTTAlpsVariablesForLooseMuons(const shared_ptr<Event> event) {
  if (muonMatchingParams.empty()) return;

  float weight = GetEventWeight(event);

  for (auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    FillLooseMuonsHistograms(event, muonCollectionName);

    string muonVertexCollectionName = "LooseMuonsVertex" + matchingMethod + "Match";
    FillMuonVertexHistograms(event, muonVertexCollectionName);
  }
}

/// --------- Dimuon Vertex Collection Histograms --------- ///
/// ------------ flag: runLLPNanoAODHistograms ------------ ///

void TTAlpsHistogramFiller::FillCustomTTAlpsVariablesForMuonVertexCollections(const shared_ptr<Event> event) {
  if (muonVertexCollection.first.empty() && muonVertexCollection.second.empty()) return;
  
  float weight = GetEventWeight(event);

  string muonVertexCollectionName = muonVertexCollection.first;
  FillMuonVertexHistograms(event, muonVertexCollectionName);
  FillNminus1HistogramsForMuonVertexCollection(event);
}

void TTAlpsHistogramFiller::FillLooseMuonsHistograms(const shared_ptr<NanoMuons> muons, string collectionName, float weight) {
  float size = muons->size();
  histogramsHandler->Fill("Event_n" + collectionName, muons->size(), weight);

  for (auto muon : *muons) {
    float muonWeight = GetObjectWeight(muon->GetPhysicsObject(), "LooseMuons");

    histogramsHandler->Fill(collectionName + "_pt", muon->Get("pt"), weight * muonWeight);
    histogramsHandler->Fill(collectionName + "_eta", muon->Get("eta"), weight * muonWeight);
    histogramsHandler->Fill(collectionName + "_phi", muon->Get("phi"), weight * muonWeight);
    histogramsHandler->Fill(collectionName + "_dxy", muon->Get("dxy"), weight * muonWeight);

    int isPATMuon(0), isTightMuon(0);
    if (!muon->isDSA()) {
      histogramsHandler->Fill(collectionName + "_pfRelIso04all", muon->Get("pfRelIso04_all"), weight * muonWeight);
      isPATMuon = 1;
      if (muon->isTight()) isTightMuon = 1;
    }
    histogramsHandler->Fill(collectionName + "_isPAT", isPATMuon, weight * muonWeight);
    histogramsHandler->Fill(collectionName + "_isTight", isTightMuon, weight * muonWeight);
  }
}

void TTAlpsHistogramFiller::FillLooseMuonsHistograms(const shared_ptr<Event> event, string collectionName) {
  float weight = GetEventWeight(event);

  auto muons = asNanoMuons(event->GetCollection(collectionName));
  FillLooseMuonsHistograms(muons, collectionName, weight);
}

void TTAlpsHistogramFiller::FillMuonVertexHistograms(const shared_ptr<Event> event,
                                                     const shared_ptr<Collection<shared_ptr<PhysicsObject>>> vertexCollection,
                                                     string vertexName) {
  float weight = GetEventWeight(event);

  int nPatDSA = 0;
  int nPat = 0;
  int nDSA = 0;
  for (auto vertex : *vertexCollection) {
    auto dimuonVertex = asNanoDimuonVertex(vertex, event);
    auto muon1 = dimuonVertex->Muon1();
    auto muon2 = dimuonVertex->Muon2();
    float muonWeight1 = GetObjectWeight(muon1->GetPhysicsObject(), "LooseMuons");
    float muonWeight2 = GetObjectWeight(muon2->GetPhysicsObject(), "LooseMuons");

    string vertexCategory = dimuonVertex->GetVertexCategory();
    vector<string> categories = {"", "_" + vertexCategory};

    for (string category : categories) {
      histogramsHandler->Fill(vertexName + category + "_normChi2", dimuonVertex->Get("normChi2"), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_Lxy", dimuonVertex->GetLxyFromPV(), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_logLxy", log10(dimuonVertex->GetLxyFromPV()), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_LxySigma", dimuonVertex->GetLxySigmaFromPV(), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_LxySignificance", dimuonVertex->GetLxyFromPV() / dimuonVertex->GetLxySigmaFromPV(),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_dR", dimuonVertex->Get("dR"), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_proxDR", dimuonVertex->Get("dRprox"), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_outerDR", dimuonVertex->GetOuterDeltaR(), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_maxHitsInFrontOfVert",
                              max(float(dimuonVertex->Get("hitsInFrontOfVert1")), float(dimuonVertex->Get("hitsInFrontOfVert2"))),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_hitsInFrontOfVert1", dimuonVertex->Get("hitsInFrontOfVert1"), weight * muonWeight1);
      histogramsHandler->Fill(vertexName + category + "_hitsInFrontOfVert2", dimuonVertex->Get("hitsInFrontOfVert2"), weight * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_dca", dimuonVertex->Get("dca"), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_absCollinearityAngle", abs(dimuonVertex->GetCollinearityAngle()),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_absPtLxyDPhi1", abs(dimuonVertex->GetDPhiBetweenMuonpTAndLxy(1)),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_absPtLxyDPhi2", abs(dimuonVertex->GetDPhiBetweenMuonpTAndLxy(2)),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_invMass", dimuonVertex->GetInvariantMass(), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_logInvMass", log10(dimuonVertex->GetInvariantMass()),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_pt", dimuonVertex->GetDimuonPt(), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_eta", dimuonVertex->GetDimuonEta(), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_dEta", abs((float)muon1->Get("eta") - (float)muon2->Get("eta")),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_dPhi", abs((float)muon1->Get("phi") - (float)muon2->Get("phi")),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_chargeProduct", dimuonVertex->GetDimuonChargeProduct(),
                              weight * muonWeight1 * muonWeight2);

      histogramsHandler->Fill(vertexName + category + "_3Dangle", dimuonVertex->Get3DOpeningAngle(), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_cos3Dangle", dimuonVertex->GetCosine3DOpeningAngle(),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_nSegments", dimuonVertex->GetTotalNumberOfSegments(),
                              weight * muonWeight1 * muonWeight2);

      // Isolations:
      histogramsHandler->Fill(vertexName + category + "_displacedTrackIso03Dimuon1", dimuonVertex->Get("displacedTrackIso03Dimuon1"),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_displacedTrackIso04Dimuon1", dimuonVertex->Get("displacedTrackIso04Dimuon1"),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_displacedTrackIso03Dimuon2", dimuonVertex->Get("displacedTrackIso03Dimuon2"),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_displacedTrackIso04Dimuon2", dimuonVertex->Get("displacedTrackIso04Dimuon2"),
                              weight * muonWeight1 * muonWeight2);
      float pfRelIso04_all1(0), pfRelIso04_all2(0), nSegments1(0), nSegments2(0);
      if (category == "_Pat") {
        pfRelIso04_all1 = muon1->Get("pfRelIso04_all");
        pfRelIso04_all2 = muon2->Get("pfRelIso04_all");
      }
      if (category == "_PatDSA") {
        pfRelIso04_all1 = muon1->Get("pfRelIso04_all");
        nSegments2 = muon2->Get("nSegments");
      }
      if (category == "_DSA") {
        nSegments1 = muon1->Get("nSegments");
        nSegments2 = muon2->Get("nSegments");
      }
      histogramsHandler->Fill(vertexName + category + "_nSegments1", nSegments1, weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_nSegments2", nSegments2, weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_pfRelIso04all1", pfRelIso04_all1, weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_pfRelIso04all2", pfRelIso04_all2, weight * muonWeight1 * muonWeight2);

      // Muons in vertex variables:
      histogramsHandler->Fill(vertexName + category + "_leadingPt", max((float)muon1->Get("pt"), (float)muon2->Get("pt")),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_dxyPVTraj1", muon1->Get("dxyPVTraj"), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_dxyPVTraj2", muon2->Get("dxyPVTraj"), weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_dxyPVTrajSig1", (float)muon1->Get("dxyPVTraj") / (float)muon1->Get("dxyPVTrajErr"),
                              weight * muonWeight1 * muonWeight2);
      histogramsHandler->Fill(vertexName + category + "_dxyPVTrajSig2", (float)muon2->Get("dxyPVTraj") / (float)muon2->Get("dxyPVTrajErr"),
                              weight * muonWeight1 * muonWeight2);

      histogramsHandler->Fill(vertexName + category + "_log3Dangle_logLxySignificance", log10(dimuonVertex->Get3DOpeningAngle()),
                              log10(dimuonVertex->GetLxyFromPV() / dimuonVertex->GetLxySigmaFromPV()), weight * muonWeight1 * muonWeight2);
    }

    if (vertexCategory == "PatDSA") nPatDSA++;
    if (vertexCategory == "Pat") nPat++;
    if (vertexCategory == "DSA") nDSA++;
  }
  histogramsHandler->Fill("Event_n" + vertexName, vertexCollection->size(), weight);
  histogramsHandler->Fill("Event_n" + vertexName + "_PatDSA", nPatDSA, weight);
  histogramsHandler->Fill("Event_n" + vertexName + "_Pat", nPat, weight);
  histogramsHandler->Fill("Event_n" + vertexName + "_DSA", nDSA, weight);
}

void TTAlpsHistogramFiller::FillMuonVertexHistograms(const shared_ptr<Event> event, string vertexName) {
  auto vertexCollection = event->GetCollection(vertexName);
  FillMuonVertexHistograms(event, vertexCollection, vertexName);
}

void TTAlpsHistogramFiller::FillNminus1HistogramsForMuonVertexCollection(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  string collectionName = muonVertexCollection.first;
  auto collectionCuts = muonVertexCollection.second;

  for (auto cut : collectionCuts) {
    // Skip the BestDimuonVertex cut
    if (cut == "BestDimuonVertex") continue;

    string nminus1CollectionName = collectionName + "Nminus1" + cut;

    auto bestMuonVertex = event->GetCollection(nminus1CollectionName);
    if (bestMuonVertex->size() < 1) continue;
    if (bestMuonVertex->size() > 1) {
      warn() << "More than one vertex in collection: " << collectionName << ". Expected only one but the size is "
              << bestMuonVertex->size() << std::endl;
      continue;
    }
    auto dimuonVertex = asNanoDimuonVertex(bestMuonVertex->at(0), event);
    float muon1Weight = GetObjectWeight(dimuonVertex->Muon1()->GetPhysicsObject(), "LooseMuons");
    float muon2Weight = GetObjectWeight(dimuonVertex->Muon2()->GetPhysicsObject(), "LooseMuons");
    string nminus1HistogramsName = collectionName + "Nminus1";
    FillDimuonVertexNminus1HistogramForCut(nminus1HistogramsName, cut, dimuonVertex, weight * muon1Weight * muon2Weight);
    if (dimuonVertex->isDSAMuon1() && dimuonVertex->isDSAMuon2())
      nminus1HistogramsName = collectionName + "Nminus1_DSA";
    else if (!dimuonVertex->isDSAMuon1() && !dimuonVertex->isDSAMuon2())
      nminus1HistogramsName = collectionName + "Nminus1_Pat";
    else
      nminus1HistogramsName = collectionName + "Nminus1_PatDSA";
    FillDimuonVertexNminus1HistogramForCut(nminus1HistogramsName, cut, dimuonVertex, weight * muon1Weight * muon2Weight);
  }
}

void TTAlpsHistogramFiller::FillDimuonVertexNminus1HistogramForCut(string collectionName, string cut,
                                                                   shared_ptr<NanoDimuonVertex> dimuonVertex, float weight) {
  string histogramName = collectionName + "_" + cut;
  if (cut == "InvariantMassCut") {
    histogramsHandler->Fill(collectionName + "_invMass", dimuonVertex->GetInvariantMass(), weight);
    histogramsHandler->Fill(collectionName + "_logInvMass", log10(dimuonVertex->GetInvariantMass()), weight);
  }
  if (cut == "ChargeCut") histogramsHandler->Fill(collectionName + "_chargeProduct", dimuonVertex->GetDimuonChargeProduct(), weight);
  if (cut == "HitsInFrontOfVertexCut")
    histogramsHandler->Fill(collectionName + "_maxHitsInFrontOfVert",
                            max(float(dimuonVertex->Get("hitsInFrontOfVert1")), float(dimuonVertex->Get("hitsInFrontOfVert2"))), weight);
  if (cut == "DPhiBetweenMuonpTAndLxyCut") {
    if (!dimuonVertex->isDSAMuon1())
      histogramsHandler->Fill(collectionName + "_absPtLxyDPhi1", abs(dimuonVertex->GetDPhiBetweenMuonpTAndLxy(1)), weight);
  }
  if (cut == "DCACut") histogramsHandler->Fill(collectionName + "_dca", dimuonVertex->Get("dca"), weight);
  if (cut == "CollinearityAngleCut")
    histogramsHandler->Fill(collectionName + "_absCollinearityAngle", abs(dimuonVertex->GetCollinearityAngle()), weight);
  if (cut == "Chi2Cut") histogramsHandler->Fill(collectionName + "_normChi2", dimuonVertex->Get("normChi2"), weight);
  if (cut == "DisplacedIsolationCut" || cut == "PFRelIsolationCut") {
    histogramsHandler->Fill(collectionName + "_displacedTrackIso03Dimuon1", dimuonVertex->Get("displacedTrackIso03Dimuon1"), weight);
    histogramsHandler->Fill(collectionName + "_displacedTrackIso03Dimuon2", dimuonVertex->Get("displacedTrackIso03Dimuon2"), weight);
    if (!dimuonVertex->isDSAMuon1())
      histogramsHandler->Fill(collectionName + "_pfRelIso1", dimuonVertex->Muon1()->Get("pfRelIso04_all"), weight);
    if (!dimuonVertex->isDSAMuon2())
      histogramsHandler->Fill(collectionName + "_pfRelIso2", dimuonVertex->Muon2()->Get("pfRelIso04_all"), weight);
  }
  if (cut == "LxyCut") histogramsHandler->Fill(collectionName + "_Lxy", dimuonVertex->GetLxyFromPV(), weight);
  if (cut == "DeltaEtaCut") {
    histogramsHandler->Fill(collectionName + "_DeltaEta", abs(dimuonVertex->GetDeltaEta()), weight);
    histogramsHandler->Fill(collectionName + "_OuterDeltaEta", abs(dimuonVertex->GetOuterDeltaEta()), weight);
  }
  if (cut == "DeltaPhiCut") {
    histogramsHandler->Fill(collectionName + "_DeltaPhi", abs(dimuonVertex->GetDeltaPhi()), weight);
    histogramsHandler->Fill(collectionName + "_OuterDeltaPhi", abs(dimuonVertex->GetOuterDeltaPhi()), weight);
  }
  if (cut == "DeltaRCut") {
    histogramsHandler->Fill(collectionName + "_DeltaR", dimuonVertex->Get("dR"), weight);
    histogramsHandler->Fill(collectionName + "_OuterDeltaR", dimuonVertex->GetOuterDeltaR(), weight);
    histogramsHandler->Fill(collectionName + "_ProxDeltaR", dimuonVertex->Get("dRprox"), weight);
  }
  if (cut == "DeltaPixelHitsCut") histogramsHandler->Fill(collectionName + "_DeltaPixelHits", dimuonVertex->GetDeltaPixelHits(), weight);
  if (cut == "BarrelDeltaEtaCut") {
    histogramsHandler->Fill(collectionName + "_dimuonEta", dimuonVertex->GetDimuonEta(), weight);
    histogramsHandler->Fill(collectionName + "_DeltaEta", abs(dimuonVertex->GetDeltaEta()), weight);
  }
  if (cut.find("LogLxy") != string::npos) histogramsHandler->Fill(collectionName + "_LogLxy", log(dimuonVertex->GetLxyFromPV()), weight);
}

/// --------- Gen-Level Muon Histograms --------- ///
/// -------- flag: runGenMuonHistograms --------- ///

void TTAlpsHistogramFiller::FillCustomTTAlpsGenMuonVariables(const shared_ptr<Event> event) {
  FillGenALPsHistograms(event);
  FillGenDimuonResonancesHistograms(event);
  FillGenMatchedLooseMuonsHistograms(event);
  FillLooseMuonsFromWsHistograms(event);
}

void TTAlpsHistogramFiller::FillGenALPsHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  auto genALPs = asTTAlpsEvent(event)->GetGenALPs();

  histogramsHandler->Fill("Event_nGenALP", genALPs->size(), weight);

  for (int i = 0; i < genALPs->size(); i++) {
    auto genALP = genALPs->at(i);
    int pdgId = genALP->Get("pdgId");
    histogramsHandler->Fill("GenALP_pdgId", pdgId, weight);
    histogramsHandler->Fill("GenALP_pt", genALP->Get("pt"), weight);
    histogramsHandler->Fill("GenALP_mass", genALP->Get("mass"), weight);
    histogramsHandler->Fill("GenALP_eta", genALP->Get("eta"), weight);
    histogramsHandler->Fill("GenALP_phi", genALP->Get("phi"), weight);
  }
}

void TTAlpsHistogramFiller::FillGenDimuonResonancesHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);
  auto pv_x = event->GetAs<float>("PV_x");
  auto pv_y = event->GetAs<float>("PV_y");
  auto pv_z = event->GetAs<float>("PV_z");

  // Gen Dimuon from ALP
  auto genDimuonFromALP = asTTAlpsEvent(event)->GetGenDimuonFromALP();
  auto genDimuonFromALPindices = asTTAlpsEvent(event)->GetGenMuonIndicesFromALP();
  auto genParticles = event->GetCollection("GenPart");

  if (!asTTAlpsEvent(event)->IsALPDecayWithinCMS()) return;

  if (genDimuonFromALP) {
    histogramsHandler->Fill("GenDimuonFromALP_index1", genDimuonFromALPindices.at(0), weight);
    histogramsHandler->Fill("GenDimuonFromALP_index2", genDimuonFromALPindices.at(1), weight);

    histogramsHandler->Fill("Event_nGenDimuonFromALP", 1, weight);
    auto genMuon1 = genDimuonFromALP->first;
    auto genMuon2 = genDimuonFromALP->second;
    TLorentzVector genMuon1fourVector = asNanoGenParticle(genMuon1)->GetFourVector(muonMass);
    TLorentzVector genMuon2fourVector = asNanoGenParticle(genMuon2)->GetFourVector(muonMass);

    FillGenDimuonHistograms(genDimuonFromALP, "GenDimuonFromALP", event);
  }
  // Not from ALPs
  auto genMuonsNotFromALP = asTTAlpsEvent(event)->GetGenMuonsNotFromALP();
  auto genDimuonResonancesNotFromALP = asTTAlpsEvent(event)->GetGenDimuonsNotFromALP();
  histogramsHandler->Fill("Event_nGenDimuonsNonresonancesNotFromALP", genMuonsNotFromALP->size(), weight);
  histogramsHandler->Fill("Event_nGenDimuonResonancesNotFromALP", genDimuonResonancesNotFromALP->size(), weight);

  // Muon Pair resonances
  for (auto genDimuon : *genDimuonResonancesNotFromALP) {
    FillGenDimuonHistograms(make_shared<MuonPair>(genDimuon.first, genDimuon.second), "GenDimuonResonancesNotFromALP", event);
  }
  // All muon pair combinations
  for (int i = 0; i < genMuonsNotFromALP->size(); i++) {
    for (int j = i + 1; j < genMuonsNotFromALP->size(); j++) {
      if (j == i) continue;
      auto genMuonPair = make_shared<MuonPair>(genMuonsNotFromALP->at(i), genMuonsNotFromALP->at(j));
      FillGenDimuonHistograms(genMuonPair, "GenDimuonsNonresonancesNotFromALP", event);
    }
  }
}

  void TTAlpsHistogramFiller::FillGenMatchedLooseMuonsHistograms(const shared_ptr<Event> event) {
  if (muonMatchingParams.empty()) return;
  
  float weight = GetEventWeight(event);

  auto pv_x = event->GetAs<float>("PV_x");
  auto pv_y = event->GetAs<float>("PV_y");
  auto pv_z = event->GetAs<float>("PV_z");

  auto genDimuonFromALP = asTTAlpsEvent(event)->GetGenDimuonFromALP();
  auto genParticles = event->GetCollection("GenPart");

  if (!asTTAlpsEvent(event)->IsALPDecayWithinCMS()) return;

  auto ttAlpsEvent = asTTAlpsEvent(event);

  string category = ttAlpsEvent->GetTTbarEventCategory();
  bool hmuCategory = category == "hmu";

  for (auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    string muonVertexCollectionName = "LooseMuonsVertex" + matchingMethod + "Match";

    auto looseMuons = asNanoMuons(event->GetCollection(muonCollectionName));
    auto tightMuons = ttAlpsEvent->GetTightMuonsInCollection(looseMuons);

    FillRecoGenMatchedResonanceHistograms(event, looseMuons, muonVertexCollectionName);

    auto looseDimuonFromALP = ttAlpsEvent->GetDimuonMatchedToGenMuonsFromALP(looseMuons);
    // string looseMuonVertexFromALPsName = "LooseMuonsVertex" + matchingMethod + "MatchFromALP";
    string looseMuonFromALPsName = "LooseMuons" + matchingMethod + "MatchFromALP";
    string tightMuonFromALPsName = "TightMuons" + matchingMethod + "MatchFromALP";

    if (!looseDimuonFromALP) continue;

    if (genDimuonFromALP) {
      FillGenMuonMinDRHistograms(genDimuonFromALP->first, looseMuons, "GenDimuonFromALP1", muonCollectionName, weight);
      FillGenMuonMinDRHistograms(genDimuonFromALP->second, looseMuons, "GenDimuonFromALP2", muonCollectionName, weight);
      auto looseDimuonFromALPCollection = make_shared<NanoMuons>();
      looseDimuonFromALPCollection->push_back(looseDimuonFromALP->first);
      FillGenMuonMinDRHistograms(genDimuonFromALP->first, looseDimuonFromALPCollection, "GenDimuonFromALP1", muonCollectionName + "Final",
                                 weight);
      looseDimuonFromALPCollection->at(0) = looseDimuonFromALP->second;
      FillGenMuonMinDRHistograms(genDimuonFromALP->second, looseDimuonFromALPCollection, "GenDimuonFromALP2", muonCollectionName + "Final",
                                 weight);
    }

    // Tight leading muon from ALP study
    auto looseMuonsFromALPCollection = std::make_shared<NanoMuons>();
    looseMuonsFromALPCollection->push_back(looseDimuonFromALP->first);
    looseMuonsFromALPCollection->push_back(looseDimuonFromALP->second);
    auto tightMuonsFromALP = ttAlpsEvent->GetTightMuonsInCollection(looseMuonsFromALPCollection);
    histogramsHandler->Fill("Event_n" + tightMuonFromALPsName, tightMuonsFromALP->size(), weight);
    if (hmuCategory) histogramsHandler->Fill("Event_n" + tightMuonFromALPsName + "_hmu", tightMuonsFromALP->size(), weight);
    for (int j = 0; j < tightMuonsFromALP->size(); j++) {
      float muonWeight = GetObjectWeight(tightMuonsFromALP->at(j)->GetPhysicsObject(), "TightMuons");
      histogramsHandler->Fill(tightMuonFromALPsName + "_index", tightMuonsFromALP->at(j)->Get("idx"), weight * muonWeight);
      histogramsHandler->Fill(tightMuonFromALPsName + "_pt", tightMuonsFromALP->at(j)->Get("pt"), weight * muonWeight);
      if (hmuCategory) {
        histogramsHandler->Fill(tightMuonFromALPsName + "_hmu_index", tightMuonsFromALP->at(j)->Get("idx"), weight * muonWeight);
        histogramsHandler->Fill(tightMuonFromALPsName + "_hmu_pt", tightMuonsFromALP->at(j)->Get("pt"), weight * muonWeight);
      }
    }
    int leadingLooseMuonFromALP = 0;
    if (ttAlpsEvent->IsLeadingMuonInCollection(looseMuonsFromALPCollection, looseMuons)) leadingLooseMuonFromALP = 1;
    histogramsHandler->Fill(looseMuonFromALPsName + "_hasLeadingMuon", leadingLooseMuonFromALP, weight);
    if (hmuCategory) {
      histogramsHandler->Fill(looseMuonFromALPsName + "_hmu_hasLeadingMuon", leadingLooseMuonFromALP, weight);
    }
    int leadingTightMuonFromALP = 0;
    if (tightMuons->size() > 0 && tightMuonsFromALP->size() > 0) {
      if (ttAlpsEvent->IsLeadingMuonInCollection(tightMuonsFromALP, tightMuons)) leadingTightMuonFromALP = 1;
    }
    histogramsHandler->Fill(tightMuonFromALPsName + "_hasLeadingMuon", leadingTightMuonFromALP, weight);
    if (hmuCategory) histogramsHandler->Fill(tightMuonFromALPsName + "_hmu_hasLeadingMuon", leadingTightMuonFromALP, weight);
  }
}

void TTAlpsHistogramFiller::FillLooseMuonsFromWsHistograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  auto genMuonsFromW = asTTAlpsEvent(event)->GetGenMuonsFromW();
  auto genMuonsFromW_indices = asTTAlpsEvent(event)->GetGenMuonIndicesFromW();
  auto genParticles = event->GetCollection("GenPart");
  histogramsHandler->Fill("Event_nGenMuonFromW", genMuonsFromW->size(), weight);
  if (genMuonsFromW_indices.size() > 0) {
    histogramsHandler->Fill("GenMuonFromW_index1", genMuonsFromW_indices.at(0), weight);
    if (genMuonsFromW_indices.size() > 1) {
      histogramsHandler->Fill("GenMuonFromW_index2", genMuonsFromW_indices.at(1), weight);
      if (genMuonsFromW_indices.size() > 2) histogramsHandler->Fill("GenMuonFromW_index3", genMuonsFromW_indices.at(2), weight);
    }
  }
  auto ttAlpsEvent = asTTAlpsEvent(event);
  string category = ttAlpsEvent->GetTTbarEventCategory();
  bool hmuCategory = category == "hmu";

  for (auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    auto looseMuons = asNanoMuons(event->GetCollection(muonCollectionName));
    auto tightMuons = ttAlpsEvent->GetTightMuonsInCollection(looseMuons);

    auto looseMuonsFromW = ttAlpsEvent->GetLooseMuonsMatchedToGenMuons(genMuonsFromW, looseMuons, 0.01);
    auto tightMuonsFromW = ttAlpsEvent->GetTightMuonsInCollection(looseMuonsFromW);

    string muonFromWsCollectionName = "LooseMuons" + matchingMethod + "MatchFromW";
    string tightMuonFromWsCollectionName = "TightMuons" + matchingMethod + "MatchFromW";

    histogramsHandler->Fill("Event_n" + tightMuonFromWsCollectionName, tightMuonsFromW->size(), weight);
    if (hmuCategory) histogramsHandler->Fill("Event_n" + tightMuonFromWsCollectionName + "_hmu", tightMuonsFromW->size(), weight);

    int leadingLooseMuonFromW = 0;
    int leadingTightMuonFromW = 0;
    if (looseMuonsFromW->size() > 0) {
      FillLooseMuonsHistograms(looseMuonsFromW, muonFromWsCollectionName, weight);
      auto looseMuonsFromWCollection = make_shared<NanoMuons>();
      looseMuonsFromWCollection->push_back(looseMuonsFromW->at(0));

      FillGenMuonMinDRHistograms(genMuonsFromW->at(0), looseMuonsFromWCollection, "GenMuonFromW1", muonCollectionName + "Final", weight);
      if (looseMuonsFromW->size() > 1) {
        looseMuonsFromWCollection->at(0) = looseMuonsFromW->at(1);
        FillGenMuonMinDRHistograms(genMuonsFromW->at(1), looseMuonsFromWCollection, "GenMuonFromW2", muonCollectionName + "Final", weight);
      }
      if (ttAlpsEvent->IsLeadingMuonInCollection(looseMuonsFromW, looseMuons)) leadingLooseMuonFromW = 1;
      if (tightMuons->size() > 0 && tightMuonsFromW->size() > 0) {
        if (ttAlpsEvent->IsLeadingMuonInCollection(tightMuonsFromW, tightMuons)) leadingTightMuonFromW = 1;
        for (int j = 0; j < tightMuonsFromW->size(); j++) {
          float muonWeight = GetObjectWeight(tightMuonsFromW->at(j)->GetPhysicsObject(), "LooseMuons");

          histogramsHandler->Fill(tightMuonFromWsCollectionName + "_index", tightMuonsFromW->at(j)->Get("idx"), weight * muonWeight);
          histogramsHandler->Fill(tightMuonFromWsCollectionName + "_pt", tightMuonsFromW->at(j)->Get("pt"), weight * muonWeight);
          if (hmuCategory) {
            histogramsHandler->Fill(tightMuonFromWsCollectionName + "_hmu_index", tightMuonsFromW->at(j)->Get("idx"), weight * muonWeight);
            histogramsHandler->Fill(tightMuonFromWsCollectionName + "_hmu_pt", tightMuonsFromW->at(j)->Get("pt"), weight * muonWeight);
          }
        }
      }
    }
    histogramsHandler->Fill(muonFromWsCollectionName + "_hasLeadingMuon", leadingLooseMuonFromW, weight);
    histogramsHandler->Fill(tightMuonFromWsCollectionName + "_hasLeadingMuon", leadingTightMuonFromW, weight);
    if (hmuCategory) {
      histogramsHandler->Fill(muonFromWsCollectionName + "_hmu_hasLeadingMuon", leadingLooseMuonFromW, weight);
      histogramsHandler->Fill(tightMuonFromWsCollectionName + "_hmu_hasLeadingMuon", leadingTightMuonFromW, weight);
    }
  }
}

void TTAlpsHistogramFiller::FillGenDimuonHistograms(shared_ptr<MuonPair> muonPair, string collectionName, const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  auto pv_x = event->GetAs<float>("PV_x");
  auto pv_y = event->GetAs<float>("PV_y");
  auto pv_z = event->GetAs<float>("PV_z");

  auto muon1 = muonPair->first;
  auto muon2 = muonPair->second;
  float muon1Weight = 1;
  float muon2Weight = 1;
  TLorentzVector muon1fourVector = asNanoGenParticle(muon1)->GetFourVector(muonMass);
  TLorentzVector muon2fourVector = asNanoGenParticle(muon2)->GetFourVector(muonMass);

  histogramsHandler->Fill(collectionName + "_invMass", (muon1fourVector + muon2fourVector).M(), weight * muon1Weight * muon2Weight);
  histogramsHandler->Fill(collectionName + "_logInvMass", log10((muon1fourVector + muon2fourVector).M()),
                          weight * muon1Weight * muon2Weight);
  histogramsHandler->Fill(collectionName + "_deltaR", muon1fourVector.DeltaR(muon2fourVector), weight * muon1Weight * muon2Weight);

  float Lx1 = (float)muon1->Get("vx") - pv_x;
  float Ly1 = (float)muon1->Get("vy") - pv_y;
  float Lz1 = (float)muon1->Get("vz") - pv_z;
  float Lxy1 = sqrt(Lx1 * Lx1 + Ly1 * Ly1);
  TVector3 Lxyz1(Lx1, Ly1, Lz1);
  histogramsHandler->Fill(collectionName + "_Lxy", Lxy1, weight);
  histogramsHandler->Fill(collectionName + "_logLxy", log10(Lxy1), weight);

  auto genParticles = event->GetCollection("GenPart");
  auto genMother = asNanoGenParticle(genParticles->at(asNanoGenParticle(muon1)->GetMotherIndex()));
  float boost = float(genMother->GetPt()) / float(genMother->GetMass());
  histogramsHandler->Fill(collectionName + "_properLxy", Lxy1 / boost, weight);

  auto motherIDs1 = asTTAlpsEvent(event)->GetFiveFirstMotherIDsOfParticle(muon1);
  auto motherIDs2 = asTTAlpsEvent(event)->GetFiveFirstMotherIDsOfParticle(muon2);
  for (int j = 0; j < motherIDs1.size(); j++) {
    histogramsHandler->Fill(collectionName + "_motherID1" + to_string(j + 1), motherIDs1[j], weight);
    histogramsHandler->Fill(collectionName + "_motherID2" + to_string(j + 1), motherIDs2[j], weight);
  }

  TVector3 ptVector(muon1fourVector.Px() + muon2fourVector.Px(), muon1fourVector.Py() + muon2fourVector.Py(),
                    muon1fourVector.Pz() + muon2fourVector.Pz());
  float absCollinearityAngle = ptVector.DeltaPhi(Lxyz1);
  histogramsHandler->Fill(collectionName + "_absCollinearityAngle", absCollinearityAngle, weight);

  TVector3 pt1Vector(muon1fourVector.Px(), muon1fourVector.Py(), muon1fourVector.Pz());
  TVector3 pt2Vector(muon2fourVector.Px(), muon2fourVector.Py(), muon2fourVector.Pz());
  float ptLxyDPhi1 = pt1Vector.DeltaPhi(Lxyz1);
  float ptLxyDPhi2 = pt2Vector.DeltaPhi(Lxyz1);
  histogramsHandler->Fill(collectionName + "_absPtLxyDPhi1", abs(ptLxyDPhi1), weight);
  histogramsHandler->Fill(collectionName + "_absPtLxyDPhi2", abs(ptLxyDPhi2), weight);
}

void TTAlpsHistogramFiller::FillGenMuonMinDRHistograms(const shared_ptr<PhysicsObject> genMuon, const shared_ptr<NanoMuons> muonCollection,
                                                       string genMuonCollectionName, string looseMuonCollectionName, float weight) {
  TLorentzVector genMuonFourVector = asNanoGenParticle(genMuon)->GetFourVector(muonMass);
  float deltaRmin = 9999.;
  float muonWeightDR = 1;
  float deltaPhimin = 9999.;
  float muonWeightDPhi = 1;
  float deltaEtamin = 9999.;
  float muonWeightDEta = 1;
  for (auto muon : *muonCollection) {
    TLorentzVector muonFourVector = muon->GetFourVector();
    if (genMuonFourVector.DeltaR(muonFourVector) < deltaRmin) {
      deltaRmin = genMuonFourVector.DeltaR(muonFourVector);
      muonWeightDR = GetObjectWeight(muon->GetPhysicsObject(), "LooseMuons");
    }
    if (genMuonFourVector.DeltaPhi(muonFourVector) < deltaPhimin) {
      deltaPhimin = genMuonFourVector.DeltaPhi(muonFourVector);
      muonWeightDPhi = GetObjectWeight(muon->GetPhysicsObject(), "LooseMuons");
    }
    float dEta = abs(genMuonFourVector.Eta() - muonFourVector.Eta());
    if (dEta < deltaEtamin) {
      deltaEtamin = dEta;
      muonWeightDEta = GetObjectWeight(muon->GetPhysicsObject(), "LooseMuons");
    }
  }
  if (deltaRmin < 9999.)
    histogramsHandler->Fill(genMuonCollectionName + "_" + looseMuonCollectionName + "MinDR", deltaRmin, weight * muonWeightDR);
  if (deltaPhimin < 9999.)
    histogramsHandler->Fill(genMuonCollectionName + "_" + looseMuonCollectionName + "MinDPhi", deltaPhimin, weight * muonWeightDPhi);
  if (deltaEtamin < 9999.)
    histogramsHandler->Fill(genMuonCollectionName + "_" + looseMuonCollectionName + "MinDEta", deltaEtamin, weight * muonWeightDEta);
}

void TTAlpsHistogramFiller::FillRecoGenMatchedResonanceHistograms(const shared_ptr<Event> event, const shared_ptr<NanoMuons> muonCollection,
                                                                  string collectionName,
                                                                  const shared_ptr<PhysicsObjects> vertexCollection) {
  float weight = GetEventWeight(event);
  auto ttAlpsEvent = asTTAlpsEvent(event);

  // Get resonant dimuons for all possible muon combinations in collection
  auto dimuonFromALP = ttAlpsEvent->GetDimuonMatchedToGenMuonsFromALP(muonCollection);
  auto resonantDimuonsNotFromALP = ttAlpsEvent->GetMuonsMatchedToGenDimuonsNotFromALP(muonCollection);
  // Get non-resonant dimuons for alremainingl possible muon combinations in collection
  auto resonantDimuons = make_shared<NanoMuonPairs>(*resonantDimuonsNotFromALP);
  if (dimuonFromALP) resonantDimuons->push_back(*dimuonFromALP);
  auto nonresonantMuons = ttAlpsEvent->GetRemainingNonResonantMuons(muonCollection, resonantDimuons);

  auto resonantDimuonsVertexNotFromALP = make_shared<Collection<shared_ptr<PhysicsObject>>>();
  auto nonresonantMuonsVertex = make_shared<Collection<shared_ptr<PhysicsObject>>>();
  if (vertexCollection) {
    // Make sure the muon combinations are in the vertex collection
    auto allDimuonsVertexsNotFromALP = asNanoEvent(event)->GetVerticesForDimuons(resonantDimuonsNotFromALP);
    for (auto vertex : *allDimuonsVertexsNotFromALP) {
      for (auto v : *vertexCollection) {
        if (vertex == v) {
          resonantDimuonsVertexNotFromALP->push_back(vertex);
          break;
        }
      }
    }
    auto allNonresonantMuonsVertices = asNanoEvent(event)->GetVerticesForMuons(nonresonantMuons);
    for (auto vertex : *allNonresonantMuonsVertices) {
      for (auto v : *vertexCollection) {
        if (vertex == v) {
          nonresonantMuonsVertex->push_back(vertex);
          break;
        }
      }
    }
  } else {
    resonantDimuonsVertexNotFromALP = asNanoEvent(event)->GetVerticesForDimuons(resonantDimuonsNotFromALP);
    nonresonantMuonsVertex = asNanoEvent(event)->GetVerticesForMuons(nonresonantMuons);
  }

  string dimuonFromALPsCollectionName = collectionName + "FromALP";
  string dimuonNotFromALPsVertexCollectionName = collectionName + "ResonancesNotFromALP";
  string muonNotFromALPsVertexCollectionName = collectionName + "NonresonancesNotFromALP";

  if (dimuonFromALP) {
    auto dimuonVertexFromALP = asNanoEvent(event)->GetVertexForDimuon(dimuonFromALP->first, dimuonFromALP->second);
    if (dimuonVertexFromALP) {
      auto dimuonVertexFromALPCollection = make_shared<Collection<shared_ptr<PhysicsObject>>>();
      dimuonVertexFromALPCollection->push_back(dimuonVertexFromALP);
      FillMuonVertexHistograms(event, dimuonVertexFromALPCollection, dimuonFromALPsCollectionName);

      string category = asNanoDimuonVertex(dimuonVertexFromALP, event)->GetVertexCategory();
      histogramsHandler->Fill("Event_n" + dimuonFromALPsCollectionName + "_" + category, 1, weight);
    }
  }
  map<string, int> nResonantMuonsVerticesNotFromALP = {{"Pat", 0}, {"PatDSA", 0}, {"DSA", 0}};
  map<string, int> nNonresonantMuonsVertices = {{"Pat", 0}, {"PatDSA", 0}, {"DSA", 0}};
  FillMuonVertexHistograms(event, resonantDimuonsVertexNotFromALP, dimuonNotFromALPsVertexCollectionName);
  for (int i = 0; i < resonantDimuonsVertexNotFromALP->size(); i++) {
    nResonantMuonsVerticesNotFromALP[asNanoDimuonVertex(resonantDimuonsVertexNotFromALP->at(i), event)->GetVertexCategory()]++;
  }

  FillMuonVertexHistograms(event, nonresonantMuonsVertex, muonNotFromALPsVertexCollectionName);
  for (int i = 0; i < nonresonantMuonsVertex->size(); i++) {
    nNonresonantMuonsVertices[asNanoDimuonVertex(nonresonantMuonsVertex->at(i), event)->GetVertexCategory()]++;
  }
  for (const auto &[category, count] : nResonantMuonsVerticesNotFromALP) {
    histogramsHandler->Fill("Event_n" + dimuonNotFromALPsVertexCollectionName + "_" + category, count, weight);
    histogramsHandler->Fill("Event_n" + muonNotFromALPsVertexCollectionName + "_" + category, nNonresonantMuonsVertices.at(category),
                            weight);
  }
}

/// --------- Gen-Level Dimuon Vertex Collection Histograms --------- ///
/// ---------- flag: runGenMuonVertexCollectionHistograms ----------- ///

void TTAlpsHistogramFiller::FillCustomTTAlpsGenMuonVertexCollectionsVariables(const shared_ptr<Event> event) {
  if (muonVertexCollection.first.empty() && muonVertexCollection.second.empty()) return;

  string collectionName = muonVertexCollection.first;
  auto vertexCollection = event->GetCollection(collectionName);
  auto muonCollection = asTTAlpsEvent(event)->GetMuonsInVertexCollection(vertexCollection);
  FillRecoGenMatchedResonanceHistograms(event, muonCollection, collectionName, vertexCollection);
  
  FillMuonCollectionFromALPsNminus1Histograms(event);
}

void TTAlpsHistogramFiller::FillMuonCollectionFromALPsNminus1Histograms(const shared_ptr<Event> event) {
  float weight = GetEventWeight(event);

  // Gen-level muon vertex collection from ALP is given for both "Best" and "Good" collections
  string bestMuonVertexCollectionName = muonVertexCollection.first;
  auto muonVertexCollectionCuts = muonVertexCollection.second;
  string goodMuonVertexCollectionName = bestMuonVertexCollectionName;
  goodMuonVertexCollectionName.replace(0, 4, "Good");
  vector<string> muonVertexNminus1CollectionNames = {bestMuonVertexCollectionName, goodMuonVertexCollectionName};

  for (auto collectionName : muonVertexNminus1CollectionNames) {
    for (auto cut : muonVertexCollectionCuts) {
      // Skip the BestDimuonVertex cut
      if (cut == "BestDimuonVertex") continue;

      string nminus1CollectionName = collectionName + "Nminus1" + cut;

      auto looseMuonVertices = event->GetCollection(nminus1CollectionName);
      auto looseMuons = asTTAlpsEvent(event)->GetMuonsInVertexCollection(looseMuonVertices);
      auto looseMuonsFromALP = asTTAlpsEvent(event)->GetDimuonMatchedToGenMuonsFromALP(looseMuons);
      if (!looseMuonsFromALP) continue;
      auto dimuonVertex = asNanoEvent(event)->GetVertexForDimuon(looseMuonsFromALP->first, looseMuonsFromALP->second);
      if (!dimuonVertex) continue;
      string muonFromALPsCollectionName = collectionName + "FromALPNminus1";
      // n minus 1 collection name given as collectionName + "Nminus1" + cut
      float muon1Weight = GetObjectWeight(looseMuonsFromALP->first->GetPhysicsObject(), "LooseMuons");
      float muon2Weight = GetObjectWeight(looseMuonsFromALP->second->GetPhysicsObject(), "LooseMuons");
      FillDimuonVertexNminus1HistogramForCut(muonFromALPsCollectionName, cut, asNanoDimuonVertex(dimuonVertex, event),
                                             weight * muon1Weight * muon2Weight);
      if (looseMuonsFromALP->first->isDSA() && looseMuonsFromALP->second->isDSA()) {
        muonFromALPsCollectionName = collectionName + "FromALPNminus1_DSA";
      } else if (!looseMuonsFromALP->first->isDSA() && !looseMuonsFromALP->second->isDSA()) {
        muonFromALPsCollectionName = collectionName + "FromALPNminus1_Pat";
      } else {
        muonFromALPsCollectionName = collectionName + "FromALPNminus1_PatDSA";
      }
    }
  }
}

/// --------- Muon Matching Histograms --------- ///
/// ----- flag: runMuonMatchingHistograms ------ ///

void TTAlpsHistogramFiller::FillCustomTTAlpsMuonMatchingVariables(const shared_ptr<Event> event) {
  FillMatchingHistograms(event, "LoosePATMuons", "LooseDSAMuons");
}

void TTAlpsHistogramFiller::FillMatchingHistograms(const shared_ptr<Event> event, string patMuonCollection, string dsaMuonCollection) {
  float weight = GetEventWeight(event);

  auto looseMuons = asNanoMuons(event->GetCollection(patMuonCollection));
  auto looseDsaMuons = asNanoMuons(event->GetCollection(dsaMuonCollection));

  float matchingMinDeltaR = 0.1;

  // Segment-based matching
  float nSegmentMatched = 0;
  float nSegmentDRMatched = 0;
  float nSegmentOuterDRMatched = 0;
  for (auto dsaMuon : *looseDsaMuons) {
    float muonWeight = GetObjectWeight(dsaMuon->GetPhysicsObject(), "LooseMuons");
    float nSegments = dsaMuon->Get("nSegments");
    float minRatio = float(2) / float(3);

    histogramsHandler->Fill(dsaMuonCollection + "_nSegments", nSegments, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection + "_muonMatch1", dsaMuon->Get("muonMatch1"), weight * muonWeight);
    float ratio1 = float(dsaMuon->Get("muonMatch1")) / nSegments;
    histogramsHandler->Fill(dsaMuonCollection + "_matchRatio1", ratio1, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection + "_muonMatch2", dsaMuon->Get("muonMatch2"), weight * muonWeight);
    float ratio2 = float(dsaMuon->Get("muonMatch2")) / nSegments;
    histogramsHandler->Fill(dsaMuonCollection + "_matchRatio2", ratio2, weight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection + "_muonMatch1_nSegments", dsaMuon->Get("muonMatch1"), nSegments,
                            weight * muonWeight * muonWeight);
    histogramsHandler->Fill(dsaMuonCollection + "_muonMatch2_nSegments", dsaMuon->Get("muonMatch2"), nSegments,
                            weight * muonWeight * muonWeight);

    float matchFound = false;
    float muon_idx = -1;
    float maxMatches = -1;
    float ratio = -1;
    for (int i = 1; i <= 5; i++) {
      float ratio_tmp = dsaMuon->GetMatchesForNthBestMatch(i) / nSegments;
      if (!matchFound && ratio_tmp >= minRatio) {
        if (asNanoEvent(event)->PATMuonIndexExist(looseMuons, dsaMuon->GetMatchIdxForNthBestMatch(i))) {
          matchFound = true;
          muon_idx = dsaMuon->GetMatchIdxForNthBestMatch(i);
          maxMatches = dsaMuon->GetMatchesForNthBestMatch(i);
          ratio = ratio_tmp;
        }
      }
    }
    if (matchFound) {
      nSegmentMatched++;
      pair<float, int> dsaGenMinDR = asNanoEvent(event)->GetDeltaRandIndexOfClosestGenMuon(dsaMuon);
      float dsaMinDR = dsaGenMinDR.first;
      float dsaMinDR_genidx = dsaGenMinDR.second;
      auto muon = asNanoEvent(event)->GetPATMuonWithIndex(muon_idx, patMuonCollection);
      pair<float, int> patGenMinDR = asNanoEvent(event)->GetDeltaRandIndexOfClosestGenMuon(muon);
      float patMinDR = patGenMinDR.first;
      float patMinDR_genidx = patGenMinDR.second;
      float muonWeight = GetObjectWeight(muon->GetPhysicsObject(), "LooseMuons");
      float dsaMuonWeight = GetObjectWeight(dsaMuon->GetPhysicsObject(), "LooseMuons");

      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_genMinDR", patMinDR, dsaMinDR,
                              weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_genMinDRidx", patMinDR_genidx,
                              dsaMinDR_genidx, weight * muonWeight);

      FillMatchedMuonHistograms(muon, "SegmentMatch" + patMuonCollection, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_nSegments", nSegments, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_matchingRatio", ratio, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_maxMatches", maxMatches, weight * muonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_muonMatchIdx", muon_idx, weight * muonWeight);

      FillMatchedMuonHistograms(muon, "SegmentMatch" + dsaMuonCollection, weight * dsaMuonWeight);

      histogramsHandler->Fill("SegmentMatch" + dsaMuonCollection + "_eta_outerEta", dsaMuon->Get("eta"), dsaMuon->Get("outerEta"),
                              weight * dsaMuonWeight * dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch" + dsaMuonCollection + "_phi_outerPhi", dsaMuon->Get("phi"), dsaMuon->Get("outerPhi"),
                              weight * dsaMuonWeight * dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_eta_outerEta", muon->Get("eta"), muon->Get("outerEta"),
                              weight * muonWeight * muonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_phi_outerPhi", muon->Get("phi"), muon->Get("outerPhi"),
                              weight * muonWeight * muonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_eta", muon->Get("eta"), dsaMuon->Get("eta"),
                              weight * muonWeight * dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_phi", muon->Get("phi"), dsaMuon->Get("phi"),
                              weight * muonWeight * dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_outerEta", muon->Get("outerEta"),
                              dsaMuon->Get("outerEta"), weight * muonWeight * dsaMuonWeight);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_outerPhi", muon->Get("outerPhi"),
                              dsaMuon->Get("outerPhi"), weight * muonWeight * dsaMuonWeight);

      // Segment-based + DR matching
      auto dsaMuonP4 = dsaMuon->GetFourVector();
      auto muonP4 = muon->GetFourVector();
      if (muonP4.DeltaR(dsaMuonP4) < matchingMinDeltaR) {
        nSegmentDRMatched++;
        FillMatchedMuonHistograms(muon, "SegmentDRMatch" + patMuonCollection, weight * muonWeight);
        histogramsHandler->Fill("SegmentDRMatch" + patMuonCollection + "_nSegments", nSegments, weight * muonWeight);
        histogramsHandler->Fill("SegmentDRMatch" + patMuonCollection + "_matchingRatio", ratio, weight * muonWeight);
        histogramsHandler->Fill("SegmentDRMatch" + patMuonCollection + "_maxMatches", maxMatches, weight * muonWeight);
        histogramsHandler->Fill("SegmentDRMatch" + patMuonCollection + "_muonMatchIdx", muon_idx, weight * muonWeight);
      }

      // Segment-based + Outer DR matching
      float eta1 = dsaMuon->Get("outerEta");
      float phi1 = dsaMuon->Get("outerPhi");
      float eta2 = muon->Get("outerEta");
      float phi2 = muon->Get("outerPhi");
      if (asNanoEvent(event)->DeltaR(eta1, phi1, eta2, phi2) < matchingMinDeltaR) {
        nSegmentOuterDRMatched++;
        FillMatchedMuonHistograms(muon, "SegmentOuterDRMatch" + patMuonCollection, weight * muonWeight);
        histogramsHandler->Fill("SegmentOuterDRMatch" + patMuonCollection + "_nSegments", nSegments, weight * muonWeight);
        histogramsHandler->Fill("SegmentOuterDRMatch" + patMuonCollection + "_matchingRatio", ratio, weight * muonWeight);
        histogramsHandler->Fill("SegmentOuterDRMatch" + patMuonCollection + "_maxMatches", maxMatches, weight * muonWeight);
        histogramsHandler->Fill("SegmentOuterDRMatch" + patMuonCollection + "_muonMatchIdx", muon_idx, weight * muonWeight);
      }
    }
  }
  histogramsHandler->Fill("Event_nSegmentMatch" + patMuonCollection, nSegmentMatched, weight);
  histogramsHandler->Fill("Event_nSegmentMatch" + dsaMuonCollection, nSegmentMatched, weight);
  histogramsHandler->Fill("Event_nSegmentDRMatch" + patMuonCollection, nSegmentDRMatched, weight);
  histogramsHandler->Fill("Event_nSegmentOuterDRMatch" + patMuonCollection, nSegmentOuterDRMatched, weight);

  // Delta R matching values
  for (auto dsaMuon : *looseDsaMuons) {
    auto dsaMuonP4 = dsaMuon->GetFourVector();
    float dsaMuonWeight = GetObjectWeight(dsaMuon->GetPhysicsObject(), "LooseMuons");

    for (auto patMuon : *looseMuons) {
      float patMuonWeight = GetObjectWeight(patMuon->GetPhysicsObject(), "LooseMuons");
      auto patMuonP4 = patMuon->GetFourVector();
      float outerDeltaR = dsaMuon->OuterDeltaRtoMuon(patMuon);
      float deltaR = dsaMuonP4.DeltaR(patMuonP4);
      histogramsHandler->Fill(dsaMuonCollection + "_PATDR", deltaR, weight * dsaMuonWeight * patMuonWeight);
      histogramsHandler->Fill(dsaMuonCollection + "_PATOuterDR", outerDeltaR, weight * dsaMuonWeight * patMuonWeight);

      auto vertex = asNanoEvent(event)->GetVertexForDimuon(dsaMuon, patMuon);
      if (vertex) {
        float proxDR = vertex->Get("dRprox");
        histogramsHandler->Fill(dsaMuonCollection + "_PATProxDR", proxDR, weight * dsaMuonWeight * patMuonWeight);
      }
    }
  }
}

void TTAlpsHistogramFiller::FillMatchedMuonHistograms(const shared_ptr<NanoMuon> muon, string muonCollectionName, float weight) {
  histogramsHandler->Fill(muonCollectionName + "_pt", muon->Get("pt"), weight);
  histogramsHandler->Fill(muonCollectionName + "_eta", muon->Get("eta"), weight);
  histogramsHandler->Fill(muonCollectionName + "_phi", muon->Get("phi"), weight);
  histogramsHandler->Fill(muonCollectionName + "_dxyPVTraj", muon->Get("dxyPVTraj"), weight);
  float dxyPVTrajSig = abs(float(muon->Get("dxyPVTraj")) / float(muon->Get("dxyPVTrajErr")));
  histogramsHandler->Fill(muonCollectionName + "_dxyPVTrajSig", dxyPVTrajSig, weight);
  histogramsHandler->Fill(muonCollectionName + "_ip3DPVSigned", muon->Get("ip3DPVSigned"), weight);
  float ip3DPVSignedSig = abs(float(muon->Get("ip3DPVSigned")) / float(muon->Get("ip3DPVSignedErr")));
  histogramsHandler->Fill(muonCollectionName + "_ip3DPVSignedSig", ip3DPVSignedSig, weight);
}

/// --------- Trigger study Histograms --------- ///
/// ------ flag: runLLPTriggerHistograms ------ ///

void TTAlpsHistogramFiller::FillTriggerStudyHistograms(const shared_ptr<Event> event, string triggerName) {
  float weight = GetEventWeight(event);

  auto genMuonsFromALP = asTTAlpsEvent(event)->GetGenDimuonFromALP();
  string muonCollectionName = triggerName + "GenMuonFromALP";

  int nGenMuonsFromALP = 0;
  if (genMuonsFromALP) nGenMuonsFromALP = 1;
  histogramsHandler->Fill("Event_n" + muonCollectionName, nGenMuonsFromALP, weight);

  if (genMuonsFromALP) {
    auto genMuon1 = genMuonsFromALP->first;
    auto genMuon2 = genMuonsFromALP->second;
    histogramsHandler->Fill(muonCollectionName + "_pt1", genMuon1->Get("pt"), weight);
    histogramsHandler->Fill(muonCollectionName + "_pt2", genMuon2->Get("pt"), weight);
    float leadingPt = max((float)genMuon1->Get("pt"), (float)genMuon2->Get("pt"));
    float subleadingPt = min((float)genMuon1->Get("pt"), (float)genMuon2->Get("pt"));
    histogramsHandler->Fill(muonCollectionName + "_leadingPt", leadingPt, weight);
    histogramsHandler->Fill(muonCollectionName + "_subleadingPt", subleadingPt, weight);
  }
}

/// --------- Dimuon Cutflow Histograms --------- ///

void TTAlpsHistogramFiller::FillDimuonCutFlows(const shared_ptr<CutFlowManager> cutFlowManager, string dimuonCategory) {
  if (muonVertexCollection.first.empty() && muonVertexCollection.second.empty()) return;

  string collectionName = muonVertexCollection.first;
  if (dimuonCategory != "") collectionName = collectionName + "_" + dimuonCategory;
  int cutFlowLength = cutFlowManager->GetCutFlow(collectionName).size();
  string cutFlowName = "dimuonCutFlow_" + collectionName;
  string rawEventsCutFlowName = "rawEventsDimuonCutFlow_" + collectionName;
  auto cutFlowHist = new TH1D(cutFlowName.c_str(), cutFlowName.c_str(), cutFlowLength, 0, cutFlowLength);
  auto rawEventsCutFlowHist = new TH1D(rawEventsCutFlowName.c_str(), rawEventsCutFlowName.c_str(), cutFlowLength, 0, cutFlowLength);

  map<int, pair<string, float>> sortedWeightsAfterCuts;
  map<int, pair<string, float>> sortedRawEventsAfterCuts;
  auto cutFlow = cutFlowManager->GetCutFlow(collectionName);
  auto rawEventsCutFlow = cutFlowManager->GetRawEventsCutFlow(collectionName);
  for (auto &[cutName, sumOfWeights] : cutFlowManager->GetCutFlow(collectionName)) {
    string number = cutName.substr(0, cutName.find("_"));
    int index = stoi(number);
    sortedWeightsAfterCuts[index] = {cutName, sumOfWeights};
    sortedRawEventsAfterCuts[index] = {cutName, rawEventsCutFlow[cutName]};
  }

  int bin = 1;
  for (auto &[index, values] : sortedWeightsAfterCuts) {
    cutFlowHist->SetBinContent(bin, get<1>(values));
    rawEventsCutFlowHist->SetBinContent(bin, get<1>(sortedRawEventsAfterCuts[index]));
    cutFlowHist->GetXaxis()->SetBinLabel(bin, get<0>(values).c_str());
    rawEventsCutFlowHist->GetXaxis()->SetBinLabel(bin, get<0>(sortedRawEventsAfterCuts[index]).c_str());
    bin++;
  }
  histogramsHandler->SetHistogram1D(cutFlowName.c_str(), cutFlowHist);
  histogramsHandler->SetHistogram1D(rawEventsCutFlowName.c_str(), rawEventsCutFlowHist);
}

/// --------- ABCD Histograms --------- ///
/// ----- flag: runABCDHistograms ----- ///

void TTAlpsHistogramFiller::FillABCDHistograms(const shared_ptr<Event> event, vector<string> abcdCollections) {
  double weight = GetEventWeight(event);

  auto genMuons = event->GetCollection("GenPart");

  for (string collectionName : abcdCollections) {
    auto collection = event->GetCollection(collectionName);

    if (collection->size() < 1) continue;

    for (auto vertex : *collection) {
      auto dimuon = asNanoDimuonVertex(vertex, event);
      auto muon1 = dimuon->Muon1();
      auto muon2 = dimuon->Muon2();

      float muon1weight = GetObjectWeight(muon1->GetPhysicsObject(), "LooseMuons");
      float muon2weight = GetObjectWeight(muon2->GetPhysicsObject(), "LooseMuons");

      map<string, double> variables = {
          {"Lxy", dimuon->GetLxyFromPV()},
          {"LxySignificance", dimuon->GetLxyFromPV() / dimuon->GetLxySigmaFromPV()},
          {"absCollinearityAngle", dimuon->GetCollinearityAngle()},
          {"3Dangle", dimuon->Get3DOpeningAngle()},

          {"logLxy", TMath::Log10(dimuon->GetLxyFromPV())},
          {"logLxySignificance", TMath::Log10(dimuon->GetLxyFromPV() / dimuon->GetLxySigmaFromPV())},
          {"logAbsCollinearityAngle", TMath::Log10(dimuon->GetCollinearityAngle())},
          {"log3Dangle", TMath::Log10(dimuon->Get3DOpeningAngle())},
      };

      for (auto &[varName_1, varValue_1] : variables) {
        for (auto &[varName_2, varValue_2] : variables) {
          if (varName_1 == varName_2) continue;
          histogramsHandler->Fill(collectionName + "_" + varName_2 + "_vs_" + varName_1, varValue_1, varValue_2,
                                  weight * muon1weight * muon2weight);
        }
      }
      auto genMuon1 = muon1->GetGenMuon(genMuons, 0.3);
      auto genMuon2 = muon2->GetGenMuon(genMuons, 0.3);

      auto mother1_index = genMuon1 ? genMuon1->GetMotherIndex() : -1;
      auto mother2_index = genMuon2 ? genMuon2->GetMotherIndex() : -1;

      int mother1_pid = mother1_index >= 0 ? genMuons->at(mother1_index)->Get("pdgId") : -1;
      int mother2_pid = mother2_index >= 0 ? genMuons->at(mother2_index)->Get("pdgId") : -1;

      histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2", mother1_pid, mother2_pid, weight * muon1weight * muon2weight);

      float lxySignificance = variables["logLxySignificance"];
      float angle3D = variables["log3Dangle"];

      if (lxySignificance > -2.0 && lxySignificance < -1.0 && angle3D > -1.5 && angle3D < -1.0) {
        histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2_lowBlob", mother1_pid, mother2_pid,
                                weight * muon1weight * muon2weight);
      }
      if (lxySignificance > -0.5 && lxySignificance < 0.5 && angle3D > 0.0 && angle3D < 0.4) {
        histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2_rightBlob", mother1_pid, mother2_pid,
                                weight * muon1weight * muon2weight);
      }
      if (lxySignificance > -0.5 && lxySignificance < 0.5 && angle3D > -1.5 && angle3D < -1.0) {
        histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2_centralBlob", mother1_pid, mother2_pid,
                                weight * muon1weight * muon2weight);
      }
    }
  }
}
