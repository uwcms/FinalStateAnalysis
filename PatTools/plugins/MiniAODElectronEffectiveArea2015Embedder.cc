//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODElectronEffectiveArea2015Embedder.cc                            //
//                                                                          //
//   Embeds electron effective areas using the 2015 HZZ4l definition.       //
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


class MiniAODElectronEffectiveArea2015Embedder : public edm::EDProducer
{
public:
  explicit MiniAODElectronEffectiveArea2015Embedder(const edm::ParameterSet&);
  ~MiniAODElectronEffectiveArea2015Embedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  float getEA2015(const edm::Ptr<pat::Electron>& elec) const;

  // Data
  edm::EDGetTokenT<edm::View<pat::Electron> > electronCollectionToken_;
  const std::string label_; // label for the embedded userfloat
  std::unique_ptr<std::vector<pat::Electron> > out; // Collection we'll output at the end
};


// Constructors and destructors

MiniAODElectronEffectiveArea2015Embedder::MiniAODElectronEffectiveArea2015Embedder(const edm::ParameterSet& iConfig):
  electronCollectionToken_(consumes<edm::View<pat::Electron> >(iConfig.exists("src") ? 
                                                               iConfig.getParameter<edm::InputTag>("src") :
                                                               edm::InputTag("slimmedElectrons"))),
  label_(iConfig.exists("label") ?
	 iConfig.getParameter<std::string>("label") :
	 std::string("EffectiveArea_HZZ4l2015"))
{
  produces<std::vector<pat::Electron> >();
}


void MiniAODElectronEffectiveArea2015Embedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Electron> >(new std::vector<pat::Electron>);

  edm::Handle<edm::View<pat::Electron> > electronsIn;

  iEvent.getByToken(electronCollectionToken_, electronsIn);

  for(edm::View<pat::Electron>::const_iterator ei = electronsIn->begin();
      ei != electronsIn->end(); ei++) // loop over electrons
    {
      const edm::Ptr<pat::Electron> eptr(electronsIn, ei - electronsIn->begin());

      out->push_back(*ei); // copy electron to save correctly in event

      float ea = getEA2015(eptr);
	
      out->back().addUserFloat(label_, ea);
    }

    iEvent.put(std::move(out));
}



float MiniAODElectronEffectiveArea2015Embedder::getEA2015(const edm::Ptr<pat::Electron>& elec) const
{
  float eta = fabs(elec->eta());

  if(eta >= 2.2)
    return 0.2680;
  else if(eta >= 2.0)
    return 0.1565;
  else if(eta >= 1.3)
    return 0.1077;
  else if(eta >= 0.8)
    return 0.1734;
  else
    return 0.1830;
}


void MiniAODElectronEffectiveArea2015Embedder::beginJob()
{}


void MiniAODElectronEffectiveArea2015Embedder::endJob()
{}


void
MiniAODElectronEffectiveArea2015Embedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODElectronEffectiveArea2015Embedder);








