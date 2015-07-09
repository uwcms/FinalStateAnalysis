//////////////////////////////////////////////////////////////////////////////
//									    //
//   MiniAODElectronIDEmbedder.cc				            //
//									    //
//   Takes cut based ID decisions from the common ID framework's value      //
//       maps and embeds them as user floats (1 for true, 0 for false)      //
//									    //
//   Author: Nate Woods, U. Wisconsin					    //
//									    //
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


class MiniAODElectronIDEmbedder : public edm::EDProducer
{
public:
  explicit MiniAODElectronIDEmbedder(const edm::ParameterSet&);
  ~MiniAODElectronIDEmbedder() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  // Data
  edm::EDGetTokenT<edm::View<pat::Electron> > electronCollectionToken_;
  std::vector<edm::EDGetTokenT<edm::ValueMap<bool> > > idMapTokens_; // store all ID tokens
  std::vector<std::string> idLabels_; // labels for the userInts holding results
  std::vector<std::string> valueLabels_;
  std::vector<edm::EDGetTokenT<edm::ValueMap<float> > > valueTokens_;
  std::auto_ptr<std::vector<pat::Electron> > out; // Collection we'll output at the end
};


// Constructors and destructors

MiniAODElectronIDEmbedder::MiniAODElectronIDEmbedder(const edm::ParameterSet& iConfig):
  electronCollectionToken_(consumes<edm::View<pat::Electron> >(iConfig.exists("src") ? 
							       iConfig.getParameter<edm::InputTag>("src") :
							       edm::InputTag("slimmedElectrons"))),
  idLabels_(iConfig.exists("idLabels") ?
	    iConfig.getParameter<std::vector<std::string> >("idLabels") :
	    std::vector<std::string>()),
  valueLabels_(iConfig.exists("valueLabels") ?
               iConfig.getParameter<std::vector<std::string> >("valueLabels") :
               std::vector<std::string>())
{
  std::vector<edm::InputTag> idTags = iConfig.getParameter<std::vector<edm::InputTag> >("ids");

  for(unsigned int i = 0;
      (i < idTags.size() && i < idLabels_.size()); // ignore IDs with no known label
      ++i)
    {
      idMapTokens_.push_back(consumes<edm::ValueMap<bool> >(idTags.at(i)));
    }

  std::vector<edm::InputTag> valueTags = iConfig.getParameter<std::vector<edm::InputTag> >("values");
  for(unsigned int i = 0;
      (i < valueTags.size() && i < valueLabels_.size()); // ignore IDs with no known label
      ++i)
    {
      valueTokens_.push_back(consumes<edm::ValueMap<float> >(valueTags.at(i)));
    }

  produces<std::vector<pat::Electron> >();
}


void MiniAODElectronIDEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Electron> >(new std::vector<pat::Electron>);

  edm::Handle<edm::View<pat::Electron> > electronsIn;
  std::vector<edm::Handle<edm::ValueMap<bool> > > ids(idMapTokens_.size(), edm::Handle<edm::ValueMap<bool> >() );
  std::vector<edm::Handle<edm::ValueMap<float> > > values(valueTokens_.size(), edm::Handle<edm::ValueMap<float> >() );

  iEvent.getByToken(electronCollectionToken_, electronsIn);

  for(unsigned int i = 0;
      i < idMapTokens_.size();
      ++i)
    {
      iEvent.getByToken(idMapTokens_.at(i), ids.at(i));
    }
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

      for(unsigned int i = 0; // Loop over ID working points
	  i < ids.size(); ++i)
	{
	  bool result = (*(ids.at(i)))[eptr];
	  out->back().addUserFloat(idLabels_.at(i), float(result)); // 1 for true, 0 for false
	}
      for(unsigned int i = 0; // Loop over mva values
          i < values.size(); ++i)
        {
          float result = (*(values.at(i)))[eptr];
          out->back().addUserFloat(valueLabels_.at(i), float(result));
        }

    }

  iEvent.put(out);
}


void MiniAODElectronIDEmbedder::beginJob()
{}


void MiniAODElectronIDEmbedder::endJob()
{}


void
MiniAODElectronIDEmbedder::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODElectronIDEmbedder);








