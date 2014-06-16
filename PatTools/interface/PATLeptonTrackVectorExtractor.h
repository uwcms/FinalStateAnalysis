#ifndef FinalStateAnalysis_PatTools_PATLeptonTrackVectorExtractor_h
#define FinalStateAnalysis_PatTools_PATLeptonTrackVectorExtractor_h

/** \class PATLeptonTrackVectorExtractor
 *
 * Auxiliary class to encapsulate the different methods
 * for accessing the tracks of pat::Electrons and pat::Muons
 * and "signal" tracks of pat::Taus
 *
 * \author Christian Veelken, UC Davis
 *
 * \version $Revision: 1.1 $
 *
 * $Id: PATLeptonTrackVectorExtractor.h,v 1.1 2011/08/15 14:36:17 friis Exp $
 *
 */

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "DataFormats/Candidate/interface/Candidate.h"

// Don't conflict with tau analysis package
namespace ek {

template <typename T>
class PATLeptonTrackVectorExtractor
{
 public:
  std::vector<const reco::Track*> operator()(const T& lepton) const
  {
    assert (0);
  }
};

// add template specialization for pat::(GSF)Electrons
template <>
class PATLeptonTrackVectorExtractor<pat::Electron>
{
 public:
  std::vector<const reco::Track*> operator()(const pat::Electron& electron) const
  {
    //std::cout << "<PATLeptonTrackVectorExtractor<pat::Electron>::operator()>" << std::endl;
    std::vector<const reco::Track*> retVal;
    if ( electron.gsfTrack().isNonnull() ) retVal.push_back(electron.gsfTrack().get());
    return retVal;
  }
};

// add template specialization for pat::Muons
template <>
class PATLeptonTrackVectorExtractor<pat::Muon>
{
 public:
  std::vector<const reco::Track*> operator()(const pat::Muon& muon) const
  {
    //std::cout << "<PATLeptonTrackVectorExtractor<pat::Muon>::operator()>" << std::endl;
    std::vector<const reco::Track*> retVal;
    if ( muon.track().isNonnull() ) retVal.push_back(muon.track().get());
    return retVal;
  }
};

// add template specialization for pat::Taus
template <>
class PATLeptonTrackVectorExtractor<pat::Tau>
{
 public:
  std::vector<const reco::Track*> operator()(const pat::Tau& tau) const
  {
    //std::cout << "<PATLeptonTrackVectorExtractor<pat::Tau>::operator()>" << std::endl;
    std::vector<const reco::Track*> retVal;
    const std::vector<reco::PFCandidatePtr>& pfChargedHadrons = tau.signalPFChargedHadrCands();
    for ( std::vector<reco::PFCandidatePtr>::const_iterator pfChargedHadronPtr = pfChargedHadrons.begin();
        pfChargedHadronPtr != pfChargedHadrons.end(); ++pfChargedHadronPtr ) {
      if ( (*pfChargedHadronPtr)->trackRef().isNonnull() ) {
        retVal.push_back((*pfChargedHadronPtr)->trackRef().get());
      } else if ( (*pfChargedHadronPtr)->gsfTrackRef().isNonnull() ) {
        retVal.push_back((*pfChargedHadronPtr)->gsfTrackRef().get());
      }
    }
    return retVal;
  }
};

}

#endif
