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
#include "SimDataFormats/GeneratorProducts/interface/GenFilterInfo.h"
#include "DataFormats/VertexReco/interface/Vertex.h"


#include "FWCore/Framework/interface/GetterOfProducts.h" 
#include "FWCore/Framework/interface/ProcessMatch.h"

// For covariance matrix
#include "DataFormats/Math/interface/Error.h"


class PATFinalStateEventProducer : public edm::EDProducer {
public:
  PATFinalStateEventProducer(const edm::ParameterSet& pset);
  virtual ~PATFinalStateEventProducer(){}
  void produce(edm::Event& evt, const edm::EventSetup& es);

private:

  template<typename T> edm::RefProd<T> getRefProd(
                                                  const edm::InputTag& src, const edm::Event& evt) const;

  typedef math::Error<2>::type Matrix;
  // General global quantities
  edm::InputTag rhoSrc_;
  edm::EDGetTokenT<edm::View<reco::Vertex> > pvSrc_;
  edm::EDGetTokenT<edm::View<reco::Vertex> > pvBackSrc_;
  edm::EDGetTokenT<edm::View<reco::Vertex> > verticesSrc_;

  // The final tau/jet/muon etc collections in the event
  edm::InputTag electronSrc_;
  edm::InputTag jetSrc_;
  edm::InputTag muonSrc_;
  edm::InputTag tauSrc_;
  edm::InputTag phoSrc_;

  // Information about PFLOW
  edm::InputTag pfSrc_;

  // Information about tracks
  edm::InputTag trackSrc_;
  edm::InputTag gsfTrackSrc_;

  // Information about the MET
  edm::EDGetTokenT<edm::View<pat::MET> > metSrc_;
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

  edm::InputTag photonCoreSrc_;
  edm::InputTag gsfCoreSrc_;

  edm::InputTag packedPFSrc_;
  edm::InputTag packedGenSrc_;

  edm::InputTag trgPrescaleSrc_;
  edm::InputTag trgResultsSrc_;

  edm::InputTag jetAK8Src_;

  typedef std::pair<std::string, edm::EDGetTokenT<edm::View<pat::MET> > > METTokenMap;
  std::vector<METTokenMap> metCfg_;

  bool forbidMissing_;

  // initialize getterOfProducts (replacing getByType)
  edm::GetterOfProducts<LHEEventProduct> getLHEEventProduct_;
  edm::GetterOfProducts<GenEventInfoProduct> getGenEventInfoProduct_;

};

PATFinalStateEventProducer::PATFinalStateEventProducer(
                                                       const edm::ParameterSet& pset) {
  rhoSrc_ = pset.getParameter<edm::InputTag>("rhoSrc");
  pvSrc_ = consumes<edm::View<reco::Vertex> >(pset.getParameter<edm::InputTag>("pvSrc"));
  pvBackSrc_ = consumes<edm::View<reco::Vertex> >(pset.getParameter<edm::InputTag>("pvSrcBackup"));
  verticesSrc_ = consumes<edm::View<reco::Vertex> >(pset.getParameter<edm::InputTag>("verticesSrc"));

  electronSrc_ = pset.getParameter<edm::InputTag>("electronSrc");
  muonSrc_ = pset.getParameter<edm::InputTag>("muonSrc");
  tauSrc_ = pset.getParameter<edm::InputTag>("tauSrc");
  jetSrc_ = pset.getParameter<edm::InputTag>("jetSrc");
  phoSrc_ = pset.getParameter<edm::InputTag>("phoSrc");

  metSrc_ = consumes<edm::View<pat::MET> >(pset.getParameter<edm::InputTag>("metSrc"));
  trgSrc_ = pset.getParameter<edm::InputTag>("trgSrc");
  puInfoSrc_ = pset.getParameter<edm::InputTag>("puInfoSrc");
  truthSrc_ = pset.getParameter<edm::InputTag>("genParticleSrc");
  extraWeights_ = pset.getParameterSet("extraWeights");
  puScenario_ = pset.getParameter<std::string>("puTag");

  forbidMissing_ = pset.exists("forbidMissing") ?
    pset.getParameter<bool>("forbidMissing") : true;

  trgResultsSrc_ = pset.getParameter<edm::InputTag>("trgResultsSrc");

  photonCoreSrc_ = pset.getParameter<edm::InputTag>("photonCoreSrc");
  gsfCoreSrc_ = pset.getParameter<edm::InputTag>("gsfCoreSrc");

  packedPFSrc_ = pset.getParameter<edm::InputTag>("packedPFSrc");
  packedGenSrc_ = pset.getParameter<edm::InputTag>("packedGenSrc");

  trgPrescaleSrc_ = pset.getParameter<edm::InputTag>("trgPrescaleSrc");

  jetAK8Src_ = pset.getParameter<edm::InputTag>("jetAK8Src");

  // Get different type of METs
  edm::ParameterSet mets = pset.getParameterSet("mets");
  for (size_t i = 0; i < mets.getParameterNames().size(); ++i) {
    metCfg_.push_back(
                      std::make_pair(
                                     mets.getParameterNames()[i],
                                     consumes<edm::View<pat::MET> >(mets.getParameter<edm::InputTag>(mets.getParameterNames()[i]))
                                     ));
  }

  produces<PATFinalStateEventCollection>();

  getLHEEventProduct_ = edm::GetterOfProducts<LHEEventProduct>(edm::ProcessMatch("*"), this);
  getGenEventInfoProduct_ = edm::GetterOfProducts<GenEventInfoProduct>(edm::ProcessMatch("*"), this);

  callWhenNewProductsRegistered([this](edm::BranchDescription const& bd){
      getLHEEventProduct_(bd); 
      getGenEventInfoProduct_(bd); 
    });
}

