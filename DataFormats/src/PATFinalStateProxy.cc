#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateProxy.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"

PATFinalStateProxy::PATFinalStateProxy(PATFinalState* finalState):
  finalState_(finalState) {}

PATFinalStateProxy::PATFinalStateProxy() {}

const PATFinalState* PATFinalStateProxy::get() const {
  return finalState_.get();
}

const PATFinalState* PATFinalStateProxy::operator->() const {
  return finalState_.get();
}
