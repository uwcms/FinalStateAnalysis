#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include "CondFormats/RecoMuonObjects/interface/MuScleFitDBobject.h"
#include "CondFormats/DataRecord/interface/MuScleFitDBobjectRcd.h"
#include "MuonAnalysis/MomentumScaleCalibration/interface/MomentumScaleCorrector.h"

class PATMuonSystematicsEmbedder : public edm::EDProducer {
  public:
    // Our dataformat for storing shifted candidates
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;

    // Muscle fit DB object
    class CorrectorFromDB {
      public:
        CorrectorFromDB(const std::string& label) {
          label_ = label;
          cache_ = 0;
        }
        // Get the correct from the DB
        void refresh(const edm::EventSetup& es) {
          unsigned long long newCache =
            es.get<MuScleFitDBobjectRcd>().cacheIdentifier();
          if (newCache != cache_) {
            if (label_ != "") {
              es.get<MuScleFitDBobjectRcd>().get(label_, object_);
            } else {
              es.get<MuScleFitDBobjectRcd>().get(object_);
            }
            corrector_.reset(new MomentumScaleCorrector(object_.product()));
          }
          cache_ = newCache;
        }
        MomentumScaleCorrector * get() const {return corrector_.get();}
      private:
        std::string label_;
        unsigned long long cache_;
        edm::ESHandle<MuScleFitDBobject> object_;
        boost::shared_ptr<MomentumScaleCorrector> corrector_;
    };

    PATMuonSystematicsEmbedder(const edm::ParameterSet& pset);
    virtual ~PATMuonSystematicsEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    CorrectorFromDB corrector_;
    CorrectorFromDB correctorUp_;
    CorrectorFromDB correctorDown_;
};

PATMuonSystematicsEmbedder::PATMuonSystematicsEmbedder(
    const edm::ParameterSet& pset):
  corrector_(pset.getParameter<std::string>("corrTag")),
  correctorUp_(pset.getParameter<std::string>("corrTagUp")),
  correctorDown_(pset.getParameter<std::string>("corrTagDown")) {

  // Embedded output collection
  produces<pat::MuonCollection>();
  // Collections of shifted candidates
  produces<ShiftedCandCollection>("p4OutUncorr");
  produces<ShiftedCandCollection>("p4OutCorr");
  produces<ShiftedCandCollection>("p4OutUp");
  produces<ShiftedCandCollection>("p4OutDown");

  src_ = pset.getParameter<edm::InputTag>("src");
}

void PATMuonSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  corrector_.refresh(es);
  correctorUp_.refresh(es);
  correctorDown_.refresh(es);
  assert(corrector_.get());
  assert(correctorUp_.get());
  assert(correctorDown_.get());

  std::auto_ptr<pat::MuonCollection> output(new pat::MuonCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutCorr(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutUncorr(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutUp(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutDown(new ShiftedCandCollection);

  edm::Handle<edm::View<pat::Muon> > muons;
  evt.getByLabel(src_, muons);

  output->reserve(muons->size());
  p4OutCorr->reserve(muons->size());
  p4OutUncorr->reserve(muons->size());
  p4OutUp->reserve(muons->size());
  p4OutDown->reserve(muons->size());

  for (size_t i = 0; i < muons->size(); ++i) {
    pat::Muon muon = muons->at(i); // make a local copy

    double correctedPt = (*corrector_.get())(muon);
    double correctedPtUp = (*correctorUp_.get())(muon);
    double correctedPtDown = (*correctorDown_.get())(muon);

    double eta = muon.eta();
    double phi = muon.phi();
    double mass = muon.mass();

    ShiftedCand uncorr = muon;
    ShiftedCand nominal = muon;
    ShiftedCand mesUp = muon;
    ShiftedCand mesDown = muon;

    // Don't apply the correction by default, no one else does.

    nominal.setP4(reco::Particle::PolarLorentzVector(
          correctedPt, eta, phi, mass));

    mesUp.setP4(reco::Particle::PolarLorentzVector(
          correctedPtUp, eta, phi, mass));

    mesDown.setP4(reco::Particle::PolarLorentzVector(
          correctedPtDown, eta, phi, mass));

    output->push_back(muon);
    p4OutUncorr->push_back(uncorr);
    p4OutCorr->push_back(nominal);
    p4OutUp->push_back(mesUp);
    p4OutDown->push_back(mesDown);
  }

  // Put the shifted collections in the event
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  PutHandle p4OutUncorrH = evt.put(p4OutUncorr, "p4OutUncorr");
  PutHandle p4OutCorrH = evt.put(p4OutCorr, "p4OutCorr");
  PutHandle p4OutUpH = evt.put(p4OutUp, "p4OutUp");
  PutHandle p4OutDownH = evt.put(p4OutDown, "p4OutDown");

  // Now embed the shifted collections into the output muon collection
  for (size_t i = 0; i < muons->size(); ++i) {
    CandidatePtr uncorrPtr(p4OutUncorrH, i);
    CandidatePtr nomPtr(p4OutCorrH, i);
    CandidatePtr upPtr(p4OutDownH, i);
    CandidatePtr downPtr(p4OutDownH, i);

    pat::Muon& muon = output->at(i);

    muon.addUserCand("uncorr", uncorrPtr);
    muon.addUserCand("corr", nomPtr);
    muon.addUserCand("mes-", downPtr);
    muon.addUserCand("mes+", upPtr);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonSystematicsEmbedder);
