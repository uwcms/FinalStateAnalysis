#include "FinalStateAnalysis/DataAlgos/interface/CollectionFilter.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

// Function cache
namespace {

typedef StringCutObjectSelector<reco::Candidate, true> CandFunc;
typedef std::map<std::string, CandFunc> CandFuncCache;
static CandFuncCache functions_;

const CandFunc& getFunction(const std::string& function) {
  CandFuncCache::iterator findFunc = functions_.find(function);
  // Build it if we haven't made it
  if (findFunc == functions_.end()) {
    functions_.insert(std::make_pair(function, CandFunc(function)));
    findFunc = functions_.find(function);
  }
  return findFunc->second;
}

}

// Get objects at least [minDeltaR] away from hardScatter objects
std::vector<const reco::Candidate*> getVetoObjects(
    const std::vector<const reco::Candidate*>& hardScatter,
    const std::vector<const reco::Candidate*>& vetoCollection,
    double minDeltaR,
    const std::string& filter) {
  std::vector<const reco::Candidate*> output;

  const CandFunc& filterFunc = getFunction(filter);

  for (size_t i = 0; i < vetoCollection.size(); ++i) {
    const reco::Candidate* ptr = vetoCollection[i];
    bool awayFromEverything = true;
    for (size_t j = 0; j < hardScatter.size(); ++j) {
      double deltaR = reco::deltaR(ptr->p4(), hardScatter[j]->p4());
      if (deltaR < minDeltaR) {
        awayFromEverything = false;
        break;
      }
    }
    if (awayFromEverything && (filterFunc)(*ptr)) {
      output.push_back(ptr);
    }
  }
  return output;
}

std::vector<const reco::Candidate*> getVetoOSObjects(
    const std::vector<const reco::Candidate*>& hardScatter,
    const std::vector<const reco::Candidate*>& vetoCollection,
    double minDeltaR,
    const std::string& filter) {
  std::vector<const reco::Candidate*> output;

  const CandFunc& filterFunc = getFunction(filter);

  for (size_t i = 0; i < vetoCollection.size(); ++i) {
    const reco::Candidate* ptr = vetoCollection[i];
    bool awayFromEverything = true;
    for (size_t j = 0; j < 1; ++j) {
      double deltaR = reco::deltaR(ptr->p4(), hardScatter[j]->p4());
      if (deltaR < minDeltaR) {
        awayFromEverything = false;
        break;
      }
    }
    if (awayFromEverything && (filterFunc)(*ptr) && ptr->charge()*hardScatter[0]->charge()<0) {
      output.push_back(ptr);
    }
  }
  return output;
}


// Get objects within [minDeltaR] from [object] passing [filter]
std::vector<const reco::Candidate*> getOverlapObjects(
    const reco::Candidate& candidate,
    const std::vector<const reco::Candidate*>& overlapCollection,
    double minDeltaR,
    const std::string& filter) {
  std::vector<const reco::Candidate*> output;

  const CandFunc& filterFunc = getFunction(filter);

  for (size_t i = 0; i < overlapCollection.size(); ++i) {
    const reco::Candidate* ptr = overlapCollection[i];
    double deltaR = reco::deltaR(ptr->p4(), candidate.p4());
    if (deltaR < minDeltaR) {
      if ((filterFunc)(*ptr)) {
        output.push_back(ptr);
      }
    }
  }
  return output;
}


// Get objects passing filter
std::vector<const reco::Candidate*> getObjectsPassingFilter(
    const std::vector<const reco::Candidate*>& collection,
    const std::string& filter) {
  std::vector<const reco::Candidate*> output;

  const CandFunc& filterFunc = getFunction(filter);

  for (size_t i = 0; i < collection.size(); ++i) {
    const reco::Candidate* ptr = collection[i];
    if ((filterFunc)(*ptr)) {
      output.push_back(ptr);
    }
  }
  return output;
}


