/*
 * EDFilter which saves events which pass all selections of a
 * PATFinalStateAnalysis.
 *
 * Author: Evan K. Friis UW Madison
 */

#include <iostream>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Common/interface/LuminosityBlockBase.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/one/EDFilter.h"
#include "FWCore/Framework/interface/one/filterAbilityToImplementor.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"

#include "FinalStateAnalysis/NtupleTools/interface/PATFinalStateAnalysis.h"

class PATFinalStateAnalysisFilter : public edm::one::EDFilter<edm::one::WatchLuminosityBlocks> {
  public:
    PATFinalStateAnalysisFilter(const edm::ParameterSet& pset);
    virtual ~PATFinalStateAnalysisFilter(){}
    void beginJob();
    void endJob();
    bool filter(edm::Event& evt, const edm::EventSetup& es);
    void beginLuminosityBlock(edm::LuminosityBlock const& ls, 
				     edm::EventSetup const& es) override;
    void endLuminosityBlock(edm::LuminosityBlock const& ls, 
				   edm::EventSetup const& es) override;
  private:
    std::auto_ptr<PATFinalStateAnalysis> analysis_;
};

PATFinalStateAnalysisFilter::PATFinalStateAnalysisFilter(
    const edm::ParameterSet& pset) {
  edm::Service<TFileService> fs;
  TFileDirectory &fd =  fs->tFileDirectory();
  //analysis_.reset(new PATFinalStateAnalysis(pset, fd, consumesCollector()));
  analysis_.reset(new PATFinalStateAnalysis(pset, fd));

}

bool PATFinalStateAnalysisFilter::filter(
    edm::Event& evt, const edm::EventSetup& es) {
  const edm::EventBase& evtBase = evt;
  return analysis_->filter(evtBase);
}

void PATFinalStateAnalysisFilter::beginLuminosityBlock(
    edm::LuminosityBlock const& ls, edm::EventSetup const& es) {

  const edm::LuminosityBlockBase& lsBase = ls;
  analysis_->beginLuminosityBlock(lsBase);
}

void PATFinalStateAnalysisFilter::endLuminosityBlock(
    edm::LuminosityBlock const& ls, edm::EventSetup const& es) {
  const edm::LuminosityBlockBase& lsBase = ls;

  analysis_->endLuminosityBlock(lsBase);
}

void PATFinalStateAnalysisFilter::beginJob() {
  analysis_->beginJob();
}
void PATFinalStateAnalysisFilter::endJob() {
  analysis_->endJob();
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATFinalStateAnalysisFilter);
