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
    if (muonMatchingParams.empty()) {
      muonVertexCollectionInput = "";
    } else {
      string matchingMethod = muonMatchingParams.begin()->first;
      muonVertexCollectionInput = "LooseMuonsVertex" + matchingMethod + "Match";
    }
  }
  try {
    config.GetValue("applySegmentMatchingAfterSelections", applySegmentMatchingAfterSelections);
  } catch (const Exception &e) {
    warn() << "Couldn't read applySegmentMatchingAfterSelections from config file - is needed to apply matching after dimuon selection" << endl;
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
      float minSegmentRatio = param;
      if (applySegmentMatchingAfterSelections) {
        minSegmentRatio = 1.5; // no segment matching applied here
      }
      InsertSegmentMatchedLooseMuonsCollections(event, minSegmentRatio, looseMuons);
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
  auto looseDSAMuonsSegmentMatch = make_shared<PhysicsObjects>();
  auto loosePATMuonsSegmentMatch = make_shared<PhysicsObjects>();
  for (auto muon : *looseMuonsSegmentMatch) {
    if (muon->IsDSA()) looseDSAMuonsSegmentMatch->push_back(muon->GetPhysicsObject());
    else loosePATMuonsSegmentMatch->push_back(muon->GetPhysicsObject());
  }
  event->AddCollection("LooseDSAMuonsSegmentMatch", looseDSAMuonsSegmentMatch);
  event->AddCollection("LoosePATMuonsSegmentMatch", loosePATMuonsSegmentMatch);

  try {
    auto looseMuonVerticesSegmentMatch = asNanoEvent(event)->GetVerticesForMuons(looseMuonsSegmentMatch);
    event->AddCollection("LooseMuonsVertexSegmentMatch", looseMuonVerticesSegmentMatch);
  } catch (const Exception &e) {
    warn() << "Couldn't get vertices for segment matched muons. Collection will not be inserted." << endl;
  }
}

void TTAlpsObjectsManager::InsertNonLeadingLooseMuonsCollections(shared_ptr<Event> event) {
  
  auto tightMuons = event->GetCollection("TightMuons");
  auto leadingTightMuon = asTTAlpsEvent(event)->GetLeadingMuon(asNanoMuons(tightMuons));
  auto loosePATMuons = event->GetCollection("LoosePATMuons");
  auto looseDisplacedPATMuons = event->GetCollection("LooseDisplacedPATMuons");
  auto looseDSAMuons = event->GetCollection("LooseDSAMuons");
  
  auto looseMuonsSegmentMatch = make_shared<PhysicsObjects>();
  auto looseMuonsVertexSegmentMatch = make_shared<PhysicsObjects>();
  if (muonMatchingParams.find("Segment") != muonMatchingParams.end()) {
    looseMuonsSegmentMatch = event->GetCollection("LooseMuonsSegmentMatch");
    looseMuonsVertexSegmentMatch = event->GetCollection("LooseMuonsVertexSegmentMatch");
  }

  // No leading tight muon in the event
  if (!leadingTightMuon) {
    event->AddCollection("LooseNonLeadingPATMuons", loosePATMuons);
    event->AddCollection("LooseNonLeadingDisplacedPATMuons", looseDisplacedPATMuons);
    if (muonMatchingParams.size() != 0) {
      event->AddCollection("LooseNonLeadingMuonsSegmentMatch", looseMuonsSegmentMatch);
      event->AddCollection("LooseNonLeadingMuonsVertexSegmentMatch", looseMuonsVertexSegmentMatch);
    }
    return;
  }

  // Non-leading muon (vertex) collections
  auto looseNonLeadingPATMuons = make_shared<PhysicsObjects>();
  for (auto muon : *loosePATMuons) {
    if (muon == leadingTightMuon->GetPhysicsObject())
      continue;
    looseNonLeadingPATMuons->push_back(muon);
  }
  event->AddCollection("LooseNonLeadingPATMuons", looseNonLeadingPATMuons);
  auto looseNonLeadingPATMuonsVertex = asNanoEvent(event)->GetVerticesForMuons(asNanoMuons(looseNonLeadingPATMuons));
  event->AddCollection("LooseNonLeadingPATMuonsVertex", looseNonLeadingPATMuonsVertex);

  auto looseNonLeadingDisplacedPATMuons = make_shared<PhysicsObjects>();
  for (auto muon : *looseDisplacedPATMuons) {
    if (muon == leadingTightMuon->GetPhysicsObject())
      continue;
    looseNonLeadingDisplacedPATMuons->push_back(muon);
  }
  event->AddCollection("LooseNonLeadingDisplacedPATMuons", looseNonLeadingDisplacedPATMuons);
  
  // only segment matched implemented for now
  if (muonMatchingParams.find("Segment") == muonMatchingParams.end()) {
    warn() << "InsertNonLeadingLooseMuonsCollections only implemented for Segment matching "
            <<  "- and Segment is not defined in muonMatchingParams" << endl;
    return;
  }
    
  float segmentRatio = muonMatchingParams["Segment"];
  auto looseNonLeadingMuonsSegmentMatch = make_shared<PhysicsObjects>();
  auto looseNonLeadingPATMuonsSegmentMatch = make_shared<PhysicsObjects>();
  auto looseNonLeadingDSAMuonsSegmentMatch = make_shared<PhysicsObjects>();
  auto leadingTightMuonCollection = make_shared<NanoMuons>();
  leadingTightMuonCollection->push_back(leadingTightMuon);
  for (auto muon : *looseMuonsSegmentMatch) {
    if (asNanoMuon(muon)->IsDSA()) {
      // make sure DSA muon is not matched to leading thight muon
      bool matchFound = asNanoMuon(muon)->HasPATSegmentMatch(leadingTightMuonCollection, event, segmentRatio);
      if (!matchFound) {
        looseNonLeadingMuonsSegmentMatch->push_back(muon);
        looseNonLeadingDSAMuonsSegmentMatch->push_back(muon);
      }
    }
    else {
      if (muon != leadingTightMuon->GetPhysicsObject()) {
        looseNonLeadingMuonsSegmentMatch->push_back(muon);
        looseNonLeadingPATMuonsSegmentMatch->push_back(muon);
      }
    }
  }
  event->AddCollection("LooseNonLeadingMuonsSegmentMatch", looseNonLeadingMuonsSegmentMatch);
  event->AddCollection("LooseNonLeadingDSAMuonsSegmentMatch", looseNonLeadingDSAMuonsSegmentMatch);
  event->AddCollection("LooseNonLeadingPATMuonsSegmentMatch", looseNonLeadingPATMuonsSegmentMatch);
  auto looseNonLeadingMuonsVertexSegmentMatch = asNanoEvent(event)->GetVerticesForMuons(asNanoMuons(looseNonLeadingMuonsSegmentMatch));
  event->AddCollection("LooseNonLeadingMuonsVertexSegmentMatch", looseNonLeadingMuonsVertexSegmentMatch);
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
  if (muonVertexCollectionInput.empty()) return;

  try {
    auto vertices = event->GetCollection(muonVertexCollectionInput);

    InsertMuonVertexCollection(event, vertices);
  } catch (const Exception &e) {
    warn() << "Couldn't insert the muon vertex collection." << endl;
  }
}

void TTAlpsObjectsManager::InsertRevertedMatchedMuonsCollections(shared_ptr<Event> event) {
  if (muonMatchingParams.empty()) return;

  auto looseDSAMuons = asNanoMuons(event->GetCollection("LooseDSAMuons"));
  auto loosePATMuons = make_shared<NanoMuons>();
  auto looseDisplacedPATMuons = make_shared<NanoMuons>();
  try {
    loosePATMuons = asNanoMuons(event->GetCollection("LooseNonLeadingPATMuons"));
    loosePATMuons = asNanoMuons(event->GetCollection("LooseNonLeadingDisplacedPATMuons"));
  } catch (const Exception &e) {
    info() << "Using LoosePATMuons collection for reverted PAT-DSA matching" << endl;
    loosePATMuons = asNanoMuons(event->GetCollection("LoosePATMuons"));
    looseDisplacedPATMuons = asNanoMuons(event->GetCollection("LooseDisplacedPATMuons"));
  }
  for (auto &[matchingMethod, param] : muonMatchingParams) {
    if (matchingMethod == "DR") {
      auto matchedMuons = asNanoEvent(event)->GetRevertedDRMatchedMuons(looseDSAMuons, loosePATMuons, param);
      auto matchedDSAMuons = matchedMuons.first;
      auto matchedPATMuons = matchedMuons.second;
      event->AddCollection("RevertedDRMatchedDSAMuons", asPhysicsObjects(matchedDSAMuons));
      event->AddCollection("RevertedDRMatchedPATMuons", asPhysicsObjects(matchedPATMuons));
      continue;
    }
    if (matchingMethod == "OuterDR") {
      auto matchedMuons = asNanoEvent(event)->GetRevertedOuterDRMatchedMuons(looseDSAMuons, loosePATMuons, param);
      auto matchedDSAMuons = matchedMuons.first;
      auto matchedPATMuons = matchedMuons.second;
      event->AddCollection("RevertedOuterDRMatchedDSAMuons", asPhysicsObjects(matchedDSAMuons));
      event->AddCollection("RevertedOuterDRMatchedPATMuons", asPhysicsObjects(matchedPATMuons));
      continue;
    }
    if (matchingMethod == "ProxDR") {
      auto matchedMuons = asNanoEvent(event)->GetRevertedProximityDRMatchedMuons(looseDSAMuons, loosePATMuons, param);
      auto matchedDSAMuons = matchedMuons.first;
      auto matchedPATMuons = matchedMuons.second;
      event->AddCollection("RevertedProximityDRMatchedDSAMuons", asPhysicsObjects(matchedDSAMuons));
      event->AddCollection("RevertedProximityDRMatchedPATMuons", asPhysicsObjects(matchedPATMuons));
      continue;
    }
    if (matchingMethod == "Segment") {
      auto matchedMuons = asNanoEvent(event)->GetRevertedSegmentMatchedMuons(looseDSAMuons, loosePATMuons, param);
      auto matchedDSAMuons = matchedMuons.first;
      auto matchedPATMuons = matchedMuons.second;
      event->AddCollection("RevertedSegmentMatchedDSAMuons", asPhysicsObjects(matchedDSAMuons));
      event->AddCollection("RevertedSegmentMatchedPATMuons", asPhysicsObjects(matchedPATMuons));
      auto matchedDSAMuonsVertex = asNanoEvent(event)->GetVerticesForMuons(matchedDSAMuons);
      event->AddCollection("RevertedSegmentMatchedDSAMuonsVertex", matchedDSAMuonsVertex);
      auto matchedDisplacedMuons = asNanoEvent(event)->GetRevertedSegmentMatchedMuons(looseDSAMuons, looseDisplacedPATMuons, param);
      auto matchedDisplacedDSAMuons = matchedDisplacedMuons.first;
      auto matchedDisplacedPATMuons = matchedDisplacedMuons.second;
      event->AddCollection("RevertedSegmentMatchedDisplacedDSAMuons", asPhysicsObjects(matchedDisplacedDSAMuons));
      event->AddCollection("RevertedSegmentMatchedDisplacedPATMuons", asPhysicsObjects(matchedDisplacedPATMuons));
      continue;
    }
  }
}

void TTAlpsObjectsManager::InsertRevertedMatchedDSAMuonVertexCollection(shared_ptr<Event> event) {
  if (muonMatchingParams.size() == 0) return;
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;
  if (muonVertexCollectionInput.empty()) return;

  if (muonMatchingParams.find("Segment") == muonMatchingParams.end()) {
    error() << "InsertRevertedMatchedDSAMuonVertexCollection only implemented for Segment matching "
            <<  "- and Segment is not defined in muonMatchingParams" << endl;
    return;
  }
  auto segmentRatio = muonMatchingParams["Segment"];
  
  string muonVertexCollectionName = muonVertexCollection.first;
  auto muonVertexCollection = event->GetCollection(muonVertexCollectionName);
  auto revertedMuonVertexCollection = make_shared<PhysicsObjects>();
  auto matchedPATMuonVertexCollection = make_shared<PhysicsObjects>();
  auto matchedPATDSAMuonVertexCollection = make_shared<PhysicsObjects>();

  auto looseDSAMuons = asNanoMuons(event->GetCollection("LooseDSAMuons"));

  for (auto vertex : *muonVertexCollection) {
    auto nanoVertex = asNanoDimuonVertex(vertex,event);
    if (nanoVertex->IsPatDSADimuon() || nanoVertex->IsDSADimuon()) {
      continue;
    }
    // Get PAT-DSA and DSA-DSA dimuon version of PAT-PAT dimuon vertex
    auto patMuons = make_shared<NanoMuons>();
    patMuons->push_back(nanoVertex->Muon1());
    patMuons->push_back(nanoVertex->Muon2());
    auto matchedMuons = asNanoEvent(event)->GetRevertedSegmentMatchedMuons(looseDSAMuons,patMuons,segmentRatio);
    auto matchedDSAMuons = matchedMuons.first;
    // PAT-DSA dimuon
    if (matchedDSAMuons->size() == 1) {
      auto matchedPATMuon = matchedMuons.second->at(0);
      auto matchedPATDSAMuons = make_shared<NanoMuons>();
      matchedPATDSAMuons->push_back(matchedDSAMuons->at(0));
      // Find non-matched PAT muon
      if (matchedPATMuon == nanoVertex->Muon1()) {
        matchedPATDSAMuons->push_back(nanoVertex->Muon1());
      } else if (matchedPATMuon == nanoVertex->Muon2()) {
        matchedPATDSAMuons->push_back(nanoVertex->Muon2());
      } else {
        warn() << "PAT-DSA matching did not work properly: matched PAT muon doesn't respond to original PAT muon" << endl;
        continue;
      }
      auto matchedPATDSAMuonsVertices = asNanoEvent(event)->GetVerticesForMuons(matchedPATDSAMuons);
      auto bestMatchedPATDSAMuonsVertex = GetBestMuonVertex(matchedPATDSAMuonsVertices,event);
      if (bestMatchedPATDSAMuonsVertex) {
        revertedMuonVertexCollection->push_back(bestMatchedPATDSAMuonsVertex);
        matchedPATDSAMuonVertexCollection->push_back(vertex);
      }
      // DSA-DSA dimuon
    } else if (matchedDSAMuons->size() > 1) {
      auto matchedDSAMuonsVertices = asNanoEvent(event)->GetVerticesForMuons(matchedDSAMuons);
      auto bestMatchedDSAMuonsVertex = GetBestMuonVertex(matchedDSAMuonsVertices,event);
      if (bestMatchedDSAMuonsVertex) {
        revertedMuonVertexCollection->push_back(bestMatchedDSAMuonsVertex);
        matchedPATMuonVertexCollection->push_back(vertex);
      }
    }
  }
  event->AddCollection(muonVertexCollectionName+"_revertedMatching",revertedMuonVertexCollection);
  event->AddCollection(muonVertexCollectionName+"_matchedToPatDSA",matchedPATDSAMuonVertexCollection);
  event->AddCollection(muonVertexCollectionName+"_matchedToDSA",matchedPATMuonVertexCollection);
}

void TTAlpsObjectsManager::InsertMuonVertexCollection(shared_ptr<Event> event, shared_ptr<PhysicsObjects> vertices, MuonVertexCollectionSetup muonVertexCollectionInput) {
  if (muonMatchingParams.size() == 0) return;
  if ((muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) &&
      (muonVertexCollectionInput.first.empty() || muonVertexCollectionInput.second.empty())) return;
  
  string muonVertexCollectionName;
  vector<string> muonVertexCollectionCuts;
  if (!muonVertexCollectionInput.first.empty() && !muonVertexCollectionInput.second.empty()) {
    muonVertexCollectionName = muonVertexCollectionInput.first;
    muonVertexCollectionCuts = muonVertexCollectionInput.second;
  }
  else {
    muonVertexCollectionName = muonVertexCollection.first;
    muonVertexCollectionCuts = muonVertexCollection.second;
  }
  bool includeBestVertex = false;
  for (auto cutName : muonVertexCollectionCuts) {
    if (cutName == "BestDimuonVertex") {
      includeBestVertex = true;
      break;
    }
  }
  if (includeBestVertex)
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

  if (includeBestVertex) {
    auto bestVertex = GetBestMuonVertex(passedVertices, event);
    if (bestVertex) {
      if (applySegmentMatchingAfterSelections) {
        float minRatio = 2.0f / 3.0f;
        if (muonMatchingParams.find("Segment") != muonMatchingParams.end()) {
          minRatio = muonMatchingParams["Segment"];
        }
        auto bestSegmentMatchedVertex = asNanoEvent(event)->GetSegmentMatchedBestDimuonVertex(
          asNanoDimuonVertex(bestVertex,event), asNanoDimuonVertices(passedVertices,event), minRatio);
        if (bestSegmentMatchedVertex) {
          finalCollection->push_back(bestSegmentMatchedVertex->GetPhysicsObject());
        }
      }
      else {
        finalCollection->push_back(bestVertex);
      }
    }
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
    bool includeBestVertex = false;
    if (muonVertexCollectionCuts.back() == "BestDimuonVertex") {
      includeBestVertex = true;
      muonVertexCollectionCuts.pop_back();
    }

    for (auto nMinus1Cut : muonVertexCollectionCuts) {
      auto passedVertices = make_shared<PhysicsObjects>();
      for (auto vertex : *vertices) {
        bool passed = true;
        auto dimuonVertex = asNanoDimuonVertex(vertex, event);
        for (auto cut : muonVertexCollectionCuts) {
          if (cut == nMinus1Cut) continue;
          if (!ttAlpsCuts->PassesCut(dimuonVertex, cut)) {
            passed = false;
            break;
          }
        }
        if (passed) passedVertices->push_back(vertex);
      }
      string nminus1CollectionName = muonVertexCollectionName + "Nminus1" + nMinus1Cut;
      auto finalCollection = make_shared<PhysicsObjects>();
      if (includeBestVertex) {
        auto bestVertex = GetBestMuonVertex(passedVertices, event);
        if (bestVertex) {

          if (applySegmentMatchingAfterSelections) {
            float minRatio = 2.0f / 3.0f;
            if (muonMatchingParams.find("Segment") != muonMatchingParams.end()) {
              minRatio = muonMatchingParams["Segment"];
            }
            auto bestSegmentMatchedVertex = asNanoEvent(event)->GetSegmentMatchedBestDimuonVertex(
              asNanoDimuonVertex(bestVertex,event), asNanoDimuonVertices(passedVertices,event), minRatio);
            if (bestSegmentMatchedVertex) {
              finalCollection->push_back(bestSegmentMatchedVertex->GetPhysicsObject());
            }
          }
          else {
            finalCollection->push_back(bestVertex);
          }
        }
        string goodNminus1CollectionName = nminus1CollectionName;
        goodNminus1CollectionName.replace(0, 4, "Good");
        event->AddCollection(goodNminus1CollectionName, passedVertices);
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
