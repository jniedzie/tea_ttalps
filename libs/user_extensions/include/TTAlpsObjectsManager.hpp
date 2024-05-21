#ifndef TTAlpsObjectsManager_hpp
#define TTAlpsObjectsManager_hpp

#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "Helpers.hpp"
#include "UserExtensionsHelpers.hpp"

class TTAlpsObjectsManager {
 public:
  TTAlpsObjectsManager();
  ~TTAlpsObjectsManager() = default;

  void InsertMatchedLooseMuonsCollections(std::shared_ptr<Event> event);
  void InsertDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR);
  void InsertOuterDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR);
  void InsertProximityDRMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float maxDR);
  void InsertSegmentMatchedLooseMuonsCollections(std::shared_ptr<Event> event, float minSegmentRatio);
  void InsertGoodLooseMuonVertexCollection(std::shared_ptr<Event> event);
  void InsertMatchedLooseMuonEfficiencyCollections(std::shared_ptr<Event> event);

 private:

  std::map<std::string, float> muonMatchingParams;

  bool IsGoodMuonVertex(const std::shared_ptr<PhysicsObject> vertex, std::shared_ptr<Event> event);
  bool IsGoodDisplacedMuonVertex(const std::shared_ptr<PhysicsObject> vertex, std::shared_ptr<Event> event);
  bool IsGoodMuonVertexWithLargeDR(const std::shared_ptr<PhysicsObject> vertex, std::shared_ptr<Event> event);

};

#endif /* TTAlpsEvent_hpp */