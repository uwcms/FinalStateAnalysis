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
#include "DataFormats/Provenance/interface/LuminosityBlockID.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateLSFwd.h"

class PATFinalStateLS {
  public:
    PATFinalStateLS();
    PATFinalStateLS(const edm::LuminosityBlockID& id,
        double integratedLuminosity,
        double instantaneousLumi,
        const std::vector<LumiSummary::HLT>& hltInfos,
        const std::vector<LumiSummary::L1>& l1Infos);

    /// Get the ID with lumi & run number
    const edm::LuminosityBlockID& lsID() const;

    /// Get the inst. luminosity in this lumi
    double instantaneousLumi() const;

    /// Get the recorded int. luminosity in this lumi
    double intLumi() const;

    /// Get the recorded int. luminosity given the listed triggers
    double intLumi(const std::string& triggers) const;

  private:
    edm::LuminosityBlockID id_;
    double integratedLumi_;
    double instaneousLumi_;
    std::vector<LumiSummary::HLT> hltInfos_;
    std::vector<LumiSummary::L1> l1Infos_;
};

#endif /* end of include guard: PATFINALSTATELS_HT41P3HF */
