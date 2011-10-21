/*
 * PATFinalStateLS
 *
 * A smart container class that holds lumisection level information and has
 * functionality to process that information.
 *
 * */

#ifndef PATFINALSTATELS_HT41P3HF
#define PATFINALSTATELS_HT41P3HF

#include <string>
#include "FWCore/Common/interface/LuminosityBlockId.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"

class PATFinalStateLS {
  public:
    PATFinalStateLS();
    PATFinalStateLS(const LuminosityBlockID& id,
        const LumiSumary& lumiSummary);

    /// Get the ID with lumi & run number
    const LuminosityBlockID& id() const;

    /// Access to the lumi summary information
    const LumiSumary& lumiSummary() const;

    /// Get the inst. luminosity in this lumi
    double instantaneousLumi() const;

    /// Get the recorded int. luminosity in this lumi
    double intLumi() const;

    /// Get the recorded int. luminosity given the listed triggers
    double intLumi(const std::string& triggers) const;

  private:
    LuminosityBlockID id_;
    LumiSumary lumiSummary_;
};

#endif /* end of include guard: PATFINALSTATELS_HT41P3HF */
