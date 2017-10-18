/*
 * =====================================================================================
 *
 *       Filename:  DumpTriggerResults.cc
 *
 *    Description:  Dumps the results of the HLT to stdout
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include <iostream>
#include <iomanip>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "DataFormats/PatCandidates/interface/TriggerEvent.h"

class DumpTriggerResults : public edm::EDAnalyzer {
  public:
    DumpTriggerResults(const edm::ParameterSet& pset);
    virtual ~DumpTriggerResults(){}
    void analyze(const edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
};

DumpTriggerResults::DumpTriggerResults(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
}

void
DumpTriggerResults::analyze(const edm::Event& evt, const edm::EventSetup& es) {
  using namespace std;
  using namespace reco;
  edm::Handle<pat::TriggerEvent> trigEv;
  evt.getByLabel(src_, trigEv);

  cout << "============================================================="
    << endl;
  cout << "Run:  " << setiosflags(ios::right) << setw(10) << evt.id().run();
  cout << "Lumi: " << setiosflags(ios::right) << setw(10) << evt.id().luminosityBlock();
  cout << "Event:" << setiosflags(ios::right) << setw(15) << evt.id().event();
  cout << endl;

  cout << "============================================================="
    << endl;

  cout << setw(10) << "Pass" << setw(10) << "Prescale" << setw(70) << "Name" << std::endl;

  const pat::TriggerPathCollection* paths = trigEv->paths();

  for (size_t i = 0; i < paths->size(); ++i) {
    const pat::TriggerPath& path = paths->at(i);
    cout << setw(10) << path.wasAccept()
      << setw(10) << path.prescale()
      << setw(70) << path.name() << std::endl;
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(DumpTriggerResults);
