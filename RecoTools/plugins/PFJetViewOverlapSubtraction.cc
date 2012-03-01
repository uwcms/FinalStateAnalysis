/*
 * PFJetViewOverlapSubtraction
 *
 * Takes two View of PFJets, and removes all those from the first collection
 * [src] that overlap (within some [minDeltaR]) with objects in the second
 * collection [subtractSrc]
 *
 * The output collection is a new PFJetCollection.
 *
 * Author: Evan K. Friis, UW Madison
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"

#include "DataFormats/Math/interface/deltaR.h"

class PFJetViewOverlapSubtraction : public edm::EDFilter {
  public:
    PFJetViewOverlapSubtraction(const edm::ParameterSet& pset);
    virtual ~PFJetViewOverlapSubtraction(){}
    bool filter(edm::Event& evt, const edm::EventSetup& es);
    private:
    edm::InputTag src_;
    edm::InputTag subtractSrc_;
    double minDeltaR_;
    bool filter_;
};

PFJetViewOverlapSubtraction::PFJetViewOverlapSubtraction(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  subtractSrc_ = pset.getParameter<edm::InputTag>("subtractSrc");
  minDeltaR_ = pset.getParameter<double>("minDeltaR");
  filter_ = pset.getParameter<bool>("filter");
  produces<reco::CandidateBaseRefVector>();
}

bool PFJetViewOverlapSubtraction::filter(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<edm::View<reco::PFJet> > candsToFilter;
  evt.getByLabel(src_, candsToFilter);

  edm::Handle<edm::View<reco::Candidate> > candsToSubtract;
  evt.getByLabel(subtractSrc_, candsToSubtract);

  std::auto_ptr<reco::PFJetCollection> output(
      new reco::PFJetCollection());

  const edm::PtrVector<reco::PFJet> &toFilter = candsToFilter->ptrVector();
  const reco::CandidateBaseRefVector &toSubtract = candsToSubtract->refVector();

  for (size_t i = 0; i < toFilter.size(); ++i) {
    edm::Ptr<reco::PFJet> baseRef = toFilter[i];
    bool passes = true;
    for (size_t j = 0; j < toSubtract.size(); ++j) {
      double deltaR = reco::deltaR(baseRef->p4(), toSubtract[j]->p4());
      if (deltaR < minDeltaR_) {
        passes = false;
        break;
      }
    }
    if (passes) {
      output->push_back(*baseRef);
    }
  }
  size_t outputSize = output->size();
  evt.put(output);
  return ( !filter_ || outputSize );
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PFJetViewOverlapSubtraction);
