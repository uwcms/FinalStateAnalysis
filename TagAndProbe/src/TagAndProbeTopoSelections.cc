#include "FinalStateAnalysis/TagAndProbe/interface/TagAndProbeTopoSelections.h"

TagAndProbeTopoSelector::TagAndProbeTopoSelector(const edm::ParameterSet& pset):
  TagAndProbeBaseSelector(pset),
  topoCut_(pset.getParameter<std::string>("topoCut")) {
  // register cuts
  muSysTag_ = pset.getParameter<std::string>("muSysTag");
  tauSysTag_ = pset.getParameter<std::string>("tauSysTag");
  metSysTag_ = pset.getParameter<std::string>("metSysTag");

  visPZetaFactor_ = pset.getParameter<double>("visPZetaFactor");
  pZetaDiffMin_ = pset.getParameter<double>("pZetaDiffMin");
  pZetaDiffMax_ = pset.getParameter<double>("pZetaDiffMax");
  deltaPhiMax_ = pset.getParameter<double>("deltaPhiMax");
  /*code*/

  std::string chargeType = pset.getParameter<std::string>("charge");

  if (chargeType == "OS")
    isOS_ = true;
  else if (chargeType == "SS")
    isOS_ = false;
  else
    assert("bad charge type!");

  push_back("TopoCut");
  push_back("DeltaPhi", deltaPhiMax_);
  push_back("PZeta", pZetaDiffMin_);
  push_back(chargeType);

  topoCutIndex_ = index_type(&bits_, "TopoCut");
  deltaPhiIndex_ = index_type(&bits_, "DeltaPhi");
  pZetaCutIndex_ = index_type(&bits_, "PZeta");
  signCutIndex_ = index_type(&bits_, chargeType);

  // Turn on all cuts
  bits_.set(true);

  loadIgnored(pset);
}


bool TagAndProbeTopoSelector::operator()(const PATMuTauSystematicsPtrs& input,
    pat::strbitset& ret) {
  clear();
  ret.set(false);
  for (size_t i = 0; i < input.size(); ++i) {
    // Load all the stuff
    const PATMuTauSystematics* muTauRef = input.at(i);
    const PATMuTauSystematics& muTau = *muTauRef;
    const pat::Muon& muon = *muTau.daughter1();
    const pat::Tau& tau = *muTau.daughter2();

    if (topoCut_(muTau) || ignoreCut(topoCutIndex_)) {
      passCutFilter(topoCutIndex_, ret, muTauRef);
      if (std::abs(muTau.deltaPhi12(muSysTag_, tauSysTag_)) < deltaPhiMax_ ||
          ignoreCut(deltaPhiIndex_)) {
        passCutFilter(deltaPhiIndex_, ret, muTauRef);

        std::pair<double,double> pZetaInfo = muTau.pZetas(
            muSysTag_, tauSysTag_, metSysTag_);

        double pZetaValue = pZetaInfo.first + visPZetaFactor_*pZetaInfo.second;

        // apply pt cut
        if ((pZetaValue > pZetaDiffMin_ && pZetaValue < pZetaDiffMax_) ||
            ignoreCut(pZetaCutIndex_)) {
          passCutFilter(pZetaCutIndex_, ret, muTauRef);

          int chargeProduct = muon.charge()*tau.charge();
          assert(chargeProduct != 0);
          bool passesChargeCut = (isOS_) ? chargeProduct < 0 : chargeProduct > 0;

          if (passesChargeCut || ignoreCut(signCutIndex_)) {
            passCutFilter(signCutIndex_, ret, muTauRef);
          }
        }
      }
    }
  }
  return (bool)ret;
}

