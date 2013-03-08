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
    break;
  default:
    _nonPromptParents.push_back(p);
  }
  
  const int nmom = p->numberOfMothers();
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
    if( lp == _leptonParents.cbegin() ) {
      _leptonParent = *lp;
    } else if( hasAsParent(_leptonParent,*lp) ) {
      _leptonParent = *lp;
    }
  }

  auto qp = _qcdParents.cbegin();
  auto qpend = _qcdParents.cend();
  std::cout << "QCD parents of gen-matched photon: " << std::endl;
  for( ; qp != qpend; ++qp ) {
    std::cout << (*qp)->pdgId() << ' ' 
	      << (*qp)->status() << std::endl;
    if( qp == _qcdParents.cbegin() ) {
      _qcdParent = *qp;
    } else if( hasAsParent(_qcdParent,*qp) ) {
      _qcdParent = *qp;
    }    
  }

  auto ep = _ewkBosonParents.cbegin();
  auto epend = _ewkBosonParents.cend();  
  std::cout << "EWK Boson parents of gen-matched photon: " << std::endl;
  for( ; ep != epend; ++ep ) {
    std::cout << (*ep)->pdgId() << ' ' 
	      << (*ep)->status() << std::endl;  
    if( ep == _ewkBosonParents.cbegin() ) {
      _ewkBosonParent = *ep;
    } else if( hasAsParent(_ewkBosonParent,*ep) ) {
      _ewkBosonParent = *ep;
    }   
  }
  
  auto np = _nonPromptParents.cbegin();
  auto npend = _nonPromptParents.cend();
  std::cout << "Non-prompt parents of gen-matched photon: " << std::endl;
  for( ; np != npend; ++np ) {
    std::cout << (*np)->pdgId() << ' ' 
	      << (*np)->status() << std::endl;
    if( np == _nonPromptParents.cbegin() ) {
      _nonPromptParent = *np;
    } else if( hasAsParent(_nonPromptParent,*np) ) {
      _nonPromptParent = *np;
    }   
  }

  std::cout << "Best parents:" << std::endl;
  if( _leptonParent.isNonnull() && _leptonParent.isAvailable() ) {
    std::cout << "Lepton Parent: " << _leptonParent->pdgId() << ' ' 
	      << _leptonParent->status() << std::endl;
  }
  if( _qcdParent.isNonnull() && _qcdParent.isAvailable() ) {
    std::cout << "QCD Parent: " << _qcdParent->pdgId() << ' ' 
	      << _qcdParent->status() << std::endl;
  }
  if( _ewkBosonParent.isNonnull() && _ewkBosonParent.isAvailable() ) {
    std::cout << "EWK Boson Parent: " << _ewkBosonParent->pdgId() << ' ' 
	      << _ewkBosonParent->status() << std::endl;
  }
  if( _nonPromptParent.isNonnull() && _nonPromptParent.isAvailable() ) {
    std::cout << "NonPrompt Parent: " << _nonPromptParent->pdgId() << ' ' 
	      << _nonPromptParent->status() << std::endl;
  }
    

}

bool PhotonParentage::hasAsParent(const reco::GenParticleRef& d,
				  const reco::GenParticleRef& pc) const {
  if( d->numberOfMothers() == 0 ) return false;
  const int nmom = d->numberOfMothers();
  bool result = false;
  for( int i = 0; i < nmom; ++i ) {
    if( pc == d->motherRef(i) ) return true;
    else {
      result += hasAsParent(d->motherRef(i),pc);
    }
  }
  return result;
}
