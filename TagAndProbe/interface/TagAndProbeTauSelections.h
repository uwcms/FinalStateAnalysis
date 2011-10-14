#ifndef TagAndProbeTauSelections
#define TagAndProbeTauSelections

#include "FinalStateAnalysis/TagAndProbe/interface/TagAndProbeBaseSelector.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

class TagAndProbeTauSelector : public TagAndProbeBaseSelector {
  public:
    TagAndProbeTauSelector(const edm::ParameterSet& pset);
    bool operator()(const PATMuTauSystematicsPtrs& input,
        pat::strbitset& ret);
    const index_type& finalCut() const { return discrimCutIndex_; }
  private:
    std::string systematicsTag_;
    double minDRMuon_;
    double jetPt_;
    double jetEta_;
    double leadTrackPt_;
    StringCutObjectSelector<pat::Tau> preselCut_;
    StringCutObjectSelector<pat::Tau> antiMuonCut_;
    StringCutObjectSelector<pat::Tau> antiElectronCut_;
    StringCutObjectSelector<pat::Tau> discrimCut_;

    // Don't do a string lookup each time
    index_type muonDRIndex_;
    index_type jetPtIndex_;
    index_type jetEtaIndex_;
    index_type leadTrackPtIndex_;
    index_type preselCutIndex_;
    index_type antiMuonCutIndex_;
    index_type antiElectronCutIndex_;
    index_type discrimCutIndex_;
};

#endif /* end of include guard: TagAndProbeTauSelections.h */
