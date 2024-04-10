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

  void InsertLooseMuonsMatchedCollections(std::shared_ptr<Event> event);
  void InsertLooseMuonVerticesMatchedCollections(std::shared_ptr<Event> event);
  void InsertGoodLooseMuonVertexCollection(std::shared_ptr<Event> event);
  void InsertLooseMuonMatchingEfficiencyCollections(std::shared_ptr<Event> event);

 private:

  bool IsGoodMuonVertex(const std::shared_ptr<PhysicsObject> vertex, std::shared_ptr<Event> event);

};

#endif /* TTAlpsEvent_hpp */