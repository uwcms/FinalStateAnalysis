#include "FinalStateAnalysis/PatTools/plugins/ObjectMCRematchEmbedder.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

typedef MCRematchEmbedder<pat::MuonCollection> PATMuonGenRematchEmbedder;
typedef MCRematchEmbedder<pat::TauCollection> PATTauGenRematchEmbedder;
typedef MCRematchEmbedder<pat::ElectronCollection> PATElectronGenRematchEmbedder;
typedef MCRematchEmbedder<pat::PhotonCollection> PATPhotonGenRematchEmbedder;
typedef MCRematchEmbedder<pat::JetCollection> PATJetGenRematchEmbedder;


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonGenRematchEmbedder);
DEFINE_FWK_MODULE(PATElectronGenRematchEmbedder);
DEFINE_FWK_MODULE(PATTauGenRematchEmbedder);
DEFINE_FWK_MODULE(PATPhotonGenRematchEmbedder);
DEFINE_FWK_MODULE(PATJetGenRematchEmbedder);
