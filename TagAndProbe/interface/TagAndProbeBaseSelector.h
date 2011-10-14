#ifndef TagAndProbeMuonBaseSelector
#define TagAndProbeMuonBaseSelector
/*
 * Class which implements a multi-level Muon selector
 *
 */

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematics.h"
#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematicsFwd.h"

#include <map>
#include <string>
#include <sstream>

typedef std::vector<const PATMuTauSystematics*> PATMuTauSystematicsPtrs;

class TagAndProbeBaseSelector : public Selector<PATMuTauSystematicsPtrs> {
  public:
    typedef std::map<index_type, PATMuTauSystematicsPtrs>
      SelectedPairsCutMap;

    TagAndProbeBaseSelector(const edm::ParameterSet& pset) {}

    // Parse the PSet to figure out if we wanto to ignore any cuts
    void loadIgnored(const edm::ParameterSet& pset) {
      if (pset.exists("cutsToIgnore"))
        setIgnoredCuts(
            pset.getParameter<std::vector<std::string> >("cutsToIgnore"));
    }

    index_type getIndex(const std::string& cut) const {
      return index_type(&bits_, cut);
    }

    // Return the final cut in this sequence
    virtual const index_type& finalCut() const = 0;

    const PATMuTauSystematicsPtrs& selectedObjects(
        const index_type& index) const {

      const PATMuTauSystematicsPtrs& result = selectedObjectsByCut_[index];

      return result;
    }

    const PATMuTauSystematicsPtrs& selectedObjects(
        const std::string& cut) const {
      return selectedObjects(getIndex(cut));
    }

    // Customized version of pass cut which additionally adds the passing
    // object to the cutflow collections
    void passCutFilter(const index_type& index, pat::strbitset& ret,
        const PATMuTauSystematics* object) {
      selectedObjectsByCut_[index].push_back(object);
      this->passCut(ret, index);
    }

  protected:
    void clear() {
      for (SelectedPairsCutMap::iterator iCut = selectedObjectsByCut_.begin();
          iCut != selectedObjectsByCut_.end(); ++iCut) {
        iCut->second.clear();
      }
    }
    mutable SelectedPairsCutMap selectedObjectsByCut_;
};

#endif
