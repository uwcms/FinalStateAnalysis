#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

class MiniAODJERSystematicsEmbedder : public edm::EDProducer {
  public:
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;
    typedef reco::Candidate::LorentzVector LorentzVector;

    MiniAODJERSystematicsEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODJERSystematicsEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<pat::Jet> > srcToken_;
    edm::EDGetTokenT<edm::View<pat::Jet> > upToken_;
    edm::EDGetTokenT<edm::View<pat::Jet> > downToken_;
};

MiniAODJERSystematicsEmbedder::MiniAODJERSystematicsEmbedder(const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("src"));
  upToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("up"));
  downToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("down"));
  produces<pat::JetCollection>();
}
void MiniAODJERSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > jets;
  evt.getByToken(srcToken_, jets);
  size_t nJets = jets->size();

  edm::Handle<edm::View<pat::Jet> > jetsU;
  evt.getByToken(upToken_, jetsU);
  edm::Handle<edm::View<pat::Jet> > jetsD;
  evt.getByToken(downToken_, jetsD);

  output->reserve(jets->size());

  for (size_t i = 0; i < nJets; ++i) {
    pat::Jet jet = jets->at(i);
    pat::Jet jet_up = jetsU->at(i);
    pat::Jet jet_down = jetsD->at(i);
    float ptup=jet_up.pt();
    float ptdown=jet_down.pt();
    jet.addUserFloat("jer+", ptup);
    jet.addUserFloat("jer-", ptdown);
    output->push_back(jet); // make our own copy
  }

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJERSystematicsEmbedder);
