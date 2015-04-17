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

#include "DataFormats/TrackReco/interface/HitPattern.h"

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
  output += met()->p4();
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

  edm::Ptr<pat::MET> mvaMet = evt()->met("mvamet");

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
  return fshelpers::transverseMass(daughterUserCandP4(i, tag), metP4);
}

double PATFinalState::mtMET(int i, const std::string& metTag) const {
  return mtMET(i, "", metTag);
}

double PATFinalState::mtMET(int i, const std::string& tag,
			    const std::string& metName, const std::string& metTag, 
			    const int applyPhiCorr) const {
  return mtMET(i, tag, metTag);
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
PATFinalState::subcandfsr( int i, int j, const std::string& fsrLabel ) const
{
  std::vector<reco::CandidatePtr> output;
  output.push_back( daughterPtr(i) );
  output.push_back( daughterPtr(j) );
  
  const reco::CandidatePtr fsrPho = bestFSROfZ(i, j, fsrLabel);
  if(fsrPho.isNonnull() && fsrPho.isAvailable())
    output.push_back(fsrPho);
  return PATFinalStateProxy(new PATMultiCandFinalState(output, evt()));
}

const reco::CandidatePtr PATFinalState::bestFSROfZ(int i, int j, const std::string& fsrLabel) const
{
  bool iIsElectron = false;
  bool jIsElectron = false;

  edm::Ptr<pat::Electron> ei = daughterAsElectron(i);
  edm::Ptr<pat::Muon> mi = daughterAsMuon(i);
  if(daughter(i)->isElectron() && ei.isNonnull() && ei.isAvailable())
    {
      iIsElectron = true;
    }
  else 
    {
      if(!(daughter(i)->isMuon() && mi.isNonnull() && mi.isAvailable()))
	return reco::CandidatePtr();
    }

  edm::Ptr<pat::Electron> ej = daughterAsElectron(j);
  edm::Ptr<pat::Muon> mj = daughterAsMuon(j);
  if(daughter(j)->isElectron() && ej.isNonnull() && ej.isAvailable())
    {
      jIsElectron = true;
    }
  else 
    {
      if(!(daughter(j)->isMuon() && mj.isNonnull() && mj.isAvailable()))
	return reco::CandidatePtr();//edm::Ptr<reco::Candidate>(new const reco::Candidate());
    }

  int leptonOfBest; // index of daughter that has best FSR cand 
  int bestFSR = -1; // index of best photon as userCand
  double bestFSRPt = -1; // Pt of best photon
  double bestFSRDeltaR = 1000; // delta R between best FSR and nearest lepton
  float noFSRDist = zCompatibility(i,j); // must be better Z candidate than no FSR
  if(noFSRDist == -1000) // Same sign leptons
    return reco::CandidatePtr();
  PATFinalState::LorentzVector p4NoFSR = daughter(i)->p4() + daughter(j)->p4();

  if((iIsElectron?ei->hasUserInt("n"+fsrLabel):mi->hasUserInt("n"+fsrLabel)))
    {
      for(int ind = 0; ind < (iIsElectron?ei->userInt("n"+fsrLabel):mi->userInt("n"+fsrLabel)); ++ind)
	{
	  PATFinalState::LorentzVector fsrCandP4 = daughterUserCandP4(i, fsrLabel+std::to_string(ind));
	  PATFinalState::LorentzVector zCandP4 = p4NoFSR + fsrCandP4;
	  if(zCandP4.mass() < 4. || zCandP4.mass() > 100.) // overall mass cut
	    continue;
	  if(zCompatibility(zCandP4) > noFSRDist) // Must bring us closer to on-shell Z
	    continue;
	  // If any FSR candidate has pt > 4, pick the highest pt candidate. 
	  // Otherwise, pick the one with the smallest deltaR to its lepton.
	  if(bestFSRPt > 4. || fsrCandP4.pt() > 4.)
	    {
	      if(fsrCandP4.pt() < bestFSRPt)
		continue;
	    }
	  else if(reco::deltaR(daughter(i)->p4(), fsrCandP4) > bestFSRDeltaR)
	    continue;

	  // This one looks like the best for now
	  leptonOfBest = i;
	  bestFSR = ind;
	  bestFSRPt = fsrCandP4.pt();
	  bestFSRDeltaR = reco::deltaR(daughter(i)->p4(), fsrCandP4);
	}
    }
  if((jIsElectron?ej->hasUserInt("n"+fsrLabel):mj->hasUserInt("n"+fsrLabel)))
    {
      //      std::cout << "Found an embedded candidate in event " << evt()->evtId().event() << std::endl;
      for(int ind = 0; ind < (jIsElectron?ej->userInt("n"+fsrLabel):mj->userInt("n"+fsrLabel)); ++ind)
	{
	  PATFinalState::LorentzVector fsrCandP4 = daughterUserCandP4(j, fsrLabel+std::to_string(ind));
	  PATFinalState::LorentzVector zCandP4 = p4NoFSR + fsrCandP4;
	  if(zCandP4.mass() < 4. || zCandP4.mass() > 100.) // overall mass cut
	    continue;
	  if(zCompatibility(zCandP4) > noFSRDist) // Must bring us closer to on-shell Z
	    continue;
	  // If any FSR candidate has pt > 4, pick the highest pt candidate. 
	  // Otherwise, pick the one with the smallest deltaR to its lepton.
	  if(bestFSRPt > 4. || fsrCandP4.pt() > 4.)
	    {
	      if(fsrCandP4.pt() < bestFSRPt)
		continue;
	    }
	  else if(reco::deltaR(daughter(j)->p4(), fsrCandP4) > bestFSRDeltaR)
	    continue;

	  // This one looks like the best for now
	  leptonOfBest = j;
	  bestFSR = ind;
	  bestFSRPt = fsrCandP4.pt();
	  bestFSRDeltaR = reco::deltaR(daughter(j)->p4(), fsrCandP4);
	}
    }
  if(bestFSR != -1)
    {
      //  std::cout << "Accepted FSR cand, event " << evt()->evtId().event() << std::endl;
      return daughterUserCand(leptonOfBest, fsrLabel+std::to_string(bestFSR));
    }
  //  std::cout << "Rejected FSR cand, event " << evt()->evtId().event() << std::endl;
  return reco::CandidatePtr();//edm::Ptr<reco::Candidate>(new const reco::Candidate());
}

PATFinalState::LorentzVector
PATFinalState::p4fsr(const std::string& fsrLabel) const
{
  PATFinalStateProxy bestZ;
  int bestL1 = 0;
  int bestL2 = 1;
  
  for(int lep1 = 0; lep1 < 3; ++lep1)
    {
      for(int lep2 = lep1 + 1; lep2 <= 3; ++lep2)
        {
          PATFinalStateProxy cand = subcandfsr(lep1,lep2,fsrLabel);
          if(lep1 == 0 && lep2 == 1) // no best Z yet
    	{
    	  bestZ = cand;
    	  continue;
    	}
          
          if(zCompatibility(cand) < zCompatibility(bestZ))
    	{
    	  bestZ = cand;
    	  bestL1 = lep1;
    	  bestL2 = lep2;
    	  continue;
    	}
        }
    }

  int otherL1 = -1;
  int otherL2 = -1;
  for(int foo = 0; foo < 4; ++foo)
    {
      if(foo != bestL1 && foo != bestL2)
        {
          if(otherL1 == -1)
    	{
    	  otherL1 = foo;
    	}
          else
    	{
    	  otherL2 = foo;
    	}
        }
    }
  PATFinalStateProxy otherZ = subcandfsr(otherL1, otherL2, fsrLabel);

  return bestZ->p4() + otherZ->p4();
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

double PATFinalState::zCompatibility(int i, int j, const LorentzVector& thirdWheel) const {
  if (likeSigned(i, j)) {
    return 1000;
  }
  LorentzVector totalP4 = daughter(i)->p4() + daughter(j)->p4() + thirdWheel;
  return std::abs(totalP4.mass() - 91.1876);
}

double PATFinalState::zCompatibility(PATFinalStateProxy& cand) const
{
  if(cand->charge() != 0) // assume this will only be used for 2 leptons + photon
    return 1000;
  return std::abs(cand->mass() - 91.1876);
}

double PATFinalState::zCompatibility(const PATFinalState::LorentzVector& p4) const 
{
  // Assumes you already checked for opposite-sign-ness
  return std::abs(p4.mass() - 91.1876);
}

double PATFinalState::zCompatibilityFSR(int i, int j, const std::string fsrLabel) const
{
  PATFinalStateProxy z = subcandfsr(i, j, fsrLabel);
  return zCompatibility(z);
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

const float PATFinalState::getIP3DErr(const size_t i) const
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

const float PATFinalState::getIP2D(const size_t i) const
{
  if(abs(daughter(i)->pdgId()) == 11)
    {
      return fabs(daughterAsElectron(i)->dB(pat::Electron::PV2D));
    }
  else if (abs(daughter(i)->pdgId()) == 13)
    {
      return fabs(daughterAsMuon(i)->dB(pat::Muon::PV2D));
    }
  
  throw cms::Exception("InvalidParticle") << "FSA can only find SIP3D for electron and muon for now" << std::endl;
}

const float PATFinalState::getIP2DErr(const size_t i) const
{
  if(abs(daughter(i)->pdgId()) == 11)
    {
      return daughterAsElectron(i)->edB(pat::Electron::PV2D);
    }
  else if (abs(daughter(i)->pdgId()) == 13)
    {
      return daughterAsMuon(i)->edB(pat::Muon::PV2D);
    }
  
  throw cms::Exception("InvalidParticle") << "FSA can only find SIP2D for electron and muon for now" << std::endl;
}

const float PATFinalState::getPVDZ(const size_t i) const
{
  if(abs(daughter(i)->pdgId()) == 11)
    {
      const edm::Ptr<reco::Vertex> pv = event_->pv();
      return daughterAsElectron(i)->gsfTrack()->dz(pv->position());
    }
  else if(abs(daughter(i)->pdgId()) == 13)
    {
      const edm::Ptr<reco::Vertex> pv = event_->pv();
      return daughterAsMuon(i)->innerTrack()->dz(pv->position());
    }
  throw cms::Exception("InvalidParticle") << "FSA can only find dZ for electron and muon for now" << std::endl;
}

const float PATFinalState::getPVDXY(const size_t i) const
{
  if(abs(daughter(i)->pdgId()) == 11)
    {
      const edm::Ptr<reco::Vertex> pv = event_->pv();
      return daughterAsElectron(i)->gsfTrack()->dxy(pv->position());
    }
  else if(abs(daughter(i)->pdgId()) == 13)
    {
      const edm::Ptr<reco::Vertex> pv = event_->pv();
      return daughterAsMuon(i)->innerTrack()->dxy(pv->position());
    }
  else if(abs(daughter(i)->pdgId()) == 15)
    {
      return daughterAsTau(i)->dxy();
    }
  throw cms::Exception("InvalidParticle") << "FSA can only find dXY for electron, muon, and tau for now" << std::endl;
}

const bool PATFinalState::isTightMuon(const size_t i) const
{
  return daughterAsMuon(i)->isTightMuon(*vertexObject());
}

const int PATFinalState::getElectronMissingHits(const size_t i) const
{
  if(daughterAsElectron(i)->gsfTrack().isNonnull())
    return daughterAsElectron(i)->gsfTrack()->hitPattern().numberOfHits(reco::HitPattern::MISSING_INNER_HITS);
  std::cout << "Daughter " << i << " has null gsf track" << std::endl;
  return -1;
}

const float PATFinalState::electronClosestMuonDR(const size_t i) const
{
  float closestDR = 999;
  for(pat::MuonCollection::const_iterator iMu = evt()->muons().begin();
      iMu != evt()->muons().end(); ++iMu)
    {
      if(!( // have to pass loose muon cuts + global or PF muon
	   (iMu->isGlobalMuon() || iMu->isPFMuon())
	   && iMu->pt() > 5 
	   && fabs(iMu->eta()) < 2.4
	   && iMu->muonBestTrack()->dxy(evt()->pv()->position()) < 0.5
	   && iMu->muonBestTrack()->dz(evt()->pv()->position()) < 1.
	   ))
	continue;
      float thisDR = reco::deltaR(daughter(i)->p4(), iMu->p4());
      if(thisDR < closestDR)
	closestDR = thisDR;
    }

  return closestDR;
}

const int PATFinalState::getMuonHits(const size_t i) const
{
  if(daughterAsMuon(i)->globalTrack().isNonnull())
    return daughterAsMuon(i)->globalTrack()->hitPattern().numberOfHits(reco::HitPattern::TRACK_HITS);
  std::cout << "Daughter " << i << " has null global track" << std::endl;
  return -1;
}

const bool PATFinalState::genVtxPVMatch(const size_t i) const
{
  unsigned int pdgId = abs(daughter(i)->pdgId());
  if(!(getDaughterGenParticle(i, pdgId, 0).isAvailable() && getDaughterGenParticle(i, pdgId, 0).isNonnull()))
    return false;

  float genVZ = getDaughterGenParticle(i, pdgId, 0)->vz();
  float genVtxPVDZ = fabs(event_->pv()->z() - genVZ);

  // Loop over all vertices, and if there's one that's better, say so
  for(edm::PtrVector<reco::Vertex>::const_iterator iVtx = event_->recoVertices().begin();
      iVtx != event_->recoVertices().end(); ++iVtx)
    {
      if(fabs((*iVtx)->z() - genVZ) < genVtxPVDZ)
	return false;
    }
  // Didn't find a better one, PV must be the best
  return true;
}









