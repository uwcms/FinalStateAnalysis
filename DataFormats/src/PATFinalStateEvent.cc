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

void unpackTrigger(std::vector<pat::TriggerObjectStandAlone> trig, const edm::TriggerNames& names) {
  for (pat::TriggerObjectStandAlone obj : trig) {
    obj.unpackPathNames(names);
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
    bool miniAOD,
    double rho,
    const edm::Ptr<reco::Vertex>& pv,
    const edm::PtrVector<reco::Vertex>& recoVertices,
    const edm::Ptr<pat::MET>& met,
    const TMatrixD& metCovariance,
    const pat::TriggerEvent triggerEvent,
    const edm::RefProd<std::vector<pat::TriggerObjectStandAlone>>& triggerObjects,
    const edm::TriggerNames& names,
    const pat::PackedTriggerPrescales& triggerPrescale,
    const edm::TriggerResults& triggerResults,
    const std::vector<PileupSummaryInfo>& puInfo,
    const lhef::HEPEUP& hepeup,
    const reco::GenParticleRefProd& genParticles,
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
    const reco::PFCandidateRefProd& pfRefProd,
    const edm::RefProd<pat::PackedCandidateCollection>& packedPFRefProd,
    const reco::TrackRefProd& tracks,
    const reco::GsfTrackRefProd& gsfTracks,
    const std::map<std::string, edm::Ptr<pat::MET> >& mets
    ):
  miniAOD_(miniAOD),
  rho_(rho),
  triggerEvent_(triggerEvent),
  triggerObjects_(triggerObjects),
  names_(names),
  triggerPrescale_(triggerPrescale),
  triggerResults_(triggerResults),
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
  packedPFRefProd_(packedPFRefProd),
  tracks_(tracks),
  gsfTracks_(gsfTracks),
  mets_(mets)
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

const GenFilterInfo& PATFinalStateEvent::generatorFilter() const {
  return generatorFilter_;
}

double PATFinalStateEvent::rho() const { return rho_; }

const pat::TriggerEvent& PATFinalStateEvent::trig() const {
  return triggerEvent_; }

const std::vector<pat::TriggerObjectStandAlone>& PATFinalStateEvent::trigStandAlone() const {
  return *triggerObjects_; }

const edm::TriggerNames& PATFinalStateEvent::names() const {
  return names_; }

const pat::PackedTriggerPrescales& PATFinalStateEvent::trigPrescale() const {
  return triggerPrescale_; }

const edm::TriggerResults& PATFinalStateEvent::trigResults() const {
  return triggerResults_; }

const edm::Ptr<pat::MET>& PATFinalStateEvent::met() const {
  return met_;
}

const edm::Ptr<pat::MET> PATFinalStateEvent::met(
    const std::string& type) const 
{
  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit != mets_.end() && findit->second.isNonnull())
    return findit->second;
  return edm::Ptr<pat::MET>();
}

const TMatrixD& PATFinalStateEvent::metCovariance() const {
  return metCovariance_;
}

double PATFinalStateEvent::metSignificance() const {
  return fshelpers::xySignficance(met_->momentum(), metCovariance_);
}

const reco::Candidate::LorentzVector PATFinalStateEvent::met4vector(
								    const std::string& type, 
								    const std::string& tag, 
								    const int applyPhiCorr) const 
{
  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit == mets_.end() || findit->second.isNull())
    return reco::Candidate::LorentzVector();
  if(tag == "jes+")
    return met(type)->shiftedP4(pat::MET::JetEnUp);
  else if(tag == "ues+")
    return met(type)->shiftedP4(pat::MET::UnclusteredEnUp);
  else if(tag == "tes+")
    return met(type)->shiftedP4(pat::MET::TauEnUp);
  else if(tag == "mes+")
    return met(type)->shiftedP4(pat::MET::MuonEnUp);
  else
    return met(type)->p4();      

  // TODO
  //if (applyPhiCorr == 1)
  //  return fshelpers::metPhiCorrection(metp4, recoVertices_.size(), !isRealData_);
}

const edm::EventID& PATFinalStateEvent::evtId() const {
  return evtID_;
}

// Superseded by the smart trigger
int PATFinalStateEvent::hltResult(const std::string& pattern) const {
  SmartTriggerResult result = miniAOD_ ? smartTrigger(pattern, names(), trigPrescale(), trigResults(), evtID_) : 
    smartTrigger(pattern, trig(), evtID_);
  return result.passed;
}

int PATFinalStateEvent::hltPrescale(const std::string& pattern) const {
  SmartTriggerResult result = miniAOD_ ? smartTrigger(pattern, names(), trigPrescale(), trigResults(), evtID_) : 
    smartTrigger(pattern, trig(), evtID_);
  return result.prescale;
}

int PATFinalStateEvent::hltGroup(const std::string& pattern) const {
  SmartTriggerResult result = miniAOD_ ? smartTrigger(pattern, names(), trigPrescale(), trigResults(), evtID_) : 
    smartTrigger(pattern, trig(), evtID_);
  return result.group;
}

int PATFinalStateEvent::matchedToFilter(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  std::vector<const pat::TriggerFilter*> filters = miniAOD_ ?
    matchingTriggerFilters(trigStandAlone(), names(), pattern) :
    matchingTriggerFilters(trig(), pattern);
  if (!filters.size())
    return -1;
  return miniAOD_ ? matchedToAnObject(trigStandAlone(), cand, maxDeltaR) :
    matchedToAnObject(triggerEvent_.filterObjects(filters[0]->label()), cand, maxDeltaR);
}

int PATFinalStateEvent::matchedToPath(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  // std::cout << "matcher: " << pattern << std::endl;
  SmartTriggerResult result = miniAOD_ ? smartTrigger(pattern, names(), trigPrescale(), trigResults(), evtID_) : 
    smartTrigger(pattern, trig(), evtID_);
  //std::cout << " result: " << result.group << " " << result.prescale << " " << result.passed << std::endl;
  // Loop over all the paths that fired and see if any matched this object.
  if (!result.passed)
    return -1;
  int matchCount = 0;
  for (size_t i = 0; i < result.paths.size(); ++i) {
    bool matched = miniAOD_ ? matchedToAnObject(trigStandAlone(), cand, maxDeltaR) :
      matchedToAnObject(triggerEvent_.pathObjects(result.paths[i]), cand, maxDeltaR);
    // std::cout << " - path: " << result.paths[i] << " matched: " << matched << std::endl;
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

const pat::PhotonCollection& PATFinalStateEvent::photons() const {
  if (!phoRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The photon RefProd is null!" << std::endl;
  return *phoRefProd_;
}

const reco::PFCandidateCollection& PATFinalStateEvent::pflow() const {
  if (!pfRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The PFLOW RefProd is null!" << std::endl;
  return *pfRefProd_;
}

const pat::PackedCandidateCollection& PATFinalStateEvent::packedPflow() const {
  if (!packedPFRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The Packed PFLOW RefProd is null!" << std::endl;
  return *packedPFRefProd_;
}

const bool PATFinalStateEvent::findDecay(const int pdgIdMother, const int pdgIdDaughter) const{
  return fshelpers::findDecay(genParticles_, pdgIdMother, pdgIdDaughter);
}

float  PATFinalStateEvent::jetVariables(const reco::CandidatePtr jet, const std::string& myvar) const{
  return fshelpers::jetQGVariables( jet, myvar, recoVertices_);
}

