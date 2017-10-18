//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//    HZZMEProcesses.h                                                      //
//                                                                          //
//    Associates a MELA/MEKD value with the process and calculator it       //
//        represents. getHZZMEProcessInfo() is for calculations that        //
//        require only the 4 leptons in the candidate,                      //
//        getHZZMEProcessInfoJets() is for calculations that also want      //
//        the two leading jets.                                             //
//                                                                          //
//    Author: Nate Woods, U. Wisconsin                                      //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////

#include <unordered_map>
#include <utility> // contains pair
#include <string>

#include "ZZMatrixElement/MEMCalculators/interface/MEMCalculators.h"

typedef std::pair<MEMNames::Processes, MEMNames::MEMCalcs> MEMPair;
typedef std::unordered_map<std::string, MEMPair> ProcessMap;

const ProcessMap getHZZMEProcessInfo()
{
  ProcessMap out = ProcessMap();

  // Define more processes here. The pair should be ordered (process, calculator).
  out.emplace("p0plus_VAJHU", MEMPair(MEMNames::kSMHiggs, MEMNames::kJHUGen));
  out.emplace("p0minus_VAJHU", MEMPair(MEMNames::k0minus, MEMNames::kJHUGen));
  out.emplace("Dgg10_VAMCFM", MEMPair(MEMNames::kggHZZ_10, MEMNames::kMCFM));
  out.emplace("bkg_VAMCFM", MEMPair(MEMNames::kqqZZ, MEMNames::kMCFM));

  return out;
}

const ProcessMap getHZZMEProcessInfoJets()
{
  ProcessMap out = ProcessMap();

  // Define more processes here. The pair should be ordered (process, calculator).
  out.emplace("phjj_VAJHU", MEMPair(MEMNames::kJJ_SMHiggs_GG, MEMNames::kJHUGen));
  out.emplace("pvbf_VAJHU", MEMPair(MEMNames::kJJ_SMHiggs_VBF, MEMNames::kJHUGen));

  return out;
}



