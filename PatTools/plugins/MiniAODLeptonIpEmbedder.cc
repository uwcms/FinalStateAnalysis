/** \class MiniAODLeptonIpEmbedder
 *
 * Embed the track IP w.r.t an input PV as a user float in a pat collection
 * Also embeds the 3D & 2D IP and significance
 *
 * \author Konstantinos A. Petridis, Imperial College;
 *  modified by Christian Veelken
 *  modified by Evan Friis
 *  modified by Devin Taylor (for miniAOD)
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FinalStateAnalysis/PatTools/interface/PATLeptonTrackVectorExtractor.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "FWCore/Utilities/interface/Exception.h" 

#include <vector>

template<typename T>
class MiniAODLeptonIpEmbedder : public edm::EDProducer {
  public:
    MiniAODLeptonIpEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODLeptonIpEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<T> > srcToken_;
    edm::EDGetTokenT<reco::VertexCollection> vtxSrcToken_;
    ek::PATLeptonTrackVectorExtractor<T> trackExtractor_;
};

template<typename T>
MiniAODLeptonIpEmbedder<T>::MiniAODLeptonIpEmbedder(const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<T> >(pset.getParameter<edm::InputTag>("src"));
  vtxSrcToken_ = consumes<reco::VertexCollection>(pset.getParameter<edm::InputTag>("vtxSrc"));
  produces<std::vector<T> >();
}

template<typename T>
void MiniAODLeptonIpEmbedder<T>::produce(edm::Event& evt, const edm::EventSetup& es) {

  std::unique_ptr<std::vector<T> > output(new std::vector<T>());

  edm::Handle<edm::View<T> > handle;
  evt.getByToken(srcToken_, handle);

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByToken(vtxSrcToken_, vertices);

  const reco::Vertex& thePV = *vertices->begin();

  for (size_t iObject = 0; iObject < handle->size(); ++iObject) {
    const T& object = handle->at(iObject);
    std::vector<const reco::Track*> tracks = trackExtractor_(object);
    const reco::Track* track = tracks.size() ? tracks.at(0) : NULL;
    double ip = -1;
    double dz = -1;
    double vz = -999;
    double ip3D = -1;
    double ip3DS = -1;

    if (track) {
      ip = track->dxy(thePV.position());
      dz = track->dz(thePV.position());
      vz = track->vz();
      ip3D = fabs(object.dB(T::PV3D));
      ip3DS = fabs(object.edB(T::PV3D));
    }
    T newObject = object;
    newObject.addUserFloat("ipDXY", ip);
    newObject.addUserFloat("dz", dz);
    newObject.addUserFloat("vz", vz);
    newObject.addUserFloat("ip3D", ip3D);
    newObject.addUserFloat("ip3DS", ip3DS);
    output->push_back(newObject);
  }

  evt.put(std::move(output));
}

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

typedef MiniAODLeptonIpEmbedder<pat::Muon> MiniAODMuonIpEmbedder;
typedef MiniAODLeptonIpEmbedder<pat::Electron> MiniAODElectronIpEmbedder;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODMuonIpEmbedder);
DEFINE_FWK_MODULE(MiniAODElectronIpEmbedder);
