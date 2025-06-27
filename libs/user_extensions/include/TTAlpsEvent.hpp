#ifndef TTAlpsEvent_hpp
#define TTAlpsEvent_hpp

#include "Event.hpp"
#include "NanoEvent.hpp"
#include "Helpers.hpp"
#include "EventProcessor.hpp"
#include "NanoEventProcessor.hpp"

class TTAlpsEvent {
 public:
  TTAlpsEvent(std::shared_ptr<Event> event_);

  auto Get(std::string branchName, const char* file = __builtin_FILE(), const char* function = __builtin_FUNCTION(),
           int line = __builtin_LINE()) {
    return event->Get(branchName, file, function, line);
  }

  template <typename T>
  T GetAs(std::string branchName) { return event->GetAs<T>(branchName); }
  std::shared_ptr<PhysicsObjects> GetCollection(std::string name) const { return event->GetCollection(name); }
  
  std::map<std::string,float> GetEventWeights();

  // returns all Loose (PAT and DSA) muons in the event. If matchingParams are defined it returns the collection after the first matching
  std::shared_ptr<NanoMuons> GetAllLooseMuons();

  // returns 2 muons from the dimuon vertex (if there is one defined in the config), and the leading remaining muon
  std::shared_ptr<NanoMuons> GetTTAlpsEventMuons();

  std::map<std::string,float> GetDimuonEfficiencyScaleFactors();

  std::map<std::string, float> GetJetEnergyCorrections(std::shared_ptr<Event> event, int minJets, int maxJets,
    int minBJets, int maxBJets, float minMETpt, float maxMETpt);

  std::pair<float,float> GetEventCut(std::string eventVariable);

  std::shared_ptr<PhysicsObjects> GetGenALPs();
  std::shared_ptr<MuonPair> GetGenDimuonFromALP();
  std::vector<int> GetGenMuonIndicesFromALP();

  std::shared_ptr<PhysicsObjects> GetGenMuonsNotFromALP();
  std::shared_ptr<MuonPairs> GetGenDimuonsNotFromALP();

  std::shared_ptr<PhysicsObjects> GetGenMuonsFromW();
  std::vector<int> GetGenMuonIndicesFromW();
  
  std::shared_ptr<NanoMuonPair> GetDimuonMatchedToGenMuonsFromALP(std::shared_ptr<NanoMuons> muonCollection, float maxDeltaR = 0.3);
  
  std::shared_ptr<PhysicsObjects> GetMuonsMatchedToGenMuonsNotFromALP(std::shared_ptr<PhysicsObjects> muonCollection, float maxDeltaR = 0.3);
  std::shared_ptr<NanoMuonPairs> GetMuonsMatchedToGenDimuonsNotFromALP(std::shared_ptr<NanoMuons> muonCollection, float maxDeltaR = 0.3);
  
  std::shared_ptr<NanoMuonPair> GetLooseDimuonMatchedToGenDimuon(std::shared_ptr<MuonPair> genMuonPair, std::shared_ptr<NanoMuons> looseMuonCollection, float maxDeltaR = 0.3);
  std::shared_ptr<NanoMuons> GetLooseMuonsMatchedToGenMuons(std::shared_ptr<PhysicsObjects> genMuonCollection, std::shared_ptr<NanoMuons> looseMuonCollection, float maxDeltaR);
  std::shared_ptr<NanoMuons> GetRemainingNonResonantMuons(std::shared_ptr<NanoMuons> muonCollection, std::shared_ptr<NanoMuonPairs> resonantCollection);
  
  std::vector<int> GetFiveFirstMotherIDsOfParticle(std::shared_ptr<PhysicsObject> particle);

  float GetPhiAngleBetweenDimuonAndALP(std::shared_ptr<PhysicsObject> muon1, std::shared_ptr<PhysicsObject> muon2, std::shared_ptr<PhysicsObject> alp, bool recoMuon);

  std::shared_ptr<NanoMuon> GetLeadingMuon(std::shared_ptr<NanoMuons> muonCollection);
  bool IsLeadingMuonInCollection(std::shared_ptr<NanoMuons> collection, std::shared_ptr<NanoMuons> allMuons);
  std::shared_ptr<NanoMuons> GetTightMuonsInCollection(std::shared_ptr<NanoMuons> muonCollection);

  bool IsALPDecayWithinCMS(float CMS_Lxy_max = 600);

  std::string GetTTbarEventCategory();

  std::shared_ptr<NanoMuons> GetMuonsInVertexCollection(std::shared_ptr<PhysicsObjects> vertexCollection);

 private:
  std::shared_ptr<Event> event;
  std::unique_ptr<EventProcessor> eventProcessor;
  std::unique_ptr<NanoEventProcessor> nanoEventProcessor;
  std::string weightsBranchName;
  std::map<std::string, float> muonMatchingParams;
  std::pair<std::string, std::vector<std::string>> muonVertexCollection;

  std::vector<int> GetTopIndices();
  std::vector<int> GetBottomIndices();
  bool IsGoodParticle(int particleIndex, std::vector<int> topIndices, std::vector<int> bottomIndices);
  bool ParticlesMotherInIndices(int particleIndex, std::vector<int> indices);
  bool ParticleHasISRmotherAfterTopMother(int particleIndex);
  bool IsGoodMuonFromALP(int muonIndex);
  bool IsGoodMuonNotFromALP(int muonIndex);
  bool IsGoodMuonFromMotherWithParticleID(int genMuonIndex, int motherParticleID);
};

struct FinalState {
  std::map<std::string, int> nObjects = {
      {"neutrinos", 0}, {"electrons", 0}, {"muons", 0}, {"taus", 0}, {"udsc_jets", 0}, {"b_jets", 0},
  };

  void print() {
    for (auto& [name, count] : nObjects) {
      if (count > 0) std::cout << count << " " << name << ", ";
    }
    std::cout << std::endl;
  }

  void AddParticle(int pid) {
    if (abs(pid) == 12 || abs(pid) == 14 || abs(pid) == 16) nObjects["neutrinos"]++;
    if (abs(pid) == 11) nObjects["electrons"]++;
    if (abs(pid) == 13) nObjects["muons"]++;
    if (abs(pid) == 15) nObjects["taus"]++;
    if (abs(pid) >= 0 && abs(pid) <= 4) nObjects["udsc_jets"]++;
    if (abs(pid) == 5) nObjects["b_jets"]++;
  }

  bool IsConsistent() {
    if (nObjects["b_jets"] != 2) return false;
    int nLeptons = nObjects["electrons"] + nObjects["muons"] + nObjects["taus"];

    if (nLeptons == 2 && nObjects["neutrinos"] == 2) return true;                                // fully leptonic
    if (nLeptons == 1 && nObjects["neutrinos"] == 1 && nObjects["udsc_jets"] == 2) return true;  // semi-leptonic
    if (nObjects["udsc_jets"] == 4) return true;                                                 // fully hadronic

    return false;
  }

  std::string GetShortName() {
    if (nObjects["udsc_jets"] == 4) return "hh";
    if (nObjects["electrons"] == 2) return "ee";
    if (nObjects["muons"] == 2) return "mumu";
    if (nObjects["taus"] == 2) return "tautau";

    std::string name = "";
    if (nObjects["udsc_jets"] == 2) name += "h";
    if (nObjects["electrons"] == 1) name += "e";
    if (nObjects["muons"] == 1) name += "mu";
    if (nObjects["taus"] == 1) name += "tau";

    return name;
  }
};

#endif /* TTAlpsEvent_hpp */
