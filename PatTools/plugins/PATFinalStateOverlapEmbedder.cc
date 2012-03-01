/*
 * Embed an extra collection into a PAT final state.  The objects in the
 * embedded collection using the overlaps(..) functionality.
 *
 * The input collection is filtered w/ an optional string cut, and a minimum
 * deltaR to any candidate.
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include <string>
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "DataFormats/Math/interface/deltaR.h"

class PATFinalStateOverlapEmbedder : public edm::EDProducer {
  public:
    PATFinalStateOverlapEmbedder(const edm::ParameterSet& pset);
    virtual ~PATFinalStateOverlapEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag toEmbedSrc_;
    std::string name_;
    StringCutObjectSelector<reco::Candidate> cut_;
    double minDeltaR_;
    double maxDeltaR_;

};

PATFinalStateOverlapEmbedder::PATFinalStateOverlapEmbedder(
    const edm::ParameterSet& pset):cut_(
      pset.getParameter<std::string>("cut"), true){
  src_ = pset.getParameter<edm::InputTag>("src");
  toEmbedSrc_ = pset.getParameter<edm::InputTag>("toEmbedSrc");
  name_ = pset.getParameter<std::string>("name");
  minDeltaR_ = pset.getParameter<double>("minDeltaR");
  maxDeltaR_ = pset.getParameter<double>("maxDeltaR");
  produces<PATFinalStateCollection>();
}
void PATFinalStateOverlapEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStatesH;
  evt.getByLabel(src_, finalStatesH);

  edm::Handle<edm::View<reco::Candidate> > toEmbedH;
  evt.getByLabel(toEmbedSrc_, toEmbedH);

  for (size_t i = 0; i < finalStatesH->size(); ++i) {
    PATFinalState* embedInto = finalStatesH->ptrAt(i)->clone();
    reco::CandidatePtrVector overlaps;
    for (size_t j = 0; j < toEmbedH->size(); ++j) {
      const reco::CandidatePtr toTest = toEmbedH->ptrAt(j);
      if (!cut_(*toTest))
        continue;
      bool passes = true;
      for (size_t i = 0; i < embedInto->numberOfDaughters(); ++i) {
        const reco::Candidate* dau = embedInto->daughter(i);
        double deltaR = reco::deltaR(dau->p4(), toTest->p4());
        if (deltaR < minDeltaR_ || deltaR > maxDeltaR_) {
          passes = false;
          break;
        }
      }
      if (passes)
        overlaps.push_back(toTest);
    }
    embedInto->setOverlaps(name_, overlaps);
    output->push_back(embedInto); // takes ownership
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateOverlapEmbedder);
