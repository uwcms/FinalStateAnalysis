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

class MiniAODJetFullSystematicsEmbedder : public edm::EDProducer {
  public:
    typedef reco::LeafCandidate ShiftedCand;
    typedef std::vector<ShiftedCand> ShiftedCandCollection;
    typedef reco::CandidatePtr CandidatePtr;
    typedef reco::Candidate::LorentzVector LorentzVector;

    MiniAODJetFullSystematicsEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODJetFullSystematicsEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
    edm::EDGetTokenT<edm::View<pat::Jet> > srcToken_;
    std::string label_;
    //std::string fName_ = "Spring16_25nsV9_DATA_UncertaintySources_AK4PFchs.txt"; // recommended by JetMET
    std::string fName_;
    std::vector< std::string > uncertNames = {
        "AbsoluteFlavMap",
        "AbsoluteMPFBias",
        "AbsoluteScale",
        "AbsoluteStat",
        //"CorrelationGroupFlavor",
        //"CorrelationGroupIntercalibration",
        //"CorrelationGroupMPFInSitu",
        //"CorrelationGroupUncorrelated",
        //"CorrelationGroupbJES",
        //"FlavorPhotonJet",
        //"FlavorPureBottom",
        //"FlavorPureCharm",
        //"FlavorPureGluon",
        //"FlavorPureQuark",
        "FlavorQCD",
        //"FlavorZJet",
        "Fragmentation",
        "PileUpDataMC",
        //"PileUpEnvelope",
        //"PileUpMuZero",
        "PileUpPtBB",
        "PileUpPtEC1",
        "PileUpPtEC2",
        "PileUpPtHF",
        "PileUpPtRef",
        "RelativeFSR",
        "RelativeJEREC1",
        "RelativeJEREC2",
        "RelativeJERHF",
        "RelativePtBB",
        "RelativePtEC1",
        "RelativePtEC2",
        "RelativePtHF",
        "RelativeStatEC",
        "RelativeStatFSR",
        "RelativeStatHF",
        "SinglePionECAL",
        "SinglePionHCAL",
        "SubTotalAbsolute",
        "SubTotalMC",
        "SubTotalPileUp",
        "SubTotalPt",
        "SubTotalRelative",
        "SubTotalScale",
        "TimePtEta",
        //"TimeRunBCD",
        //"TimeRunE",
        //"TimeRunF",
        //"TimeRunGH",
        //"TotalNoFlavorNoTime",
        //"TotalNoFlavor",
        //"TotalNoTime",
        "Total",
        "Closure",
    }; // end uncertNames
    std::map<std::string, JetCorrectorParameters const *> JetCorParMap;
    std::map<std::string, JetCorrectionUncertainty* > JetUncMap;
};

MiniAODJetFullSystematicsEmbedder::MiniAODJetFullSystematicsEmbedder(const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("src"));
  label_ = pset.getParameter<std::string>("corrLabel");
  fName_ = pset.getParameter<std::string>("fName");
  std::cout << "Uncert File: " << fName_ << std::endl;
  produces<pat::JetCollection>();
  for (auto const& name : uncertNames) {
    produces<ShiftedCandCollection>("p4OutJESUpJetsUncor"+name);
    produces<ShiftedCandCollection>("p4OutJESDownJetsUncor"+name);

    // Create the uncertainty tool for each uncert
    // skip Closure, which is a comparison at the end
    if (name == "Closure") continue;
    JetCorrectorParameters const * JetCorPar = new JetCorrectorParameters(fName_, name);
    JetCorParMap[name] = JetCorPar;

    JetCorrectionUncertainty * jecUnc(
        new JetCorrectionUncertainty(*JetCorParMap[name]));
    JetUncMap[name] = jecUnc;
  };
}

void MiniAODJetFullSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);
  edm::Handle<edm::View<pat::Jet> > jets;
  evt.getByToken(srcToken_, jets);
  size_t nJets = jets->size();

  // Make our own copy of the jets to fill
  for (size_t i = 0; i < nJets; ++i) {
    const pat::Jet& jet = jets->at(i);
    output->push_back(jet);
  }

  // For comparing with Total for Closure test
  // assume symmetric uncertainties and ignore Down
  std::vector<double> factorizedTotalUp(nJets, 0.0);

  for (auto const& name : uncertNames) {
    std::auto_ptr<ShiftedCandCollection> p4OutJESUpJets(new ShiftedCandCollection);
    std::auto_ptr<ShiftedCandCollection> p4OutJESDownJets(new ShiftedCandCollection);
    
    p4OutJESUpJets->reserve(nJets);
    p4OutJESDownJets->reserve(nJets);

    for (size_t i = 0; i < nJets; ++i) {
      const pat::Jet& jet = jets->at(i);
  
      double unc = 0;
      if (std::abs(jet.eta()) < 5.2 && jet.pt() > 9 && name != "Closure") {
        JetUncMap[name]->setJetEta(jet.eta());
        JetUncMap[name]->setJetPt(jet.pt());
        unc = JetUncMap[name]->getUncertainty(true);
      }

      // Save our factorized uncertainties into a cumulative total
      // Apply this uncertainty to loop "Closure" for future
      // comparison (also skim SubTotals)
      if (name != "Total" && name != "Closure" && !name.find("SubTotal") ) factorizedTotalUp[i] += unc*unc;
      if (std::abs(jet.eta()) < 5.2 && jet.pt() > 9 && name == "Closure") {
        unc = std::sqrt(factorizedTotalUp[i]);
      }
  
      // Get uncorrected pt
      assert(jet.jecSetsAvailable());
  
      LorentzVector uncDown = (1-unc)*jet.p4();
      LorentzVector uncUp = (1+unc)*jet.p4();
  
      //std::cout << name << ":  uncDown pt: " << uncDown.pt() << " ,uncUp pt: " << uncUp.pt() << std::endl;
  
      ShiftedCand candUncDown = jet;
      candUncDown.setP4(uncDown);
      ShiftedCand candUncUp = jet;
      candUncUp.setP4(uncUp);
  
      p4OutJESUpJets->push_back(candUncUp);
      p4OutJESDownJets->push_back(candUncDown);
    }
  
    PutHandle p4OutJESUpJetsH = evt.put(p4OutJESUpJets, "p4OutJESUpJetsUncor"+name);
    PutHandle p4OutJESDownJetsH = evt.put(p4OutJESDownJets, "p4OutJESDownJetsUncor"+name);
  
    // Now embed the shifted collections into our output pat jets
    for (size_t i = 0; i < output->size(); ++i) {
      pat::Jet& jet = output->at(i);
      //std::cout << "Jet " << i << " uncorr pt: " << jet.pt() << std::endl;
      jet.addUserCand("jes"+name+"+", CandidatePtr(p4OutJESUpJetsH, i));
      jet.addUserCand("jes"+name+"-", CandidatePtr(p4OutJESDownJetsH, i));
    } // end cycle over all uncertainties
  } // end jets

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetFullSystematicsEmbedder);
