#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

class PATJetSystematicsEmbedder : public edm::EDProducer {
  public:
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;
    typedef reco::Candidate::LorentzVector LorentzVector;

    PATJetSystematicsEmbedder(const edm::ParameterSet& pset);
    virtual ~PATJetSystematicsEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    std::string label_;
    double unclusteredEnergyScale_;
};

PATJetSystematicsEmbedder::PATJetSystematicsEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  label_ = pset.getParameter<std::string>("corrLabel");
  unclusteredEnergyScale_ = pset.getParameter<double>("unclusteredEnergyScale");
  produces<pat::JetCollection>();
  produces<ShiftedCandCollection>("p4OutJESUpJets");
  produces<ShiftedCandCollection>("p4OutJESDownJets");
  produces<ShiftedCandCollection>("p4OutUESUpJets");
  produces<ShiftedCandCollection>("p4OutUESDownJets");
}
void PATJetSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > jets;
  evt.getByLabel(src_, jets);
  size_t nJets = jets->size();

  std::unique_ptr<ShiftedCandCollection> p4OutJESUpJets(new ShiftedCandCollection);
  std::unique_ptr<ShiftedCandCollection> p4OutJESDownJets(new ShiftedCandCollection);
  std::unique_ptr<ShiftedCandCollection> p4OutUESUpJets(new ShiftedCandCollection);
  std::unique_ptr<ShiftedCandCollection> p4OutUESDownJets(new ShiftedCandCollection);

  p4OutJESUpJets->reserve(nJets);
  p4OutJESDownJets->reserve(nJets);
  p4OutUESUpJets->reserve(nJets);
  p4OutUESDownJets->reserve(nJets);

  edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
  es.get<JetCorrectionsRecord>().get(label_, JetCorParColl);
  JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
  std::unique_ptr<JetCorrectionUncertainty> jecUnc(
      new JetCorrectionUncertainty(JetCorPar));

  for (size_t i = 0; i < nJets; ++i) {
    const pat::Jet& jet = jets->at(i);
    output->push_back(jet); // make our own copy

    double unc = 0;
    if (std::abs(jet.eta()) < 5.2 && jet.pt() > 9) {
      jecUnc->setJetEta(jet.eta());
      jecUnc->setJetPt(jet.pt()); // here you must use the CORRECTED jet pt
      unc = jecUnc->getUncertainty(true);
    }

    // Get uncorrected pt
    assert(jet.jecSetsAvailable());

    LorentzVector uncDown = (1-unc)*jet.p4();
    LorentzVector uncUp = (1+unc)*jet.p4();
    LorentzVector uncUESDown = (1-unclusteredEnergyScale_)*jet.p4();
    LorentzVector uncUESUp = (1+unclusteredEnergyScale_)*jet.p4();

    ShiftedCand candUncDown = *jet.clone();
    candUncDown.setP4(uncDown);
    ShiftedCand candUncUp = *jet.clone();
    candUncUp.setP4(uncUp);

    ShiftedCand candUncUESDown = *jet.clone();
    candUncUESDown.setP4(uncUESDown);
    ShiftedCand candUncUESUp = *jet.clone();
    candUncUESUp.setP4(uncUESUp);

    p4OutJESUpJets->push_back(candUncUp);
    p4OutJESDownJets->push_back(candUncDown);
    p4OutUESUpJets->push_back(candUncUESUp);
    p4OutUESDownJets->push_back(candUncUESDown);
  }

  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  PutHandle p4OutJESUpJetsH = evt.put(std::move(p4OutJESUpJets), "p4OutJESUpJets");
  PutHandle p4OutJESDownJetsH = evt.put(std::move(p4OutJESDownJets), "p4OutJESDownJets");
  PutHandle p4OutUESUpJetsH = evt.put(std::move(p4OutUESUpJets), "p4OutUESUpJets");
  PutHandle p4OutUESDownJetsH = evt.put(std::move(p4OutUESDownJets), "p4OutUESDownJets");

  // Now embed the shifted collections into our output pat taus
  for (size_t i = 0; i < output->size(); ++i) {
    pat::Jet& jet = output->at(i);
    jet.addUserCand("jes+", CandidatePtr(p4OutJESUpJetsH, i));
    jet.addUserCand("jes-", CandidatePtr(p4OutJESDownJetsH, i));
    jet.addUserCand("ues+", CandidatePtr(p4OutUESUpJetsH, i));
    jet.addUserCand("ues-", CandidatePtr(p4OutUESDownJetsH, i));
  }

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATJetSystematicsEmbedder);
