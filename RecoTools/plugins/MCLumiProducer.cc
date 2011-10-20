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

class MCLumiProducer : public edm::EDProducer {
  public:
    MCLumiProducer(const edm::ParameterSet& pset);
    virtual ~MCLumiProducer(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
    void endLuminosityBlock(
        edm::LuminosityBlock& ls, const edm::EventSetup& es);
  private:
    // The process xsec
    const double xSec_;
    const double xSecErrUp_;
    unsigned int eventCount_;

};

MCLumiProducer::MCLumiProducer(const edm::ParameterSet& pset):
  xSec_(pset.getParameter<double>("xSec")),
  xSecErr_(pset.getParameter<double>("xSecErr")),
  eventCount_ = 0;
  produces<LumiSummary, edm::InLumi>();
}

void MCLumiProducer::produce(edm::Event& evt, const edm::EventSetup& es) {
  eventCount_ += 1;
}

void MCLumiProducer::endLuminosityBlock(
        edm::LuminosityBlock& ls, const edm::EventSetup& es) {
  double effLumi = eventCount_ / xSec_;
  double effLumiErr = eventCount_ / xSecErr_;

  std::auto_ptr<LumiSummary> output(new LumiSummary);
  output->setLumiVersion("MC");
  output->setLumiData(effLumi, effLumiErr, LUMI_QUALITY);
  output->setlsnumber(ls.LUMI_NUM);

  // Now we need to get the L1 & HLT info somehow.
  std::vector<LumiSummary::HLT> hltInfos;
  // paths = ?
  for (size_t i = 0; i < paths.size(); ++i) {
    const std::string& pathName = ;
    int prescale = ;
    int ratecount = ;
    int inputcount = ;
    LumiSummary::HLT hltInfo;
    hltInfo.pathname = pathName;
    hltInfo.prescale = prescale;
    hltInfo.ratecount = ratecount;
    hltInfo.inputcount = inputcount;
    hltInfos.push_back(hltInfo);
  }

  std::vector<LumiSummary::L1> l1Infos;
  // paths = ?
  for (size_t i = 0; i < triggers.size(); ++i) {
    const std::string& triggerName = ;
    int prescale = ;
    int ratecount = ;
    LumiSummary::L1 l1Info;
    l1Info.pathname = pathName;
    l1Info.prescale = prescale;
    l1Info.ratecount = ratecount;
    l1Infos.push_back(l1Info);
  }
  output->swapHLTData(hltInfos);
  output->swapL1Data(l1Infos);
  ls.put(output);
  eventCount_ = 0;
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MCLumiProducer);
