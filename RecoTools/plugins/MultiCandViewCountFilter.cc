/*
 * MultiCandViewCountFilter
 *
 * Apply a multiplicity cut on the combination of one or more collections.
 *
 * Author: Evan K. Friis, UW Madison
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include <limits>

class MultiCandViewCountFilter : public edm::EDFilter {
  public:
    MultiCandViewCountFilter(const edm::ParameterSet& pset);
    virtual ~MultiCandViewCountFilter(){}
    bool filter(edm::Event& evt, const edm::EventSetup& es);
  private:
    typedef std::vector<edm::InputTag> VInputTag;
    VInputTag srcs_;
    unsigned int minCount_;
    unsigned int maxCount_;
};

MultiCandViewCountFilter::MultiCandViewCountFilter(const edm::ParameterSet& pset) {
  srcs_ = pset.getParameter<VInputTag>("srcs");
  minCount_ = pset.getParameter<unsigned int>("minCount");
  maxCount_ = pset.exists("maxCount") ?
    pset.getParameter<unsigned int>("maxCount") :
    std::numeric_limits<unsigned int>::max();
}

bool MultiCandViewCountFilter::filter(edm::Event& evt, const edm::EventSetup& es) {
  unsigned int count = 0;
  for (size_t i = 0; i < srcs_.size(); ++i) {
    edm::Handle<reco::CandidateView> cands;
    evt.getByLabel(srcs_[i], cands);
    count += cands->size();
    if (count > maxCount_)
      return false;
  }
  return count >= minCount_;
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MultiCandViewCountFilter);
