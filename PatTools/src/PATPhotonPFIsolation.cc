#include "FinalStateAnalysis/PatTools/interface/PATPhotonPFIsolation.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

// this has a ton of using directives in it...
#include "EgammaAnalysis/ElectronTools/interface/PFIsolationEstimator.h"

namespace pattools {
  typedef reco::PFCandidateCollection PFCandColl;
  typedef edm::Handle<reco::VertexCollection> VtxHandle;

  PATPhotonPFIsolation::PATPhotonPFIsolation(const float cone_size):
    _iso(new PFIsolationEstimator()),
    _cone_size(cone_size) {
    _iso->initializePhotonIsolation(kTRUE);
    _iso->setConeSize(cone_size);
  }

  PATPhotonPFIsolation::~PATPhotonPFIsolation() {
    delete _iso;
  }

  pfisolation PATPhotonPFIsolation::operator() (const pat::Photon* p_pho,
						const PFCandColl* p_pfs,
						reco::VertexRef r_vtx,
						VtxHandle h_vtxs) {
    pfisolation the_iso;

    const reco::Photon* pRef =
      dynamic_cast<const reco::Photon*>(p_pho->originalObjectRef().get());

    _iso->fGetIsolation(pRef,p_pfs,r_vtx,h_vtxs);

    the_iso.cone_size    = _cone_size;
    the_iso.iso_chg_had  = _iso->getIsolationCharged();
    the_iso.iso_neut_had = _iso->getIsolationNeutral();
    the_iso.iso_photon   = _iso->getIsolationPhoton();

    return the_iso;
  }

}
