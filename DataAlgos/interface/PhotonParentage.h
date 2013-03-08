#ifndef __FSA_DATAALGOS_PHOTONPARENTAGE_H__
#define __FSA_DATAALGOS_PHOTONPARENTAGE_H__

#include <DataFormats/Common/interface/Ref.h>
#include <DataFormats/PatCandidates/interface/Photon.h>
#include <DataFormats/HepMCCandidate/interface/GenParticle.h>

// This class eats a pat photon. If it contains gen-matching
// information it recurses down the information until 
// the photon's provenance is determined.

namespace phohelpers {
  class PhotonParentage {
  public:
    PhotonParentage(const edm::Ref<std::vector<pat::Photon> >& );
    
    reco::GenParticleRef match() const {return _match;}
    
    reco::GenParticleRef parent() const {return _realParent;}

    bool hasQCDParent() const { return _qcdParent.isNonnull(); }
    reco::GenParticleRef getQuarkParent() const { return _qcdParent; }

    bool hasLeptonParent() const { return _leptonParent.isNonnull(); }
    reco::GenParticleRef getLeptonParent() const { return _leptonParent; }

    bool hasBosonParent()  const { return _ewkBosonParent.isNonnull(); }
    reco::GenParticleRef getBosonParent() const { return _ewkBosonParent; }

    bool hasNonPromptParent()  const { return _nonPromptParent.isNonnull(); }
    reco::GenParticleRef getNonPromptParent() const 
      { return _nonPromptParent; }

  private:    
    void getParentageRecursive(const reco::GenParticleRef&);    
    void resolveParentage();
    bool hasAsParent(const reco::GenParticleRef& daughter,
		     const reco::GenParticleRef& parent_check) const;

    reco::GenParticleRef _match;
    //niave parent is just the direct parent of this photon
    //real parent is the parent after accounting for intermediate
    //decays (taus and such)    
    reco::GenParticleRef _realParent,_leptonParent,_qcdParent,
      _ewkBosonParent,_nonPromptParent;
    std::vector<reco::GenParticleRef> _leptonParents,_qcdParents,
      _ewkBosonParents,_nonPromptParents;
  };
}

#endif
