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
    //edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationDpfToken_;
    //edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationTightDpfToken_;
    //edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationDpfv0Token_;
    //edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationTightDpfv0Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationDeepVSmurawToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVVLooseDeepVSmuToken_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaIsolationVVLooseDeepVSmuToken_;
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

    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaAgainstElectronMVA6Raw2018Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaAgainstElectronMVA6category2018Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaAgainstElectronVLooseMVA62018Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaAgainstElectronLooseMVA62018Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaAgainstElectronMediumMVA62018Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaAgainstElectronTightMVA62018Token_;
    edm::EDGetTokenT<pat::PATTauDiscriminator> mvaAgainstElectronVTightMVA62018Token_;
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
  //mvaIsolationDpfToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byDpfTau2016v1VSallraw"));
  //mvaIsolationTightDpfToken_ = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byTightDpfTau2016v1VSall"));
  //mvaIsolationDpfv0Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byDpfTau2016v0VSallraw"));
  //mvaIsolationTightDpfv0Token_ = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byTightDpfTau2016v0VSall"));
  mvaIsolationDeepVSmurawToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byDeepTau2017v2VSmuraw"));
  mvaIsolationVVVLooseDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVVLooseDeepTau2017v2VSmu"));
  mvaIsolationVVLooseDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVLooseDeepTau2017v2VSmu"));
  mvaIsolationVLooseDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVLooseDeepTau2017v2VSmu"));
  mvaIsolationLooseDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byLooseDeepTau2017v2VSmu"));
  mvaIsolationMediumDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byMediumDeepTau2017v2VSmu"));
  mvaIsolationTightDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byTightDeepTau2017v2VSmu"));
  mvaIsolationVTightDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVTightDeepTau2017v2VSmu"));
  mvaIsolationVVTightDeepVSmuToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVTightDeepTau2017v2VSmu"));
  mvaIsolationDeepVSerawToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byDeepTau2017v2VSeraw"));
  mvaIsolationVVVLooseDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVVLooseDeepTau2017v2VSe"));
  mvaIsolationVVLooseDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVLooseDeepTau2017v2VSe"));
  mvaIsolationVLooseDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVLooseDeepTau2017v2VSe"));
  mvaIsolationLooseDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byLooseDeepTau2017v2VSe"));
  mvaIsolationMediumDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byMediumDeepTau2017v2VSe"));
  mvaIsolationTightDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byTightDeepTau2017v2VSe"));
  mvaIsolationVTightDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVTightDeepTau2017v2VSe"));
  mvaIsolationVVTightDeepVSeToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVTightDeepTau2017v2VSe"));
  mvaIsolationDeepVSjetrawToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byDeepTau2017v2VSjetraw"));
  mvaIsolationVVVLooseDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVVLooseDeepTau2017v2VSjet"));
  mvaIsolationVVLooseDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVLooseDeepTau2017v2VSjet"));
  mvaIsolationVLooseDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVLooseDeepTau2017v2VSjet"));
  mvaIsolationLooseDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byLooseDeepTau2017v2VSjet"));
  mvaIsolationMediumDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byMediumDeepTau2017v2VSjet"));
  mvaIsolationTightDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byTightDeepTau2017v2VSjet"));
  mvaIsolationVTightDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVTightDeepTau2017v2VSjet"));
  mvaIsolationVVTightDeepVSjetToken_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("byVVTightDeepTau2017v2VSjet"));

  mvaAgainstElectronMVA6Raw2018Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("againstElectronMVA6Raw2018"));
  mvaAgainstElectronMVA6category2018Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("againstElectronMVA6category2018"));
  mvaAgainstElectronVLooseMVA62018Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("againstElectronVLooseMVA62018"));
  mvaAgainstElectronLooseMVA62018Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("againstElectronLooseMVA62018"));
  mvaAgainstElectronMediumMVA62018Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("againstElectronMediumMVA62018"));
  mvaAgainstElectronTightMVA62018Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("againstElectronTightMVA62018"));
  mvaAgainstElectronVTightMVA62018Token_  = consumes<pat::PATTauDiscriminator>(pset.getParameter<edm::InputTag>("againstElectronVTightMVA62018"));

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

  //edm::Handle<pat::PATTauDiscriminator> mvaIsoDpf;
  //evt.getByToken(mvaIsolationDpfToken_,mvaIsoDpf);

  //edm::Handle<pat::PATTauDiscriminator> mvaIsoTightDpf;
  //evt.getByToken(mvaIsolationTightDpfToken_,mvaIsoTightDpf);

  //edm::Handle<pat::PATTauDiscriminator> mvaIsoDpfv0;
  //evt.getByToken(mvaIsolationDpfv0Token_,mvaIsoDpfv0);

  //edm::Handle<pat::PATTauDiscriminator> mvaIsoTightDpfv0;
  //evt.getByToken(mvaIsolationTightDpfv0Token_,mvaIsoTightDpfv0);

  edm::Handle<pat::PATTauDiscriminator> mvaIsoDeepVSmuraw;
  evt.getByToken(mvaIsolationDeepVSmurawToken_,mvaIsoDeepVSmuraw);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVVLooseDeepVSmu;
  evt.getByToken(mvaIsolationVVVLooseDeepVSmuToken_,mvaIsoVVVLooseDeepVSmu);
  edm::Handle<pat::PATTauDiscriminator> mvaIsoVVLooseDeepVSmu;
  evt.getByToken(mvaIsolationVVLooseDeepVSmuToken_,mvaIsoVVLooseDeepVSmu);
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

  edm::Handle<pat::PATTauDiscriminator> mvaAgainstElectronMVA6Raw2018;
  evt.getByToken(mvaAgainstElectronMVA6Raw2018Token_,mvaAgainstElectronMVA6Raw2018);
  edm::Handle<pat::PATTauDiscriminator> mvaAgainstElectronMVA6category2018;
  evt.getByToken(mvaAgainstElectronMVA6category2018Token_,mvaAgainstElectronMVA6category2018);
  edm::Handle<pat::PATTauDiscriminator> mvaAgainstElectronVLooseMVA62018;
  evt.getByToken(mvaAgainstElectronVLooseMVA62018Token_,mvaAgainstElectronVLooseMVA62018);
  edm::Handle<pat::PATTauDiscriminator> mvaAgainstElectronLooseMVA62018;
  evt.getByToken(mvaAgainstElectronLooseMVA62018Token_,mvaAgainstElectronLooseMVA62018);
  edm::Handle<pat::PATTauDiscriminator> mvaAgainstElectronMediumMVA62018;
  evt.getByToken(mvaAgainstElectronMediumMVA62018Token_,mvaAgainstElectronMediumMVA62018);
  edm::Handle<pat::PATTauDiscriminator> mvaAgainstElectronTightMVA62018;
  evt.getByToken(mvaAgainstElectronTightMVA62018Token_,mvaAgainstElectronTightMVA62018);
  edm::Handle<pat::PATTauDiscriminator> mvaAgainstElectronVTightMVA62018;
  evt.getByToken(mvaAgainstElectronVTightMVA62018Token_,mvaAgainstElectronVTightMVA62018);

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

        //tau.addUserFloat("byDpfTau2016v1VSallraw", (*mvaIsoDpf)[tauRef]);
        //tau.addUserFloat("byTightDpfTau2016v1VSall", (*mvaIsoTightDpf)[tauRef]);
        //tau.addUserFloat("byDpfTau2016v0VSallraw", (*mvaIsoDpfv0)[tauRef]);
        //tau.addUserFloat("byTightDpfTau2016v0VSall", (*mvaIsoTightDpfv0)[tauRef]);

        tau.addUserFloat("byDeepTau2017v2VSmuraw", (*mvaIsoDeepVSmuraw)[tauRef]);
        tau.addUserFloat("byVVVLooseDeepTau2017v2VSmu", (*mvaIsoVVVLooseDeepVSmu)[tauRef]);
        tau.addUserFloat("byVVLooseDeepTau2017v2VSmu", (*mvaIsoVVLooseDeepVSmu)[tauRef]);
        tau.addUserFloat("byVLooseDeepTau2017v2VSmu", (*mvaIsoVLooseDeepVSmu)[tauRef]);
        tau.addUserFloat("byLooseDeepTau2017v2VSmu", (*mvaIsoLooseDeepVSmu)[tauRef]);
        tau.addUserFloat("byMediumDeepTau2017v2VSmu", (*mvaIsoMediumDeepVSmu)[tauRef]);
        tau.addUserFloat("byTightDeepTau2017v2VSmu", (*mvaIsoTightDeepVSmu)[tauRef]);
        tau.addUserFloat("byVTightDeepTau2017v2VSmu", (*mvaIsoVTightDeepVSmu)[tauRef]);
        tau.addUserFloat("byVVTightDeepTau2017v2VSmu", (*mvaIsoVVTightDeepVSmu)[tauRef]);

        tau.addUserFloat("byDeepTau2017v2VSeraw", (*mvaIsoDeepVSeraw)[tauRef]);
        tau.addUserFloat("byVVVLooseDeepTau2017v2VSe", (*mvaIsoVVVLooseDeepVSe)[tauRef]);
        tau.addUserFloat("byVVLooseDeepTau2017v2VSe", (*mvaIsoVVLooseDeepVSe)[tauRef]);
        tau.addUserFloat("byVLooseDeepTau2017v2VSe", (*mvaIsoVLooseDeepVSe)[tauRef]);
        tau.addUserFloat("byLooseDeepTau2017v2VSe", (*mvaIsoLooseDeepVSe)[tauRef]);
        tau.addUserFloat("byMediumDeepTau2017v2VSe", (*mvaIsoMediumDeepVSe)[tauRef]);
        tau.addUserFloat("byTightDeepTau2017v2VSe", (*mvaIsoTightDeepVSe)[tauRef]);
        tau.addUserFloat("byVTightDeepTau2017v2VSe", (*mvaIsoVTightDeepVSe)[tauRef]);
        tau.addUserFloat("byVVTightDeepTau2017v2VSe", (*mvaIsoVVTightDeepVSe)[tauRef]);

        tau.addUserFloat("byDeepTau2017v2VSjetraw", (*mvaIsoDeepVSjetraw)[tauRef]);
        tau.addUserFloat("byVVVLooseDeepTau2017v2VSjet", (*mvaIsoVVVLooseDeepVSjet)[tauRef]);
        tau.addUserFloat("byVVLooseDeepTau2017v2VSjet", (*mvaIsoVVLooseDeepVSjet)[tauRef]);
        tau.addUserFloat("byVLooseDeepTau2017v2VSjet", (*mvaIsoVLooseDeepVSjet)[tauRef]);
        tau.addUserFloat("byLooseDeepTau2017v2VSjet", (*mvaIsoLooseDeepVSjet)[tauRef]);
        tau.addUserFloat("byMediumDeepTau2017v2VSjet", (*mvaIsoMediumDeepVSjet)[tauRef]);
        tau.addUserFloat("byTightDeepTau2017v2VSjet", (*mvaIsoTightDeepVSjet)[tauRef]);
        tau.addUserFloat("byVTightDeepTau2017v2VSjet", (*mvaIsoVTightDeepVSjet)[tauRef]);
        tau.addUserFloat("byVVTightDeepTau2017v2VSjet", (*mvaIsoVVTightDeepVSjet)[tauRef]);

        tau.addUserFloat("againstElectronMVA6Raw2018", (*mvaAgainstElectronMVA6Raw2018)[tauRef]);
        tau.addUserFloat("againstElectronMVA6category2018", (*mvaAgainstElectronMVA6category2018)[tauRef]);
        tau.addUserFloat("againstElectronVLooseMVA62018", (*mvaAgainstElectronVLooseMVA62018)[tauRef]);
        tau.addUserFloat("againstElectronLooseMVA62018", (*mvaAgainstElectronLooseMVA62018)[tauRef]);
        tau.addUserFloat("againstElectronMediumMVA62018", (*mvaAgainstElectronMediumMVA62018)[tauRef]);
        tau.addUserFloat("againstElectronTightMVA62018", (*mvaAgainstElectronTightMVA62018)[tauRef]);
        tau.addUserFloat("againstElectronVTightMVA62018", (*mvaAgainstElectronVTightMVA62018)[tauRef]);

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

        //tau.addUserFloat("byDpfTau2016v1VSallraw", -10.0);
        //tau.addUserFloat("byTightDpfTau2016v1VSall", -10.0);
        //tau.addUserFloat("byDpfTau2016v0VSallraw", -10.0);
        //tau.addUserFloat("byTightDpfTau2016v0VSall", -10.0);

        tau.addUserFloat("byDeepTau2017v2VSmuraw", -10.0);
        tau.addUserFloat("byVVVLooseDeepTau2017v2VSmu", -10.0);
        tau.addUserFloat("byVVLooseDeepTau2017v2VSmu", -10.0);
        tau.addUserFloat("byLooseDeepTau2017v2VSmu", -10.0);
        tau.addUserFloat("byMediumDeepTau2017v2VSmu", -10.0);
        tau.addUserFloat("byTightDeepTau2017v2VSmu", -10.0);
        tau.addUserFloat("byVTightDeepTau2017v2VSmu", -10.0);
        tau.addUserFloat("byVVTightDeepTau2017v2VSmu", -10.0);
        tau.addUserFloat("byVLooseDeepTau2017v2VSmu", -10.0);

        tau.addUserFloat("byDeepTau2017v2VSjetraw", -10.0);
        tau.addUserFloat("byVVVLooseDeepTau2017v2VSjet", -10.0);
        tau.addUserFloat("byVVLooseDeepTau2017v2VSjet", -10.0);
        tau.addUserFloat("byLooseDeepTau2017v2VSjet", -10.0);
        tau.addUserFloat("byMediumDeepTau2017v2VSjet", -10.0);
        tau.addUserFloat("byTightDeepTau2017v2VSjet", -10.0);
        tau.addUserFloat("byVTightDeepTau2017v2VSjet", -10.0);
        tau.addUserFloat("byVVTightDeepTau2017v2VSjet", -10.0);
        tau.addUserFloat("byVLooseDeepTau2017v2VSjet", -10.0);

        tau.addUserFloat("byDeepTau2017v2VSeraw", -10.0);
        tau.addUserFloat("byVVVLooseDeepTau2017v2VSe", -10.0);
        tau.addUserFloat("byVVLooseDeepTau2017v2VSe", -10.0);
        tau.addUserFloat("byLooseDeepTau2017v2VSe", -10.0);
        tau.addUserFloat("byMediumDeepTau2017v2VSe", -10.0);
        tau.addUserFloat("byTightDeepTau2017v2VSe", -10.0);
        tau.addUserFloat("byVTightDeepTau2017v2VSe", -10.0);
        tau.addUserFloat("byVVTightDeepTau2017v2VSe", -10.0);
        tau.addUserFloat("byVLooseDeepTau2017v2VSe", -10.0);

        tau.addUserFloat("againstElectronMVA6Raw2018", -10.0);
        tau.addUserFloat("againstElectronMVA6category2018", -10.0);
        tau.addUserFloat("againstElectronVLooseMVA62018", -10.0);
        tau.addUserFloat("againstElectronLooseMVA62018", -10.0);
        tau.addUserFloat("againstElectronMediumMVA62018", -10.0);
        tau.addUserFloat("againstElectronTightMVA62018", -10.0);
        tau.addUserFloat("againstElectronVTightMVA62018", -10.0);

      } // end taus don't match
      output->push_back(tau);
  } // end tau loop

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODTauRerunIDEmbedder);
