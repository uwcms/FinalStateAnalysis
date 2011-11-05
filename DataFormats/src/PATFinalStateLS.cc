#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"
#include "FinalStateAnalysis/DataFormats/interface/SmartTrigger.h"

PATFinalStateLS::PATFinalStateLS() {}

PATFinalStateLS::PATFinalStateLS(const edm::LuminosityBlockID& id,
        double integratedLuminosity,
        double instantaneousLumi,
        const std::vector<LumiSummary::HLT>& hltInfos,
        const std::vector<LumiSummary::L1>& l1Infos):
  id_(id),
  integratedLumi_(integratedLuminosity),
  instaneousLumi_(instantaneousLumi),
  hltInfos_(hltInfos),l1Infos_(l1Infos) {}

const edm::LuminosityBlockID&
PATFinalStateLS::lsID() const { return id_; }

double PATFinalStateLS::instantaneousLumi() const {
  return instaneousLumi_;
}

double PATFinalStateLS::intLumi() const {
  return integratedLumi_;
}

double PATFinalStateLS::intLumi(const std::string& triggers) const {
  return -1;
  // FIXME
//  SmartTriggerResult result = smartTrigger(triggers, lumiSummary_);
//  int prescale = result.prescale;
//  if (prescale == 0)
//    return 0.;
//  else
//    return intLumi()/prescale;
}
