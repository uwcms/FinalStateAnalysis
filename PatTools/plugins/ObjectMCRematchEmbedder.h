/*
 * re-embed the MC matching information
 *
 * author: L. Gray
 *
 */

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "Math/GenVector/VectorUtil.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"

// class declaration
//
template <typename Collection>
class MCRematchEmbedder : public edm::EDProducer {
  typedef edm::Association<reco::GenParticleCollection> GenMatchMap;
  typedef edm::Association<reco::GenJetCollection> GenJetMatchMap;
  typedef edm::Ref<Collection> ObjectRef;
  public:
    MCRematchEmbedder (const edm::ParameterSet& iConfig):
      srcToken_(consumes<Collection>(iConfig.getParameter<edm::InputTag>("src"))),
      matchSrcToken_(consumes<GenMatchMap>(iConfig.getParameter<edm::InputTag>("matchSrc"))) {
      produces< Collection >();
    }
    ~MCRematchEmbedder () { }

    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
 private:
    edm::EDGetTokenT<Collection> srcToken_;
    edm::EDGetTokenT<GenMatchMap> matchSrcToken_;
};

template<typename Collection>
void MCRematchEmbedder<Collection>::produce(edm::Event& iEvent, 
					    const edm::EventSetup& iSetup) {
  std::auto_ptr<Collection> out(new Collection);

  edm::Handle<Collection> in;
  edm::Handle<GenMatchMap> match;

  iEvent.getByToken(srcToken_,in);
  iEvent.getByToken(matchSrcToken_,match);

  typename Collection::const_iterator i = in->begin();
  typename Collection::const_iterator b = in->begin();
  typename Collection::const_iterator e = in->end();
  
  for( ; i != e; ++i ) {
    typename Collection::value_type temp = *i;
    ObjectRef oref(in,i-b);
    
    reco::GenParticleRef genp = (*match)[oref];
    temp.setGenParticleRef((*match)[oref]);
    out->push_back(temp);
  }

  iEvent.put(out);
}


#include "DataFormats/PatCandidates/interface/Jet.h"
template <>
class MCRematchEmbedder<pat::JetCollection> : public edm::EDProducer {
  typedef edm::Association<reco::GenParticleCollection> GenMatchMap;
  typedef edm::Association<reco::GenJetCollection> GenJetMatchMap;
  typedef edm::Ref<pat::JetCollection> ObjectRef;
 public:
  MCRematchEmbedder (const edm::ParameterSet& iConfig):
    srcToken_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("src"))),
    matchSrcToken_(consumes<GenMatchMap>(iConfig.getParameter<edm::InputTag>("matchSrc"))),
    genJetMatchSrcToken_(consumes<GenJetMatchMap>(iConfig.getParameter<edm::InputTag>("genJetMatchSrc"))) {
    produces< pat::JetCollection >();
    produces< reco::GenJetCollection >(); // for forward refs
  }
  ~MCRematchEmbedder () { }
  
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
 private:
  edm::EDGetTokenT<pat::JetCollection> srcToken_;
  edm::EDGetTokenT<GenMatchMap> matchSrcToken_;
  edm::EDGetTokenT<GenJetMatchMap> genJetMatchSrcToken_;
};

void 
MCRematchEmbedder<pat::JetCollection>::produce(edm::Event& iEvent, 
					       const edm::EventSetup& iSetup) {
  std::auto_ptr<pat::JetCollection> out(new pat::JetCollection);
  std::auto_ptr<reco::GenJetCollection> genjetsout(new reco::GenJetCollection);

  edm::RefProd<reco::GenJetCollection > h_genJetsOut = 
    iEvent.getRefBeforePut<reco::GenJetCollection >( );

  edm::Handle<pat::JetCollection> in;
  edm::Handle<GenMatchMap> match;
  edm::Handle<GenJetMatchMap> jetmatch;

  iEvent.getByToken(srcToken_,in);
  iEvent.getByToken(matchSrcToken_,match);
  iEvent.getByToken(genJetMatchSrcToken_,jetmatch);

  pat::JetCollection::const_iterator i = in->begin();
  pat::JetCollection::const_iterator b = in->begin();
  pat::JetCollection::const_iterator e = in->end();
  
  for( ; i != e; ++i ) {
    pat::JetCollection::value_type temp = *i;
    ObjectRef oref(in,i-b);
    reco::GenJetRef genjet = (*jetmatch)[oref];
    reco::GenParticleRef genp = (*match)[oref];

    if( genp.isAvailable() && genp.isNonnull() ) {
      temp.setGenParton((*match)[oref]);
    }

    if( genjet.isAvailable() && genjet.isNonnull() ) {
      genjetsout->push_back(*genjet);
      // set the "forward" ref to the thinned collection
      edm::Ref<reco::GenJetCollection > 
	genForwardRef ( h_genJetsOut, genjetsout->size() - 1 );
	// set the "backward" ref to the original collection
	edm::Ref<reco::GenJetCollection > genBackRef ( genjet );
	// make the FwdPtr
	edm::FwdRef<reco::GenJetCollection > 
	  genjetFwdRef ( genForwardRef, genBackRef );
	temp.setGenJetRef(genjetFwdRef );
    }

    out->push_back(temp);
  }

  iEvent.put(genjetsout);
  iEvent.put(out);
}


