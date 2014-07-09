#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventMini.h"
#include "FinalStateAnalysis/DataAlgos/interface/SmartTrigger.h"
#include "FinalStateAnalysis/DataAlgos/interface/PileupWeighting.h"
#include "FinalStateAnalysis/DataAlgos/interface/PileupWeighting3D.h"
#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"
#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"

#include "DataFormats/Math/interface/deltaR.h"

#define FSA_DATA_FORMAT_VERSION 3

namespace {
  int matchedToAnObject(const std::vector<pat::TriggerObjectStandAlone> trgObjects,
      const reco::Candidate& cand, double maxDeltaR) {
    bool matched = false;
    for (size_t i = 0; i < trgObjects.size(); ++i) {
      if (reco::deltaR(cand, trgObjects.at(i)) < maxDeltaR) {
        matched = true;
        break;
      }
    }
    if (matched)
      return 1;
    else return 0;
  }
}

PATFinalStateEventMini::PATFinalStateEventMini() {}

// testing CTOR
PATFinalStateEventMini::PATFinalStateEventMini(
    const edm::Ptr<reco::Vertex>& pv,
    const edm::Ptr<pat::MET>& met):
  pv_(pv),
  met_(met) { }

PATFinalStateEventMini::PATFinalStateEventMini(
    double rho,
    const edm::Ptr<reco::Vertex>& pv,
    const edm::PtrVector<reco::Vertex>& recoVertices,
    const edm::Ptr<pat::MET>& met,
    const TMatrixD& metCovariance,
    const edm::RefProd<std::vector<pat::TriggerObjectStandAlone>>& triggerObjects,
    const pat::PackedTriggerPrescales& triggerPrescale,
    const std::vector<PileupSummaryInfo>& puInfo,
    const lhef::HEPEUP& hepeup,
    const edm::RefProd<pat::PackedGenParticleCollection>& genParticles,
    const edm::EventID& evtId,
    const GenEventInfoProduct& genEventInfo,
    const GenFilterInfo& generatorFilter,
    bool isRealData,
    const std::string& puScenario,
    const edm::RefProd<pat::ElectronCollection>& electronRefProd,
    const edm::RefProd<pat::MuonCollection>& muonRefProd,
    const edm::RefProd<pat::TauCollection>& tauRefProd,
    const edm::RefProd<pat::JetCollection>& jetRefProd,
    const edm::RefProd<pat::PhotonCollection>& phoRefProd,
    const edm::RefProd<pat::PackedCandidateCollection>& pfRefProd,
    const reco::PhotonCoreRefProd& photonCore,
    const reco::GsfElectronCoreRefProd& gsfCore,
    const std::map<std::string, edm::Ptr<pat::MET> >& mets
    ):
  rho_(rho),
  triggerObjects_(triggerObjects),
  triggerPrescale_(triggerPrescale),
  pv_(pv),
  recoVertices_(recoVertices),
  met_(met),
  metCovariance_(metCovariance),
  puInfo_(puInfo),
  lhe_(hepeup),
  genParticles_(genParticles),
  evtID_(evtId),
  genEventInfoProduct_(genEventInfo),
  generatorFilter_(generatorFilter),
  isRealData_(isRealData),
  puScenario_(puScenario),
  fsaDataFormatVersion_(FSA_DATA_FORMAT_VERSION),
  electronRefProd_(electronRefProd),
  muonRefProd_(muonRefProd),
  tauRefProd_(tauRefProd),
  jetRefProd_(jetRefProd),
  phoRefProd_(phoRefProd),
  pfRefProd_(pfRefProd),
  photonCore_(photonCore),
  gsfCore_(gsfCore),
  mets_(mets)
{ }

const edm::Ptr<reco::Vertex>& PATFinalStateEventMini::pv() const { return pv_; }

const edm::PtrVector<reco::Vertex>& PATFinalStateEventMini::recoVertices() const {
  return recoVertices_;
}

const std::vector<PileupSummaryInfo>& PATFinalStateEventMini::puInfo() const {
  return puInfo_;
}

const lhef::HEPEUP& PATFinalStateEventMini::lesHouches() const {
  return lhe_;
}

const GenEventInfoProduct& PATFinalStateEventMini::genEventInfo() const {
  return genEventInfoProduct_;
}

const GenFilterInfo& PATFinalStateEventMini::generatorFilter() const {
  return generatorFilter_;
}

double PATFinalStateEventMini::rho() const { return rho_; }

const std::vector<pat::TriggerObjectStandAlone>& PATFinalStateEventMini::trig() const {
  return *triggerObjects_; }

const pat::PackedTriggerPrescales& PATFinalStateEventMini::trigPrescale() const {
  return triggerPrescale_; }

const edm::Ptr<pat::MET>& PATFinalStateEventMini::met() const {
  return met_;
}

const TMatrixD& PATFinalStateEventMini::metCovariance() const {
  return metCovariance_;
}

double PATFinalStateEventMini::metSignificance() const {
  return fshelpers::xySignficance(met_->momentum(), metCovariance_);
}

