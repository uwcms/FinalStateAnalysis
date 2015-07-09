//////////////////////////////////////////////////////////////////////////////
//									    //
//   MiniAODElectronMVAIDEmbedder.cc    				    //
//									    //
//   Takes MVA ID values from the common ID framework                       //
//       and embeds them as user floats in the electron                     //
//									    //
//   Author: Nate Woods, U. Wisconsin					    //
//									    //
//////////////////////////////////////////////////////////////////////////////


// system includes
#include <memory>
#include <vector>

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


class MiniAODElectronMVAIDEmbedder : public edm::EDProducer
{
public:
  explicit MiniAODElectronMVAIDEmbedder(const edm::ParameterSet&);
  ~MiniAODElectronMVAIDEmbedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  // Data
  edm::EDGetTokenT<edm::View<pat::Electron> > electronCollectionToken_;
  std::vector<std::string> valueLabels_;
  std::vector<edm::EDGetTokenT<edm::ValueMap<float> > > valueTokens_;
  std::auto_ptr<std::vector<pat::Electron> > out; // Collection we'll output at the end
};


// Constructors and destructors

MiniAODElectronMVAIDEmbedder::MiniAODElectronMVAIDEmbedder(const edm::ParameterSet& iConfig):
  electronCollectionToken_(consumes<edm::View<pat::Electron> >(iConfig.exists("src") ?
							       iConfig.getParameter<edm::InputTag>("src") :
							       edm::InputTag("slimmedElectrons"))),
  valueLabels_(iConfig.exists("valueLabels") ?
               iConfig.getParameter<std::vector<std::string> >("valueLabels") :
               std::vector<std::string>())
                                                    
{
  std::vector<edm::InputTag> valueTags = iConfig.getParameter<std::vector<edm::InputTag> >("values");
  for(unsigned int i = 0;
      (i < valueTags.size() && i < valueLabels_.size()); // ignore IDs with no known label
      ++i)
    {
      valueTokens_.push_back(consumes<edm::ValueMap<float> >(valueTags.at(i)));
    }

  produces<std::vector<pat::Electron> >();
}


void MiniAODElectronMVAIDEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Electron> >(new std::vector<pat::Electron>);

  edm::Handle<edm::View<pat::Electron> > electronsIn;
  iEvent.getByToken(electronCollectionToken_, electronsIn);

  std::vector<edm::Handle<edm::ValueMap<float> > > values(valueTokens_.size(), edm::Handle<edm::ValueMap<float> >() );

  for(unsigned int i = 0;
      i < valueTokens_.size();
      ++i)
    {
      iEvent.getByToken(valueTokens_.at(i), values.at(i));
    }

  for(edm::View<pat::Electron>::const_iterator ei = electronsIn->begin();
      ei != electronsIn->end(); ei++) // loop over electrons
    {
      const edm::Ptr<pat::Electron> eptr(electronsIn, ei - electronsIn->begin());

      out->push_back(*ei); // copy electron to save correctly in event

      for(unsigned int i = 0; // Loop over mva values
          i < values.size(); ++i)
        {
          float result = (*(values.at(i)))[eptr];
          out->back().addUserFloat(valueLabels_.at(i), float(result));
        }
    }

  iEvent.put(out);
}


void MiniAODElectronMVAIDEmbedder::beginJob()
{}


void MiniAODElectronMVAIDEmbedder::endJob()
{}


void
MiniAODElectronMVAIDEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODElectronMVAIDEmbedder);








