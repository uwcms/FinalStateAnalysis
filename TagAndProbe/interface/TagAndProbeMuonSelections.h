#ifndef TagAndProbeMuonSelections
#define TagAndProbeMuonSelections

#include "FinalStateAnalysis/TagAndProbe/interface/TagAndProbeBaseSelector.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

class TagAndProbeMuonSelector : public TagAndProbeBaseSelector {
  public:
    TagAndProbeMuonSelector(const edm::ParameterSet& pset);
    bool operator()(const PATMuTauSystematicsPtrs& input,
        pat::strbitset& ret);
    const index_type& finalCut() const { return muonIso_; }
  private:
    std::string systematicsTag_;
    double muonPt_;
    double muonEta_;
    std::string isoTag_;
    StringCutObjectSelector<pat::Muon> isoCut_;
    double maxDXY_;
    bool invertIsolation_;

    // Don't do a string lookup each time
    index_type muonPtIndex_;
    index_type muonEtaIndex_;
    index_type muonGlobalIndex_;
    index_type muonInTrkIndex_;
    index_type muonTIP_;
    index_type muonID_;
    index_type muonIso_;
};

#endif /* end of include guard: TagAndProbeMuonSelections.h */
