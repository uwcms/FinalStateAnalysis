#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"

#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"
#include "FinalStateAnalysis/DataAlgos/interface/CollectionFilter.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"

#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/erase.hpp>
#include <algorithm>
#include "TMath.h"

namespace {

  // Predicate to sort a collection of indices, which correspond to a list of
  // candidates, by descending pt
  class CandPtIndexOrdering {
    public:
      CandPtIndexOrdering(const std::vector<const reco::Candidate*>& cands):
        cands_(cands){}
      bool operator()(size_t i1, size_t i2) {
        const reco::Candidate* cand1 = cands_[i1];
        assert(cand1);
        const reco::Candidate* cand2 = cands_[i2];
        assert(cand2);
        return cand1->pt() > cand2->pt();
      }
    private:
      const std::vector<const reco::Candidate*>& cands_;
  };

  class CandPtOrdering {
    public:
      bool operator()(const reco::Candidate* c1, const reco::Candidate* c2) {
        assert(c1); assert(c2);
        return c1->pt() > c2->pt();
      }
  };
}

// empty constructor
PATFinalState::PATFinalState():PATLeafCandidate(){}

PATFinalState::PATFinalState(
    int charge, const reco::Candidate::LorentzVector& p4,
    const edm::Ptr<PATFinalStateEvent>& event):PATLeafCandidate(
      reco::LeafCandidate(charge, p4)) {
  event_ = event;
}

const edm::Ptr<pat::MET>& PATFinalState::met() const {
  return event_->met();
}

const edm::Ptr<reco::Vertex>& PATFinalState::vertexObject() const {
  return event_->pv();
}

const reco::Candidate* PATFinalState::daughter(size_t i) const {
  const reco::Candidate* output = daughterUnsafe(i);
  if (!output) {
    throw cms::Exception("NullDaughter") <<
      "PATFinalState::daughter(" << i << ") is null!" << std::endl;
  }
  return output;
}

const reco::CandidatePtr PATFinalState::daughterPtr(size_t i) const {
  reco::CandidatePtr output = daughterPtrUnsafe(i);
  if (output.isNull())
    throw cms::Exception("NullDaughter") <<
      "PATFinalState::daughterPtr(" << i << ") is null!" << std::endl;
  return output;
}

const reco::CandidatePtr
PATFinalState::daughterUserCand(size_t i, const std::string& tag) const {
  const reco::CandidatePtr output = daughterUserCandUnsafe(i, tag);
  if (output.isNull())
    throw cms::Exception("NullDaughter") <<
      "PATFinalState::daughterUserCand(" << i << ","
      << tag << ") is null!" << std::endl;
  return output;
}

bool
PATFinalState::daughterHasUserCand(size_t i, const std::string& tag) const {
  reco::CandidatePtr userCand = daughterUserCandUnsafe(i, tag);
  return userCand.isNonnull();
}

const PATFinalState::LorentzVector&
PATFinalState::daughterUserCandP4(size_t i, const std::string& tag) const {
  if (tag == "")
    return daughter(i)->p4();
  reco::CandidatePtr userCand = daughterUserCand(i, tag);
  assert(userCand.isNonnull());
  return userCand->p4();
}

std::vector<const reco::Candidate*> PATFinalState::daughters() const {
  std::vector<const reco::Candidate*> output;
  for (size_t i = 0; i < numberOfDaughters(); ++i) {
    output.push_back(daughter(i));
  }
  return output;
}

std::vector<reco::CandidatePtr>
PATFinalState::daughterPtrs(const std::string& tags) const {
  std::vector<std::string> tokens;
  tokens.reserve(numberOfDaughters());

  // remove any whitespace
  std::string cleanSysTags = boost::algorithm::erase_all_copy(tags, " ");
  boost::split(tokens, cleanSysTags, boost::is_any_of(","));

  if (tokens.size() != numberOfDaughters()) {
    throw cms::Exception("BadTokens") <<
      "PATFinalState::daughterPtrs(tags) The number of parsed tokens ("
      << tokens.size() << ") from the token string: " << tags
      << " does not match the number of daughters (" << numberOfDaughters()
      << ")" << std::endl;
  }

  std::vector<reco::CandidatePtr> output;
  for (size_t i = 0; i < numberOfDaughters(); ++i) {
    const std::string& token = tokens[i];
    if (token == "#") // skip daughter
      continue;
    if (token == "" || token == "@") // no sys tag specified
      output.push_back(daughterPtr(i));
    else
      output.push_back(daughterUserCand(i, token));
  }
  return output;
}

std::vector<reco::CandidatePtr>
PATFinalState::daughterPtrs() const {
  std::vector<reco::CandidatePtr> output;
  for (size_t i = 0; i < numberOfDaughters(); ++i) {
    output.push_back(daughterPtr(i));
  }
  return output;
}

std::vector<const reco::Candidate*>
PATFinalState::daughters(const std::string& tags) const {
  if (tags == "")
    return daughters();
  std::vector<std::string> tokens;
  tokens.reserve(numberOfDaughters());

  // remove any whitespace
  std::string cleanSysTags = boost::algorithm::erase_all_copy(tags, " ");
  boost::split(tokens, cleanSysTags, boost::is_any_of(","));

  if (tokens.size() != numberOfDaughters()) {
    throw cms::Exception("BadTokens") <<
      "PATFinalState::daughters(tags) The number of parsed tokens ("
      << tokens.size() << ") from the token string: " << tags
      << " does not match the number of daughters (" << numberOfDaughters()
      << ")" << std::endl;
  }

  std::vector<const reco::Candidate*> output;
  for (size_t i = 0; i < numberOfDaughters(); ++i) {
    const std::string& token = tokens[i];
    if (token == "#") // skip daughter
      continue;
    if (token == "" || token == "@") // no sys tag specified
      output.push_back(daughter(i));
    else
      output.push_back(daughterUserCand(i, token).get());
  }
  return output;
}

std::vector<size_t> PATFinalState::indicesByPt(const std::string& tags) const {
  std::vector<const reco::Candidate*> daughtersToSort;
  daughtersToSort.reserve(numberOfDaughters());
  if (tags == "") {
    daughtersToSort = daughters();
  } else {
    daughtersToSort = daughters(tags);
  }
  std::vector<size_t> indices;
  indices.reserve(3);
  indices.push_back(0); indices.push_back(1); indices.push_back(2);

  std::sort(indices.begin(), indices.end(),
      CandPtIndexOrdering(daughtersToSort));
  return indices;
}

std::vector<const reco::Candidate*> PATFinalState::daughtersByPt(
        const std::string& tags) const {
  std::vector<const reco::Candidate*> daughtersToSort;
  daughtersToSort.reserve(numberOfDaughters());
  if (tags == "") {
    daughtersToSort = daughters();
  } else {
    daughtersToSort = daughters(tags);
  }
  std::sort(daughtersToSort.begin(), daughtersToSort.end(), CandPtOrdering());
  return daughtersToSort;
}
const reco::Candidate*
PATFinalState::daughterByPt(size_t i, const std::string& tags) const {
  return daughtersByPt(tags).at(i);
}

bool
PATFinalState::ptOrdered(size_t i, size_t j, const std::string& tags) const {
  std::vector<const reco::Candidate*> d = daughters(tags);
  assert(i < d.size());
  assert(j < d.size());
  return d[i]->pt() > d[j]->pt();
}

int
PATFinalState::matchToHLTFilter(size_t i, const std::string& filter,
    double maxDeltaR) const {
  const reco::Candidate* dau = this->daughter(i);
  assert(dau);
  return evt()->matchedToFilter(*dau, filter, maxDeltaR);
}

int
PATFinalState::matchToHLTPath(size_t i, const std::string& path,
    double maxDeltaR) const {
  const reco::Candidate* dau = this->daughter(i);
  assert(dau);
  return evt()->matchedToPath(*dau, path, maxDeltaR);
}

double PATFinalState::eval(const std::string& function) const {
  StringObjectFunction<PATFinalState> functor(function, true);
  return functor(*this);
}

bool PATFinalState::filter(const std::string& cut) const {
  StringCutObjectSelector<PATFinalState> cutter(cut, true);
  return cutter(*this);
}

PATFinalState::LorentzVector
PATFinalState::visP4(const std::string& tags) const {
  LorentzVector output;
  std::vector<const reco::Candidate*> theDaughters = daughters(tags);
  for (size_t i = 0; i < numberOfDaughters(); ++i) {
    output += theDaughters[i]->p4();
  }
  return output;
}

PATFinalState::LorentzVector
PATFinalState::visP4() const {
  LorentzVector output;
  std::vector<const reco::Candidate*> theDaughters = daughters();
  for (size_t i = 0; i < numberOfDaughters(); ++i) {
    output += theDaughters[i]->p4();
  }
  return output;
}

PATFinalState::LorentzVector PATFinalState::totalP4(
    const std::string& tags, const std::string& metSysTag) const {
  reco::Candidate::LorentzVector output = visP4(tags);
  if (metSysTag != "" && metSysTag != "@") {
    const reco::CandidatePtr& metUserCand = met()->userCand(metSysTag);
    assert(metUserCand.isNonnull());
    output += metUserCand->p4();
  } else {
    output += met()->p4();
  }
  return output;
}

PATFinalState::LorentzVector PATFinalState::totalP4() const {
  return visP4() + met()->p4();
}

double
PATFinalState::dPhi(int i, const std::string& sysTagI,
    int j, const std::string& sysTagJ) const {
  return reco::deltaPhi(daughterUserCandP4(i, sysTagI).phi(),
      daughterUserCandP4(j, sysTagJ).phi());
}

double
PATFinalState::dPhi(int i, int j) const {
  return dPhi(i, "", j, "");
}

double
PATFinalState::smallestDeltaPhi() const {
  double smallestDeltaPhi = 1e9;
  for (size_t i = 0; i < numberOfDaughters()-1; ++i) {
    for (size_t j = i+1; j < numberOfDaughters(); ++j) {
      double deltaPhiIJ = deltaPhi(i, j);
      if (deltaPhiIJ < smallestDeltaPhi) {
        smallestDeltaPhi = deltaPhiIJ;
      }
    }
  }
  return smallestDeltaPhi;
}

double
PATFinalState::dR(int i, const std::string& sysTagI,
    int j, const std::string& sysTagJ) const {
  return reco::deltaR(daughterUserCandP4(i, sysTagI),
      daughterUserCandP4(j, sysTagJ));
}

double
PATFinalState::dR(int i, int j) const {
  return dR(i, "", j, "");
}

double
PATFinalState::smallestDeltaR() const {
  double smallestDeltaR = 1e9;
  for (size_t i = 0; i < numberOfDaughters()-1; ++i) {
    for (size_t j = i+1; j < numberOfDaughters(); ++j) {
      double deltaRIJ = dR(i, j);
      if (deltaRIJ < smallestDeltaR) {
        smallestDeltaR = deltaRIJ;
      }
    }
  }
  return smallestDeltaR;
}

double
PATFinalState::deltaPhiToMEt(int i, const std::string& sysTag,
    const std::string& metTag) const {
  double metPhi = met()->phi();
  if (metTag != "") {
    const reco::CandidatePtr& metUserCand = met()->userCand(metTag);
    assert(metUserCand.isNonnull());
    metPhi = metUserCand->phi();
  }
  return reco::deltaPhi(daughterUserCandP4(i, sysTag).phi(), metPhi);
}

double
PATFinalState::deltaPhiToMEt(int i) const {
  return deltaPhiToMEt(i, "", "");
}

double
PATFinalState::mt(int i, const std::string& sysTagI,
    int j, const std::string& sysTagJ) const {
  return fshelpers::transverseMass(daughterUserCandP4(i, sysTagI),
      daughterUserCandP4(j, sysTagJ));
}

double
PATFinalState::mt(int i, int j) const {
  return mt(i, "", j, "");
}

double PATFinalState::mtMET(int i, const std::string& tag,
    const std::string& metTag) const {
  if (metTag != "") {
    return fshelpers::transverseMass(daughterUserCandP4(i, tag),
        met()->userCand(metTag)->p4());
  } else {
    return fshelpers::transverseMass(daughterUserCandP4(i, tag),
        met()->p4());
  }
}

double PATFinalState::mtMET(int i, const std::string& metTag) const {
  if (metTag != "") {
    return fshelpers::transverseMass(daughterUserCandP4(i, ""),
        met()->userCand(metTag)->p4());
  } else {
    return fshelpers::transverseMass(daughterUserCandP4(i, ""), met()->p4());
  }
}

double PATFinalState::ht(const std::string& sysTags) const {
  std::vector<const reco::Candidate*> theDaughters = daughters(sysTags);
  double output = 0;
  for (size_t i = 0; i < numberOfDaughters(); ++i) {
    output += theDaughters[i]->pt();
  }
  return output;
}

double PATFinalState::ht() const {
  std::vector<const reco::Candidate*> theDaughters = daughters();
  double output = 0;
  for (size_t i = 0; i < numberOfDaughters(); ++i) {
    output += theDaughters[i]->pt();
  }
  return output;
}

double PATFinalState::pZeta(int i, int j) const {
  return fshelpers::pZeta(daughter(i)->p4(), daughter(j)->p4(),
      met()->px(), met()->py()).first;
}

double PATFinalState::pZetaVis(int i, int j) const {
  return fshelpers::pZeta(daughter(i)->p4(), daughter(j)->p4(),
      met()->px(), met()->py()).second;
}

std::vector<reco::CandidatePtr> PATFinalState::extras(
    const std::string& label, const std::string& filter) const {
  // maybe this needs to be optimized
  StringCutObjectSelector<reco::Candidate> cut(filter, true);
  const reco::CandidatePtrVector& unfiltered = overlaps(label);
  std::vector<reco::CandidatePtr> output;
  for (size_t i = 0; i < unfiltered.size(); ++i) {
    const reco::CandidatePtr& cand = unfiltered[i];
    if (cut(*cand))
      output.push_back(cand);
  }
  return output;
}

std::vector<reco::CandidatePtr> PATFinalState::filteredOverlaps(
    int i, const std::string& label, const std::string& filter) const {
  // maybe this needs to be optimized
  StringCutObjectSelector<reco::Candidate> cut(filter, true);
  const reco::CandidatePtrVector& unfiltered = daughterOverlaps(i, label);
  std::vector<reco::CandidatePtr> output;
  for (size_t i = 0; i < unfiltered.size(); ++i) {
    const reco::CandidatePtr& cand = unfiltered[i];
    if (cut(*cand))
      output.push_back(cand);
  }
  return output;
}

std::vector<const reco::Candidate*> PATFinalState::vetoMuons(
    double dR, const std::string& filter) const {
  return getVetoObjects(
      daughters(),
      ptrizeCollection(evt()->muons()),
      dR, filter);
}

std::vector<const reco::Candidate*> PATFinalState::vetoElectrons(
    double dR, const std::string& filter) const {
  return getVetoObjects(
      daughters(),
      ptrizeCollection(evt()->electrons()),
      dR, filter);
}

std::vector<const reco::Candidate*> PATFinalState::vetoTaus(
    double dR, const std::string& filter) const {
  return getVetoObjects(
      daughters(),
      ptrizeCollection(evt()->taus()),
      dR, filter);
}

std::vector<const reco::Candidate*> PATFinalState::vetoJets(
    double dR, const std::string& filter) const {
  return getVetoObjects(
      daughters(),
      ptrizeCollection(evt()->jets()),
      dR, filter);
}

std::vector<const reco::Candidate*> PATFinalState::overlapMuons(
    int i, double dR, const std::string& filter) const {
  return getOverlapObjects(
      *daughter(i),
      ptrizeCollection(evt()->muons()),
      dR, filter);
}

std::vector<const reco::Candidate*> PATFinalState::overlapElectrons(
    int i, double dR, const std::string& filter) const {
  return getOverlapObjects(
      *daughter(i),
      ptrizeCollection(evt()->electrons()),
      dR, filter);
}

std::vector<const reco::Candidate*> PATFinalState::overlapTaus(
    int i, double dR, const std::string& filter) const {
  return getOverlapObjects(
      *daughter(i),
      ptrizeCollection(evt()->taus()),
      dR, filter);
}

std::vector<const reco::Candidate*> PATFinalState::overlapJets(
    int i, double dR, const std::string& filter) const {
  return getOverlapObjects(
      *daughter(i),
      ptrizeCollection(evt()->jets()),
      dR, filter);
}

//double PATFinalState::massUsingSuperCluster(
//    int electronIndex, int j, int x, int y, int z) const {
//  reco::Candidate::LorentzVector total;
//  total += daughterAsElectron(electronIndex);
//  total += daughter(j)->p4();
//}

PATFinalStateProxy
PATFinalState::subcand(int i, int j, int x, int y, int z) const {
  std::vector<reco::CandidatePtr> output;
  output.push_back(daughterPtr(i));
  output.push_back(daughterPtr(j));
  if (x > -1)
    output.push_back(daughterPtr(x));
  if (y > -1)
    output.push_back(daughterPtr(y));
  if (z > -1)
    output.push_back(daughterPtr(z));
  return PATFinalStateProxy(
      new PATMultiCandFinalState(output, evt()));
}

PATFinalStateProxy
PATFinalState::subcand(const std::string& tags) const {
  const std::vector<reco::CandidatePtr> daus = daughterPtrs(tags);
  return PATFinalStateProxy(
      new PATMultiCandFinalState(daus, evt()));
}

PATFinalStateProxy
PATFinalState::subcand(const std::string& tags,
    const std::string& extraColl, const std::string& filter) const {
  const std::vector<reco::CandidatePtr> daus = daughterPtrs(tags);
  const std::vector<reco::CandidatePtr> cands = extras(extraColl, filter);
  std::vector<reco::CandidatePtr> toAdd;
  toAdd.reserve(daus.size() + cands.size());
  for (size_t i = 0; i < cands.size(); ++i) {
    toAdd.push_back(cands[i]);
  }
  for (size_t i = 0; i < daus.size(); ++i) {
    toAdd.push_back(daus[i]);
  }
  return PATFinalStateProxy(
      new PATMultiCandFinalState(toAdd, evt()));
}

bool PATFinalState::likeSigned(int i, int j) const {
  return daughter(i)->charge()*daughter(j)->charge() > 0;
}

bool PATFinalState::likeFlavor(int i, int j) const {
  return std::abs(daughter(i)->pdgId()) == std::abs(daughter(j)->pdgId());
}

double PATFinalState::zCompatibility(int i, int j) const {
  if (likeSigned(i, j)) {
    return 1000;
  }
  return std::abs(subcand(i, j)->mass() - 91.2);
}

VBFVariables PATFinalState::vbfVariables(const std::string& jetCuts) const {
  std::vector<const reco::Candidate*> hardScatter = this->daughters();
  std::vector<const reco::Candidate*> jets = this->vetoJets(0.3, jetCuts);
  const reco::Candidate::LorentzVector& metp4 = met()->p4();
  // todo cache this
  return computeVBFInfo(hardScatter, metp4, jets);
}

bool PATFinalState::orderedInPt(int i, int j) const {
  return daughter(i)->pt() > daughter(j)->pt();
}

edm::Ptr<pat::Tau> PATFinalState::daughterAsTau(size_t i) const {
  return daughterAs<pat::Tau>(i);
}
edm::Ptr<pat::Muon> PATFinalState::daughterAsMuon(size_t i) const {
  return daughterAs<pat::Muon>(i);
}
edm::Ptr<pat::Electron> PATFinalState::daughterAsElectron(size_t i) const {
  return daughterAs<pat::Electron>(i);
}
edm::Ptr<pat::Jet> PATFinalState::daughterAsJet(size_t i) const {
  return daughterAs<pat::Jet>(i);
}
