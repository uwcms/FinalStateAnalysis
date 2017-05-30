// -*- C++ -*-
//
// Package:    FinalStateAnalysis/PatTools
// Class:      PATElectronSystematicsEmbedderLFV
// 
/**\class PATElectronSystematicsEmbedderLFV PATElectronSystematicsEmbedderLFV.cc FinalStateAnalysis/PatTools/plugins/PATElectronSystematicsEmbedderLFV.cc

 Description: [Embeds EGM Scale, Smearing systematics into ntuples]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Nabarun Dev
//         Created:  Tue, 28 Feb 2017 12:00:57 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "EgammaAnalysis/ElectronTools/interface/EnergyScaleCorrection_class.h"
#include "TRandom3.h"

//
// class declaration
//

class PATElectronSystematicsEmbedderLFV : public edm::stream::EDProducer<> {
public:
  // Our dataformat for storing shifted candidates                                                                        
  typedef reco::LeafCandidate ShiftedCand;
  typedef std::vector<ShiftedCand> ShiftedCandCollection;
  typedef reco::CandidatePtr CandidatePtr;
      
  PATElectronSystematicsEmbedderLFV(const edm::ParameterSet&);
  virtual ~PATElectronSystematicsEmbedderLFV();
  void produce(edm::Event&, const edm::EventSetup&) override;


  
private:
  TRandom3* rgen_;
  EnergyScaleCorrection_class eScaler_; //correctionloader
  edm::EDGetTokenT<edm::View<pat::Electron> > srcTokencalib_;
  edm::EDGetTokenT<edm::View<pat::Electron> > srcTokenuncalib_;
  edm::EDGetTokenT<EcalRecHitCollection> recHitCollectionEBToken_;
  edm::EDGetTokenT<EcalRecHitCollection> recHitCollectionEEToken_;
  double nominal_;
  double eScaleUp_;
  double eScaleDown_;

};

 
PATElectronSystematicsEmbedderLFV::PATElectronSystematicsEmbedderLFV(const edm::ParameterSet& pset)
{
  rgen_=new TRandom3(8675389);
  eScaler_=EnergyScaleCorrection_class("EgammaAnalysis/ElectronTools/data/ScalesSmearings/Moriond17_23Jan_ele");
  

  srcTokencalib_ = consumes<edm::View<pat::Electron> >(pset.getParameter<edm::InputTag>("calibratedElectrons"));
  srcTokenuncalib_ = consumes<edm::View<pat::Electron> >(pset.getParameter<edm::InputTag>("uncalibratedElectrons"));

  recHitCollectionEBToken_=consumes<EcalRecHitCollection>(pset.getParameter<edm::InputTag>( "recHitCollectionEB" ));
  recHitCollectionEEToken_=consumes<EcalRecHitCollection>(pset.getParameter<edm::InputTag>( "recHitCollectionEE" ));
  // Embedded output collection
  produces<pat::ElectronCollection>();

  // Collections of shifted candidates

  produces<ShiftedCandCollection>("p4OutUncorr");

  produces<ShiftedCandCollection>("p4OutUp");    //Scale up and down
  produces<ShiftedCandCollection>("p4OutDown");

  produces<ShiftedCandCollection>("p4OutResUp"); //Resolution up and down for rho parameter
  produces<ShiftedCandCollection>("p4OutResDown");

  produces<ShiftedCandCollection>("p4OutResPhiDown");//Resolution up and down for phi parameter
  //egamma recommends to decouple the changes and use phi down only
}


PATElectronSystematicsEmbedderLFV::~PATElectronSystematicsEmbedderLFV()
{
 
   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)

}



// ------------ method called to produce the data  ------------
void
PATElectronSystematicsEmbedderLFV::produce(edm::Event& evt, const edm::EventSetup& iSetup)
{
   using namespace edm;
   using namespace std;

   std::auto_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
   std::auto_ptr<ShiftedCandCollection> p4OutUncorr(new ShiftedCandCollection);
   std::auto_ptr<ShiftedCandCollection> p4OutUp(new ShiftedCandCollection);
   std::auto_ptr<ShiftedCandCollection> p4OutDown(new ShiftedCandCollection);
   std::auto_ptr<ShiftedCandCollection> p4OutResUp(new ShiftedCandCollection);
   std::auto_ptr<ShiftedCandCollection> p4OutResDown(new ShiftedCandCollection);
   std::auto_ptr<ShiftedCandCollection> p4OutResPhiDown(new ShiftedCandCollection);

   edm::Handle<edm::View<pat::Electron> > uncalibratedPatElectrons;
   evt.getByToken(srcTokenuncalib_, uncalibratedPatElectrons);

   edm::Handle<edm::View<pat::Electron> > calibratedPatElectrons;
   evt.getByToken(srcTokencalib_, calibratedPatElectrons);
   

   output->reserve(uncalibratedPatElectrons->size());

   p4OutUncorr->reserve(uncalibratedPatElectrons->size());

   p4OutUp->reserve(uncalibratedPatElectrons->size());
   p4OutDown->reserve(uncalibratedPatElectrons->size());

   p4OutResUp->reserve(uncalibratedPatElectrons->size());
   p4OutResDown->reserve(uncalibratedPatElectrons->size());
   p4OutResPhiDown->reserve(uncalibratedPatElectrons->size());
   
   edm::Handle<EcalRecHitCollection> recHitCollectionEBHandle;
   edm::Handle<EcalRecHitCollection> recHitCollectionEEHandle;

   evt.getByToken(recHitCollectionEBToken_, recHitCollectionEBHandle);
   evt.getByToken(recHitCollectionEEToken_, recHitCollectionEEHandle);


   for (size_t i = 0; i < uncalibratedPatElectrons->size(); ++i) {
     pat::Electron electron = uncalibratedPatElectrons->at(i); // make a local copy
     double pt = electron.pt();

     double eta = electron.eta();
     double phi = electron.phi();
     double mass = electron.mass();

     pat::Electron calibratedElectron=calibratedPatElectrons->at(i);

     double pt2 = calibratedElectron.pt();

     double eta2 = calibratedElectron.eta();
     double phi2 = calibratedElectron.phi();
     double mass2 = calibratedElectron.mass();
     double etEle2=calibratedElectron.et();



     ShiftedCand uncorr = electron;

     //     cout<<"pt, pz, p, mt, mass, et, energy, charge ,eta, phi  :"<<electron.pt()<<", "<<electron.pz()<<", "<<electron.p()<<", "<<electron.mt()<<", "<<electron.mass()<<", "<<electron.et()<<", "<<electron.energy()<<", "<<electron.charge()<<", "<<electron.eta()<<", "<<electron.phi()<<", "<<endl;

     //     cout<<electron.r9()<<endl;
   
     bool isEBEle=electron.isEB();
     int runnum=evt.run();
     
     double etaSCEle=electron.superCluster().get()->eta();
     double full5x5r9=electron.full5x5_r9();
     double etEle=electron.et();
     

     const EcalRecHitCollection* recHits = (electron.isEB()) ? recHitCollectionEBHandle.product() : recHitCollectionEEHandle.product();

     DetId seedDetId = electron.superCluster()->seed()->seed();

     EcalRecHitCollection::const_iterator seedRecHit = recHits->find(seedDetId);


     unsigned int gainSeedSC = 12;
     if (seedRecHit != recHits->end()) {
       if(seedRecHit->checkFlag(EcalRecHit::kHasSwitchToGain6)) gainSeedSC = 6;
       if(seedRecHit->checkFlag(EcalRecHit::kHasSwitchToGain1)) gainSeedSC = 1;
       }


     //     std::bitset<scAll> uncBitMask=100;
     //scale 
     float error_scale=eScaler_.ScaleCorrectionUncertainty(runnum,isEBEle,full5x5r9,etaSCEle,etEle2,gainSeedSC,3); //error in scale correction

     double Up_factor = (1+error_scale);
     double Down_factor =  (1-error_scale);

     ShiftedCand eesUp = calibratedElectron;          //scale up and down uncertainties to be applied on the calibrated/smeared nominal value
     ShiftedCand eesDown = calibratedElectron;

     eesUp.setP4(reco::Particle::PolarLorentzVector(pt2*Up_factor, eta2, phi2, mass2));
     eesDown.setP4(reco::Particle::PolarLorentzVector(pt2*Down_factor, eta2, phi2, mass2));



     //resolution

     float sigma_up=eScaler_.getSmearingSigma(runnum,isEBEle,full5x5r9,etaSCEle,etEle,gainSeedSC,1,0); //corrected sigma ->sigma+/-sigma_err
     float sigma_down=eScaler_.getSmearingSigma(runnum,isEBEle,full5x5r9,etaSCEle,etEle,gainSeedSC,-1,0); //corrected sigma ->sigma+/-sigma_e
     
     double ResUp_factor = rgen_->Gaus(1,sigma_up);
     double ResDown_factor = rgen_->Gaus(1,sigma_down);

     float sigma_resphidown=eScaler_.getSmearingSigma(runnum,isEBEle,full5x5r9,etaSCEle,etEle,gainSeedSC,0,-1); //corrected sigma ->sigma+/-sigma_e

     double ResPhiDown_factor =rgen_->Gaus(1,sigma_resphidown);

     ShiftedCand eResUp = electron; //scale up and down uncertainties to be applied using modified sigmas on unsmeared/uncalibrated nominal value                                      
     ShiftedCand eResDown = electron;

     ShiftedCand eResPhiDown = electron;

     eResUp.setP4(reco::Particle::PolarLorentzVector(pt*ResUp_factor, eta, phi, mass));
     eResDown.setP4(reco::Particle::PolarLorentzVector(pt*ResDown_factor, eta, phi, mass));
     eResPhiDown.setP4(reco::Particle::PolarLorentzVector(pt*ResPhiDown_factor, eta, phi, mass));

     output->push_back(calibratedElectron);

     p4OutUncorr->push_back(uncorr); //save the uncorrected as usercand in case we use it to recorrect the MET

     p4OutUp->push_back(eesUp);
     p4OutDown->push_back(eesDown);

     p4OutResUp->push_back(eResUp);
     p4OutResDown->push_back(eResDown);
     p4OutResPhiDown->push_back(eResPhiDown);

   }

   // Put the shifted collections in the event
   typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
   PutHandle p4OutUncorrH = evt.put(p4OutUncorr, "p4OutUncorr");

   PutHandle p4OutUpH = evt.put(p4OutUp, "p4OutUp");
   PutHandle p4OutDownH = evt.put(p4OutDown, "p4OutDown");

   PutHandle p4OutResUpH = evt.put(p4OutResUp, "p4OutResUp");
   PutHandle p4OutResDownH = evt.put(p4OutResDown, "p4OutResDown");
   PutHandle p4OutResPhiDownH = evt.put(p4OutResPhiDown, "p4OutResPhiDown");

   // Now embed the shifted collections into the output electron collection
   for (size_t i = 0; i < calibratedPatElectrons->size(); ++i) {
     CandidatePtr uncorrPtr(p4OutUncorrH, i);

     CandidatePtr upPtr(p4OutUpH, i);
     CandidatePtr downPtr(p4OutDownH, i);

     CandidatePtr resupPtr(p4OutResUpH, i);
     CandidatePtr resdownPtr(p4OutResDownH, i);
     CandidatePtr resphidownPtr(p4OutResPhiDownH, i);

     pat::Electron& electron = output->at(i);

     electron.addUserCand("uncorr", uncorrPtr);
   
     electron.addUserCand("eScaleUp", downPtr);
     electron.addUserCand("eScaleDown", upPtr);
  
     electron.addUserCand("eResUp", resupPtr);
     electron.addUserCand("eResDown", resdownPtr);
     electron.addUserCand("eResPhiDown", resphidownPtr);


 }

   evt.put(output);

 
}


//define this as a plug-in
DEFINE_FWK_MODULE(PATElectronSystematicsEmbedderLFV);
