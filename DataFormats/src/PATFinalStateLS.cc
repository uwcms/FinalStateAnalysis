#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"
#include "FinalStateAnalysis/DataFormats/interface/SmartTrigger.h"

PATFinalStateLS::PATFinalStateLS() {}

PATFinalStateLS::PATFinalStateLS(const LuminosityBlockID& id,
        const LumiSumary& lumiSummary):
  id_(id),lumiSummary_(lumiSummary) {}


const LuminosityBlockID&
PATFinalStateLS::id() const { return id_; }

const LumiSumary&
PATFinalStateLS::lumiSummary() const { return lumiSummary_; }

double PATFinalStateLS::instantaneousLumi() const {
  return lumiSummary_.instRecLumi();
}

double PATFinalStateLS::intLumi() const {
  return lumiSummary_.intRecLumi();
}

double PATFinalStateLS::intLumi(const std::string& triggers) const {
  SmartTriggerResult result = smartTrigger(triggers, lumiSummary_);
  int prescale = result.prescale;
  if (prescale == 0)
    return 0.;
  else
    return lumiSummary_.intRecLumi()/prescale;
}