template<typename T> edm::RefProd<T>
PATFinalStateEventProducer::getRefProd(const edm::InputTag& src,
                                       const edm::Event& evt) const {
  edm::Handle<T> handle;
  evt.getByLabel(src, handle);
  // If we are being permissive, and the product doesn't exist,
  // emit an error and a null ref.
  if (!forbidMissing_ && !handle.isValid()) {
    edm::LogWarning("FSAEventMissingProduct") << "The FSA collection "
                                              << src.label() << " is missing.  It will be null." << std::endl;
    return edm::RefProd<T>();
  }
  return edm::RefProd<T>(handle);
}

void PATFinalStateEventProducer::produce(edm::Event& evt,
                                         const edm::EventSetup& es) {
  std::auto_ptr<PATFinalStateEventCollection> output(
                                                     new PATFinalStateEventCollection);

  edm::Handle<double> rho;
  evt.getByLabel(rhoSrc_, rho);

  edm::Handle<edm::View<reco::Vertex> > pv;
  evt.getByToken(pvSrc_, pv);

  edm::Handle<edm::View<reco::Vertex> > pv_back;
  evt.getByToken(pvBackSrc_, pv_back);

  edm::Ptr<reco::Vertex> pvPtr;
  if( pv->size() )
    pvPtr = pv->ptrAt(0);
  else if( pv_back->size() ) {
    // std::cout << "!!!!! There are no selected primary vertices,"
    //           << " pvPtr is set to unclean vertex !!!!!" << std::endl;
    pvPtr = pv_back->ptrAt(0);
  } // else
    // std::cout << "!!!!! There are no primary vertices,"
    //           << " pvPtr is not set !!!!!" << std::endl;
  edm::Handle<edm::View<reco::Vertex> > vertices;
  evt.getByToken(verticesSrc_, vertices);
  std::vector<edm::Ptr<reco::Vertex>> verticesPtr = vertices->ptrs();

  // Get refs to the objects in the event
  edm::RefProd<pat::ElectronCollection> electronRefProd =
    getRefProd<pat::ElectronCollection>(electronSrc_, evt);
  edm::RefProd<pat::MuonCollection> muonRefProd =
    getRefProd<pat::MuonCollection>(muonSrc_, evt);
  edm::RefProd<pat::JetCollection> jetRefProd =
    getRefProd<pat::JetCollection>(jetSrc_, evt);
  edm::RefProd<pat::PhotonCollection> phoRefProd =
    getRefProd<pat::PhotonCollection>(phoSrc_, evt);
  edm::RefProd<pat::TauCollection> tauRefProd =
    getRefProd<pat::TauCollection>(tauSrc_, evt);
  edm::RefProd<pat::PackedCandidateCollection> packedPFRefProd =
    getRefProd<pat::PackedCandidateCollection>(packedPFSrc_, evt);
  edm::RefProd<reco::PFCandidateCollection> pfRefProd;
  edm::RefProd<reco::TrackCollection> trackRefProd;
  edm::RefProd<reco::GsfTrackCollection> gsftrackRefProd;

  edm::Handle<edm::View<pat::MET> > met;
  evt.getByToken(metSrc_, met);
  edm::Ptr<pat::MET> metPtr = met->ptrAt(0);
  TMatrixD metCovariance(2,2);

  std::map<std::string, edm::Ptr<pat::MET> > theMEts;
  // Get different types of METs - this will be a map like
  // "pfmet" ->
  // "mvamet" ->
  for (size_t i = 0; i < metCfg_.size(); ++i) {
    edm::Handle<edm::View<pat::MET> > theMet;
    evt.getByToken(metCfg_[i].second, theMet);
    edm::Ptr<pat::MET> theMetPtr;
    if (!forbidMissing_ && !theMet.isValid()) {
      edm::LogWarning("FSAEventMissingProduct")
        << "The FSA collection for "
        << metCfg_[i].first
        << " is missing.  It will be null." << std::endl;
    } else {
      theMetPtr = theMet->ptrAt(0);
    }
    theMEts[metCfg_[i].first] = theMetPtr;
  }

  edm::Handle<pat::TriggerEvent> trig;

  edm::RefProd<std::vector<pat::TriggerObjectStandAlone> > trigStandAlone =
    getRefProd<std::vector<pat::TriggerObjectStandAlone> >(trgSrc_, evt);

  edm::Handle<pat::PackedTriggerPrescales> trigPrescale;
  edm::Handle<edm::TriggerResults> trigResults;
  evt.getByLabel(trgResultsSrc_, trigResults);
  const edm::TriggerNames& names = evt.triggerNames(*trigResults);
  evt.getByLabel(trgPrescaleSrc_, trigPrescale);

  edm::Handle<std::vector<PileupSummaryInfo> > puInfo;
  evt.getByLabel(puInfoSrc_, puInfo);

  // Only get PU info if it exist (i.e. not for data)
  std::vector<PileupSummaryInfo> myPuInfo;
  if (puInfo.isValid())
    myPuInfo = * puInfo;

  // Try and get the Les Hoochies information
  // replace to getterOfProducts (getByType depreciated)
  std::vector<edm::Handle<LHEEventProduct> > hoochie;
  getLHEEventProduct_.fillHandles(evt, hoochie);
  // Get the event tag
  lhef::HEPEUP genInfo;
  if (hoochie.size()) {
    if (hoochie[0].isValid()) {
      genInfo = hoochie[0]->hepeup();
    }
  }

  // Try and get the GenParticleInfo information
  // replace to getterOfProducts (getByType depreciated)
  std::vector<edm::Handle<GenEventInfoProduct> > genEventInfoH;
  getGenEventInfoProduct_.fillHandles(evt, genEventInfoH);
  // Get the event tag
  GenEventInfoProduct genEventInfo;
  if (genEventInfoH.size()) {
    if (genEventInfoH[0].isValid()) {
      genEventInfo = *genEventInfoH[0];
    }
  }

  // Try and get the GenFilterInfo information
  edm::Handle<GenFilterInfo> generatorFilterH;
  evt.getByLabel("generator","minVisPtFilter",generatorFilterH);
  GenFilterInfo generatorFilter;
  if (generatorFilterH.isValid())
    generatorFilter = *generatorFilterH;
        
  // Try and get the gen information if it exists
  edm::Handle<reco::GenParticleCollection> genParticles;
  evt.getByLabel(truthSrc_, genParticles);
  reco::GenParticleRefProd genParticlesRef;
  if (!evt.isRealData())
    genParticlesRef = reco::GenParticleRefProd(genParticles);

  pat::TriggerEvent trg;
  PATFinalStateEvent theEvent(*rho, pvPtr, verticesPtr, metPtr, metCovariance,
                              trg, trigStandAlone, names, *trigPrescale, *trigResults, myPuInfo, genInfo, genParticlesRef, 
                              evt.id(), genEventInfo, generatorFilter, evt.isRealData(), puScenario_,
                              electronRefProd, muonRefProd, tauRefProd, jetRefProd,
                              phoRefProd, pfRefProd, packedPFRefProd, trackRefProd, gsftrackRefProd, theMEts);

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
