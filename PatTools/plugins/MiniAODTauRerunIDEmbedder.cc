/*
 * Embed Rerun Tau MVA IDs (see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#Rerunning_of_the_tau_ID_on_MiniA)
 * into pat::Taus
 *
 * Based off of : https://github.com/cms-tau-pog/cmssw/blob/CMSSW_8_0_X_tau-pog_miniAOD-backport-tauID/RecoTauTag/RecoTau/test/rerunMVAIsolationOnMiniAOD.cc
 *
 * Author: Tyler Ruggles, UW Madison
 */


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/PATTauDiscriminator.h"

#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauFwd.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "DataFormats/TauReco/interface/PFTauTransverseImpactParameterAssociation.h"

#include "RecoTauTag/RecoTau/interface/PFRecoTauClusterVariables.h"

// Include below later if we want to add new AntiElectronID
//#include "RecoTauTag/RecoTau/interface/AntiElectronIDMVA6.h"



class MiniAODTauRerunIDEmbedder : public edm::EDProducer {
  public:
    MiniAODTauRerunIDEmbedder(const edm::ParameterSet& pset);

    virtual ~MiniAODTauRerunIDEmbedder(){
    }

    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<pat::TauCollection> srcTauToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVLooseToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationLooseToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationMediumToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationTightToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVTightToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVTightToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationv2Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVLoosev2Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVLoosev2Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationLoosev2Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationMediumv2Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationTightv2Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVTightv2Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVTightv2Token_;

    
    //newDM
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationv2TokennewDM_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVLoosev2TokennewDM_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVLoosev2TokennewDM_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationLoosev2TokennewDM_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationMediumv2TokennewDM_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationTightv2TokennewDM_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVTightv2TokennewDM_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVTightv2TokennewDM_;
    
};

MiniAODTauRerunIDEmbedder::MiniAODTauRerunIDEmbedder(const edm::ParameterSet& pset) {
  srcTauToken_              = consumes<pat::TauCollection>(pset.getParameter<edm::InputTag>("src"));
  mvaIsolationToken_        = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idRaw"));
  mvaIsolationVLooseToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVLoose"));
  mvaIsolationLooseToken_   = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idLoose"));
  mvaIsolationMediumToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idMedium"));
  mvaIsolationTightToken_   = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idTight"));
  mvaIsolationVTightToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVTight"));
  mvaIsolationVVTightToken_ = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVVTight"));
  mvaIsolationv2Token_        = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idRawv2"));
  mvaIsolationVVLoosev2Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVVLoosev2"));
  mvaIsolationVLoosev2Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVLoosev2"));
  mvaIsolationLoosev2Token_   = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idLoosev2"));
  mvaIsolationMediumv2Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idMediumv2"));
  mvaIsolationTightv2Token_   = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idTightv2"));
  mvaIsolationVTightv2Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVTightv2"));
  mvaIsolationVVTightv2Token_ = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVVTightv2"));

    //newDm
    mvaIsolationv2TokennewDM_        = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idRawv2newDM"));
    mvaIsolationVVLoosev2TokennewDM_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVVLoosev2newDM"));
    mvaIsolationVLoosev2TokennewDM_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVLoosev2newDM"));
    mvaIsolationLoosev2TokennewDM_   = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idLoosev2newDM"));
    mvaIsolationMediumv2TokennewDM_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idMediumv2newDM"));
    mvaIsolationTightv2TokennewDM_   = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idTightv2newDM"));
    mvaIsolationVTightv2TokennewDM_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVTightv2newDM"));
    mvaIsolationVVTightv2TokennewDM_ = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("idVVTightv2newDM"));
    
  produces<pat::TauCollection>();

}

void MiniAODTauRerunIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<pat::TauCollection> output(new pat::TauCollection);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoRaw;
  evt.getByToken(mvaIsolationToken_,mvaIsoRaw);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoVLoose;
  evt.getByToken(mvaIsolationVLooseToken_,mvaIsoVLoose);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoLoose;
  evt.getByToken(mvaIsolationLooseToken_,mvaIsoLoose);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoMedium;
  evt.getByToken(mvaIsolationMediumToken_,mvaIsoMedium);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoTight;
  evt.getByToken(mvaIsolationTightToken_,mvaIsoTight);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoVTight;
  evt.getByToken(mvaIsolationVTightToken_,mvaIsoVTight);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVTight;
  evt.getByToken(mvaIsolationVVTightToken_,mvaIsoVVTight);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoRawv2;
  evt.getByToken(mvaIsolationv2Token_,mvaIsoRawv2);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVLoosev2;
  evt.getByToken(mvaIsolationVVLoosev2Token_,mvaIsoVVLoosev2);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoVLoosev2;
  evt.getByToken(mvaIsolationVLoosev2Token_,mvaIsoVLoosev2);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoLoosev2;
  evt.getByToken(mvaIsolationLoosev2Token_,mvaIsoLoosev2);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoMediumv2;
  evt.getByToken(mvaIsolationMediumv2Token_,mvaIsoMediumv2);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoTightv2;
  evt.getByToken(mvaIsolationTightv2Token_,mvaIsoTightv2);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoVTightv2;
  evt.getByToken(mvaIsolationVTightv2Token_,mvaIsoVTightv2);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVTightv2;
  evt.getByToken(mvaIsolationVVTightv2Token_,mvaIsoVVTightv2);

//newDM
    edm::Handle<pat::PATTauDiscriminator> mvaIsoRawv2newDM;
    evt.getByToken(mvaIsolationv2TokennewDM_,mvaIsoRawv2newDM);
    
    edm::Handle<pat::PATTauDiscriminator> mvaIsoVVLoosev2newDM;
    evt.getByToken(mvaIsolationVVLoosev2TokennewDM_,mvaIsoVVLoosev2newDM);
    
    edm::Handle<pat::PATTauDiscriminator> mvaIsoVLoosev2newDM;
    evt.getByToken(mvaIsolationVLoosev2TokennewDM_,mvaIsoVLoosev2newDM);
    
    edm::Handle<pat::PATTauDiscriminator> mvaIsoLoosev2newDM;
    evt.getByToken(mvaIsolationLoosev2TokennewDM_,mvaIsoLoosev2newDM);
    
    edm::Handle<pat::PATTauDiscriminator> mvaIsoMediumv2newDM;
    evt.getByToken(mvaIsolationMediumv2TokennewDM_,mvaIsoMediumv2newDM);
    
    edm::Handle<pat::PATTauDiscriminator> mvaIsoTightv2newDM;
    evt.getByToken(mvaIsolationTightv2TokennewDM_,mvaIsoTightv2newDM);
    
    edm::Handle<pat::PATTauDiscriminator> mvaIsoVTightv2newDM;
    evt.getByToken(mvaIsolationVTightv2TokennewDM_,mvaIsoVTightv2newDM);
    
    edm::Handle<pat::PATTauDiscriminator> mvaIsoVVTightv2newDM;
    evt.getByToken(mvaIsolationVVTightv2TokennewDM_,mvaIsoVVTightv2newDM);
    


//


  edm::Handle<pat::TauCollection> inTaus;
  evt.getByToken(srcTauToken_, inTaus);
  output->reserve(inTaus->size());


  for(size_t iTau = 0; iTau < inTaus->size(); iTau++) {
      pat::Tau tau = inTaus->at(iTau);
      float valueAODisoRaw = tau.tauID("byIsolationMVArun2v1DBoldDMwLTraw");

      pat::TauRef tauRef(inTaus,iTau);
      float valueAODRefIsoRaw = tauRef->tauID("byIsolationMVArun2v1DBoldDMwLTraw");

      // If for some reason our taus don't align 
      // don't fill with a garbage value, instead skip
      // and fill with -10
      if(valueAODisoRaw == valueAODRefIsoRaw) {

        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTrawRerun", (*mvaIsoRaw)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTVLooseRerun", (*mvaIsoVLoose)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTLooseRerun", (*mvaIsoLoose)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTMediumRerun", (*mvaIsoMedium)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTTightRerun", (*mvaIsoTight)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTVTightRerun", (*mvaIsoVTight)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTVVTightRerun", (*mvaIsoVVTight)[tauRef]);

        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTrawRerun", (*mvaIsoRawv2)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTVVLooseRerun", (*mvaIsoVVLoosev2)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTVLooseRerun", (*mvaIsoVLoosev2)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTLooseRerun", (*mvaIsoLoosev2)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTMediumRerun", (*mvaIsoMediumv2)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTTightRerun", (*mvaIsoTightv2)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTVTightRerun", (*mvaIsoVTightv2)[tauRef]);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTVVTightRerun", (*mvaIsoVVTightv2)[tauRef]);

    //newDM
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTrawRerun", (*mvaIsoRawv2newDM)[tauRef]);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTVVLooseRerun", (*mvaIsoVVLoosev2newDM)[tauRef]);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTVLooseRerun", (*mvaIsoVLoosev2newDM)[tauRef]);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTLooseRerun", (*mvaIsoLoosev2newDM)[tauRef]);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTMediumRerun", (*mvaIsoMediumv2newDM)[tauRef]);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTTightRerun", (*mvaIsoTightv2newDM)[tauRef]);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTVTightRerun", (*mvaIsoVTightv2newDM)[tauRef]);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTVVTightRerun", (*mvaIsoVVTightv2newDM)[tauRef]);

      



      } // taus match
      // taus don't match
      else { 

        std::cout<<"Tau " << iTau << " didn't match: old raw iso: " << valueAODisoRaw << " old raw iso ref: " << valueAODRefIsoRaw << std::endl;
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTrawRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTVLooseRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTLooseRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTMediumRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTTightRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTVTightRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v1DBoldDMwLTVVTightRerun", -10.0);

        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTrawRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTVVLooseRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTVLooseRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTLooseRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTMediumRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTTightRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTVTightRerun", -10.0);
        tau.addUserFloat("byIsolationMVArun2v2DBoldDMwLTVVTightRerun", -10.0);

      //newDM
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTrawRerun", -10.0);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTVVLooseRerun", -10.0);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTVLooseRerun", -10.0);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTLooseRerun", -10.0);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTMediumRerun", -10.0);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTTightRerun", -10.0);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTVTightRerun", -10.0);
      tau.addUserFloat("byIsolationMVArun2v2DBnewDMwLTVVTightRerun", -10.0);
          


      } // end taus don't match
      output->push_back(tau);
  } // end tau loop

  evt.put(std::move(output));
}



#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODTauRerunIDEmbedder);
