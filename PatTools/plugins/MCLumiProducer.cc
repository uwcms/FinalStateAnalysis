/*
 * MCLumiProducer
 *
 * Produces a LumiSummary object in MC events.  The only relevant data the added
 * is the effective integrated luminosity (intRecLumi) in that LS.   This allows
 * the normalization factor used to plot to final the events automatically
 * calculated.
 *
 * The integrated lumi and x_sec are/should be specified in pb.
 *
 * The integrated luminosity is calculated as
 *
 * int_lumi = n_events_in_lumi / x_sec
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"

class MCLumiProducer : public edm::EDProducer {
  public:
    MCLumiProducer(const edm::ParameterSet& pset);
    virtual ~MCLumiProducer(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
    void endLuminosityBlock(
        edm::LuminosityBlock& ls, const edm::EventSetup& es);
  private:
    const edm::InputTag trigSrc_;
    // The process xsec
    const double xSec_;
    const double xSecErr_;
    unsigned int eventCount_;
    // Store a copy of the trigger event from one of the events
    bool needTriggerEvent_;
    pat::TriggerEvent trigEvent_;
};

MCLumiProducer::MCLumiProducer(const edm::ParameterSet& pset):
  trigSrc_(pset.getParameter<edm::InputTag>("trigSrc")),
  xSec_(pset.getParameter<double>("xSec")),
  xSecErr_(pset.getParameter<double>("xSecErr")) {
  eventCount_ = 0;
  needTriggerEvent_ = true;
  produces<LumiSummary, edm::InLumi>();
}

void MCLumiProducer::produce(edm::Event& evt, const edm::EventSetup& es) {
  // FIXME JUST FILL LS::HLT/L1 vectors here
  eventCount_ += 1;
  if (needTriggerEvent_) {
    edm::Handle<pat::TriggerEvent> trigEv;
    evt.getByLabel(trigSrc_,trigEv);
    trigEvent_ = *trigEv;
    needTriggerEvent_ = false;
  }
}

void MCLumiProducer::endLuminosityBlock(
        edm::LuminosityBlock& ls, const edm::EventSetup& es) {
  double effLumi = eventCount_ / xSec_;
  double effLumiErr = eventCount_ / (xSec_ + xSecErr_);

  std::auto_ptr<LumiSummary> output(new LumiSummary);
  output->setLumiVersion("MC");
  output->setLumiData(effLumi, effLumiErr, 1); // last field is lumi quality??
  output->setlsnumber(ls.id().luminosityBlock());

  // Now we need to get the L1 & HLT info somehow.
  std::vector<LumiSummary::HLT> hltInfos;
  const pat::TriggerPathCollection * paths = trigEvent_.paths();
  assert(paths);
  for (size_t i = 0; i < paths->size(); ++i) {
    const std::string& pathName = paths->at(i).name();
    int prescale = paths->at(i).prescale();
    int ratecount = -1;
    int inputcount = -1;
    LumiSummary::HLT hltInfo;
    hltInfo.pathname = pathName;
    hltInfo.prescale = prescale;
    hltInfo.ratecount = ratecount;
    hltInfo.inputcount = inputcount;
    hltInfos.push_back(hltInfo);
  }

  std::vector<LumiSummary::L1> l1Infos;
  const pat::TriggerAlgorithmCollection* triggers = trigEvent_.algorithms();
  assert(triggers);
  for (size_t i = 0; i < triggers->size(); ++i) {
    const std::string& triggerName = triggers->at(i).name();
    int prescale = triggers->at(i).prescale();
    int ratecount = 999;
    LumiSummary::L1 l1Info;
    l1Info.triggername = triggerName;
    l1Info.prescale = prescale;
    l1Info.ratecount = ratecount;
    l1Infos.push_back(l1Info);
  }
  output->swapHLTData(hltInfos);
  output->swapL1Data(l1Infos);
  ls.put(output);
  eventCount_ = 0;
  needTriggerEvent_ = true;
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MCLumiProducer);
