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
// $Id: PATVBTFMuonEmbedder.h,v 1.3 2011/01/23 21:54:15 bachtis Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"


#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include "Math/GenVector/VectorUtil.h"
//
// class decleration



class PATVBTFMuonEmbedder : public edm::EDProducer {
   public:



  explicit PATVBTFMuonEmbedder(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src")),
    maxDxDy_(iConfig.getParameter<double>("maxDxDy")),
    maxChi2_(iConfig.getParameter<double>("maxChi2")),
    minTrackerHits_(iConfig.getParameter<int>("minTrackerHits")),
    minPixelHits_(iConfig.getParameter<int>("minPixelHits")),
    minMuonHits_(iConfig.getParameter<int>("minMuonHits")),
    minMatches_(iConfig.getParameter<int>("minMatches")),
    maxResol_(iConfig.getParameter<double>("maxResol"))
  {
    produces<pat::MuonCollection>();
  }

  ~PATVBTFMuonEmbedder() {}
   private:



  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
  {
    using namespace edm;
    using namespace reco;

    Handle<reco::BeamSpot> beamSpotHandle;
    if (!iEvent.getByLabel(InputTag("offlineBeamSpot"), beamSpotHandle)) {
      LogTrace("") << ">>> No beam spot found !!!";
      return;
    }

    std::unique_ptr<pat::MuonCollection > out(new pat::MuonCollection);


    Handle<pat::MuonCollection > cands;
    if(iEvent.getByLabel(src_,cands))
      for(unsigned int  i=0;i!=cands->size();++i){
	pat::Muon muon = cands->at(i);

	bool passID=false;

	if(muon.isGlobalMuon()&&muon.isTrackerMuon())
	  if(fabs(muon.globalTrack()->dxy(beamSpotHandle->position()))<maxDxDy_)
	    if(muon.globalTrack()->normalizedChi2()<maxChi2_)
	      if(muon.innerTrack()->hitPattern().numberOfValidTrackerHits()>=minTrackerHits_)
		if(muon.innerTrack()->hitPattern().numberOfValidPixelHits()>=minPixelHits_)
		  //		  if(muon.innerTrack()->ptError()/muon.innerTrack()->pt()<=maxResol_)
		    if(muon.numberOfMatches()>=minMatches_)
		    passID=true;

	if(passID)
	  muon.addUserInt("VBTF",1);
	else
	  muon.addUserInt("VBTF",0);
	out->push_back(muon);

      }


    iEvent.put(std::move(out));

  }

      // ----------member data ---------------------------
      edm::InputTag src_;
      double maxDxDy_;
      double maxChi2_;
      int minTrackerHits_;
      int minPixelHits_;
      int minMuonHits_;
      int minMatches_;
      double maxResol_;
};

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATVBTFMuonEmbedder);
