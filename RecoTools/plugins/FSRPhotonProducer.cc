/*  ---------------------
File: FSRPhotonProducer
Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison
Description: Make the FSR photon candidate collection for ZZ4L analysis
*/


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
//
// class decleration

#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"


class FSRPhotonProducer : public edm::EDProducer {
  public:
    explicit FSRPhotonProducer(const edm::ParameterSet& iConfig):
      src_(iConfig.getParameter<edm::InputTag>("src"))
  {
    produces<reco::PFCandidateCollection>();
  }

    ~FSRPhotonProducer() {}
  private:



    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
    {
      std::unique_ptr<reco::PFCandidateCollection> out(new reco::PFCandidateCollection);
      //https://twiki.cern.ch/twiki/bin/view/CMS/HiggsZZ4l2012SummerSync#Synchronizations_with_FSR
      //Photon definition:
      //PF photons from the particleFlow collection, plus PF photons created from the ecalEnergy of the muon PF candidates (sample code1, sample code 2, with properly massless photons)
      //Preselection: pT > 2 GeV, |η| < 2.4

      edm::Handle<reco::PFCandidateCollection> pfcands;

      if(iEvent.getByLabel(src_,pfcands)) {
        for ( reco::PFCandidateCollection::const_iterator it=pfcands->begin(); it!=pfcands->end(); ++it )    {
          // todo: look at nearest leptons, apply iso?
          if (it->pdgId() == 22 && it->charge()==0 && it->pt()>2 && fabs(it->eta())<2.4){
            out->push_back(*it);
            //std::cout << "Adding: " << it->pt() << " (eta, phi): " << it->eta() << " " << it->phi() << std::endl;
          }
          if (abs(it->pdgId())==13 && fabs(it->eta())<2.4){
            reco::Particle::PolarLorentzVector p4(it->ecalEnergy()*it->pt()/it->p(),it->eta(),it->phi(),0.0);
            if (p4.pt() > 2.0) {
              out->push_back( reco::PFCandidate(0,reco::Particle::LorentzVector(p4), reco::PFCandidate::gamma) );
              //std::cout << "Adding: " << p4.pt() << " (eta, phi): " << p4.eta() << " " << p4.phi() << std::endl;
            }
          }
        }
      }
      iEvent.put(std::move(out));
    }

    // ----------member data ---------------------------
    edm::InputTag src_;

};

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"

DEFINE_FWK_MODULE(FSRPhotonProducer);
