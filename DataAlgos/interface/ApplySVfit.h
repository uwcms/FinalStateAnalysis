///////////
// getSVFit mass
// based on standalone SVfit instructions
// https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#SVFit_Christian_Lorenzo_Aram_Rog
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////

#ifndef APPLYSVFIT_TO_FSA
#define APPLYSVFIT_TO_FSA

#include "TauAnalysis/CandidateTools/interface/NSVfitStandaloneAlgorithm.h"
#include "DataFormats/Provenance/interface/EventID.h"

using NSVfitStandalone::Vector;
using NSVfitStandalone::LorentzVector;
using NSVfitStandalone::MeasuredTauLepton;

namespace ApplySVfit {

  double getSVfitMass(
      std::vector<MeasuredTauLepton>,
      Vector,
      const TMatrixD&,
      unsigned int, const edm::EventID );
}

#endif // end of include guard: APPLYSVFIT_TO_FSA
