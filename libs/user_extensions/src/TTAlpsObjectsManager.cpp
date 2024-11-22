#include "TTAlpsObjectsManager.hpp"

#include "ConfigManager.hpp"
#include "Logger.hpp"

using namespace std;

TTAlpsObjectsManager::TTAlpsObjectsManager() {
  auto& config = ConfigManager::GetInstance();

  ttAlpsSelections = make_unique<TTAlpsDimuonSelections>();

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

  bool nonIso = false;
  try {
    config.GetValue("nonIsolatedLooseMuons", nonIso);
  } catch (const Exception &e) {
    info() << "Couldn't read nonIsolatedLooseMuons from config file - will use isolated LooseMuons collection with isolation cuts" << endl;
  }
  nonIsolatedLooseMuons = nonIso;
}

void TTAlpsObjectsManager::InsertMatchedLooseMuonsCollections(shared_ptr<Event> event) {

  auto loosePATMuons = event->GetCollection("LooseMuons");
  auto looseDSAMuons = event->GetCollection("LooseDSAMuons");
  if(nonIsolatedLooseMuons) loosePATMuons = event->GetCollection("LooseNonIsoMuons");
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
  shared_ptr<PhysicsObjects> looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons(maxDR, muonCollection);
  shared_ptr<PhysicsObjects> looseMuonVerticesDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsDRMatch);
  
  event->AddCollection("LooseMuonsDRMatch", looseMuonsDRMatch);
  event->AddCollection("LooseMuonsVertexDRMatch", looseMuonVerticesDRMatch);
}
  
void TTAlpsObjectsManager::InsertOuterDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR, shared_ptr<Collection<shared_ptr<PhysicsObject>>> muonCollection) {
  
  shared_ptr<PhysicsObjects> looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons(maxDR, muonCollection);
  shared_ptr<PhysicsObjects> looseMuonVerticesOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsOuterDRMatch);

  event->AddCollection("LooseMuonsOuterDRMatch", looseMuonsOuterDRMatch);
  event->AddCollection("LooseMuonsVertexOuterDRMatch", looseMuonVerticesOuterDRMatch);
}

void TTAlpsObjectsManager::InsertProximityDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR, shared_ptr<Collection<shared_ptr<PhysicsObject>>> muonCollection) {
  
  shared_ptr<PhysicsObjects> looseMuonsProxDRMatch = asNanoEvent(event)->GetProximityDRMatchedMuons(maxDR, muonCollection);
  shared_ptr<PhysicsObjects> looseMuonVerticesProxDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsProxDRMatch);

  event->AddCollection("LooseMuonsProxDRMatch", looseMuonsProxDRMatch);
  event->AddCollection("LooseMuonsVertexProxDRMatch", looseMuonVerticesProxDRMatch);
}

void TTAlpsObjectsManager::InsertSegmentMatchedLooseMuonsCollections(shared_ptr<Event> event, float minSegmentRatio, shared_ptr<Collection<shared_ptr<PhysicsObject>>> muonCollection) {

  shared_ptr<PhysicsObjects> looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons(minSegmentRatio, muonCollection);
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
  if(muonVertexCollectionCuts.back() == "BestDimuonVertex") {
    bestVertex = true;
    muonVertexCollectionCuts.pop_back();
  }
  auto passedVertices = make_shared<PhysicsObjects>();
  for(auto vertex : *vertices) {
    auto dimuonVertex = asNanoDimuonVertex(vertex, event);
    for(auto cutName : muonVertexCollectionCuts) {
      if(!ttAlpsSelections->PassesCut(dimuonVertex, cutName)) continue;
    }
    passedVertices->push_back(vertex);
  }

  auto finalCollection = make_shared<PhysicsObjects>();
  if(bestVertex) {
    if(GetBestMuonVertex(passedVertices, event)) finalCollection->push_back(GetBestMuonVertex(passedVertices, event));
  }
  else finalCollection = passedVertices;

  event->AddCollection(muonVertexCollectionName, passedVertices);
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
      auto dimuonVertex = asNanoDimuonVertex(vertex, event);
      for(int j = 0; j < nCuts; j++) {
        if(j == i) continue;
        if(!ttAlpsSelections->PassesCut(dimuonVertex, muonVertexCollectionCuts[j])) continue;
      }
      passedVertices->push_back(vertex);
    }

    auto finalCollection = make_shared<PhysicsObjects>();
    if(bestVertex) {
      if(GetBestMuonVertex(passedVertices, event)) finalCollection->push_back(GetBestMuonVertex(passedVertices, event));
    }
    else finalCollection = passedVertices;
    string nminus1CollectionName = muonVertexCollectionName+"Nminus1"+muonVertexCollectionCuts[i];
    event->AddCollection(nminus1CollectionName, passedVertices);
  }
}

bool TTAlpsObjectsManager::IsGoodBaseMuonVertex(const shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  auto dimuonVertex = asNanoDimuonVertex(vertex,event);
  if(!ttAlpsSelections->PassesLLPnanoAODVertexCuts(dimuonVertex)) return false;
  

  if(!ttAlpsSelections->PassesChargeCut(dimuonVertex)) return false;
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
  auto looseMuonsSegmentDRMatch = make_shared<PhysicsObjects>();
  shared_ptr<PhysicsObjects> looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons();
  shared_ptr<PhysicsObjects> looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons();
  shared_ptr<PhysicsObjects> looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons();

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
