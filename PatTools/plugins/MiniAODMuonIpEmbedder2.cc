/** \class MiniAODMuonIpEmbedder2
 *
 * Embed the track IP w.r.t an input PV as a user float in a pat collection
 * Also embeds the 3D & 2D IP and significance
 *
 * \author Konstantinos A. Petridis, Imperial College;
 *  modified by Christian Veelken
 *  modified by Evan Friis
 *  modified by Devin Taylor (for miniAOD)
 *  modified by Tyler Ruggles (for muonBestTrack)
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

#include "DataFormats/PatCandidates/interface/Muon.h"

class MiniAODMuonIpEmbedder2 : public edm::EDProducer {
  public:
    MiniAODMuonIpEmbedder2(const edm::ParameterSet& pset);
    virtual ~MiniAODMuonIpEmbedder2(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<pat::MuonCollection> srcToken_;
    edm::EDGetTokenT<reco::VertexCollection> vtxSrcToken_;
};

MiniAODMuonIpEmbedder2::MiniAODMuonIpEmbedder2(const edm::ParameterSet& pset) {
  srcToken_ = consumes<pat::MuonCollection>(pset.getParameter<edm::InputTag>("muonSrc"));
  vtxSrcToken_ = consumes<reco::VertexCollection>(pset.getParameter<edm::InputTag>("vtxSrc"));
  produces<pat::MuonCollection>();
}

void MiniAODMuonIpEmbedder2::produce(edm::Event& evt, const edm::EventSetup& es) {

  std::unique_ptr<pat::MuonCollection> output(new pat::MuonCollection());

  edm::Handle<pat::MuonCollection> handle;
  evt.getByToken(srcToken_, handle);

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByToken(vtxSrcToken_, vertices);

  const reco::Vertex& thePV = *vertices->begin();

  for (size_t iObject = 0; iObject < handle->size(); ++iObject) {
    const pat::Muon& object = handle->at(iObject);
    double dz2 = -999;

    dz2 = object.muonBestTrack()->dz(thePV.position());

    pat::Muon newObject = object;
    newObject.addUserFloat("dz2", dz2);
    output->push_back(newObject);
  }

  evt.put(std::move(output));
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODMuonIpEmbedder2);
