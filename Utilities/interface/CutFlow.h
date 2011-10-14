#ifndef FinalStateAnalysis_Utilities_CutFlow_h
#define FinalStateAnalysis_Utilities_CutFlow_h

/*
 * Implements a wrapper around a TH1I which holds a cut flow.
 *
 * The cut flow is filled using the pat::strbitset objects produced by
 * Selector<T> modules.
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#include <iostream>
// We use the non-copyable base class to ensure the class cannot be copied, as
// this may cause two instances of the class to point to the same underlying
// TH1I.
#include <boost/utility.hpp>
#include <vector>
#include <string>

namespace pat {
  class strbitset;
}
class TFileDirectory;
class TH1F;

namespace ek {

class CutFlow : public boost::noncopyable {
  public:
    typedef pat::strbitset CutSet;
    // Constructors from a set of cuts.  The histogram will be built into
    // relevant directory with the given name
    CutFlow(const CutSet& cuts, const std::string& name, TFileDirectory& fs);
    CutFlow(const std::vector<const CutSet*>& cuts, const std::string& name,
        TFileDirectory& fs);
    // Constructor from an existing histogram
    CutFlow(const TH1F& histo);

    virtual ~CutFlow();

    // Filler
    void fill(const CutSet& cuts, double w=1.0);
    void fill(const std::vector<const CutSet*>& cuts, double w=1.0);

    const TH1F* cutFlow() const { return cutFlow_; }

    // Get information about the nth cut
    double passed(size_t n) const;
    double efficiency(size_t n) const;
    double cumulativeEff(size_t n) const;
    const char* name(size_t n) const;
    size_t nCuts() const;

    // Print cut flow to stdout
    void print(std::ostream& out) const;

  private:

    void initialize(const std::vector<std::string>& cutNames,
        const std::string& name, TFileDirectory& fs);

    void fillImpl(const CutSet& cuts, double w, size_t idx);

    bool mustCleanupHistogram_;
    TH1F* cutFlow_;
};

}

#endif
