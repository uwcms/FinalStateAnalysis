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

class MiniAODJetSystematicsEmbedder : public edm::EDProducer {
  public:
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;
    typedef reco::Candidate::LorentzVector LorentzVector;

    MiniAODJetSystematicsEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODJetSystematicsEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    std::string label_;
};

MiniAODJetSystematicsEmbedder::MiniAODJetSystematicsEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  label_ = pset.getParameter<std::string>("corrLabel");
  produces<pat::JetCollection>();
  produces<ShiftedCandCollection>("p4OutJESUpJets");
  produces<ShiftedCandCollection>("p4OutJESDownJets");
}
void MiniAODJetSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > jets;
  evt.getByLabel(src_, jets);
  size_t nJets = jets->size();

  std::auto_ptr<ShiftedCandCollection> p4OutJESUpJets(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutJESDownJets(new ShiftedCandCollection);

  p4OutJESUpJets->reserve(nJets);
  p4OutJESDownJets->reserve(nJets);

  edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
  es.get<JetCorrectionsRecord>().get(label_, JetCorParColl);
  JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
  std::auto_ptr<JetCorrectionUncertainty> jecUnc(
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

    std::cout << "uncDown pt: " << uncDown.pt() << " ,uncUp pt: " << uncUp.pt() << std::endl;

    ShiftedCand candUncDown = *jet.clone();
    candUncDown.setP4(uncDown);
    ShiftedCand candUncUp = *jet.clone();
    candUncUp.setP4(uncUp);

    p4OutJESUpJets->push_back(candUncUp);
    p4OutJESDownJets->push_back(candUncDown);
  }

  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  PutHandle p4OutJESUpJetsH = evt.put(p4OutJESUpJets, "p4OutJESUpJets");
  PutHandle p4OutJESDownJetsH = evt.put(p4OutJESDownJets, "p4OutJESDownJets");

  // Now embed the shifted collections into our output pat jets
  for (size_t i = 0; i < output->size(); ++i) {
    pat::Jet& jet = output->at(i);
    jet.addUserCand("jes+", CandidatePtr(p4OutJESUpJetsH, i));
    jet.addUserCand("jes-", CandidatePtr(p4OutJESDownJetsH, i));
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetSystematicsEmbedder);
