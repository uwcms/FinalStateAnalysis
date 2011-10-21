#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"
#include "FinalStateAnalysis/DataFormats/interface/SmartTrigger.h"

PATFinalStateLS::PATFinalStateLS() {}

PATFinalStateLS::PATFinalStateLS(const edm::LuminosityBlockID& id,
        const LumiSummary& lumiSummary):
  id_(id),lumiSummary_(lumiSummary) {}


const edm::LuminosityBlockID&
PATFinalStateLS::id() const { return id_; }

const LumiSummary&
PATFinalStateLS::lumiSummary() const { return lumiSummary_; }

double PATFinalStateLS::instantaneousLumi() const {
  return lumiSummary_.avgInsRecLumi();
}

double PATFinalStateLS::intLumi() const {
  return lumiSummary_.intgRecLumi();
}

double PATFinalStateLS::intLumi(const std::string& triggers) const {
  SmartTriggerResult result = smartTrigger(triggers, lumiSummary_);
  int prescale = result.prescale;
  if (prescale == 0)
    return 0.;
  else
    return lumiSummary_.intgRecLumi()/prescale;
}
