//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODMuonHZZIDDecider.cc                                             //
//                                                                          //
//   Embeds muon ID and isolation decisions as userfloats                   //
//       (1 for true, 0 for false), for use in other modules using          //
//       HZZ4l2015 definitions.                                             //
//                                                                          //
//   Author: Nate Woods, U. Wisconsin                                       //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////


// system includes
#include <memory>
#include <vector>
#include <iostream>

// CMS includes
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


class MiniAODMuonHZZIDDecider : public edm::EDProducer
{
public:
  explicit MiniAODMuonHZZIDDecider(const edm::ParameterSet&);
  ~MiniAODMuonHZZIDDecider() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  bool passKinematics(const edm::Ptr<pat::Muon>& mu) const;
  bool passVertex(const edm::Ptr<pat::Muon>& mu) const;
  bool passType(const edm::Ptr<pat::Muon>& mu) const;
  float PFRelIsoDBNoFSR(const edm::Ptr<pat::Muon>& mu) const;

  // Data
  edm::EDGetTokenT<edm::View<pat::Muon> > muonCollectionToken_;
  std::string idLabel_; // label for the decision userfloat
  std::string isoLabel_;
  const edm::EDGetTokenT<reco::VertexCollection> vtxSrcToken_; // primary vertex (for veto PV and SIP cuts)
  edm::Handle<reco::VertexCollection> vertices;
  std::auto_ptr<std::vector<pat::Muon> > out; // Collection we'll output at the end

  double ptCut;
  double etaCut;
  double sipCut;
  double pvDXYCut;
  double pvDZCut;
  double isoCut;

};


// Constructors and destructors

MiniAODMuonHZZIDDecider::MiniAODMuonHZZIDDecider(const edm::ParameterSet& iConfig):
  muonCollectionToken_(consumes<edm::View<pat::Muon> >(iConfig.exists("src") ? 
						       iConfig.getParameter<edm::InputTag>("src") :
						       edm::InputTag("slimmedMuons"))),
  idLabel_(iConfig.exists("idLabel") ?
	   iConfig.getParameter<std::string>("idLabel") :
	   std::string("HZZ4lIDPass")),
  isoLabel_(iConfig.exists("isoLabel") ?
	   iConfig.getParameter<std::string>("isoLabel") :
	   std::string("HZZ4lIsoPass")),
  vtxSrcToken_(consumes<reco::VertexCollection>(iConfig.exists("vtxSrc") ? iConfig.getParameter<edm::InputTag>("vtxSrc") : edm::InputTag("selectedPrimaryVertex"))),
  ptCut(iConfig.exists("ptCut") ? iConfig.getParameter<double>("ptCut") : 5.),
  etaCut(iConfig.exists("etaCut") ? iConfig.getParameter<double>("etaCut") : 2.4),
  sipCut(iConfig.exists("sipCut") ? iConfig.getParameter<double>("sipCut") : 4.),
  pvDXYCut(iConfig.exists("pvDXYCut") ? iConfig.getParameter<double>("pvDXYCut") : 0.5),
  pvDZCut(iConfig.exists("pvDZCut") ? iConfig.getParameter<double>("pvDZCut") : 1.),
  isoCut(iConfig.exists("isoCut") ? iConfig.getParameter<double>("isoCut") : 0.4)
{
  produces<std::vector<pat::Muon> >();
}


void MiniAODMuonHZZIDDecider::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Muon> >(new std::vector<pat::Muon>);

  edm::Handle<edm::View<pat::Muon> > muonsIn;
  iEvent.getByToken(muonCollectionToken_, muonsIn);

  iEvent.getByToken(vtxSrcToken_,vertices);


  for(edm::View<pat::Muon>::const_iterator mi = muonsIn->begin();
      mi != muonsIn->end(); mi++) // loop over muons
    {
      const edm::Ptr<pat::Muon> mptr(muonsIn, mi - muonsIn->begin());

      out->push_back(*mi); // copy muon to save correctly in event

      bool idResult = (passKinematics(mptr) && passVertex(mptr) && passType(mptr));
      out->back().addUserFloat(idLabel_, float(idResult)); // 1 for true, 0 for false

      out->back().addUserFloat(idLabel_+"Tight", float(idResult && mi->isPFMuon())); // 1 for true, 0 for false
      
      bool isoResult = (PFRelIsoDBNoFSR(mptr) < isoCut);
      out->back().addUserFloat(isoLabel_, float(isoResult)); // 1 for true, 0 for false
    }

  iEvent.put(out);
}


bool MiniAODMuonHZZIDDecider::passKinematics(const edm::Ptr<pat::Muon>& mu) const
{
  bool result = (mu->pt() > ptCut);
  result = (result && fabs(mu->eta()) < etaCut);
  return result;
}


bool MiniAODMuonHZZIDDecider::passVertex(const edm::Ptr<pat::Muon>& mu) const
{
  return (fabs(mu->dB(pat::Muon::PV3D))/mu->edB(pat::Muon::PV3D) < sipCut && 
	  fabs(mu->muonBestTrack()->dxy(vertices->at(0).position())) < pvDXYCut &&
	  fabs(mu->muonBestTrack()->dz(vertices->at(0).position())) < pvDZCut);
}


bool MiniAODMuonHZZIDDecider::passType(const edm::Ptr<pat::Muon>& mu) const
{
  // Global muon or (arbitrated) tracker muon
  return (mu->isGlobalMuon() || (mu->isTrackerMuon() && mu->numberOfMatchedStations() > 0)) && mu->muonBestTrackType() != 2;
}


float MiniAODMuonHZZIDDecider::PFRelIsoDBNoFSR(const edm::Ptr<pat::Muon>& mu) const
{
  float chHadIso = mu->chargedHadronIso();
  float nHadIso = mu->neutralHadronIso();
  float phoIso = mu->photonIso();
  float puCorrection = 0.5 * mu->puChargedHadronIso();
  
  float neutralIso = nHadIso + phoIso - puCorrection;
  if(neutralIso < 0.)
    neutralIso = 0.;

  return ((chHadIso + neutralIso) / mu->pt());
}


void MiniAODMuonHZZIDDecider::beginJob()
{}


void MiniAODMuonHZZIDDecider::endJob()
{}


void
MiniAODMuonHZZIDDecider::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODMuonHZZIDDecider);








