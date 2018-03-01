// system include files
#include <memory>
#include <vector>
#include <algorithm>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/GetterOfProducts.h" 
#include "FWCore/Framework/interface/ProcessMatch.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "DataFormats/Common/interface/MergeableCounter.h"


class WeightedEventCountProducer : public edm::one::EDProducer<edm::one::WatchLuminosityBlocks,
                                                       edm::EndLuminosityBlockProducer> {
public:
  explicit WeightedEventCountProducer(const edm::ParameterSet&);
  ~WeightedEventCountProducer() override;

private:
  virtual void produce(edm::Event &, const edm::EventSetup&) override;
  virtual void beginLuminosityBlock(const edm::LuminosityBlock &, const edm::EventSetup&) override;
  virtual void endLuminosityBlock(edm::LuminosityBlock const&, const edm::EventSetup&) override;
  virtual void endLuminosityBlockProduce(edm::LuminosityBlock &, const edm::EventSetup&) override;
      
  // ----------member data ---------------------------

  double summedWeightsInLumi_;

  edm::GetterOfProducts<GenEventInfoProduct> getGenEventInfoProduct_;
};



using namespace edm;
using namespace std;



WeightedEventCountProducer::WeightedEventCountProducer(const edm::ParameterSet& iConfig){
  //produces<edm::MergeableCounter, edm::InLumi>();
  produces<edm::MergeableCounter, edm::Transition::EndLuminosityBlock>();
  //produces<edm::MergeableCounter>();
  getGenEventInfoProduct_ = edm::GetterOfProducts<GenEventInfoProduct>(edm::ProcessMatch("*"), this);

  callWhenNewProductsRegistered([this](edm::BranchDescription const& bd){
      getGenEventInfoProduct_(bd); 
    });
}


WeightedEventCountProducer::~WeightedEventCountProducer(){}


void
WeightedEventCountProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){

  std::vector<edm::Handle<GenEventInfoProduct> > genEventInfoH;
  getGenEventInfoProduct_.fillHandles(iEvent, genEventInfoH);
  GenEventInfoProduct genEventInfo;
  if (genEventInfoH.size()) {
    if (genEventInfoH[0].isValid()) {
      genEventInfo = *genEventInfoH[0];
      if (genEventInfo.weights().size()>0)
        summedWeightsInLumi_ += genEventInfo.weights()[0];
    }
  }

  return;

}


void 
WeightedEventCountProducer::beginLuminosityBlock(const LuminosityBlock & theLuminosityBlock, const EventSetup & theSetup) {
  summedWeightsInLumi_ = 0.;
  return;
}

void 
WeightedEventCountProducer::endLuminosityBlock(LuminosityBlock const& theLuminosityBlock, const EventSetup & theSetup) {
}

void 
WeightedEventCountProducer::endLuminosityBlockProduce(LuminosityBlock & theLuminosityBlock, const EventSetup & theSetup) {
  LogTrace("WeightedEventCounting") << "endLumi: adding " << summedWeightsInLumi_ << " weights" << endl;

  unique_ptr<edm::MergeableCounter> summedWeightsPtr(new edm::MergeableCounter);
  summedWeightsPtr->value = summedWeightsInLumi_;
  theLuminosityBlock.put(std::move(summedWeightsPtr));

  return;
}



//define this as a plug-in
DEFINE_FWK_MODULE(WeightedEventCountProducer);
