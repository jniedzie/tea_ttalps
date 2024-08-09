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

void TTAlpsObjectsManager::InsertGoodLooseMuonVertexCollection(shared_ptr<Event> event) {
  
  if(muonMatchingParams.size() == 0) {
    error() << "Requested to insert GoodLooseMuonVertex collection, but no muonMatchingParams are set in the config file." << endl;
    return;
  }
  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  auto vertices = event->GetCollection("LooseMuonsVertex"+matchingMethod+"Match");
  auto baseVertices = make_shared<PhysicsObjects>();
  auto baseDimuonVertices = make_shared<PhysicsObjects>();
  auto bestVertex = make_shared<PhysicsObjects>();
  auto bestDimuonVertex = make_shared<PhysicsObjects>();
  auto goodBestDimuonVertex = make_shared<PhysicsObjects>();
  auto goodBestDimuonVertexTight = make_shared<PhysicsObjects>();

  for(auto vertex : *vertices) {
    if(IsGoodBaseMuonVertex(vertex, event)) {
      baseVertices->push_back(vertex); 
      if(IsGoodDimuonVertex(vertex, event)) baseDimuonVertices->push_back(vertex);
    }
  }

  if(GetBestMuonVertex(baseDimuonVertices, event)) bestDimuonVertex->push_back(GetBestMuonVertex(baseDimuonVertices, event));
  if(bestDimuonVertex->size()>0) {
    if(IsGoodBestDimuonVertex(bestDimuonVertex->at(0), event)) goodBestDimuonVertex->push_back(bestDimuonVertex->at(0));
  }
  event->AddCollection("BaseLooseMuonsVertex", baseVertices);
  event->AddCollection("BaseLooseDimuonsVertex", baseDimuonVertices);
  event->AddCollection("BestLooseMuonsVertex", bestVertex);
  event->AddCollection("BestLooseDimuonsVertex", bestDimuonVertex);
  event->AddCollection("GoodBestLooseDimuonsVertex", goodBestDimuonVertex);
}

void TTAlpsObjectsManager::InsertNminus1VertexCollections(shared_ptr<Event> event) {  
  if(muonMatchingParams.size() == 0) {
    error() << "Requested to insert GoodLooseMuonVertex collection, but no muonMatchingParams are set in the config file." << endl;
    return;
  }

  // if(nonIsolatedLooseMuons) InsertNonIsolatedNminus1VertexCollections(event);
  // else InsertIsolatedNminus1VertexCollections(event);
  InsertIsolatedNminus1VertexCollections(event);
}

void TTAlpsObjectsManager::InsertIsolatedNminus1VertexCollections(shared_ptr<Event> event) {  
  if(muonMatchingParams.size() == 0) {
    error() << "Requested to insert GoodLooseMuonVertex collection, but no muonMatchingParams are set in the config file." << endl;
    return;
  }
  // Only first matching method for now
  string matchingMethod = muonMatchingParams.begin()->first;
  auto vertices = event->GetCollection("LooseMuonsVertex"+matchingMethod+"Match");
  auto verticesNminus1All = make_shared<PhysicsObjects>();
  auto verticesNminus1Collinearity = make_shared<PhysicsObjects>();
  auto verticesNminus1DCA = make_shared<PhysicsObjects>();
  auto verticesNminus1DPhiMuonpTLxy = make_shared<PhysicsObjects>();
  auto verticesNminus1HitsInFrontOfVertex = make_shared<PhysicsObjects>();
  auto verticesNminus1Charge = make_shared<PhysicsObjects>();
  auto verticesNminus1DR = make_shared<PhysicsObjects>();
  auto bestVertex = make_shared<PhysicsObjects>();
  auto bestVertexNminus1Collinearity = make_shared<PhysicsObjects>();
  auto bestVertexNminus1DCA = make_shared<PhysicsObjects>();
  auto bestVertexNminus1DPhiMuonpTLxy = make_shared<PhysicsObjects>();
  auto bestVertexNminus1HitsInFrontOfVertex = make_shared<PhysicsObjects>();
  auto bestVertexNminus1Charge = make_shared<PhysicsObjects>();
  auto bestVertexNminus1DR = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1Collinearity = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1DCA = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1DPhiMuonpTLxy = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1HitsInFrontOfVertex = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1Charge = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1Chi2 = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1DR = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1All = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1AllVxy = make_shared<PhysicsObjects>();
  auto verticesNminus1Iso = make_shared<PhysicsObjects>();
  auto bestVertexNminus1Iso = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1Iso = make_shared<PhysicsObjects>();
  auto verticesNminus1InvMass = make_shared<PhysicsObjects>();
  auto bestVertexNminus1InvMass = make_shared<PhysicsObjects>();
  auto goodBestVertexNminus1InvMass = make_shared<PhysicsObjects>();

  for(auto vertex : *vertices) {
    auto dimuonVertex = asNanoDimuonVertex(vertex,event);
    if(!ttAlpsSelections->PassesLLPnanoAODVertexCuts(dimuonVertex)) continue;
    
    if(ttAlpsSelections->PassesInvariantMassCuts(dimuonVertex) &&
      ttAlpsSelections->PassesChargeCut(dimuonVertex) &&
      ttAlpsSelections->PassesHitsInFrontOfVertexCut(dimuonVertex) &&
      ttAlpsSelections->PassesDPhiBetweenMuonpTAndLxyCut(dimuonVertex) &&
      ttAlpsSelections->PassesDCACut(dimuonVertex) &&
      ttAlpsSelections->PassesCollinearityAngleCut(dimuonVertex) &&
      ttAlpsSelections->PassesDisplacedIsolationCut(dimuonVertex, "displacedTrackIso03Dimuon") &&
      ttAlpsSelections->PassesDeltaRCut(dimuonVertex)) {
        verticesNminus1All->push_back(vertex);
    }
    if(ttAlpsSelections->PassesInvariantMassCuts(dimuonVertex) &&
      ttAlpsSelections->PassesChargeCut(dimuonVertex) &&
      ttAlpsSelections->PassesHitsInFrontOfVertexCut(dimuonVertex) &&
      ttAlpsSelections->PassesDPhiBetweenMuonpTAndLxyCut(dimuonVertex) &&
      ttAlpsSelections->PassesDCACut(dimuonVertex) &&
      ttAlpsSelections->PassesCollinearityAngleCut(dimuonVertex) &&
      ttAlpsSelections->PassesDeltaRCut(dimuonVertex)) {
        verticesNminus1Iso->push_back(vertex);
    }
    if(ttAlpsSelections->PassesInvariantMassCuts(dimuonVertex) &&
      ttAlpsSelections->PassesChargeCut(dimuonVertex) &&
      ttAlpsSelections->PassesHitsInFrontOfVertexCut(dimuonVertex) &&
      ttAlpsSelections->PassesDPhiBetweenMuonpTAndLxyCut(dimuonVertex) &&
      ttAlpsSelections->PassesDCACut(dimuonVertex) &&
      ttAlpsSelections->PassesDisplacedIsolationCut(dimuonVertex, "displacedTrackIso03Dimuon") &&
      ttAlpsSelections->PassesDeltaRCut(dimuonVertex)) {
        verticesNminus1Collinearity->push_back(vertex);
    }
    if(ttAlpsSelections->PassesInvariantMassCuts(dimuonVertex) &&
      ttAlpsSelections->PassesChargeCut(dimuonVertex) &&
      ttAlpsSelections->PassesHitsInFrontOfVertexCut(dimuonVertex) &&
      ttAlpsSelections->PassesDPhiBetweenMuonpTAndLxyCut(dimuonVertex) &&
      ttAlpsSelections->PassesCollinearityAngleCut(dimuonVertex) &&
      ttAlpsSelections->PassesDisplacedIsolationCut(dimuonVertex, "displacedTrackIso03Dimuon") &&
      ttAlpsSelections->PassesDeltaRCut(dimuonVertex)) {
        verticesNminus1DCA->push_back(vertex);
    }
    if(ttAlpsSelections->PassesInvariantMassCuts(dimuonVertex) &&
      ttAlpsSelections->PassesChargeCut(dimuonVertex) &&
      ttAlpsSelections->PassesHitsInFrontOfVertexCut(dimuonVertex) &&
      ttAlpsSelections->PassesDCACut(dimuonVertex) &&
      ttAlpsSelections->PassesCollinearityAngleCut(dimuonVertex) &&
      ttAlpsSelections->PassesDisplacedIsolationCut(dimuonVertex, "displacedTrackIso03Dimuon") &&
      ttAlpsSelections->PassesDeltaRCut(dimuonVertex)) {
        verticesNminus1DPhiMuonpTLxy->push_back(vertex);
    }
    if(ttAlpsSelections->PassesInvariantMassCuts(dimuonVertex) &&
      ttAlpsSelections->PassesChargeCut(dimuonVertex) &&
      ttAlpsSelections->PassesDPhiBetweenMuonpTAndLxyCut(dimuonVertex) &&
      ttAlpsSelections->PassesDCACut(dimuonVertex) &&
      ttAlpsSelections->PassesCollinearityAngleCut(dimuonVertex) &&
      ttAlpsSelections->PassesDisplacedIsolationCut(dimuonVertex, "displacedTrackIso03Dimuon") &&
      ttAlpsSelections->PassesDeltaRCut(dimuonVertex)) {
        verticesNminus1HitsInFrontOfVertex->push_back(vertex);
    }
    if(ttAlpsSelections->PassesInvariantMassCuts(dimuonVertex) &&
      ttAlpsSelections->PassesHitsInFrontOfVertexCut(dimuonVertex) &&
      ttAlpsSelections->PassesDPhiBetweenMuonpTAndLxyCut(dimuonVertex) &&
      ttAlpsSelections->PassesDCACut(dimuonVertex) &&
      ttAlpsSelections->PassesCollinearityAngleCut(dimuonVertex) &&
      ttAlpsSelections->PassesDisplacedIsolationCut(dimuonVertex, "displacedTrackIso03Dimuon") &&
      ttAlpsSelections->PassesDeltaRCut(dimuonVertex)) {
        verticesNminus1Charge->push_back(vertex);
    }
    if(ttAlpsSelections->PassesChargeCut(dimuonVertex) &&
      ttAlpsSelections->PassesHitsInFrontOfVertexCut(dimuonVertex) &&
      ttAlpsSelections->PassesDPhiBetweenMuonpTAndLxyCut(dimuonVertex) &&
      ttAlpsSelections->PassesDCACut(dimuonVertex) &&
      ttAlpsSelections->PassesCollinearityAngleCut(dimuonVertex) &&
      ttAlpsSelections->PassesDisplacedIsolationCut(dimuonVertex, "displacedTrackIso03Dimuon") &&
      ttAlpsSelections->PassesDeltaRCut(dimuonVertex)) {
        verticesNminus1InvMass->push_back(vertex);
    }
    if(ttAlpsSelections->PassesInvariantMassCuts(dimuonVertex) &&
      ttAlpsSelections->PassesChargeCut(dimuonVertex) &&
      ttAlpsSelections->PassesHitsInFrontOfVertexCut(dimuonVertex) &&
      ttAlpsSelections->PassesDPhiBetweenMuonpTAndLxyCut(dimuonVertex) &&
      ttAlpsSelections->PassesDCACut(dimuonVertex) &&
      ttAlpsSelections->PassesCollinearityAngleCut(dimuonVertex) &&
      ttAlpsSelections->PassesDisplacedIsolationCut(dimuonVertex, "displacedTrackIso03Dimuon")) {
        verticesNminus1DR->push_back(vertex);
    }
  }

  if(GetBestMuonVertex(verticesNminus1All, event)) bestVertex->push_back(GetBestMuonVertex(verticesNminus1All, event));
  if(GetBestMuonVertex(verticesNminus1DCA, event)) bestVertexNminus1DCA->push_back(GetBestMuonVertex(verticesNminus1DCA, event));
  if(GetBestMuonVertex(verticesNminus1DPhiMuonpTLxy, event)) bestVertexNminus1DPhiMuonpTLxy->push_back(GetBestMuonVertex(verticesNminus1DPhiMuonpTLxy, event));
  if(GetBestMuonVertex(verticesNminus1HitsInFrontOfVertex, event)) bestVertexNminus1HitsInFrontOfVertex->push_back(GetBestMuonVertex(verticesNminus1HitsInFrontOfVertex, event));
  if(GetBestMuonVertex(verticesNminus1Charge, event)) bestVertexNminus1Charge->push_back(GetBestMuonVertex(verticesNminus1Charge, event));
  if(GetBestMuonVertex(verticesNminus1Collinearity, event)) bestVertexNminus1Collinearity->push_back(GetBestMuonVertex(verticesNminus1Collinearity, event));
  if(GetBestMuonVertex(verticesNminus1Iso, event)) bestVertexNminus1Iso->push_back(GetBestMuonVertex(verticesNminus1Iso, event));
  if(GetBestMuonVertex(verticesNminus1InvMass, event)) bestVertexNminus1InvMass->push_back(GetBestMuonVertex(verticesNminus1InvMass, event));
  if(GetBestMuonVertex(verticesNminus1DR, event)) bestVertexNminus1DR->push_back(GetBestMuonVertex(verticesNminus1DR, event));

  if(verticesNminus1All->size()>0) {
    auto dimuonVertex = asNanoDimuonVertex(bestVertex->at(0),event);
    goodBestVertexNminus1Chi2->push_back(bestVertex->at(0));

    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex)) goodBestVertexNminus1All->push_back(bestVertex->at(0));
    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex) && ttAlpsSelections->PassesVxyCut(dimuonVertex)) goodBestVertexNminus1AllVxy->push_back(bestVertex->at(0));
  }
  if(bestVertexNminus1Collinearity->size()>0) {
    auto dimuonVertex = asNanoDimuonVertex(bestVertexNminus1Collinearity->at(0),event);
    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex)) {
        goodBestVertexNminus1Collinearity->push_back(bestVertexNminus1Collinearity->at(0));
    }
  }
  if(bestVertexNminus1DCA->size()>0) {
    auto dimuonVertex = asNanoDimuonVertex(bestVertexNminus1DCA->at(0),event);
    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex)) {
        goodBestVertexNminus1DCA->push_back(bestVertexNminus1DCA->at(0));
    }
  }
  if(bestVertexNminus1DPhiMuonpTLxy->size()>0) {
    auto dimuonVertex = asNanoDimuonVertex(bestVertexNminus1DPhiMuonpTLxy->at(0),event);
    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex)) {
        goodBestVertexNminus1DPhiMuonpTLxy->push_back(bestVertexNminus1DPhiMuonpTLxy->at(0));
    }
  }
  if(bestVertexNminus1HitsInFrontOfVertex->size()>0) {
    auto dimuonVertex = asNanoDimuonVertex(bestVertexNminus1HitsInFrontOfVertex->at(0),event);
    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex)) {
        goodBestVertexNminus1HitsInFrontOfVertex->push_back(bestVertexNminus1HitsInFrontOfVertex->at(0));
    }
  }
  if(bestVertexNminus1Charge->size()>0) {
    auto dimuonVertex = asNanoDimuonVertex(bestVertexNminus1Charge->at(0),event);
    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex)) {
        goodBestVertexNminus1Charge->push_back(bestVertexNminus1Charge->at(0));
    }
  }
  if(bestVertexNminus1Iso->size()>0) {
    auto dimuonVertex = asNanoDimuonVertex(bestVertexNminus1Iso->at(0),event);
    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex)) {
        goodBestVertexNminus1Iso->push_back(bestVertexNminus1Iso->at(0));
    }
  }
  if(bestVertexNminus1InvMass->size()>0) {
    auto dimuonVertex = asNanoDimuonVertex(bestVertexNminus1InvMass->at(0),event);
    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex)) {
        goodBestVertexNminus1InvMass->push_back(bestVertexNminus1InvMass->at(0));
    }
  }
  if(bestVertexNminus1DR->size()>0) {
    auto dimuonVertex = asNanoDimuonVertex(bestVertexNminus1DR->at(0),event);
    if(ttAlpsSelections->PassesChi2Cut(dimuonVertex)) {
        goodBestVertexNminus1DR->push_back(bestVertexNminus1DR->at(0));
    }
  }
  
  event->AddCollection("GoodBestVertexNminus1Collinearity", goodBestVertexNminus1Collinearity);
  event->AddCollection("GoodBestVertexNminus1DCA", goodBestVertexNminus1DCA);
  event->AddCollection("GoodBestVertexNminus1DPhiMuonpTLxy", goodBestVertexNminus1DPhiMuonpTLxy);
  event->AddCollection("GoodBestVertexNminus1HitsInFrontOfVertex", goodBestVertexNminus1HitsInFrontOfVertex);
  event->AddCollection("GoodBestVertexNminus1Charge", goodBestVertexNminus1Charge);
  event->AddCollection("GoodBestVertexNminus1Chi2", goodBestVertexNminus1Chi2);
  event->AddCollection("GoodBestVertexNminus1DR", goodBestVertexNminus1DR);
  event->AddCollection("GoodBestVertexNminus1All", goodBestVertexNminus1All);
  event->AddCollection("GoodBestVertexNminus1AllVxy", goodBestVertexNminus1AllVxy);
  event->AddCollection("GoodBestVertexNminus1Iso", goodBestVertexNminus1Iso);
  event->AddCollection("GoodBestVertexNminus1InvMass", goodBestVertexNminus1InvMass);
}

bool TTAlpsObjectsManager::IsGoodBaseMuonVertex(const shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  auto dimuonVertex = asNanoDimuonVertex(vertex,event);
  if(!ttAlpsSelections->PassesLLPnanoAODVertexCuts(dimuonVertex)) return false;

  if(!ttAlpsSelections->PassesInvariantMassCuts(dimuonVertex)) return false;
  if(!ttAlpsSelections->PassesChargeCut(dimuonVertex)) return false;
  return true;
}

bool TTAlpsObjectsManager::IsGoodBestDimuonVertex(const shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  auto dimuonVertex = asNanoDimuonVertex(vertex,event);
  
  if(!ttAlpsSelections->PassesChi2Cut(dimuonVertex)) return false;
  if(!ttAlpsSelections->PassesDeltaRCut(dimuonVertex)) return false;  
  return true;
}

bool TTAlpsObjectsManager::IsGoodDimuonVertex(const shared_ptr<PhysicsObject> vertex, shared_ptr<Event> event) {
  auto dimuonVertex = asNanoDimuonVertex(vertex,event);

  if(!ttAlpsSelections->PassesHitsInFrontOfVertexCut(dimuonVertex)) return false;
  if(!ttAlpsSelections->PassesDPhiBetweenMuonpTAndLxyCut(dimuonVertex)) return false;
  if(!ttAlpsSelections->PassesDCACut(dimuonVertex)) return false;
  if(!ttAlpsSelections->PassesCollinearityAngleCut(dimuonVertex)) return false;
  if(!ttAlpsSelections->PassesDisplacedIsolationCut(dimuonVertex, "displacedTrackIso03Dimuon")) return false;
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
