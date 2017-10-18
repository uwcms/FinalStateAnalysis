/*
 * =====================================================================================
 *
 *       Filename:  CandComparator.cc
 *
 *    Description:  Compare two views of candidates (must be the same size)
 *                  and make 2D histograms of various string quantities.
 *                  The axes correspond to the two collections.
 *
 *         Author:  Evan Friis (), evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "TH2F.h"

#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

class CandComparator : public edm::EDAnalyzer {
  public:
    struct Comparison {
      boost::shared_ptr<StringObjectFunction<reco::Candidate> > func_;
      std::string funcStr_;
      TH2F* histo_;
      TH1F* diff_;
    };

    CandComparator(const edm::ParameterSet& pset);
    virtual ~CandComparator(){}
    void analyze(const edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src1_;
    edm::InputTag src2_;
    std::vector<Comparison> comparisons_;
};

CandComparator::CandComparator(const edm::ParameterSet& pset) {
  src1_ = pset.getParameter<edm::InputTag>("src1");
  src2_ = pset.getParameter<edm::InputTag>("src2");
  std::string moduleName = pset.getParameter<std::string>("@module_label");

  edm::Service<TFileService> fs;
  TFileDirectory directory(fs->mkdir(moduleName));

  edm::ParameterSet comparisons = pset.getParameterSet("comparisons");

  std::vector<std::string> titles =
    comparisons.getParameterNamesForType<edm::ParameterSet>();

  for (size_t i = 0; i < titles.size(); ++i) {
    edm::ParameterSet compPSet = comparisons.getParameterSet(titles[i]);
    std::string func = compPSet.getParameter<std::string>("func");
    Comparison comp;
    comp.func_.reset(new StringObjectFunction<reco::Candidate>(
          func, true));
    comp.funcStr_ = func;
    size_t nbins = compPSet.getParameter<unsigned int>("nbins");
    double min = compPSet.getParameter<double>("min");
    double max = compPSet.getParameter<double>("max");
    TH2F* histo = directory.make<TH2F>(
        titles[i].c_str(),
        titles[i].c_str(),
        nbins, min, max, nbins, min, max);
    comp.histo_ = histo;
    std::string diffTitle = titles[i] + "_diff";
    TH1F* diffHisto_ = directory.make<TH1F>(
        diffTitle.c_str(),
        diffTitle.c_str(),
        nbins, min, max);
    comp.diff_ = diffHisto_;
    comparisons_.push_back(comp);
  }
}

void CandComparator::analyze(const edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<reco::CandidateView> cands1;
  evt.getByLabel(src1_, cands1);

  edm::Handle<reco::CandidateView> cands2;
  evt.getByLabel(src2_, cands2);

  assert(cands1->size() == cands2->size());

  for (size_t iComp = 0; iComp < comparisons_.size(); ++iComp) {
    Comparison& comp = comparisons_[iComp];

    for (size_t i = 0; i < cands1->size(); ++i) {
      const reco::Candidate& cand1 = (*cands1)[i];
      const reco::Candidate& cand2 = (*cands2)[i];
      double val1 = (*comp.func_)(cand1);
      double val2 = (*comp.func_)(cand2);
      std::cout << cand1.pt() << std::endl;
      comp.histo_->Fill(val1, val2);
      comp.diff_->Fill(val1 - val2);
    }
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(CandComparator);
