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

#include "DataFormats/JetReco/interface/GenJet.h"

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
  //std::cout << "Will match to " << path << " with dR " << maxDeltaR << std::endl;
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

std::vector<double>
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


std::vector<double>
PATFinalState::getMVAMET(size_t i, size_t j ) const {
  //std::cout << "new mva mets" << std::endl;
  std::vector<double> returns;
  std::vector<double> failedV(6, -1.0);
  std::vector<pat::MET> Mets;
  Mets = evt()->MVAMETs();
  if (Mets.size() == 0) return failedV;
  else {
    double pt1 = daughter(i)->pt();
    double pt2 = daughter(j)->pt();
    double eta1 = daughter(i)->eta();
    double eta2 = daughter(j)->eta();
    double phi1 = daughter(i)->phi();
    double phi2 = daughter(j)->phi();
    double pdgId1 = daughter(i)->pdgId();
    double pdgId2 = daughter(j)->pdgId();
    //std::cout << "daughter1 pt: " << pt1 << std::endl;
    //std::cout << "daughter2 pt: " << pt2 << std::endl;
    //std::cout << daughter(i) << std::endl;
    //std::cout << daughter(j) << std::endl;
    //std::cout << "mets:" << std::endl;
    //int cnt = 0;
    for ( auto met : Mets ) {
      //std::cout << "met: "<<cnt<<std::endl;
      double ptm1 = met.userCand("lepton0")->pt();
      double ptm2 = met.userCand("lepton1")->pt();
      double etam1 = met.userCand("lepton0")->eta();
      double etam2 = met.userCand("lepton1")->eta();
      double phim1 = met.userCand("lepton0")->phi();
      double phim2 = met.userCand("lepton1")->phi();
      double pdgIdm1 = met.userCand("lepton0")->pdgId();
      double pdgIdm2 = met.userCand("lepton1")->pdgId();

      bool ptMatch = false;
      bool etaMatch = false;
      bool phiMatch = false;
      bool pdgIdMatch = false;

      if ((pt1==ptm1 && pt2==ptm2) || (pt1==ptm2&&pt2==ptm1)) ptMatch = true;
      else continue;
      if ((eta1==etam1 && eta2==etam2) || (eta1==etam2&&eta2==etam1)) etaMatch = true;
      else continue;
      if ((phi1==phim1 && phi2==phim2) || (phi1==phim2&&phi2==phim1)) phiMatch = true;
      else continue;
      if ((pdgId1==pdgIdm1 && pdgId2==pdgIdm2) || (pdgId1==pdgIdm2&&pdgId2==pdgIdm1)) pdgIdMatch = true;
      else continue;
      if (ptMatch && etaMatch && phiMatch && pdgIdMatch) {
        //std::cout << "\nEQUAL\n" << std::endl;
        //std::cout << " - MEt: " << met.pt() << std::endl;
        //std::cout << " - MEtPhi: " << met.phi() << std::endl;
        //std::cout << " - Cov00: " << met.getSignificanceMatrix()[0][0] << std::endl;
        //std::cout << " - Cov10: " << met.getSignificanceMatrix()[1][0] << std::endl;
        //std::cout << " - Cov01: " << met.getSignificanceMatrix()[0][1] << std::endl;
        //std::cout << " - Cov11: " << met.getSignificanceMatrix()[1][1] << std::endl;
        returns.push_back( met.pt() );
        returns.push_back( met.phi() );
        returns.push_back( met.getSignificanceMatrix()[0][0] );
        returns.push_back( met.getSignificanceMatrix()[1][0] );
        returns.push_back( met.getSignificanceMatrix()[0][1] );
        returns.push_back( met.getSignificanceMatrix()[1][1] );
        return returns;
      }
  
  
    }
  return failedV;
  }
}



double
PATFinalState::tauGenMatch( size_t i ) const {
    // Check that there are gen particles (MC)
    if (!event_->genParticleRefProd()) return -1;
    // Get all gen particles in the event
    const reco::GenParticleRefProd genCollectionRef = event_->genParticleRefProd();
    reco::GenParticleCollection genParticles = *genCollectionRef;

    // Find the closest gen particle to our candidate
    if ( genParticles.size() > 0 ) {
        reco::GenParticle& closest = genParticles[0];
        double closestDR = 999;
        for(size_t m = 0; m != genParticles.size(); ++m) {
          reco::GenParticle& genp = genParticles[m];
          //std::cout << " -- " << reco::deltaR( daughter(i)->p4(), genp.p4() ) << std::endl;
          double tmpDR = reco::deltaR( daughter(i)->p4(), genp.p4() );
          if ( tmpDR < closestDR ) { closest = genp; closestDR = tmpDR; }
        }
        //if (closestDR > 0.2) return 6.0;
        //std::cout << "Closest DR: " << closestDR << std::endl;
        //double dID = abs(daughter(i)->pdgId());
        double genID = abs(closest.pdgId());
        //std::cout << "Cand pdgID: " << dID << " Gen pdgID: " << genID << std::endl;
        if (genID == 11 && closest.pt() > 8 && closest.statusFlags().isPrompt() ) return 1.0;
        else if (genID == 13 && closest.pt() > 8 && closest.statusFlags().isPrompt() ) return 2.0;
        else if (genID == 11 && closest.pt() > 8 && closest.statusFlags().isDirectPromptTauDecayProduct() ) return 3.0;
        else if (genID == 13 && closest.pt() > 8 && closest.statusFlags().isDirectPromptTauDecayProduct() ) return 4.0;
        // If closest wasn't E / Mu, we need to rebuild taus and check them
        else {

          // Get rebuilt gen taus w/o neutrino energy
          std::vector<reco::Candidate::LorentzVector> genTaus = buildGenTaus();

          for ( auto vec : genTaus ) {
            double tmpDR2 = reco::deltaR( daughter(i)->p4(), vec );
            //std::cout << "DR: " << tmpDR2 << "   genTauPt: " << vec.Pt() <<std::endl;
            //std::cout << "DR: " << tmpDR2 << std::endl;
            if (tmpDR2 < 0.2) {
              //std::cout << " ~~~~~ Found Gen Tau " << std::endl;
              return 5.0;}
          }
          //std::cout << " - - - - No Gen Tau " << std::endl;
          return 6.0;

        }
    }
    return -1.0;
} 



double
PATFinalState::tauGenMatch2( size_t i ) const {
    // Check that there are gen particles (MC)
    if (!event_->genParticleRefProd()) return -1;
    // Get all gen particles in the event
    const reco::GenParticleRefProd genCollectionRef = event_->genParticleRefProd();
    reco::GenParticleCollection genParticles = *genCollectionRef;


    // Find the closest gen particle to our candidate
    if ( genParticles.size() > 0 ) {
        reco::GenParticle& closest = genParticles[0];
        double closestDR = 999;
        // The first two codes are based off of matching to true electrons/muons
        // Find the closest gen particle...
        for(size_t m = 0; m != genParticles.size(); ++m) {
            reco::GenParticle& genp = genParticles[m];
            double tmpDR = reco::deltaR( daughter(i)->p4(), genp.p4() );
            if ( tmpDR < closestDR ) { closest = genp; closestDR = tmpDR; }
        }
        double genID = abs(closest.pdgId());

        // The remaining codes are based off of matching to reconstructed tau decay products
        const std::vector<reco::GenJet> genHTaus = event_->genHadronicTaus();
        const std::vector<reco::GenJet> genETaus = event_->genElectronicTaus();
        const std::vector<reco::GenJet> genMTaus = event_->genMuonicTaus();

        // Loop over all versions of gen taus and find closest one
        double closestDR_HTau = 999;
        double closestDR_ETau = 999;
        double closestDR_MTau = 999;
        if ( genHTaus.size() > 0 ) {
            for (size_t j = 0; j != genHTaus.size(); ++j) {
                double tmpDR = reco::deltaR( daughter(i)->p4(), genHTaus[j].p4() );
                if (tmpDR < closestDR_HTau) closestDR_HTau = tmpDR;
            }
        }
        if ( genETaus.size() > 0 ) {
            for (size_t j = 0; j != genETaus.size(); ++j) {
                double tmpDR = reco::deltaR( daughter(i)->p4(), genETaus[j].p4() );
                if (tmpDR < closestDR_ETau) closestDR_ETau = tmpDR;
            }
        }
        if ( genMTaus.size() > 0 ) {
            for (size_t j = 0; j != genMTaus.size(); ++j) {
                double tmpDR = reco::deltaR( daughter(i)->p4(), genMTaus[j].p4() );
                if (tmpDR < closestDR_MTau) closestDR_MTau = tmpDR;
            }
        }

        // Now return the value based on which object is closer, the closest
        // single gen particle, or the rebuild gen taus
        // The first two codes are based off of matching to true electrons/muons
        double closestGetTau = TMath::Min(closestDR_ETau, closestDR_MTau);
        if (closestDR_HTau < closestGetTau) closestGetTau = closestDR_HTau;
        if (closestDR < closestGetTau) {
            if (genID == 11 && closest.pt() > 8 && closest.statusFlags().isPrompt() && closestDR < 0.2 ) return 1.0;
            if (genID == 13 && closest.pt() > 8 && closest.statusFlags().isPrompt() && closestDR < 0.2 ) return 2.0;
        }
        // Other codes based off of not matching previous 2 options
        // as closest gen particle, retruns based on closest rebuilt gen tau
        if (closestDR_ETau < 0.2 && closestDR_ETau < TMath::Min(closestDR_MTau, closestDR_HTau)) return 3.0;
        if (closestDR_MTau < 0.2 && closestDR_MTau < TMath::Min(closestDR_ETau, closestDR_HTau)) return 4.0;
        if (closestDR_HTau < 0.2 && closestDR_HTau < TMath::Min(closestDR_ETau, closestDR_MTau)) return 5.0;
        return 6.0; // No match, return 6 for "fake tau"
    }
    return -1.0;
} 


double
PATFinalState::tauGenMatch3( size_t i ) const {
    if (!event_->genParticleRefProd()) return -1;
    const reco::GenParticleRefProd genCollectionRef = event_->genParticleRefProd();
    reco::GenParticleCollection genParticles = *genCollectionRef;

    if ( genParticles.size() > 0 ) {
        reco::GenParticle& closest = genParticles[0];
        double closestDR = 999;
        for(size_t m = 0; m != genParticles.size(); ++m) {
            reco::GenParticle& genp = genParticles[m];
            double tmpDR = reco::deltaR( daughter(i)->p4(), genp.p4() );
            if ( tmpDR < closestDR ) { closest = genp; closestDR = tmpDR; }
        }
        double genID = abs(closest.pdgId());

            if (genID == 11 && closestDR < 0.1 ) return 1.0;
            else if (genID == 13 && closestDR < 0.1 ) return 2.0;
            else if (genID == 11 && closestDR < 0.2 ) return 11.0;
            else if (genID == 13 && closestDR < 0.2 ) return 22.0;
        return 6.0; // No match, return 6 for "fake tau"
    }
    return -1.0;
}

std::vector<double>
PATFinalState::tauGenKin( size_t i ) const {
    std::vector<double> output;
    // Check that there are gen particles (MC)
    if (!event_->genParticleRefProd()) {
        for (int i = 0; i < 4; ++i) {
            output.push_back( -10 );
        }
        return output;
    }

    // Build gen tau jets in the event
    std::vector<reco::Candidate::LorentzVector> genTaus = buildGenTaus();

    // Find closest tau jet
    double closestDR = 999;
    reco::Candidate::LorentzVector closest;
    for ( auto vec : genTaus ) {
        double tmpDR = reco::deltaR( daughter(i)->p4(), vec );
        if ( tmpDR < closestDR ) { closest = vec; closestDR = tmpDR; }
    }

    if (closestDR == 999) {
        for (int i = 0; i < 4; ++i) {
            output.push_back( -10 );
        }
    }
    else {
        output.push_back( closest.pt() );
        output.push_back( closest.eta() );
        output.push_back( closest.phi() );
        output.push_back( closestDR );
    }

    return output;
} 


std::vector<reco::Candidate::LorentzVector>
PATFinalState::buildGenTaus() const {
    bool include_leptonic = false;
    std::vector< reco::Candidate::LorentzVector > genTauJets;
    // Check that there are gen particles (MC)
    if (!event_->genParticleRefProd()) return genTauJets;
    // Get all gen particles in the event
    const reco::GenParticleRefProd genCollectionRef = event_->genParticleRefProd();
    reco::GenParticleCollection genParticles = *genCollectionRef;

    if ( genParticles.size() > 0 ) {
        for(size_t m = 0; m != genParticles.size(); ++m) {
          reco::GenParticle& genp = genParticles[m];
          size_t id = abs(genp.pdgId());
          if (id == 15) {
            //std::cout << " - pdgId: " << id << std::endl;
            bool prompt = genp.statusFlags().isPrompt();
            if (prompt) {
              //std::cout << " --- status: " << prompt << std::endl;
              //std::cout << " ----- Num of daughters: " << genp.numberOfDaughters() << std::endl;
              //std::cout << " ----- Num of mothers: " << genp.numberOfMothers() << std::endl;
              if (genp.numberOfDaughters() > 0) {
                //std::cout << " ------- Gen > 0" << std::endl;
                bool has_tau_daughter = false;
                bool has_lepton_daughter = false;
                for (unsigned j = 0; j < genp.numberOfDaughters(); ++j) {
                  if (abs(genp.daughterRef(j)->pdgId()) == 15) has_tau_daughter = true;
                  if (abs(genp.daughterRef(j)->pdgId()) == 11 || abs(genp.daughterRef(j)->pdgId()) == 13) has_lepton_daughter = true;
                }
                if (has_tau_daughter) {
                  //std::cout << "Has Tau Daughter" << std::endl;
                  continue;}
                if (has_lepton_daughter && !include_leptonic) {
                  //std::cout << "Has E/Mu Daughter" << std::endl;
                  continue;}

                reco::Candidate::LorentzVector genTau;
                for(size_t dau = 0; dau != genp.numberOfDaughters(); ++dau) {
                  size_t id_d = abs(genp.daughterRef( dau )->pdgId());
                  //if (id_d == 11 || id_d == 12 || id_d == 13 || id_d == 14 || id_d == 16) continue; //exclude neutrinos
                  if (id_d == 12 || id_d == 14 || id_d == 16) continue; //exclude neutrinos
                  genTau += genp.daughterRef( dau )->p4();
                  //std::cout << " ------- " << dau << ": " << genTau.Pt() << std::endl;
                } // daughers loop
                genTauJets.push_back( genTau );
              } // daughers > 0
            } // prompt
          } // tau ID
        } // gen Loop
        //std::cout << "Total # of Gen Taus Jets: " << genTauJets.size() << std::endl;
    }
    return genTauJets;
} 

std::vector<double>
PATFinalState::tauGenMotherKinErsatz( size_t j ) const {

    std::vector<double> output;

    // Check that there are gen particles (MC)
    if (!event_->genParticleRefProd()) {
        for (int i = 0; i < 10; ++i) output.push_back( -10 );
        return output;}
    // Get all gen particles in the event
    const reco::GenParticleRefProd genCollectionRef = event_->genParticleRefProd();
    reco::GenParticleCollection genParticles = *genCollectionRef;

    reco::Candidate::LorentzVector visVec;
    reco::Candidate::LorentzVector withInvisVec;
    if ( genParticles.size() > 0 ) {
        for(size_t m = 0; m != genParticles.size(); ++m) {
          reco::GenParticle& genp = genParticles[m];
          bool fromHardProcessFinalState = genp.fromHardProcessFinalState();
          bool isDirectHardProcessTauDecayProduct = genp.statusFlags().isDirectHardProcessTauDecayProduct();
          bool isMuon = false;
          bool isElectron = false;
          bool isNeutrino = false;
          int pdgId = fabs( genp.pdgId() );
          if (pdgId == 11) isElectron = true;
          if (pdgId == 13) isMuon = true;
          if (pdgId == 12) isNeutrino = true;
          if (pdgId == 14) isNeutrino = true;
          if (pdgId == 16) isNeutrino = true;
          if ((fromHardProcessFinalState && (isMuon || isElectron || isNeutrino)) || isDirectHardProcessTauDecayProduct) {
            withInvisVec += genp.p4();}
          if ((fromHardProcessFinalState && (isMuon || isElectron)) || (isDirectHardProcessTauDecayProduct && !isNeutrino)) {
	     if (reco::deltaR( daughter(j)->p4(), genp.p4())>0.5 )
                 visVec += genp.p4();}
        }
    }
    output.push_back( visVec.px() );
    output.push_back( visVec.py() );
    output.push_back( withInvisVec.px() );
    output.push_back( withInvisVec.py() );
    output.push_back( withInvisVec.pt() );
    output.push_back( withInvisVec.M() );
    output.push_back( withInvisVec.eta() );
    output.push_back( withInvisVec.phi() );
    return output;
}

