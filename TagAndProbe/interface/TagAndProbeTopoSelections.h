/*
 * =====================================================================================
 *
 *       Filename:  TagAndProbeTopoSelections.h
 *
 *    Description:  Topological selections used in Tau T&P analysis
 *
 *         Author:  Evan K. Friis
 *
 * =====================================================================================
 */

#ifndef TAGANDPROBETOPOSELECTIONS_5R9AEQDB
#define TAGANDPROBETOPOSELECTIONS_5R9AEQDB

#include "FinalStateAnalysis/TagAndProbe/interface/TagAndProbeBaseSelector.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

class TagAndProbeTopoSelector : public TagAndProbeBaseSelector {
  public:
    TagAndProbeTopoSelector(const edm::ParameterSet& pset);
    bool operator()(const PATMuTauSystematicsPtrs& input,
        pat::strbitset& ret);
    const index_type& finalCut() const { return signCutIndex_; }
  private:
    std::string muSysTag_;
    std::string tauSysTag_;
    std::string metSysTag_;

    double visPZetaFactor_;
    double pZetaDiffMin_;
    double pZetaDiffMax_;

    double deltaPhiMax_;

    StringCutObjectSelector<PATMuTauSystematics> topoCut_;

    bool isOS_;

    // Don't do a string lookup each time
    index_type deltaPhiIndex_;
    index_type topoCutIndex_;
    index_type pZetaCutIndex_;
    index_type signCutIndex_;
};



#endif /* end of include guard: TAGANDPROBETOPOSELECTIONS_5R9AEQDB */
