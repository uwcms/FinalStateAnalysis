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

#include <algorithm>
#include <string>

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
    std::string fName_;
    std::vector< std::string > outputNames = {
    "Absolute", 
    "Absoluteyear", 
    "BBEC1",
    "BBEC1year",
    "EC2", 
    "EC2year",
    "FlavorQCD",
    "HF",
    "HFyear",
    "RelativeBal",
    "RelativeSample",
    "Total"
    };

    std::vector< std::string > uncertNames2016 = {
    "Absolute",
    "Absolute_2016",
    "BBEC1",
    "BBEC1_2016",
    "EC2",
    "EC2_2016",
    "FlavorQCD",
    "HF",
    "HF_2016",
    "RelativeBal",
    "RelativeSample_2016",
    "Total"
    };

    std::vector< std::string > uncertNames2017 = {
    "Absolute",
    "Absolute_2017",
    "BBEC1",
    "BBEC1_2017",
    "EC2",
    "EC2_2017",
    "FlavorQCD",
    "HF",
    "HF_2017",
    "RelativeBal",
    "RelativeSample_2017",
    "Total"
    };

    std::vector< std::string > uncertNames2018 = {
    "Absolute",
    "Absolute_2018",
    "BBEC1",
    "BBEC1_2018",
    "EC2",
    "EC2_2018",
    "FlavorQCD",
    "HF",
    "HF_2018",
    "RelativeBal",
    "RelativeSample_2018",
    "Total"
    };

    std::vector< std::string > uncertNames = {
    "Absolute",
    "Absoluteyear",
    "BBEC1",
    "BBEC1year",
    "EC2",
    "EC2year",
    "FlavorQCD",
    "HF",
    "HFyear",
    "RelativeBal",
    "RelativeSample",
    "Total"
    };

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

  size_t found2016 = fName_.find("Summer16");
  size_t found2017 = fName_.find("Fall17");
  size_t found2018 = fName_.find("Autumn18");

  int k=0;
  for (auto const& name : uncertNames) {
     if (found2016!=std::string::npos) uncertNames[k]=uncertNames2016[k];
     else if (found2017!=std::string::npos) uncertNames[k]=uncertNames2017[k];
     else if (found2018!=std::string::npos) uncertNames[k]=uncertNames2018[k];
     k=k+1;
  }

  // Create the uncertainty tool for each uncert
  k=0;
  for (auto const& name : uncertNames) {
    produces<ShiftedCandCollection>("p4OutJESUpJetsUncor"+outputNames[k]);
    produces<ShiftedCandCollection>("p4OutJESDownJetsUncor"+outputNames[k]);

    JetCorrectorParameters const * JetCorPar = new JetCorrectorParameters(fName_, name);
    JetCorParMap[name] = JetCorPar;

    JetCorrectionUncertainty * jecUnc(
        new JetCorrectionUncertainty(*JetCorParMap[name]));
    JetUncMap[name] = jecUnc;
    k=k+1;
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

  int k=-1;
  for (auto const& name : uncertNames) {
    k=k+1;
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
        if ( !(name == "Closure")) {
          JetUncMap[name]->setJetEta(jet.eta());
          JetUncMap[name]->setJetPt(jet.pt());
          unc = JetUncMap[name]->getUncertainty(true);
        }
      } // Shifted jets within absEta and pT

  
      // Get uncorrected pt
      assert(jet.jecSetsAvailable());

      LorentzVector uncDown = (1-unc)*jet.p4();
      LorentzVector uncUp = (1+unc)*jet.p4();
  
      ShiftedCand candUncDown = jet;
      candUncDown.setP4(uncDown);
      ShiftedCand candUncUp = jet;
      candUncUp.setP4(uncUp);
  
      p4OutJESUpJets->push_back(candUncUp);
      p4OutJESDownJets->push_back(candUncDown);
    }
 
    PutHandle p4OutJESUpJetsH = evt.put(std::move(p4OutJESUpJets), std::string("p4OutJESUpJetsUncor"+outputNames[k]));
    PutHandle p4OutJESDownJetsH = evt.put(std::move(p4OutJESDownJets), std::string("p4OutJESDownJetsUncor"+outputNames[k]));
  
    // Now embed the shifted collections into our output pat jets
    for (size_t i = 0; i < output->size(); ++i) {
      pat::Jet& jet = output->at(i);
      jet.addUserCand("jes"+outputNames[k]+"+", CandidatePtr(p4OutJESUpJetsH, i));
      jet.addUserCand("jes"+outputNames[k]+"-", CandidatePtr(p4OutJESDownJetsH, i));
    } // end jets

  } // end cycle over all uncertainties

  evt.put(std::move(output));

}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetFullSystematicsEmbedder);
