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
    edm::EDGetTokenT<edm::View<pat::Jet> > srcToken_;
    std::string label_;
    //std::string fName_ = "Spring16_25nsV9_DATA_UncertaintySources_AK4PFchs.txt"; // recommended by JetMET
    std::string fName_;
    std::vector< std::string > uncertNames = {
        "AbsoluteFlavMap",
        "AbsoluteMPFBias",
        "AbsoluteScale",
        "AbsoluteStat",
        "CorrelationGroupFlavor",
        "CorrelationGroupIntercalibration",
        "CorrelationGroupMPFInSitu",
        "CorrelationGroupUncorrelated",
        "CorrelationGroupbJES",
        "FlavorPhotonJet",
        "FlavorPureBottom",
        "FlavorPureCharm",
        "FlavorPureGluon",
        "FlavorPureQuark",
        "FlavorQCD",
        "FlavorZJet",
        "Fragmentation",
        "PileUpDataMC",
        "PileUpEnvelope",
        "PileUpMuZero",
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
        "TimeRunBCD",
        "TimeRunE",
        "TimeRunF",
        "TimeRunGH",
        "TotalNoFlavorNoTime",
        "TotalNoFlavor",
        "TotalNoTime",
        "Total",
    }; // end uncertNames
    //std::vector<JetCorrectorParameters const &> JetCorParList; // FIXME
};

MiniAODJetFullSystematicsEmbedder::MiniAODJetFullSystematicsEmbedder(const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("src"));
  label_ = pset.getParameter<std::string>("corrLabel");
  fName_ = pset.getParameter<std::string>("fName");
  produces<pat::JetCollection>();
  for (auto const& name : uncertNames) {
    produces<ShiftedCandCollection>("p4OutJESUpJetsUncor"+name);
    produces<ShiftedCandCollection>("p4OutJESDownJetsUncor"+name);

    // Do these files have to load every event without this?
    //JetCorrectorParameters const & JetCorPar = JetCorrectorParameters(fName_, name); // FIXME
    //JetCorParList.push_back( JetCorPar ); // FIXME
  };
}

void MiniAODJetFullSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);
  edm::Handle<edm::View<pat::Jet> > jets;
  std::cout << "Uncert File: " << fName_ << std::endl;
  evt.getByToken(srcToken_, jets);
  size_t nJets = jets->size();
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;

  // Make our own copy of the jets to fill
  for (size_t i = 0; i < nJets; ++i) {
    const pat::Jet& jet = jets->at(i);
    output->push_back(jet);
  }


  int iter = 0;
  for (auto const& name : uncertNames) {
    std::auto_ptr<ShiftedCandCollection> p4OutJESUpJets(new ShiftedCandCollection);
    std::auto_ptr<ShiftedCandCollection> p4OutJESDownJets(new ShiftedCandCollection);
    
    p4OutJESUpJets->reserve(nJets);
    p4OutJESDownJets->reserve(nJets);

    JetCorrectorParameters const & JetCorPar = JetCorrectorParameters(fName_, name);

    std::auto_ptr<JetCorrectionUncertainty> jecUnc(
        new JetCorrectionUncertainty(JetCorPar));
        //new JetCorrectionUncertainty(JetCorParList[iter])); // FIXME
    iter++;

    for (size_t i = 0; i < nJets; ++i) {
      const pat::Jet& jet = jets->at(i);
  
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
