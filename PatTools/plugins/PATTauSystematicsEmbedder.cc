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
          // shift up
          corrUncertaintyUp_->setJetEta(p4.eta());
          corrUncertaintyUp_->setJetPt(p4.pt());
          double uncUp = corrUncertaintyUp_->getUncertainty(true);
          double shiftUp = 1.0*sqrt(
              uncUp*uncUp + flavorUncertainty_*flavorUncertainty_);

          // shift down
          corrUncertaintyDown_->setJetEta(p4.eta());
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
    CorrectorFromDB jetCorrection_;
    double unclusteredEnergyScale_;
};

PATTauSystematicsEmbedder::PATTauSystematicsEmbedder(
    const edm::ParameterSet& pset):
  tauJetCorrection_(pset.getParameterSet("tauEnergyScale")),
  jetCorrection_(pset.getParameterSet("jetEnergyScale"))
{
  src_ = pset.getParameter<edm::InputTag>("src");
  unclusteredEnergyScale_ = pset.getParameter<double>(
      "unclusteredEnergyScale");

  // Produce the (corrected) nominal p4 collections for the jet and taus
  produces<ShiftedCandCollection>("p4OutNomJets");
  produces<ShiftedCandCollection>("p4OutNomTaus");

  // JES and UES affect the underlying jet
  produces<ShiftedCandCollection>("p4OutJESUpJets");
  produces<ShiftedCandCollection>("p4OutJESDownJets");
  produces<ShiftedCandCollection>("p4OutUESUpJets");
  produces<ShiftedCandCollection>("p4OutUESDownJets");

  // TES affects the tau
  produces<ShiftedCandCollection>("p4OutTESUpTaus");
  produces<ShiftedCandCollection>("p4OutTESDownTaus");

  produces<pat::TauCollection>();
}

void PATTauSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  jetCorrection_.refresh(es);
  tauJetCorrection_.refresh(es);

  edm::Handle<edm::View<pat::Tau> > taus;
  evt.getByLabel(src_, taus);
  size_t nTaus = taus->size();

  std::auto_ptr<pat::TauCollection> output(new pat::TauCollection);
  output->reserve(nTaus);

  std::auto_ptr<ShiftedCandCollection> p4OutNomJets(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutNomTaus(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutJESUpJets(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutJESDownJets(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutUESUpJets(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutUESDownJets(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutTESUpTaus(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutTESDownTaus(new ShiftedCandCollection);

  p4OutNomJets->reserve(nTaus);
  p4OutNomTaus->reserve(nTaus);
  p4OutJESUpJets->reserve(nTaus);
  p4OutJESDownJets->reserve(nTaus);
  p4OutUESUpJets->reserve(nTaus);
  p4OutUESDownJets->reserve(nTaus);
  p4OutTESUpTaus->reserve(nTaus);
  p4OutTESDownTaus->reserve(nTaus);

  for (size_t i = 0; i < nTaus; ++i) {
    const pat::Tau& origTau = taus->at(i);
    output->push_back(origTau); // make our own copy

    reco::PFJetRef pfJet = origTau.pfJetRef();
    // Create initial uncorrected versions
    ShiftedCand p4OutNomJet(*pfJet);
    ShiftedCand p4OutNomTau(origTau);
    // Now apply a correction to the jet if desired (from CV)
    if (jetCorrection_.corr()) {
      double pfJetJEC = jetCorrection_.corr()->correction(
          *pfJet, edm::RefToBase<reco::Jet>(pfJet), evt, es);
      // Correct jet four vector
      p4OutNomJet.setP4(pfJetJEC*p4OutNomJet.p4());
    }
    p4OutNomJets->push_back(p4OutNomJet);
    p4OutNomTaus->push_back(p4OutNomTau);

    // Now make the smeared versions of the jets and taus
    // TES uncertainty
    ShiftedLorentzVectors tesShifts = tauJetCorrection_.uncertainties(
        p4OutNomTau.p4());
    ShiftedCand p4OutTESUpTau(p4OutNomTau);
    p4OutTESUpTau.setP4(tesShifts.shiftedUp);
    p4OutTESUpTaus->push_back(p4OutTESUpTau);

    ShiftedCand p4OutTESDownTau(p4OutNomTau);
    p4OutTESDownTau.setP4(tesShifts.shiftedDown);
    p4OutTESDownTaus->push_back(p4OutTESDownTau);

    // JES uncertainty
    ShiftedLorentzVectors jesShifts = jetCorrection_.uncertainties(
        p4OutNomJet.p4());
    ShiftedCand p4OutJESUpJet(p4OutNomJet);
    p4OutJESUpJet.setP4(jesShifts.shiftedUp);
    p4OutJESUpJets->push_back(p4OutJESUpJet);

    ShiftedCand p4OutJESDownJet(p4OutNomJet);
    p4OutJESDownJet.setP4(jesShifts.shiftedDown);
    p4OutJESDownJets->push_back(p4OutJESDownJet);

    // UES uncertainty
    ShiftedCand p4OutUESUpJet(p4OutNomJet);
    p4OutUESUpJet.setP4((1+unclusteredEnergyScale_)*p4OutUESUpJet.p4());
    p4OutUESUpJets->push_back(p4OutUESUpJet);

    ShiftedCand p4OutUESDownJet(p4OutNomJet);
    p4OutUESDownJet.setP4((1-unclusteredEnergyScale_)*p4OutUESDownJet.p4());
    p4OutUESDownJets->push_back(p4OutUESDownJet);
  }

  // Put the shifted collections in the event
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;

  PutHandle p4OutNomJetsH = evt.put(p4OutNomJets, "p4OutNomJets");
  PutHandle p4OutNomTausH = evt.put(p4OutNomTaus, "p4OutNomTaus");
  PutHandle p4OutJESUpJetsH = evt.put(p4OutJESUpJets, "p4OutJESUpJets");
  PutHandle p4OutJESDownJetsH = evt.put(p4OutJESDownJets, "p4OutJESDownJets");
  PutHandle p4OutUESUpJetsH = evt.put(p4OutUESUpJets, "p4OutUESUpJets");
  PutHandle p4OutUESDownJetsH = evt.put(p4OutUESDownJets, "p4OutUESDownJets");
  PutHandle p4OutTESUpTausH = evt.put(p4OutTESUpTaus, "p4OutTESUpTaus");
  PutHandle p4OutTESDownTausH = evt.put(p4OutTESDownTaus, "p4OutTESDownTaus");

  // Now embed the shifted collections into our output pat taus
  for (size_t i = 0; i < output->size(); ++i) {
    pat::Tau& tau = output->at(i);
    tau.addUserCand("jet_nom", CandidatePtr(p4OutNomJetsH, i));
    tau.addUserCand("jet_jes+", CandidatePtr(p4OutJESUpJetsH, i));
    tau.addUserCand("jet_jes-", CandidatePtr(p4OutJESDownJetsH, i));
    tau.addUserCand("jet_ues+", CandidatePtr(p4OutUESUpJetsH, i));
    tau.addUserCand("jet_ues-", CandidatePtr(p4OutUESDownJetsH, i));

    tau.addUserCand("tau_nom", CandidatePtr(p4OutNomTausH, i));
    tau.addUserCand("tau_tes+", CandidatePtr(p4OutTESUpTausH, i));
    tau.addUserCand("tau_tes-", CandidatePtr(p4OutTESDownTausH, i));
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATTauSystematicsEmbedder);
