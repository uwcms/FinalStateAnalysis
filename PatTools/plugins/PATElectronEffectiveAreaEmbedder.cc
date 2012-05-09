/*
 * =====================================================================================
 *
 *       Filename:  PATElectronEffectiveAreaEmbedder.cc
 *
 *    Description:  Embed "effective area" into PAT electrons.
 *                  The effective area depends on run/MC type, and
 *                  eta. See:
 *                  https://twiki.cern.ch/twiki/bin/view/CMS/EgammaEARhoCorrection
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

#include "Rtypes.h"
#include "EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

class PATElectronEffectiveAreaEmbedder : public edm::EDProducer {
  public:
    PATElectronEffectiveAreaEmbedder(const edm::ParameterSet& pset);
    virtual ~PATElectronEffectiveAreaEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    ElectronEffectiveArea::ElectronEffectiveAreaTarget target_;
};

PATElectronEffectiveAreaEmbedder::PATElectronEffectiveAreaEmbedder(
    const edm::ParameterSet& pset):
  src_(pset.getParameter<edm::InputTag>("src")) {
    std::string target = pset.getParameter<std::string>("target");
    if (target == "2011Data") {
      target_ = ElectronEffectiveArea::kEleEAData2011;
    } else if (target == "2012Data") {
      target_ = ElectronEffectiveArea::kEleEAData2012;
    } else if (target == "Fall11MC") {
      target_ = ElectronEffectiveArea::kEleEAFall11MC;
    } else if (target == "Summer11MC") {
      target_ = ElectronEffectiveArea::kEleEASummer11MC;
    } else {
      throw cms::Exception("UnknownTarget")
        << "Bad eff. area option for electrons: " << target
        << " options are: 2011Data, Fall11MC, Summer11MC" << std::endl;
    }
    produces<pat::ElectronCollection>();
}

void PATElectronEffectiveAreaEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<edm::View<pat::Electron> > electrons;
  evt.getByLabel(src_, electrons);

  std::auto_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  output->reserve(electrons->size());

  for (size_t i = 0; i < electrons->size(); ++i) {
    // Make our own copy
    pat::Electron ele(electrons->at(i));
    double scEta = ele.superCluster()->eta();
    // Embed all the interesting effective areas
    ele.addUserFloat("EAGamma04",
        ElectronEffectiveArea::GetElectronEffectiveArea(
          ElectronEffectiveArea::kEleGammaIso04,
          scEta, target_));
    ele.addUserFloat("EANeuHadron04",
        ElectronEffectiveArea::GetElectronEffectiveArea(
          ElectronEffectiveArea::kEleNeutralHadronIso04,
          scEta, target_));
    ele.addUserFloat("EAGammaNeuHadron04",
        ElectronEffectiveArea::GetElectronEffectiveArea(
          ElectronEffectiveArea::kEleGammaAndNeutralHadronIso04,
          scEta, target_));
    output->push_back(ele);
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronEffectiveAreaEmbedder);
