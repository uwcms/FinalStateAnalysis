#include "FinalStateAnalysis/PatTools/plugins/PATObjectEmbedRho.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

typedef PATRhoOverloader<pat::Muon> MuonRhoOverloader;
typedef PATRhoOverloader<pat::Tau> TauRhoOverloader;
typedef PATRhoOverloader<pat::Electron> ElectronRhoOverloader;

DEFINE_FWK_MODULE(MuonRhoOverloader);
DEFINE_FWK_MODULE(ElectronRhoOverloader);
DEFINE_FWK_MODULE(TauRhoOverloader);
