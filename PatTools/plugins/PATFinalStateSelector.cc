//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   PATFinalStateSelector.cc                                               //
//                                                                          //
//   Removes PATFinalStates from the collection if they fail string cuts.   //
//                                                                          //
//   Author: Nate Woods, U. Wisconsin                                       //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////


// system includes
#include <memory>
#include <vector>

// CMS includes
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

// FSA includes
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"


class PATFinalStateSelector : public edm::EDProducer {
 public:
  PATFinalStateSelector(const edm::ParameterSet& pset);
  virtual ~PATFinalStateSelector(){}
 private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  // Tag of final states in question
  edm::EDGetTokenT<edm::View<PATFinalState> > srcToken_;

  // List of selectors
  std::vector<StringCutObjectSelector<PATFinalState> > cuts_;
};


PATFinalStateSelector::PATFinalStateSelector(const edm::ParameterSet& iConfig) :
  srcToken_(consumes<edm::View<PATFinalState> >(iConfig.exists("src") ?
       iConfig.getParameter<edm::InputTag>("src") :
       edm::InputTag("finalStateeeee")))
{
  const std::vector<std::string> cutStrings = (iConfig.exists("cuts") ?
                                               iConfig.getParameter<std::vector<std::string> >("cuts") :
                                               std::vector<std::string>());

  for(auto iCut = cutStrings.begin(); iCut != cutStrings.end(); ++iCut)
    {
      cuts_.push_back(StringCutObjectSelector<PATFinalState>(*iCut));
    }

  produces<PATFinalStateCollection>();
}


void PATFinalStateSelector::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) 
{
  std::unique_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStatesIn;
  iEvent.getByToken(srcToken_, finalStatesIn);

  for (size_t iFS = 0; iFS < finalStatesIn->size(); ++iFS) 
    {
      PATFinalState* fs = finalStatesIn->ptrAt(iFS)->clone();
      bool pass = true;
      for(auto iCut = cuts_.begin(); iCut != cuts_.end(); ++iCut)
	{
          if(!(*iCut)(*fs))
            {
              pass = false;
              break;
            }
	}

      if(pass)
        output->push_back(fs); // takes ownership
    }

  iEvent.put(std::move(output));
}

void PATFinalStateSelector::beginJob(){}
void PATFinalStateSelector::endJob(){}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateSelector);


