//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//    HZZMEProcesses.h                                                      //
//                                                                          //
//    Associates a MELA/MEKD value with the process and calculator it       //
//        represents.                                                       //
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
  out.emplace("bkg_VAMCFM", MEMPair(MEMNames::kqqZZ, MEMNames::kMCFM));

  return out;
}
