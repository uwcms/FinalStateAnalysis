#ifndef PATFINALSTATESELECTOR_3LY6MT3N
#define PATFINALSTATESELECTOR_3LY6MT3N

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "FinalStateAnalysis/NtupleTools/interface/AnalysisCutHolderT.h"

#include "FinalStateAnalysis/Utilities/interface/StringObjectSorter.h"

#include <boost/ptr_container/ptr_vector.hpp>

// Forward declarations
class PATFinalState;
class TFileDirectory;
namespace ek {
  class CutFlow;
}

typedef std::vector<const PATFinalState*> PATFinalStatePtrs;

class PATFinalStateSelection : public Selector<PATFinalStatePtrs> {
  public:
    typedef AnalysisCutHolderT<PATFinalState> FinalStateCut;
    PATFinalStateSelection(const edm::ParameterSet& pset, TFileDirectory& fs);
    virtual ~PATFinalStateSelection();

    // Analyze the set of final states for this event and fill the analysis
    // histograms.  Returns true if passes all cuts.
    bool operator()(const PATFinalStatePtrs& input, double weight);

    // Return the bitset giving the cuts that passed for the last go-round
    const pat::strbitset& result() const { return bits_; }
    // Return the final states that passed for the last go-round
    const PATFinalStatePtrs& passingFinalStates() const { return passing_; }
    // Get the cut flow table
    const ek::CutFlow* cutFlow() const { return cutFlow_.get(); }

  private:
    bool operator()(const PATFinalStatePtrs&, pat::strbitset&) {
      throw cms::Exception("notimplemented");
    }
    boost::ptr_vector<FinalStateCut> cuts_;
    bool eventView_;
    PATFinalStatePtrs passing_; // The passing final states
    index_type topologyCutId_;
    std::vector<pat::strbitset::index_type> cutIndices_; // for fast lookup

    // What to do with the events that pass all selections
    std::auto_ptr<StringObjectSorter<PATFinalState> > finalSort_;
    std::auto_ptr<ek::HistoFolder<PATFinalState> > finalPlots_;
    std::auto_ptr<ek::HistoFolder<PATFinalStatePtrs> > finalPlotsEventView_;
    unsigned int take_;

    // Hold the cutflow for the final states that pass the various stages of
    // this selection.
    std::auto_ptr<ek::CutFlow> cutFlow_;
};

#endif /* end of include guard: PATFINALSTATESELECTOR_3LY6MT3N */
