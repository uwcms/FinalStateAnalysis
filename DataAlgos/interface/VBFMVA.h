// Original Author:  Joshua Swanson
//         Created:  Wed 16 May 2012
#ifndef VBFMVA_DCFQNAAN
#define VBFMVA_DCFQNAAN

// system include files
#include <vector>

// user include files
#include "Rtypes.h"

// Forward declarations
namespace TMVA {
  class Reader;
}

struct VBFVariables;

namespace vbf { // so we don't collide w/ UWAnalysis

  class VBFMVA  {
    public:

      void   Initialize(  std::string Weights  );
      Bool_t IsInitialized() const { return fIsInitialized; }


      double calcVBFMVA(double mjj,
          double dEta,
          double dPhi,
          double diTau_pt,
          double diJet_pt,
          double dPhi_hj,
          double C1,
          double C2);

      // Update the mva output member in the VBF vars struct.
      void applyMVA(VBFVariables& vbf);

    protected:
      Bool_t       fIsInitialized;
      TMVA::Reader      *fTMVAReader;
      std::vector<Float_t> vbfvars;

  };

}
#endif /* end of include guard: VBFMVA_DCFQNAAN */
