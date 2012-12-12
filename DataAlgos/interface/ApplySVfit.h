///////////
// getSVFit mass
// based on standalone SVfit instructions
// https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#SVFit_Christian_Lorenzo_Aram_Rog
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////

#ifndef APPLYSVFIT_TO_FSA
#define APPLYSVFIT_TO_FSA

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include <vector>

// forward declarations
namespace pat { class MET; }
class TMatrixD;
namespace edm { class EventID; }

namespace ApplySVfit {
  double getSVfitMass(
      std::vector<reco::CandidatePtr>& cands,
      const pat::MET& met,
      const TMatrixD& covariance,
      unsigned int verbosity,
      const edm::EventID& evtId);
}

#endif // end of include guard: APPLYSVFIT_TO_FSA
