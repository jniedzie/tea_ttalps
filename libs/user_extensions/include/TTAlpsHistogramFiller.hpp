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

  void FillTriggerEfficiencies();
  void FillTriggerVariables(const std::shared_ptr<Event> event, std::string prefix = "", std::string suffix = "");
  void FillTriggerVariablesPerTriggerSet(const std::shared_ptr<Event> event, std::string ttbarCategory = "");

  void FillLeadingPt(const std::shared_ptr<Event> event, std::string histName, const HistogramParams &params);
  void FillAllSubLeadingPt(const std::shared_ptr<Event> event, std::string histName, const HistogramParams &params);

  void FillDefaultVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsVariablesFromLLPNanoAOD(const std::shared_ptr<Event> event);
  void FillCustomTTAlps2DVariablesFromLLPNanoAOD(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsDimuonNminus1Variables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsGenMuonVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsMuonMatchingVariables(const std::shared_ptr<Event> event);

  void FillNormCheck(const std::shared_ptr<Event> event);

  void FillBasicMuonVertexHistograms(const std::shared_ptr<Event> event);

 private:

  bool nonIsolatedLooseMuons = false;

  std::shared_ptr<HistogramsHandler> histogramsHandler;
  std::unique_ptr<EventProcessor> eventProcessor;
  std::unique_ptr<NanoEventProcessor> nanoEventProcessor;

  std::map<std::string, std::vector<std::string>> triggerSets;
  std::map<std::string, HistogramParams> defaultHistVariables;
  std::map<std::string, HistogramParams> ttalpsHistVariables;

  std::map<std::string, float> muonMatchingParams;
  
  std::vector<std::string> triggerNames;
  bool EndsWithTriggerName(std::string name);

  float GetEventWeight(const std::shared_ptr<Event> event);
  float GetObjectWeight(const std::shared_ptr<PhysicsObject> object, std::string collectionName);

  void FillDimuonHistograms(const std::shared_ptr<Event> event);
  void FillDiumonClosestToZhistgrams(const std::shared_ptr<Event> event);
  void FillMuonMetHistograms(const std::shared_ptr<Event> event);
  void FillJetHistograms(const std::shared_ptr<Event> event);

  void FillDimuonHistograms(const std::shared_ptr<PhysicsObject> muon1, const std::shared_ptr<PhysicsObject> muon2, std::string collectionName, float weight, bool genLevel);
  void FillMuonMinDeltaRHistograms(const std::shared_ptr<Event> event, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> muonCollection, std::string collectionName);
  void FillMuonMinDeltaRHistograms(const std::shared_ptr<Event> event, std::string collectionName);

  // LLPnanoAOD histograms
  void FillLLPnanoAODLooseMuonsHistograms(const std::shared_ptr<Event> event);
  void FillLLPnanoAODLooseMuonsVertexHistograms(const std::shared_ptr<Event> event);
  void FillLooseMuonsHistograms(const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> objectCollection, std::string collectionName, float weight);
  void FillLooseMuonsHistograms(const std::shared_ptr<Event> event, std::string collectionName);
  void FillMuonVertexHistograms(const std::shared_ptr<Event> event, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> vertexCollection, std::string vertexName);
  void FillMuonVertexHistograms(const std::shared_ptr<Event> event, std::string vertexName);
  
  // LLPnanoAOD 3D histograms
  void FillMuonVertexCorrelationHistograms(const std::shared_ptr<Event> event, std::string vertexName);

  // Gen-Level histograms
  void FillGenMuonMinDR(const std::shared_ptr<PhysicsObject> genMuon, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> muonCollection, std::string muonCollectionName, float weight);
  void FillGenALPsHistograms(const std::shared_ptr<Event> event);
  void FillGenMuonsFromALPsHistograms(const std::shared_ptr<Event> event);
  void FillLooseMuonsFromALPsHistograms(const std::shared_ptr<Event> event);

  // Muon Matching histograms
  void FillMatchedMuonHistograms(const std::shared_ptr<PhysicsObject> muon, std::string muonCollectionName, float weight);  
  void FillMatchingHistograms(const std::shared_ptr<Event> event, std::string patMuonCollection, std::string dsaMuonCollection);

};

#endif /* TTAlpsHistogramFiller_hpp */
