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

class PATJetSystematicsEmbedderFull : public edm::EDProducer {
  public:
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;
    typedef reco::Candidate::LorentzVector LorentzVector;

    PATJetSystematicsEmbedderFull(const edm::ParameterSet& pset);
    virtual ~PATJetSystematicsEmbedderFull(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag srcPFJets_;
    edm::InputTag srcPatJets_;
    std::string label_;
    double unclusteredEnergyScale_;
};

PATJetSystematicsEmbedderFull::PATJetSystematicsEmbedderFull(const edm::ParameterSet& pset) {
  srcPFJets_ = pset.getParameter<edm::InputTag>("srcPFJets");
  srcPatJets_ = pset.getParameter<edm::InputTag>("srcPatJets");
  label_ = pset.getParameter<std::string>("corrLabel");
  unclusteredEnergyScale_ = pset.getParameter<double>("unclusteredEnergyScale");
  produces<pat::JetCollection>();
  produces<ShiftedCandCollection>("p4OutNomJetsFull");
  produces<ShiftedCandCollection>("p4OutJESUpJetsFull");
  produces<ShiftedCandCollection>("p4OutJESDownJetsFull");
  produces<ShiftedCandCollection>("p4OutUESUpJetsFull");
  produces<ShiftedCandCollection>("p4OutUESDownJetsFull");
}
void PATJetSystematicsEmbedderFull::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::JetCollection> outputFull(new pat::JetCollection);

  edm::Handle<edm::View<reco::PFJet> > jetsPF;
  evt.getByLabel(srcPFJets_, jetsPF);
  size_t nJetsPF = jetsPF->size();

  edm::Handle<edm::View<pat::Jet> > jetsPat;
  evt.getByLabel(srcPatJets_, jetsPat);
  size_t nJetsPat = jetsPat->size();

  // must be sure that nJetsPF = nJetsPat
  //std::cout<<"nJetsPF: "<<nJetsPF<<"  nJetsPat: "<<nJetsPat<<std::endl;

  std::auto_ptr<ShiftedCandCollection> p4OutNomJetsFull(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutJESUpJetsFull(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutJESDownJetsFull(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutUESUpJetsFull(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutUESDownJetsFull(new ShiftedCandCollection);

  p4OutNomJetsFull->reserve(nJetsPF);
  p4OutJESUpJetsFull->reserve(nJetsPF);
  p4OutJESDownJetsFull->reserve(nJetsPF);
  p4OutUESUpJetsFull->reserve(nJetsPF);
  p4OutUESDownJetsFull->reserve(nJetsPF);

  edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
  es.get<JetCorrectionsRecord>().get(label_, JetCorParColl);
  JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
  std::auto_ptr<JetCorrectionUncertainty> jecUnc(
      new JetCorrectionUncertainty(JetCorPar));

  for (size_t i = 0; i < nJetsPF; ++i) {
   const reco::PFJet& jetPF = jetsPF->at(i);
   const pat::Jet& jetPat = jetsPat->at(i);
   // check that all jets in collections are the same, none missing
   //std::cout<<"JetPF: "<<jetPF.pt()<<" JetPat: "<<jetPat.pt()<<std::endl;
   outputFull->push_back(jetPat);
   ShiftedCand p4OutNomJetFull(jetPat);
   p4OutNomJetsFull->push_back(p4OutNomJetFull);

    double unc = 0;
    if (std::abs(jetPat.eta()) < 5.2 && jetPat.pt() > 9) {
      jecUnc->setJetEta(jetPat.eta());
      jecUnc->setJetPt(jetPat.pt()); // here you must use the CORRECTED jet pt
      unc = jecUnc->getUncertainty(true);
    }

    //// Get uncorrected pt
    //assert(jetPat.jecSetsAvailable());

    LorentzVector uncDown = (1-unc)*jetPat.p4();
    LorentzVector uncUp = (1+unc)*jetPat.p4();
    LorentzVector uncUESDown = (1-unclusteredEnergyScale_)*jetPat.p4();
    LorentzVector uncUESUp = (1+unclusteredEnergyScale_)*jetPat.p4();

    ShiftedCand candUncDown(jetPat);
    candUncDown.setP4(uncDown);
    ShiftedCand candUncUp(jetPat);
    candUncUp.setP4(uncUp);

    ShiftedCand candUncUESDown(jetPat);
    candUncUESDown.setP4(uncUESDown);
    ShiftedCand candUncUESUp(jetPat);
    candUncUESUp.setP4(uncUESUp);

    p4OutJESUpJetsFull->push_back(candUncUp);
    p4OutJESDownJetsFull->push_back(candUncDown);
    p4OutUESUpJetsFull->push_back(candUncUESUp);
    p4OutUESDownJetsFull->push_back(candUncUESDown);
  }

  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  PutHandle p4OutNomJetsFullH = evt.put(p4OutNomJetsFull, "p4OutNomJetsFull");
  PutHandle p4OutJESUpJetsFullH = evt.put(p4OutJESUpJetsFull, "p4OutJESUpJetsFull");
  PutHandle p4OutJESDownJetsFullH = evt.put(p4OutJESDownJetsFull, "p4OutJESDownJetsFull");
  PutHandle p4OutUESUpJetsFullH = evt.put(p4OutUESUpJetsFull, "p4OutUESUpJetsFull");
  PutHandle p4OutUESDownJetsFullH = evt.put(p4OutUESDownJetsFull, "p4OutUESDownJetsFull");

  // Now embed the shifted collections into our output pat taus
  for (size_t i = 0; i < outputFull->size(); ++i) {
    pat::Jet& jet = outputFull->at(i);
    jet.addUserCand("uncorrFull", CandidatePtr(p4OutNomJetsFullH, i));
    jet.addUserCand("jesFull+", CandidatePtr(p4OutJESUpJetsFullH, i));
    jet.addUserCand("jesFull-", CandidatePtr(p4OutJESDownJetsFullH, i));
    jet.addUserCand("uesFull+", CandidatePtr(p4OutUESUpJetsFullH, i));
    jet.addUserCand("uesFull-", CandidatePtr(p4OutUESDownJetsFullH, i));
  }

  ////evt.put(output);
  evt.put(outputFull);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATJetSystematicsEmbedderFull);
