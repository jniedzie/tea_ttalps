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
  auto looseMuonVerticesSegmentMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentMatch);

  event->AddCollection("LooseMuonsSegmentMatch", asPhysicsObjects(looseMuonsSegmentMatch));
  event->AddCollection("LooseMuonsVertexSegmentMatch", looseMuonVerticesSegmentMatch);
}

void TTAlpsObjectsManager::InsertBaseLooseMuonVertexCollection(shared_ptr<Event> event) {
  if (muonMatchingParams.size() == 0) return;

  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  auto vertices = event->GetCollection("LooseMuonsVertex" + matchingMethod + "Match");

  auto baseDimuonVertices = make_shared<PhysicsObjects>();
  for (auto vertex : *vertices) {
    if (IsGoodBaseMuonVertex(vertex, event)) baseDimuonVertices->push_back(vertex);
  }
  event->AddCollection("BaseDimuonVertices", baseDimuonVertices);
}

void TTAlpsObjectsManager::InsertMuonVertexCollection(shared_ptr<Event> event) {
  if (muonMatchingParams.size() == 0) return;
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  auto vertices = event->GetCollection("LooseMuonsVertex" + matchingMethod + "Match");

  auto muonVertexCollectionName = muonVertexCollection.first;
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

  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  auto vertices = event->GetCollection("LooseMuonsVertex" + matchingMethod + "Match");

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
    if (asNanoEvent(event)->MuonIndexExist(looseMuonsDRMatch, muon_idx, muon->isDSA())) {
      looseMuonsSegmentDRMatch->push_back(muon);
    }
  }
  event->AddCollection("LooseMuonsSegmentDRMatch", asPhysicsObjects(looseMuonsSegmentDRMatch));
  auto looseMuonsVertexSegmentDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentDRMatch);
  event->AddCollection("LooseMuonsVertexSegmentDRMatch", looseMuonsVertexSegmentDRMatch);

  auto looseMuonsSegmentOuterDRMatch = make_shared<NanoMuons>();
  for (auto muon : *looseMuonsSegmentMatch) {
    float muon_idx = muon->Get("idx");
    if (asNanoEvent(event)->MuonIndexExist(looseMuonsOuterDRMatch, muon_idx, muon->isDSA())) {
      looseMuonsSegmentOuterDRMatch->push_back(muon);
    }
  }
  event->AddCollection("LooseMuonsSegmentOuterDRMatch", asPhysicsObjects(looseMuonsSegmentOuterDRMatch));
  auto looseMuonsVertexSegmentOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentOuterDRMatch);
  event->AddCollection("LooseMuonsVertexSegmentOuterDRMatch", looseMuonsVertexSegmentOuterDRMatch);
}
