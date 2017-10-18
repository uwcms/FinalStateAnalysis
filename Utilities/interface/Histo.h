#ifndef FinalStateAnalysis_Utilities_Histo_h
#define FinalStateAnalysis_Utilities_Histo_h

/*
 * Plugin abstract base class for creating histograms.
 *
 * Author: Evan K. Friis, UC Davis
 *
 */

#include <string>
#include "FWCore/ParameterSet/interface/ParameterSet.h"

// Forward declarations
namespace edm {
  class EventBase;
  class EventSetup;
}

namespace ek {

template<typename T>
class Histo {
  public:
    Histo(const edm::ParameterSet& pset, TFileDirectory& fs) {};

    void fill(const T& t, double weight=1.0,
        const edm::EventBase* evt = NULL,
        const edm::EventSetup* es = NULL) = 0;
};


// Interface to build Histo plugins.  This is just some type maggic wrapper to
// reduce huge typedef pain.
template<typename T>
class HistoFactory {
  public:

    HistoFactory(){};

    Histo<T>* create(const std::string& pluginName,
        const edm::ParameterSet& pset, TFileDirectory& fs) {
      return EDMFactory::get()->create(pluginName, pset, fs);
    }

  private:
    typedef edmplugin::PluginFactory<Histo<T>*(const edm::ParameterSet& pset,
        TFileDirectory& fs)> EDMFactory;
};

} // end ek namespace

#endif /* end of include guard: FinalStateAnalysis_Utilities_Histo_h */
