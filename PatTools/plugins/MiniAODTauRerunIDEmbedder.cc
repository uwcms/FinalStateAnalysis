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

  produces<pat::TauCollection>();

}

void MiniAODTauRerunIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::TauCollection> output(new pat::TauCollection);

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

      } // end taus don't match
      output->push_back(tau);
  } // end tau loop

  evt.put(output);
}



#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODTauRerunIDEmbedder);
