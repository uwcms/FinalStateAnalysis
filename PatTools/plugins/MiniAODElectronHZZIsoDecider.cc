//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODElectronHZZIsoDecider.c                                         //
//                                                                          //
//   Embeds electron Isolation decisions as userfloats                      //
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
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


class MiniAODElectronHZZIsoDecider : public edm::EDProducer
{
public:
  explicit MiniAODElectronHZZIsoDecider(const edm::ParameterSet&);
  ~MiniAODElectronHZZIsoDecider() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  float PFRelIsoRhoFSR(const edm::Ptr<pat::Electron>& elec) const;

  // Data
  edm::EDGetTokenT<edm::View<pat::Electron> > electronCollectionToken_;
  const std::string isoLabel_;
  std::auto_ptr<std::vector<pat::Electron> > out; // Collection we'll output at the end

  const double isoCut;
  const std::string rhoLabel;
  const std::string eaLabel; // use this effective area to correct isolation
  const std::string fsrLabel;

  const double isoConeDRMax;
  const double isoConeDRMin;
  // only worry about isolation veto cone in barrel
  const double isoConeVetoEtaThreshold;
};


// Constructors and destructors

MiniAODElectronHZZIsoDecider::MiniAODElectronHZZIsoDecider(const edm::ParameterSet& iConfig):
  electronCollectionToken_(consumes<edm::View<pat::Electron> >(iConfig.exists("src") ? 
                                                               iConfig.getParameter<edm::InputTag>("src") :
                                                               edm::InputTag("slimmedElectrons"))),
  isoLabel_(iConfig.exists("isoLabel") ?
	   iConfig.getParameter<std::string>("isoLabel") :
	   std::string("HZZ4lIsoPass")),
  isoCut(iConfig.exists("isoCut") ? iConfig.getParameter<double>("isoCut") : 0.5),
  rhoLabel(iConfig.exists("rhoLabel") ?
	   iConfig.getParameter<std::string>("rhoLabel") :
	   std::string("rho_fastjet")),
  eaLabel(iConfig.exists("eaLabel") ?
	  iConfig.getParameter<std::string>("eaLabel") :
	  std::string("EffectiveArea")),
  fsrLabel(iConfig.exists("fsrLabel") ?
           iConfig.getParameter<std::string>("fsrLabel") :
           std::string("dretFSRCand")),
  isoConeDRMax(iConfig.exists("isoConeDRMax") ? 
               iConfig.getParameter<double>("isoConeDRMax") : 0.4),
  isoConeDRMin(iConfig.exists("isoConeDRMin") ? 
               iConfig.getParameter<double>("isoConeDRMin") : 0.08),
  isoConeVetoEtaThreshold(iConfig.exists("isoConeVetoEtaThreshold") ? 
                          iConfig.getParameter<double>("isoConeVetoEtaThreshold") : 
                          1.479)  
{
  produces<std::vector<pat::Electron> >();
}


void MiniAODElectronHZZIsoDecider::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Electron> >(new std::vector<pat::Electron>);

  edm::Handle<edm::View<pat::Electron> > electronsIn;

  iEvent.getByToken(electronCollectionToken_, electronsIn);

  for(edm::View<pat::Electron>::const_iterator ei = electronsIn->begin();
      ei != electronsIn->end(); ei++) // loop over electrons
    {
      const edm::Ptr<pat::Electron> eptr(electronsIn, ei - electronsIn->begin());

      out->push_back(*ei); // copy electron to save correctly in event

      bool isoResult = (PFRelIsoRhoFSR(eptr) < isoCut);
      out->back().addUserFloat(isoLabel_, float(isoResult)); // 1 for true, 0 for false
    }

  iEvent.put(out);
}


float MiniAODElectronHZZIsoDecider::PFRelIsoRhoFSR(const edm::Ptr<pat::Electron>& elec) const
{
  float chHadIso = elec->chargedHadronIso();
  float nHadIso = elec->neutralHadronIso();
  float phoIso = elec->photonIso();
  float puCorrection = elec->userFloat(rhoLabel) * elec->userFloat(eaLabel);

  float fsrCorrection = 0.;
  if(elec->hasUserCand(fsrLabel))
    {
      edm::Ptr<reco::Candidate> fsr = elec->userCand(fsrLabel);
      float fsrDR = reco::deltaR(fsr->p4(), elec->p4());
      if(fsrDR < isoConeDRMin && 
         (elec->superCluster()->eta() < isoConeVetoEtaThreshold ||
          fsrDR > isoConeDRMin))
        puCorrection = fsr->pt();
    }
  
  float neutralIso = nHadIso + phoIso - puCorrection - fsrCorrection;
  if(neutralIso < 0.)
    neutralIso = 0.;

  return ((chHadIso + neutralIso) / elec->pt());
}


void MiniAODElectronHZZIsoDecider::beginJob()
{}


void MiniAODElectronHZZIsoDecider::endJob()
{}


void
MiniAODElectronHZZIsoDecider::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODElectronHZZIsoDecider);








