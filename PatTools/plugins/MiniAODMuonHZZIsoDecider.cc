//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODMuonHZZIsoDecider.cc                                            //
//                                                                          //
//   Embeds muon isolation decisions as userfloats                          //
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
#include "DataFormats/Common/interface/View.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


class MiniAODMuonHZZIsoDecider : public edm::EDProducer
{
public:
  explicit MiniAODMuonHZZIsoDecider(const edm::ParameterSet&);
  ~MiniAODMuonHZZIsoDecider() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  float PFRelIsoDBFSR(const edm::Ptr<pat::Muon>& mu) const;

  // Data
  edm::EDGetTokenT<edm::View<pat::Muon> > muonCollectionToken_;
  std::string isoLabel_;
  std::auto_ptr<std::vector<pat::Muon> > out; // Collection we'll output at the end

  const double isoCut;
  const std::string fsrLabel;
  const double isoConeDRMax;
  const double isoConeDRMin;
  
};


// Constructors and destructors

MiniAODMuonHZZIsoDecider::MiniAODMuonHZZIsoDecider(const edm::ParameterSet& iConfig):
  muonCollectionToken_(consumes<edm::View<pat::Muon> >(iConfig.exists("src") ? 
						       iConfig.getParameter<edm::InputTag>("src") :
						       edm::InputTag("slimmedMuons"))),
  isoLabel_(iConfig.exists("isoLabel") ?
            iConfig.getParameter<std::string>("isoLabel") :
            std::string("HZZ4lIsoPass")),
  isoCut(iConfig.exists("isoCut") ? iConfig.getParameter<double>("isoCut") : 0.4),
  fsrLabel(iConfig.exists("fsrLabel") ?
           iConfig.getParameter<std::string>("fsrLabel") :
           std::string("dretFSRCand")),
  isoConeDRMax(iConfig.exists("isoCConeDRMax") ? 
               iConfig.getParameter<double>("isoConeDRMax") : 0.4),
  isoConeDRMin(iConfig.exists("isoCConeDRMin") ? 
               iConfig.getParameter<double>("isoConeDRMin") : 0.01)
{
  produces<std::vector<pat::Muon> >();
}


void MiniAODMuonHZZIsoDecider::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Muon> >(new std::vector<pat::Muon>);

  edm::Handle<edm::View<pat::Muon> > muonsIn;

  iEvent.getByToken(muonCollectionToken_, muonsIn);

  for(edm::View<pat::Muon>::const_iterator mi = muonsIn->begin();
      mi != muonsIn->end(); mi++) // loop over muons
    {
      const edm::Ptr<pat::Muon> mptr(muonsIn, mi - muonsIn->begin());

      out->push_back(*mi); // copy muon to save correctly in event

      bool isoResult = (PFRelIsoDBFSR(mptr) < isoCut);
      out->back().addUserFloat(isoLabel_, float(isoResult)); // 1 for true, 0 for false
    }

  iEvent.put(out);
}


float MiniAODMuonHZZIsoDecider::PFRelIsoDBFSR(const edm::Ptr<pat::Muon>& mu) const
{
  float chHadIso = mu->chargedHadronIso();
  float nHadIso = mu->neutralHadronIso();
  float phoIso = mu->photonIso();
  float puCorrection = 0.5 * mu->puChargedHadronIso();
  
  float fsrCorrection = 0.;
  if(mu->hasUserCand(fsrLabel))
    {
      edm::Ptr<reco::Candidate> fsr = mu->userCand(fsrLabel);
      float fsrDR = reco::deltaR(fsr->p4(), mu->p4());
      if(fsrDR < isoConeDRMin && fsrDR > isoConeDRMin)
        fsrCorrection = fsr->pt();
    }
  
  float neutralIso = nHadIso + phoIso - puCorrection - fsrCorrection;
  if(neutralIso < 0.)
    neutralIso = 0.;

  return ((chHadIso + neutralIso) / mu->pt());
}


void MiniAODMuonHZZIsoDecider::beginJob()
{}


void MiniAODMuonHZZIsoDecider::endJob()
{}


void
MiniAODMuonHZZIsoDecider::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODMuonHZZIsoDecider);








