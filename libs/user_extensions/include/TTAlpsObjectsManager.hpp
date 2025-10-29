#ifndef TTAlpsObjectsManager_hpp
#define TTAlpsObjectsManager_hpp

#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "Helpers.hpp"
#include "UserExtensionsHelpers.hpp"
#include "TTAlpsDimuonCuts.hpp"
#include "TTAlpsCuts.hpp"

class TTAlpsObjectsManager;
// pair< muonVertexCollectionName, muonVertexCollectionCuts >
typedef std::pair<std::string, std::vector<std::string>> MuonVertexCollectionSetup;

class TTAlpsObjectsManager {
 public:
  TTAlpsObjectsManager();
  ~TTAlpsObjectsManager() = default;

  void InsertMatchedLooseMuonsCollections(std::shared_ptr<Event> event);
  void InsertDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR, std::shared_ptr<NanoMuons> muonCollection = nullptr);
  void InsertOuterDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR, std::shared_ptr<NanoMuons> muonCollection = nullptr);
  void InsertProximityDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR, std::shared_ptr<NanoMuons> muonCollection = nullptr);
  void InsertSegmentMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float minSegmentRatio, std::shared_ptr<NanoMuons> muonCollection = nullptr);

  void InsertNonLeadingLooseMuonsCollections(std::shared_ptr<Event> event);

  void InsertBaseLooseMuonVertexCollection(std::shared_ptr<Event> event);
  void InsertMuonVertexCollection(std::shared_ptr<Event> event);
  void InsertMuonVertexCollection(std::shared_ptr<Event> event, std::shared_ptr<PhysicsObjects> vertices, 
                                  MuonVertexCollectionSetup muonVertexCollectionInput = MuonVertexCollectionSetup());
  void InsertNminus1VertexCollections(std::shared_ptr<Event> event);
  void InsertMatchedLooseMuonEfficiencyCollections(std::shared_ptr<Event> event);
  void InsertMuonTriggerCollections(std::shared_ptr<Event> event);

  // Get DSA and PAT muons that have been matched
  void InsertRevertedMatchedMuonsCollections(std::shared_ptr<Event> event);
  // Get PAT-DSA and DSA-DSA vertices matched to PAT-PAT dimuons
  void InsertRevertedMatchedDSAMuonVertexCollection(std::shared_ptr<Event> event);


 private:

  std::unique_ptr<TTAlpsDimuonCuts> ttAlpsCuts;

  std::map<std::string, float> muonMatchingParams;
  std::map<std::string, float> dimuonVertexCuts;
  MuonVertexCollectionSetup muonVertexCollection;
  std::string muonVertexCollectionInput;
  bool applySegmentMatchingAfterSelections = false;

  bool IsGoodBaseMuonVertex(const std::shared_ptr<PhysicsObject> vertex, std::shared_ptr<Event> event);
  std::shared_ptr<PhysicsObject> GetBestMuonVertex(const std::shared_ptr<PhysicsObjects> vertices, std::shared_ptr<Event> event);
  std::shared_ptr<PhysicsObject> GetSecondBestMuonVertex(const std::shared_ptr<PhysicsObjects> vertices, std::shared_ptr<Event> event);

};

#endif /* TTAlpsEvent_hpp */