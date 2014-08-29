#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"

#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"
#include "FinalStateAnalysis/DataAlgos/interface/CollectionFilter.h"
#include "FinalStateAnalysis/DataAlgos/interface/ApplySVfit.h"

#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"

#include "DataFormats/EgammaCandidates/interface/ConversionFwd.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/erase.hpp>
#include <algorithm>
#include <iostream>
#include <sstream>
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
    const edm::Ptr<PATFinalStateEvent>& event) : PATLeafCandidate(reco::LeafCandidate(charge, p4))
{
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
  if (!event_->isMiniAOD() && metSysTag != "" && metSysTag != "@") {
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
PATFinalState::SVfit(int i, int j) const {

  std::vector<reco::CandidatePtr> toFit;
  toFit.push_back(daughterPtr(i));
  toFit.push_back(daughterPtr(j));

  edm::Ptr<pat::MET> mvaMet;
  if(event_->isMiniAOD())
    {
      // Turn this back on when miniAOD gains MVA MET
      std::cout << "MVA MET doesn't exist in miniAOD yet. How did we even get here!?!?!?" << std::endl;
    }
  else
    {
      mvaMet = evt()->met("mvamet");
    }

  if (mvaMet.isNull()) {
    throw cms::Exception("MissingMVAMet")
      << "SV fit requires the MVAMET be available via "
      << " met('mvamet') method in PATFinalStateEvent.  It's null."
      << std::endl;
  }


  return ApplySVfit::getSVfitMass(toFit, *mvaMet,
      mvaMet->getSignificanceMatrix(), 0,
      evt()->evtId());
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
  double metPhi;
  if(metTag != "")
    {
      if (event_->isMiniAOD())
	{
	  if(metTag == "jes+")
	    metPhi = met()->shiftedPhi(pat::MET::JetEnUp);
	  else if(metTag == "ues+")
	    metPhi = met()->shiftedPhi(pat::MET::UnclusteredEnUp);
	  else if(metTag == "tes+")
	    metPhi = met()->shiftedPhi(pat::MET::TauEnUp);
	  else if(metTag == "mes+")
	    metPhi = met()->shiftedPhi(pat::MET::MuonEnUp);
	  else // all miniAOD pfMET is Type 1
	    metPhi = met()->phi();
	}
      else
	{
	  const reco::CandidatePtr& metUserCand = met()->userCand(metTag);
	  assert(metUserCand.isNonnull());
	  metPhi = metUserCand->phi();
	}
    }
  else
    metPhi = met()->phi();
      
  return reco::deltaPhi(daughterUserCandP4(i, sysTag).phi(), metPhi);
}

double 
PATFinalState::twoParticleDeltaPhiToMEt(const int i, const int j, const std::string& metTag) const
{
  PATFinalStateProxy composite = subcand(i,j);
  double compositePhi = composite.get()->phi();
  double metPhi;
  if(metTag != "")
    {
      if(event_->isMiniAOD())
	{
	  if(metTag == "jes+")
	    metPhi = met()->shiftedPhi(pat::MET::JetEnUp);
	  else if(metTag == "ues+")
	    metPhi = met()->shiftedPhi(pat::MET::UnclusteredEnUp);
	  else if(metTag == "tes+")
	    metPhi = met()->shiftedPhi(pat::MET::TauEnUp);
	  else if(metTag == "mes+")
	    metPhi = met()->shiftedPhi(pat::MET::MuonEnUp);
	  else // all miniAOD pfMET is Type 1
	    metPhi = met()->phi();
	}
      else
	{
	  const reco::CandidatePtr& metUserCand = met()->userCand(metTag);
	  assert(metUserCand.isNonnull());
	  metPhi = metUserCand->phi();
	}
    }
  else
    metPhi = met()->phi();
      
  return reco::deltaPhi(compositePhi, metPhi);
      
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
  reco::Candidate::LorentzVector metP4;
  if(event_->isMiniAOD())
    {
      if(metTag == "jes+")
	metP4 = met()->shiftedP4(pat::MET::JetEnUp);
      else if(metTag == "ues+")
	metP4 = met()->shiftedP4(pat::MET::UnclusteredEnUp);
      else if(metTag == "tes+")
	metP4 = met()->shiftedP4(pat::MET::TauEnUp);
      else if(metTag == "mes+")
	metP4 = met()->shiftedP4(pat::MET::MuonEnUp);
      else // all miniAOD pfMET is Type 1
	metP4 = met()->p4();
    }
  else if (metTag != "") 
    {
      metP4 = met()->userCand(metTag)->p4();
    } 
  else 
    {
      metP4 = met()->p4();
    }
  return fshelpers::transverseMass(daughterUserCandP4(i, tag), metP4);
}

double PATFinalState::mtMET(int i, const std::string& metTag) const {
  return mtMET(i, "", metTag);
}

double PATFinalState::mtMET(int i, const std::string& tag,
			    const std::string& metName, const std::string& metTag, 
			    const int applyPhiCorr) const {
  if(event_->isMiniAOD())
    return mtMET(i, tag, metTag);
  return fshelpers::transverseMass(daughterUserCandP4(i, tag),
				   evt()->met4vector(metName, metTag, applyPhiCorr));
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

std::vector<const reco::Candidate*> PATFinalState::vetoPhotons(
    double dR, const std::string& filter) const {
  return getVetoObjects(
      daughters(),
      ptrizeCollection(evt()->photons()),
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

std::vector<const reco::Candidate*> PATFinalState::overlapPhotons(
    int i, double dR, const std::string& filter) const {
  return getOverlapObjects(
      *daughter(i),
      ptrizeCollection(evt()->photons()),
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
PATFinalState::subcandfsr( int i, int j ) const
{
  std::vector<reco::CandidatePtr> output;
  output.push_back( daughterPtr(i) );
  output.push_back( daughterPtr(j) );

  std::stringstream ss;
  ss << "fsrPhoton" << i << j;
  std::string photon_name = ss.str();

  const std::vector<std::string>& userCandList = this->userCandNames();
  for (size_t i = 0; i < userCandList.size(); ++i)
  {
      if (userCandList[i].find(photon_name) != std::string::npos)
          output.push_back(this->userCand(userCandList[i]));
  }

  return PATFinalStateProxy(
      new PATMultiCandFinalState(output, evt()));
}

PATFinalState::LorentzVector
PATFinalState::p4fsr() const
{
  PATFinalState::LorentzVector p4_out;

  p4_out = daughter(0)->p4() + daughter(1)->p4() + daughter(2)->p4() + daughter(3)->p4();

  const std::vector<std::string>& userCandList = this->userCandNames();
  for (size_t i = 0; i < userCandList.size(); ++i)
  {
      if (userCandList[i].find("fsrPhoton1") != std::string::npos)
          p4_out += this->userCand(userCandList[i])->p4();

      if (userCandList[i].find("fsrPhoton2") != std::string::npos)
          p4_out += this->userCand(userCandList[i])->p4();
  }

  return p4_out;
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

int PATFinalState::hppCompatibility(int i, int j, int chg) const {
  if (likeSigned(i,j)) {
    if ((chg > 0 && daughter(i)->charge() > 0) ||
        (chg < 0 && daughter(i)->charge() < 0)) {
      return 1;
    }
  }
  return 0;
}

double PATFinalState::zCompatibility(int i, int j) const {
  if (likeSigned(i, j)) {
    return 1000;
  }
  return std::abs(subcand(i, j)->mass() - 91.1876);
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

edm::Ptr<pat::Photon> PATFinalState::daughterAsPhoton(size_t i) const {
  return daughterAs<pat::Photon>(i);
}

const reco::GenParticleRef PATFinalState::getDaughterGenParticle(size_t i, int pdgIdToMatch, int checkCharge) const {
  bool charge = (bool) checkCharge;
  return fshelpers::getGenParticle( daughter(i), event_->genParticleRefProd(), pdgIdToMatch, charge);
}

const reco::GenParticleRef PATFinalState::getDaughterGenParticleMotherSmart(size_t i, int pdgIdToMatch, int checkCharge) const {
  const reco::GenParticleRef genp = getDaughterGenParticle(i, pdgIdToMatch, checkCharge);
  if( genp.isAvailable() && genp.isNonnull()  )
    return fshelpers::getMotherSmart(genp, genp->pdgId());
  else
    return genp;
}

const bool PATFinalState::comesFromHiggs(size_t i, int pdgIdToMatch, int checkCharge) const {
  const reco::GenParticleRef genp = getDaughterGenParticle(i, pdgIdToMatch, checkCharge);
  if( genp.isAvailable() && genp.isNonnull()  )
    return fshelpers::comesFromHiggs(genp);
  else
    return false;
}

const reco::Candidate::Vector PATFinalState::getDaughtersRecoil() const {
  double x =0;
  double y =0;
  std::vector<const reco::Candidate*> daughters = this->daughters();
  for(std::vector<const reco::Candidate*>::const_iterator daughter = daughters.begin(); daughter != daughters.end(); ++daughter){
    TVector2 ivec;
    ivec.SetMagPhi( (*daughter)->pt(), (*daughter)->phi() );
    x += ivec.X();
    y += ivec.Y();
  }
  const reco::Candidate::Vector retval(x,y,0.);
  return retval;
}

const reco::Candidate::Vector PATFinalState::getDaughtersRecoilWithMet() const {
  const reco::Candidate::Vector dau_recoil = getDaughtersRecoil();
  const edm::Ptr<pat::MET>& met = event_->met();
  const reco::Candidate::Vector retval = dau_recoil + met->momentum();
  return retval;
}

//const double PATFinalState::getRecoilWithMetSignificance() const {
//  return fshelpers::xySignficance(getDaughtersRecoilWithMet(), event_->metCovariance());
//}


const math::XYZTLorentzVector
PATFinalState::getUserLorentzVector(size_t i,const std::string& name) const {
  edm::Ptr<pat::Electron> ele = daughterAsElectron(i);
  edm::Ptr<pat::Muon> mu = daughterAsMuon(i);
  edm::Ptr<pat::Photon> pho = daughterAsPhoton(i);
  edm::Ptr<pat::Jet> jet = daughterAsJet(i);
  edm::Ptr<pat::Tau> tau = daughterAsTau(i);

  const math::XYZTLorentzVector* result = NULL;

  if(ele.isNonnull() && ele.isAvailable())
    result = ele->userData<math::XYZTLorentzVector>(name);

  if(mu.isNonnull() && mu.isAvailable())
    result = mu->userData<math::XYZTLorentzVector>(name);

  if(pho.isNonnull() && pho.isAvailable())
    result = pho->userData<math::XYZTLorentzVector>(name);

  if(jet.isNonnull() && jet.isAvailable())
    result = jet->userData<math::XYZTLorentzVector>(name);

  if(tau.isNonnull() && tau.isAvailable())
    result = tau->userData<math::XYZTLorentzVector>(name);

  if( result ) return *result; // return the result if we have it stored

  return math::XYZTLorentzVector();
}

const float PATFinalState::getPhotonUserIsolation(size_t i,
						  const std::string& key) const {
  edm::Ptr<pat::Photon> d = daughterAsPhoton(i);
  // remove leading namespace specifier
  std::string prunedKey = ( key.find("pat::") == 0 ) ? std::string(key, 5) : key;
  if ( prunedKey == "TrackIso" ) return d->userIsolation(pat::TrackIso);
  if ( prunedKey == "EcalIso" ) return d->userIsolation(pat::EcalIso);
  if ( prunedKey == "HcalIso" ) return d->userIsolation(pat::HcalIso);
  if ( prunedKey == "PfAllParticleIso" ) return d->userIsolation(pat::PfAllParticleIso);
  if ( prunedKey == "PfChargedHadronIso" ) return d->userIsolation(pat::PfChargedHadronIso);
  if ( prunedKey == "PfNeutralHadronIso" ) return d->userIsolation(pat::PfNeutralHadronIso);
  if ( prunedKey == "PfGammaIso" ) return d->userIsolation(pat::PfGammaIso);
  if ( prunedKey == "User1Iso" ) return d->userIsolation(pat::User1Iso);
  if ( prunedKey == "User2Iso" ) return d->userIsolation(pat::User2Iso);
  if ( prunedKey == "User3Iso" ) return d->userIsolation(pat::User3Iso);
  if ( prunedKey == "User4Iso" ) return d->userIsolation(pat::User4Iso);
  if ( prunedKey == "User5Iso" ) return d->userIsolation(pat::User5Iso);
  if ( prunedKey == "UserBaseIso" ) return d->userIsolation(pat::UserBaseIso);
  if ( prunedKey == "CaloIso" ) return d->userIsolation(pat::CaloIso);
  if ( prunedKey == "PfPUChargedHadronIso" )
    return d->userIsolation(pat::PfPUChargedHadronIso);
  //throw cms::Excepton("Missing Data")
  //<< "Isolation corresponding to key "
  //<< key << " was not stored for this particle.";
  return -1.0;
}


const float PATFinalState::jetVariables(size_t i, const std::string& key) const {
  //  const reco::Candidate* mydaughter = this->daughter(i);
  if (this->daughterUserCand(i,"patJet").isAvailable() && this->daughterUserCand(i,"patJet").isNonnull()){
    return evt()->jetVariables(daughterUserCand(i,"patJet"), key);
  }
  return -100; 
}


const float PATFinalState::getIP3D(const size_t i) const
{
  if(event_->isMiniAOD())
    {
      if(abs(daughter(i)->pdgId()) == 11)
	{
	  return fabs(daughterAsElectron(i)->dB(pat::Electron::PV3D));
	}
      else if (abs(daughter(i)->pdgId()) == 13)
	{
	  return fabs(daughterAsMuon(i)->dB(pat::Muon::PV3D));
	}
      
      throw cms::Exception("InvalidParticle") << "FSA can only find SIP3D for electron and muon for now" << std::endl;
    }

  return dynamic_cast<const pat::PATObject<reco::Candidate>* >(daughter(i))->userFloat("ip3D");
}

const float PATFinalState::getIP3DSig(const size_t i) const
{
  if(event_->isMiniAOD())
    {
      if(abs(daughter(i)->pdgId()) == 11)
	{
	  return daughterAsElectron(i)->edB(pat::Electron::PV3D);
	}
      else if (abs(daughter(i)->pdgId()) == 13)
	{
	  return daughterAsMuon(i)->edB(pat::Muon::PV3D);
	}
      
      throw cms::Exception("InvalidParticle") << "FSA can only find SIP3D for electron and muon for now" << std::endl;
    }

return static_cast<const pat::PATObject<reco::Candidate> *>(daughter(i))->userFloat("ip3DS");
}

const float PATFinalState::getDZ(const size_t i) const
{
  if(event_->isMiniAOD())
    {
      if(abs(daughter(i)->pdgId()) == 11)
	{
	  const edm::Ptr<reco::Vertex> pv = event_->pv();
	  return daughterAsElectron(i)->gsfTrack()->dz(pv->position());
	}
      else if(abs(daughter(i)->pdgId()) == 13)
	{
	  const edm::Ptr<reco::Vertex> pv = event_->pv();
	  return daughterAsMuon(i)->muonBestTrack()->dz(pv->position());
	}
      
      throw cms::Exception("InvalidParticle") << "FSA can only find dZ for electron and muon for now" << std::endl;
    }
  
  return dynamic_cast<const pat::PATObject<reco::Candidate> *>(daughter(i))->userFloat("dz");
}

const bool PATFinalState::isTightMuon(const size_t i) const
{
  return daughterAsMuon(i)->isTightMuon(*vertexObject());
}

const bool PATFinalState::passElectronID(const size_t i, std::string id) const
{
  // The values are taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2
  // They should be (in order): dEtaIn, dPhiIn, full5x5_sigmaIEtaIEta, H/E, d0, dz, 1/e-1/p, pfIso, missing hits
  edm::Ptr<pat::Electron> el = daughterAsElectron(i);
  float etaSC_ = el->superCluster()->eta();
  bool pass = false;
  if (id=="cutBasedElectronID-CSA14-50ns-V1-standalone-veto"){
    if (abs(etaSC_) < 1.479){
      pass = eIDHelper(i,0.021,0.25,0.012,0.24,0.031,0.5,0.32,0.24,2);
    }
    else if (abs(etaSC_)>1.479 && abs(etaSC_)<2.5){
      pass = eIDHelper(i,0.028,0.23,0.035,0.19,0.22,0.91,0.13,0.24,3);
    }
  }
  if (id=="cutBasedElectronID-CSA14-50ns-V1-standalone-loose"){
    if (abs(etaSC_) < 1.479){
      pass = eIDHelper(i,0.016,0.08,0.012,0.15,0.019,0.036,0.11,0.18,1);
    }
    else if (abs(etaSC_)>1.479 && abs(etaSC_)<2.5){
      pass = eIDHelper(i,0.025,0.097,0.032,0.12,0.099,0.88,0.11,0.21,1);
    }
  }
  if (id=="cutBasedElectronID-CSA14-50ns-V1-standalone-medium"){
    if (abs(etaSC_) < 1.479){
      pass = eIDHelper(i,0.015,0.051,0.01,0.10,0.012,0.030,0.053,0.14,1);
    }
    else if (abs(etaSC_)>1.479 && abs(etaSC_)<2.5){
      pass = eIDHelper(i,0.023,0.056,0.030,0.099,0.068,0.78,0.11,0.15,1);
    }
  }
  if (id=="cutBasedElectronID-CSA14-50ns-V1-standalone-tight"){
    if (abs(etaSC_) < 1.479){
      pass = eIDHelper(i,0.012,0.024,0.01,0.074,0.0091,0.017,0.026,0.10,1);
    }
    else if (abs(etaSC_)>1.479 && abs(etaSC_)<2.5){
      pass = eIDHelper(i,0.019,0.043,0.029,0.08,0.037,0.065,0.076,0.14,1);
    }
  }
  if (id=="cutBasedElectronID-CSA14-PU20bx25-V0-standalone-veto"){
    if (abs(etaSC_) < 1.479){
      pass = eIDHelper(i,0.02,0.2579,0.0125,0.2564,0.025,0.5863,0.1508,0.3313,2);
    }
    else if (abs(etaSC_)>1.479 && abs(etaSC_)<2.5){
      pass = eIDHelper(i,0.0141,0.2591,0.371,0.1335,0.2232,0.9513,0.1542,0.3816,3);
    }
  }
  if (id=="cutBasedElectronID-CSA14-PU20bx25-V0-standalone-loose"){
    if (abs(etaSC_) < 1.479){
      pass = eIDHelper(i,0.0181,0.0936,0.0123,0.141,0.0166,0.54342,0.1353,0.24,1);
    }
    else if (abs(etaSC_)>1.479 && abs(etaSC_)<2.5){
      pass = eIDHelper(i,0.0124,0.0642,0.035,0.1115,0.096,0.9187,0.1443,0.3529,1);
    }
  }
  if (id=="cutBasedElectronID-CSA14-PU20bx25-V0-standalone-medium"){
    if (abs(etaSC_) < 1.479){
      pass = eIDHelper(i,0.0106,0.0323,0.0107,0.067,0.0131,0.22310,0.1043,0.2179,1);
    }
    else if (abs(etaSC_)>1.479 && abs(etaSC_)<2.5){
      pass = eIDHelper(i,0.0108,0.0455,0.0318,0.097,0.0845,0.7523,0.1201,0.254,1);
    }
  }
  if (id=="cutBasedElectronID-CSA14-PU20bx25-V0-standalone-tight"){
    if (abs(etaSC_) < 1.479){
      pass = eIDHelper(i,0.0091,0.031,0.0106,0.0532,0.0126,0.0116,0.0609,0.1649,1);
    }
    else if (abs(etaSC_)>1.479 && abs(etaSC_)<2.5){
      pass = eIDHelper(i,0.106,0.0359,0.305,0.0835,0.0163,0.5999,0.1126,0.2075,1);
    }
  }
  return pass;
}

bool PATFinalState::eIDHelper(const size_t i, double dEtaIn, double dPhiIn, double full5x5_sigmaIetaIeta,
    double hOverE, double d0, double dz, double ooEmooP, double relIsoWithDBeta, int expectedMissingInnerHits) const
{
  // What follows is from Lindsay's miniAOD code PR 5014
  edm::Ptr<pat::Electron> el = daughterAsElectron(i);
  const edm::Ptr<reco::Vertex> pv = vertexObject();
  edm::Handle<reco::ConversionCollection> convs;
  edm::Handle<reco::BeamSpot> thebs;

  float pt_ = el->pt();
  
  // ID and matching
  float dEtaIn_ = el->deltaEtaSuperClusterTrackAtVtx();
  float dPhiIn_ = el->deltaPhiSuperClusterTrackAtVtx();
  float hOverE_ = el->hcalOverEcal();
  float full5x5_sigmaIetaIeta_ = el->full5x5_sigmaIetaIeta();
  // |1/E-1/p| = |1/E - EoverPinner/E| is computed below
  // The if protects against ecalEnergy == inf or zero (always
  // the case for electrons below 5 GeV in miniAOD)
  float ooEmooP_ = 0;
  if( el->ecalEnergy() == 0 ){
    printf("Electron energy is zero!\n");
    ooEmooP_ = 1e30;
  }else if( !std::isfinite(el->ecalEnergy())){
    printf("Electron energy is not finite!\n");
    ooEmooP_ = 1e30;
  }else{
    ooEmooP_ = fabs(1.0/el->ecalEnergy() - el->eSuperClusterOverP()/el->ecalEnergy() );
  }
  
  // Isolation
  reco::GsfElectron::PflowIsolationVariables pfIso = el->pfIsolationVariables();
  // Compute isolation with delta beta correction for PU
  float absiso = pfIso.sumChargedHadronPt 
    + std::max(0.0 , pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - 0.5 * pfIso.sumPUPt );
  float relIsoWithDBeta_ = absiso/pt_;
  
  // Impact parameter
  float d0_ = (-1) * el->gsfTrack()->dxy(pv->position() );
  float dz_ = el->gsfTrack()->dz( pv->position() );
  
  // Conversion rejection
  int expectedMissingInnerHits_ = el->gsfTrack()->trackerExpectedHitsInner().numberOfHits();
  //bool passConversionVeto_ = false;
  //if( thebs.isValid() && convs.isValid() ) {
  //  passConversionVeto_ = !ConversionTools::hasMatchedConversion(*el,convs,
  //   							   thebs->position());
  //}else{
  //  printf("\n\nERROR!!! conversions not found!!!\n");
  //}
  
  return (fabs(dEtaIn_) < dEtaIn\
          && fabs(dPhiIn_) < dPhiIn\
          && full5x5_sigmaIetaIeta_ < full5x5_sigmaIetaIeta\
          && hOverE_ < hOverE\
          && fabs(d0_) < d0\
          && fabs(dz_) < dz\
          && fabs(ooEmooP_) < ooEmooP\
          && relIsoWithDBeta_ < relIsoWithDBeta\
          && expectedMissingInnerHits_ < expectedMissingInnerHits);
          //&& passConversionVeto_
}