const edm::Ptr<pat::MET> PATFinalStateEventMini::met(
    const std::string& type) const {
  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit != mets_.end())
    return findit->second;
  return edm::Ptr<pat::MET>();
}

const reco::Candidate::LorentzVector PATFinalStateEventMini::met4vector(
    const std::string& type, 
    const std::string& tag, 
    const int applyPhiCorr) const {
  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit == mets_.end())
    return reco::Candidate::LorentzVector();

  const reco::Candidate::LorentzVector& metp4 = (tag == "") ? met(type)->p4() : met(type)->userCand(tag)->p4();
  if (applyPhiCorr == 1)
    return fshelpers::metPhiCorrection(metp4, recoVertices_.size(), !isRealData_);

  return metp4;
}

const edm::EventID& PATFinalStateEventMini::evtId() const {
  return evtID_;
}

// Superseded by the smart trigger
int PATFinalStateEventMini::hltResult(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  return result.passed;
}

int PATFinalStateEventMini::hltPrescale(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  return result.prescale;
}

int PATFinalStateEventMini::hltGroup(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  return result.group;
}

int PATFinalStateEventMini::matchedToFilter(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  std::vector<const pat::TriggerFilter*> filters =
    matchingTriggerFilters(trig(), pattern);
  if (!filters.size())
    return -1;
  return matchedToAnObject(
      trig(), cand, maxDeltaR);
}

int PATFinalStateEventMini::matchedToPath(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  // std::cout << "matcher: " << pattern << std::endl;
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  // std::cout << " result: " << result.group << " " << result.prescale << " " << result.passed << std::endl;
  // Loop over all the paths that fired and see if any matched this object.
  if (!result.passed)
    return -1;
  int matchCount = 0;
  for (size_t i = 0; i < result.paths.size(); ++i) {
    bool matched = matchedToAnObject(
      trig(), cand, maxDeltaR);
    // std::cout << " - path: " << result.paths[i] << " matched: " << matched << std::endl;
    if (matched)
      matchCount += 1;
  }
  return matchCount;
}

const std::string& PATFinalStateEventMini::puTag() const {
  return puScenario_;
}

double PATFinalStateEventMini::puWeight(const std::string& dataTag) const {
  if (isRealData_)
    return 1.;
  return this->puWeight(dataTag, puTag());
}

double PATFinalStateEventMini::puWeight(const std::string& dataTag,
    const std::string& mcTag) const {
  if (isRealData_)
    return 1.;
  return getPileupWeight(dataTag, mcTag, puInfo_[1].getTrueNumInteractions());
}

double PATFinalStateEventMini::puWeight3D(const std::string& dataTag) const {
  if (isRealData_)
    return 1.;
  return this->puWeight3D(dataTag, puTag());
}

double PATFinalStateEventMini::puWeight3D(const std::string& dataTag,
    const std::string& mcTag) const {
  if (isRealData_)
    return 1.;
  return get3DPileupWeight(dataTag, mcTag, puInfo_);
}


float PATFinalStateEventMini::weight(const std::string& name) const {
  typedef std::map<std::string, float> WeightMap;
  WeightMap::const_iterator findit = weights_.find(name);
  if (findit != weights_.end())
    return findit->second;
  else
    return -999;
}
void PATFinalStateEventMini::addWeight(const std::string& name, float weight) {
  weights_[name] = weight;
}

int PATFinalStateEventMini::flag(const std::string& name) const {
  typedef std::map<std::string, int> FlagMap;
  FlagMap::const_iterator findit = flags_.find(name);
  if (findit != flags_.end())
    return findit->second;
  else
    return -999;
}
void PATFinalStateEventMini::addFlag(const std::string& name, int flag) {
  flags_[name] = flag;
}

const pat::ElectronCollection& PATFinalStateEventMini::electrons() const {
  if (!electronRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The electron RefProd is null!" << std::endl;
  return *electronRefProd_;
}

const pat::MuonCollection& PATFinalStateEventMini::muons() const {
  if (!muonRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The muon RefProd is null!" << std::endl;
  return *muonRefProd_;
}

const pat::TauCollection& PATFinalStateEventMini::taus() const {
  if (!tauRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The tau RefProd is null!" << std::endl;
  return *tauRefProd_;
}

const pat::JetCollection& PATFinalStateEventMini::jets() const {
  if (!jetRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The jet RefProd is null!" << std::endl;
  return *jetRefProd_;
}

const pat::PhotonCollection& PATFinalStateEventMini::photons() const {
  if (!phoRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The photon RefProd is null!" << std::endl;
  return *phoRefProd_;
}

const pat::PackedCandidateCollection& PATFinalStateEventMini::pflow() const {
  if (!pfRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The PFLOW RefProd is null!" << std::endl;
  return *pfRefProd_;
}

const bool PATFinalStateEventMini::findDecay(const int pdgIdMother, const int pdgIdDaughter) const{
  return fshelpers::findDecay(genParticles_, pdgIdMother, pdgIdDaughter);
}

float  PATFinalStateEventMini::jetVariables(const reco::CandidatePtr jet, const std::string& myvar) const{
  return fshelpers::jetQGVariables( jet, myvar, recoVertices_);
}

