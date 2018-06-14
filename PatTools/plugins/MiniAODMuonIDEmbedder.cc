/*
 * Embeds the muon ID as recommended by the Muon POG
 * Author: Devin N. Taylor, UW-Madison
 */

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include <math.h>

// class declaration
class MiniAODMuonIDEmbedder : public edm::EDProducer {
  public:
    explicit MiniAODMuonIDEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODMuonIDEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);

  private:
    edm::EDGetTokenT<pat::MuonCollection> muonsCollection_;
    edm::EDGetTokenT<reco::VertexCollection> vtxToken_;
    reco::Vertex pv_;
};

// class member functions
MiniAODMuonIDEmbedder::MiniAODMuonIDEmbedder(const edm::ParameterSet& pset) {
  muonsCollection_ = consumes<pat::MuonCollection>(pset.getParameter<edm::InputTag>("src"));
  vtxToken_            = consumes<reco::VertexCollection>(pset.getParameter<edm::InputTag>("vertices"));

  produces<pat::MuonCollection>();
}

void MiniAODMuonIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<std::vector<pat::Muon>> muonsCollection;
  evt.getByToken(muonsCollection_ , muonsCollection);

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByToken(vtxToken_, vertices);
  if (vertices->empty()) return; // skip the event if no PV found
  pv_ = vertices->front();

  const std::vector<pat::Muon> * muons = muonsCollection.product();

  unsigned int nbMuon =  muons->size();

  std::unique_ptr<pat::MuonCollection> output(new pat::MuonCollection);
  output->reserve(nbMuon);

  for(unsigned i = 0 ; i < nbMuon; i++){
    pat::Muon muon(muons->at(i));

    muon.addUserInt("tightID",muon.isTightMuon(pv_));
    muon.addUserInt("CutBasedIdLoose",muon.passed(reco::Muon::CutBasedIdLoose));
    muon.addUserInt("CutBasedIdMedium",muon.passed(reco::Muon::CutBasedIdMedium));
    muon.addUserInt("CutBasedIdMediumPrompt",muon.passed(reco::Muon::CutBasedIdMediumPrompt));
    muon.addUserInt("CutBasedIdTight",muon.passed(reco::Muon::CutBasedIdTight));
    muon.addUserInt("CutBasedIdGlobalHighPt",muon.passed(reco::Muon::CutBasedIdGlobalHighPt));
    muon.addUserInt("CutBasedIdTrkHighPt",muon.passed(reco::Muon::CutBasedIdTrkHighPt));
    muon.addUserInt("PFIsoVeryLoose",muon.passed(reco::Muon::PFIsoVeryLoose));
    muon.addUserInt("PFIsoLoose",muon.passed(reco::Muon::PFIsoLoose));
    muon.addUserInt("PFIsoMedium",muon.passed(reco::Muon::PFIsoMedium));
    muon.addUserInt("PFIsoTight",muon.passed(reco::Muon::PFIsoTight));
    muon.addUserInt("PFIsoVeryTight",muon.passed(reco::Muon::PFIsoVeryTight));
    // for CMSSW_10_1_X muon.addUserInt("PFIsoVeryVeryTight",muon.passed(reco::Muon::PFIsoVeryVeryTight));
    muon.addUserInt("TkIsoLoose",muon.passed(reco::Muon::TkIsoLoose));
    muon.addUserInt("TkIsoTight",muon.passed(reco::Muon::TkIsoTight));
    muon.addUserInt("SoftCutBasedId",muon.passed(reco::Muon::SoftCutBasedId));
    // for CMSSW_10_1_X muon.addUserInt("SoftMvaId",muon.passed(reco::Muon::SoftMvaId));
    muon.addUserInt("MvaLoose",muon.passed(reco::Muon::MvaLoose));
    muon.addUserInt("MvaMedium",muon.passed(reco::Muon::MvaMedium));
    muon.addUserInt("MvaTight",muon.passed(reco::Muon::MvaTight));
    muon.addUserInt("MiniIsoLoose",muon.passed(reco::Muon::MiniIsoLoose));
    muon.addUserInt("MiniIsoMedium",muon.passed(reco::Muon::MiniIsoMedium));
    muon.addUserInt("MiniIsoTight",muon.passed(reco::Muon::MiniIsoTight));
    muon.addUserInt("MiniIsoVeryTight",muon.passed(reco::Muon::MiniIsoVeryTight));
    // for CMSSW_10_1_X muon.addUserInt("TriggerIdLoose",muon.passed(reco::Muon::TriggerIdLoose));
    // for CMSSW_10_1_X muon.addUserInt("InTimeMuon",muon.passed(reco::Muon::InTimeMuon));
    // for CMSSW_10_1_X muon.addUserInt("MultiIsoLoose",muon.passed(reco::Muon::MultiIsoLoose));
    // for CMSSW_10_1_X muon.addUserInt("MultiIsoMedium",muon.passed(reco::Muon::MultiIsoMedium));

    output->push_back(muon);
  }

  evt.put(std::move(output));
}

// define plugin
DEFINE_FWK_MODULE(MiniAODMuonIDEmbedder);
