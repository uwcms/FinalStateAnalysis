//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODElectronEffectiveAreaEmbedder.cc                                //
//                                                                          //
//   Embeds electron effective areas using the EGamma POG recommendation.   //
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
#include "DataFormats/Common/interface/View.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


class MiniAODElectronEffectiveAreaEmbedder : public edm::EDProducer
{
public:
  explicit MiniAODElectronEffectiveAreaEmbedder(const edm::ParameterSet&);
  ~MiniAODElectronEffectiveAreaEmbedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  float getEA_25ns(const edm::Ptr<pat::Electron>& elec) const;
  float getEA_50ns(const edm::Ptr<pat::Electron>& elec) const;

  // Data
  edm::EDGetTokenT<edm::View<pat::Electron> > electronCollectionToken_;
  const std::string label_; // label for the embedded userfloat
  std::auto_ptr<std::vector<pat::Electron> > out; // Collection we'll output at the end
  const bool use25ns_;
};


// Constructors and destructors

MiniAODElectronEffectiveAreaEmbedder::MiniAODElectronEffectiveAreaEmbedder(const edm::ParameterSet& iConfig):
  electronCollectionToken_(consumes<edm::View<pat::Electron> >(iConfig.exists("src") ? 
                                                               iConfig.getParameter<edm::InputTag>("src") :
                                                               edm::InputTag("slimmedElectrons"))),
  label_(iConfig.exists("label") ?
	 iConfig.getParameter<std::string>("label") :
	 std::string("EffectiveArea")),
  use25ns_(iConfig.exists("use25ns") ?
	   iConfig.getParameter<bool>("use25ns") :
	   true)
{
  produces<std::vector<pat::Electron> >();
}


void MiniAODElectronEffectiveAreaEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Electron> >(new std::vector<pat::Electron>);

  edm::Handle<edm::View<pat::Electron> > electronsIn;

  iEvent.getByToken(electronCollectionToken_, electronsIn);

  for(edm::View<pat::Electron>::const_iterator ei = electronsIn->begin();
      ei != electronsIn->end(); ei++) // loop over electrons
    {
      const edm::Ptr<pat::Electron> eptr(electronsIn, ei - electronsIn->begin());

      out->push_back(*ei); // copy electron to save correctly in event

      float ea;
      if(use25ns_)
	ea = getEA_25ns(eptr);
      else
	ea = getEA_50ns(eptr);
	
      out->back().addUserFloat(label_, ea);
    }

  iEvent.put(out);
}


// Spring15 25ns tuning: https://indico.cern.ch/event/369239/contribution/4/attachments/1134761/1623262/talk_effective_areas_25ns.pdf
// RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt
float MiniAODElectronEffectiveAreaEmbedder::getEA_25ns(const edm::Ptr<pat::Electron>& elec) const
{
  float eta = fabs(elec->eta());

  if(eta >= 2.4)
    return 0.2687;
  else if(eta >= 2.3)
    return 0.2243;
  else if(eta >= 2.2)
    return 0.1903;
  else if(eta >= 2.0)
    return 0.1534;
  else if(eta >= 1.479)
    return 0.1411;
  else if(eta >= 1.0)
    return 0.1862;
  else
    return 0.1752;
}


// Spring15 50ns tuning: https://indico.cern.ch/event/369239/contribution/4/attachments/1134761/1623262/talk_effective_areas_25ns.pdf
// RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_50ns.txt
float MiniAODElectronEffectiveAreaEmbedder::getEA_50ns(const edm::Ptr<pat::Electron>& elec) const
{
  float eta = fabs(elec->eta());

  if(eta >= 2.4)
    return 0.2935;
  else if(eta >= 2.3)
    return 0.2425;
  else if(eta >= 2.2)
    return 0.2095;
  else if(eta >= 2.0)
    return 0.1571;
  else if(eta >= 1.479)
    return 0.1238;
  else if(eta >= 1.0)
    return 0.1782;
  else
    return 0.1733;
}


void MiniAODElectronEffectiveAreaEmbedder::beginJob()
{}


void MiniAODElectronEffectiveAreaEmbedder::endJob()
{}


void
MiniAODElectronEffectiveAreaEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODElectronEffectiveAreaEmbedder);








