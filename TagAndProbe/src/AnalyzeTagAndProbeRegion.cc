#include "FinalStateAnalysis/TagAndProbe/interface/AnalyzeTagAndProbeRegion.h"
#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematics.h"
#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematicsFwd.h"
#include "FinalStateAnalysis/Utilities/interface/CutFlow.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidateFwd.h"

AnalyzeTagAndProbeRegion::AnalyzeTagAndProbeRegion(const edm::ParameterSet& pset,
    TFileDirectory& fs):
  muonSelector_(pset.getParameterSet("muonSelection")),
  tauSelector_(pset.getParameterSet("tauSelection")),
  topoSelector_(pset.getParameterSet("topoSelection")),
  folder_(pset.getParameterSet("folders"), fs)
{
  muTauPairs_ = pset.getParameter<edm::InputTag>("muTauPairs");
  name_ = pset.getParameter<std::string>("name");

  zMuMuSrc_ = pset.getParameter<edm::InputTag>("zMuMuSrc");

  weights_ = pset.getParameter<std::vector<edm::InputTag> >("weightSrcs");
  /*code*/
  // Make a fake cutset for the dimuon veto
  dimuonVetoFlow_.push_back("Dimuon Veto");
  dimuonVetoIndex_ = pat::strbitset::index_type(
      &dimuonVetoFlow_, "Dimuon Veto");

  // initialize the cut flow table
  muonCutFlow_ = muonSelector_.getBitTemplate();
  tauCutFlow_ = tauSelector_.getBitTemplate();
  topoCutFlow_ = topoSelector_.getBitTemplate();

  // cutFlows_ holds pointers to the different type of cuts
  cutFlows_.push_back(&muonCutFlow_);
  cutFlows_.push_back(&dimuonVetoFlow_);
  cutFlows_.push_back(&tauCutFlow_);
  cutFlows_.push_back(&topoCutFlow_);

  // Initialize the cutflow table
  cutFlow_.reset(new ek::CutFlow(cutFlows_, "cutFlow", fs));
}

void AnalyzeTagAndProbeRegion::analyze(const edm::EventBase& evt) {

  // Get the event weight
  double eventWeight = 1.0;
  for (size_t i = 0; i < weights_.size(); ++i) {
    edm::Handle<double> weightH;
    evt.getByLabel(weights_[i], weightH);
    eventWeight *= *weightH;
  }

  edm::Handle<PATMuTauSystematicsCollection> pairs;
  evt.getByLabel(muTauPairs_, pairs);

  edm::Handle<reco::CompositeCandidateCollection> dimuons;
  evt.getByLabel(zMuMuSrc_, dimuons);

  // convert to ref vector
  std::vector<const PATMuTauSystematics*> pairRefs;
  for (size_t i = 0; i < pairs->size(); ++i) {
    const PATMuTauSystematics& ref = pairs->at(i);
    pairRefs.push_back(&ref);
  }

  muonSelector_(pairRefs, muonCutFlow_);
  const std::vector<const PATMuTauSystematics*>& passingMuonRefs =
    muonSelector_.selectedObjects(muonSelector_.finalCut());

  dimuonVetoFlow_.set(false);
  if (dimuons->size() == 0 && passingMuonRefs.size()) {
    dimuonVetoFlow_[dimuonVetoIndex_] = true;
    tauSelector_(passingMuonRefs, tauCutFlow_);
  } else {
    // Pass the tau selector an empty vector
    tauSelector_(std::vector<const PATMuTauSystematics*>(), tauCutFlow_);
  }

  const std::vector<const PATMuTauSystematics*>& passingTauRefs =
    tauSelector_.selectedObjects(tauSelector_.finalCut());

  topoSelector_(passingTauRefs, topoCutFlow_);
  const std::vector<const PATMuTauSystematics*>& finalSelectedRefs =
    topoSelector_.selectedObjects(topoSelector_.finalCut());

  cutFlow_->fill(cutFlows_, eventWeight);

  // Find the pair w/ the highest pt tau;
  double highestPairTauPt = -1;
  const PATMuTauSystematics* chosenPair = NULL;

  for (size_t i = 0; i < finalSelectedRefs.size(); ++i) {
    if (finalSelectedRefs[i]->daughter2()->pt() > highestPairTauPt) {
      chosenPair = finalSelectedRefs[i];
      highestPairTauPt = finalSelectedRefs[i]->pt();
    }
  }

  if (chosenPair)
    folder_.fill(*chosenPair, eventWeight);
}

void AnalyzeTagAndProbeRegion::endJob() {
  std::cout << "Cutflow report for region: " << name_ << std::endl;
  cutFlow_->print(std::cout);
  std::cout << std::endl;
}
