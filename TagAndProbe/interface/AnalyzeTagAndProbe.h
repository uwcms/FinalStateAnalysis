#ifndef FinalStateAnalysis_TagAndProbe_AnalyzeTagAndProbe_h
#define FinalStateAnalysis_TagAndProbe_AnalyzeTagAndProbe_h

#include "FinalStateAnalysis/TagAndProbe/interface/AnalyzeTagAndProbeRegion.h"
#include <vector>

namespace edm {
  class LuminosityBlockBase;
}

class AnalyzeTagAndProbe {
  public:
    AnalyzeTagAndProbe(const edm::ParameterSet& pset, TFileDirectory& fs);

    virtual ~AnalyzeTagAndProbe(){};
    void beginJob() {}
    void endJob();
    void analyze(const edm::EventBase& evt);
    void beginLuminosityBlock(const edm::LuminosityBlockBase& ls);

  private:
    edm::InputTag muTauPairs_;
    edm::ParameterSet regions_;
    std::vector<boost::shared_ptr<AnalyzeTagAndProbeRegion> > analyzers_;

    // For counting events
    TH1* eventCounter_;
    // For keeping track of the skimming
    edm::InputTag skimCounter_;
    TH1* skimEventCounter_;
    edm::InputTag lumiProducer_;
    TH1* integratedLumi_;
};


#endif /* end of include guard: FinalStateAnalysis_TagAndProbe_AnalyzeTagAndProbe_h */
