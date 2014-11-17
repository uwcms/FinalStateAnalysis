#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

class PATMETSystematicsEmbedder : public edm::EDProducer {
  public:
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::Candidate::LorentzVector LorentzVector;

    PATMETSystematicsEmbedder(const edm::ParameterSet& pset);
    virtual ~PATMETSystematicsEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag jetSrc_;
    edm::InputTag tauSrc_;
    edm::InputTag muonSrc_;
    edm::InputTag electronSrc_;
    edm::InputTag metSrc_;
    edm::InputTag metT1Src_;
    edm::InputTag metT0pcT1TxySrc_;
    edm::InputTag metT0rtT1TxySrc_;

    bool applyType1ForTaus_;
    bool applyType1ForMuons_;
    bool applyType1ForElectrons_;
    bool applyType1ForJets_;
    bool applyType2ForJets_;

    // How to split the taus into taus, jets, and unclustered energy
    StringCutObjectSelector<pat::Tau> tauCut_;
    StringCutObjectSelector<pat::Tau> jetCut_;
    StringCutObjectSelector<pat::Tau> unclusteredCut_;
};

PATMETSystematicsEmbedder::PATMETSystematicsEmbedder(
    const edm::ParameterSet& pset):
  tauCut_(pset.getParameter<std::string>("tauCut")),
  jetCut_(pset.getParameter<std::string>("jetCut")),
  unclusteredCut_(pset.getParameter<std::string>("unclusteredCut")) {
    produces<pat::METCollection>();

    applyType1ForTaus_ = pset.getParameter<bool>("applyType1ForTaus");
    applyType1ForMuons_ = pset.getParameter<bool>("applyType1ForMuons");
    applyType1ForElectrons_ = pset.getParameter<bool>("applyType1ForElectrons");
    applyType1ForJets_ = pset.getParameter<bool>("applyType1ForJets");
    applyType2ForJets_ = pset.getParameter<bool>("applyType2ForJets");

    jetSrc_ = pset.getParameter<edm::InputTag>("jetSrc");
    tauSrc_ = pset.getParameter<edm::InputTag>("tauSrc");
    muonSrc_ = pset.getParameter<edm::InputTag>("muonSrc");
    electronSrc_ = pset.getParameter<edm::InputTag>("electronSrc");
    metSrc_ = pset.getParameter<edm::InputTag>("src");
    metT1Src_ = pset.getParameter<edm::InputTag>("metT1Src");
    metT0pcT1TxySrc_ = pset.getParameter<edm::InputTag>("metT0pcT1TxySrc");
    metT0rtT1TxySrc_ = pset.getParameter<edm::InputTag>("metT0rtT1TxySrc");

    produces<ShiftedCandCollection>("metsRaw");
    produces<ShiftedCandCollection>("metType1");
    produces<ShiftedCandCollection>("metT0pcT1Txy");
    produces<ShiftedCandCollection>("metT0rtT1Txy");
    produces<ShiftedCandCollection>("metsMESUp");
    produces<ShiftedCandCollection>("metsMESDown");
    produces<ShiftedCandCollection>("metsTESUp");
    produces<ShiftedCandCollection>("metsTESDown");
    produces<ShiftedCandCollection>("metsEESUp");
    produces<ShiftedCandCollection>("metsEESDown");
    produces<ShiftedCandCollection>("metsJESUp");
    produces<ShiftedCandCollection>("metsJESDown");
    produces<ShiftedCandCollection>("metsUESUp");
    produces<ShiftedCandCollection>("metsUESDown");
    produces<ShiftedCandCollection>("metsFullJESUp");
    produces<ShiftedCandCollection>("metsFullJESDown");
    produces<ShiftedCandCollection>("metsFullUESUp");
    produces<ShiftedCandCollection>("metsFullUESDown");
}

// Get the transverse component of the vector
reco::Candidate::LorentzVector
transverse(const reco::Candidate::LorentzVector& input) {
  math::PtEtaPhiMLorentzVector output(input.pt(), 0, input.phi(), 0);
  reco::Candidate::LorentzVector outputT(output);
  return outputT;
}

void embedShift(pat::MET& met, edm::Event& evt,
    const std::string& branchName, const std::string& embedName,
    const reco::Candidate::LorentzVector& residual) {

  typedef reco::LeafCandidate ShiftedCand;
  typedef std::vector<ShiftedCand> ShiftedCandCollection;
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  typedef reco::CandidatePtr CandidatePtr;
  std::auto_ptr<ShiftedCandCollection> output(new ShiftedCandCollection);
  ShiftedCand newCand(met);
  newCand.setP4(transverse(newCand.p4() + residual));
  output->push_back(newCand);
  PutHandle outputH = evt.put(output, branchName);
  met.addUserCand(embedName, CandidatePtr(outputH, 0));
}

void embedShiftT1(pat::MET& met, edm::Event& evt,
    const std::string& branchName, const std::string& embedName,
    const reco::Candidate::LorentzVector& residual, 
    const reco::Candidate::LorentzVector& metT1P4) {

  typedef reco::LeafCandidate ShiftedCand;
  typedef std::vector<ShiftedCand> ShiftedCandCollection;
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  typedef reco::CandidatePtr CandidatePtr;
  std::auto_ptr<ShiftedCandCollection> output(new ShiftedCandCollection);
  ShiftedCand newCand(met);
  newCand.setP4(transverse(metT1P4 + residual));
  output->push_back(newCand);
  PutHandle outputH = evt.put(output, branchName);
  met.addUserCand(embedName, CandidatePtr(outputH, 0));
}

void PATMETSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  edm::Handle<edm::View<pat::Jet> > jets; // if patJet
  //edm::Handle<edm::View<reco::PFJet> > jets; // if PFJet
  evt.getByLabel(jetSrc_, jets);

  edm::Handle<edm::View<pat::Tau> > taus;
  evt.getByLabel(tauSrc_, taus);

  edm::Handle<edm::View<pat::Muon> > muons;
  evt.getByLabel(muonSrc_, muons);

  edm::Handle<edm::View<pat::Electron> > electrons;
  evt.getByLabel(electronSrc_, electrons);

  edm::Handle<edm::View<pat::MET> > mets;
  evt.getByLabel(metSrc_, mets);

  edm::Handle<edm::View<pat::MET> > metT1s;
  evt.getByLabel(metT1Src_, metT1s);

  edm::Handle<edm::View<pat::MET> > metT0pcT1Txys;
  evt.getByLabel(metT0pcT1TxySrc_, metT0pcT1Txys);

  edm::Handle<edm::View<pat::MET> > metT0rtT1Txys;
  evt.getByLabel(metT0rtT1TxySrc_, metT0rtT1Txys);

  assert(mets->size() == 1);

  const pat::MET& inputMET = mets->at(0);
  const pat::MET& metT1 = metT1s->at(0);
  const pat::MET& metT0pcT1Txy = metT0pcT1Txys->at(0);
  const pat::MET& metT0rtT1Txy = metT0rtT1Txys->at(0);
  pat::MET outputMET = inputMET;

  // Raw MET
  embedShift(outputMET, evt, "metsRaw", "raw", LorentzVector());

  // Keep track of the type 1 correction
  LorentzVector type1Correction;

  // Do MES shifts
  LorentzVector uncorrMuonP4;
  LorentzVector nominalMuonP4;
  LorentzVector mesUpMuonP4;
  LorentzVector mesDownMuonP4;

  // We have currently disabled the muon correction, as MusclFit is broken
  // as currently implemented.
  /*
  for (size_t i = 0; i < muons->size(); ++i) {
    const pat::Muon& muon = muons->at(i);
    assert(muon.userCand("uncorr").isNonnull());
    assert(muon.userCand("mes+").isNonnull());
    assert(muon.userCand("mes-").isNonnull());
    uncorrMuonP4 += muon.userCand("uncorr")->p4();
    nominalMuonP4 += muon.p4();
    mesUpMuonP4 += muon.userCand("mes+")->p4();
    mesDownMuonP4 += muon.userCand("mes-")->p4();
  }
  */

  // Do EES shifts
  LorentzVector uncorrElectronP4;
  LorentzVector nominalElectronP4;
  LorentzVector eesUpElectronP4;
  LorentzVector eesDownElectronP4;

  for (size_t i = 0; i < electrons->size(); ++i) {
    const pat::Electron& electron = electrons->at(i);
    assert(electron.userCand("uncorr").isNonnull());
    assert(electron.userCand("ees+").isNonnull());
    assert(electron.userCand("ees-").isNonnull());
    nominalElectronP4 += electron.p4();
    uncorrElectronP4 += electron.userCand("uncorr")->p4();
    eesUpElectronP4 += electron.userCand("ees+")->p4();
    eesDownElectronP4 += electron.userCand("ees-")->p4();
  }

  LorentzVector uncorrTauP4;
  LorentzVector nominalTauP4;
  LorentzVector tesUpTauP4;
  LorentzVector tesDownTauP4;

  LorentzVector uncorrJetP4;
  LorentzVector nominalJetP4;
  LorentzVector jesUpJetP4;
  LorentzVector jesDownJetP4;

  LorentzVector uncorrJetFullP4;
  LorentzVector nominalJetFullP4;
  LorentzVector uncorrUnclusteredFullP4;
  LorentzVector nominalUnclusteredFullP4;
  LorentzVector jesUpJetFullP4;
  LorentzVector jesDownJetFullP4;
  LorentzVector uesUpJetFullP4;
  LorentzVector uesDownJetFullP4;

  LorentzVector uncorrUnclusteredP4;
  LorentzVector nominalUnclusteredP4;
  LorentzVector uesUpUnclusteredP4;
  LorentzVector uesDownUnclusteredP4;

  for (size_t i = 0; i < jets->size(); ++i){
   const pat::Jet& jetFull = jets->at(i);
   assert(jetFull.userCand("uncorrFull").isNonnull());
   assert(jetFull.userCand("jesFull+").isNonnull());
   assert(jetFull.userCand("jesFull-").isNonnull());
   
   if (jetFull.pt() >= 10){
    uncorrJetFullP4 += jetFull.userCand("uncorrFull")->p4();
    nominalJetFullP4 += jetFull.p4();
    jesUpJetFullP4 += jetFull.userCand("jesFull+")->p4();
    jesDownJetFullP4 += jetFull.userCand("jesFull-")->p4();
   }
   if (jetFull.pt() < 10){
    uncorrUnclusteredFullP4 += jetFull.userCand("uncorrFull")->p4();
    nominalUnclusteredFullP4 += jetFull.p4();
    uesUpJetFullP4 += jetFull.userCand("uesFull+")->p4();
    uesDownJetFullP4 += jetFull.userCand("uesFull-")->p4();
   }
  }

  // Do Tau ES, Jet ES, and Unclustered ES shifts using the taus
  size_t shiftedTaus = 0; // counter for sanity check
  size_t shiftedJets = 0; // counter for sanity check
  size_t shiftedUnclustered = 0; // counter for sanity check
  for (size_t i = 0; i < taus->size(); ++i) {
    const pat::Tau& tau = taus->at(i);
    // Get the underlying seed jet
    edm::Ptr<pat::Jet> seedJet(tau.userCand("patJet"));
    assert(seedJet.isNonnull());
    const pat::Jet& jet = *seedJet;
    //std::cout<<"Jet uncorr: "<<jet.userCand("uncorr")->pt()<<std::endl;
    if (tauCut_(tau)) {
      shiftedTaus++;
      assert(tau.userCand("uncorr").isNonnull());
      assert(tau.userCand("tes+").isNonnull());
      assert(tau.userCand("tes-").isNonnull());
      uncorrTauP4 += tau.userCand("uncorr")->p4();
      nominalTauP4 += tau.p4();
      tesUpTauP4 += tau.userCand("tes+")->p4();
      tesDownTauP4 += tau.userCand("tes-")->p4();
    }
    if (jetCut_(tau)) {
      shiftedJets++;
      assert(jet.userCand("uncorr").isNonnull());
      assert(jet.userCand("jes+").isNonnull());
      assert(jet.userCand("jes-").isNonnull());
      uncorrJetP4 += jet.userCand("uncorr")->p4();
      nominalJetP4 += jet.p4();
      jesUpJetP4 += jet.userCand("jes+")->p4();
      jesDownJetP4 += jet.userCand("jes-")->p4();
    }
    if (unclusteredCut_(tau)) {
      shiftedUnclustered++;
      assert(jet.userCand("uncorr").isNonnull());
      assert(jet.userCand("ues+").isNonnull());
      assert(jet.userCand("ues-").isNonnull());
      uncorrUnclusteredP4 += jet.userCand("uncorr")->p4();
      nominalUnclusteredP4 += jet.p4();
      uesUpUnclusteredP4 += jet.userCand("ues+")->p4();
      uesDownUnclusteredP4 += jet.userCand("ues-")->p4();
    }
  }

  /*
  if (shiftedUnclustered + shiftedJets + shiftedTaus != taus->size()) {
    edm::LogWarning("BadExclusivityCuts") <<
      "The set of cuts used to split taus into real taus, jets, and unclustered"
      << " jets are not exclusive/do not span the whole space."
      << " There are " << taus->size() << " original taus and "
      << shiftedTaus << " selected as taus,"
      << shiftedJets << " selected as jets,"
      << shiftedUnclustered << " selected as unclustered." << std::endl;
  }
  */

  // Embed the type one corrected MET
  embedShift(outputMET, evt, "metType1", "type1",
      metT1.p4() - outputMET.p4());

  embedShift(outputMET, evt,"metT0pcT1Txy", "type0pcT1Txy",
      metT0pcT1Txy.p4() - outputMET.p4());
  embedShift(outputMET, evt,"metT0rtT1Txy", "type0rtT1Txy",
      metT0rtT1Txy.p4() - outputMET.p4());

  embedShiftT1(outputMET, evt, "metsMESUp", "mes+",
      nominalMuonP4 - mesUpMuonP4,
      metT1.p4() );
  embedShiftT1(outputMET, evt, "metsMESDown", "mes-",
      nominalMuonP4 - mesDownMuonP4,
      metT1.p4() );

  embedShiftT1(outputMET, evt, "metsEESUp", "ees+",
      nominalElectronP4 - eesUpElectronP4,
      metT1.p4() );
  embedShiftT1(outputMET, evt, "metsEESDown", "ees-",
      nominalElectronP4 - eesDownElectronP4,
      metT1.p4() );

  embedShiftT1(outputMET, evt, "metsTESUp", "tes+",
      nominalTauP4 - tesUpTauP4,
      metT1.p4() );
  embedShiftT1(outputMET, evt, "metsTESDown", "tes-",
      nominalTauP4 - tesDownTauP4,
      metT1.p4() );

  embedShiftT1(outputMET, evt, "metsJESUp", "jes+",
      nominalJetP4 - jesUpJetP4,
      metT1.p4() );
  embedShiftT1(outputMET, evt, "metsJESDown", "jes-",
      nominalJetP4 - jesDownJetP4,
      metT1.p4() );

  embedShiftT1(outputMET, evt, "metsUESUp", "ues+",
      nominalUnclusteredP4 - uesUpUnclusteredP4,
      metT1.p4() );
  embedShiftT1(outputMET, evt, "metsUESDown", "ues-",
      nominalUnclusteredP4 - uesDownUnclusteredP4,
      metT1.p4() );

  embedShiftT1(outputMET, evt, "metsFullJESUp", "jesFull+",
      nominalJetFullP4 - jesUpJetFullP4,
      metT1.p4() );
  embedShiftT1(outputMET, evt, "metsFullJESDown", "jesFull-",
      nominalJetFullP4 - jesDownJetFullP4,
      metT1.p4() );

  embedShiftT1(outputMET, evt, "metsFullUESUp", "uesFull+",
      nominalUnclusteredFullP4 - uesUpJetFullP4,
      metT1.p4() );
  embedShiftT1(outputMET, evt, "metsFullUESDown", "uesFull-",
      nominalUnclusteredFullP4 - uesDownJetFullP4,
      metT1.p4() );

  std::auto_ptr<pat::METCollection> outputColl(new pat::METCollection);
  outputColl->push_back(outputMET);

  evt.put(outputColl);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMETSystematicsEmbedder);
