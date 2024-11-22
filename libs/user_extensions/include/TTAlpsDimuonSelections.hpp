
#ifndef TTAlpsDimuonSelections_hpp
#define TTAlpsDimuonSelections_hpp

#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "EventProcessor.hpp"
#include "Helpers.hpp"
#include "PhysicsObject.hpp"
#include "NanoDimuonVertex.hpp"

class TTAlpsDimuonSelections {
 public:
  TTAlpsDimuonSelections();
  
  bool PassesLLPnanoAODVertexCuts(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesInvariantMassCuts(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesChargeCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDisplacedIsolationCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex, std::string isolationVariable="displacedTrackIso03Dimuon");
  bool PassesHitsInFrontOfVertexCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDPhiBetweenMuonpTAndLxyCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDCACut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesChi2Cut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesVxyCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesCollinearityAngleCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDeltaEtaCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDeltaPhiCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDeltaRCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDeltaPixelHits(std::shared_ptr<NanoDimuonVertex> dimuonVertex);

  bool PassesCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex, std::string cutName);
  
 private:
  std::map<std::string, float> dimuonVertexBaseCuts;
  std::map<std::string, float> dimuonVertexPATCuts;
  std::map<std::string, float> dimuonVertexPATDSACuts;
  std::map<std::string, float> dimuonVertexDSACuts;
  std::string dimuonSelection;

  std::map<std::string, float> GetDimuonCategoryMap(std::string category);
  std::map<std::string, std::function<bool(std::shared_ptr<NanoDimuonVertex>)>> PassesCutsMap;
};

#endif /* TTAlpsDimuonSelections_hpp */
