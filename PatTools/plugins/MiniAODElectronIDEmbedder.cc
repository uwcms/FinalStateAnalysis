/*
 * Embeds the electron ID as recommended by EGamma POG (expected to be depreciated when IDs included by default).
 * https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2
 * https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateElectronIdentificationRun2
 * https://twiki.cern.ch/twiki/bin/viewauth/CMS/HEEPElectronIdentificationRun2
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

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"

#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/PatCandidates/interface/Electron.h"

#include "EgammaAnalysis/ElectronTools/interface/EGammaMvaEleEstimatorCSA14.h"

#include <math.h>

// class declaration
class MiniAODElectronIDEmbedder : public edm::EDProducer {
  public:
    explicit MiniAODElectronIDEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODElectronIDEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);

  private:
    edm::EDGetTokenT<pat::ElectronCollection> electronsCollection_;
    edm::InputTag MVAidCollection_;
    EGammaMvaEleEstimatorCSA14* MVATrig_;
};

// class member functions
MiniAODElectronIDEmbedder::MiniAODElectronIDEmbedder(const edm::ParameterSet& pset) {
  electronsCollection_ = consumes<pat::ElectronCollection>(pset.getParameter<edm::InputTag>("src"));
  MVAidCollection_     = pset.getParameter<edm::InputTag>("MVAId");

  std::vector<std::string> myManualCatWeigths;
  myManualCatWeigths.push_back("EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_EB_BDT.weights.xml");
  myManualCatWeigths.push_back("EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_EE_BDT.weights.xml");
  
  vector<string> myManualCatWeigthsTrig;
  string the_path;
  for (unsigned i  = 0 ; i < myManualCatWeigths.size() ; i++){
    the_path = edm::FileInPath ( myManualCatWeigths[i] ).fullPath();
    myManualCatWeigthsTrig.push_back(the_path);
  }
  
  MVATrig_ = new EGammaMvaEleEstimatorCSA14();
  MVATrig_->initialize("BDT",
                       EGammaMvaEleEstimatorCSA14::kTrig,
                       true,
                       myManualCatWeigthsTrig);

  produces<pat::ElectronCollection>();
}

void MiniAODElectronIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<vector<pat::Electron>> electronsCollection;
  evt.getByToken(electronsCollection_ , electronsCollection);

  const vector<pat::Electron> * electrons = electronsCollection.product();

  unsigned int nbElectron =  electrons->size();

  std::auto_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  output->reserve(nbElectron);

  for(unsigned i = 0 ; i < nbElectron; i++){
    pat::Electron electron(electrons->at(i));

    // mva
    electron.addUserFloat("mvaTrigV0CSA14",MVATrig_->mvaValue(electrons->at(i),false));

    // cutbased id TODO
    electron.addUserFloat("cutBasedElectronID-CSA14-50ns-V1-standalone-veto",-1.);
    electron.addUserFloat("cutBasedElectronID-CSA14-50ns-V1-standalone-loose",-1.);
    electron.addUserFloat("cutBasedElectronID-CSA14-50ns-V1-standalone-medium",-1.);
    electron.addUserFloat("cutBasedElectronID-CSA14-50ns-V1-standalone-tight",-1.);
    electron.addUserFloat("cutBasedElectronID-CSA14-PU20bx25-V0-standalone-veto",-1.);
    electron.addUserFloat("cutBasedElectronID-CSA14-PU20bx25-V0-standalone-loose",-1.);
    electron.addUserFloat("cutBasedElectronID-CSA14-PU20bx25-V0-standalone-medium",-1.);
    electron.addUserFloat("cutBasedElectronID-CSA14-PU20bx25-V0-standalone-tight",-1.);

    output->push_back(electron);
  }

  evt.put(output);
}

// define plugin
DEFINE_FWK_MODULE(MiniAODElectronIDEmbedder);
