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

#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include "Math/GenVector/VectorUtil.h"


class PATElectronVBTFEmbedder : public edm::EDProducer {
  public:
    explicit PATElectronVBTFEmbedder(const edm::ParameterSet& iConfig):
      src_(iConfig.getParameter<edm::InputTag>("src")),
      sigmaEtaEta_(iConfig.getParameter<std::vector<double> >("sigmaEtaEta")),
      deltaEta_(iConfig.getParameter<std::vector<double> >("deltaEta")),
      deltaPhi_(iConfig.getParameter<std::vector<double> >("deltaPhi")),
      hoE_(iConfig.getParameter<std::vector<double> >("hoE")),
      id_(iConfig.getParameter<std::string>("id")) {
    produces<pat::ElectronCollection>();
  }
    ~PATElectronVBTFEmbedder() {}
  private:
    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
      using namespace edm;
      using namespace reco;
      std::auto_ptr<pat::ElectronCollection > out(new pat::ElectronCollection);

      Handle<pat::ElectronCollection > cands;
      if(iEvent.getByLabel(src_,cands))
        for(unsigned int  i=0;i!=cands->size();++i)
          if(cands->at(i).isEB()||cands->at(i).isEE()) {
            pat::Electron electron = cands->at(i);

            bool passID=false;
            unsigned int type=0;
            if(electron.isEE()) type=1;

            if(fabs(electron.sigmaIetaIeta())<sigmaEtaEta_[type])
              if(fabs(electron.deltaEtaSuperClusterTrackAtVtx())<deltaEta_[type])
                if(fabs(electron.deltaPhiSuperClusterTrackAtVtx())<deltaPhi_[type])
                  if(fabs(electron.hcalOverEcal())<hoE_[type])
                    passID=true;



            if(passID)
              electron.addUserFloat(id_,1.0);
            else
              electron.addUserFloat(id_,0.0);
            out->push_back(electron);

          }


      iEvent.put(out);

    }

    // ----------member data ---------------------------
    edm::InputTag src_;
    std::vector<double>  sigmaEtaEta_;
    std::vector<double>  deltaEta_;
    std::vector<double>  deltaPhi_;
    std::vector<double>  hoE_;
    std::string id_;
};

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronVBTFEmbedder);
