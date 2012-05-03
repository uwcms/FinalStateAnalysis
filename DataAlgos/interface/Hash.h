/*
 * Tools for creating hashes of various FSA types
 */

#ifndef HASH_8A5URIOI
#define HASH_8A5URIOI

#include <vector>
#include "DataFormats/Candidate/interface/CandidateFwd.h"

namespace {
  class ProductID;
}

// Hash a ProductID
size_t hash_value(const edm::ProductID&);

// Hash a single reco::Candidate Ptr
size_t hash_value(const reco::CandidatePtr&);

// Get a hash value for a set of reco::Candidate Ptrs.  The order matters.
size_t hash_value(const std::vector<reco::CandidatePtr>&);

// Get a hash value for a set of reco::Candidate Ptrs.  The has value is the
// same, regardless of the order.  The input collection is sorted in place.
size_t hashCandsByContent(std::vector<reco::CandidatePtr>&);

#endif /* end of include guard: HASH_8A5URIOI */
