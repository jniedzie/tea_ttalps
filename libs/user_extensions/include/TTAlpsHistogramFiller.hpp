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
  void FillCustomTTAlpsVariablesForLooseMuons(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsVariablesForMuonVertexCollections(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsGenMuonVertexCollectionsVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsGenMuonVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsMuonMatchingVariables(const std::shared_ptr<Event> event);

  void FillNormCheck(const std::shared_ptr<Event> event);

  void FillDimuonCutFlows(const std::shared_ptr<CutFlowManager> cutFlowManager, std::string dimuonCategory = "");

  void FillTriggerStudyHistograms(const std::shared_ptr<Event> event, std::string triggerName);

  void FillABCDHistograms(const std::shared_ptr<Event> event, std::vector<std::string> abcdCollections);

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

  std::string year;

  float muonMass = 0.105;
  
  std::vector<std::string> triggerNames;
  bool EndsWithTriggerName(std::string name);

  float GetEventWeight(const std::shared_ptr<Event> event);
  float GetObjectWeight(const std::shared_ptr<PhysicsObject> object, std::string collectionName);

  // Loose Muons and Loose muon vertex histograms
  void FillLooseMuonsHistograms(const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> objectCollection, std::string collectionName, float weight);
  void FillLooseMuonsHistograms(const std::shared_ptr<Event> event, std::string collectionName);
  void FillMuonVertexHistograms(const std::shared_ptr<Event> event, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> vertexCollection, std::string vertexName);
  void FillMuonVertexHistograms(const std::shared_ptr<Event> event, std::string vertexName);

  // Dimuon Vertex Collection Histograms
  void FillNminus1HistogramsForBestMuonVertexCollections(const std::shared_ptr<Event> event);

  // Nminus1 LLPnanoAOD histograms
  void FillDimuonVertexNminus1HistogramForCut(std::string collectionName, std::string cut, std::shared_ptr<NanoDimuonVertex> dimuonVertex, float weight);
  
  // Gen-Level histograms
  void FillGenALPsHistograms(const std::shared_ptr<Event> event);
  void FillGenDimuonResonancesHistograms(const std::shared_ptr<Event> event);
  void FillGenMatchedLooseMuonsHistograms(const std::shared_ptr<Event> event);
  // void FillLooseMuonsNotFromALPsHistograms(const std::shared_ptr<Event> event);
  void FillLooseMuonsFromWsHistograms(const std::shared_ptr<Event> event);

  void FillGenDimuonHistograms(std::shared_ptr<MuonPair> muonPair, std::string collectionName, const std::shared_ptr<Event> event);
  void FillGenMuonMinDRHistograms(const std::shared_ptr<PhysicsObject> genMuon, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject> >> muonCollection, std::string genMuonCollectionName, std::string looseMuonCollectionName, float weight);
  void FillRecoGenMatchedResonanceHistograms(const std::shared_ptr<Event> event, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject>>> muonCollection,
    std::string collectionName, const std::shared_ptr<Collection<std::shared_ptr<PhysicsObject>>> vertexCollection = nullptr);

  // Gen-Level Dimuon Vertex Collection Histograms
  void FillMuonCollectionFromALPsNminus1Histograms(const std::shared_ptr<Event> event);

  // Muon Matching histograms
  void FillMatchedMuonHistograms(const std::shared_ptr<PhysicsObject> muon, std::string muonCollectionName, float weight);  
  void FillMatchingHistograms(const std::shared_ptr<Event> event, std::string patMuonCollection, std::string dsaMuonCollection);

};

#endif /* TTAlpsHistogramFiller_hpp */
