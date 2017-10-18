/*
 * =====================================================================================
 *
 *       Filename:  PATObjectWorkingPointEmbedder.cc
 *
 *    Description:  Embed a binary working point into a PAT object.
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
#include "FWCore/Framework/interface/EDProducer.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

template<typename T>
class PATObjectWorkingPointEmbedder : public edm::EDProducer {
  public:
    typedef std::vector<T> OutputCollection;
    typedef StringCutObjectSelector<T, true>  StrCut;
    typedef boost::shared_ptr<StrCut> StrCutPtr;

    struct Category {
      std::string categoryStr;
      StrCutPtr category;
      std::vector<StrCutPtr> cuts;
      // The string values of the cuts
      std::vector<std::string> cutStrs;
    };

    PATObjectWorkingPointEmbedder(const edm::ParameterSet& pset);
    virtual ~PATObjectWorkingPointEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    std::string userIntLabel_;
    std::vector<Category> categories_;
    std::string moduleName_;
};

template<typename T>
PATObjectWorkingPointEmbedder<T>::PATObjectWorkingPointEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  userIntLabel_ = pset.getParameter<std::string>("userIntLabel");
  moduleName_ = pset.getParameter<std::string>("@module_label");

  typedef std::vector<edm::ParameterSet> VPSet;

  VPSet categories = pset.getParameter<VPSet>("categories");

  for (size_t i = 0; i < categories.size(); ++i) {
    Category cat;
    cat.categoryStr = categories[i].getParameter<std::string>("category");
    cat.category.reset(new StrCut(cat.categoryStr));
    if (categories[i].existsAs<std::string>("cut")) {
      std::string cut = categories[i].getParameter<std::string>("cut");
      cat.cuts.push_back(StrCutPtr(new StrCut(cut)));
      cat.cutStrs.push_back(cut);
    } else {
      std::vector<std::string> cuts =
        categories[i].getParameter<std::vector<std::string> >("cut");
      for (size_t j = 0; j < cuts.size(); ++j) {
        cat.cuts.push_back(StrCutPtr(new StrCut(cuts[j])));
        cat.cutStrs.push_back(cuts[j]);
      }
    }
    categories_.push_back(cat);
  }

  produces<OutputCollection>();
}

template<typename T>
void PATObjectWorkingPointEmbedder<T>::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<OutputCollection> output(new OutputCollection);

  edm::Handle<edm::View<T> > input;
  evt.getByLabel(src_, input);

  output->reserve(input->size());

  for (size_t i = 0; i < input->size(); ++i) {
    T owned = input->at(i);
    for (size_t j = 0; j < categories_.size(); ++j) {
      // Find the first category the object is in
      if ( (*categories_[j].category)(owned) ) {
        // Apply the cut for this category and exit
        bool passes = true;
        for (size_t k = 0; k < categories_[j].cuts.size(); ++k) {
          bool result = (*categories_[j].cuts[k])(owned);
          //std::cout << moduleName_ << " " << i << " " << j <<
            //" " << k << categories_[j].cutStrs[k]  << " " << result << std::endl;
          if (!result) {
            passes = false;
            break;
          }
        }
        owned.addUserInt(userIntLabel_, passes);
        break;
      }
    }
    //for (size_t q = 0; q < owned.userIntNames().size(); ++q) {
      //std::cout << q << " " << owned.userIntNames()[q] << std::endl;
    //}
    //std::cout << "wtf: " << owned.hasUserInt(userIntLabel_) << std::endl;
    output->push_back(owned);
  }
  evt.put(std::move(output));
}

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "FWCore/Framework/interface/MakerMacros.h"

typedef PATObjectWorkingPointEmbedder<pat::Tau> PATTauWorkingPointEmbedder;
DEFINE_FWK_MODULE(PATTauWorkingPointEmbedder);
typedef PATObjectWorkingPointEmbedder<pat::Muon> PATMuonWorkingPointEmbedder;
DEFINE_FWK_MODULE(PATMuonWorkingPointEmbedder);
typedef PATObjectWorkingPointEmbedder<pat::Electron> PATElectronWorkingPointEmbedder;
DEFINE_FWK_MODULE(PATElectronWorkingPointEmbedder);
