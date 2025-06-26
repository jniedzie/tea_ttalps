#include "TTAlpsEvent.hpp"

#include <tuple>

#include "ConfigManager.hpp"
#include "ExtensionsHelpers.hpp"

using namespace std;

TTAlpsEvent::TTAlpsEvent(std::shared_ptr<Event> event_) : event(event_) {
  eventProcessor = make_unique<EventProcessor>();
  nanoEventProcessor = make_unique<NanoEventProcessor>();
  auto &config = ConfigManager::GetInstance();

  try {
    config.GetValue("weightsBranchName", weightsBranchName);
  } catch (const Exception &e) {
    warn() << "Weights branch not specified -- will assume weight is 1 for all events" << endl;
  }
  try {
    config.GetMap("muonMatchingParams", muonMatchingParams);
  } catch (const Exception &e) {
    warn() << "Couldn't read muonMatchingParams from config file - will assume all PAT and DSA muons for SFs" << endl;
  }
  try {
    config.GetPair("muonVertexCollection", muonVertexCollection);
  } catch (const Exception &e) {
    warn() << "muonVertexCollection not defined - it is needed to define the SF for the muonVertexCollection in the event" << endl;
  }
}

map<string, float> TTAlpsEvent::GetEventWeights() {
  auto nanoEvent = asNanoEvent(event);
  if (nanoEventProcessor->IsDataEvent(nanoEvent)) return {{"default", 1.0}};

  float genWeight = nanoEventProcessor->GetGenWeight(nanoEvent);

  float pileupSF;
  // if (year == "2018") pileupSF = nanoEventProcessor->GetPileupScaleFactor(nanoEvent, "custom"); // TODO: do we want to use custom for all
  // years? else pileupSF = nanoEventProcessor->GetPileupScaleFactor(nanoEvent, "pileup");
  pileupSF = nanoEventProcessor->GetPileupScaleFactor(nanoEvent, "custom");
  map<string, float> muonTriggerSF = nanoEventProcessor->GetMuonTriggerScaleFactors(nanoEvent, "muonTrigger");

  int maxNjets = 4;
  auto leadingJets = eventProcessor->GetLeadingObjects(event, "GoodJets", maxNjets);
  map<string, float> PUjetIDSF = nanoEventProcessor->GetPUJetIDScaleFactors(asNanoJets(leadingJets));

  auto leadingBJets = make_shared<NanoJets>();
  auto allBJets = event->GetCollection("GoodMediumBtaggedJets");
  for (auto jet : *leadingJets) {
    for (auto bJet : *allBJets) {
      if (jet == bJet) leadingBJets->push_back(asNanoJet(jet));
    }
  }
  map<string, float> btagSF = nanoEventProcessor->GetMediumBTaggingScaleFactors(leadingBJets);
  auto muons = GetTTAlpsEventMuons();
  map<string, float> muonSF = nanoEventProcessor->GetMuonScaleFactors(muons);

  // event, minGoodJets, maxGoodJets, minGoodBJets, maxGoodBJets, minMET, maxMET
  map<string, float> jecUnc = GetJetEnergyCorrections(event, 4, 9999999, 1, 9999999, 50.0, 9999999.0);

  map<string,float> dimuonEffSF = GetDimuonEfficiencyScaleFactors();

  map<string, float> scaleFactorMap;
  scaleFactorMap["default"] = genWeight * pileupSF * muonTriggerSF["systematic"] * btagSF["systematic"] * PUjetIDSF["systematic"] *
                              muonSF["systematic"] * dimuonEffSF["systematic"];
  vector<map<string, float> *> scaleFactorMaps = {&muonTriggerSF, &btagSF, &PUjetIDSF, &muonSF, &dimuonEffSF, &jecUnc};

  for (auto scaleFactorMapPtr : scaleFactorMaps) {
    for (auto &[name, weight] : *scaleFactorMapPtr) {
      if (name == "systematic") continue;

      scaleFactorMap[name] = genWeight * pileupSF *
                             (scaleFactorMapPtr == &muonTriggerSF ? (*scaleFactorMapPtr)[name] : muonTriggerSF["systematic"]) *
                             (scaleFactorMapPtr == &btagSF ? (*scaleFactorMapPtr)[name] : btagSF["systematic"]) *
                             (scaleFactorMapPtr == &PUjetIDSF ? (*scaleFactorMapPtr)[name] : PUjetIDSF["systematic"]) *
                             (scaleFactorMapPtr == &muonSF ? (*scaleFactorMapPtr)[name] : muonSF["systematic"]) *
                             (scaleFactorMapPtr == &dimuonEffSF ? (*scaleFactorMapPtr)[name] : dimuonEffSF["systematic"]) *
                             (scaleFactorMapPtr == &jecUnc ? (*scaleFactorMapPtr)[name] : jecUnc["systematic"]);
    }
  }

  return scaleFactorMap;
}

shared_ptr<NanoMuons> TTAlpsEvent::GetAllLooseMuons() {
  auto allMuons = make_shared<NanoMuons>();
  if (muonMatchingParams.empty()) {
    for (auto muon : *event->GetCollection("LoosePATMuons")) {
      allMuons->push_back(asNanoMuon(muon));
    }
    for (auto muon : *event->GetCollection("LooseDSAMuons")) {
      allMuons->push_back(asNanoMuon(muon));
    }
    return allMuons;
  }
  // Only segment matched muons for now
  string matchingMethod = muonMatchingParams.begin()->first;
  return asNanoMuons(GetCollection("LooseMuons" + matchingMethod + "Match"));
}

shared_ptr<NanoMuons> TTAlpsEvent::GetTTAlpsEventMuons() {
  auto allMuons = GetAllLooseMuons();
  auto muons = make_shared<NanoMuons>();
  if (!muonVertexCollection.first.empty() && !muonVertexCollection.second.empty()) {
    shared_ptr<PhysicsObjects> vertex = nullptr;
    try {
      vertex = event->GetCollection(muonVertexCollection.first);
    } catch (const Exception &e) {
      warn() << "Couldn't get muon vertex collection - no dimuon cuts will be applied" << endl;
    }
    if (vertex && vertex->size() > 0) {
      auto muonVertex = asNanoDimuonVertex(vertex->at(0), event);
      muons->push_back(muonVertex->Muon1());
      muons->push_back(muonVertex->Muon2());

      auto remainingMuons = make_shared<NanoMuons>();
      for (auto muon : *allMuons) {
        if (muon->GetPhysicsObject() == muonVertex->Muon1()->GetPhysicsObject() ||
            muon->GetPhysicsObject() == muonVertex->Muon2()->GetPhysicsObject())
          continue;
        remainingMuons->push_back(muon);
      }
      allMuons = make_shared<NanoMuons>(*remainingMuons);
    }
  }
  if (GetLeadingMuon(allMuons)) muons->push_back(GetLeadingMuon(allMuons));
  return muons;
}

map<string, float> TTAlpsEvent::GetDimuonEfficiencyScaleFactors() {
  map<string, float> dimuonEffSF = {{"systematic", 1.0}};
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return dimuonEffSF;

  auto vertex = event->GetCollection(muonVertexCollection.first);
  // category is set to "" if no vertex is found - this is needed to set all SFs names for the first event
  string dimuonCategory = "";
  if (vertex->size() > 0) dimuonCategory = asNanoDimuonVertex(vertex->at(0), event)->GetVertexCategory();

  auto &scaleFactorsManager = ScaleFactorsManager::GetInstance();
  dimuonEffSF = scaleFactorsManager.GetCustomScaleFactorsForCategory("dimuonEff", dimuonCategory);
  return dimuonEffSF;
}

map<string, float> TTAlpsEvent::GetJetEnergyCorrections(shared_ptr<Event> event, int minJets, int maxJets,
                                                        int minBJets, int maxBJets, float minMETpt, float maxMETpt) {
  
  map<string, float> jec;

  auto &scaleFactorsManager = ScaleFactorsManager::GetInstance();
  // scaleFactorsManager.ReadJetEnergyCorrections();

  string baseJetCollectionName = "Jet";
  auto baseJetCollection = event->GetCollection(baseJetCollectionName);

  string goodJetCollectionName = "GoodJets";
  auto goodJetCollection = event->GetCollection(goodJetCollectionName);
  string goodBJetCollectionName = "GoodMediumBtaggedJets";
  auto goodBJetCollection = event->GetCollection(goodBJetCollectionName);

  unordered_set<PhysicsObject*> goodJetsSet;
  for (const auto &jet : *goodJetCollection) {
      goodJetsSet.insert(jet.get());
  }
  unordered_set<PhysicsObject*> goodBJetsSet;
  for (const auto &jet : *goodBJetCollection) {
      goodBJetsSet.insert(jet.get());
  }

  std::map<std::string, ExtraCollection> extraCollectionsDescriptions = event->GetExtraCollectionsDescriptions();
  std::pair<float, float> goodJetPtCuts = extraCollectionsDescriptions[goodJetCollectionName].allCuts["pt"];
  std::pair<float, float> goodBJetPtCuts = extraCollectionsDescriptions[goodBJetCollectionName].allCuts["pt"];

  auto &config = ConfigManager::GetInstance();
  string rhoBranchName;
  try {
    config.GetValue("rhoBranchName", rhoBranchName);
  } catch (const Exception &e) {
    warn() << "Rho branch not specified -- will assume standard name fixedGridRhoFastjetAll" << endl;
    rhoBranchName = "fixedGridRhoFastjetAll";
  }
  float rho = event->Get(rhoBranchName);  

  map<string,int> nPassingGoodJets;
  map<string,int> nPassingGoodBJets;
  map<string,float> totalDeltaPx;
  map<string,float> totalDeltaPy;
  for (auto jet : *baseJetCollection) {
    auto nanoJet = asNanoJet(jet);
    map<string,float> corrections = nanoJet->GetJetEnergyCorrections(rho);
    float pt = nanoJet->GetPt();

    const bool isGoodJet = goodJetsSet.count(jet.get()) != 0;
    const bool isGoodBJet = goodBJetsSet.count(jet.get()) != 0;

    for (auto &[name, correction] : corrections) {
      float newJetPt = pt*correction;

      if (nPassingGoodJets.find(name) == nPassingGoodJets.end()) {
        nPassingGoodJets[name] = 0;
        nPassingGoodBJets[name] = 0;
        totalDeltaPx[name] = 0;
        totalDeltaPy[name] = 0;
      }

      if (isGoodJet && newJetPt >= goodJetPtCuts.first && newJetPt <= goodJetPtCuts.second) {
        nPassingGoodJets[name]++;
      }
      if (isGoodBJet && newJetPt >= goodBJetPtCuts.first && newJetPt <= goodBJetPtCuts.second) {
        nPassingGoodBJets[name]++;
      }
      // Needed to propagate MET
      totalDeltaPx[name] += nanoJet->GetDeltaPx(newJetPt);
      totalDeltaPy[name] += nanoJet->GetDeltaPy(newJetPt);
    }
  }
  for (auto &[name, nPassingJets] : nPassingGoodJets) {
    jec[name] = 0.0;
    if (nPassingGoodJets[name] < minJets || nPassingGoodJets[name] > maxJets) continue;
    if (nPassingGoodBJets[name] < minBJets || nPassingGoodBJets[name] > maxBJets) continue;
    float newMetPt = nanoEventProcessor->PropagateMET(asNanoEvent(event), totalDeltaPx[name], totalDeltaPy[name]);
    if (newMetPt < minMETpt || newMetPt > maxMETpt) continue;
    jec[name] = 1.0;
  }
  return jec;
}

string TTAlpsEvent::GetTTbarEventCategory() {
  vector<int> topIndices = GetTopIndices();

  if (topIndices[0] < 0 || topIndices[1] < 0) {
    error() << "ERROR -- couldn't find tt̄ pair in the event..." << endl;
    return "error";
  }

  auto finalState = FinalState();

  vector<int> bottomIndices = GetBottomIndices();

  auto genParticles = event->GetCollection("GenPart");

  int iGenParticle = -1;
  for (auto physicsObject : *genParticles) {
    iGenParticle++;
    auto genParticle = asNanoGenParticle(physicsObject);
    if (!IsGoodParticle(iGenParticle, topIndices, bottomIndices)) continue;
    finalState.AddParticle(genParticle->GetPdgId());
  }

  if (!finalState.IsConsistent()) return "other";
  return finalState.GetShortName();
}

vector<int> TTAlpsEvent::GetTopIndices() {
  vector<int> topIndices = {-1, -1};

  auto genParticles = event->GetCollection("GenPart");

  int iGenParticle = -1;

  for (auto physicsObject : *genParticles) {
    iGenParticle++;
    auto genParticle = asNanoGenParticle(physicsObject);

    if (!genParticle->IsLastCopy()) continue;
    if (genParticle->GetPdgId() == 6) topIndices[0] = iGenParticle;
    if (genParticle->GetPdgId() == -6) topIndices[1] = iGenParticle;
    if (topIndices[0] >= 0 && topIndices[1] >= 0) break;
  }
  return topIndices;
}

vector<int> TTAlpsEvent::GetBottomIndices() {
  vector<int> bottomIndices;

  auto genParticles = event->GetCollection("GenPart");

  int iGenParticle = -1;

  for (auto physicsObject : *genParticles) {
    iGenParticle++;
    auto genParticle = asNanoGenParticle(physicsObject);

    if (abs(genParticle->GetPdgId()) == 5) {
      int motherIndex = genParticle->GetMotherIndex();
      if (motherIndex < 0) continue;
      auto mother = asNanoGenParticle(genParticles->at(motherIndex));
      if (!genParticle->IsGoodBottomQuark(mother)) continue;
      bottomIndices.push_back(iGenParticle);
    }
  }
  return bottomIndices;
}

bool TTAlpsEvent::IsGoodParticle(int particleIndex, vector<int> topIndices, vector<int> bottomIndices) {
  auto genParticles = event->GetCollection("GenPart");
  auto particle = asNanoGenParticle(genParticles->at(particleIndex));

  int motherIndex = particle->GetMotherIndex();
  if (motherIndex < 0) return false;
  auto mother = asNanoGenParticle(genParticles->at(motherIndex));

  int pid = particle->GetPdgId();

  if (abs(pid) == 5) {  // b quark
    if (!particle->IsGoodBottomQuark(mother)) return false;
  } else if (abs(pid) >= 1 && abs(pid) <= 4) {  // light quark
    if (!particle->IsGoodUdscQuark(mother)) return false;
  } else {  // leptons
    if (!particle->IsGoodLepton(mother)) return false;

    // we want to make sure it comes from a top
    if (!ParticlesMotherInIndices(particleIndex, topIndices)) return false;

    // we don't want leptons coming from b decays
    if (ParticlesMotherInIndices(particleIndex, bottomIndices)) return false;

    // no gluons/jets after the top
    if (ParticleHasISRmotherAfterTopMother(particleIndex)) return false;
  }

  return true;
}

bool TTAlpsEvent::ParticlesMotherInIndices(int particleIndex, vector<int> indices) {
  auto genParticles = event->GetCollection("GenPart");
  auto genParticle = asNanoGenParticle(genParticles->at(particleIndex));
  int motherIndex = genParticle->GetMotherIndex();

  if (find(indices.begin(), indices.end(), motherIndex) != indices.end()) return true;
  if (motherIndex < 0) return false;

  return ParticlesMotherInIndices(motherIndex, indices);
}

bool TTAlpsEvent::ParticleHasISRmotherAfterTopMother(int particleIndex) {
  auto genParticles = event->GetCollection("GenPart");
  auto genParticle = asNanoGenParticle(genParticles->at(particleIndex));
  int motherIndex = genParticle->GetMotherIndex();

  auto mother = asNanoGenParticle(genParticles->at(motherIndex));

  if (mother->IsTop()) return false;
  if (mother->IsJet()) return true;
  if (motherIndex < 0) return false;

  return ParticleHasISRmotherAfterTopMother(motherIndex);
}

bool TTAlpsEvent::IsGoodMuonFromALP(int genMuonIndex) {
  auto genParticles = event->GetCollection("GenPart");
  auto muon = asNanoGenParticle(genParticles->at(genMuonIndex));

  if (!muon->IsLastCopy()) return false;
  if (!muon->IsMuon()) return false;

  auto firstMuon = muon->GetFirstCopy(genParticles);
  if (firstMuon == nullptr) return false;

  int motherIndex = firstMuon->GetMotherIndex();
  if (motherIndex < 0) return false;
  auto mother = asNanoGenParticle(genParticles->at(motherIndex));
  // mother must be an ALP
  if (!mother->IsLastCopy()) return false;
  int ALPpdgId = 54;
  if (abs(mother->GetPdgId()) != ALPpdgId) return false;

  return true;
}

bool TTAlpsEvent::IsGoodMuonFromMotherWithParticleID(int genMuonIndex, int motherParticleID) {
  auto genParticles = event->GetCollection("GenPart");
  auto muon = asNanoGenParticle(genParticles->at(genMuonIndex));

  if (!muon->IsLastCopy()) return false;
  if (!muon->IsMuon()) return false;

  auto firstMuon = muon->GetFirstCopy(genParticles);
  if (firstMuon == nullptr) return false;

  int motherIndex = firstMuon->GetMotherIndex();
  if (motherIndex < 0) return false;
  auto mother = asNanoGenParticle(genParticles->at(motherIndex));
  // mother must be an ALP
  if (!mother->IsLastCopy()) return false;
  if (abs(mother->GetPdgId()) != motherParticleID) return false;

  return true;
}

bool TTAlpsEvent::IsGoodMuonNotFromALP(int genMuonIndex) {
  auto genParticles = event->GetCollection("GenPart");
  auto muon = asNanoGenParticle(genParticles->at(genMuonIndex));

  if (!muon->IsLastCopy()) return false;
  if (!muon->IsMuon()) return false;

  auto firstMuon = muon->GetFirstCopy(genParticles);
  if (firstMuon == nullptr) return false;

  int motherIndex = firstMuon->GetMotherIndex();
  if (motherIndex < 0) return false;
  auto mother = asNanoGenParticle(genParticles->at(motherIndex));
  // mother must be an ALP
  if (!mother->IsLastCopy()) return false;
  int ALPpdgId = 54;
  if (abs(mother->GetPdgId()) == ALPpdgId) return false;

  return true;
}

shared_ptr<PhysicsObjects> TTAlpsEvent::GetGenALPs() {
  auto genParticles = event->GetCollection("GenPart");

  auto genALPs = make_shared<PhysicsObjects>();

  for (int i = 0; i < genParticles->size(); i++) {
    auto genParticle = asNanoGenParticle(genParticles->at(i));
    if (!genParticle->IsGoodParticleWithID(54)) continue;
    genALPs->push_back(genParticles->at(i));
  }
  return genALPs;
}

shared_ptr<MuonPair> TTAlpsEvent::GetGenDimuonFromALP() {
  auto genParticles = event->GetCollection("GenPart");

  auto genMuons = make_shared<PhysicsObjects>();

  for (int muon_idx = 0; muon_idx < genParticles->size(); muon_idx++) {
    auto genParticle = asNanoGenParticle(genParticles->at(muon_idx));
    int motherIndex = genParticle->GetMotherIndex();
    if (motherIndex < 0) continue;
    auto mother = asNanoGenParticle(genParticles->at(motherIndex));
    if (!IsGoodMuonFromALP(muon_idx)) continue;
    genMuons->push_back(genParticles->at(muon_idx));
  }
  if (genMuons->size() != 2) return nullptr;
  return make_shared<MuonPair>(genMuons->at(0), genMuons->at(1));
}

vector<int> TTAlpsEvent::GetGenMuonIndicesFromALP() {
  auto genParticles = event->GetCollection("GenPart");

  vector<int> genMuonIndices;

  for (int muon_idx = 0; muon_idx < genParticles->size(); muon_idx++) {
    auto genParticle = asNanoGenParticle(genParticles->at(muon_idx));
    int motherIndex = genParticle->GetMotherIndex();
    if (motherIndex < 0) continue;
    auto mother = asNanoGenParticle(genParticles->at(motherIndex));
    if (!IsGoodMuonFromALP(muon_idx)) continue;
    genMuonIndices.push_back(muon_idx);
  }
  return genMuonIndices;
}

shared_ptr<PhysicsObjects> TTAlpsEvent::GetGenMuonsFromW() {
  auto genParticles = event->GetCollection("GenPart");

  auto genMuons = make_shared<PhysicsObjects>();

  for (int muon_idx = 0; muon_idx < genParticles->size(); muon_idx++) {
    auto genParticle = asNanoGenParticle(genParticles->at(muon_idx));
    int motherIndex = genParticle->GetMotherIndex();
    if (motherIndex < 0) continue;
    auto mother = asNanoGenParticle(genParticles->at(motherIndex));
    int WpdgId = 24;
    if (!IsGoodMuonFromMotherWithParticleID(muon_idx, WpdgId)) continue;
    genMuons->push_back(genParticles->at(muon_idx));
  }
  return genMuons;
}

vector<int> TTAlpsEvent::GetGenMuonIndicesFromW() {
  auto genParticles = event->GetCollection("GenPart");

  vector<int> genMuonIndices;

  for (int muon_idx = 0; muon_idx < genParticles->size(); muon_idx++) {
    auto genParticle = asNanoGenParticle(genParticles->at(muon_idx));
    int motherIndex = genParticle->GetMotherIndex();
    if (motherIndex < 0) continue;
    auto mother = asNanoGenParticle(genParticles->at(motherIndex));
    int WpdgId = 24;
    if (!IsGoodMuonFromMotherWithParticleID(muon_idx, WpdgId)) continue;
    genMuonIndices.push_back(muon_idx);
  }
  return genMuonIndices;
}

shared_ptr<MuonPairs> TTAlpsEvent::GetGenDimuonsNotFromALP() {
  auto genParticles = event->GetCollection("GenPart");

  auto genMuons = GetGenMuonsNotFromALP();
  auto genDimuons = make_shared<MuonPairs>();

  for (int muon1_idx = 0; muon1_idx < genMuons->size(); muon1_idx++) {
    auto genMuon1 = asNanoGenParticle(genMuons->at(muon1_idx));
    auto firstMuon1 = genMuon1->GetFirstCopy(genParticles);
    if (firstMuon1 == nullptr) continue;

    int motherIndex1 = firstMuon1->GetMotherIndex();
    if (motherIndex1 < 0) continue;
    auto mother1 = asNanoGenParticle(genParticles->at(motherIndex1));
    if (!mother1->IsLastCopy()) continue;

    for (int muon2_idx = muon1_idx + 1; muon2_idx < genMuons->size(); muon2_idx++) {
      if (muon2_idx == muon1_idx) continue;
      auto genMuon2 = asNanoGenParticle(genMuons->at(muon2_idx));
      auto firstMuon2 = genMuon2->GetFirstCopy(genParticles);
      if (firstMuon2 == nullptr) continue;

      int motherIndex2 = firstMuon2->GetMotherIndex();
      if (motherIndex2 < 0) continue;
      auto mother2 = asNanoGenParticle(genParticles->at(motherIndex2));

      if (!mother2->IsLastCopy()) continue;

      if (motherIndex1 == motherIndex2) {
        auto dimuon = make_pair(genMuons->at(muon1_idx), genMuons->at(muon2_idx));
        genDimuons->push_back(dimuon);
      }
    }
  }
  return genDimuons;
}

shared_ptr<PhysicsObjects> TTAlpsEvent::GetGenMuonsNotFromALP() {
  auto genParticles = event->GetCollection("GenPart");

  auto genMuons = make_shared<PhysicsObjects>();

  for (int muon_idx = 0; muon_idx < genParticles->size(); muon_idx++) {
    auto genParticle = asNanoGenParticle(genParticles->at(muon_idx));
    int motherIndex = genParticle->GetMotherIndex();
    if (motherIndex < 0) continue;
    auto mother = asNanoGenParticle(genParticles->at(motherIndex));

    if (!IsGoodMuonNotFromALP(muon_idx)) continue;
    genMuons->push_back(genParticles->at(muon_idx));
  }
  return genMuons;
}

shared_ptr<NanoMuonPair> TTAlpsEvent::GetDimuonMatchedToGenMuonsFromALP(shared_ptr<NanoMuons> muonCollection, float maxDeltaR) {
  auto genMuonPair = GetGenDimuonFromALP();

  return GetLooseDimuonMatchedToGenDimuon(genMuonPair, muonCollection, maxDeltaR);
}

shared_ptr<NanoMuonPair> TTAlpsEvent::GetLooseDimuonMatchedToGenDimuon(shared_ptr<MuonPair> genMuonPair,
                                                                       shared_ptr<NanoMuons> looseMuonCollection, float maxDeltaR) {
  vector<int> savedMuonIndices;
  float muonMass = 0.105;

  if (!genMuonPair) return nullptr;

  float minDeltaR1(9999), minDeltaR2(9999), secondMinDeltaR1(9999), secondMinDeltaR2(9999);
  float minDeltaR1_muonIdx(-1), minDeltaR2_muonIdx(-1), secondMinDeltaR1_muonIdx(-1), secondMinDeltaR2_muonIdx(-1);

  auto genMuon1p4 = asNanoGenParticle(genMuonPair->first)->GetFourVector(muonMass);
  auto genMuon2p4 = asNanoGenParticle(genMuonPair->second)->GetFourVector(muonMass);

  for (int i = 0; i < looseMuonCollection->size(); i++) {
    auto muonp4 = looseMuonCollection->at(i)->GetFourVector();

    float deltaR1 = muonp4.DeltaR(genMuon1p4);
    float deltaR2 = muonp4.DeltaR(genMuon2p4);

    if (deltaR1 < maxDeltaR) {
      if (deltaR1 < minDeltaR1) {
        minDeltaR1 = deltaR1;
        minDeltaR1_muonIdx = i;
      } else if (deltaR1 < secondMinDeltaR1) {
        secondMinDeltaR1 = deltaR1;
        secondMinDeltaR1_muonIdx = i;
      }
    }
    if (deltaR2 < maxDeltaR) {
      if (deltaR2 < minDeltaR2) {
        minDeltaR2 = deltaR2;
        minDeltaR2_muonIdx = i;
      } else if (deltaR2 < secondMinDeltaR2) {
        secondMinDeltaR2 = deltaR2;
        secondMinDeltaR2_muonIdx = i;
      }
    }
  }
  if (minDeltaR1_muonIdx < 0 || minDeltaR2_muonIdx < 0) return nullptr;
  // minDeltaR1_muonIdx != minDeltaR2_muonIdx
  if (minDeltaR1_muonIdx != minDeltaR2_muonIdx) {
    return make_shared<NanoMuonPair>(looseMuonCollection->at(minDeltaR1_muonIdx), looseMuonCollection->at(minDeltaR2_muonIdx));
  }
  // minDeltaR1_muonIdx < minDeltaR2_muonIdx
  if (minDeltaR1 < minDeltaR2) {
    if (secondMinDeltaR2_muonIdx >= 0) {
      return make_shared<NanoMuonPair>(looseMuonCollection->at(minDeltaR1_muonIdx), looseMuonCollection->at(secondMinDeltaR2_muonIdx));
    }
  }
  // minDeltaR1_muonIdx > minDeltaR2_muonIdx
  if (secondMinDeltaR1_muonIdx >= 0) {
    return make_shared<NanoMuonPair>(looseMuonCollection->at(secondMinDeltaR1_muonIdx), looseMuonCollection->at(minDeltaR2_muonIdx));
  }
  // secondMinDeltaR1_muonIdx < 0 or secondMinDeltaR2_muonIdx < 0
  return nullptr;
}

shared_ptr<NanoMuons> TTAlpsEvent::GetLooseMuonsMatchedToGenMuons(shared_ptr<PhysicsObjects> genMuonCollection,
                                                                  shared_ptr<NanoMuons> looseMuonCollection, float maxDeltaR) {
  auto matchedLooseMuons = make_shared<NanoMuons>();
  vector<int> savedMuonIndices;
  float muonMass = 0.105;

  vector<vector<tuple<float, int>>> minDeltaRs;

  for (int i = 0; i < genMuonCollection->size(); i++) {
    vector<tuple<float, int>> minDeltaR(5, make_tuple(9999.0f, -1));

    auto genMuonp4 = asNanoGenParticle(genMuonCollection->at(i))->GetFourVector(muonMass);

    for (int j = 0; j < looseMuonCollection->size(); j++) {
      auto looseMuonp4 = looseMuonCollection->at(j)->GetFourVector();

      float deltaR = looseMuonp4.DeltaR(genMuonp4);

      if (deltaR > maxDeltaR) continue;

      if (deltaR < get<0>(minDeltaR.back())) {
        minDeltaR.emplace_back(deltaR, j);
        sort(minDeltaR.begin(), minDeltaR.end(), [](const auto &a, const auto &b) { return get<0>(a) < get<0>(b); });
        if (minDeltaR.size() > 5) minDeltaR.pop_back();
      }
    }
    minDeltaRs.push_back(minDeltaR);
  }
  for (auto &minDeltaRs : minDeltaRs) {
    sort(minDeltaRs.begin(), minDeltaRs.end(), [](const auto &a, const auto &b) { return get<0>(a) < get<0>(b); });
  }
  for (size_t i = 0; i < minDeltaRs.size(); ++i) {
    const auto &deltaRs = minDeltaRs[i];
    for (const auto &[deltaR, muonIdx] : deltaRs) {
      if (muonIdx < 0) continue;
      if (find(savedMuonIndices.begin(), savedMuonIndices.end(), muonIdx) == savedMuonIndices.end()) {
        savedMuonIndices.push_back(muonIdx);
        matchedLooseMuons->push_back(looseMuonCollection->at(muonIdx));
        break;
      }
    }
  }
  return matchedLooseMuons;
}

shared_ptr<PhysicsObjects> TTAlpsEvent::GetMuonsMatchedToGenMuonsNotFromALP(shared_ptr<PhysicsObjects> muonCollection, float maxDeltaR) {
  auto genMuons = GetGenMuonsNotFromALP();

  auto muonsNotFromALP = make_shared<PhysicsObjects>();
  vector<int> savedMuonIndices;

  float muonMass = 0.105;

  for (auto genMuon : *genMuons) {
    auto genMuonp4 = asNanoGenParticle(genMuon)->GetFourVector(muonMass);

    float minDeltaR = 9999;
    float minDeltaR_muonIdx = -1;

    for (int i = 0; i < muonCollection->size(); i++) {
      auto muonp4 = asNanoMuon(muonCollection->at(i))->GetFourVector();

      float deltaR = muonp4.DeltaR(genMuonp4);
      if (deltaR < maxDeltaR && deltaR < minDeltaR) {
        minDeltaR = deltaR;
        minDeltaR_muonIdx = i;
      }
    }
    if (minDeltaR_muonIdx >= 0 && find(savedMuonIndices.begin(), savedMuonIndices.end(), minDeltaR_muonIdx) == savedMuonIndices.end()) {
      muonsNotFromALP->push_back(muonCollection->at(minDeltaR_muonIdx));
      savedMuonIndices.push_back(minDeltaR_muonIdx);
    }
  }
  return muonsNotFromALP;
}

std::shared_ptr<NanoMuonPairs> TTAlpsEvent::GetMuonsMatchedToGenDimuonsNotFromALP(shared_ptr<NanoMuons> muonCollection, float maxDeltaR) {
  auto genDimuons = GetGenDimuonsNotFromALP();

  auto dimuonsNotFromALP = make_shared<NanoMuonPairs>();
  vector<int> savedMuonIndices;
  float muonMass = 0.105;

  for (auto genDimuon : *genDimuons) {
    // save best 2 muons in muonCollection with smallest deltaR to genDimuon
    auto genMuon1 = asNanoGenParticle(genDimuon.first);
    auto genMuon2 = asNanoGenParticle(genDimuon.second);

    auto genMuon1p4 = genMuon1->GetFourVector(muonMass);
    auto genMuon2p4 = genMuon2->GetFourVector(muonMass);

    float bestDeltaR1 = maxDeltaR;
    float bestDeltaR2 = maxDeltaR;
    float secondBestDeltaR1 = maxDeltaR;
    float secondBestDeltaR2 = maxDeltaR;

    int bestRecoMuonIdx1 = -1;
    int secondBestRecoMuonIdx1 = -1;
    int bestRecoMuonIdx2 = -1;
    int secondBestRecoMuonIdx2 = -1;

    for (int i = 0; i < muonCollection->size(); i++) {
      if (find(savedMuonIndices.begin(), savedMuonIndices.end(), i) != savedMuonIndices.end()) {
        continue;
      }

      auto muonp4 = muonCollection->at(i)->GetFourVector();
      float deltaR1 = muonp4.DeltaR(genMuon1p4);
      float deltaR2 = muonp4.DeltaR(genMuon2p4);

      // Match reco-muon to genMuon1 if it's the best match
      if (deltaR1 < bestDeltaR1) {
        secondBestDeltaR1 = bestDeltaR1;
        secondBestRecoMuonIdx1 = bestRecoMuonIdx1;
        bestDeltaR1 = deltaR1;
        bestRecoMuonIdx1 = i;
      } else if (deltaR1 < secondBestDeltaR1) {
        secondBestDeltaR1 = deltaR1;
        secondBestRecoMuonIdx1 = i;
      }
      // Match reco-muon to genMuon2 if it's the best match
      if (deltaR2 < bestDeltaR2) {
        secondBestDeltaR2 = bestDeltaR2;
        secondBestRecoMuonIdx2 = bestRecoMuonIdx2;
        bestDeltaR2 = deltaR2;
        bestRecoMuonIdx2 = i;
      } else if (deltaR2 < secondBestDeltaR2) {
        secondBestDeltaR2 = deltaR2;
        secondBestRecoMuonIdx2 = i;
      }
    }
    // If both reco muons are matched to the same reco muon, resolve conflicts
    if (bestRecoMuonIdx1 == bestRecoMuonIdx2) {
      if (bestDeltaR1 < bestDeltaR2) {
        // Assign bestRecoMuonIdx1 to genMuon1 and use the second best for genMuon2
        bestRecoMuonIdx2 = secondBestRecoMuonIdx2;
      } else {
        // Assign bestRecoMuonIdx2 to genMuon2 and use the second best for genMuon1
        bestRecoMuonIdx1 = secondBestRecoMuonIdx1;
      }
    }
    // Only add matches if valid reco-muon indices are found for both gen-muons
    if (bestRecoMuonIdx1 >= 0 && bestRecoMuonIdx2 >= 0) {
      // Save the matched reco muons
      dimuonsNotFromALP->push_back(make_pair(muonCollection->at(bestRecoMuonIdx1), muonCollection->at(bestRecoMuonIdx2)));
      savedMuonIndices.push_back(bestRecoMuonIdx1);
      savedMuonIndices.push_back(bestRecoMuonIdx2);
    }
  }
  return dimuonsNotFromALP;
}

shared_ptr<NanoMuons> TTAlpsEvent::GetRemainingNonResonantMuons(shared_ptr<NanoMuons> muonCollection,
                                                                shared_ptr<NanoMuonPairs> resonantCollection) {
  auto nonResonantMuons = make_shared<NanoMuons>();

  for (auto muon : *muonCollection) {
    bool isResonant = false;
    for (auto resonant : *resonantCollection) {
      if (muon == resonant.first || muon == resonant.second) {
        isResonant = true;
        break;
      }
    }
    if (!isResonant) nonResonantMuons->push_back(muon);
  }
  return nonResonantMuons;
}

vector<int> TTAlpsEvent::GetFiveFirstMotherIDsOfParticle(shared_ptr<PhysicsObject> particle) {
  auto genParticles = event->GetCollection("GenPart");

  std::vector<int> motherIDs = {-1, -1, -1, -1, -1};
  bool mothersOk = true;
  int motherCount = 0;
  auto genParticle = asNanoGenParticle(particle);
  while (mothersOk && motherCount < 5) {
    auto firstMuon = genParticle->GetFirstCopy(genParticles);
    if (firstMuon != nullptr) {
      int motherIndex = firstMuon->GetMotherIndex();
      if (motherIndex >= 0) {
        auto mother = asNanoGenParticle(genParticles->at(motherIndex));
        if (mother->IsLastCopy()) {
          motherIDs[motherCount] = abs(mother->GetPdgId());
          genParticle = mother;
        } else {
          mothersOk = false;
        }
      } else {
        mothersOk = false;
      }
    } else {
      mothersOk = false;
    }
    motherCount++;
  }
  return motherIDs;
}

