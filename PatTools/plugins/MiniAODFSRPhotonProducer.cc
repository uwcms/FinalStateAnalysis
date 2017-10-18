////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///														     ///
///    MiniAODFSRPhotonProducer.cc  defines plugin MiniAODFSRPhotonProducer					     ///
///														     ///
///    Copied from https://github.com/VBF-HZZ/UFHZZAnalysisRun2/blob/csa14/FSRPhotons/plugins/FSRPhotonProducer.cc   ///
///           With only the name of the class/plugin changed. I take no credit.                                      ///
///														     ///
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// system include files
#include <memory>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include <DataFormats/MuonReco/interface/Muon.h>
#include "DataFormats/PatCandidates/interface/Muon.h"
#include <DataFormats/GsfTrackReco/interface/GsfTrack.h>
class MiniAODFSRPhotonProducer : public edm::EDProducer
{
public:
  explicit MiniAODFSRPhotonProducer(const edm::ParameterSet&);
  ~MiniAODFSRPhotonProducer();
private:
  virtual void produce(edm::Event&, const edm::EventSetup&);
  edm::EDGetTokenT<reco::CandidateView> srcCands_;
  edm::EDGetTokenT<edm::View<pat::Muon> > muons_;
  double ptThresh_;
  bool extractMuonFSR_;
};
MiniAODFSRPhotonProducer::MiniAODFSRPhotonProducer(const edm::ParameterSet& iConfig):
  srcCands_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("srcCands"))),
  muons_(consumes<edm::View<pat::Muon> >(iConfig.getParameter<edm::InputTag>("muons"))),
  ptThresh_( iConfig.getParameter<double>("ptThresh") ),
  extractMuonFSR_(iConfig.getParameter<bool>("extractMuonFSR"))
{
  produces<reco::PFCandidateCollection>();
}
MiniAODFSRPhotonProducer::~MiniAODFSRPhotonProducer()
{
}
void MiniAODFSRPhotonProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::unique_ptr<reco::PFCandidateCollection> comp( new reco::PFCandidateCollection );
  edm::Handle<reco::CandidateView> cands;
  iEvent.getByToken(srcCands_, cands);
  edm::Handle<edm::View<pat::Muon> > muons;
  if (extractMuonFSR_) iEvent.getByToken(muons_, muons);
  for( reco::CandidateView::const_iterator c = cands->begin(); c != cands->end(); ++c )
    {
      if (c->charge()==0 && c->pdgId() == 22 && c->pt() > ptThresh_)
	{
	  comp->push_back( reco::PFCandidate(0, c->p4(), reco::PFCandidate::gamma));
	  comp->back().setStatus(0);
	}
    }
  // experimental version below, need to be verified.
  if (extractMuonFSR_)
    {
      for( edm::View<pat::Muon>::const_iterator mu=muons->begin(); mu!=muons->end(); ++mu )
	{
	  double mu_energy = mu->calEnergy().emS25;
	  if (abs(mu->pdgId())==13 && mu_energy>0.0)
	    {
	      reco::Particle::PolarLorentzVector p4( mu_energy*mu->pt()/mu->p(), mu->eta(), mu->phi(), 0.);
	      if (p4.pt() > ptThresh_)
		{
		  comp->push_back( reco::PFCandidate(0, reco::Particle::LorentzVector(p4), reco::PFCandidate::gamma) );
		}
	    }
	}
    }
  iEvent.put( std::move(comp) );
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODFSRPhotonProducer);
