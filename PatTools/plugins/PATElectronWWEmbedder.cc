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
// $Id: PATElectronWWEmbedder.cc,v 1.1 2011/09/19 17:00:27 friis Exp $
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

#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "Math/GenVector/VectorUtil.h"

class PATElectronWWEmbedder : public edm::EDProducer {
  public:

    explicit PATElectronWWEmbedder(const edm::ParameterSet& iConfig):
      src_(iConfig.getParameter<edm::InputTag>("src")),
      srcVertices_(iConfig.getParameter<edm::InputTag>("srcVertices")),
      sigmaEtaEta_(iConfig.getParameter<std::vector<double> >("sigmaEtaEta")),
      deltaEta_(iConfig.getParameter<std::vector<double> >("deltaEta")),
      deltaPhi_(iConfig.getParameter<std::vector<double> >("deltaPhi")),
      hoE_(iConfig.getParameter<std::vector<double> >("hoE")),
      id_(iConfig.getParameter<std::string>("id")),
      fbrem_(iConfig.getParameter<double>("fbrem")),
      eOP_(iConfig.getParameter<double>("EOP")),
      DB_(iConfig.getParameter<double>("d0")),
      DZ_(iConfig.getParameter<double>("dz"))

  {
    produces<pat::ElectronCollection>();
  }

    ~PATElectronWWEmbedder() {}
  private:

    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
    {
      using namespace edm;
      using namespace reco;
      std::auto_ptr<pat::ElectronCollection > out(new pat::ElectronCollection);

      edm::Handle<reco::BeamSpot> bsHandle;
      iEvent.getByLabel("offlineBeamSpot", bsHandle);
      const reco::BeamSpot &thebs = *bsHandle.product();

      edm::Handle<reco::VertexCollection> vtxHandle;
      iEvent.getByLabel(srcVertices_, vtxHandle);

      edm::Handle<reco::ConversionCollection> hConversions;
      iEvent.getByLabel("allConversions", hConversions);

      Handle<pat::ElectronCollection > cands;
      if(iEvent.getByLabel(src_,cands))
        for(unsigned int  i=0;i!=cands->size();++i)
          if(cands->at(i).isEB()||cands->at(i).isEE()) {
            pat::Electron electron = cands->at(i);

            bool passID=false;
            unsigned int type=0;

            bool passconversionveto =
              !ConversionTools::hasMatchedConversion(electron,hConversions,thebs.position());

            if(electron.pt()<20&&electron.isEB()) type=0;
            if(electron.pt()<20&&electron.isEE()) type=1;
            if(electron.pt()>=20&&electron.isEB()) type=2;
            if(electron.pt()>=20&&electron.isEE()) type=3;

            if(fabs(electron.sigmaIetaIeta())<sigmaEtaEta_[type]) {
              if(fabs(electron.deltaEtaSuperClusterTrackAtVtx())<deltaEta_[type]) {
                if(fabs(electron.deltaPhiSuperClusterTrackAtVtx())<deltaPhi_[type]) {
                  if(fabs(electron.hcalOverEcal())<hoE_[type]) {
                    if(fabs(electron.dB())<DB_)
                      if(passconversionveto)
                        if(vtxHandle->size()>0)
                          if(fabs(electron.gsfTrack()->dz(vtxHandle->at(0).position()))<DZ_)
                          {
                            if(type==0||type==1) {
                              if((electron.fbrem()>fbrem_) || (fabs(electron.eta())<1. && electron.eSuperClusterOverP()>eOP_))
                                passID=true;
                            }
                            else
                            {
                              passID=true;
                            }
                          }
                  }
                }
              }
            }

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
    edm::InputTag srcVertices_;

    std::vector<double>  sigmaEtaEta_;
    std::vector<double>  deltaEta_;
    std::vector<double>  deltaPhi_;
    std::vector<double>  hoE_;
    std::string id_;
    double fbrem_;
    double eOP_;
    double DB_;
    double DZ_;

};

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronWWEmbedder);
