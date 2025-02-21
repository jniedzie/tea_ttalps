//  TTAlpsCuts.hpp
//
//  Created by Jeremi Niedziela on 16/08/2023.

#ifndef TTAlpsCuts_hpp
#define TTAlpsCuts_hpp

#include "ConfigManager.hpp"
#include "CutFlowManager.hpp"
#include "Event.hpp"
#include "EventProcessor.hpp"
#include "Helpers.hpp"
#include "PhysicsObject.hpp"
#include "TTAlpsDimuonCuts.hpp"

class TTAlpsCuts {
 public:
  TTAlpsCuts();
  
  void RegisterSignalLikeCuts(std::shared_ptr<CutFlowManager> cutFlowManager);
  
  void RegisterInitialDimuonCuts(std::shared_ptr<CutFlowManager> cutFlowManager, std::string dimuonCategory = "");
  void RegisterDimuonCuts(std::shared_ptr<CutFlowManager> cutFlowManager, std::string dimuonCategory = "");
  bool PassesDimuonCuts(const std::shared_ptr<Event> event, std::shared_ptr<CutFlowManager> cutFlowManager, std::string dimuonCategory = "");
  void PrintDimuonCutFlow(std::shared_ptr<CutFlowManager> cutFlowManager);
  void SaveDimuonCutFlows(std::shared_ptr<CutFlowManager> cutFlowManager);

  bool PassesSingleMuonTrigger(const std::shared_ptr<Event> event);
  bool PassesDoubleMuonTrigger(const std::shared_ptr<Event> event);

  // Cuts targetting semi-leptonic ttbar, and additional leptons. Requires:
  // - 1 good e/μ (the top-lepton)
  // - 0 other quasi-good leptons
  // - at least 4 good jets
  // - at least 1 good b-tagged jet
  // - some amount of MET
  bool PassesSingleLeptonCuts(const std::shared_ptr<Event> event, std::shared_ptr<CutFlowManager> cutFlowManager = nullptr);
  void RegisterSingleLeptonCuts(std::shared_ptr<CutFlowManager> cutFlowManager);

  // Cuts targetting ttZ, Z->μμ process. Requires:
  // - 1 good e/μ (the top-lepton)
  // - 2 additional quasi-good muons
  // - at least 4 good jets
  // - at least 1 good b-tagged jet
  // - some amount of MET
  bool PassesTTZLikeCuts(const std::shared_ptr<Event> event, std::shared_ptr<CutFlowManager> cutFlowManager = nullptr);
  void RegisterTTZLikeCuts(std::shared_ptr<CutFlowManager> cutFlowManager);

  bool PassesDileptonCuts(const std::shared_ptr<Event> event);
  bool PassesHadronCuts(const std::shared_ptr<Event> event);

 private:
  std::unique_ptr<EventProcessor> eventProcessor;
  std::map<std::string, float> muonMatchingParams;
  std::map<std::string, std::vector<std::string>> muonVertexCollections;

  bool PassesDimuonCuts(const std::shared_ptr<Event> event, std::shared_ptr<CutFlowManager> cutFlowManager, std::string collectionName, std::vector<std::string> vertexCuts, std::string dimuonCategory = "");

  std::vector<std::string> triggerWarningsPrinted;

};

#endif /* TTAlpsCuts_hpp */
