// -*- C++ -*-
//
// Package:    PATMuonTrackVetoSelector
// Class:      PATMuonTrackVetoSelector
//
/**\class PATMuonTrackVetoSelector PATMuonTrackVetoSelector.cc UWAnalysis/PATMuonTrackVetoSelector/src/PATMuonTrackVetoSelector.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Michail Bachtis
//         Created:  Sun Jan 31 15:04:57 CST 2010
// $Id: GSFTrackCandidateProducer.h,v 1.1 2011/01/23 22:00:02 bachtis Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidateFwd.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "Math/GenVector/VectorUtil.h"
//
// class decleration



class GSFTrackCandidateProducer : public edm::EDProducer {
   public:



  explicit GSFTrackCandidateProducer(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src")),
    threshold_(iConfig.getParameter<double>("threshold"))
  {
    produces<reco::RecoChargedCandidateCollection>();
  }

  ~GSFTrackCandidateProducer() {}
   private:



  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
  {
    using namespace edm;
    using namespace reco;

    std::auto_ptr<reco::RecoChargedCandidateCollection> out(new  RecoChargedCandidateCollection);
    edm::Handle<reco::VertexCollection> vertices;
    reco::Vertex primary;
    if(iEvent.getByLabel("offlinePrimaryVerticesWithBS",vertices))
      if(vertices->size()>0)
	primary = vertices->at(0);

    edm::Handle<reco::GsfTrackCollection> tracks;
    if(iEvent.getByLabel(src_,tracks))       {
      for(unsigned int i=0;i<tracks->size();++i) {
	reco::Candidate::LorentzVector p4(tracks->at(i).px(),tracks->at(i).py(),tracks->at(i).pz(),tracks->at(i).p());
	math::XYZPoint vtx(0.,0.,0.);
	if(vertices->size()>0)
	  vtx = primary.position();

	RecoChargedCandidate cand(tracks->at(i).charge() , p4, vtx);
	if(cand.pt()>threshold_)
	  out->push_back(cand);
      }

    }


    iEvent.put(out);

  }

      // ----------member data ---------------------------
  edm::InputTag src_;
  double threshold_;
};

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"

DEFINE_FWK_MODULE(GSFTrackCandidateProducer);
