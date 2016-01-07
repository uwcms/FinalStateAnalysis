// -*- C++ -*-
//
// Package:    MiniAODGenLeptonFSRFilter
// Class:      MiniAODGenLeptonFSRFilter
// 
//
// Original Author:  Nick Smith
//         Created:  Fri Jun 12 02:15:46 CDT 2015


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"

//
// class declaration
//

class MiniAODGenLeptonFSRFilter : public edm::EDFilter {
   public:
      explicit MiniAODGenLeptonFSRFilter(const edm::ParameterSet&);
      ~MiniAODGenLeptonFSRFilter();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual bool beginRun(edm::Run&, edm::EventSetup const&);
      virtual bool endRun(edm::Run&, edm::EventSetup const&);
      virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------

   edm::EDGetTokenT<edm::View<reco::GenParticle> > genParticlesToken_;
   double photonPtCut_;
   double photonDrCut_;
   bool reverseDecision_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
MiniAODGenLeptonFSRFilter::MiniAODGenLeptonFSRFilter(const edm::ParameterSet& iConfig) :
  genParticlesToken_(consumes<edm::View<reco::GenParticle> >(iConfig.getParameter<edm::InputTag>("src"))),
  photonPtCut_(iConfig.exists("ptCut") ? iConfig.getParameter<double>("ptCut") : 12.),
  photonDrCut_(iConfig.exists("drCut") ? iConfig.getParameter<double>("drCut") : 0.),
  reverseDecision_(iConfig.exists("reverseDecision") ? iConfig.getParameter<bool>("reverseDecision") : false)
{

}


MiniAODGenLeptonFSRFilter::~MiniAODGenLeptonFSRFilter()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
MiniAODGenLeptonFSRFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<edm::View<reco::GenParticle> > genParticles;
   iEvent.getByToken(genParticlesToken_, genParticles);

   // some alias
   bool keep = !reverseDecision_;
   bool reject = reverseDecision_;

   // keep event in ZG
   bool keepEvent = false;

   // Get the photon
   for ( auto& genPhoton : *genParticles ) {
      if ( //genPhoton.status() == 1 
            genPhoton.isPromptFinalState()
            && genPhoton.pdgId() == 22 
            //&& (abs(genPhoton.mother(0)->pdgId()) == 11 || abs(genPhoton.mother(0)->pdgId()) == 13 || abs(genPhoton.mother(0)->pdgId()) == 15 || abs(genPhoton.mother(0)->pdgId()) < 7) 
            && genPhoton.pt() > photonPtCut_
            ) {
         // pt of photon above threshold and parent is quark or lepton
         keepEvent = true;
         //std::cout << "found high pt lepton" << std::endl;
         // Get lepton
         for  ( auto& genLepton : *genParticles ) {
           double deltaR = reco::deltaR(genPhoton.p4(), genLepton.p4());
           if ( genLepton.status() == 1
                && (abs(genLepton.pdgId()) == 11 || abs(genLepton.pdgId()) == 13 || abs(genLepton.pdgId()) == 15)
                && (deltaR < photonDrCut_)
                ) {
             // lepton within dr of lepton
             //std::cout << "photon within dr of lepton" << std::endl;
             keepEvent = false;
          }
          // reject if have photon close to lepton
          if (!keepEvent) {
             //std::cout << "return (fail dr): " << reject << std::endl;
             return reject;
          }
        }
      }
   }

   // keep event if we had a passing fsr photon
   if (keepEvent) {
       //std::cout << "return: " << keep << std::endl;
       return keep;
   }
   else {
       //std::cout << "return: " << reject << std::endl;
       return reject;
   }

}

// ------------ method called once each job just before starting event loop  ------------
void 
MiniAODGenLeptonFSRFilter::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MiniAODGenLeptonFSRFilter::endJob() {
}

// ------------ method called when starting to processes a run  ------------
bool 
MiniAODGenLeptonFSRFilter::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool 
MiniAODGenLeptonFSRFilter::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
MiniAODGenLeptonFSRFilter::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool 
MiniAODGenLeptonFSRFilter::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MiniAODGenLeptonFSRFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODGenLeptonFSRFilter);

