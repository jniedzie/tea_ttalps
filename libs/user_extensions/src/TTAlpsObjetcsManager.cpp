#include "TTAlpsObjectsManager.hpp"

#include "ConfigManager.hpp"
#include "Logger.hpp"

using namespace std;

TTAlpsObjectsManager::TTAlpsObjectsManager() {
  auto& config = ConfigManager::GetInstance();
}

void TTAlpsObjectsManager::InsertLooseMuonsMatchedCollections(shared_ptr<Event> event) {

  shared_ptr<PhysicsObjects> looseMuonsDRMatch = asNanoEvent(event)->GetDRMatchedMuons(0.1);
  shared_ptr<PhysicsObjects> looseMuonsOuterDRMatch = asNanoEvent(event)->GetOuterDRMatchedMuons(0.1);
  shared_ptr<PhysicsObjects> looseMuonsSegmentMatch = asNanoEvent(event)->GetSegmentMatchedMuons();
  
  event->AddCollection("LooseMuonsDRMatch", looseMuonsDRMatch);
  event->AddCollection("LooseMuonsOuterDRMatch", looseMuonsOuterDRMatch);
  event->AddCollection("LooseMuonsSegmentMatch", looseMuonsSegmentMatch);
}

void TTAlpsObjectsManager::InsertLooseMuonVerticesMatchedCollections(shared_ptr<Event> event) {
  auto looseMuonsDRMatch = event->GetCollection("LooseMuonsDRMatch");
  auto looseMuonsOuterDRMatch = event->GetCollection("LooseMuonsOuterDRMatch");
  auto looseMuonsSegmentMatch = event->GetCollection("LooseMuonsSegmentMatch");

  shared_ptr<PhysicsObjects> looseMuonVerticesDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsDRMatch);
  shared_ptr<PhysicsObjects> looseMuonVerticesOuterDRMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsOuterDRMatch);
  shared_ptr<PhysicsObjects> looseMuonVerticesSegmentMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentMatch);
  
  event->AddCollection("LooseMuonsVertexDRMatch", looseMuonVerticesDRMatch);
  event->AddCollection("LooseMuonsVertexOuterDRMatch", looseMuonVerticesOuterDRMatch);
  event->AddCollection("LooseMuonsVertexSegmentMatch", looseMuonVerticesSegmentMatch);
}

void TTAlpsObjectsManager::InsertGoodLooseMuonVertexCollection(shared_ptr<Event> event) {
  // Only segment matched muons for now
  auto vertices = event->GetCollection("LooseMuonsVertexSegmentMatch");
  auto goodVertices = make_shared<PhysicsObjects>();
  auto goodMuons = make_shared<PhysicsObjects>();

  for(auto vertex : *vertices) {
    if(!IsGoodMuonVertex(vertex, event)) continue;
    goodVertices->push_back(vertex);
  }
  event->AddCollection("GoodLooseMuonsVertex", goodVertices);
}

void TTAlpsObjectsManager::InsertLooseMuonMatchingEfficiencyCollections(shared_ptr<Event> event) {
  auto looseMuonsSegmentDRMatch = make_shared<PhysicsObjects>();
  auto looseMuonsDRMatch = event->GetCollection("LooseMuonsDRMatch");
  auto looseMuonsOuterDRMatch = event->GetCollection("LooseMuonsOuterDRMatch");
  auto looseMuonsSegmentMatch = event->GetCollection("LooseMuonsSegmentMatch");

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

bool TTAlpsObjectsManager::IsGoodMuonVertex(const std::shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  if (!asNanoDimuonVertex(vertex)->PassesDimuonChargeCut(event)) return false;
  if (!asNanoDimuonVertex(vertex)->PassesChi2Cut()) return false;
  if (!asNanoDimuonVertex(vertex)->PassesDeltaRCut()) return false;
  return true;
}