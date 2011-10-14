#include "FinalStateAnalysis/TagAndProbe/interface/TagAndProbeTauSelections.h"

TagAndProbeTauSelector::TagAndProbeTauSelector(
    const edm::ParameterSet& pset): TagAndProbeBaseSelector(pset),
  preselCut_(pset.getParameter<std::string>("preselCut")),
  antiMuonCut_(pset.getParameter<std::string>("antiMuonCut")),
  antiElectronCut_(pset.getParameter<std::string>("antiElectronCut")),
  discrimCut_(pset.getParameter<std::string>("discrimCut"))
{
  systematicsTag_ = pset.getParameter<std::string>("sysTag");
  minDRMuon_ = pset.getParameter<double>("minDRMuon");
  jetPt_ = pset.getParameter<double>("jetPt");
  jetEta_ = pset.getParameter<double>("jetEta");
  leadTrackPt_ = pset.getParameter<double>("leadTrackPt");

  push_back("XClean", minDRMuon_);
  push_back("Tau Pt", jetPt_);
  push_back("Tau Eta", jetEta_);
  push_back("Tau LeadTrk", leadTrackPt_);
  push_back("Tau Presel");
  push_back("Tau Anti-mu");
  push_back("Tau Anti-e");
  push_back("Tau ID");

  muonDRIndex_ = getIndex("XClean");
  jetPtIndex_ = getIndex("Tau Pt");
  jetEtaIndex_ = getIndex("Tau Eta");
  leadTrackPtIndex_ = getIndex("Tau LeadTrk");
  preselCutIndex_ = getIndex("Tau Presel");
  antiMuonCutIndex_ = getIndex("Tau Anti-mu");
  antiElectronCutIndex_ = getIndex("Tau Anti-e");
  discrimCutIndex_ = getIndex("Tau ID");

  // Turn on all cuts
  bits_.set(true);

  loadIgnored(pset);
}

bool TagAndProbeTauSelector::operator()(const PATMuTauSystematicsPtrs& input,
    pat::strbitset& ret) {
  clear();
  ret.set(false);
  for (size_t i = 0; i < input.size(); ++i) {
    // Load all the stuff
    const PATMuTauSystematics* muTauRef = input.at(i);
    const PATMuTauSystematics& muTau = *muTauRef;
    const pat::Tau& tau = *muTau.daughter2();
    const reco::Candidate& sysCand = *tau.userCand("jet_" + systematicsTag_);

    if (tau.userFloat("ps_drMuon") > minDRMuon_ || ignoreCut(muonDRIndex_)) {
      passCutFilter(muonDRIndex_, ret, muTauRef);
      if (sysCand.pt() > jetPt_ || ignoreCut(jetPtIndex_)) {
        passCutFilter(jetPtIndex_, ret, muTauRef);
        if (std::abs(sysCand.eta()) < jetEta_ || ignoreCut(jetEtaIndex_)) {
          passCutFilter(jetEtaIndex_, ret, muTauRef);
          if (tau.userFloat("ps_ldTrkPt") > leadTrackPt_ || ignoreCut(leadTrackPtIndex_)) {
            passCutFilter(leadTrackPtIndex_, ret, muTauRef);
            if (preselCut_(tau)  || ignoreCut(preselCutIndex_)) {
              passCutFilter(preselCutIndex_, ret, muTauRef);
              if (antiMuonCut_(tau) || ignoreCut(antiMuonCutIndex_)) {
                passCutFilter(antiMuonCutIndex_, ret, muTauRef);
                if (antiElectronCut_(tau) || ignoreCut(antiElectronCutIndex_)) {
                  passCutFilter(antiElectronCutIndex_, ret, muTauRef);
                  if (discrimCut_(tau) || ignoreCut(discrimCutIndex_)) {
                    passCutFilter(discrimCutIndex_, ret, muTauRef);
                  }
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
