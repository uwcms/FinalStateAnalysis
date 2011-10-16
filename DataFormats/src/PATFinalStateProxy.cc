#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateProxy.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"

PATFinalStateProxy::PATFinalStateProxy(PATFinalStateProxy* finalState):
  finalState_(finalState) {}

const PATFinalState* PATFinalStateProxy::get() const {
  return finalState_.get();
}

const PATFinalState& PATFinalStateProxy::operator->() const {
  return *finalState_;
}
