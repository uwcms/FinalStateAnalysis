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
#include "EgammaAnalysis/ElectronTools/interface/EGammaMvaEleEstimatorCSA14.h"


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
  std::vector<std::string> trigWeights_; // xml files for weights for triggering and non-triggering MVA
  std::vector<std::string> nonTrigWeights_;
  std::string trigLabel_; // labels for the userFloats holding results
  std::string nonTrigLabel_;
  std::auto_ptr<std::vector<pat::Electron> > out; // Collection we'll output at the end
  EGammaMvaEleEstimatorCSA14 trigMVA;
  EGammaMvaEleEstimatorCSA14 nonTrigMVA;
};


// Constructors and destructors

MiniAODElectronMVAIDEmbedder::MiniAODElectronMVAIDEmbedder(const edm::ParameterSet& iConfig):
  electronCollectionToken_(consumes<edm::View<pat::Electron> >(iConfig.getParameter<edm::InputTag>("src"))),
  trigWeights_(iConfig.getParameter<std::vector<std::string> >("trigWeights")),
  nonTrigWeights_(iConfig.getParameter<std::vector<std::string> >("nonTrigWeights")),
  trigLabel_(iConfig.getParameter<std::string>("trigLabel")),
  nonTrigLabel_(iConfig.getParameter<std::string>("nonTrigLabel"))
{
  std::vector<std::string> trigWeightPaths;
  std::vector<std::string> nonTrigWeightPaths;
  string the_path;
  for (unsigned i = 0 ; i < trigWeights_.size() ; i++){
    the_path = edm::FileInPath ( trigWeights_[i] ).fullPath();
    trigWeightPaths.push_back(the_path);
  }
  for (unsigned i = 0 ; i < nonTrigWeights_.size() ; i++){
    the_path = edm::FileInPath ( nonTrigWeights_[i] ).fullPath();
    nonTrigWeightPaths.push_back(the_path);
  }

  trigMVA = EGammaMvaEleEstimatorCSA14();
  nonTrigMVA = EGammaMvaEleEstimatorCSA14();

  trigMVA.initialize("BDT", EGammaMvaEleEstimatorCSA14::kTrig,
		     true, trigWeightPaths);		  
  nonTrigMVA.initialize("BDT", EGammaMvaEleEstimatorCSA14::kNonTrig,
			true, nonTrigWeightPaths);		  

  produces<std::vector<pat::Electron> >();
}


void MiniAODElectronMVAIDEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out->clear();

  edm::Handle<edm::View<pat::Electron> > electronsIn;
  iEvent.getByToken(electronCollectionToken_, electronsIn);

  for(edm::View<pat::Electron>::const_iterator ei = electronsIn->begin();
      ei != electronsIn->end(); ei++) // loop over electrons
    {
      out->push_back(*ei); // copy electron to save correctly in event

      float trigMVAVal = trigMVA.mvaValue(*ei, false);
      float nonTrigMVAVal = nonTrigMVA.mvaValue(*ei, false);
      
      out->back().addUserFloat(trigLabel_, trigMVAVal);
      out->back().addUserFloat(nonTrigLabel_, nonTrigMVAVal);
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








