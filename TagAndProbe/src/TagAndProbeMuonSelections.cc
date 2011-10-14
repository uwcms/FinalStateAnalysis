#include "FinalStateAnalysis/TagAndProbe/interface/TagAndProbeMuonSelections.h"

TagAndProbeMuonSelector::TagAndProbeMuonSelector(const edm::ParameterSet& pset):
  TagAndProbeBaseSelector(pset),
  isoCut_(pset.getParameter<std::string>("isoCut")) {
  // register cuts
  systematicsTag_ = pset.getParameter<std::string>("sysTag");
  muonPt_ = pset.getParameter<double>("muonPt");
  muonEta_ = pset.getParameter<double>("muonEta");
  maxDXY_ = pset.getParameter<double>("maxDXY");

  push_back("Muon Pt", muonPt_);
  push_back("Muon Eta", muonEta_);
  push_back("Muon Global");
  push_back("Muon InTrk");
  push_back("Muon TIP", maxDXY_);
  push_back("Muon ID");
  push_back("Muon Iso");

  muonPtIndex_ = index_type(&bits_, "Muon Pt");
  muonEtaIndex_ = index_type(&bits_, "Muon Eta");
  muonGlobalIndex_ = index_type(&bits_, "Muon Global");
  muonInTrkIndex_ = index_type(&bits_, "Muon InTrk");
  muonTIP_ = index_type(&bits_, "Muon TIP");
  muonID_ = index_type(&bits_, "Muon ID");
  muonIso_ = index_type(&bits_, "Muon Iso");

  // Turn on all cuts
  bits_.set(true);

  loadIgnored(pset);
}


bool TagAndProbeMuonSelector::operator()(const PATMuTauSystematicsPtrs& input,
    pat::strbitset& ret) {
  clear();
  ret.set(false);
  for (size_t i = 0; i < input.size(); ++i) {
    // Load all the stuff
    const PATMuTauSystematics* muTauRef = input.at(i);
    const PATMuTauSystematics& muTau = *muTauRef;
    const pat::Muon& muon = *muTau.daughter1();
    const reco::Candidate& sysCand = *muon.userCand(systematicsTag_);

    // apply pt cut
    if (sysCand.pt() > muonPt_ || ignoreCut(muonPtIndex_)) {
      passCutFilter(muonPtIndex_, ret, muTauRef);
      if (std::abs(sysCand.eta()) < muonEta_ || ignoreCut(muonEtaIndex_)) {
        passCutFilter(muonEtaIndex_, ret, muTauRef);
        if (muon.isGlobalMuon() || ignoreCut(muonGlobalIndex_)) {
          passCutFilter(muonGlobalIndex_, ret, muTauRef);
          if (muon.innerTrack().isNonnull() || ignoreCut(muonInTrkIndex_)) {
            passCutFilter(muonInTrkIndex_, ret, muTauRef);
            if (muon.userFloat("vertexDXY") < maxDXY_ || ignoreCut(muonTIP_)) {
              passCutFilter(muonTIP_, ret, muTauRef);
              if (muon.userInt("WWID") || ignoreCut(muonID_)) {
                passCutFilter(muonID_, ret, muTauRef);
                if (isoCut_(muon) || ignoreCut(muonIso_)) {
                  passCutFilter(muonIso_, ret, muTauRef);
                }
              }
            }
          }
        }
      }
    }
  }
  return (bool)ret;
}

