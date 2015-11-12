///////////
// getSVFit mass
// based on standalone SVfit instructions
// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#SVfit
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////

#ifndef APPLYSVFITLFV_TO_FSA
#define APPLYSVFITLFV_TO_FSA

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include <vector>
#include "TMatrixDfwd.h"
#include "Math/SMatrixDfwd.h"

// forward declarations
namespace pat { class MET; }
namespace edm { class EventID; }

namespace ApplySVfitLFV {
  double getSVfitMassLFV(
      std::vector<reco::CandidatePtr>& cands,
      const pat::MET& met,
      const ROOT::Math::SMatrix2D& covariance, 
      unsigned int verbosity,
      const edm::EventID& evtId, bool mutau);

  // Needed to ensure compatibility with CMSSW_7_2+
  TMatrixD convert_matrix(const ROOT::Math::SMatrix2D& mat);
  TMatrixD convert_matrix(const TMatrixD& mat); 
}

#endif // end of include guard: APPLYSVFIT_TO_FSA
