/*
 * EDFilter which saves events which pass all selections of a
 * PATFinalStateAnalysis.
 *
 * Author: Evan K. Friis UW Madison
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Common/interface/LuminosityBlockBase.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FinalStateAnalysis/Selectors/interface/PATFinalStateAnalysis.h"

class PATFinalStateAnalysisFilter : public edm::EDFilter {
  public:
    PATFinalStateAnalysisFilter(const edm::ParameterSet& pset);
    virtual ~PATFinalStateAnalysisFilter(){}
    void beginJob();
    void endJob();
    bool filter(edm::Event& evt, const edm::EventSetup& es);
    bool beginLuminosityBlock(
        edm::LuminosityBlock& ls, const edm::EventSetup & es);
  private:
    std::auto_ptr<PATFinalStateAnalysis> analysis_;
};

PATFinalStateAnalysisFilter::PATFinalStateAnalysisFilter(
    const edm::ParameterSet& pset) {
  edm::Service<TFileService> fs;
  analysis_.reset(new PATFinalStateAnalysis(pset, *fs));
}

bool PATFinalStateAnalysisFilter::filter(
    edm::Event& evt, const edm::EventSetup& es) {
  const edm::EventBase& evtBase = evt;
  return analysis_->filter(evtBase);
}

bool PATFinalStateAnalysisFilter::beginLuminosityBlock(
    edm::LuminosityBlock& ls, const edm::EventSetup& es) {
  const edm::LuminosityBlockBase& lsBase = ls;
  analysis_->beginLuminosityBlock(lsBase);
  return true;
}

void PATFinalStateAnalysisFilter::beginJob() {
  analysis_->beginJob();
}
void PATFinalStateAnalysisFilter::endJob() {
  analysis_->endJob();
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateAnalysisFilter);
