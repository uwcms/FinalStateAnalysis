/*
 * =====================================================================================
 *
 *       Filename:  PATMuonEffectiveAreaEmbedder.cc
 *
 *    Description:  Embed "effective area" into PAT muons.
 *                  The effective area depends on run/MC type, and
 *                  eta. See:
 *                  https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Muon_Isolation
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
#include "Muon/MuonAnalysisTools/interface/MuonEffectiveArea.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

class PATMuonEffectiveAreaEmbedder : public edm::EDProducer {
  public:
    PATMuonEffectiveAreaEmbedder(const edm::ParameterSet& pset);
    virtual ~PATMuonEffectiveAreaEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    MuonEffectiveArea::MuonEffectiveAreaTarget target_;
};

PATMuonEffectiveAreaEmbedder::PATMuonEffectiveAreaEmbedder(
    const edm::ParameterSet& pset):
  src_(pset.getParameter<edm::InputTag>("src")) {
    std::string target = pset.getParameter<std::string>("target");
    if (target == "2011Data") {
      target_ = MuonEffectiveArea::kMuEAData2011;
    } else if (target == "2012Data") {
      target_ = MuonEffectiveArea::kMuEAData2012;
    } else if (target == "Fall11MC") {
      target_ = MuonEffectiveArea::kMuEAFall11MC;
    } else if (target == "Summer11MC") {
      target_ = MuonEffectiveArea::kMuEASummer11MC;
    } else {
      throw cms::Exception("UnknownTarget")
        << "Bad eff. area option for muons: " << target
        << " options are: 2011Data, Fall11MC, Summer11MC" << std::endl;
    }
    produces<pat::MuonCollection>();
}

void PATMuonEffectiveAreaEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<edm::View<pat::Muon> > muons;
  evt.getByLabel(src_, muons);

  std::auto_ptr<pat::MuonCollection> output(new pat::MuonCollection);
  output->reserve(muons->size());

  for (size_t i = 0; i < muons->size(); ++i) {
    // Make our own copy
    pat::Muon muon(muons->at(i));
    double eta = muon.eta();
    // Embed all the interesting effective areas
    muon.addUserFloat("EAGamma04",
        MuonEffectiveArea::GetMuonEffectiveArea(
          MuonEffectiveArea::kMuGammaIso04,
          eta, target_));
    muon.addUserFloat("EANeuHadron04",
        MuonEffectiveArea::GetMuonEffectiveArea(
          MuonEffectiveArea::kMuNeutralHadronIso04,
          eta, target_));
    muon.addUserFloat("EAGammaNeuHadron04",
        MuonEffectiveArea::GetMuonEffectiveArea(
          MuonEffectiveArea::kMuGammaAndNeutralHadronIso04,
          eta, target_));
    output->push_back(muon);
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonEffectiveAreaEmbedder);
