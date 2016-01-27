#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Electron.h"

#include "DataFormats/Candidate/interface/LeafCandidate.h"

class PATElectronSystematicsEmbedder : public edm::EDProducer {
  public:
    // Our dataformat for storing shifted candidates
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;

    // Muscle fit DB object
    PATElectronSystematicsEmbedder(const edm::ParameterSet& pset);
    virtual ~PATElectronSystematicsEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<pat::Electron> > srcToken_;
    double nominal_;
    double eScaleUp_;
    double eScaleDown_;
};

PATElectronSystematicsEmbedder::PATElectronSystematicsEmbedder(
    const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<pat::Electron> >(pset.getParameter<edm::InputTag>("src"));
  nominal_ = pset.getParameter<double>("nominal");
  eScaleUp_ = pset.getParameter<double>("eScaleUp");
  eScaleDown_ = pset.getParameter<double>("eScaleDown");

  // Embedded output collection
  produces<pat::ElectronCollection>();
  // Collections of shifted candidates
  produces<ShiftedCandCollection>("p4OutUncorr");
  produces<ShiftedCandCollection>("p4OutUp");
  produces<ShiftedCandCollection>("p4OutDown");
}

void PATElectronSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutNom(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutUp(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutDown(new ShiftedCandCollection);

  edm::Handle<edm::View<pat::Electron> > electrons;
  evt.getByToken(srcToken_, electrons);

  output->reserve(electrons->size());
  p4OutNom->reserve(electrons->size());
  p4OutUp->reserve(electrons->size());
  p4OutDown->reserve(electrons->size());

  for (size_t i = 0; i < electrons->size(); ++i) {
    pat::Electron electron = electrons->at(i); // make a local copy

    double pt = electron.pt();
    ShiftedCand uncorr = electron;

    double correctedPt = nominal_*pt;
    double correctedPtUp = eScaleUp_*pt;
    double correctedPtDown = eScaleDown_*pt;

    double eta = electron.eta();
    double phi = electron.phi();
    double mass = electron.mass();

    electron.setP4(reco::Particle::PolarLorentzVector(
          correctedPt, eta, phi, mass));

    ShiftedCand mesUp = electron;
    ShiftedCand mesDown = electron;

    mesUp.setP4(reco::Particle::PolarLorentzVector(
          correctedPtUp, eta, phi, mass));

    mesDown.setP4(reco::Particle::PolarLorentzVector(
          correctedPtDown, eta, phi, mass));

    output->push_back(electron);
    p4OutNom->push_back(uncorr);
    p4OutUp->push_back(mesUp);
    p4OutDown->push_back(mesDown);
  }

  // Put the shifted collections in the event
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  PutHandle p4OutNomH = evt.put(p4OutNom, "p4OutUncorr");
  PutHandle p4OutUpH = evt.put(p4OutUp, "p4OutUp");
  PutHandle p4OutDownH = evt.put(p4OutDown, "p4OutDown");

  // Now embed the shifted collections into the output electron collection
  for (size_t i = 0; i < electrons->size(); ++i) {
    CandidatePtr nomPtr(p4OutDownH, i);
    CandidatePtr upPtr(p4OutDownH, i);
    CandidatePtr downPtr(p4OutDownH, i);

    pat::Electron& electron = output->at(i);

    electron.addUserCand("uncorr", nomPtr);
    electron.addUserCand("ees-", downPtr);
    electron.addUserCand("ees+", upPtr);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronSystematicsEmbedder);
