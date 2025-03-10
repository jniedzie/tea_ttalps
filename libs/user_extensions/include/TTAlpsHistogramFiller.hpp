#ifndef TTAlpsHistogramFiller_hpp
#define TTAlpsHistogramFiller_hpp

#include "Event.hpp"
#include "EventProcessor.hpp"
#include "Helpers.hpp"
#include "HistogramsHandler.hpp"
#include "CutFlowManager.hpp"
#include "NanoEventProcessor.hpp"

class TTAlpsHistogramFiller {
 public:
  TTAlpsHistogramFiller(std::shared_ptr<HistogramsHandler> histogramsHandler_);
  ~TTAlpsHistogramFiller();

  void FillLeadingPt(const std::shared_ptr<Event> event, std::string histName, const HistogramParams &params);
  void FillAllSubLeadingPt(const std::shared_ptr<Event> event, std::string histName, const HistogramParams &params);

  void FillDefaultVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsVariablesFromLLPNanoAOD(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsGenMuonVertexCollectionsVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsGenMuonVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsMuonMatchingVariables(const std::shared_ptr<Event> event);
  void FillGenLevelMuonCollectionHistograms(const std::shared_ptr<Event> event);

  void FillNormCheck(const std::shared_ptr<Event> event);

  void FillDimuonCutFlows(const std::shared_ptr<CutFlowManager> cutFlowManager, std::string dimuonCategory = "");

  void FillTriggerStudyHistograms(const std::shared_ptr<Event> event, std::string triggerName);

  void FillABCDHistograms(const std::shared_ptr<Event> event, std::string abcdCollection);

 private:

  std::shared_ptr<HistogramsHandler> histogramsHandler;
  std::unique_ptr<EventProcessor> eventProcessor;
  std::unique_ptr<NanoEventProcessor> nanoEventProcessor;

  std::map<std::string, std::vector<std::string>> triggerSets;
  std::map<std::string, HistogramParams> defaultHistVariables;

  std::map<std::string, float> muonMatchingParams;

  std::vector<std::string> muonVertexCollectionNames;
  std::map<std::string, std::vector<std::string>> muonVertexCollections;
  std::vector<std::string> muonVertexNminus1Collections;
  
  std::vector<std::string> triggerNames;
  bool EndsWithTriggerName(std::string name);

  float GetEventWeight(const std::shared_ptr<Event> event);
  float GetObjectWeight(const std::shared_ptr<PhysicsObject> object, std::string collectionName);

  void FillDimuonHistograms(const std::shared_ptr<PhysicsObject> muon1, const std::shared_ptr<PhysicsObject> muon2, std::string collectionName, const std::shared_ptr<Event> event, bool genLevel);
  void FillMuonMinDeltaRHistograms(const std::shared_ptr<Event> event, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> muonCollection, std::string collectionName);
  void FillMuonMinDeltaRHistograms(const std::shared_ptr<Event> event, std::string collectionName);

  // LLPnanoAOD histograms
  void FillLLPnanoAODLooseMuonsHistograms(const std::shared_ptr<Event> event);
  void FillLLPnanoAODLooseMuonsVertexHistograms(const std::shared_ptr<Event> event);
  void FillLLPnanoAODLooseMuonsNminus1VertexHistograms(const std::shared_ptr<Event> event);
  void FillLooseMuonsHistograms(const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> objectCollection, std::string collectionName, float weight);
  void FillLooseMuonsHistograms(const std::shared_ptr<Event> event, std::string collectionName);
  void FillMuonVertexHistograms(const std::shared_ptr<Event> event, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> vertexCollection, std::string vertexName);
  void FillMuonVertexHistograms(const std::shared_ptr<Event> event, std::string vertexName);

  // Nminus1 LLPnanoAOD histograms
  void FillDimuonVertexNminus1HistogramForCut(std::string collectionName, std::string cut, std::shared_ptr<NanoDimuonVertex> dimuonVertex, float weight);
  
  // LLPnanoAOD 3D histograms
  void FillMuonVertexCorrelationHistograms(const std::shared_ptr<Event> event, std::string vertexName);

  // Gen-Level histograms
  void FillGenMuonMinDRHistograms(const std::shared_ptr<PhysicsObject> genMuon, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> muonCollection, std::string genMuonCollectionName, std::string looseMuonCollectionName, float weight);
  void FillGenMuonMinDRHistograms(const std::shared_ptr<PhysicsObject> genMuon, const std::shared_ptr<PhysicsObject> looseMuon, std::string genMuonCollectionName, std::string looseMuonCollectionName, float weight);
  void FillGenALPsHistograms(const std::shared_ptr<Event> event);
  void FillGenMuonsFromALPsHistograms(const std::shared_ptr<Event> event);
  void FillGenMuonsNotFromALPsHistograms(const std::shared_ptr<Event> event);
  void FillLooseMuonsFromALPsHistograms(const std::shared_ptr<Event> event);
  void FillLooseMuonsFromALPsNminus1Histograms(const std::shared_ptr<Event> event);
  void FillLooseMuonsNotFromALPsHistograms(const std::shared_ptr<Event> event);
  void FillLooseMuonsFromWsHistograms(const std::shared_ptr<Event> event);

  // Muon Matching histograms
  void FillMatchedMuonHistograms(const std::shared_ptr<PhysicsObject> muon, std::string muonCollectionName, float weight);  
  void FillMatchingHistograms(const std::shared_ptr<Event> event, std::string patMuonCollection, std::string dsaMuonCollection);

};

#endif /* TTAlpsHistogramFiller_hpp */
