#include "TTAlpsObjectsManager.hpp"

#include "ConfigManager.hpp"
#include "Logger.hpp"

using namespace std;

TTAlpsObjectsManager::TTAlpsObjectsManager() {
  auto &config = ConfigManager::GetInstance();

  ttAlpsCuts = make_unique<TTAlpsDimuonCuts>();
  try {
    config.GetMap("muonMatchingParams", muonMatchingParams);
  } catch (const Exception &e) {
    warn() << "Couldn't read muonMatchingParams from config file - no muon matching methods will be applied to muon collections" << endl;
  }
  try {
    config.GetPair("muonVertexCollection", muonVertexCollection);
  } catch (const Exception &e) {
    warn() << "Couldn't read muonVertexCollection from config file - is needed for dimuon vertex collection" << endl;
  }
  try {
    config.GetValue("muonVertexCollectionInput", muonVertexCollectionInput);
  } catch (const Exception &e) {
    warn()
        << "Couldn't read muonVertexCollectionInput from config file - using first defined muonMatchingParams vertex collection as default"
        << endl;
    try {
      string matchingMethod = muonMatchingParams.begin()->first;

      muonVertexCollectionInput = "LooseMuonsVertex" + matchingMethod + "Match";
    } catch (const std::bad_alloc &e) {
      warn() << "Couldn't read muonMatchingParams from config file - no muon matching methods will be applied to muon collections" << endl;
      muonVertexCollectionInput = "";
    }
  }
}

void TTAlpsObjectsManager::InsertMatchedLooseMuonsCollections(shared_ptr<Event> event) {
  if (muonMatchingParams.empty()) return;
  auto loosePATMuons = asNanoMuons(event->GetCollection("LoosePATMuons"));
  auto looseDSAMuons = asNanoMuons(event->GetCollection("LooseDSAMuons"));
  auto looseMuons = make_shared<NanoMuons>();
  for (auto muon : *loosePATMuons) {
    looseMuons->push_back(muon);
  }
  for (auto muon : *looseDSAMuons) {
    looseMuons->push_back(muon);
  }
  for (auto &[matchingMethod, param] : muonMatchingParams) {
    if (matchingMethod == "DR") {
      InsertDRMatchedLooseMuonsCollections(event, param, looseMuons);
      continue;
    }
    if (matchingMethod == "OuterDR") {
      InsertOuterDRMatchedLooseMuonsCollections(event, param, looseMuons);
      continue;
    }
    if (matchingMethod == "ProxDR") {
      InsertProximityDRMatchedLooseMuonsCollections(event, param, looseMuons);
      continue;
    }
    if (matchingMethod == "Segment") {
      InsertSegmentMatchedLooseMuonsCollections(event, param, looseMuons);
      continue;
    }
  }
}

void TTAlpsObjectsManager::InsertDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR,
                                                                shared_ptr<NanoMuons> muonCollection) {
  auto looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons(muonCollection, maxDR);
  auto looseMuonVerticesDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsDRMatch);

  event->AddCollection("LooseMuonsDRMatch", asPhysicsObjects(looseMuonsDRMatch));
  event->AddCollection("LooseMuonsVertexDRMatch", looseMuonVerticesDRMatch);
}

void TTAlpsObjectsManager::InsertOuterDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR,
                                                                     shared_ptr<NanoMuons> muonCollection) {
  auto looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons(muonCollection, maxDR);
  auto looseMuonVerticesOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsOuterDRMatch);

  event->AddCollection("LooseMuonsOuterDRMatch", asPhysicsObjects(looseMuonsOuterDRMatch));
  event->AddCollection("LooseMuonsVertexOuterDRMatch", looseMuonVerticesOuterDRMatch);
}

void TTAlpsObjectsManager::InsertProximityDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR,
                                                                         shared_ptr<NanoMuons> muonCollection) {
  auto looseMuonsProxDRMatch = asNanoEvent(event)->GetProximityDRMatchedMuons(muonCollection, maxDR);
  auto looseMuonVerticesProxDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsProxDRMatch);

  event->AddCollection("LooseMuonsProxDRMatch", asPhysicsObjects(looseMuonsProxDRMatch));
  event->AddCollection("LooseMuonsVertexProxDRMatch", looseMuonVerticesProxDRMatch);
}

void TTAlpsObjectsManager::InsertSegmentMatchedLooseMuonsCollections(shared_ptr<Event> event, float minSegmentRatio,
                                                                     shared_ptr<NanoMuons> muonCollection) {
  auto looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons(muonCollection, minSegmentRatio);
  event->AddCollection("LooseMuonsSegmentMatch", asPhysicsObjects(looseMuonsSegmentMatch));

  try {
    auto looseMuonVerticesSegmentMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentMatch);
    event->AddCollection("LooseMuonsVertexSegmentMatch", looseMuonVerticesSegmentMatch);
  } catch (const Exception &e) {
    warn() << "Couldn't get vertices for segment matched muons. Collection will not be inserted." << endl;
  }
}

void TTAlpsObjectsManager::InsertBaseLooseMuonVertexCollection(shared_ptr<Event> event) {
  if (muonMatchingParams.size() == 0) return;
  if (muonVertexCollectionInput.empty()) return;

  try {
    auto vertices = event->GetCollection(muonVertexCollectionInput);

    auto baseDimuonVertices = make_shared<PhysicsObjects>();
    for (auto vertex : *vertices) {
      if (IsGoodBaseMuonVertex(vertex, event)) baseDimuonVertices->push_back(vertex);
    }
    event->AddCollection("BaseDimuonVertices", baseDimuonVertices);
  } catch (const Exception &e) {
    warn() << "Couldn't insert the base dimuon vertex collection." << endl;
  }
}

void TTAlpsObjectsManager::InsertMuonVertexCollection(shared_ptr<Event> event) {
  if (muonMatchingParams.size() == 0) return;
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  try {
    auto vertices = event->GetCollection(muonVertexCollectionInput);

    InsertMuonVertexCollection(event, vertices);
  } catch (const Exception &e) {
    warn() << "Couldn't insert the muon vertex collection." << endl;
  }
}

void TTAlpsObjectsManager::InsertNonLeadingMuonVertexCollections(shared_ptr<Event> event) {
  if (muonMatchingParams.size() == 0) return;
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  try {
    auto vertices = event->GetCollection("LooseMuonsVertex" + matchingMethod + "Match");

    auto triggerMuonCollection = event->GetCollection("TriggerMuonMatch");
    auto nonTriggerMuonVertexCollectionName = "BestNonTrigger" + muonVertexCollection.first.substr(4);
    auto nonTriggerVertices = make_shared<PhysicsObjects>();
    if (triggerMuonCollection->size() < 1)
      warn() << "TriggerMuonMatch collection is empty" << endl;
    else {
      auto triggerMuon = triggerMuonCollection->at(0);
      for (auto vertex : *vertices) {
        auto muon1 = asNanoDimuonVertex(vertex, event)->Muon1();
        auto muon2 = asNanoDimuonVertex(vertex, event)->Muon2();
        if (muon1->GetPhysicsObject() == triggerMuon || muon2->GetPhysicsObject() == triggerMuon) continue;
        nonTriggerVertices->push_back(vertex);
      }
    }
    event->AddCollection("LooseNonTriggerMuonsVertex" + matchingMethod + "Match", nonTriggerVertices);

    auto tightMuons = event->GetCollection("TightMuons");
    auto leadingTightMuon = asTTAlpsEvent(event)->GetLeadingMuon(asNanoMuons(tightMuons));
    auto nonLeadingMuonVertexCollectionName = "BestNonLeading" + muonVertexCollection.first.substr(4);
    auto nonLeadingMuonVertices = make_shared<PhysicsObjects>();
    if (leadingTightMuon) {
      for (auto vertex : *vertices) {
        auto muon1 = asNanoDimuonVertex(vertex, event)->Muon1();
        auto muon2 = asNanoDimuonVertex(vertex, event)->Muon2();
        if (muon1->GetPhysicsObject() == leadingTightMuon->GetPhysicsObject() ||
            muon2->GetPhysicsObject() == leadingTightMuon->GetPhysicsObject())
          continue;
        nonLeadingMuonVertices->push_back(vertex);
      }
    }
    event->AddCollection("LooseNonLeadingMuonsVertex" + matchingMethod + "Match", nonLeadingMuonVertices);
  } catch (const Exception &e) {
    warn() << "Couldn't insert the non-leading muon vertex collection." << endl;
  }
}

void TTAlpsObjectsManager::InsertMuonVertexCollection(shared_ptr<Event> event, shared_ptr<PhysicsObjects> vertices) {
  if (muonMatchingParams.size() == 0) return;
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  string muonVertexCollectionName = muonVertexCollection.first;
  auto muonVertexCollectionCuts = muonVertexCollection.second;
  bool bestVertex = false;
  for (auto cutName : muonVertexCollectionCuts) {
    if (cutName == "BestDimuonVertex") {
      bestVertex = true;
      break;
    }
  }
  if (bestVertex)
    muonVertexCollectionCuts.erase(std::remove(muonVertexCollectionCuts.begin(), muonVertexCollectionCuts.end(), "BestDimuonVertex"),
                                   muonVertexCollectionCuts.end());

  auto passedVertices = make_shared<PhysicsObjects>();
  for (auto vertex : *vertices) {
    auto dimuonVertex = asNanoDimuonVertex(vertex, event);
    bool passed = true;
    for (auto cutName : muonVertexCollectionCuts) {
      if (!ttAlpsCuts->PassesCut(dimuonVertex, cutName)) {
        passed = false;
        break;
      }
    }
    if (passed) passedVertices->push_back(vertex);
  }

  auto finalCollection = make_shared<PhysicsObjects>();
  if (bestVertex) {
    if (GetBestMuonVertex(passedVertices, event)) finalCollection->push_back(GetBestMuonVertex(passedVertices, event));
    // If input muonVertexCollection is "Best" vertex collection we also make a good vertex collection
    string goodMuonVertexCollectionName = muonVertexCollectionName;
    goodMuonVertexCollectionName.replace(0, 4, "Good");
    event->AddCollection(goodMuonVertexCollectionName, passedVertices);
  } else
    finalCollection = passedVertices;

  event->AddCollection(muonVertexCollectionName, finalCollection);
}

void TTAlpsObjectsManager::InsertNminus1VertexCollections(shared_ptr<Event> event) {
  if (muonMatchingParams.size() == 0) return;
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  try {
    auto vertices = event->GetCollection(muonVertexCollectionInput);

    auto muonVertexCollectionName = muonVertexCollection.first;
    auto muonVertexCollectionCuts = muonVertexCollection.second;
    bool bestVertex = false;
    if (muonVertexCollectionCuts.back() == "BestDimuonVertex") {
      bestVertex = true;
      muonVertexCollectionCuts.pop_back();
    }

    int nCuts = muonVertexCollectionCuts.size();
    for (int i = 0; i < nCuts; i++) {
      auto passedVertices = make_shared<PhysicsObjects>();
      for (auto vertex : *vertices) {
        bool passed = true;
        auto dimuonVertex = asNanoDimuonVertex(vertex, event);
        for (int j = 0; j < nCuts; j++) {
          if (j == i) continue;
          if (!ttAlpsCuts->PassesCut(dimuonVertex, muonVertexCollectionCuts[j])) {
            passed = false;
            break;
          }
        }
        if (passed) passedVertices->push_back(vertex);
      }
      string nminus1CollectionName = muonVertexCollectionName + "Nminus1" + muonVertexCollectionCuts[i];
      auto finalCollection = make_shared<PhysicsObjects>();
      if (bestVertex) {
        if (GetBestMuonVertex(passedVertices, event)) finalCollection->push_back(GetBestMuonVertex(passedVertices, event));
        // If input muonVertexCollection is "Best" vertex collection we also make a good vertex collection
        string goodMuonVertexCollectionName = nminus1CollectionName;
        goodMuonVertexCollectionName.replace(0, 4, "Good");
        event->AddCollection(goodMuonVertexCollectionName, passedVertices);
      } else
        finalCollection = passedVertices;
      event->AddCollection(nminus1CollectionName, finalCollection);
    }
  } catch (const Exception &e) {
    warn() << "Couldn't insert the N-1 muon vertex collection." << endl;
  }
}

bool TTAlpsObjectsManager::IsGoodBaseMuonVertex(const shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  auto dimuonVertex = asNanoDimuonVertex(vertex, event);
  if (!ttAlpsCuts->PassesLLPnanoAODVertexCuts(dimuonVertex)) return false;

  if (!ttAlpsCuts->PassesChargeCut(dimuonVertex)) return false;
  return true;
}

shared_ptr<PhysicsObject> TTAlpsObjectsManager::GetBestMuonVertex(const shared_ptr<PhysicsObjects> vertices, shared_ptr<Event> event) {
  if (vertices->size() == 0) return nullptr;
  if (vertices->size() == 1) return vertices->at(0);
  auto bestVertex = vertices->at(0);
  for (auto vertex : *vertices) {
    if ((float)asNanoDimuonVertex(vertex, event)->Get("normChi2") < (float)asNanoDimuonVertex(bestVertex, event)->Get("normChi2")) {
      bestVertex = vertex;
    }
  }
  return bestVertex;
}

void TTAlpsObjectsManager::InsertMatchedLooseMuonEfficiencyCollections(shared_ptr<Event> event) {
  auto loosePATMuons = asNanoMuons(event->GetCollection("LoosePATMuons"));
  auto looseDSAMuons = asNanoMuons(event->GetCollection("LooseDSAMuons"));
  auto looseMuons = make_shared<NanoMuons>();
  for (auto muon : *loosePATMuons) {
    looseMuons->push_back(muon);
  }
  for (auto muon : *looseDSAMuons) {
    looseMuons->push_back(muon);
  }
  auto looseMuonsSegmentDRMatch = make_shared<NanoMuons>();
  auto looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons(looseMuons);
  auto looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons(looseMuons);
  auto looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons(looseMuons);

  for (auto muon : *looseMuonsSegmentMatch) {
    float muon_idx = muon->Get("idx");
    if (asNanoEvent(event)->MuonIndexExist(looseMuonsDRMatch, muon_idx, muon->IsDSA())) {
      looseMuonsSegmentDRMatch->push_back(muon);
    }
  }
  event->AddCollection("LooseMuonsSegmentDRMatch", asPhysicsObjects(looseMuonsSegmentDRMatch));
  auto looseMuonsVertexSegmentDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentDRMatch);
  event->AddCollection("LooseMuonsVertexSegmentDRMatch", looseMuonsVertexSegmentDRMatch);

  auto looseMuonsSegmentOuterDRMatch = make_shared<NanoMuons>();
  for (auto muon : *looseMuonsSegmentMatch) {
    float muon_idx = muon->Get("idx");
    if (asNanoEvent(event)->MuonIndexExist(looseMuonsOuterDRMatch, muon_idx, muon->IsDSA())) {
      looseMuonsSegmentOuterDRMatch->push_back(muon);
    }
  }
  event->AddCollection("LooseMuonsSegmentOuterDRMatch", asPhysicsObjects(looseMuonsSegmentOuterDRMatch));
  auto looseMuonsVertexSegmentOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentOuterDRMatch);
  event->AddCollection("LooseMuonsVertexSegmentOuterDRMatch", looseMuonsVertexSegmentOuterDRMatch);
}

void TTAlpsObjectsManager::InsertMuonTriggerCollections(shared_ptr<Event> event) {
  auto muonTrigObjs = event->GetCollection("MuonTrigObj");
  auto muonTriggerObjectsCollection = make_shared<PhysicsObjects>();
  auto muonTriggerCollection = make_shared<PhysicsObjects>();
  auto triggerMuonCollection = make_shared<PhysicsObjects>();

  for (auto muonTrigObj : *muonTrigObjs) {
    int filterBits = muonTrigObj->Get("filterBits");
    if (!(filterBits & 2)) continue;
    muonTriggerObjectsCollection->push_back(muonTrigObj);
  }
  event->AddCollection("MuonTriggerObjects", muonTriggerObjectsCollection);
  int leadingMuonTrigger_idx = -1;
  float leadingMuonTrigger_pt = -1.;
  for (int i = 0; i < muonTriggerObjectsCollection->size(); i++) {
    auto muonTrigger = muonTriggerObjectsCollection->at(i);
    if ((float)muonTrigger->Get("pt") > leadingMuonTrigger_pt) {
      leadingMuonTrigger_pt = muonTrigger->Get("pt");
      leadingMuonTrigger_idx = i;
    }
  }
  if (leadingMuonTrigger_idx >= 0) {
    auto leadingMuonTrigger = muonTriggerObjectsCollection->at(leadingMuonTrigger_idx);
    muonTriggerCollection->push_back(leadingMuonTrigger);

    auto tightMuons = event->GetCollection("TightMuons");
    float minDR = 9999.;
    int minDR_idx = -1;
    float maxDR = 0.3;
    TLorentzVector muonTrigger4Vector;
    ;
    muonTrigger4Vector.SetPtEtaPhiM(leadingMuonTrigger->Get("pt"), leadingMuonTrigger->Get("eta"), leadingMuonTrigger->Get("phi"), 0.105);
    for (int i = 0; i < tightMuons->size(); i++) {
      auto muon = tightMuons->at(i);
      auto muon4Vector = asNanoMuon(muon)->GetFourVector();
      float dR = muonTrigger4Vector.DeltaR(muon4Vector);
      if (dR < minDR && dR < maxDR) {
        minDR = dR;
        minDR_idx = i;
      }
    }
    if (minDR_idx > -1) triggerMuonCollection->push_back(tightMuons->at(minDR_idx));

  } else {
    warn() << "No valid leading muon trigger found in MuonTriggerObjects collection" << endl;
  }
  event->AddCollection("LeadingMuonTriggerObject", muonTriggerCollection);
  event->AddCollection("TriggerMuonMatch", triggerMuonCollection);
}
