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
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationDeepVSmurawToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVLooseDeepVSmuToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationLooseDeepVSmuToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationMediumDeepVSmuToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationTightDeepVSmuToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVTightDeepVSmuToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVTightDeepVSmuToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationDeepVSjetrawToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVVLooseDeepVSjetToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVLooseDeepVSjetToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVLooseDeepVSjetToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationLooseDeepVSjetToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationMediumDeepVSjetToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationTightDeepVSjetToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVTightDeepVSjetToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVTightDeepVSjetToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationDeepVSerawToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVVLooseDeepVSeToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVLooseDeepVSeToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVLooseDeepVSeToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationLooseDeepVSeToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationMediumDeepVSeToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationTightDeepVSeToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVTightDeepVSeToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVTightDeepVSeToken_;

};

MiniAODTauRerunIDEmbedder::MiniAODTauRerunIDEmbedder(const edm::ParameterSet& pset) {
  srcTauToken_              = consumes<pat::TauCollection>(pset.getParameter<edm::InputTag>("src"));
  mvaIsolationDeepVSmurawToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byDeepTau2017v2p1VSmuraw"));
  mvaIsolationVLooseDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVLooseDeepTau2017v2p1VSmu"));
  mvaIsolationLooseDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byLooseDeepTau2017v2p1VSmu"));
  mvaIsolationMediumDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byMediumDeepTau2017v2p1VSmu"));
  mvaIsolationTightDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byTightDeepTau2017v2p1VSmu"));
  mvaIsolationVTightDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVTightDeepTau2017v2p1VSmu"));
  mvaIsolationVVTightDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVTightDeepTau2017v2p1VSmu"));
  mvaIsolationDeepVSerawToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byDeepTau2017v2p1VSeraw"));
  mvaIsolationVVVLooseDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVVLooseDeepTau2017v2p1VSe"));
  mvaIsolationVVLooseDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVLooseDeepTau2017v2p1VSe"));
  mvaIsolationVLooseDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVLooseDeepTau2017v2p1VSe"));
  mvaIsolationLooseDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byLooseDeepTau2017v2p1VSe"));
  mvaIsolationMediumDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byMediumDeepTau2017v2p1VSe"));
  mvaIsolationTightDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byTightDeepTau2017v2p1VSe"));
  mvaIsolationVTightDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVTightDeepTau2017v2p1VSe"));
  mvaIsolationVVTightDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVTightDeepTau2017v2p1VSe"));
  mvaIsolationDeepVSjetrawToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byDeepTau2017v2p1VSjetraw"));
  mvaIsolationVVVLooseDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVVLooseDeepTau2017v2p1VSjet"));
  mvaIsolationVVLooseDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVLooseDeepTau2017v2p1VSjet"));
  mvaIsolationVLooseDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVLooseDeepTau2017v2p1VSjet"));
  mvaIsolationLooseDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byLooseDeepTau2017v2p1VSjet"));
  mvaIsolationMediumDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byMediumDeepTau2017v2p1VSjet"));
  mvaIsolationTightDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byTightDeepTau2017v2p1VSjet"));
  mvaIsolationVTightDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVTightDeepTau2017v2p1VSjet"));
  mvaIsolationVVTightDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVTightDeepTau2017v2p1VSjet"));


  produces<pat::TauCollection>();

}

void MiniAODTauRerunIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<pat::TauCollection> output(new pat::TauCollection);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoDeepVSmuraw;
  evt.getByToken(mvaIsolationDeepVSmurawToken_,mvaIsoDeepVSmuraw);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVLooseDeepVSmu;
  evt.getByToken(mvaIsolationVLooseDeepVSmuToken_,mvaIsoVLooseDeepVSmu);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoLooseDeepVSmu;
  evt.getByToken(mvaIsolationLooseDeepVSmuToken_,mvaIsoLooseDeepVSmu);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoMediumDeepVSmu;
  evt.getByToken(mvaIsolationMediumDeepVSmuToken_,mvaIsoMediumDeepVSmu);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoTightDeepVSmu;
  evt.getByToken(mvaIsolationTightDeepVSmuToken_,mvaIsoTightDeepVSmu);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVTightDeepVSmu;
  evt.getByToken(mvaIsolationVTightDeepVSmuToken_,mvaIsoVTightDeepVSmu);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVTightDeepVSmu;
  evt.getByToken(mvaIsolationVVTightDeepVSmuToken_,mvaIsoVVTightDeepVSmu);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoDeepVSjetraw;
  evt.getByToken(mvaIsolationDeepVSjetrawToken_,mvaIsoDeepVSjetraw);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVVLooseDeepVSjet;
  evt.getByToken(mvaIsolationVVVLooseDeepVSjetToken_,mvaIsoVVVLooseDeepVSjet);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVLooseDeepVSjet;
  evt.getByToken(mvaIsolationVVLooseDeepVSjetToken_,mvaIsoVVLooseDeepVSjet);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVLooseDeepVSjet;
  evt.getByToken(mvaIsolationVLooseDeepVSjetToken_,mvaIsoVLooseDeepVSjet);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoLooseDeepVSjet;
  evt.getByToken(mvaIsolationLooseDeepVSjetToken_,mvaIsoLooseDeepVSjet);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoMediumDeepVSjet;
  evt.getByToken(mvaIsolationMediumDeepVSjetToken_,mvaIsoMediumDeepVSjet);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoTightDeepVSjet;
  evt.getByToken(mvaIsolationTightDeepVSjetToken_,mvaIsoTightDeepVSjet);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVTightDeepVSjet;
  evt.getByToken(mvaIsolationVTightDeepVSjetToken_,mvaIsoVTightDeepVSjet);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVTightDeepVSjet;
  evt.getByToken(mvaIsolationVVTightDeepVSjetToken_,mvaIsoVVTightDeepVSjet);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoDeepVSeraw;
  evt.getByToken(mvaIsolationDeepVSerawToken_,mvaIsoDeepVSeraw);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVVLooseDeepVSe;
  evt.getByToken(mvaIsolationVVVLooseDeepVSeToken_,mvaIsoVVVLooseDeepVSe);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVLooseDeepVSe;
  evt.getByToken(mvaIsolationVVLooseDeepVSeToken_,mvaIsoVVLooseDeepVSe);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVLooseDeepVSe;
  evt.getByToken(mvaIsolationVLooseDeepVSeToken_,mvaIsoVLooseDeepVSe);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoLooseDeepVSe;
  evt.getByToken(mvaIsolationLooseDeepVSeToken_,mvaIsoLooseDeepVSe);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoMediumDeepVSe;
  evt.getByToken(mvaIsolationMediumDeepVSeToken_,mvaIsoMediumDeepVSe);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoTightDeepVSe;
  evt.getByToken(mvaIsolationTightDeepVSeToken_,mvaIsoTightDeepVSe);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVTightDeepVSe;
  evt.getByToken(mvaIsolationVTightDeepVSeToken_,mvaIsoVTightDeepVSe);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVTightDeepVSe;
  evt.getByToken(mvaIsolationVVTightDeepVSeToken_,mvaIsoVVTightDeepVSe);

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

        tau.addUserFloat("byDeepTau2017v2p1VSmuraw", (*mvaIsoDeepVSmuraw)[tauRef]);
        tau.addUserFloat("byVLooseDeepTau2017v2p1VSmu", (*mvaIsoVLooseDeepVSmu)[tauRef]);
        tau.addUserFloat("byLooseDeepTau2017v2p1VSmu", (*mvaIsoLooseDeepVSmu)[tauRef]);
        tau.addUserFloat("byMediumDeepTau2017v2p1VSmu", (*mvaIsoMediumDeepVSmu)[tauRef]);
        tau.addUserFloat("byTightDeepTau2017v2p1VSmu", (*mvaIsoTightDeepVSmu)[tauRef]);
        tau.addUserFloat("byVTightDeepTau2017v2p1VSmu", (*mvaIsoVTightDeepVSmu)[tauRef]);
        tau.addUserFloat("byVVTightDeepTau2017v2p1VSmu", (*mvaIsoVVTightDeepVSmu)[tauRef]);

        tau.addUserFloat("byDeepTau2017v2p1VSeraw", (*mvaIsoDeepVSeraw)[tauRef]);
        tau.addUserFloat("byVVVLooseDeepTau2017v2p1VSe", (*mvaIsoVVVLooseDeepVSe)[tauRef]);
        tau.addUserFloat("byVVLooseDeepTau2017v2p1VSe", (*mvaIsoVVLooseDeepVSe)[tauRef]);
        tau.addUserFloat("byVLooseDeepTau2017v2p1VSe", (*mvaIsoVLooseDeepVSe)[tauRef]);
        tau.addUserFloat("byLooseDeepTau2017v2p1VSe", (*mvaIsoLooseDeepVSe)[tauRef]);
        tau.addUserFloat("byMediumDeepTau2017v2p1VSe", (*mvaIsoMediumDeepVSe)[tauRef]);
        tau.addUserFloat("byTightDeepTau2017v2p1VSe", (*mvaIsoTightDeepVSe)[tauRef]);
        tau.addUserFloat("byVTightDeepTau2017v2p1VSe", (*mvaIsoVTightDeepVSe)[tauRef]);
        tau.addUserFloat("byVVTightDeepTau2017v2p1VSe", (*mvaIsoVVTightDeepVSe)[tauRef]);

        tau.addUserFloat("byDeepTau2017v2p1VSjetraw", (*mvaIsoDeepVSjetraw)[tauRef]);
        tau.addUserFloat("byVVVLooseDeepTau2017v2p1VSjet", (*mvaIsoVVVLooseDeepVSjet)[tauRef]);
        tau.addUserFloat("byVVLooseDeepTau2017v2p1VSjet", (*mvaIsoVVLooseDeepVSjet)[tauRef]);
        tau.addUserFloat("byVLooseDeepTau2017v2p1VSjet", (*mvaIsoVLooseDeepVSjet)[tauRef]);
        tau.addUserFloat("byLooseDeepTau2017v2p1VSjet", (*mvaIsoLooseDeepVSjet)[tauRef]);
        tau.addUserFloat("byMediumDeepTau2017v2p1VSjet", (*mvaIsoMediumDeepVSjet)[tauRef]);
        tau.addUserFloat("byTightDeepTau2017v2p1VSjet", (*mvaIsoTightDeepVSjet)[tauRef]);
        tau.addUserFloat("byVTightDeepTau2017v2p1VSjet", (*mvaIsoVTightDeepVSjet)[tauRef]);
        tau.addUserFloat("byVVTightDeepTau2017v2p1VSjet", (*mvaIsoVVTightDeepVSjet)[tauRef]);


      } // taus match
      // taus don't match
      else { 

        std::cout<<"Tau " << iTau << " didn't match: old raw iso: " << valueAODisoRaw << " old raw iso ref: " << valueAODRefIsoRaw << std::endl;

        tau.addUserFloat("byDeepTau2017v2p1VSmuraw", -10.0);
        tau.addUserFloat("byLooseDeepTau2017v2p1VSmu", -10.0);
        tau.addUserFloat("byMediumDeepTau2017v2p1VSmu", -10.0);
        tau.addUserFloat("byTightDeepTau2017v2p1VSmu", -10.0);
        tau.addUserFloat("byVTightDeepTau2017v2p1VSmu", -10.0);
        tau.addUserFloat("byVVTightDeepTau2017v2p1VSmu", -10.0);
        tau.addUserFloat("byVLooseDeepTau2017v2p1VSmu", -10.0);

        tau.addUserFloat("byDeepTau2017v2p1VSjetraw", -10.0);
        tau.addUserFloat("byVVVLooseDeepTau2017v2p1VSjet", -10.0);
        tau.addUserFloat("byVVLooseDeepTau2017v2p1VSjet", -10.0);
        tau.addUserFloat("byLooseDeepTau2017v2p1VSjet", -10.0);
        tau.addUserFloat("byMediumDeepTau2017v2p1VSjet", -10.0);
        tau.addUserFloat("byTightDeepTau2017v2p1VSjet", -10.0);
        tau.addUserFloat("byVTightDeepTau2017v2p1VSjet", -10.0);
        tau.addUserFloat("byVVTightDeepTau2017v2p1VSjet", -10.0);
        tau.addUserFloat("byVLooseDeepTau2017v2p1VSjet", -10.0);

        tau.addUserFloat("byDeepTau2017v2p1VSeraw", -10.0);
        tau.addUserFloat("byVVVLooseDeepTau2017v2p1VSe", -10.0);
        tau.addUserFloat("byVVLooseDeepTau2017v2p1VSe", -10.0);
        tau.addUserFloat("byLooseDeepTau2017v2p1VSe", -10.0);
        tau.addUserFloat("byMediumDeepTau2017v2p1VSe", -10.0);
        tau.addUserFloat("byTightDeepTau2017v2p1VSe", -10.0);
        tau.addUserFloat("byVTightDeepTau2017v2p1VSe", -10.0);
        tau.addUserFloat("byVVTightDeepTau2017v2p1VSe", -10.0);
        tau.addUserFloat("byVLooseDeepTau2017v2p1VSe", -10.0);


      } // end taus don't match
      output->push_back(tau);
  } // end tau loop

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODTauRerunIDEmbedder);
