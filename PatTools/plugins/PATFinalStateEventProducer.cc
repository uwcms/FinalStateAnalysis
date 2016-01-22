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
      const edm::EDGetTokenT<T>& srcToken, const edm::Event& evt) const;

  typedef math::Error<2>::type Matrix;
  // General global quantities
  edm::EDGetTokenT<double> rhoSrcToken_;
  edm::EDGetTokenT<edm::View<reco::Vertex> > pvSrcToken_;
  edm::EDGetTokenT<edm::View<reco::Vertex> > pvBackSrcToken_;
  edm::EDGetTokenT<edm::View<reco::Vertex> > verticesSrcToken_;

  // The final tau/jet/muon etc collections in the event
  edm::EDGetTokenT<pat::ElectronCollection> electronSrcToken_;
  edm::EDGetTokenT<pat::JetCollection> jetSrcToken_;
  edm::EDGetTokenT<pat::MuonCollection> muonSrcToken_;
  edm::EDGetTokenT<pat::TauCollection> tauSrcToken_;
  edm::EDGetTokenT<pat::PhotonCollection> phoSrcToken_;

  // Information about PFLOW
  //edm::EDGetTokenT<edm::InputTag> pfSrcToken_;

  // Information about tracks
  //edm::EDGetTokenT<edm::InputTag> trackSrcToken_;
  //edm::EDGetTokenT<edm::InputTag> gsfTrackSrcToken_;

  // Information about the MET
  edm::EDGetTokenT<edm::View<pat::MET> > metSrcToken_;
  //edm::EDGetTokenT<edm::InputTag> metCovSrcToken_;

  // Trigger input
  edm::EDGetTokenT<std::vector<pat::TriggerObjectStandAlone> > trgSrcToken_;

  // PU information
  edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puInfoSrcToken_;

  // MC information
  edm::EDGetTokenT<reco::GenParticleCollection> truthSrcToken_;
  edm::ParameterSet extraWeights_;

  edm::EDGetTokenT<GenFilterInfo> generatorFilterToken_;

  // The PU scenario to use
  std::string puScenario_;

  //edm::EDGetTokenT<edm::InputTag> photonCoreSrcToken_;
  //edm::EDGetTokenT<edm::InputTag> gsfCoreSrcToken_;

  edm::EDGetTokenT<pat::PackedCandidateCollection> packedPFSrcToken_;
  //edm::EDGetTokenT<edm::InputTag> packedGenSrcToken_;

  edm::EDGetTokenT<pat::PackedTriggerPrescales> trgPrescaleSrcToken_;
  edm::EDGetTokenT<edm::TriggerResults> trgResultsSrcToken_;

  //edm::EDGetTokenT<pat::JetCollection> jetAK8SrcToken_;

  typedef std::pair<std::string, edm::EDGetTokenT<edm::View<pat::MET> > > METTokenMap;
  std::vector<METTokenMap> metCfg_;

  bool forbidMissing_;

  // initialize getterOfProducts (replacing getByType)
  edm::GetterOfProducts<LHEEventProduct> getLHEEventProduct_;
  edm::GetterOfProducts<GenEventInfoProduct> getGenEventInfoProduct_;

};

