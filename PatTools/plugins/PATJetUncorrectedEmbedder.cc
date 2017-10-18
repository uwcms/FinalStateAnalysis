/*
 * PATJetUncorrectedEmbedder
 *
 * Embed a userCand into a pat jet which represents the original,
 * uncorrected (JEC), unsmeared pat jet.  Needed to do type 1 met corrections
 * later on.
 *
 * Author: Evan K. Friis, UW Madison
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"

class PATJetUncorrectedEmbedder : public edm::EDProducer {
  public:
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;
    typedef reco::Candidate::LorentzVector LorentzVector;

    PATJetUncorrectedEmbedder(const edm::ParameterSet& pset);
    virtual ~PATJetUncorrectedEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
};

PATJetUncorrectedEmbedder::PATJetUncorrectedEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  produces<pat::JetCollection>();
  produces<ShiftedCandCollection>("uncorrected");
}

void PATJetUncorrectedEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > jets;
  evt.getByLabel(src_, jets);
  size_t nJets = jets->size();

  std::unique_ptr<ShiftedCandCollection> uncorrected(new ShiftedCandCollection);
  uncorrected->reserve(nJets);

  for (size_t i = 0; i < nJets; ++i) {
    const pat::Jet& jet = jets->at(i);
    output->push_back(jet); // make our own copy
    ShiftedCand uncorr = jet;
    LorentzVector uncorrectedP4 = jet.correctedP4("Uncorrected");
    uncorr.setP4(uncorrectedP4);
    uncorrected->push_back(uncorr);
  }
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  PutHandle uncorrectedH = evt.put(std::move(uncorrected), std::string("uncorrected"));

  for (size_t i = 0; i < output->size(); ++i) {
    pat::Jet& jet = output->at(i);
    jet.addUserCand("uncorr", CandidatePtr(uncorrectedH, i));
  }

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATJetUncorrectedEmbedder);
