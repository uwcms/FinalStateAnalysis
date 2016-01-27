#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

class PATTauSystematicsEmbedder : public edm::EDProducer {
  public:
    // Our dataformat for storing shifted candidates
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;
    typedef reco::Candidate::LorentzVector LorentzVector;

    struct ShiftedLorentzVectors {
      LorentzVector shiftedUp;
      LorentzVector shiftedDown;
    };

    // JEC DB object
    class CorrectorFromDB {
      public:
        CorrectorFromDB(const edm::ParameterSet& pset) {
          // Check if we are apply correction
          applyCorrection_ = pset.getParameter<bool>("applyCorrection");
          corrLabel_ = pset.exists("corrLabel") ?
            pset.getParameter<std::string>("corrLabel") : "";

          // Get uncertainties
          uncLabelUp_ = pset.getParameter<std::string>("uncLabelUp");
          uncLabelDown_ = pset.getParameter<std::string>("uncLabelDown");
          uncTag_ = pset.getParameter<std::string>("uncTag");

          flavorUncertainty_ = pset.exists("flavorUncertainty") ?
            pset.getParameter<double>("flavorUncertainty") : 0.0;

          cache_ = 0;
          jetEnergyCorrector_ = 0;

        }
        // Get the correct from the DB
        void refresh(const edm::EventSetup& es) {

          unsigned long long newCache =
            es.get<JetCorrectionsRecord>().cacheIdentifier();

          if (newCache != cache_) {
            // Get uncertainty up
            if (uncLabelUp_ != "") {
              es.get<JetCorrectionsRecord>().get(uncLabelUp_, uncObjectUp_);
            } else {
              es.get<JetCorrectionsRecord>().get(uncObjectUp_);
            }
            corrUncertaintyUp_.reset(new JetCorrectionUncertainty(
                  (*uncObjectUp_)[uncTag_]));

            // Get uncertainty down
            if (uncLabelDown_ != "") {
              es.get<JetCorrectionsRecord>().get(uncLabelDown_, uncObjectDown_);
            } else {
              es.get<JetCorrectionsRecord>().get(uncObjectDown_);
            }
            corrUncertaintyDown_.reset(new JetCorrectionUncertainty(
                  (*uncObjectDown_)[uncTag_]));
          }
          cache_ = newCache;

          if (applyCorrection_)
            jetEnergyCorrector_ = JetCorrector::getJetCorrector(corrLabel_, es);
        }

        ShiftedLorentzVectors uncertainties(const LorentzVector& p4) {
          ShiftedLorentzVectors output;
          assert(corrUncertaintyUp_.get());
          assert(corrUncertaintyDown_.get());
          // make sure we are within the jet acceptance bounds
          double jetEta = p4.eta();
          if (jetEta > 5.19)
            jetEta = 5.19;
          else if (jetEta < -5.19)
            jetEta = -5.19;

          // shift up
          corrUncertaintyUp_->setJetEta(jetEta);
          corrUncertaintyUp_->setJetPt(p4.pt());
          double uncUp = corrUncertaintyUp_->getUncertainty(true);
          double shiftUp = 1.0*sqrt(
              uncUp*uncUp + flavorUncertainty_*flavorUncertainty_);

          // shift down
          corrUncertaintyDown_->setJetEta(jetEta);
          corrUncertaintyDown_->setJetPt(p4.pt());
          double uncDown = corrUncertaintyDown_->getUncertainty(true);
          double shiftDown = -1.0*sqrt(
              uncDown*uncDown + flavorUncertainty_*flavorUncertainty_);

          output.shiftedUp = (1.0 + shiftUp)*p4;
          output.shiftedDown = (1.0 + shiftDown)*p4;
          return output;
        }

        const JetCorrector*  corr() { return jetEnergyCorrector_; }

      private:
        bool applyCorrection_;
        std::string uncLabelUp_;
        std::string uncLabelDown_;
        std::string uncTag_;
        std::string corrLabel_;
        double flavorUncertainty_;
        unsigned long long cache_;
        edm::ESHandle<JetCorrectorParametersCollection> uncObjectUp_;
        edm::ESHandle<JetCorrectorParametersCollection> uncObjectDown_;
        boost::shared_ptr<JetCorrectionUncertainty> corrUncertaintyUp_;
        boost::shared_ptr<JetCorrectionUncertainty> corrUncertaintyDown_;
        const JetCorrector* jetEnergyCorrector_;
    };

    PATTauSystematicsEmbedder(const edm::ParameterSet& pset);
    virtual ~PATTauSystematicsEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    CorrectorFromDB tauJetCorrection_;
};

PATTauSystematicsEmbedder::PATTauSystematicsEmbedder(
    const edm::ParameterSet& pset):
  tauJetCorrection_(pset.getParameterSet("tauEnergyScale"))
{
  src_ = pset.getParameter<edm::InputTag>("src");

  // Produce the (corrected) nominal p4 collections for the jet and taus
  produces<ShiftedCandCollection>("p4OutNomTaus");

  // TES affects the tau
  produces<ShiftedCandCollection>("p4OutTESUpTaus");
  produces<ShiftedCandCollection>("p4OutTESDownTaus");

  produces<pat::TauCollection>();
}

void PATTauSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  tauJetCorrection_.refresh(es);

  edm::Handle<edm::View<pat::Tau> > taus;
  evt.getByLabel(src_, taus);
  size_t nTaus = taus->size();

  std::auto_ptr<pat::TauCollection> output(new pat::TauCollection);
  output->reserve(nTaus);

  std::auto_ptr<ShiftedCandCollection> p4OutNomTaus(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutTESUpTaus(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutTESDownTaus(new ShiftedCandCollection);

  p4OutNomTaus->reserve(nTaus);
  p4OutTESUpTaus->reserve(nTaus);
  p4OutTESDownTaus->reserve(nTaus);

  for (size_t i = 0; i < nTaus; ++i) {
    const pat::Tau& origTau = taus->at(i);
    output->push_back(origTau); // make our own copy
    ShiftedCand p4OutNomTau = origTau; // makes copy
    p4OutNomTaus->push_back(p4OutNomTau);
    // Now make the smeared versions of the jets and taus
    // TES uncertainty
    ShiftedLorentzVectors tesShifts = tauJetCorrection_.uncertainties(
        p4OutNomTau.p4());
    ShiftedCand p4OutTESUpTau = p4OutNomTau;
    p4OutTESUpTau.setP4(tesShifts.shiftedUp);
    p4OutTESUpTaus->push_back(p4OutTESUpTau);

    ShiftedCand p4OutTESDownTau = p4OutNomTau;
    p4OutTESDownTau.setP4(tesShifts.shiftedDown);
    p4OutTESDownTaus->push_back(p4OutTESDownTau);
  }

  // Put the shifted collections in the event
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;

  PutHandle p4OutNomTausH = evt.put(p4OutNomTaus, "p4OutNomTaus");
  PutHandle p4OutTESUpTausH = evt.put(p4OutTESUpTaus, "p4OutTESUpTaus");
  PutHandle p4OutTESDownTausH = evt.put(p4OutTESDownTaus, "p4OutTESDownTaus");

  // Now embed the shifted collections into our output pat taus
  for (size_t i = 0; i < output->size(); ++i) {
    pat::Tau& tau = output->at(i);
    tau.addUserCand("uncorr", CandidatePtr(p4OutNomTausH, i));
    tau.addUserCand("tes+", CandidatePtr(p4OutTESUpTausH, i));
    tau.addUserCand("tes-", CandidatePtr(p4OutTESDownTausH, i));
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATTauSystematicsEmbedder);
