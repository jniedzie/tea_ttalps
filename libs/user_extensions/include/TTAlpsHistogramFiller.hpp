#ifndef TTAlpsHistogramFiller_hpp
#define TTAlpsHistogramFiller_hpp

#include "Event.hpp"
#include "EventProcessor.hpp"
#include "Helpers.hpp"
#include "HistogramsHandler.hpp"
#include "CutFlowManager.hpp"

class TTAlpsHistogramFiller {
 public:
  TTAlpsHistogramFiller(std::shared_ptr<ConfigManager> _config, std::shared_ptr<HistogramsHandler> histogramsHandler_);
  ~TTAlpsHistogramFiller();

  void FillTriggerEfficiencies();
  void FillTriggerVariables(const std::shared_ptr<Event> event, std::string prefix = "", std::string suffix = "");
  void FillTriggerVariablesPerTriggerSet(const std::shared_ptr<Event> event, std::string ttbarCategory = "");

  void FillLeadingPt(const std::shared_ptr<Event> event, std::string histName, std::vector<std::string> variableLocation);
  void FillAllSubLeadingPt(const std::shared_ptr<Event> event, std::string histName, std::vector<std::string> variableLocation);

  void FillCustomTTAlpsVariables(const std::shared_ptr<Event> event);

 private:
  std::shared_ptr<HistogramsHandler> histogramsHandler;
  std::unique_ptr<EventProcessor> eventProcessor;

  std::map<std::string, std::vector<std::string>> triggerSets;
  std::map<std::string, std::vector<std::string>> defaultHistVariables;
  std::map<std::string, std::vector<std::string>> ttalpsHistVariables;

  std::string weightsBranchName;

  std::vector<std::string> triggerNames;
  bool EndsWithTriggerName(std::string name);
};

#endif /* TTAlpsHistogramFiller_hpp */
