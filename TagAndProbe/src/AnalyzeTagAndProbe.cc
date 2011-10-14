#include "FinalStateAnalysis/TagAndProbe/interface/AnalyzeTagAndProbe.h"
#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematics.h"
#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematicsFwd.h"
#include "FinalStateAnalysis/Utilities/interface/CutFlow.h"
#include "FWCore/Common/interface/LuminosityBlockBase.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"

AnalyzeTagAndProbe::AnalyzeTagAndProbe(const edm::ParameterSet& pset,
    TFileDirectory& fs) {
  muTauPairs_ = pset.getParameter<edm::InputTag>("muTauPairs");
  edm::InputTag zMuMuSrc = pset.getParameter<edm::InputTag>("zMuMuSrc");
  std::vector<edm::InputTag> weightSrcs =
    pset.getParameter<std::vector<edm::InputTag> >("weightSrcs");
  // Build all our regions
  regions_ = pset.getParameterSet("regions");
  std::vector<std::string> names = regions_.getParameterNames();
  for (size_t i = 0; i < names.size(); ++i) {
    edm::ParameterSet regionPSet = regions_.getParameterSet(names[i]);
    regionPSet.addParameter<edm::InputTag>("muTauPairs", muTauPairs_);
    regionPSet.addParameter<edm::InputTag>("zMuMuSrc", zMuMuSrc);
    regionPSet.addParameter<std::vector<edm::InputTag> >(
        "weightSrcs", weightSrcs);
    regionPSet.addParameter<std::string>("name", names[i]);
    TFileDirectory subdir = fs.mkdir(names[i]);
    boost::shared_ptr<AnalyzeTagAndProbeRegion> analyzer(
        new AnalyzeTagAndProbeRegion(regionPSet, subdir));
    analyzers_.push_back(analyzer);
  }

  skimCounter_ = pset.getParameter<edm::InputTag>("skimCounter");
  lumiProducer_ = pset.exists("lumiProducer") ?
    pset.getParameter<edm::InputTag>("lumiProducer") :
    edm::InputTag("lumiProducer");

  // Initialize our counter histograms
  eventCounter_ = fs.make<TH1F>("eventCount", "Events Processed",
      1, -0.5, 0.5);
  skimEventCounter_ = fs.make<TH1F>("skimEventCount", "Skim Events Processed",
      1, -0.5, 0.5);
  integratedLumi_ = fs.make<TH1F>("integratedLumi", "Integrated Luminosity",
      1, -0.5, 0.5);

}

void AnalyzeTagAndProbe::beginLuminosityBlock(
    const edm::LuminosityBlockBase& ls) {
  /*
  edm::Handle<edm::MergeableCounter> skimmedEvents;
  ls.getByLabel(skimCounter_, skimmedEvents);
  skimEventCounter_->Fill(0.0, skimmedEvents->value);
  */

  // Get int. lumi
  edm::Handle<LumiSummary> lumiSummary;
  ls.getByLabel(lumiProducer_, lumiSummary);
  if (lumiSummary.isValid()) {
    integratedLumi_->Fill(0.0, lumiSummary->intgRecLumi());
  }
}

void AnalyzeTagAndProbe::analyze(const edm::EventBase& evt) {

  // Count this event
  eventCounter_->Fill(0.0);

  for (size_t i = 0; i < analyzers_.size(); ++i) {
    analyzers_[i]->analyze(evt);
  }
}

void AnalyzeTagAndProbe::endJob() {
  for (size_t i = 0; i < analyzers_.size(); ++i) {
    analyzers_[i]->endJob();
  }
}
