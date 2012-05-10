/*
 * =====================================================================================
 *
 *       Filename:  PATTriggerEventFilter.cc
 *
 *    Description:  Filter events by string cut on a PAT Trigger event
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

class PATTriggerEventFilter : public edm::EDFilter {
  public:
    PATTriggerEventFilter(const edm::ParameterSet& pset);
    virtual ~PATTriggerEventFilter(){}
    bool filter(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    StringCutObjectSelector<pat::TriggerEvent> cut_;
};

PATTriggerEventFilter::PATTriggerEventFilter(const edm::ParameterSet& pset):
  src_(pset.getParameter<edm::InputTag>("src")),
  cut_(pset.getParameter<std::string>("cut"), true) { }

bool PATTriggerEventFilter::filter(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<pat::TriggerEvent> trgevt;
  evt.getByLabel(src_, trgevt);
  return cut_(*trgevt);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATTriggerEventFilter);