// Particle can be either a genParticle or a reco muon, Mother has to be a genParticle
float TTAlpsEvent::GetPhiAngleBetweenDimuonAndALP(shared_ptr<PhysicsObject> muon1, shared_ptr<PhysicsObject> muon2,
                                                  shared_ptr<PhysicsObject> alp, bool recoMuon) {
  auto pv_x = GetAs<float>("PV_x");
  auto pv_y = GetAs<float>("PV_y");
  auto pv_z = GetAs<float>("PV_z");

  TLorentzVector muon1fourVector, muon2fourVector;
  float muonMass = 0.105;
  if (recoMuon) {
    muon1fourVector = asNanoMuon(muon1)->GetFourVector();
    muon2fourVector = asNanoMuon(muon2)->GetFourVector();
  } else {
    muon1fourVector = asNanoGenParticle(muon1)->GetFourVector(muonMass);
    muon2fourVector = asNanoGenParticle(muon2)->GetFourVector(muonMass);
  }

  TVector3 muon1ptVector(muon1fourVector.Px(), muon1fourVector.Py(), muon1fourVector.Pz());
  TVector3 muon2ptVector(muon2fourVector.Px(), muon2fourVector.Py(), muon2fourVector.Pz());
  TVector3 alpLxyzVector((float)alp->Get("vx") - pv_x, (float)alp->Get("vy") - pv_y, (float)alp->Get("vz") - pv_z);

  TVector3 muonPtNormal = muon1ptVector.Cross(muon2ptVector).Unit();

  double muonNormalTheta = muonPtNormal.Theta();
  double alpLxyzTheta = alpLxyzVector.Theta();

  muonPtNormal.SetTheta(muonNormalTheta - alpLxyzTheta);

  return muonPtNormal.Phi();
}

shared_ptr<NanoMuon> TTAlpsEvent::GetLeadingMuon(shared_ptr<NanoMuons> muonCollection) {
  int leadingMuonIdx = -1;
  float leadingMuonPt = -1;

  for (int i = 0; i < muonCollection->size(); i++) {
    if ((float)muonCollection->at(i)->Get("pt") > leadingMuonPt) {
      leadingMuonPt = (float)muonCollection->at(i)->Get("pt");
      leadingMuonIdx = i;
    }
  }
  if (leadingMuonIdx < 0) return nullptr;
  return muonCollection->at(leadingMuonIdx);
}

shared_ptr<NanoMuons> TTAlpsEvent::GetTightMuonsInCollection(shared_ptr<NanoMuons> muonCollection) {
  auto tightMuons = make_shared<NanoMuons>();

  for (auto muon : *muonCollection) {
    if (muon->IsDSA()) continue;
    if (muon->IsTight() && (float)muon->Get("pt") > 30 && abs((float)muon->Get("eta")) < 2.4) {
      tightMuons->push_back(muon);
    }
  }
  return tightMuons;
}

bool TTAlpsEvent::IsALPDecayWithinCMS(float CMS_Lxy_max) {
  auto genMuonsFromALP = GetGenDimuonFromALP();
  float ALPvx = genMuonsFromALP->first->Get("vx");
  float ALPvy = genMuonsFromALP->first->Get("vy");
  float ALPvxy = sqrt(ALPvx * ALPvx + ALPvy * ALPvy);
  return ALPvxy < CMS_Lxy_max;
}

bool TTAlpsEvent::IsLeadingMuonInCollection(shared_ptr<NanoMuons> collection, shared_ptr<NanoMuons> allMuons) {
  auto leadingLooseMuon = GetLeadingMuon(allMuons);
  float leadingLoosePt = leadingLooseMuon->Get("pt");
  for (auto muon : *collection) {
    if ((float)muon->Get("pt") == leadingLoosePt) return true;
  }
  return false;
}

shared_ptr<NanoMuons> TTAlpsEvent::GetMuonsInVertexCollection(shared_ptr<PhysicsObjects> vertexCollection) {
  auto muons = make_shared<NanoMuons>();
  vector<int> DSAmuonIndices;
  vector<int> PATmuonIndices;
  for (auto vertex : *vertexCollection) {
    auto dimuonVertex = asNanoDimuonVertex(vertex, event);
    if (dimuonVertex->IsDSAMuon1()) {
      if (std::find(DSAmuonIndices.begin(), DSAmuonIndices.end(), dimuonVertex->MuonIndex1()) != DSAmuonIndices.end()) continue;
      DSAmuonIndices.push_back(dimuonVertex->MuonIndex1());
      muons->push_back(dimuonVertex->Muon1());
    } else {
      if (std::find(PATmuonIndices.begin(), PATmuonIndices.end(), dimuonVertex->MuonIndex1()) != PATmuonIndices.end()) continue;
      PATmuonIndices.push_back(dimuonVertex->MuonIndex1());
      muons->push_back(dimuonVertex->Muon1());
    }
    if (dimuonVertex->IsDSAMuon2()) {
      if (std::find(DSAmuonIndices.begin(), DSAmuonIndices.end(), dimuonVertex->MuonIndex2()) != DSAmuonIndices.end()) continue;
      DSAmuonIndices.push_back(dimuonVertex->MuonIndex2());
      muons->push_back(dimuonVertex->Muon2());
    } else {
      if (std::find(PATmuonIndices.begin(), PATmuonIndices.end(), dimuonVertex->MuonIndex2()) != PATmuonIndices.end()) continue;
      PATmuonIndices.push_back(dimuonVertex->MuonIndex2());
      muons->push_back(dimuonVertex->Muon2());
    }
  }
  return muons;
}
