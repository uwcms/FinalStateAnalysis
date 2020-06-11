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
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/L1Trigger/interface/BXVector.h"
#include "DataFormats/L1Trigger/interface/Tau.h"


#include "FWCore/Framework/interface/GetterOfProducts.h" 
#include "FWCore/Framework/interface/ProcessMatch.h"

// For covariance matrix
#include "DataFormats/Math/interface/Error.h"

// For Rivet Tools
#include "SimDataFormats/HTXS/interface/HiggsTemplateCrossSections.h"

#define DEBUG_ 0 
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

  edm::EDGetTokenT< double > prefweight_token;
  edm::EDGetTokenT< double > prefweightup_token;
  edm::EDGetTokenT< double > prefweightdown_token;

  // The final tau/jet/muon etc collections in the event
  edm::EDGetTokenT<pat::ElectronCollection> electronSrcToken_;
  edm::EDGetTokenT<pat::JetCollection> jetSrcToken_;
  edm::EDGetTokenT<pat::MuonCollection> muonSrcToken_;
  edm::EDGetTokenT<pat::TauCollection> tauSrcToken_;
  edm::EDGetTokenT<pat::PhotonCollection> phoSrcToken_;

  edm::EDGetTokenT<LHEEventProduct> lheToken_;

  // Information about PFLOW
  //edm::EDGetTokenT<edm::InputTag> pfSrcToken_;

  // Information about tracks
  //edm::EDGetTokenT<edm::InputTag> trackSrcToken_;
  //edm::EDGetTokenT<edm::InputTag> gsfTrackSrcToken_;

  // Information about the MET
  edm::EDGetTokenT<edm::View<pat::MET> > metSrcToken_;
  edm::EDGetTokenT<std::vector<pat::MET> > MVAMETSrcToken_;
  edm::EDGetTokenT<Matrix> metCovSrcToken_;
  edm::EDGetTokenT<double> metSigSrcToken_;

  // Trigger input
  edm::EDGetTokenT<std::vector<pat::TriggerObjectStandAlone> > trgSrcToken_;

  // PU information
  edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puInfoSrcToken_;

  // MC information
  edm::EDGetTokenT<reco::GenParticleCollection> truthSrcToken_;
  edm::EDGetTokenT<reco::GenJetCollection> dressedSrcToken_;
  edm::EDGetTokenT<reco::METCollection> rivetmetSrcToken_;
  edm::EDGetTokenT<std::vector<reco::GenJet>> genHadronicTausToken_;
  edm::EDGetTokenT<std::vector<reco::GenJet>> genElectronicTausToken_;
  edm::EDGetTokenT<std::vector<reco::GenJet>> genMuonicTausToken_;
  edm::ParameterSet extraWeights_;

  edm::EDGetTokenT<GenFilterInfo> generatorFilterToken_;

  // The PU scenario to use
  std::string puScenario_;

  //edm::EDGetTokenT<edm::InputTag> photonCoreSrcToken_;
  //edm::EDGetTokenT<edm::InputTag> gsfCoreSrcToken_;

  edm::EDGetTokenT<std::map<std::string, bool>> filterFlagsToken_;

  edm::EDGetTokenT<pat::PackedCandidateCollection> packedPFSrcToken_;
  //edm::EDGetTokenT<edm::InputTag> packedGenSrcToken_;

  edm::EDGetTokenT<pat::PackedTriggerPrescales> trgPrescaleSrcToken_;
  edm::EDGetTokenT<edm::TriggerResults> trgResultsSrcToken_;
  edm::EDGetTokenT<edm::TriggerResults> trgResultsSrc2Token_;
  edm::EDGetTokenT< BXVector<l1t::Tau> > l1extraIsoTauSrcToken_;

  //edm::EDGetTokenT<pat::JetCollection> jetAK8SrcToken_;

  edm::EDGetTokenT<HTXS::HiggsClassification> htxsSrc_;

  typedef std::pair<std::string, edm::EDGetTokenT<edm::View<pat::MET> > > METTokenMap;
  std::vector<METTokenMap> metCfg_;

  bool forbidMissing_;

  bool isEmbedded_;

  // initialize getterOfProducts (replacing getByType)
  edm::GetterOfProducts<LHEEventProduct> getLHEEventProduct_;
  edm::GetterOfProducts<GenEventInfoProduct> getGenEventInfoProduct_;

  edm::InputTag triggersource;

};

PATFinalStateEventProducer::PATFinalStateEventProducer(
                                                       const edm::ParameterSet& pset) {
  rhoSrcToken_ = consumes<double>(pset.getParameter<edm::InputTag>("rhoSrc"));
  pvSrcToken_ = consumes<edm::View<reco::Vertex> >(pset.getParameter<edm::InputTag>("pvSrc"));
  pvBackSrcToken_ = consumes<edm::View<reco::Vertex> >(pset.getParameter<edm::InputTag>("pvSrcBackup"));
  verticesSrcToken_ = consumes<edm::View<reco::Vertex> >(pset.getParameter<edm::InputTag>("verticesSrc"));

  prefweight_token = consumes< double >(pset.getParameter<edm::InputTag>("prefiringSrc"));
  prefweightup_token = consumes< double >(pset.getParameter<edm::InputTag>("prefiringUpSrc"));
  prefweightdown_token = consumes< double >(pset.getParameter<edm::InputTag>("prefiringDownSrc"));

  electronSrcToken_ = consumes<pat::ElectronCollection>(pset.getParameter<edm::InputTag>("electronSrc"));
  muonSrcToken_     = consumes<pat::MuonCollection>(pset.getParameter<edm::InputTag>("muonSrc"));
  tauSrcToken_      = consumes<pat::TauCollection>(pset.getParameter<edm::InputTag>("tauSrc"));
  jetSrcToken_      = consumes<pat::JetCollection>(pset.getParameter<edm::InputTag>("jetSrc"));
  phoSrcToken_      = consumes<pat::PhotonCollection>(pset.getParameter<edm::InputTag>("phoSrc"));

  metSrcToken_ = consumes<edm::View<pat::MET> >(pset.getParameter<edm::InputTag>("metSrc"));
  MVAMETSrcToken_ = consumes<std::vector<pat::MET> >(pset.getParameter<edm::InputTag>("MVAMETSrc"));
  metCovSrcToken_ = consumes< Matrix >(pset.getParameter<edm::InputTag>("metCovarianceSrc"));
  metSigSrcToken_ = consumes< double >(pset.getParameter<edm::InputTag>("metSignificanceSrc"));
  trgSrcToken_ = consumes<std::vector<pat::TriggerObjectStandAlone> >(pset.getParameter<edm::InputTag>("trgSrc"));
  puInfoSrcToken_ = consumes<std::vector<PileupSummaryInfo> >(pset.getParameter<edm::InputTag>("puInfoSrc"));
  truthSrcToken_ = consumes<reco::GenParticleCollection>(pset.getParameter<edm::InputTag>("genParticleSrc"));
  dressedSrcToken_ = consumes<reco::GenJetCollection>(pset.getParameter<edm::InputTag>("dressedParticleSrc"));
  rivetmetSrcToken_ = consumes<reco::METCollection>(pset.getParameter<edm::InputTag>("rivetmetParticleSrc"));
  genHadronicTausToken_ = consumes<std::vector<reco::GenJet>>(pset.getParameter<edm::InputTag>("tauHadronicSrc")),
  genElectronicTausToken_ = consumes<std::vector<reco::GenJet>>(pset.getParameter<edm::InputTag>("tauElectronicSrc")),
  genMuonicTausToken_ = consumes<std::vector<reco::GenJet>>(pset.getParameter<edm::InputTag>("tauMuonicSrc")),
  extraWeights_ = pset.getParameterSet("extraWeights");
  puScenario_ = pset.getParameter<std::string>("puTag");

  triggersource=pset.getParameter<edm::InputTag>("trgSrc");

  forbidMissing_ = pset.exists("forbidMissing") ?
    pset.getParameter<bool>("forbidMissing") : true;
  isEmbedded_ = pset.getParameter<bool>("isEmbedded");

  trgResultsSrcToken_ = consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("trgResultsSrc"));
						      trgResultsSrc2Token_ = consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("trgResultsSrc2"));
  l1extraIsoTauSrcToken_ = consumes< BXVector<l1t::Tau> >(pset.getParameter<edm::InputTag>("l1extraIsoTauSrc"));
  htxsSrc_ = consumes<HTXS::HiggsClassification>(edm::InputTag("rivetProducerHTXS","HiggsClassification"));

  //photonCoreSrcToken_ = consumes<edm::InputTag>(pset.getParameter<edm::InputTag>("photonCoreSrc"));
  //gsfCoreSrcToken_ = consumes<edm::InputTag>(pset.getParameter<edm::InputTag>("gsfCoreSrc"));
  filterFlagsToken_ = consumes<std::map<std::string, bool>>(pset.getParameter<edm::InputTag>("filterFlagsSrc"));


  packedPFSrcToken_ = consumes<pat::PackedCandidateCollection>(pset.getParameter<edm::InputTag>("packedPFSrc"));
  //packedGenSrcToken_ = consumes<edm::InputTag>(pset.getParameter<edm::InputTag>("packedGenSrc"));

  trgPrescaleSrcToken_ = consumes<pat::PackedTriggerPrescales>(pset.getParameter<edm::InputTag>("trgPrescaleSrc"));

  //jetAK8SrcToken_ = consumes<pat::JetCollection>(pset.getParameter<edm::InputTag>("jetAK8Src"));

  generatorFilterToken_ = consumes<GenFilterInfo>(edm::InputTag("generator","minVisPtFilter"));
  lheToken_ = consumes<LHEEventProduct>(edm::InputTag("externalLHEProducer"));

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
  std::unique_ptr<PATFinalStateEventCollection> output(
                                                     new PATFinalStateEventCollection);

  edm::Handle<double> rho;
  evt.getByToken(rhoSrcToken_, rho);

  edm::Handle<edm::View<reco::Vertex> > pv;
  evt.getByToken(pvSrcToken_, pv);

  edm::Handle<edm::View<reco::Vertex> > pv_back;
  evt.getByToken(pvBackSrcToken_, pv_back);

  // Only get LHEEventProduct info if it exist
  edm::Handle<LHEEventProduct> EvtHandle ;
  evt.getByLabel("externalLHEProducer", EvtHandle) ;
  std::vector<float> lheweights;
  if (EvtHandle.isValid()) {
    for (unsigned int i=0; i<EvtHandle->weights().size(); i++) {
       lheweights.push_back(EvtHandle->weights()[i].wgt/EvtHandle->originalXWGTUP()); 
       //std::cout<<i<<" "<<EvtHandle->weights()[i].id<<" "<<EvtHandle->weights()[i].wgt<<" "<<EvtHandle->originalXWGTUP()<<std::endl;
    };
  }

  edm::Handle< double > theprefweight;
  evt.getByToken(prefweight_token, theprefweight ) ;
  edm::Handle< double > theprefweightup;
  evt.getByToken(prefweightup_token, theprefweightup ) ;
  edm::Handle< double > theprefweightdown;
  evt.getByToken(prefweightdown_token, theprefweightdown ) ;

  std::vector<float> prefiringweights;
  prefiringweights.push_back(*theprefweight);
  prefiringweights.push_back(*theprefweightup);
  prefiringweights.push_back(*theprefweightdown);


  int npNLO=-1;
  if (EvtHandle.isValid()) {
     npNLO=EvtHandle->npNLO();
  }

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

  // Only get new pairwise Mva Met info if it exist
  edm::Handle<std::vector<pat::MET> > MVAMETs;
  evt.getByToken(MVAMETSrcToken_, MVAMETs);
  std::vector<pat::MET> MVAMETInfo;
  if (MVAMETs.isValid()) {
    MVAMETInfo = * MVAMETs;}
  // MET Significance
  edm::Handle<double> metSigHandle;
  evt.getByToken(metSigSrcToken_, metSigHandle);
  double metSig = -999.;
  if (metSigHandle.isValid()) {
   metSig = * metSigHandle;}
  // MET Covariance
  edm::Handle<Matrix> metCovHandle;
  evt.getByToken(metCovSrcToken_, metCovHandle);
  Matrix metCov;
  if (metCovHandle.isValid()) {
    metCov = * metCovHandle;}

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
  //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " trgSrcToken " << triggersource << std::endl;
  edm::RefProd<std::vector<pat::TriggerObjectStandAlone> > trigStandAlone =
    getRefProd<std::vector<pat::TriggerObjectStandAlone> >(trgSrcToken_, evt);
  //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " refProd of trigger  " <<  trigStandAlone.isNonnull() << std::endl;

  edm::Handle<pat::PackedTriggerPrescales> trigPrescale;
  edm::Handle<edm::TriggerResults> trigResults;
  
  evt.getByToken(trgResultsSrcToken_, trigResults);

  if (!trigResults.isValid()){
    evt.getByToken(trgResultsSrc2Token_, trigResults);
    if (!trigResults.isValid()){
      throw edm::Exception(edm::errors::ProductNotFound) << " could not find any HLTResult collection \n";
	return;
    }
  }
  const edm::TriggerNames& names = evt.triggerNames(*trigResults);
  evt.getByToken(trgPrescaleSrcToken_, trigPrescale);

  for (unsigned int index = 0 ; index<trigResults.product()->size(); index++){
    if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " index " << index << " "<< names.triggerName(index) << ", prescale "<< trigPrescale.product()->getPrescaleForIndex(index)<< std::endl; 
  }

  edm::Handle< BXVector<l1t::Tau> > l1extraIsoTaus;
  evt.getByToken(l1extraIsoTauSrcToken_, l1extraIsoTaus);

  edm::Handle<HTXS::HiggsClassification> htxs;
  evt.getByToken(htxsSrc_,htxs);
  // Only get Rivet data if valid
  HTXS::HiggsClassification htxsRivetInfo;
  if (htxs.isValid())
    htxsRivetInfo = * htxs;


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

  //edm::Handle<GenEventInfoProduct> GenInfoHandle ;
  //evt.getByLabel("generator", GenInfoHandle) ;
  std::vector<float> geninfoweights;
  if (genEventInfoH.size() && EvtHandle.isValid()) {
    std::vector<double> myweights=genEventInfo.weights();
    for (unsigned int i=0; i<myweights.size(); i++) {
       geninfoweights.push_back(myweights[i]/EvtHandle->originalXWGTUP());
    }; 
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
  if (!evt.isRealData() || isEmbedded_)
    genParticlesRef = reco::GenParticleRefProd(genParticles);

  // Try and get the gen information if it exists
  edm::Handle<reco::GenJetCollection> dressedParticles;
  evt.getByToken(dressedSrcToken_, dressedParticles);
  reco::GenJetRefProd dressedParticlesRef;
  if (!evt.isRealData() || isEmbedded_)
    dressedParticlesRef = reco::GenJetRefProd(dressedParticles);

  // Try and get the gen information if it exists
  edm::Handle<reco::METCollection> rivetmetParticles;
  evt.getByToken(rivetmetSrcToken_, rivetmetParticles);
  edm::RefProd<reco::METCollection> rivetmetParticlesRef;
  if (!evt.isRealData() || isEmbedded_)
    rivetmetParticlesRef = edm::RefProd<reco::METCollection>(rivetmetParticles);

  // Try and get gen taus built from gen products if they were included
  edm::Handle<std::vector<reco::GenJet>> tausHadronic;   
  evt.getByToken(genHadronicTausToken_, tausHadronic);
  edm::Handle<std::vector<reco::GenJet>> tausElectronic;   
  evt.getByToken(genElectronicTausToken_, tausElectronic);
  edm::Handle<std::vector<reco::GenJet>> tausMuonic;   
  evt.getByToken(genMuonicTausToken_, tausMuonic);
  std::vector<reco::GenJet> hTaus;
  std::vector<reco::GenJet> eTaus;
  std::vector<reco::GenJet> mTaus;
  if (tausHadronic.isValid()) { // Hadronic, electronic, and muonic are all run
  // together, so checking one should work for all
    hTaus = *tausHadronic;
    eTaus = *tausElectronic;
    mTaus = *tausMuonic;
  }

  edm::Handle<std::map<std::string, bool>> filterFlagsMap;   
  evt.getByToken(filterFlagsToken_, filterFlagsMap);
  std::map<std::string, bool> filterFlagsInfo;   
  if (filterFlagsMap.isValid())
    filterFlagsInfo = * filterFlagsMap;

  pat::TriggerEvent trg;
  PATFinalStateEvent theEvent(*rho, pvPtr, verticesPtr, metPtr, metCovariance, MVAMETInfo, metSig, metCov,
                              trg, trigStandAlone, names, *trigPrescale, *trigResults, *l1extraIsoTaus, myPuInfo, genInfo, genParticlesRef, dressedParticlesRef, rivetmetParticlesRef, 
                              hTaus, eTaus, mTaus, htxsRivetInfo,
                              evt.id(), genEventInfo, generatorFilter, evt.isRealData(), isEmbedded_, puScenario_,
                              electronRefProd, muonRefProd, tauRefProd, jetRefProd,
                              phoRefProd, pfRefProd, packedPFRefProd, trackRefProd, gsftrackRefProd, theMEts,
                              lheweights, geninfoweights, prefiringweights, npNLO, filterFlagsInfo); //FIXME 

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
  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateEventProducer);
