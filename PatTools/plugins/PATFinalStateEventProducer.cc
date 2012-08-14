/*
 * Produce a PATFinalStateEvent container with some interesting event info.
 *
 * */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"

#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

// For covariance matrix
#include "DataFormats/Math/interface/Error.h"


class PATFinalStateEventProducer : public edm::EDProducer {
  public:
    PATFinalStateEventProducer(const edm::ParameterSet& pset);
    virtual ~PATFinalStateEventProducer(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    typedef math::Error<2>::type Matrix;
    // General global quantities
    edm::InputTag rhoSrc_;
    edm::InputTag pvSrc_;
    edm::InputTag verticesSrc_;

    // The final tau/jet/muon etc collections in the event
    edm::InputTag electronSrc_;
    edm::InputTag jetSrc_;
    edm::InputTag muonSrc_;
    edm::InputTag tauSrc_;

    // Information about PFLOW
    edm::InputTag pfSrc_;

    // Information about tracks
    edm::InputTag trackSrc_;
    edm::InputTag gsfTrackSrc_;

    // Information about the MET
    edm::InputTag metSrc_;
    edm::InputTag metCovSrc_;

    // Trigger input
    edm::InputTag trgSrc_;

    // PU information
    edm::InputTag puInfoSrc_;

    // MC information
    edm::InputTag truthSrc_;
    edm::ParameterSet extraWeights_;
    // The PU scenario to use
    std::string puScenario_;
};

PATFinalStateEventProducer::PATFinalStateEventProducer(
    const edm::ParameterSet& pset) {
  rhoSrc_ = pset.getParameter<edm::InputTag>("rhoSrc");
  pvSrc_ = pset.getParameter<edm::InputTag>("pvSrc");
  verticesSrc_ = pset.getParameter<edm::InputTag>("verticesSrc");

  electronSrc_ = pset.getParameter<edm::InputTag>("electronSrc");
  muonSrc_ = pset.getParameter<edm::InputTag>("muonSrc");
  tauSrc_ = pset.getParameter<edm::InputTag>("tauSrc");
  jetSrc_ = pset.getParameter<edm::InputTag>("jetSrc");

  pfSrc_ = pset.getParameter<edm::InputTag>("pfSrc");

  trackSrc_ = pset.getParameter<edm::InputTag>("trackSrc");
  gsfTrackSrc_ = pset.getParameter<edm::InputTag>("gsfTrackSrc");

  metSrc_ = pset.getParameter<edm::InputTag>("metSrc");
  metCovSrc_ = pset.getParameter<edm::InputTag>("metCovSrc");
  trgSrc_ = pset.getParameter<edm::InputTag>("trgSrc");
  puInfoSrc_ = pset.getParameter<edm::InputTag>("puInfoSrc");
  truthSrc_ = pset.getParameter<edm::InputTag>("genParticleSrc");
  extraWeights_ = pset.getParameterSet("extraWeights");
  puScenario_ = pset.getParameter<std::string>("puTag");

  produces<PATFinalStateEventCollection>();
}

void PATFinalStateEventProducer::produce(edm::Event& evt,
    const edm::EventSetup& es) {
  std::auto_ptr<PATFinalStateEventCollection> output(
      new PATFinalStateEventCollection);

  edm::Handle<double> rho;
  evt.getByLabel(rhoSrc_, rho);

  edm::Handle<edm::View<reco::Vertex> > pv;
  evt.getByLabel(pvSrc_, pv);
  edm::Ptr<reco::Vertex> pvPtr = pv->ptrAt(0);

  edm::Handle<edm::View<reco::Vertex> > vertices;
  evt.getByLabel(verticesSrc_, vertices);
  edm::PtrVector<reco::Vertex> verticesPtr = vertices->ptrVector();

  // Get refs to the objects in the event
  edm::Handle<pat::ElectronCollection> electrons;
  evt.getByLabel(electronSrc_, electrons);
  edm::RefProd<pat::ElectronCollection> electronRefProd(electrons);

  edm::Handle<pat::MuonCollection> muons;
  evt.getByLabel(muonSrc_, muons);
  edm::RefProd<pat::MuonCollection> muonRefProd(muons);

  edm::Handle<pat::JetCollection> jets;
  evt.getByLabel(jetSrc_, jets);
  edm::RefProd<pat::JetCollection> jetRefProd(jets);

  edm::Handle<pat::TauCollection> taus;
  evt.getByLabel(tauSrc_, taus);
  edm::RefProd<pat::TauCollection> tauRefProd(taus);

  edm::Handle<reco::PFCandidateCollection> pf;
  evt.getByLabel(pfSrc_, pf);
  reco::PFCandidateRefProd pfRefProd(pf);

  edm::Handle<reco::TrackCollection> tracks;
  evt.getByLabel(trackSrc_, tracks);
  reco::TrackRefProd trackRefProd(tracks);

  edm::Handle<reco::GsfTrackCollection> gsftracks;
  evt.getByLabel(gsfTrackSrc_, gsftracks);
  reco::GsfTrackRefProd gsftrackRefProd(gsftracks);

  edm::Handle<edm::View<pat::MET> > met;
  evt.getByLabel(metSrc_, met);
  edm::Ptr<pat::MET> metPtr = met->ptrAt(0);

  // Get MET covariance matrix
  edm::Handle<Matrix> metCov;
  evt.getByLabel(metCovSrc_, metCov);
  // Covert to TMatrixD
  TMatrixD metCovariance(2,2);
  metCovariance(0,0) = (*metCov)(0,0);
  metCovariance(0,1) = (*metCov)(0,1);
  metCovariance(1,0) = (*metCov)(1,0);
  metCovariance(1,1) = (*metCov)(1,1);

  edm::Handle<pat::TriggerEvent> trig;
  evt.getByLabel(trgSrc_, trig);

  edm::Handle<std::vector<PileupSummaryInfo> > puInfo;
  evt.getByLabel(puInfoSrc_, puInfo);

  // Only get PU info if it exist (i.e. not for data)
  std::vector<PileupSummaryInfo> myPuInfo;
  if (puInfo.isValid())
    myPuInfo = * puInfo;

  // Try and get the Les Hoochies information
  edm::Handle<LHEEventProduct> hoochie;
  evt.getByType(hoochie);
  // Get the event tag
  lhef::HEPEUP genInfo;
  if (hoochie.isValid())
    genInfo = hoochie->hepeup();

  // Try and get the GenParticleInfo information
  edm::Handle<GenEventInfoProduct> genEventInfoH;
  evt.getByType(genEventInfoH);
  // Get the event tag
  GenEventInfoProduct genEventInfo;
  if (genEventInfoH.isValid())
    genEventInfo = *genEventInfoH;

  // Try and get the gen information if it exists
  edm::Handle<reco::GenParticleCollection> genParticles;
  evt.getByLabel(truthSrc_, genParticles);
  reco::GenParticleRefProd genParticlesRef;
  if (!evt.isRealData())
    genParticlesRef = reco::GenParticleRefProd(genParticles);

  PATFinalStateEvent theEvent(*rho, pvPtr, verticesPtr, metPtr, metCovariance,
      *trig, myPuInfo, genInfo, genParticlesRef, evt.id(), genEventInfo,
      evt.isRealData(), puScenario_,
      electronRefProd, muonRefProd, tauRefProd, jetRefProd, pfRefProd,
      trackRefProd, gsftrackRefProd);

  std::vector<std::string> extras = extraWeights_.getParameterNames();
  for (size_t i = 0; i < extras.size(); ++i) {
    if (extraWeights_.existsAs<double>(extras[i])) {
      theEvent.addWeight(extras[i],
          extraWeights_.getParameter<double>(extras[i]));
    } else {
      edm::InputTag weightSrc = extraWeights_.getParameter<edm::InputTag>(
          extras[i]);
      edm::Handle<double> weightH;
      evt.getByLabel(weightSrc, weightH);
      theEvent.addWeight(extras[i], *weightH);
    }
  }
  output->push_back(theEvent);
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateEventProducer);
