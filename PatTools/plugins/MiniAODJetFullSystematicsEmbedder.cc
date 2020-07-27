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

  output->reserve(jets->size());
  for (size_t i = 0; i < jets->size(); ++i) {
    pat::Jet jet = jets->at(i);

    int k=-1;
    for (auto const& name : uncertNames) {
      k=k+1;
      double unc = 0;
      if (std::abs(jet.eta()) < 5.2 && jet.pt() > 9) {
          JetUncMap[name]->setJetEta(jet.eta());
          JetUncMap[name]->setJetPt(jet.pt());
          unc = JetUncMap[name]->getUncertainty(true);
      } // Shifted jets within absEta and pT
      float ptplus=(1+unc)*jet.pt();
      float ptminus=(1-unc)*jet.pt();
      jet.addUserFloat("jes"+outputNames[k]+"+", ptplus);
      jet.addUserFloat("jes"+outputNames[k]+"-", ptminus);
    } // end loop over uncertainties
    output->push_back(jet);
  } // end loop over jets

  evt.put(std::move(output));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetFullSystematicsEmbedder);
