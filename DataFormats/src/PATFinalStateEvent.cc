#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/SmartTrigger.h"

#include "FWCore/Utilities/interface/RegexMatch.h"
#include "DataFormats/Math/interface/deltaR.h"
#include <boost/regex.hpp>

namespace {
  int matchedToAnObject(const pat::TriggerObjectRefVector& trgObjects,
      const reco::Candidate& cand, double maxDeltaR) {
    bool matched = false;
    for (size_t i = 0; i < trgObjects.size(); ++i) {
      if (reco::deltaR(cand, *trgObjects.at(i)) < maxDeltaR) {
        matched = true;
        break;
      }
    }
    if (matched)
      return 1;
    else return 0;
  }
}

PATFinalStateEvent::PATFinalStateEvent() {}

PATFinalStateEvent::PATFinalStateEvent(
    double rho,
    const edm::Ptr<reco::Vertex>& pv,
    const edm::PtrVector<reco::Vertex>& recoVertices,
    const edm::Ptr<pat::MET>& met,
    const pat::TriggerEvent& triggerEvent,
    const std::vector<PileupSummaryInfo>& puInfo,
    const edm::EventID& evtId) {
  rho_ = rho;
  pv_ = pv;
  met_ = met;
  recoVertices_ = recoVertices;
  triggerEvent_ = triggerEvent;
  puInfo_ = puInfo;
  evtID_ = evtId;
}

const edm::Ptr<reco::Vertex>& PATFinalStateEvent::pv() const { return pv_; }

const edm::PtrVector<reco::Vertex>& PATFinalStateEvent::recoVertices() const {
  return recoVertices_; }

const std::vector<PileupSummaryInfo>& PATFinalStateEvent::puInfo() const {
  return puInfo_;
}

double PATFinalStateEvent::rho() const { return rho_; }

const pat::TriggerEvent& PATFinalStateEvent::trig() const {
  return triggerEvent_; }

const edm::Ptr<pat::MET>& PATFinalStateEvent::met() const {
  return met_;
}

const edm::EventID& PATFinalStateEvent::id() const {
  return evtID_;
}

// Superseded by the smart trigger
std::vector<const pat::TriggerPath*> PATFinalStateEvent::matchingTriggerPaths(
    const std::string& pattern, bool ez) const {
  std::vector<const pat::TriggerPath*> output;
  boost::regex matcher(ez ? edm::glob2reg(pattern) : pattern);
  const pat::TriggerPathCollection* paths = trig().paths();
  for (size_t i = 0; i < paths->size(); ++i) {
    //std::cout << " path: " << paths->at(i).name() << " " << pattern;
    if (boost::regex_match(paths->at(i).name(), matcher)) {
      output.push_back(&paths->at(i));
      //std::cout << " match!";
    }
    //std::cout << std::endl;
  }
  return output;
}

std::vector<const pat::TriggerFilter*>
PATFinalStateEvent::matchingTriggerFilters(const std::string& pattern,
    bool ez) const {
  std::vector<const pat::TriggerFilter*> output;
  boost::regex matcher(ez ? edm::glob2reg(pattern) : pattern);
  const pat::TriggerFilterCollection* filters = trig().filters();
  for (size_t i = 0; i < filters->size(); ++i) {
    if (boost::regex_match(filters->at(i).label(), matcher))
      output.push_back(&filters->at(i));
  }
  return output;
}

int PATFinalStateEvent::hltResult(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig());
  return result.passed;
}

int PATFinalStateEvent::hltPrescale(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig());
  return result.prescale;
}

int PATFinalStateEvent::hltGroup(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig());
  return result.group;
}

int PATFinalStateEvent::matchedToFilter(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  std::vector<const pat::TriggerFilter*> filters =
    matchingTriggerFilters(pattern);
  if (!filters.size())
    return -1;
  return matchedToAnObject(
      triggerEvent_.filterObjects(filters[0]->label()), cand, maxDeltaR);
}

int PATFinalStateEvent::matchedToPath(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  SmartTriggerResult result = smartTrigger(pattern, trig());
  // Loop over all the paths that fired and see if any matched this object.
  if (!result.paths.size())
    return -1;
  int result = 0;
  for (size_t i = 0; i < result.paths.size(); ++i) {
    bool matched = matchedToAnObject(
      triggerEvent_.pathObjects(result.paths[i]->name()), cand, maxDeltaR);
    if (matched)
      result += 1;
  }
  return matched;
}

float PATFinalStateEvent::weight(const std::string& name) const {
  typedef std::map<std::string, float> WeightMap;
  WeightMap::const_iterator findit = weights_.find(name);
  if (findit != weights_.end())
    return findit->second;
  else
    return -999;
}
void PATFinalStateEvent::addWeight(const std::string& name, float weight) {
  weights_[name] = weight;
}

int PATFinalStateEvent::flag(const std::string& name) const {
  typedef std::map<std::string, int> FlagMap;
  FlagMap::const_iterator findit = flags_.find(name);
  if (findit != flags_.end())
    return findit->second;
  else
    return -999;
}
void PATFinalStateEvent::addFlag(const std::string& name, int flag) {
  flags_[name] = flag;
}
