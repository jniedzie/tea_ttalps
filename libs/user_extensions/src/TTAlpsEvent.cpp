#include "TTAlpsEvent.hpp"
#include "ExtensionsHelpers.hpp"

using namespace std;

string TTAlpsEvent::GetTTbarEventCategory() {
  vector<int> topIndices = GetTopIndices();

  if (topIndices[0] < 0 || topIndices[1] < 0) {
    cout << "ERROR -- couldn't find tt̄ pair in the event..." << endl;
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
  if(!muon->IsMuon()) return false;

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

shared_ptr<PhysicsObjects> TTAlpsEvent::GetGenALPs() {
  auto genParticles = event->GetCollection("GenPart");

  auto genALPs = make_shared<PhysicsObjects>();

  for (int i = 0; i < genParticles->size(); i++)
  {
    auto genParticle = asNanoGenParticle(genParticles->at(i));
    if(!genParticle->IsGoodParticleWithID(54)) continue;
    genALPs->push_back(genParticles->at(i));
  }
  return genALPs;
}

shared_ptr<PhysicsObjects> TTAlpsEvent::GetGenMuonsFromALP() {
  auto genParticles = event->GetCollection("GenPart");

  auto genMuons = make_shared<PhysicsObjects>();

  for (int muon_idx = 0; muon_idx < genParticles->size(); muon_idx++)
  {
    auto genParticle = asNanoGenParticle(genParticles->at(muon_idx));
    int motherIndex = genParticle->GetMotherIndex();
    if (motherIndex < 0) continue;
    auto mother = asNanoGenParticle(genParticles->at(motherIndex));
    if(!IsGoodMuonFromALP(muon_idx)) continue;
    genMuons->push_back(genParticles->at(muon_idx));
  }
  return genMuons;
}

shared_ptr<PhysicsObjects> TTAlpsEvent::GetMuonsMatchedToGenMuonsFromALP(shared_ptr<PhysicsObjects> muonCollection, float maxDeltaR) {
  auto genMuons = GetGenMuonsFromALP();

  auto muonsFromALP = make_shared<PhysicsObjects>();
  vector<int> savedMuonIndices;

  float muonMass = 0.105;

  for (auto genMuon : *genMuons) {
    auto genMuonp4 = asNanoGenParticle(genMuon)->GetFourVector(muonMass);

    float minDeltaR = 9999;
    float minDeltaR_muonIdx = -1;

    for (int i = 0; i < muonCollection->size(); i++) {
      auto muonp4 = asNanoMuon(muonCollection->at(i))->GetFourVector();

      float deltaR = muonp4.DeltaR(genMuonp4);
      if(deltaR < maxDeltaR && deltaR < minDeltaR) {
        minDeltaR = deltaR;
        minDeltaR_muonIdx = i;
      }
    }
    if(minDeltaR_muonIdx >= 0 && find(savedMuonIndices.begin(), savedMuonIndices.end(), minDeltaR_muonIdx) == savedMuonIndices.end()) {
      muonsFromALP->push_back(muonCollection->at(minDeltaR_muonIdx));
      savedMuonIndices.push_back(minDeltaR_muonIdx);
    }
  }
  return muonsFromALP;
}
