#include "FinalStateAnalysis/PatTools/plugins/TriggerMatcher.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

typedef MyTriggerMatcher<pat::Muon> PATMuonTriggerMatcher;
typedef MyTriggerMatcher<pat::Tau> PATTauTriggerMatcher;
typedef MyTriggerMatcher<pat::Electron> PATElectronTriggerMatcher;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonTriggerMatcher);
DEFINE_FWK_MODULE(PATElectronTriggerMatcher);
DEFINE_FWK_MODULE(PATTauTriggerMatcher);
