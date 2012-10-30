// -*- C++ -*-
//
// Package:    PATElectronVBTFEmbedder
// Class:      PATElectronVBTFEmbedder
//
//  Description: Embeds VBTF ID in pat::Electrons
//
// Original Author:  Michail Bachtis
// Modified: Evan Friis
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
#include "DataFormats/PatCandidates/interface/Electron.h"

#include "EGamma/EGammaAnalysisTools/interface/EGammaCutBasedEleId.h"

#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include "DataFormats/EgammaCandidates/interface/ConversionFwd.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "Math/GenVector/VectorUtil.h"

namespace eid = EgammaCutBasedEleId;



class PATElectronCutBasedIdEmbedder : public edm::EDProducer {
  typedef std::vector<std::string> vstring;
  typedef std::map<std::string,eid::WorkingPoint> wp_map;  
  
  public:
    explicit PATElectronCutBasedIdEmbedder(const edm::ParameterSet& iConfig):
      _src(iConfig.getParameter<edm::InputTag>("src")),
      _bssrc(iConfig.getParameter<edm::InputTag>("beamspotSrc")),
      _vtxsrc(iConfig.getParameter<edm::InputTag>("vtxSrc")),
      _convsrc(iConfig.getParameter<edm::InputTag>("conversionsSrc")),
      _wps_applied(iConfig.getParameter<vstring>("wps_to_apply")) {
      
      edm::VParameterSet wps = 
	iConfig.getParameterSetVector("available_working_points");

      edm::VParameterSet::const_iterator i = wps.begin();
      edm::VParameterSet::const_iterator e = wps.end();

      for( ; i != e; ++i)
	_wps[i->getParameter<std::string>("name")] =
	  (eid::WorkingPoint)i->getParameter<int>("index");
      

      // do not apply isolation criteria to the selection
      eid::PassAll = 
	( eid::DETAIN | eid::DPHIIN  | eid::SIGMAIETAIETA | 
	  eid::HOE    | eid::OOEMOOP | eid::D0VTX  | 
	  eid::DZVTX  | eid::VTXFIT  | eid::MHITS );

      produces<pat::ElectronCollection>();
  }
    ~PATElectronCutBasedIdEmbedder() {}
  private:
    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
      using namespace edm;
      using namespace reco;
      std::auto_ptr<pat::ElectronCollection > out(new pat::ElectronCollection);

      Handle<BeamSpot> the_bs;
      iEvent.getByLabel(_bssrc,the_bs);

      Handle<VertexCollection> the_vtxs;
      iEvent.getByLabel(_vtxsrc,the_vtxs);

      Handle<ConversionCollection> the_convs;
      iEvent.getByLabel(_convsrc,the_convs);

      vstring::const_iterator ii;
      vstring::const_iterator ee = _wps_applied.end();

      Handle<pat::ElectronCollection > cands;
      if(iEvent.getByLabel(_src,cands))
        for(unsigned int  i=0;i!=cands->size();++i) {
          
	  pat::Electron* electron = const_cast<pat::Electron*>(&cands->at(i));
	  
	  ii = _wps_applied.begin();
	  for( ; ii != ee; ++ii ) {
	    // iso applied later/differently
	    int pass = (int)eid::PassWP(_wps[*ii],*electron,
					the_convs,*the_bs.product(),
					the_vtxs,
					0.0,0.0,0.0,0.0); 
	    electron->addUserInt(*ii,pass);	    
	  }

	  out->push_back(*electron);
	}

      iEvent.put(out);
    }

  // ----------member data ---------------------------
  edm::InputTag _src,_bssrc,_vtxsrc,_convsrc;
  vstring _wps_applied;
  wp_map _wps;
};

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronCutBasedIdEmbedder);
