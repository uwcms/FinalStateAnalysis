/*
 * Embeds MIT MVA Electron ID information into pat::Electrons
 *
 * Author: Evan K. Friis, UW Madison
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FinalStateAnalysis/RecoTools/interface/ElectronIDMVA.h"

class PATElectronMVAIDEmbedder : public edm::EDProducer {
  public:
    PATElectronMVAIDEmbedder(const edm::ParameterSet& pset);
    virtual ~PATElectronMVAIDEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag ebRecHits_;
    edm::InputTag eeRecHits_;
    std::string userLabel_;
    ElectronIDMVA mva_;
};

PATElectronMVAIDEmbedder::PATElectronMVAIDEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  ebRecHits_ = pset.getParameter<edm::InputTag>("ebRecHits");
  eeRecHits_ = pset.getParameter<edm::InputTag>("eeRecHits");
  userLabel_ = pset.getParameter<std::string>("userLabel");
  /*code*/

  std::string method_ = pset.getParameter<std::string>("methodName");
  edm::FileInPath Subdet0Pt10To20Weights = pset.getParameter<edm::FileInPath>("Subdet0PtLowPtWeights");
  edm::FileInPath Subdet1Pt10To20Weights = pset.getParameter<edm::FileInPath>("Subdet1PtLowPtWeights");
  edm::FileInPath Subdet2Pt10To20Weights = pset.getParameter<edm::FileInPath>("Subdet2PtLowPtWeights");
  edm::FileInPath Subdet0Pt20ToInfWeights = pset.getParameter<edm::FileInPath>("Subdet0Pt20ToInfWeights");
  edm::FileInPath Subdet1Pt20ToInfWeights = pset.getParameter<edm::FileInPath>("Subdet1Pt20ToInfWeights");
  edm::FileInPath Subdet2Pt20ToInfWeights = pset.getParameter<edm::FileInPath>("Subdet2Pt20ToInfWeights");
  ElectronIDMVA::MVAType mvaType = static_cast<ElectronIDMVA::MVAType>(
      pset.getParameter<unsigned int>("mvaType"));

  mva_.Initialize(
      method_,
      Subdet0Pt10To20Weights.fullPath(),
      Subdet1Pt10To20Weights.fullPath(),
      Subdet2Pt10To20Weights.fullPath(),
      Subdet0Pt20ToInfWeights.fullPath(),
      Subdet1Pt20ToInfWeights.fullPath(),
      Subdet2Pt20ToInfWeights.fullPath(),
      mvaType);

  produces<pat::ElectronCollection>();
}

void PATElectronMVAIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<edm::View<pat::Electron> > electrons;
  evt.getByLabel(src_, electrons);

  std::auto_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  output->reserve(electrons->size());

  for (size_t i = 0; i < electrons->size(); ++i) {
    // Make our own copy
    pat::Electron electron(electrons->at(i));
    // Compute the mva value
    double mvaResult = mva_.MVAValue(
        &electron, evt, es, ebRecHits_, eeRecHits_);
    // Add it as a user float
    electron.addUserFloat(userLabel_, mvaResult);
    output->push_back(electron);
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronMVAIDEmbedder);