std::vector<double>
PATFinalState::tauGenMotherKin() const {

    std::vector<double> output;

    // Check that there are gen particles (MC)
    if (!event_->genParticleRefProd()) {
        for (int i = 0; i < 10; ++i) output.push_back( -10 );
        return output;}
    // Get all gen particles in the event
    const reco::GenParticleRefProd genCollectionRef = event_->genParticleRefProd();
    reco::GenParticleCollection genParticles = *genCollectionRef;

    reco::Candidate::LorentzVector visVec;
    reco::Candidate::LorentzVector withInvisVec;

    if ( genParticles.size() > 0 ) {
        for(size_t m = 0; m != genParticles.size(); ++m) {
          reco::GenParticle& genp = genParticles[m];
          bool fromHardProcessFinalState = genp.fromHardProcessFinalState();
          bool isDirectHardProcessTauDecayProduct = genp.statusFlags().isDirectHardProcessTauDecayProduct();
          bool isMuon = false;
          bool isElectron = false;
          bool isNeutrino = false;
          int pdgId = fabs( genp.pdgId() );
          if (pdgId == 11) isElectron = true;
          if (pdgId == 13) isMuon = true;
          if (pdgId == 12) isNeutrino = true;
          if (pdgId == 14) isNeutrino = true;
          if (pdgId == 16) isNeutrino = true;
          if ((fromHardProcessFinalState && (isMuon || isElectron || isNeutrino)) || isDirectHardProcessTauDecayProduct) {
            withInvisVec += genp.p4();}
          if ((fromHardProcessFinalState && (isMuon || isElectron)) || (isDirectHardProcessTauDecayProduct && !isNeutrino)) {
            visVec += genp.p4();}
        }
    }
    output.push_back( visVec.px() );
    output.push_back( visVec.py() );
    output.push_back( withInvisVec.px() );
    output.push_back( withInvisVec.py() );
    output.push_back( withInvisVec.pt() );
    output.push_back( withInvisVec.M() );
    output.push_back( withInvisVec.eta() );
    output.push_back( withInvisVec.phi() );
    return output;
} 

std::vector<double>
PATFinalState::getTopQuarkInitialPts() const {

    std::vector<double> output;

    // Check that there are gen particles (MC)
    if (!event_->genParticleRefProd()) {
        for (int i = 0; i < 2; ++i) output.push_back( -10 );
        return output;}
    // Get all gen particles in the event
    const reco::GenParticleRefProd genCollectionRef = event_->genParticleRefProd();
    reco::GenParticleCollection genParticles = *genCollectionRef;

    // Get pt of generator top quarks
    //int cnt = 0;
    if ( genParticles.size() > 0 ) {
        for(size_t m = 0; m != genParticles.size(); ++m) {
          reco::GenParticle& genp = genParticles[m];
          int pdgId = fabs( genp.pdgId() );
          if (pdgId == 6) {
            bool fromHardProcess = genp.statusFlags().fromHardProcess();
            bool isLastCopy = genp.statusFlags().isLastCopy();
            if (fromHardProcess && isLastCopy) {
              //cnt += 1;
              output.push_back( genp.pt() );
              //std::cout << cnt << " Gen Pt: " << genp.pt() << std::endl;
            }
          }
        }
    }
    if (output.size() < 2) {
        output.push_back( -10 ); output.push_back( -10 );
    }
    return output;
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
PATFinalState::channelSpecificObjCuts( const std::string& channel ) const {
  // daughters are position ordered in FSA
  // for channel ElecTau, daughter 0 = elec
  // daughter 1 = tau
  double pt0=daughter(0)->pt();
  double pt1=daughter(1)->pt();
  if (channel == "TauTau"   && pt0 > 33 && pt1 > 33) return 1.;
  if (channel == "ElecTau"  && pt0 > 23 && pt1 > 19) return 1.;
  if (channel == "MuTau"    && pt0 > 19 && pt1 > 19) return 1.;
  if (channel == "EMu"    && pt0 + pt1 > 30) return 1.;

  // If channel isn't specificed above, return 1.
  if (channel != "TauTau" && channel != "ElecTau" && channel != "MuTau")
    return 1.;

  // Failed
  return 0.;
}

double
PATFinalState::deltaPhiToMEt(int i, const std::string& sysTag,
    const std::string& metTag) const {

  reco::Candidate::LorentzVector p1;
  if(daughterHasUserCand(i, sysTag))
          p1=daughterUserCandP4(i, sysTag);
  else  p1=daughter(i)->p4();

  double metPhi=METP4("",metTag).phi();

  return reco::deltaPhi(p1.phi(), metPhi);
}

double 
PATFinalState::twoParticleDeltaPhiToMEt(const int i, const int j, const std::string& metTag) const
{

  PATFinalStateProxy composite = subcand(i,j);
  double compositePhi = composite.get()->phi();
  double metPhi=METP4("",metTag).phi();
      
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

reco::Candidate::LorentzVector PATFinalState::METP4(const std::string& metName, const std::string& metTag, const int applyPhiCorr) const{

  //keeping this one for consistency since there is a mt formula that wanted to use PhiCorr - but it does nothing wiht it... 
  // Awaiting further developments?

  return METP4(metName,metTag);
}

reco::Candidate::LorentzVector PATFinalState::METP4(const std::string& metName, const std::string& metTag) const {
   
  reco::Candidate::LorentzVector metP4;

  if(metName=="mvamet"){  
     metP4=evt()->met("mvamet")->p4();
  } 
  else if ( met()->hasUserCand(metTag) ){ 
       metP4=met()->userCand(metTag)->p4();
  }
  else{
      if(metTag == "jres+")
        metP4 = met()->shiftedP4(pat::MET::JetResUp);
      else if(metTag == "jres-")
        metP4 = met()->shiftedP4(pat::MET::JetResDown);
      else if(metTag == "jes+")
        metP4 = met()->shiftedP4(pat::MET::JetEnUp);
      else if(metTag == "jes-")
        metP4 = met()->shiftedP4(pat::MET::JetEnDown);
      else if(metTag == "mes+")
        metP4 = met()->shiftedP4(pat::MET::MuonEnUp);
      else if(metTag == "mes-")
        metP4 = met()->shiftedP4(pat::MET::MuonEnDown);
      else if(metTag == "ees+")
        metP4 = met()->shiftedP4(pat::MET::ElectronEnUp);
      else if(metTag == "ees-")
        metP4 = met()->shiftedP4(pat::MET::ElectronEnDown);
      else if(metTag == "tes+")
        metP4 = met()->shiftedP4(pat::MET::TauEnUp);
      else if(metTag == "tes-")
        metP4 = met()->shiftedP4(pat::MET::TauEnDown);
      else if(metTag == "ues+")
        metP4 = met()->shiftedP4(pat::MET::UnclusteredEnUp);
      else if(metTag == "ues-")
        metP4 = met()->shiftedP4(pat::MET::UnclusteredEnDown);
      else if(metTag == "pes+")
        metP4 = met()->shiftedP4(pat::MET::PhotonEnUp);
      else if(metTag == "pes-")
        metP4 = met()->shiftedP4(pat::MET::PhotonEnDown);
      else if(metTag == "raw")
        metP4 = met()->uncorP4();
      else
        metP4 = met()->p4();
  } 

  //std::cout<<evt()->met4vector(metName,metTag).pt()<<"   "<<metP4.pt()<<std::endl;

  return metP4;
}

double PATFinalState::mtMET(int i, const std::string& tag,
    const std::string& metTag) const {
 
  reco::Candidate::LorentzVector p1;
  if(daughterHasUserCand(i, tag)) 
          p1=daughterUserCandP4(i, tag); 
  else  p1=daughter(i)->p4(); 

  reco::Candidate::LorentzVector metP4=METP4("",metTag);

  return fshelpers::transverseMass(p1, metP4);
}

double PATFinalState::collinearMassMET(int i, const std::string& tag1, int j, const std::string& tag2, const std::string& metTag) const {
  reco::Candidate::LorentzVector metP4,p1,p2;
 
  if(daughterHasUserCand(i, tag1))
          p1=daughterUserCandP4(i, tag1);
  else  p1=daughter(i)->p4();

  if(daughterHasUserCand(j, tag2))
          p2=daughterUserCandP4(j, tag2);
  else  p2=daughter(j)->p4();

  metP4=METP4("",metTag);

  return fshelpers::collinearMass(p1,p2, metP4);
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

double PATFinalState::jetHt(const std::string& jetCuts) const {
  std::vector<const reco::Candidate*> jets = this->vetoJets(0.0, jetCuts);
  double output = 0;
  for (size_t i = 0; i < jets.size(); ++i) {
    output += jets[i]->pt();
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

double PATFinalState::PtDiTauSyst(int i, int j) const {
  return (daughter(i)->p4() + daughter(j)->p4() + met()->p4()).Pt();
}

double PATFinalState::MtTotal(int i, int j) const {
  edm::Ptr<pat::MET> mvaMet = evt()->met("mvamet");
  double rad;
  // Check if mvaMet is available before trying to use it
  if (mvaMet.isNull()) {
    rad = (2 * daughter(i)->pt() * met()->pt()) * (1 - TMath::Cos( daughter(i)->phi() - met()->phi()));
    rad += (2 * daughter(j)->pt() * met()->pt()) * (1 - TMath::Cos( daughter(j)->phi() - met()->phi()));
    rad += (2 * daughter(i)->pt() * daughter(j)->pt()) * (1 - TMath::Cos( daughter(i)->phi() - daughter(j)->phi()));
  }
  // if MVA MET
  else {
    rad = (2 * daughter(i)->pt() * mvaMet->pt()) * (1 - TMath::Cos( daughter(i)->phi() - mvaMet->phi()));
    rad += (2 * daughter(j)->pt() * mvaMet->pt()) * (1 - TMath::Cos( daughter(j)->phi() - mvaMet->phi()));
    rad += (2 * daughter(i)->pt() * daughter(j)->pt()) * (1 - TMath::Cos( daughter(i)->phi() - daughter(j)->phi()));
  }
  return TMath::Sqrt( rad );
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

std::vector<const reco::Candidate*> PATFinalState::vetoSecondMuon(
    double dR, const std::string& filter) const {
  return getVetoOSObjects(
      daughters(),
      ptrizeCollection(evt()->muons()),
      dR, filter);
}

std::vector<const reco::Candidate*> PATFinalState::vetoSecondElectron(
    double dR, const std::string& filter) const {
  return getVetoOSObjects(
      daughters(),
      ptrizeCollection(evt()->electrons()),
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

std::vector<const reco::Candidate*> PATFinalState::vetoTracks(
    double dR, const std::string& filter) const {
  return getVetoObjects(
      daughters(),
      ptrizeCollection(evt()->packedPflow()),
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
PATFinalState::subcand(int i, const std::string&  tagi,int j, const std::string&  tagj, int x, int y, int z) const {
  std::vector<reco::CandidatePtr> output;
 
 if(daughterHasUserCand(i,tagi)){
 output.push_back(daughterUserCand(i,tagi));
 } else { output.push_back(daughterPtr(i));}
 if(daughterHasUserCand(j,tagj)){
 output.push_back(daughterUserCand(j,tagj));
 } else { output.push_back(daughterPtr(j));}

  if (x > -1)
    output.push_back(daughterPtr(x));  // not touching this, I think we only want this for the pt/eta/mass, not the internal 
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

double PATFinalState::zCompatibilityWithUserCands(const size_t i, 
                                                  const size_t j, 
                                                  const std::string& candLabel)
  const
{
  if (likeSigned(i, j))
    return 1000;

  PATFinalState::LorentzVector p4WithCands = diObjectP4WithUserCands(i, j, candLabel);

  return zCompatibility(p4WithCands);
}

double PATFinalState::closestZ(int i, const std::string& filter, std::vector<const reco::Candidate*> legs) const
{
  std::vector<const reco::Candidate*> zFirstLeg;
  zFirstLeg.push_back(daughter(i));
  int charge = daughter(i)->charge();
  std::string newfilter = filter;
  if (charge>0) {
    newfilter += "charge()<0";
  }
  else {
    newfilter += "charge()>0";
  }
  std::vector<const reco::Candidate*> zSecondLegs = getVetoObjects(
      zFirstLeg, legs, 0.0, newfilter);
  double result = 1000;
  for (size_t j=0; j<zSecondLegs.size(); j++) {
    LorentzVector totalP4 = daughter(i)->p4() + zSecondLegs.at(j)->p4();
    double temp = std::abs(totalP4.mass() - 91.1876);
    if (temp < result) result = temp;
  }
  if (zSecondLegs.size() == 0) return -999;
  return result;
}

double PATFinalState::closestZElectron(int i, const std::string& filter="") const
{
  return closestZ(i,filter,ptrizeCollection(evt()->electrons()));
}

double PATFinalState::closestZMuon(int i, const std::string& filter="") const
{
  return closestZ(i,filter,ptrizeCollection(evt()->muons()));
}

double PATFinalState::closestZTau(int i, const std::string& filter="") const
{
  return closestZ(i,filter,ptrizeCollection(evt()->taus()));
}

double PATFinalState::smallestMll(int i, const std::string& filter, std::vector<const reco::Candidate*> legs) const
{
  std::vector<const reco::Candidate*> zFirstLeg;
  zFirstLeg.push_back(daughter(i));
  int charge = daughter(i)->charge();
  std::string newfilter = filter;
  if (charge>0) {
    newfilter += "charge()<0";
  }
  else {
    newfilter += "charge()>0";
  }
  std::vector<const reco::Candidate*> zSecondLegs = getVetoObjects(
      zFirstLeg, legs, 0.0, newfilter);
  double result = 1000;
  for (size_t j=0; j<zSecondLegs.size(); j++) {
    LorentzVector totalP4 = daughter(i)->p4() + zSecondLegs.at(j)->p4();
    double temp = totalP4.mass();
    if (temp < result) result = temp;
  }
  return result;
}

double PATFinalState::smallestMee(int i, const std::string& filter="") const
{
  return smallestMll(i,filter,ptrizeCollection(evt()->electrons()));
}

double PATFinalState::smallestMmm(int i, const std::string& filter="") const
{
  return smallestMll(i,filter,ptrizeCollection(evt()->muons()));
}

double PATFinalState::smallestMtt(int i, const std::string& filter="") const
{
  return smallestMll(i,filter,ptrizeCollection(evt()->taus()));
}


VBFVariables PATFinalState::vbfVariables(const std::string& jetCuts, double dr ) const {
  std::string jetSysTag = "";
  std::vector<const reco::Candidate*> hardScatter = this->daughters();
  std::vector<const reco::Candidate*> jets = this->vetoJets(dr, jetCuts);
  //const reco::Candidate::LorentzVector& metp4 = met()->p4();
  reco::Candidate::LorentzVector metp4;
  if (jetCuts.find("jes+") != std::string::npos) {
      jetSysTag = "jes+";
      metp4 =  met()->shiftedP4(pat::MET::JetEnUp);
   }
   else if (jetCuts.find("jes-") != std::string::npos) {
      jetSysTag = "jes-";
      metp4 = met()->shiftedP4(pat::MET::JetEnDown);
   }
   else if (jetCuts.find("jres+") != std::string::npos) {
      jetSysTag = "jres+";
      metp4 = met()->shiftedP4(pat::MET::JetResUp);
   }
   else if (jetCuts.find("jres-") != std::string::npos) {
      jetSysTag = "jres-";
      metp4 = met()->shiftedP4(pat::MET::JetResDown);
   }
   else{
      metp4 = met()->p4();
   }
  // todo cache this
  return computeVBFInfo(hardScatter, metp4, jets,jetSysTag);
}

std::vector<double> PATFinalState::jetVariables(const std::string& jetCuts, double dr ) const {
  std::vector<const reco::Candidate*> hardScatter = this->daughters();
  std::vector<const reco::Candidate*> jets = this->vetoJets(dr, jetCuts);
  // todo cache this
  return computeJetInfo(jets);
}

std::vector<double> PATFinalState::trackVariables(const std::string& trackCuts, double dr ) const {
  std::vector<const reco::Candidate*> hardScatter = this->daughters();
  std::vector<const reco::Candidate*> tracks = this->vetoTracks(dr, trackCuts);
  bool has_gen=true;
  if (!event_->genParticleRefProd()) has_gen=false;
  // todo cache this
  return computeTrackInfo(tracks,evt()->packedPflow(),event_->genParticleRefProd(),has_gen);
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

const reco::GenParticleRef PATFinalState::getDaughterGenParticle(size_t i, int pdgIdToMatch, int checkCharge, int preFSR) const {
  bool charge = (bool) checkCharge;
  bool pFSR = (bool) preFSR;
  return fshelpers::getGenParticle( daughter(i), event_->genParticleRefProd(), pdgIdToMatch, charge, pFSR);
}

const reco::GenParticleRef PATFinalState::getDaughterGenParticleMotherSmart(size_t i, int pdgIdToMatch, int checkCharge) const {
  const reco::GenParticleRef genp = getDaughterGenParticle(i, pdgIdToMatch, checkCharge);
  if( genp.isAvailable() && genp.isNonnull()  )
    return fshelpers::getMotherSmart(genp, genp->pdgId());
  else
    return genp;
}


const reco::GenParticleRef PATFinalState::getDaughterGenParticleMotherSmartRef(size_t i) const {
  const reco::GenParticleRef genp = daughterAsTau(i)->genParticleRef();
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

const bool PATFinalState::comesFromHiggsRef(size_t i) const {
  const reco::GenParticleRef genp=daughterAsTau(i)->genParticleRef();
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
      return daughterAsMuon(i)->muonBestTrack()->dz(pv->position());
    }
  else if(abs(daughter(i)->pdgId()) == 15)
    {
      pat::PackedCandidate const* packedLeadTauCand = dynamic_cast<pat::PackedCandidate const*>(daughterAsTau(i)->leadChargedHadrCand().get());
      return (packedLeadTauCand->dz());
    }
  throw cms::Exception("InvalidParticle") << "FSA can only find dZ for electron, muon and tau for now" << std::endl;
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
      return daughterAsMuon(i)->muonBestTrack()->dxy(pv->position());
    }
  else if(abs(daughter(i)->pdgId()) == 15)
    {
      pat::PackedCandidate const* packedLeadTauCand = dynamic_cast<pat::PackedCandidate const*>(daughterAsTau(i)->leadChargedHadrCand().get());
      return (packedLeadTauCand->dxy());
      //return daughterAsTau(i)->dxy();
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
    return daughterAsElectron(i)->gsfTrack()->hitPattern().numberOfAllHits(reco::HitPattern::MISSING_INNER_HITS);
  std::cout << "Daughter " << i << " has null gsf track" << std::endl;
  return -1;
}

const float PATFinalState::electronClosestMuonDR(const size_t i) const
{
  float closestDR = 999;
  for(pat::MuonCollection::const_iterator iMu = evt()->muons().begin();
      iMu != evt()->muons().end(); ++iMu)
    {
      if(!( // have to pass tight muon cuts + SIP
           (iMu->isGlobalMuon() || (iMu->isTrackerMuon() && iMu->numberOfMatchedStations() > 0))
           && iMu->isPFMuon()
           && iMu->pt() > 5 
           && fabs(iMu->eta()) < 2.4
           && iMu->muonBestTrack()->dxy(evt()->pv()->position()) < 0.5
           && iMu->muonBestTrack()->dz(evt()->pv()->position()) < 1.
           && iMu->muonBestTrackType() != 2
           && fabs(iMu->dB(pat::Muon::PV3D) / iMu->edB(pat::Muon::PV3D)) < 4
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
    return daughterAsMuon(i)->globalTrack()->hitPattern().numberOfAllHits(reco::HitPattern::TRACK_HITS);
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
  for(std::vector<edm::Ptr<reco::Vertex>>::const_iterator iVtx = event_->recoVertices().begin();
      iVtx != event_->recoVertices().end(); ++iVtx)
    {
      if(fabs((*iVtx)->z() - genVZ) < genVtxPVDZ)
        return false;
    }
  // Didn't find a better one, PV must be the best
  return true;
}


// Get the invariant mass of the ith and jth jet in the event
const float PATFinalState::dijetMass(const size_t i, const size_t j) const
{
  if(evt()->jets().size() <= i || evt()->jets().size() <= j)
    return -999.;

  return (evt()->jets().at(i).p4() + evt()->jets().at(j).p4()).M();
}

PATFinalState::LorentzVector PATFinalState::daughterP4WithUserCand(const size_t i, const std::string& label) const
{
  LorentzVector out = daughter(i)->p4();

  if(daughterHasUserCand(i, label))
    out += daughterUserCandP4(i, label);

  return out;
}


PATFinalState::LorentzVector PATFinalState::diObjectP4WithUserCands(const size_t i, const size_t j, const std::string&label) const
{
  return (daughterP4WithUserCand(i, label) + daughterP4WithUserCand(j, label));
}


PATFinalState::LorentzVector PATFinalState::p4WithUserCands(const std::string& label) const
{
  LorentzVector out = LorentzVector();
  for(size_t i = 0; i < numberOfDaughters(); ++i)
    out += daughterP4WithUserCand(i, label);

  return out;
}


const float PATFinalState::ptOfDaughterUserCand(const size_t i, const std::string& label) const
{
  if(daughterHasUserCand(i, label))
    {
      reco::CandidatePtr uCand = daughterUserCand(i, label);
      return uCand->pt();
    }

  return 0.;
}


const float PATFinalState::daughterUserCandIsoContribution(const size_t i, const std::string& label) const
{
  if(daughterHasUserCand(i, label))
    {
      // muons and electrons do isolation vetos differently, and electrons 
      // do it weirdly
      float vetoCone = 0.01;
      if(daughter(i)->isElectron())
        {
          if(fabs(daughterAsElectron(i)->superCluster()->eta()) < 1.479)
            vetoCone = 0.;
          else
            vetoCone = 0.08;
        }

      reco::CandidatePtr cand = daughterUserCand(i, label);
      float dR = reco::deltaR(daughter(i)->p4(), cand->p4());
      if(dR > vetoCone && dR < 0.4)
        return cand->pt();
    }

  return 0.;
}

const float PATFinalState::l1extraIsoTauMatching(const size_t i) const
{
    BXVector<l1t::Tau> isoTaus = evt()->l1extraIsoTaus();
    //for (int i = 0; i < isoTaus.size(); ++i) {
    for ( auto isoTau : isoTaus ) {
        //std::cout << " - l1 p4: " << isoTau.p4() << std::endl;
        if (isoTau.pt() < 32) { // 32 GeV is correct value for 2017 data
            //std::cout << " --- Pt small" << std::endl;
            continue;}
        float dR = reco::deltaR(daughter(i)->p4(), isoTau.p4() );
        //std::cout << " --- dR: " << dR << std::endl;
        if (dR < 0.5) return 1;
    }

    return 0.0;
}

const float PATFinalState::l1extraIsoTauPt(const size_t i) const
{
    BXVector<l1t::Tau> isoTaus = evt()->l1extraIsoTaus();
    //for (int i = 0; i < isoTaus.size(); ++i) {
    for ( auto isoTau : isoTaus ) {
        float dR = reco::deltaR(daughter(i)->p4(), isoTau.p4() );
        //std::cout << " --- dR: " << dR << std::endl;
        if (dR < 0.5) return isoTau.pt();
    }

    return -1.0;
}


const float PATFinalState::doubleL1extraIsoTauMatching(const size_t i, const size_t j) const
{
    BXVector<l1t::Tau> isoTaus = evt()->l1extraIsoTaus();
    //for (int i = 0; i < isoTaus.size(); ++i) {
    int p1MatchCnt = 0;
    int p2MatchCnt = 0;
    int bothMatchCnt = 0;
    
    // check for matching to each tau, pay attention to objects that match
    // both taus
    for ( auto isoTau : isoTaus ) {
        //std::cout << " - l1 p4: " << isoTau.p4() << std::endl;
        if (isoTau.pt() < 32) { // 32 GeV is correct value for 2017 data
            //std::cout << " --- Pt small" << std::endl;
            continue;}
        float dR1 = reco::deltaR(daughter(i)->p4(), isoTau.p4() );
        float dR2 = reco::deltaR(daughter(j)->p4(), isoTau.p4() );
        //std::cout << " --- dR1: " << dR1 << std::endl;
        //std::cout << " --- dR2: " << dR2 << std::endl;
        if (dR1 < 0.5) p1MatchCnt += 1;
        if (dR2 < 0.5) p2MatchCnt += 1;
        if (dR1 < 0.5 && dR2 < 0.5) bothMatchCnt += 1;
    }
 
    //std::cout << "p1Match "<<p1MatchCnt<<" p2 "<<p2MatchCnt<<" both "<<bothMatchCnt<<std::endl;
    // both match different iso taus
    if (p1MatchCnt > 0 && p2MatchCnt > 0 && bothMatchCnt == 0) return 1.0;
    // both share a single iso tau, but one tau matching 2 iso objects so
    // it's okay
    else if ((p1MatchCnt + p2MatchCnt) == 3 && bothMatchCnt == 1) return 2.0;
    // This should never happen...probably
    else if ((p1MatchCnt + p2MatchCnt) == 4 && bothMatchCnt == 2) return 3.0;
   
    return 0.0;
}


const float PATFinalState::closestZMassEE(const std::string& filter="") const {
  std::vector<const reco::Candidate*> candidates = getObjectsPassingFilter(
    ptrizeCollection(evt()->electrons()), filter);

  if (candidates.size() == 0) return 999;
  float bestZmass = 999;
  float absBestZmass = 999;
  float currentZmass = 999;
  float absCurrentZmass = 999;
  // Make sure we don't calculate this unnecessairly
  int cnt1 = 0;
  for (auto cand1 : candidates) {
    int cnt2 = 0;
    for (auto cand2 : candidates) {
      if (cnt2 <= cnt1) {
        //std::cout << "Skipping: " << cnt1 << " : " << cnt2 << std::endl;
        ++cnt2;
        continue;
      }
      ++cnt2;
      //std::cout << "pre - e1: " << cand1->pt() << " e2: " <<  cand2->pt() << std::endl;
      if (cand1->pt() == cand2->pt()) continue;
      if (cand1->charge()*cand2->charge() > 0) continue;
      if (reco::deltaR(cand1->p4(), cand2->p4() ) < 0.3) continue;
      LorentzVector lorentzTmp;
      lorentzTmp += cand1->p4();
      lorentzTmp += cand2->p4();
      currentZmass = lorentzTmp.M();
      absCurrentZmass = fabs( currentZmass - 91.1876 );
      if ( absCurrentZmass < absBestZmass ) {
        absBestZmass = absCurrentZmass;
        bestZmass = currentZmass;
      }
      //std::cout << " --- mass: " << currentZmass << " abs: " << absCurrentZmass << " bestM: " << bestZmass << " absBM: " << absBestZmass << std::endl;
    }
    ++cnt1;
  }
  return bestZmass;
}


const float PATFinalState::closestZMassMM(const std::string& filter="") const {
  std::vector<const reco::Candidate*> candidates = getObjectsPassingFilter(
    ptrizeCollection(evt()->muons()), filter);

  if (candidates.size() == 0) return 999;
  float bestZmass = 999;
  float absBestZmass = 999;
  float currentZmass = 999;
  float absCurrentZmass = 999;
  // Make sure we don't calculate this unnecessairly
  int cnt1 = 0;
  for (auto cand1 : candidates) {
    int cnt2 = 0;
    for (auto cand2 : candidates) {
      if (cnt2 <= cnt1) {
        //std::cout << "Skipping: " << cnt1 << " : " << cnt2 << std::endl;
        ++cnt2;
        continue;
      }
      ++cnt2;
      //std::cout << "pre - e1: " << cand1->pt() << " e2: " <<  cand2->pt() << std::endl;
      if (cand1->pt() == cand2->pt()) continue;
      if (cand1->charge()*cand2->charge() > 0) continue;
      if (reco::deltaR(cand1->p4(), cand2->p4() ) < 0.3) continue;
      LorentzVector lorentzTmp;
      lorentzTmp += cand1->p4();
      lorentzTmp += cand2->p4();
      currentZmass = lorentzTmp.M();
      absCurrentZmass = fabs( currentZmass - 91.1876 );
      if ( absCurrentZmass < absBestZmass ) {
        absBestZmass = absCurrentZmass;
        bestZmass = currentZmass;
      }
      //std::cout << " --- mass: " << currentZmass << " abs: " << absCurrentZmass << " bestM: " << bestZmass << " absBM: " << absBestZmass << std::endl;
    }
    ++cnt1;
  }
  return bestZmass;
}



