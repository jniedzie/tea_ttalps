#ifndef TTAlpsObjectsManager_hpp
#define TTAlpsObjectsManager_hpp

#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "Helpers.hpp"
#include "UserExtensionsHelpers.hpp"
#include "TTAlpsDimuonSelections.hpp"
#include "TTAlpsSelections.hpp"

class TTAlpsObjectsManager {
 public:
  TTAlpsObjectsManager();
  ~TTAlpsObjectsManager() = default;

  void InsertMatchedLooseMuonsCollections(std::shared_ptr<Event> event);
  void InsertDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR, std::shared_ptr<Collection<std::shared_ptr<PhysicsObject>>> muonCollection = nullptr);
  void InsertOuterDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR, std::shared_ptr<Collection<std::shared_ptr<PhysicsObject>>> muonCollection = nullptr);
  void InsertProximityDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR, std::shared_ptr<Collection<std::shared_ptr<PhysicsObject>>> muonCollection = nullptr);
  void InsertSegmentMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float minSegmentRatio, std::shared_ptr<Collection<std::shared_ptr<PhysicsObject>>> muonCollection = nullptr);
  void InsertBaseLooseMuonVertexCollection(std::shared_ptr<Event> event);
  void InsertGoodLooseMuonVertexCollection(std::shared_ptr<Event> event);
  void InsertGoodLooseMuonVertexCollection(std::shared_ptr<Event> event, std::string muonVertexCollectionName, std::vector<std::string> muonVertexCollectionCuts);
  void InsertNminus1VertexCollections(std::shared_ptr<Event> event);
  void InsertNminus1VertexCollections(std::shared_ptr<Event> event, std::string muonVertexCollectionName, std::vector<std::string> muonVertexCollectionCuts);
  void InsertMatchedLooseMuonEfficiencyCollections(std::shared_ptr<Event> event);

 private:

  bool useNonIsolatedLooseMuons = false;

  std::unique_ptr<TTAlpsDimuonSelections> ttAlpsSelections;

  std::map<std::string, float> muonMatchingParams;
  std::map<std::string, float> dimuonVertexCuts;
  std::map<std::string, std::vector<std::string>> muonVertexCollections;
  std::vector<std::string> muonVertexNminus1Collections;

  bool IsGoodBaseMuonVertex(const std::shared_ptr<PhysicsObject> vertex, std::shared_ptr<Event> event);
  std::shared_ptr<PhysicsObject> GetBestMuonVertex(const std::shared_ptr<PhysicsObjects> vertices, std::shared_ptr<Event> event);
  std::shared_ptr<PhysicsObject> GetSecondBestMuonVertex(const std::shared_ptr<PhysicsObjects> vertices, std::shared_ptr<Event> event);

};

#endif /* TTAlpsEvent_hpp */