
#ifndef TTAlpsDimuonCuts_hpp
#define TTAlpsDimuonCuts_hpp

#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "EventProcessor.hpp"
#include "Helpers.hpp"
#include "PhysicsObject.hpp"
#include "NanoDimuonVertex.hpp"

class TTAlpsDimuonCuts {
 public:
  TTAlpsDimuonCuts();
  
  bool PassesLLPnanoAODVertexCuts(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesInvariantMassCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesChargeCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDisplacedIsolationCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex, std::string isolationVariable="displacedTrackIso03Dimuon");
  bool PassesPFRelIsolationCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesHitsInFrontOfVertexCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDPhiBetweenMuonpTAndLxyCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDCACut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesChi2Cut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesLxyCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesLogLxyCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex, float* logLxyMin = nullptr);
  bool PassesCollinearityAngleCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDeltaEtaCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDeltaPhiCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDeltaRCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDeltaPixelHitsCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesBarrelDeltaEtaCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesChi2DCACut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesDxyCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesMuonPtCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);
  bool PassesCos3DAngleCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex);

  bool PassesCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex, std::string cutName);
  
 private:
  std::map<std::string, float> dimuonVertexPATCuts;
  std::map<std::string, float> dimuonVertexPATDSACuts;
  std::map<std::string, float> dimuonVertexDSACuts;
  std::string dimuonSelection;

  std::map<std::string, float> GetDimuonCategoryMap(std::string category);
  std::map<std::string, std::function<bool(std::shared_ptr<NanoDimuonVertex>)>> PassesCutsMap;

  float LogLxyMinus1 = -1.0f;
  float LogLxyMinus2 = -2.0f;
  float LogLxyMinus3 = -3.0f;
};

#endif /* TTAlpsDimuonCuts_hpp */
