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

  std::cout << "Photon gen-matched to: " << _match->pdgId() << std::endl;

  auto lp = _leptonParents.cbegin();
  auto lpend = _leptonParents.cend();
  std::cout << "Lepton parents of gen-matched photon: " << std::endl;
  for( ; lp != lpend; ++lp ) {
    std::cout << (*lp)->pdgId() << ' ' 
	      << (*lp)->status() << std::endl;
  }

  auto qp = _qcdParents.cbegin();
  auto qpend = _qcdParents.cend();
  std::cout << "QCD parents of gen-matched photon: " << std::endl;
  for( ; qp != qpend; ++qp ) {
    std::cout << (*qp)->pdgId() << ' ' 
	      << (*qp)->status() << std::endl;
  }

  auto ep = _ewkBosonParents.cbegin();
  auto epend = _ewkBosonParents.cend();
  std::cout << "EWK Boson parents of gen-matched photon: " << std::endl;
  for( ; ep != epend; ++ep ) {
    std::cout << (*ep)->pdgId() << ' ' 
	      << (*ep)->status() << std::endl;
  }
  
  auto np = _nonPromptParents.cbegin();
  auto npend = _nonPromptParents.cend();
  std::cout << "Non-prompt parents of gen-matched photon: " << std::endl;
  for( ; np != epend; ++np ) {
    std::cout << (*np)->pdgId() << ' ' 
	      << (*np)->status() << std::endl;
  }
}
