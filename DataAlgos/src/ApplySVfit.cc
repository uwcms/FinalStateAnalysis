///////////
// imp of function getSVfitMass
// based on standalone SVfit instructions
// https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#SVFit_Christian_Lorenzo_Aram_Rog
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////


#include "DataFormats/Provenance/interface/EventID.h"
#include "FinalStateAnalysis/DataAlgos/interface/ApplySVfit.h"
#include "TauAnalysis/CandidateTools/interface/NSVfitStandaloneAlgorithm.h"
#include "TLorentzVector.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"
#include <iostream>
#include <iomanip>
#include <map>
#include <stdio.h>
#include <string>


namespace ApplySVfit {

  using NSVfitStandalone::Vector;
  using NSVfitStandalone::LorentzVector;
  using NSVfitStandalone::MeasuredTauLepton;

  // Caching and translation layer
  typedef std::map<size_t, double> SVFitCache;
  static SVFitCache theCache;
  static edm::EventID lastSVfitEvent; // last processed event

  double getSVfitMass(std::vector<reco::CandidatePtr>& cands,
      const pat::MET& met, const TMatrixD& covMET, unsigned int verbosity,
      const edm::EventID& evtId) {

    // Check if this a new event
    if (evtId != lastSVfitEvent) {
      theCache.clear();
    }
    lastSVfitEvent = evtId;

    // Hash our candidates - NB cands will be sorted in place
    size_t hash = hashCandsByContent(cands);

    // Check if we've already computed it
    SVFitCache::const_iterator lookup = theCache.find(hash);
    if (lookup != theCache.end()) {
      return lookup->second;
    }

    // No pain no gain
    Vector measuredMET = met.momentum();
    std::vector<MeasuredTauLepton> measuredTauLeptons;

    for (size_t dau = 0; dau < cands.size(); ++dau) {
      int pdgId = std::abs(cands[dau]->pdgId());
      if (pdgId == 11 || pdgId == 13)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(NSVfitStandalone::kLepDecay,cands[dau]->p4()));
      else if (pdgId == 15)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(NSVfitStandalone::kHadDecay,cands[dau]->p4()));
      else
        throw cms::Exception("BadPdgId") << "I don't understand PDG id: "
          << pdgId << ", sorry." << std::endl;
    }

    NSVfitStandaloneAlgorithm algo(measuredTauLeptons,
        measuredMET, covMET, verbosity);
    algo.addLogM(false);
    algo.integrate();
    double mass = algo.getMass(); // mass uncertainty not implemented yet

    theCache[hash] = mass;
    return mass;
  }

} // namespace ApplySVfit
