#ifndef TTAlpsHistogramFiller_hpp
#define TTAlpsHistogramFiller_hpp

#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "EventProcessor.hpp"
#include "Helpers.hpp"
#include "HistogramsHandler.hpp"
#include "NanoEventProcessor.hpp"

class TTAlpsHistogramFiller {
 public:
  TTAlpsHistogramFiller(std::shared_ptr<HistogramsHandler> histogramsHandler_);
  ~TTAlpsHistogramFiller();

  void FillDefaultVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsVariablesForLooseMuons(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsVariablesForMuonVertexCollections(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsGenMuonVertexCollectionsVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsGenMuonVariables(const std::shared_ptr<Event> event);
  void FillCustomTTAlpsMuonMatchingVariables(const std::shared_ptr<Event> event);

  void FillNormCheck();
  void FillDataCheck(const std::shared_ptr<Event> event);

  void FillDimuonCutFlows(const std::shared_ptr<CutFlowManager> cutFlowManager, std::string dimuonCategory = "");

  void FillTriggerStudyHistograms(const std::shared_ptr<Event> event, std::string triggerName);

  void FillABCDHistograms(const std::shared_ptr<Event> event);
  void FillABCDMothersHistograms(const std::shared_ptr<Event> event, bool runFakesHistograms);
  void FillFakesHistograms(const std::shared_ptr<Event> event);

  void FillMuonTriggerObjectsHistograms(const std::shared_ptr<Event> event);

  void FillMuonMatchingRatioEffectHistograms(const std::shared_ptr<Event> event);

 private:
  std::shared_ptr<HistogramsHandler> histogramsHandler;
  std::unique_ptr<EventProcessor> eventProcessor;
  std::unique_ptr<NanoEventProcessor> nanoEventProcessor;

  std::map<std::string, std::vector<std::string>> triggerSets;
  std::map<std::string, HistogramParams> defaultHistVariables;

  std::map<std::string, float> muonMatchingParams;

  std::pair<std::string, std::vector<std::string>> muonVertexCollection;
  std::string muonVertexCollectionInput;

  std::string year;

  float muonMass = 0.105;

  std::vector<std::string> triggerNames;
  bool EndsWithTriggerName(std::string name);

  // Loose Muons and Loose muon vertex histograms
  void FillLooseMuonsHistograms(const std::shared_ptr<NanoMuon> muon, const std::shared_ptr<NanoMuon> leadingTightMuon, std::string name);
  void FillLooseMuonsHistograms(const std::shared_ptr<NanoMuons> muons, const std::shared_ptr<NanoMuon> leadingTightMuon, std::string collectionName);
  void FillLooseMuonsHistograms(const std::shared_ptr<Event> event, std::string collectionName);
  
  void FillMuonVertexHistograms(const std::shared_ptr<Event> event, const std::shared_ptr<PhysicsObjects> vertexCollection, std::string vertexName);
  void FillMuonVertexHistograms(const std::shared_ptr<Event> event, std::string vertexName);
  void FillMuonVertexHistograms(const std::shared_ptr<NanoDimuonVertex> dimuon, std::string name);

  // Dimuon Vertex Collection Histograms
  void FillNminus1HistogramsForMuonVertexCollection(const std::shared_ptr<Event> event);

  // Nminus1 LLPnanoAOD histograms
  void FillDimuonVertexNminus1HistogramForCut(std::string collectionName, std::string cut, std::shared_ptr<NanoDimuonVertex> dimuonVertex);

  // Gen-Level histograms
  void FillGenALPsHistograms(const std::shared_ptr<Event> event);
  void FillGenDimuonResonancesHistograms(const std::shared_ptr<Event> event);
  void FillGenMatchedLooseMuonsHistograms(const std::shared_ptr<Event> event);
  // void FillLooseMuonsNotFromALPsHistograms(const std::shared_ptr<Event> event);
  void FillLooseMuonsFromWsHistograms(const std::shared_ptr<Event> event);

  void FillGenDimuonHistograms(std::shared_ptr<MuonPair> muonPair, std::string collectionName, const std::shared_ptr<Event> event);
  void FillGenMuonMinDRHistograms(const std::shared_ptr<PhysicsObject> genMuon, const std::shared_ptr<NanoMuons> muonCollection,
                                  std::string genMuonCollectionName, std::string looseMuonCollectionName);
  void FillRecoGenMatchedResonanceHistograms(const std::shared_ptr<Event> event, const std::shared_ptr<NanoMuons> muonCollection,
                                             std::string collectionName, const std::shared_ptr<PhysicsObjects> vertexCollection = nullptr);
  void FillRecoGenSingleMuonHistograms(const std::shared_ptr<Event> event, const std::shared_ptr<PhysicsObjects> vertexCollection, std::string collectionName);

  // Gen-Level Dimuon Vertex Collection Histograms
  void FillMuonCollectionFromALPsNminus1Histograms(const std::shared_ptr<Event> event);

  // Muon Matching histograms
  void FillMatchedMuonHistograms(const std::shared_ptr<NanoMuon> muon, std::string muonCollectionName);
  void FillMatchingHistograms(const std::shared_ptr<Event> event, std::string patMuonCollection, std::string dsaMuonCollection);
};

#endif /* TTAlpsHistogramFiller_hpp */
