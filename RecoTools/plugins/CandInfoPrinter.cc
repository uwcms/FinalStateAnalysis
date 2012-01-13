/*
 * =====================================================================================
 *
 *       Filename:  CandInfoPrinter.cc
 *
 *    Description:  Print out information (from string cuts)
 *
 *         Author:  Evan K. Friis evan.friis@cern.ch, UW Madison
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

class CandInfoPrinter : public edm::EDAnalyzer {
  public:
    CandInfoPrinter(const edm::ParameterSet& pset);
    virtual ~CandInfoPrinter(){}
    void analyze(const edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::ParameterSet cfg_;
};

CandInfoPrinter::CandInfoPrinter(const edm::ParameterSet& pset):cfg_(pset) {}

void
CandInfoPrinter::analyze(const edm::Event& evt, const edm::EventSetup& es) {
  // Check if we want to print the event header or not
  bool printHeader = cfg_.exists("printHeader") ?
    cfg_.getParameter<bool>("printHeader") : false;

  if (printHeader) {
    std::cout << "===================================================="
      << std::endl;
    std::cout << " run: " << evt.run()
      << " lumi: " << evt.getLuminosityBlock().id()
      << " evt: "  << evt.id() << std::endl;
    std::cout << "===================================================="
      << std::endl;
  }

  // This only happens if we only want to print the header
  if (!cfg_.exists("src"))
    return;

  edm::InputTag src = cfg_.getParameter<edm::InputTag>("src");

  edm::Handle<reco::CandidateView> cands;
  evt.getByLabel(src, cands);

  size_t nCands = cands->size();
  for (size_t i = 0; i < nCands; ++i) {
    std::cout << "--- " << src << " --- [" << (i+1) << "/" << nCands << "]"
      << std::endl;
    // Loop over all variables to print
    std::vector<std::string> functions =
      cfg_.getParameterNamesForType<std::string>();

    // This is slow but who cares
    for (size_t j = 0; j < functions.size(); ++j) {
      const std::string& funcname = functions[j];
      // Skip the CMSSW EDM info like @edm_module_type
      if (funcname.find("@") != std::string::npos)
        continue;
      std::string funcstr = cfg_.getParameter<std::string>(funcname);
      StringObjectFunction<reco::Candidate> func(funcstr, true);
      std::cout << " " << funcname << " = " << func(cands->at(i))
        << std::endl;
    }
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(CandInfoPrinter);
