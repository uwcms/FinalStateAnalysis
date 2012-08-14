#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataAlgos/interface/SmartTrigger.h"
#include "FinalStateAnalysis/DataAlgos/interface/PileupWeighting.h"
#include "FinalStateAnalysis/DataAlgos/interface/PileupWeighting3D.h"
#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"
#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"

#include "DataFormats/Math/interface/deltaR.h"

#define FSA_DATA_FORMAT_VERSION 3

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

// testing CTOR
PATFinalStateEvent::PATFinalStateEvent(
    const edm::Ptr<reco::Vertex>& pv,
    const edm::Ptr<pat::MET>& met):
  pv_(pv),
  met_(met) { }

PATFinalStateEvent::PATFinalStateEvent(
    double rho,
    const edm::Ptr<reco::Vertex>& pv,
    const edm::PtrVector<reco::Vertex>& recoVertices,
    const edm::Ptr<pat::MET>& met,
    const TMatrixD& metCovariance,
    const pat::TriggerEvent& triggerEvent,
    const std::vector<PileupSummaryInfo>& puInfo,
    const lhef::HEPEUP& hepeup,
    const reco::GenParticleRefProd& genParticles,
    const edm::EventID& evtId,
    const GenEventInfoProduct& genEventInfo,
    bool isRealData,
    const std::string& puScenario,
    const edm::RefProd<pat::ElectronCollection>& electronRefProd,
    const edm::RefProd<pat::MuonCollection>& muonRefProd,
    const edm::RefProd<pat::TauCollection>& tauRefProd,
    const edm::RefProd<pat::JetCollection>& jetRefProd,
    const reco::PFCandidateRefProd& pfRefProd,
    const reco::TrackRefProd& tracks,
    const reco::GsfTrackRefProd& gsfTracks
    ):
  rho_(rho),
  triggerEvent_(triggerEvent),
  pv_(pv),
  recoVertices_(recoVertices),
  met_(met),
  metCovariance_(metCovariance),
  puInfo_(puInfo),
  lhe_(hepeup),
  genParticles_(genParticles),
  evtID_(evtId),
  genEventInfoProduct_(genEventInfo),
  isRealData_(isRealData),
  puScenario_(puScenario),
  fsaDataFormatVersion_(FSA_DATA_FORMAT_VERSION),
  electronRefProd_(electronRefProd),
  muonRefProd_(muonRefProd),
  tauRefProd_(tauRefProd),
  jetRefProd_(jetRefProd),
  pfRefProd_(pfRefProd),
  tracks_(tracks),
  gsfTracks_(gsfTracks)
{ }

const edm::Ptr<reco::Vertex>& PATFinalStateEvent::pv() const { return pv_; }

const edm::PtrVector<reco::Vertex>& PATFinalStateEvent::recoVertices() const {
  return recoVertices_;
}

const std::vector<PileupSummaryInfo>& PATFinalStateEvent::puInfo() const {
  return puInfo_;
}

const lhef::HEPEUP& PATFinalStateEvent::lesHouches() const {
  return lhe_;
}

const GenEventInfoProduct& PATFinalStateEvent::genEventInfo() const {
  return genEventInfoProduct_;
}

double PATFinalStateEvent::rho() const { return rho_; }

const pat::TriggerEvent& PATFinalStateEvent::trig() const {
  return triggerEvent_; }

const edm::Ptr<pat::MET>& PATFinalStateEvent::met() const {
  return met_;
}

const TMatrixD& PATFinalStateEvent::metCovariance() const {
  return metCovariance_;
}

double PATFinalStateEvent::metSignificance() const {
  return fshelpers::xySignficance(met_->momentum(), metCovariance_);
}

const edm::EventID& PATFinalStateEvent::evtId() const {
  return evtID_;
}

// Superseded by the smart trigger
int PATFinalStateEvent::hltResult(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  return result.passed;
}

int PATFinalStateEvent::hltPrescale(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  return result.prescale;
}

int PATFinalStateEvent::hltGroup(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  return result.group;
}

int PATFinalStateEvent::matchedToFilter(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  std::vector<const pat::TriggerFilter*> filters =
    matchingTriggerFilters(trig(), pattern);
  if (!filters.size())
    return -1;
  return matchedToAnObject(
      triggerEvent_.filterObjects(filters[0]->label()), cand, maxDeltaR);
}

int PATFinalStateEvent::matchedToPath(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  // Loop over all the paths that fired and see if any matched this object.
  if (!result.paths.size())
    return -1;
  int matchCount = 0;
  for (size_t i = 0; i < result.paths.size(); ++i) {
    bool matched = matchedToAnObject(
      triggerEvent_.pathObjects(result.paths[i]), cand, maxDeltaR);
    if (matched)
      matchCount += 1;
  }
  return matchCount;
}

const std::string& PATFinalStateEvent::puTag() const {
  return puScenario_;
}

double PATFinalStateEvent::puWeight(const std::string& dataTag) const {
  if (isRealData_)
    return 1.;
  return this->puWeight(dataTag, puTag());
}

double PATFinalStateEvent::puWeight(const std::string& dataTag,
    const std::string& mcTag) const {
  if (isRealData_)
    return 1.;
  return getPileupWeight(dataTag, mcTag, puInfo_[1].getTrueNumInteractions());
}

double PATFinalStateEvent::puWeight3D(const std::string& dataTag) const {
  if (isRealData_)
    return 1.;
  return this->puWeight3D(dataTag, puTag());
}

double PATFinalStateEvent::puWeight3D(const std::string& dataTag,
    const std::string& mcTag) const {
  if (isRealData_)
    return 1.;
  return get3DPileupWeight(dataTag, mcTag, puInfo_);
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

const pat::ElectronCollection& PATFinalStateEvent::electrons() const {
  if (!electronRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The electron RefProd is null!" << std::endl;
  return *electronRefProd_;
}

const pat::MuonCollection& PATFinalStateEvent::muons() const {
  if (!muonRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The muon RefProd is null!" << std::endl;
  return *muonRefProd_;
}

const pat::TauCollection& PATFinalStateEvent::taus() const {
  if (!tauRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The tau RefProd is null!" << std::endl;
  return *tauRefProd_;
}

const pat::JetCollection& PATFinalStateEvent::jets() const {
  if (!jetRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The jet RefProd is null!" << std::endl;
  return *jetRefProd_;
}

const reco::PFCandidateCollection& PATFinalStateEvent::pflow() const {
  if (!pfRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The PFLOW RefProd is null!" << std::endl;
  return *pfRefProd_;
}
