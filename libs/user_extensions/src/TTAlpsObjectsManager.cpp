#include "TTAlpsObjectsManager.hpp"

#include "ConfigManager.hpp"
#include "Logger.hpp"

using namespace std;

TTAlpsObjectsManager::TTAlpsObjectsManager() {
  auto& config = ConfigManager::GetInstance();

  ttAlpsCuts = make_unique<TTAlpsDimuonCuts>();

  try {
    config.GetMap("muonMatchingParams", muonMatchingParams);
  } catch (const Exception &e) {
    info() << "Couldn't read muonMatchingParams from config file - no muon matching methods will be applied to muon collections" << endl;
  }
  try {
    config.GetMap("dimuonVertexCuts", dimuonVertexCuts);
  } catch (const Exception &e) {
    info() << "Couldn't read dimuonVertexCuts from config file - is needed for GoodLooseMuonVertex collections" << endl;
  }
  try {
    config.GetMap("muonVertexCollections", muonVertexCollections);
  } catch (const Exception &e) {
    info() << "Couldn't read muonVertexCollections from config file - is needed for GoodLooseMuonVertex collections" << endl;
  } 
  try {
    config.GetVector("muonVertexNminus1Collections", muonVertexNminus1Collections);
  } catch (const Exception &e) {
    info() << "Couldn't read muonVertexNminus1Collections from config file - is needed for GoodLooseMuonVertex N-1 collections" << endl;
  } 
}

void TTAlpsObjectsManager::InsertMatchedLooseMuonsCollections(shared_ptr<Event> event) {

  auto loosePATMuons = event->GetCollection("LoosePATMuons");
  auto looseDSAMuons = event->GetCollection("LooseDSAMuons");
  auto looseMuons = make_shared<PhysicsObjects>();
  for (auto muon : *loosePATMuons) {
    looseMuons->push_back(muon);
  }
  for (auto muon : *looseDSAMuons) {
    looseMuons->push_back(muon);
  }
  for(auto &[matchingMethod, param] : muonMatchingParams) {
    if(matchingMethod == "DR") {
      InsertDRMatchedLooseMuonsCollections(event, param, looseMuons);
      continue;
    }
    if(matchingMethod == "OuterDR") {
      InsertOuterDRMatchedLooseMuonsCollections(event, param, looseMuons);
      continue;
    }
    if(matchingMethod == "ProxDR") {
      InsertProximityDRMatchedLooseMuonsCollections(event, param, looseMuons);
      continue;
    }
    if(matchingMethod == "Segment") {
      InsertSegmentMatchedLooseMuonsCollections(event, param, looseMuons);
      continue;
    }
  }
}

void TTAlpsObjectsManager::InsertDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR, shared_ptr<Collection<shared_ptr<PhysicsObject>>> muonCollection) {
  shared_ptr<PhysicsObjects> looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons(muonCollection, maxDR);
  shared_ptr<PhysicsObjects> looseMuonVerticesDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsDRMatch);
  
  event->AddCollection("LooseMuonsDRMatch", looseMuonsDRMatch);
  event->AddCollection("LooseMuonsVertexDRMatch", looseMuonVerticesDRMatch);
}
  
void TTAlpsObjectsManager::InsertOuterDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR, shared_ptr<Collection<shared_ptr<PhysicsObject>>> muonCollection) {
  
  shared_ptr<PhysicsObjects> looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons(muonCollection, maxDR);
  shared_ptr<PhysicsObjects> looseMuonVerticesOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsOuterDRMatch);

  event->AddCollection("LooseMuonsOuterDRMatch", looseMuonsOuterDRMatch);
  event->AddCollection("LooseMuonsVertexOuterDRMatch", looseMuonVerticesOuterDRMatch);
}

void TTAlpsObjectsManager::InsertProximityDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR, shared_ptr<Collection<shared_ptr<PhysicsObject>>> muonCollection) {
  
  shared_ptr<PhysicsObjects> looseMuonsProxDRMatch = asNanoEvent(event)->GetProximityDRMatchedMuons(muonCollection, maxDR);
  shared_ptr<PhysicsObjects> looseMuonVerticesProxDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsProxDRMatch);

  event->AddCollection("LooseMuonsProxDRMatch", looseMuonsProxDRMatch);
  event->AddCollection("LooseMuonsVertexProxDRMatch", looseMuonVerticesProxDRMatch);
}

void TTAlpsObjectsManager::InsertSegmentMatchedLooseMuonsCollections(shared_ptr<Event> event, float minSegmentRatio, shared_ptr<Collection<shared_ptr<PhysicsObject>>> muonCollection) {

  shared_ptr<PhysicsObjects> looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons(muonCollection, minSegmentRatio);
  shared_ptr<PhysicsObjects> looseMuonVerticesSegmentMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentMatch);
  
  event->AddCollection("LooseMuonsSegmentMatch", looseMuonsSegmentMatch);
  event->AddCollection("LooseMuonsVertexSegmentMatch", looseMuonVerticesSegmentMatch);
}

void TTAlpsObjectsManager::InsertBaseLooseMuonVertexCollection(shared_ptr<Event> event) {
  if(muonMatchingParams.size() == 0) {
    error() << "Requested to insert GoodLooseMuonVertex collection, but no muonMatchingParams are set in the config file." << endl;
    return;
  }
  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  auto vertices = event->GetCollection("LooseMuonsVertex"+matchingMethod+"Match");
  
  auto baseDimuonVertices = make_shared<PhysicsObjects>();
  for(auto vertex : *vertices) {
    if(IsGoodBaseMuonVertex(vertex, event)) baseDimuonVertices->push_back(vertex);
  }
  event->AddCollection("BaseDimuonVertices", baseDimuonVertices);
}

void TTAlpsObjectsManager::InsertGoodLooseMuonVertexCollection(shared_ptr<Event> event) {
  for(auto &[muonVertexCollectionName, muonVertexCollectionCuts] : muonVertexCollections) {
    InsertGoodLooseMuonVertexCollection(event, muonVertexCollectionName, muonVertexCollectionCuts);
  }
}

void TTAlpsObjectsManager::InsertNminus1VertexCollections(shared_ptr<Event> event) {
  for(auto muonVertexCollectionName : muonVertexNminus1Collections) {
    if(muonVertexCollections.find(muonVertexCollectionName) == muonVertexCollections.end()) {
      warn() << "Requested to insert N-1 vertex collection: " << muonVertexCollectionName << ", but the collection name cannot be found in muonVertexCollections. Skipped." << endl;
      continue;
    }
    auto muonVertexCollectionCuts = muonVertexCollections[muonVertexCollectionName];
    InsertNminus1VertexCollections(event, muonVertexCollectionName, muonVertexCollectionCuts);
  }
}

void TTAlpsObjectsManager::InsertGoodLooseMuonVertexCollection(shared_ptr<Event> event, string muonVertexCollectionName, vector<string> muonVertexCollectionCuts) {
  if(muonMatchingParams.size() == 0) {
    error() << "Requested to insert GoodLooseMuonVertex collection, but no muonMatchingParams are set in the config file." << endl;
    return;
  }
  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  auto vertices = event->GetCollection("LooseMuonsVertex"+matchingMethod+"Match");

  bool bestVertex = false;
  for(auto cutName : muonVertexCollectionCuts) {
    if(cutName == "BestDimuonVertex") {
      bestVertex = true;
      break;
    }
  }
  if (bestVertex) muonVertexCollectionCuts.erase(std::remove(muonVertexCollectionCuts.begin(), muonVertexCollectionCuts.end(), "BestDimuonVertex"), muonVertexCollectionCuts.end());

  auto passedVertices = make_shared<PhysicsObjects>();
  for(auto vertex : *vertices) {
    auto dimuonVertex = asNanoDimuonVertex(vertex, event);
    bool passed = true;
    for(auto cutName : muonVertexCollectionCuts) {
      if(!ttAlpsCuts->PassesCut(dimuonVertex, cutName)) {
        passed = false;
        break;
      }
    }
    if(passed) passedVertices->push_back(vertex);
  }

  auto finalCollection = make_shared<PhysicsObjects>();
  if(bestVertex) {
    if(GetBestMuonVertex(passedVertices, event)) finalCollection->push_back(GetBestMuonVertex(passedVertices, event));
  }
  else finalCollection = passedVertices;

  event->AddCollection(muonVertexCollectionName, finalCollection);
}

void TTAlpsObjectsManager::InsertNminus1VertexCollections(shared_ptr<Event> event, string muonVertexCollectionName, vector<string> muonVertexCollectionCuts) {  
  if(muonMatchingParams.size() == 0) {
    error() << "Requested to insert GoodLooseMuonVertex collection, but no muonMatchingParams are set in the config file." << endl;
    return;
  }
  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  auto vertices = event->GetCollection("LooseMuonsVertex"+matchingMethod+"Match");

  bool bestVertex = false;
  if(muonVertexCollectionCuts.back() == "BestDimuonVertex") {
    bestVertex = true;
    muonVertexCollectionCuts.pop_back();
  }

  int nCuts = muonVertexCollectionCuts.size();
  for(int i = 0; i < nCuts; i++) {
    auto passedVertices = make_shared<PhysicsObjects>();
    for(auto vertex : *vertices) {
      bool passed = true;
      auto dimuonVertex = asNanoDimuonVertex(vertex, event);
      for(int j = 0; j < nCuts; j++) {
        if(j == i) continue;
        if(!ttAlpsCuts->PassesCut(dimuonVertex, muonVertexCollectionCuts[j])) {
          passed = false;
          break;
        }
      }
      if(passed) passedVertices->push_back(vertex);
    }
    string nminus1CollectionName = muonVertexCollectionName+"Nminus1"+muonVertexCollectionCuts[i];
    auto finalCollection = make_shared<PhysicsObjects>();
    if(bestVertex) {
      if(GetBestMuonVertex(passedVertices, event)) finalCollection->push_back(GetBestMuonVertex(passedVertices, event));
    }
    else finalCollection = passedVertices;
    event->AddCollection(nminus1CollectionName, finalCollection);
  }
}

bool TTAlpsObjectsManager::IsGoodBaseMuonVertex(const shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  auto dimuonVertex = asNanoDimuonVertex(vertex,event);
  if(!ttAlpsCuts->PassesLLPnanoAODVertexCuts(dimuonVertex)) return false;
  

  if(!ttAlpsCuts->PassesChargeCut(dimuonVertex)) return false;
  return true;
}

shared_ptr<PhysicsObject> TTAlpsObjectsManager::GetBestMuonVertex(const shared_ptr<PhysicsObjects> vertices, shared_ptr<Event> event) {
  if(vertices->size() == 0) return nullptr;
  if(vertices->size() == 1) return vertices->at(0);
  auto bestVertex = vertices->at(0);
  for(auto vertex : *vertices) {
    if((float)asNanoDimuonVertex(vertex,event)->Get("normChi2") < (float)asNanoDimuonVertex(bestVertex,event)->Get("normChi2")) {
      bestVertex = vertex;
    }
  }
  return bestVertex;
}

void TTAlpsObjectsManager::InsertMatchedLooseMuonEfficiencyCollections(shared_ptr<Event> event) {
  auto loosePATMuons = event->GetCollection("LoosePATMuons");
  auto looseDSAMuons = event->GetCollection("LooseDSAMuons");
  auto looseMuons = make_shared<PhysicsObjects>();
  for (auto muon : *loosePATMuons) {
    looseMuons->push_back(muon);
  }
  for (auto muon : *looseDSAMuons) {
    looseMuons->push_back(muon);
  }
  auto looseMuonsSegmentDRMatch = make_shared<PhysicsObjects>();
  shared_ptr<PhysicsObjects> looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons(looseMuons);
  shared_ptr<PhysicsObjects> looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons(looseMuons);
  shared_ptr<PhysicsObjects> looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons(looseMuons);

  for(auto muon : *looseMuonsSegmentMatch){
    float muon_idx = muon->Get("idx");
    if(asNanoEvent(event)->MuonIndexExist(looseMuonsDRMatch,muon_idx,asNanoMuon(muon)->isDSA())) {
      looseMuonsSegmentDRMatch->push_back(muon);
    }
  }
  event->AddCollection("LooseMuonsSegmentDRMatch", looseMuonsSegmentDRMatch);
  auto looseMuonsVertexSegmentDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentDRMatch);
  event->AddCollection("LooseMuonsVertexSegmentDRMatch", looseMuonsVertexSegmentDRMatch);

  auto looseMuonsSegmentOuterDRMatch = make_shared<PhysicsObjects>();
  for(auto muon : *looseMuonsSegmentMatch){
    float muon_idx = muon->Get("idx");
    if(asNanoEvent(event)->MuonIndexExist(looseMuonsOuterDRMatch,muon_idx,asNanoMuon(muon)->isDSA())) {
      looseMuonsSegmentOuterDRMatch->push_back(muon);
    }
  }
  event->AddCollection("LooseMuonsSegmentOuterDRMatch", looseMuonsSegmentOuterDRMatch);
  auto looseMuonsVertexSegmentOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentOuterDRMatch);
  event->AddCollection("LooseMuonsVertexSegmentOuterDRMatch", looseMuonsVertexSegmentOuterDRMatch);
}
