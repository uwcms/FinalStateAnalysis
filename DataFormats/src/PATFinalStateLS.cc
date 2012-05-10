#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLS.h"
#include "FinalStateAnalysis/DataAlgos/interface/SmartTrigger.h"

PATFinalStateLS::PATFinalStateLS() {}

PATFinalStateLS::PATFinalStateLS(const edm::LuminosityBlockID& id,
        double integratedLuminosity,
        double instantaneousLumi):
  id_(id),
  integratedLumi_(integratedLuminosity),
  instaneousLumi_(instantaneousLumi) {}

const edm::LuminosityBlockID&
PATFinalStateLS::lsID() const { return id_; }

double PATFinalStateLS::instantaneousLumi() const {
  return instaneousLumi_;
}

double PATFinalStateLS::intLumi() const {
  return integratedLumi_;
}
