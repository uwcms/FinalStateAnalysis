/*
 * =====================================================================================
 *
 *       Filename:  PATElectronEmbedCalibratedGsf.cc
 *
 *    Description:  Embed links to the calibrated GSF electrons.
 *                  This is sort of dumb - the calibratedGsfElectrons
 *                  must match 1-to-1 with the PAT Electrons.
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

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"

class PATElectronEmbedCalibratedGsf : public edm::EDProducer {
  public:
    PATElectronEmbedCalibratedGsf(const edm::ParameterSet& pset);
    virtual ~PATElectronEmbedCalibratedGsf(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag calibSrc_;

};
PATElectronEmbedCalibratedGsf::PATElectronEmbedCalibratedGsf(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  calibSrc_ = pset.getParameter<edm::InputTag>("calibSrc");

  produces<pat::ElectronCollection>();
}
void PATElectronEmbedCalibratedGsf::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<pat::ElectronCollection> electrons;
  evt.getByLabel(src_, electrons);

  edm::Handle<reco::GsfElectronCollection> calibrated;
  evt.getByLabel(calibSrc_, calibrated);

  std::auto_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  output->reserve(electrons->size());

  assert(calibrated->size() == electrons->size());

  for (size_t i = 0; i < electrons->size(); ++i) {
    pat::Electron ele(electrons->at(i));
    double bestDeltaR = 1e9;
    reco::CandidatePtr bestCalib;
    // Sigh - we have to do this since sometimes the pat electron producer
    // swaps them around.
    for (size_t j = 0; j < calibrated->size(); ++j) {
      reco::CandidatePtr calib(calibrated, j);
      double deltaR = reco::deltaR(calib->p4(), ele.p4());
      if (deltaR < bestDeltaR) {
        bestDeltaR = deltaR;
        bestCalib = calib;
      }
    }
    ele.addUserCand("calibrated", bestCalib);
    if (bestDeltaR > 0.05) {
      edm::LogWarning("BigCalibration")
        << " The calibrated gsf electron " << std::endl
        << "pt/eta/phi: "
        << bestCalib->pt() << "/" << bestCalib->eta() << "/" << bestCalib->phi()
        << std::endl
        << " is more than 0.05 away from the uncalibrated: "
        << "pt/eta/phi: "
        << ele.pt() << "/" << ele.eta() << "/" << ele.phi()
        << std::endl;
    }
    output->push_back(ele);
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronEmbedCalibratedGsf);
