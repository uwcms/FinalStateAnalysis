#include "FinalStateAnalysis/PatTools/plugins/PATFinalStateRankEmbedder.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

typedef PATRankEmbedder<pat::Muon> PATMuonRanker;
typedef PATRankEmbedder<pat::Jet> PATJetRanker;
typedef PATRankEmbedder<pat::Electron> PATElectronRanker;
typedef PATRankEmbedder<pat::Tau> PATTauRanker;
typedef PATRankEmbedder<pat::Photon> PATPhotonRanker;

DEFINE_FWK_MODULE(PATMuonRanker);
DEFINE_FWK_MODULE(PATJetRanker);
DEFINE_FWK_MODULE(PATElectronRanker);
DEFINE_FWK_MODULE(PATTauRanker);
DEFINE_FWK_MODULE(PATPhotonRanker);


