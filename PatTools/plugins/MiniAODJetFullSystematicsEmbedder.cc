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
#include "DataFormats/PatCandidates/interface/MET.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

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
        "RelativeBal",
        //"RelativeSample", // New for 2017
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
        //"SubTotalAbsolute", // We don't use the Subtotals, just skip them
        //"SubTotalMC",
        //"SubTotalPileUp",
        //"SubTotalPt",
        //"SubTotalRelative",
        //"SubTotalScale",
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
        "Eta0to3",
        "Eta0to5",
        "Eta3to5",
	"EC2",
        "ClosureNew"
    }; // end uncertNames
    std::map<std::string, JetCorrectorParameters const *> JetCorParMap;
    std::map<std::string, JetCorrectionUncertainty* > JetUncMap;
};

// Get the transverse component of the vector
reco::Candidate::LorentzVector
transverseVector(const reco::Candidate::LorentzVector& input) {
  math::PtEtaPhiMLorentzVector outputV(input.pt(), 0, input.phi(), 0);
    reco::Candidate::LorentzVector outputT(outputV);
      return outputT;
      }



MiniAODJetFullSystematicsEmbedder::MiniAODJetFullSystematicsEmbedder(const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("src"));
  label_ = pset.getParameter<std::string>("corrLabel");
  fName_ = pset.getParameter<std::string>("fName");
  std::cout << "Uncert File: " << fName_ << std::endl;
  produces<pat::JetCollection>();

  size_t found = fName_.find("Summer16");
  if (found==std::string::npos) uncertNames.push_back("RelativeSample");

  // Create the uncertainty tool for each uncert
  for (auto const& name : uncertNames) {
    produces<ShiftedCandCollection>("p4OutJESUpJetsUncor"+name);
    produces<ShiftedCandCollection>("p4OutJESDownJetsUncor"+name);
    // skip Closure, which is a comparison at the end
    if (name == "Closure") continue;
    // Also skip the combined eta range uncertainties
    if (name == "Eta0to3") continue;
    if (name == "Eta0to5") continue;
    if (name == "Eta3to5") continue;
    if (name == "EC2") continue;
    if (name == "ClosureNew") continue;
    JetCorrectorParameters const * JetCorPar = new JetCorrectorParameters(fName_, name);
    JetCorParMap[name] = JetCorPar;

    JetCorrectionUncertainty * jecUnc(
        new JetCorrectionUncertainty(*JetCorParMap[name]));
    JetUncMap[name] = jecUnc;
  };
}

void MiniAODJetFullSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {


  std::unique_ptr<pat::JetCollection> output(new pat::JetCollection);

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
  // For the combined eta range uncertainties
  std::vector<double> factorizedEta0to3Up(nJets, 0.0);
  std::vector<double> factorizedEta0to5Up(nJets, 0.0);
  std::vector<double> factorizedEta3to5Up(nJets, 0.0);
  std::vector<double> factorizedEC2Up(nJets, 0.0);
  std::vector<double> factorizedClosureNewUp(nJets, 0.0);

  for (auto const& name : uncertNames) {
    std::unique_ptr<ShiftedCandCollection> p4OutJESUpJets(new ShiftedCandCollection);
    std::unique_ptr<ShiftedCandCollection> p4OutJESDownJets(new ShiftedCandCollection);

    p4OutJESUpJets->reserve(nJets);
    p4OutJESDownJets->reserve(nJets);


    for (size_t i = 0; i < nJets; ++i) {
      const pat::Jet& jet = jets->at(i);
  
      double unc = 0;
      // Only shift jets within absEta < 5.2 and with pT > 9
      // Unc = zero for all others
      if (std::abs(jet.eta()) < 5.2 && jet.pt() > 9) {
        // Get unc for normal 28 and Total
        if ( !(name == "Closure") && !(name == "EC2") && !(name == "Eta0to3") && !(name == "Eta0to5") && !(name == "Eta3to5") && !(name == "ClosureNew")) {
          JetUncMap[name]->setJetEta(jet.eta());
          JetUncMap[name]->setJetPt(jet.pt());
          unc = JetUncMap[name]->getUncertainty(true);
        }

        // Save our factorized uncertainties into a cumulative total
        // Apply this uncertainty to loop "Closure" for future
        // comparison (also skip SubTotals)
        // ALL factorized uncertainties pass this if statment
        if ( !(name == "Total") && !(name == "Closure") && !(name == "EC2") && !(name == "Eta0to3") && 
              !(name == "Eta0to5") && !(name == "Eta3to5") && !(name == "ClosureNew")) {
          // All 28
          factorizedTotalUp[i] += unc*unc;

          // Uncertainties focused in center of detector
          if ((name == "PileUpPtEC1") ||
              (name == "PileUpPtBB") ||
              (name == "RelativeJEREC1") ||
              (name == "RelativePtEC1") ||
              (name == "RelativeStatEC") ||
              (name == "RelativePtBB") )
                  factorizedEta0to3Up[i] += unc*unc;

          // Uncertainties affecting the entire detector
          if ((name == "SinglePionECAL") ||
              (name == "SinglePionHCAL") ||
              (name == "AbsoluteFlavMap") ||
              (name == "AbsoluteMPFBias") ||
              (name == "AbsoluteScale") ||
              (name == "AbsoluteStat") ||
              (name == "Fragmentation") ||
              (name == "FlavorQCD") ||
              (name == "TimePtEta") ||
              (name == "PileUpDataMC") ||
              (name == "RelativeFSR") ||
              (name == "RelativeStatFSR") ||
              (name == "PileUpPtRef") )
                  factorizedEta0to5Up[i] += unc*unc;

          // Uncertainties focused in forward region of detector
          if ((name == "RelativeStatHF") ||
              (name == "RelativePtHF") ||
              (name == "PileUpPtHF") ||
              (name == "RelativeJERHF") )
                  factorizedEta3to5Up[i] += unc*unc;

          if ((name == "PileUpPtEC2") ||
              (name == "RelativeJEREC2") ||
              (name == "RelativePtEC2") )
                  factorizedEC2Up[i] += unc*unc;

          // New closure test for updated method
          // These two contributed here and the Eta split regions are
          // summed below
          if ((name == "RelativeBal") ||
              (name == "RelativeSample") )
                  factorizedClosureNewUp[i] += unc*unc;
        }

        // std::vector is ordered, so Closure comes after all 28 factorized
        // options.  Same for the below Eta regions
        if (name == "Closure") {
          unc = std::sqrt(factorizedTotalUp[i]);
        }
        if (name == "Eta0to3") {
          unc = std::sqrt(factorizedEta0to3Up[i]);
          factorizedClosureNewUp[i] += unc*unc;
        }
        if (name == "Eta0to5") {
          unc = std::sqrt(factorizedEta0to5Up[i]);
          factorizedClosureNewUp[i] += unc*unc;
        }
        if (name == "Eta3to5") {
          unc = std::sqrt(factorizedEta3to5Up[i]);
          factorizedClosureNewUp[i] += unc*unc;
        }
        if (name == "EC2") {
          unc = std::sqrt(factorizedEC2Up[i]);
          factorizedClosureNewUp[i] += unc*unc;
        }
        if (name == "ClosureNew")
          unc = std::sqrt(factorizedClosureNewUp[i]);
      } // Shifted jets within absEta and pT

  
      // Get uncorrected pt
      assert(jet.jecSetsAvailable());
  
      LorentzVector uncDown = (1-unc)*jet.p4();
      LorentzVector uncUp = (1+unc)*jet.p4();
  
      //std::cout << name << ":  jet pt: " << jet.pt() << "  unc: " << unc << std::endl;
  
      ShiftedCand candUncDown = jet;
      candUncDown.setP4(uncDown);
      ShiftedCand candUncUp = jet;
      candUncUp.setP4(uncUp);
  
      p4OutJESUpJets->push_back(candUncUp);
      p4OutJESDownJets->push_back(candUncDown);
    }
 
    PutHandle p4OutJESUpJetsH = evt.put(std::move(p4OutJESUpJets), std::string("p4OutJESUpJetsUncor"+name));
    PutHandle p4OutJESDownJetsH = evt.put(std::move(p4OutJESDownJets), std::string("p4OutJESDownJetsUncor"+name));
  
    // Now embed the shifted collections into our output pat jets
    for (size_t i = 0; i < output->size(); ++i) {
      pat::Jet& jet = output->at(i);
      //std::cout << "Jet " << i << " uncorr pt: " << jet.pt() << std::endl;
      jet.addUserCand("jes"+name+"+", CandidatePtr(p4OutJESUpJetsH, i));
      jet.addUserCand("jes"+name+"-", CandidatePtr(p4OutJESDownJetsH, i));
  } // end jets

  } // end cycle over all uncertainties

  evt.put(std::move(output));




}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetFullSystematicsEmbedder);
