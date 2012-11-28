#include "FinalStateAnalysis/PatTools/interface/PATPhotonPFIsolation.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#ifdef ENABLE_PAT_PROD
// this has a ton of using directives in it...
#include "EGamma/EGammaAnalysisTools/interface/PFIsolationEstimator.h"
#endif

namespace pattools {
  typedef reco::PFCandidateCollection PFCandColl;
  typedef edm::Handle<reco::VertexCollection> VtxHandle;

  PATPhotonPFIsolation::PATPhotonPFIsolation(const float cone_size):
    _cone_size(cone_size) {
#ifdef ENABLE_PAT_PROD
    _iso.reset(new PFIsolationEstimator());
    _iso->setConeSize(cone_size);
    _iso->initializePhotonIsolation(kTRUE);
#endif
  }

  PATPhotonPFIsolation::~PATPhotonPFIsolation(){}

  pfisolation PATPhotonPFIsolation::operator() (const reco::Photon* p_pho,
						const PFCandColl* p_pfs,
						reco::VertexRef r_vtx,
						VtxHandle h_vtxs) {
#ifdef ENABLE_PAT_PROD
    pfisolation the_iso;
    _iso->fGetIsolation(p_pho,p_pfs,r_vtx,h_vtxs);

    the_iso.cone_size    = _cone_size;
    the_iso.iso_chg_had  = _iso->getIsolationCharged();
    the_iso.iso_neut_had = _iso->getIsolationNeutral();
    the_iso.iso_photon   = _iso->getIsolationPhoton();
    return the_iso;
#else
    throw cms::Exception("PATPhotonPFIsolation::()")
      << "PAT dependencies not checked out, this will never work!"
      << std::endl;
#endif

  }

}
