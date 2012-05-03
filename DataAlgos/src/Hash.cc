#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"
#include <boost/functional/hash.hpp>
#include <algorithm>

size_t hash_value(const edm::ProductID& id) {
  size_t seed = 0;
  boost::hash_combine(seed, id.processIndex());
  boost::hash_combine(seed, id.productIndex());
  return seed;
}

size_t hash_value(const reco::CandidatePtr& ptr) {
  size_t seed = 0;
  boost::hash_combine(seed, hash_value(ptr.refCore().id()));
  boost::hash_combine(seed, ptr.key());
  return seed;
}

size_t hash_value(const std::vector<reco::CandidatePtr>& ptrs) {
  size_t seed = 0;
  for (size_t i = 0; i < ptrs.size(); ++i) {
    boost::hash_combine(seed, hash_value(ptrs[i]));
  }
  return seed;
}

size_t hashCandsByContent(std::vector<reco::CandidatePtr>& ptrs) {
  // First sort them
  std::sort(ptrs.begin(), ptrs.end());
  // Now order is invariant
  return hash_value(ptrs);
}
