#ifndef TTAlpsObjectsManager_hpp
#define TTAlpsObjectsManager_hpp

#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "Helpers.hpp"
#include "UserExtensionsHelpers.hpp"
#include "TTAlpsDimuonCuts.hpp"
#include "TTAlpsCuts.hpp"

class TTAlpsObjectsManager {
 public:
  TTAlpsObjectsManager();
  ~TTAlpsObjectsManager() = default;

  void InsertMatchedLooseMuonsCollections(std::shared_ptr<Event> event);
  void InsertDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR, std::shared_ptr<NanoMuons> muonCollection = nullptr);
  void InsertOuterDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR, std::shared_ptr<NanoMuons> muonCollection = nullptr);
  void InsertProximityDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR, std::shared_ptr<NanoMuons> muonCollection = nullptr);
  void InsertSegmentMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float minSegmentRatio, std::shared_ptr<NanoMuons> muonCollection = nullptr);

  void InsertBaseLooseMuonVertexCollection(std::shared_ptr<Event> event);
  void InsertMuonVertexCollection(std::shared_ptr<Event> event);
  void InsertMuonVertexCollection(std::shared_ptr<Event> event, std::shared_ptr<PhysicsObjects> vertices, std::pair<std::string, 
                                  std::vector<std::string>> muonVertexCollectionInput = std::pair<std::string, std::vector<std::string>>());
  void InsertNminus1VertexCollections(std::shared_ptr<Event> event);
  void InsertMatchedLooseMuonEfficiencyCollections(std::shared_ptr<Event> event);
  void InsertMuonTriggerCollections(std::shared_ptr<Event> event);
  void InsertNonLeadingMuonVertexCollections(std::shared_ptr<Event> event, std::string inputCollection = "");

 private:

  std::unique_ptr<TTAlpsDimuonCuts> ttAlpsCuts;

  std::map<std::string, float> muonMatchingParams;
  std::map<std::string, float> dimuonVertexCuts;
  std::pair<std::string, std::vector<std::string>> muonVertexCollection;
  std::string muonVertexCollectionInput;
  bool applySegmentMatchingAfterSelections = false;

  bool IsGoodBaseMuonVertex(const std::shared_ptr<PhysicsObject> vertex, std::shared_ptr<Event> event);
  std::shared_ptr<PhysicsObject> GetBestMuonVertex(const std::shared_ptr<PhysicsObjects> vertices, std::shared_ptr<Event> event);
  std::shared_ptr<PhysicsObject> GetSecondBestMuonVertex(const std::shared_ptr<PhysicsObjects> vertices, std::shared_ptr<Event> event);

};

#endif /* TTAlpsEvent_hpp */