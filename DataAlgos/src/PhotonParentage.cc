#include "FinalStateAnalysis/DataAlgos/interface/PhotonParentage.h"

using namespace phohelpers;

PhotonParentage::
PhotonParentage(const edm::Ref<std::vector<pat::Photon> >& pho) {
  _match = pho->genParticleRef();
  if( _match.isNonnull() && _match.isAvailable() ) {
    getParentageRecursive(_match);
    resolveParentage();
  }
}

void PhotonParentage::getParentageRecursive(const reco::GenParticleRef& p) {
  // stopping condition
  if( p->numberOfMothers() == 0 ) return;
  const int nmom = p->numberOfMothers();
  
  // only keep track of parent types we care about
  switch(std::abs(p->pdgId())) {
  case 12:
  case 14:
  case 16:
  case 22:
    break; // disregard neutrinos, photons
  case 11:
  case 13:
  case 15:
    _leptonParents.push_back(p);
    break;
  case 21:
  case 1:
  case 2:
  case 3:
  case 4:
  case 5:
  case 6:
    _qcdParents.push_back(p);
    break;
  case 23:
  case 24:
  case 25:
    _ewkBosonParents.push_back(p);
  default:
    _nonPromptParents.push_back(p);
  }

  for( int i = 0; i < nmom; ++i ) {
    reco::GenParticleRef next = p->motherRef(i);
    if( next.isAvailable() && next.isNonnull() ) {
      getParentageRecursive(next);
    }
  }
}

void PhotonParentage::resolveParentage() {
}
