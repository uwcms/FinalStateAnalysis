/** \class PATLeptonIpEmbedder
 *
 * Embed the track IP w.r.t an input PV as a user float in a pat collection
 * Also embeds the 3D & 2D IP and significance
 *
 * \author Konstantinos A. Petridis, Imperial College;
 *  modified by Christian Veelken
 *  modified by Evan Friis
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

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/IPTools/interface/IPTools.h"

#include <vector>

template<typename T>
class PATLeptonIpEmbedder : public edm::EDProducer {
  public:
    PATLeptonIpEmbedder(const edm::ParameterSet& pset);
    virtual ~PATLeptonIpEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag vtxSrc_;
    ek::PATLeptonTrackVectorExtractor<T> trackExtractor_;
};

template<typename T>
PATLeptonIpEmbedder<T>::PATLeptonIpEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  vtxSrc_ = pset.getParameter<edm::InputTag>("vtxSrc");
  produces<std::vector<T> >();
}

template<typename T>
void PATLeptonIpEmbedder<T>::produce(edm::Event& evt, const edm::EventSetup& es) {

  edm::ESHandle<TransientTrackBuilder> ttrackBuilder;
  es.get<TransientTrackRecord>().get(
      "TransientTrackBuilder", ttrackBuilder);

  std::unique_ptr<std::vector<T> > output(new std::vector<T>());

  edm::Handle<edm::View<T> > handle;
  evt.getByLabel(src_, handle);

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByLabel(vtxSrc_, vertices);

  const reco::Vertex& thePV = *vertices->begin();

  typedef std::pair<bool,Measurement1D> IPResult;

  for (size_t iObject = 0; iObject < handle->size(); ++iObject) {
    const T& object = handle->at(iObject);
    std::vector<const reco::Track*> tracks = trackExtractor_(object);
    const reco::Track* track = tracks.size() ? tracks.at(0) : NULL;
    double ip = -1;
    double dz = -1;
    double vz = -999;
    double ip3D = -1;
    double ip3DS = -1;
    double tip = -1;
    double tipS = -1;

    if (track) {
      reco::TransientTrack ttrack = ttrackBuilder->build(track);
      // Linearized functions
      ip = track->dxy(thePV.position());
      dz = track->dz(thePV.position());
      vz = track->vz();
      IPResult ip3DRes = IPTools::absoluteImpactParameter3D(ttrack, thePV);
      if (ip3DRes.first) {
        ip3D = ip3DRes.second.value();
        ip3DS = ip3DRes.second.significance();
      }
      IPResult tipRes = IPTools::absoluteTransverseImpactParameter(ttrack, thePV);
      if (tipRes.first) {
        tip = tipRes.second.value();
        tipS = tipRes.second.significance();
      }
    }
    T newObject = object;
    newObject.addUserFloat("ipDXY", ip);
    newObject.addUserFloat("dz", dz);
    newObject.addUserFloat("vz", vz);
    newObject.addUserFloat("ip3D", ip3D);
    newObject.addUserFloat("ip3DS", ip3DS);
    newObject.addUserFloat("tip", tip);
    newObject.addUserFloat("tipS", tipS);
    output->push_back(newObject);
  }

  evt.put(std::move(output));
}

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

typedef PATLeptonIpEmbedder<pat::Muon> PATMuonIpEmbedder;
typedef PATLeptonIpEmbedder<pat::Electron> PATElectronIpEmbedder;
typedef PATLeptonIpEmbedder<pat::Tau> PATTauIpEmbedder;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonIpEmbedder);
DEFINE_FWK_MODULE(PATElectronIpEmbedder);
DEFINE_FWK_MODULE(PATTauIpEmbedder);