PATFinalStateEventProducer::PATFinalStateEventProducer(
                                                       const edm::ParameterSet& pset) {
  rhoSrcToken_ = consumes<double>(pset.getParameter<edm::InputTag>("rhoSrc"));
  pvSrcToken_ = consumes<edm::View<reco::Vertex> >(pset.getParameter<edm::InputTag>("pvSrc"));
  pvBackSrcToken_ = consumes<edm::View<reco::Vertex> >(pset.getParameter<edm::InputTag>("pvSrcBackup"));
  verticesSrcToken_ = consumes<edm::View<reco::Vertex> >(pset.getParameter<edm::InputTag>("verticesSrc"));

  electronSrcToken_ = consumes<pat::ElectronCollection>(pset.getParameter<edm::InputTag>("electronSrc"));
  muonSrcToken_     = consumes<pat::MuonCollection>(pset.getParameter<edm::InputTag>("muonSrc"));
  tauSrcToken_      = consumes<pat::TauCollection>(pset.getParameter<edm::InputTag>("tauSrc"));
  jetSrcToken_      = consumes<pat::JetCollection>(pset.getParameter<edm::InputTag>("jetSrc"));
  phoSrcToken_      = consumes<pat::PhotonCollection>(pset.getParameter<edm::InputTag>("phoSrc"));

  metSrcToken_ = consumes<edm::View<pat::MET> >(pset.getParameter<edm::InputTag>("metSrc"));
  trgSrcToken_ = consumes<std::vector<pat::TriggerObjectStandAlone> >(pset.getParameter<edm::InputTag>("trgSrc"));
  puInfoSrcToken_ = consumes<std::vector<PileupSummaryInfo> >(pset.getParameter<edm::InputTag>("puInfoSrc"));
  truthSrcToken_ = consumes<reco::GenParticleCollection>(pset.getParameter<edm::InputTag>("genParticleSrc"));
  extraWeights_ = pset.getParameterSet("extraWeights");
  puScenario_ = pset.getParameter<std::string>("puTag");

  forbidMissing_ = pset.exists("forbidMissing") ?
    pset.getParameter<bool>("forbidMissing") : true;

  trgResultsSrcToken_ = consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("trgResultsSrc"));

  //photonCoreSrcToken_ = consumes<edm::InputTag>(pset.getParameter<edm::InputTag>("photonCoreSrc"));
  //gsfCoreSrcToken_ = consumes<edm::InputTag>(pset.getParameter<edm::InputTag>("gsfCoreSrc"));

  packedPFSrcToken_ = consumes<pat::PackedCandidateCollection>(pset.getParameter<edm::InputTag>("packedPFSrc"));
  //packedGenSrcToken_ = consumes<edm::InputTag>(pset.getParameter<edm::InputTag>("packedGenSrc"));

  trgPrescaleSrcToken_ = consumes<pat::PackedTriggerPrescales>(pset.getParameter<edm::InputTag>("trgPrescaleSrc"));

  //jetAK8SrcToken_ = consumes<pat::JetCollection>(pset.getParameter<edm::InputTag>("jetAK8Src"));

  generatorFilterToken_ = consumes<GenFilterInfo>(edm::InputTag("generator","minVisPtFilter"));

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
PATFinalStateEventProducer::getRefProd(const edm::EDGetTokenT<T>& srcToken,
                                       const edm::Event& evt) const {
  edm::Handle<T> handle;
  evt.getByToken(srcToken, handle);
  // If we are being permissive, and the product doesn't exist,
  // emit an error and a null ref.
  if (!forbidMissing_ && !handle.isValid()) {
    edm::LogWarning("FSAEventMissingProduct") << "The FSA token is invalid.  It will be null." << std::endl;
    return edm::RefProd<T>();
  }
  return edm::RefProd<T>(handle);
}

void PATFinalStateEventProducer::produce(edm::Event& evt,
                                         const edm::EventSetup& es) {
  std::auto_ptr<PATFinalStateEventCollection> output(
                                                     new PATFinalStateEventCollection);

  edm::Handle<double> rho;
  evt.getByToken(rhoSrcToken_, rho);

  edm::Handle<edm::View<reco::Vertex> > pv;
  evt.getByToken(pvSrcToken_, pv);

  edm::Handle<edm::View<reco::Vertex> > pv_back;
  evt.getByToken(pvBackSrcToken_, pv_back);

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
  evt.getByToken(verticesSrcToken_, vertices);
  std::vector<edm::Ptr<reco::Vertex>> verticesPtr = vertices->ptrs();

  // Get refs to the objects in the event
  edm::RefProd<pat::ElectronCollection> electronRefProd =
    getRefProd<pat::ElectronCollection>(electronSrcToken_, evt);
  edm::RefProd<pat::MuonCollection> muonRefProd =
    getRefProd<pat::MuonCollection>(muonSrcToken_, evt);
  edm::RefProd<pat::JetCollection> jetRefProd =
    getRefProd<pat::JetCollection>(jetSrcToken_, evt);
  edm::RefProd<pat::PhotonCollection> phoRefProd =
    getRefProd<pat::PhotonCollection>(phoSrcToken_, evt);
  edm::RefProd<pat::TauCollection> tauRefProd =
    getRefProd<pat::TauCollection>(tauSrcToken_, evt);
  edm::RefProd<pat::PackedCandidateCollection> packedPFRefProd =
    getRefProd<pat::PackedCandidateCollection>(packedPFSrcToken_, evt);
  edm::RefProd<reco::PFCandidateCollection> pfRefProd;
  edm::RefProd<reco::TrackCollection> trackRefProd;
  edm::RefProd<reco::GsfTrackCollection> gsftrackRefProd;

  edm::Handle<edm::View<pat::MET> > met;
  evt.getByToken(metSrcToken_, met);
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
    getRefProd<std::vector<pat::TriggerObjectStandAlone> >(trgSrcToken_, evt);

  edm::Handle<pat::PackedTriggerPrescales> trigPrescale;
  edm::Handle<edm::TriggerResults> trigResults;
  evt.getByToken(trgResultsSrcToken_, trigResults);
  const edm::TriggerNames& names = evt.triggerNames(*trigResults);
  evt.getByToken(trgPrescaleSrcToken_, trigPrescale);

  edm::Handle<std::vector<PileupSummaryInfo> > puInfo;
  evt.getByToken(puInfoSrcToken_, puInfo);

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
  evt.getByToken(generatorFilterToken_,generatorFilterH);
  GenFilterInfo generatorFilter;
  if (generatorFilterH.isValid())
    generatorFilter = *generatorFilterH;
        
  // Try and get the gen information if it exists
  edm::Handle<reco::GenParticleCollection> genParticles;
  evt.getByToken(truthSrcToken_, genParticles);
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
