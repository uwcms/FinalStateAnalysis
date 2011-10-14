#include "FinalStateAnalysis/PatTools/interface/PATMuonIdSelector.h"
#include "CommonTools/UtilAlgos/interface/ObjectSelector.h"

typedef ObjectSelector<PATMuonIdSelectorImp> PATMuonIdSelector;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonIdSelector);
