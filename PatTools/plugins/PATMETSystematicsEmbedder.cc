#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
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
    edm::InputTag tauSrc_;
    edm::InputTag muonSrc_;
    edm::InputTag electronSrc_;
    edm::InputTag metSrc_;
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

  tauSrc_ = pset.getParameter<edm::InputTag>("tauSrc");
  muonSrc_ = pset.getParameter<edm::InputTag>("muonSrc");
  electronSrc_ = pset.getParameter<edm::InputTag>("electronSrc");
  metSrc_ = pset.getParameter<edm::InputTag>("src");

  produces<ShiftedCandCollection>("metsNominal");
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
  newCand.setP4(newCand.p4() + residual);
  output->push_back(newCand);
  PutHandle outputH = evt.put(output, branchName);
  met.addUserCand(embedName, CandidatePtr(outputH, 0));
}


void PATMETSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  edm::Handle<edm::View<pat::Tau> > taus;
  evt.getByLabel(tauSrc_, taus);

  edm::Handle<edm::View<pat::Muon> > muons;
  evt.getByLabel(muonSrc_, muons);

  edm::Handle<edm::View<pat::Electron> > electrons;
  evt.getByLabel(electronSrc_, electrons);

  edm::Handle<pat::METCollection> mets;
  evt.getByLabel(metSrc_, mets);

  assert(mets->size() == 1);

  const pat::MET& inputMET = mets->at(0);
  pat::MET outputMET = inputMET;

  // Nominal MET
  embedShift(outputMET, evt, "metsNominal", "nom", LorentzVector());

  // Do MES shifts
  LorentzVector nominalMuonP4;
  LorentzVector mesUpMuonP4;
  LorentzVector mesDownMuonP4;

  for (size_t i = 0; i < muons->size(); ++i) {
    const pat::Muon& muon = muons->at(i);
    nominalMuonP4 += muon.userCand("nom")->p4();
    mesUpMuonP4 += muon.userCand("mes+")->p4();
    mesDownMuonP4 += muon.userCand("mes-")->p4();
  }

  embedShift(outputMET, evt, "metsMESUp", "mes+",
      nominalMuonP4 - mesUpMuonP4);
  embedShift(outputMET, evt, "metsMESDown", "mes-",
      nominalMuonP4 - mesDownMuonP4);

  // Do EES shifts
  LorentzVector nominalElectronP4;
  LorentzVector eesUpElectronP4;
  LorentzVector eesDownElectronP4;

  for (size_t i = 0; i < electrons->size(); ++i) {
    const pat::Electron& electron = electrons->at(i);
    nominalElectronP4 += electron.userCand("nom")->p4();
    eesUpElectronP4 += electron.userCand("ees+")->p4();
    eesDownElectronP4 += electron.userCand("ees-")->p4();
  }

  embedShift(outputMET, evt, "metsEESUp", "ees+",
      nominalElectronP4 - eesUpElectronP4);
  embedShift(outputMET, evt, "metsEESDown", "ees-",
      nominalElectronP4 - eesDownElectronP4);

  LorentzVector nominalTauP4;
  LorentzVector tesUpTauP4;
  LorentzVector tesDownTauP4;

  LorentzVector nominalJetP4;
  LorentzVector jesUpJetP4;
  LorentzVector jesDownJetP4;

  LorentzVector nominalUnclusteredP4;
  LorentzVector uesUpUnclusteredP4;
  LorentzVector uesDownUnclusteredP4;

  // Do Tau ES, Jet ES, and Unclustered ES shifts using the taus
  size_t shiftedTaus = 0; // counter for sanity check
  size_t shiftedJets = 0; // counter for sanity check
  size_t shiftedUnclustered = 0; // counter for sanity check
  for (size_t i = 0; i < taus->size(); ++i) {
    const pat::Tau& tau = taus->at(i);
    if (tauCut_(tau)) {
      shiftedTaus++;
      nominalTauP4 += tau.userCand("tau_nom")->p4();
      tesUpTauP4 += tau.userCand("tau_tes+")->p4();
      tesDownTauP4 += tau.userCand("tau_tes-")->p4();
    }
    if (jetCut_(tau)) {
      shiftedJets++;
      nominalJetP4 += tau.userCand("jet_nom")->p4();
      jesUpJetP4 == tau.userCand("jet_jes+")->p4();
      jesDownJetP4 == tau.userCand("jet_jes-")->p4();
    }
    if (unclusteredCut_(tau)) {
      shiftedUnclustered++;
      nominalUnclusteredP4 += tau.userCand("jet_nom")->p4();
      uesUpUnclusteredP4 == tau.userCand("jet_ues+")->p4();
      uesDownUnclusteredP4 == tau.userCand("jet_ues-")->p4();
    }
  }

  if (shiftedUnclustered + shiftedJets + shiftedTaus != taus->size()) {
    throw cms::Exception("BadExclusivityCuts") <<
      "The set of cuts used to split taus into real taus, jets, and unclustered"
      << " jets are not exclusive/do not span the whole space."
      << " There are " << taus->size() << " original taus and "
      << shiftedTaus << " selected as taus,"
      << shiftedJets << " selected as jets,"
      << shiftedUnclustered << " selected as unclustered." << std::endl;
  }

  embedShift(outputMET, evt, "metsJESUp", "jes+",
      nominalJetP4 - jesUpJetP4);
  embedShift(outputMET, evt, "metsJESDown", "jes-",
      nominalJetP4 - jesDownJetP4);

  embedShift(outputMET, evt, "metsUESUp", "ues+",
      nominalUnclusteredP4 - uesUpUnclusteredP4);
  embedShift(outputMET, evt, "metsUESDown", "ues-",
      nominalUnclusteredP4 - uesDownUnclusteredP4);

  std::auto_ptr<pat::METCollection> outputColl(new pat::METCollection);
  outputColl->push_back(outputMET);

  evt.put(outputColl);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMETSystematicsEmbedder);
