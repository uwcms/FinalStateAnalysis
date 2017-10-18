/*
 * =====================================================================================
 *
 *       Filename:  PATMuonPFMuonEmbedder.cc
 *
 *    Description:  Embeds a PF Muon reference into pat::Muon
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"

#include "DataFormats/Common/interface/RefToPtr.h"

class PATMuonPFMuonEmbedder : public edm::EDProducer {
  public:
    PATMuonPFMuonEmbedder(const edm::ParameterSet& pset);
    virtual ~PATMuonPFMuonEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag pfSrc_;
};

PATMuonPFMuonEmbedder::PATMuonPFMuonEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  pfSrc_ = pset.getParameter<edm::InputTag>("pfSrc");

  produces<pat::MuonCollection>();
}

void PATMuonPFMuonEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<pat::MuonCollection> output(new pat::MuonCollection);

  edm::Handle<edm::View<pat::Muon> > muons;
  evt.getByLabel(src_, muons);
  output->reserve(muons->size());

  edm::Handle<reco::PFCandidateCollection> pfCands;
  evt.getByLabel(pfSrc_, pfCands);

  std::vector<reco::PFCandidateRef> pfMuons;
  if (muons->size()) {
    for (size_t ipf = 0; ipf < pfCands->size(); ++ipf) {
      reco::PFCandidateRef ref(pfCands, ipf);
      if (std::abs(ref->pdgId()) == 13)
        pfMuons.push_back(ref);
    }
  }

  for (size_t i = 0; i < muons->size(); ++i) {
    pat::Muon muon = muons->at(i); // make a local copy
    reco::CandidatePtr srcRef = muon.originalObjectRef();
    reco::PFCandidateRef bestCand;
    // Find the best matching muon
    for(size_t iPF = 0; iPF < pfMuons.size(); ++iPF) {
      reco::CandidatePtr pfMuonRef(edm::refToPtr(pfMuons[iPF]->muonRef()));
      if (pfMuonRef == srcRef) {
        bestCand = pfMuons[iPF];
        break;
      }
    }
    muon.setPFCandidateRef(bestCand);
    output->push_back(muon);
  }
  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonPFMuonEmbedder);
