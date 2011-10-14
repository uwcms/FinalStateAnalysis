#ifndef FinalStateAnalysis_TagAndProbe_AnalyzeTagAndProbeRegion_h
#define FinalStateAnalysis_TagAndProbe_AnalyzeTagAndProbeRegion_h

#include "FinalStateAnalysis/TagAndProbe/interface/TagAndProbeMuonSelections.h"
#include "FinalStateAnalysis/TagAndProbe/interface/TagAndProbeTauSelections.h"
#include "FinalStateAnalysis/TagAndProbe/interface/TagAndProbeTopoSelections.h"
#include <memory>
#include "FinalStateAnalysis/Utilities/interface/CutFlow.h"
#include "FinalStateAnalysis/Utilities/interface/HistoFolder.h"

namespace pat {
  class strbitset;
}

class AnalyzeTagAndProbeRegion {
  public:
    AnalyzeTagAndProbeRegion(const edm::ParameterSet& pset, TFileDirectory& fs);
    virtual ~AnalyzeTagAndProbeRegion(){};

    void beginJob() {}
    void endJob();
    void analyze(const edm::EventBase& evt);

  private:

    edm::InputTag muTauPairs_;
    edm::InputTag zMuMuSrc_;
    std::vector<edm::InputTag> weights_;
    std::string name_;

    TagAndProbeMuonSelector muonSelector_;
    TagAndProbeTauSelector tauSelector_;
    TagAndProbeTopoSelector topoSelector_;

    pat::strbitset dimuonVetoFlow_;
    pat::strbitset::index_type dimuonVetoIndex_;
    pat::strbitset muonCutFlow_;
    pat::strbitset tauCutFlow_;
    pat::strbitset topoCutFlow_;
    std::vector<const pat::strbitset*> cutFlows_;

    std::auto_ptr<ek::CutFlow> cutFlow_;

    ek::HistoFolder<PATMuTauSystematics> folder_;
};

#endif
