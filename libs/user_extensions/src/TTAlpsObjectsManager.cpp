#include "TTAlpsObjectsManager.hpp"

#include "ConfigManager.hpp"
#include "Logger.hpp"

using namespace std;

TTAlpsObjectsManager::TTAlpsObjectsManager() {
  auto& config = ConfigManager::GetInstance();

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

}

void TTAlpsObjectsManager::InsertMatchedLooseMuonsCollections(shared_ptr<Event> event) {

  for(auto &[matchingMethod, param] : muonMatchingParams) {
    if(matchingMethod == "DR") {
      InsertDRMatchedLooseMuonsCollections(event, param);
      continue;
    }
    if(matchingMethod == "OuterDR") {
      InsertOuterDRMatchedLooseMuonsCollections(event, param);
      continue;
    }
    if(matchingMethod == "ProxDR") {
      InsertProximityDRMatchedLooseMuonsCollections(event, param);
      continue;
    }
    if(matchingMethod == "Segment") {
      InsertSegmentMatchedLooseMuonsCollections(event, param);
      continue;
    }
  }
}

void TTAlpsObjectsManager::InsertDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR) {
  shared_ptr<PhysicsObjects> looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons(maxDR);
  shared_ptr<PhysicsObjects> looseMuonVerticesDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsDRMatch);
  
  event->AddCollection("LooseMuonsDRMatch", looseMuonsDRMatch);
  event->AddCollection("LooseMuonsVertexDRMatch", looseMuonVerticesDRMatch);
}
  
void TTAlpsObjectsManager::InsertOuterDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR) {
  
  shared_ptr<PhysicsObjects> looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons(maxDR);
  shared_ptr<PhysicsObjects> looseMuonVerticesOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsOuterDRMatch);

  event->AddCollection("LooseMuonsOuterDRMatch", looseMuonsOuterDRMatch);
  event->AddCollection("LooseMuonsVertexOuterDRMatch", looseMuonVerticesOuterDRMatch);
}

void TTAlpsObjectsManager::InsertProximityDRMatchedLooseMuonsCollections(shared_ptr<Event> event, float maxDR) {
  
  shared_ptr<PhysicsObjects> looseMuonsProxDRMatch = asNanoEvent(event)->GetProximityDRMatchedMuons(maxDR);
  shared_ptr<PhysicsObjects> looseMuonVerticesProxDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsProxDRMatch);

  event->AddCollection("LooseMuonsProxDRMatch", looseMuonsProxDRMatch);
  event->AddCollection("LooseMuonsVertexProxDRMatch", looseMuonVerticesProxDRMatch);
}

void TTAlpsObjectsManager::InsertSegmentMatchedLooseMuonsCollections(shared_ptr<Event> event, float minSegmentRatio) {

  shared_ptr<PhysicsObjects> looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons(minSegmentRatio);
  shared_ptr<PhysicsObjects> looseMuonVerticesSegmentMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentMatch);
  
  event->AddCollection("LooseMuonsSegmentMatch", looseMuonsSegmentMatch);
  event->AddCollection("LooseMuonsVertexSegmentMatch", looseMuonVerticesSegmentMatch);
}

void TTAlpsObjectsManager::InsertGoodLooseMuonVertexCollection(shared_ptr<Event> event) {
  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  auto vertices = event->GetCollection("LooseMuonsVertex"+matchingMethod+"Match");
  auto goodVertices = make_shared<PhysicsObjects>();
  auto goodVerticesTight = make_shared<PhysicsObjects>();
  auto maskedVertices = make_shared<PhysicsObjects>();
  auto goodMaskedVertices = make_shared<PhysicsObjects>();
  auto bestVertex = make_shared<PhysicsObjects>();
  auto secondBestVertex = make_shared<PhysicsObjects>();
  auto goodBestVertex = make_shared<PhysicsObjects>();
  auto goodSecondBestVertex = make_shared<PhysicsObjects>();
  auto goodBestVertexTight = make_shared<PhysicsObjects>();
  auto goodSecondBestVertexTight = make_shared<PhysicsObjects>();

  for(auto vertex : *vertices) {
    if(IsGoodMuonVertex(vertex, event)) {
      goodVertices->push_back(vertex);
      if(IsGoodMuonVertexTight(vertex, event)) goodVerticesTight->push_back(vertex);
    }
    if(IsGoodMaskedMuonVertex(vertex, event)) {
      maskedVertices->push_back(vertex);
      if(IsGoodMuonVertex(vertex, event)) goodMaskedVertices->push_back(vertex);
    }
  }

  if(GetBestMuonVertex(maskedVertices, event)) bestVertex->push_back(GetBestMuonVertex(maskedVertices, event));
  if(GetSecondBestMuonVertex(maskedVertices, event)) secondBestVertex->push_back(GetSecondBestMuonVertex(maskedVertices, event));
  if(bestVertex->size()>0) {
    if(IsGoodMuonVertex(bestVertex->at(0), event)) goodBestVertex->push_back(bestVertex->at(0));
    if(IsGoodMuonVertexTight(bestVertex->at(0), event)) {
      goodBestVertexTight->push_back(bestVertex->at(0));
      std::cout << "goodBestVertexTight" << std::endl;
    }
  }
  if(secondBestVertex->size()>0) {
    if(IsGoodMuonVertex(secondBestVertex->at(0), event)) goodSecondBestVertex->push_back(secondBestVertex->at(0));
    if(IsGoodMuonVertexTight(secondBestVertex->at(0), event)) goodSecondBestVertexTight->push_back(secondBestVertex->at(0));
  }
  
  event->AddCollection("MaskedLooseMuonsVertex", maskedVertices);
  event->AddCollection("GoodLooseMuonsVertex", goodVertices);
  event->AddCollection("GoodLooseMuonsVertexTight", goodVertices);
  event->AddCollection("GoodMaskedLooseMuonsVertex", goodMaskedVertices);
  event->AddCollection("BestLooseMuonsVertex", bestVertex);
  event->AddCollection("SecondBestLooseMuonsVertex", secondBestVertex);
  event->AddCollection("GoodBestLooseMuonsVertex", goodBestVertex);
  event->AddCollection("GoodSecondBestLooseMuonsVertex", goodSecondBestVertex);
  event->AddCollection("GoodBestLooseMuonsVertexTight", goodBestVertexTight);
  event->AddCollection("GoodSecondBestLooseMuonsVertexTight", goodSecondBestVertexTight);
}

void TTAlpsObjectsManager::InsertMatchedLooseMuonEfficiencyCollections(shared_ptr<Event> event) {
  auto looseMuonsSegmentDRMatch = make_shared<PhysicsObjects>();
  shared_ptr<PhysicsObjects> looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons();
  shared_ptr<PhysicsObjects> looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons();
  shared_ptr<PhysicsObjects> looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons();
  // auto looseMuonsDRMatch = event->GetCollection("LooseMuonsDRMatch");
  // auto looseMuonsOuterDRMatch = event->GetCollection("LooseMuonsOuterDRMatch");
  // auto looseMuonsSegmentMatch = event->GetCollection("LooseMuonsSegmentMatch");

  for(auto muon : *looseMuonsSegmentMatch){
    float muon_idx = muon->Get("idx");
    if(asNanoEvent(event)->MuonIndexExist(looseMuonsDRMatch,muon_idx,asNanoMuon(muon)->isDSAMuon())) {
      looseMuonsSegmentDRMatch->push_back(muon);
    }
  }
  event->AddCollection("LooseMuonsSegmentDRMatch", looseMuonsSegmentDRMatch);
  auto looseMuonsVertexSegmentDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentDRMatch);
  event->AddCollection("LooseMuonsVertexSegmentDRMatch", looseMuonsVertexSegmentDRMatch);

  auto looseMuonsSegmentOuterDRMatch = make_shared<PhysicsObjects>();
  for(auto muon : *looseMuonsSegmentMatch){
    float muon_idx = muon->Get("idx");
    if(asNanoEvent(event)->MuonIndexExist(looseMuonsOuterDRMatch,muon_idx,asNanoMuon(muon)->isDSAMuon())) {
      looseMuonsSegmentOuterDRMatch->push_back(muon);
    }
  }
  event->AddCollection("LooseMuonsSegmentOuterDRMatch", looseMuonsSegmentOuterDRMatch);
  auto looseMuonsVertexSegmentOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentOuterDRMatch);
  event->AddCollection("LooseMuonsVertexSegmentOuterDRMatch", looseMuonsVertexSegmentOuterDRMatch);

}

bool TTAlpsObjectsManager::IsGoodMuonVertex(const shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  auto dimuonVertex = asNanoDimuonVertex(vertex,event);
    std::string category = dimuonVertex->GetVertexCategory();
  if (!dimuonVertex->isValid()) return false;
  if (!(float)dimuonVertex->Get("dca") < dimuonVertexCuts["maxBaseDCA"]) return false;
  
  int hitsInFrontOfVertex = 0;
  if((float)dimuonVertex->Get("hitsInFrontOfVert1") > 0) hitsInFrontOfVertex += (float)dimuonVertex->Get("hitsInFrontOfVert1");
  if((float)dimuonVertex->Get("hitsInFrontOfVert2") > 0) hitsInFrontOfVertex += (float)dimuonVertex->Get("hitsInFrontOfVert2");

  if(category == "PatDSA" && !hitsInFrontOfVertex < dimuonVertexCuts["maxHitsInFrontOfVertexPatDSA"]) return false;
  if(category == "Pat" && !hitsInFrontOfVertex < dimuonVertexCuts["maxHitsInFrontOfVertexPat"]) return false;
  if(category == "DSA" && !hitsInFrontOfVertex < dimuonVertexCuts["maxHitsInFrontOfVertexDSA"]) return false;

  if(category == "PatDSA" && !abs(dimuonVertex->GetPATpTLxyDPhi()) < dimuonVertexCuts["maxPATpTLxyDPhiPatDSA"]) return false;
  
  if(!(float)dimuonVertex->Get("normChi2") < dimuonVertexCuts["maxChi2"]) return false;

  return true;
}

bool TTAlpsObjectsManager::IsGoodMuonVertexTight(const shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  if (!IsGoodMuonVertex(vertex,event)) return false;
  auto dimuonVertex = asNanoDimuonVertex(vertex,event);
  std::string category = dimuonVertex->GetVertexCategory();
  if(!abs(dimuonVertex->GetCollinearityAngle()) < dimuonVertexCuts["maxCollinearityAngle"]) return false;

  if(category == "PatDSA" && !(float)dimuonVertex->Get("dRprox") < dimuonVertexCuts["maxProxDRPatDSA"]) return false;
  if(category == "Pat" && !(float)dimuonVertex->Get("dR ") < dimuonVertexCuts["maxDRPat"]) return false;
  if(category == "DSA" && !dimuonVertex->GetOuterDeltaR() < dimuonVertexCuts["maxOuterDRDSA"]) return false;
  
  return true;
}

bool TTAlpsObjectsManager::IsGoodMaskedMuonVertex(const shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  auto dimuonVertex = asNanoDimuonVertex(vertex,event);
  if (!dimuonVertex->isValid()) return false;
  if (!(float)dimuonVertex->Get("dca") < dimuonVertexCuts["maxBaseDCA"]) return false;
  float invMass = dimuonVertex->GetInvariantMass();
  if(invMass > dimuonVertexCuts["maxInvariantMass"]) return false;
  if(invMass > dimuonVertexCuts["minJpsiMass"] && invMass < dimuonVertexCuts["maxJpsiMass"]) return false;
  if(invMass > dimuonVertexCuts["minpsiMass"] && invMass < dimuonVertexCuts["maxpsiMass"]) return false;
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

shared_ptr<PhysicsObject> TTAlpsObjectsManager::GetSecondBestMuonVertex(const shared_ptr<PhysicsObjects> vertices, shared_ptr<Event> event) {
  if(vertices->size() == 0) return nullptr;
  if(vertices->size() == 1) return nullptr;
  auto bestVertex = GetBestMuonVertex(vertices,event);
  auto secondBestVertex = vertices->at(0);
  for(auto vertex : *vertices) {
    if(vertex == bestVertex) continue;
    if((float)asNanoDimuonVertex(vertex,event)->Get("normChi2") < (float)asNanoDimuonVertex(secondBestVertex,event)->Get("normChi2")) {
      secondBestVertex = vertex;
    }
  }
  return secondBestVertex;
}
