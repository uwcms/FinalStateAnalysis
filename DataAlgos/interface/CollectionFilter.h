/*
 * =====================================================================================
 *
 *       Filename:  CollectionFilter.h
 *
 *    Description:  Filters collections of objects for vetos and cleaning.
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#ifndef COLLECTIONFILTER_EKK6HP4C
#define COLLECTIONFILTER_EKK6HP4C

#include <vector>
#include <string>

namespace reco {
  class Candidate;
}

// Convert collection to vector of reco::Candidate ptrs
template<class C>
std::vector<const reco::Candidate*> ptrizeCollection(const C& collection) {
  std::vector<const reco::Candidate*> output;
  output.reserve(collection.size());
  for (size_t i = 0; i < collection.size(); ++i) {
    output.push_back(&collection[i]);
  }
  return output;
}

// Get objects at least [minDeltaR] away from [hardScatter] objects
// that pass [filter]
std::vector<const reco::Candidate*> getVetoObjects(
    const std::vector<const reco::Candidate*>& hardScatter,
    const std::vector<const reco::Candidate*>& vetoCollection,
    double minDeltaR,
    const std::string& filter
);

std::vector<const reco::Candidate*> getVetoOSObjects(
    const std::vector<const reco::Candidate*>& hardScatter,
    const std::vector<const reco::Candidate*>& vetoCollection,
    double minDeltaR,
    const std::string& filter
);

// Get objects passing [filter] within [minDeltaR] of [candidate]
// that pass [filter]
std::vector<const reco::Candidate*> getOverlapObjects(
    const reco::Candidate& candidate,
    const std::vector<const reco::Candidate*>& overlapCollection,
    double minDeltaR,
    const std::string& filter
);

// Get objects passing [filter]
std::vector<const reco::Candidate*> getObjectsPassingFilter(
    const std::vector<const reco::Candidate*>& overlapCollection,
    const std::string& filter
);


#endif /* end of include guard: COLLECTIONFILTER_EKK6HP4C */
