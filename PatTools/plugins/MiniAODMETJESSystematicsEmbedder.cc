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

#include <string>

class MiniAODMETJesSystematicsEmbedder : public edm::EDProducer {
 public:
  typedef reco::LeafCandidate ShiftedCand;
  typedef std::vector<ShiftedCand> ShiftedCandCollection;
  typedef reco::CandidatePtr CandidatePtr;
  typedef reco::Candidate::LorentzVector LorentzVector;

  MiniAODMETJesSystematicsEmbedder(const edm::ParameterSet& pset);
  virtual ~MiniAODMETJesSystematicsEmbedder(){}
  void produce(edm::Event& evt, const edm::EventSetup& es);
 private:
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  edm::EDGetTokenT<edm::View<pat::Jet> > srcToken_;
  edm::EDGetTokenT<edm::View<pat::MET> > srcMETToken_;
  edm::EDGetTokenT<edm::View<pat::MET> > srcDownMETToken_;
  edm::EDGetTokenT<edm::View<pat::MET> > srcUpMETToken_;
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
    "RelativeSample"
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
    "RelativeSample_2016"
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
    "RelativeSample_2017"
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
    "RelativeSample_2018"
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
    "RelativeSample"
    };

  std::map<std::string, JetCorrectorParameters const *> JetCorParMap;
  std::map<std::string, JetCorrectionUncertainty* > JetUncMap;
};

// Get the transverse component of the vector
reco::Candidate::LorentzVector
transverseVEC(const reco::Candidate::LorentzVector& input) {
 math::PtEtaPhiMLorentzVector outputV(input.pt(), 0, input.phi(), 0);
 reco::Candidate::LorentzVector outputT(outputV);
 return outputT;
}



MiniAODMETJesSystematicsEmbedder::MiniAODMETJesSystematicsEmbedder(const edm::ParameterSet& pset) {
 std::cout<<"MET uncert"<<std::endl;
 srcToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("src"));
 srcMETToken_ = consumes<edm::View<pat::MET> >(pset.getParameter<edm::InputTag>("srcMET"));
 srcUpMETToken_ = consumes<edm::View<pat::MET> >(pset.getParameter<edm::InputTag>("upMET"));
 srcDownMETToken_ = consumes<edm::View<pat::MET> >(pset.getParameter<edm::InputTag>("downMET"));
 label_ = pset.getParameter<std::string>("corrLabel");
 fName_ = pset.getParameter<std::string>("fName");
 std::cout << "Uncert File: " << fName_ << std::endl;
 produces<pat::METCollection>();//"METMETJesSystematics");

 produces<ShiftedCandCollection>("p4OutMETUpJetsUncorUESUP");
 produces<ShiftedCandCollection>("p4OutMETDownJetsUncorUESDOWN");
 produces<ShiftedCandCollection>("METJERUp");
 produces<ShiftedCandCollection>("METJERDown");

  size_t found2016 = fName_.find("Summer16");
  size_t found2017 = fName_.find("Fall17");
  size_t found2018 = fName_.find("Autumn18");

  int k=0;
  for (auto const& name : uncertNames) {
     if (found2016!=std::string::npos) uncertNames[k]=uncertNames2016[k];
     if (found2017!=std::string::npos) uncertNames[k]=uncertNames2017[k];
     if (found2018!=std::string::npos) uncertNames[k]=uncertNames2018[k];
     k=k+1;
  }

 k=0;
 for (auto const& name : uncertNames) {
  produces<ShiftedCandCollection>("p4OutMETUpJetsUncor"+outputNames[k]);
  produces<ShiftedCandCollection>("p4OutMETDownJetsUncor"+outputNames[k]);

  // Create the uncertainty tool for each uncert
  JetCorrectorParameters const * JetCorPar = new JetCorrectorParameters(fName_, name);
  JetCorParMap[name] = JetCorPar;

  JetCorrectionUncertainty * jecUnc(
    new JetCorrectionUncertainty(*JetCorParMap[name]));
  JetUncMap[name] = jecUnc;
  k=k+1;
 };
}

void MiniAODMETJesSystematicsEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {


 std::unique_ptr<pat::METCollection> outputMET(new pat::METCollection);

 edm::Handle<edm::View<pat::Jet> > jets;
 evt.getByToken(srcToken_, jets);
 size_t nJets = jets->size();


 edm::Handle<edm::View<pat::MET> > mets;
 evt.getByToken(srcMETToken_, mets);
 assert(mets->size() == 1);
 const pat::MET& inputMET = mets->at(0);
 pat::MET extendedMET = inputMET;

 edm::Handle<edm::View<pat::MET> > mets_jerdown;
 evt.getByToken(srcDownMETToken_, mets_jerdown);
 const pat::MET& inputMET_JERDown = mets_jerdown->at(0);
 pat::MET extendedMET_JERDown = inputMET_JERDown;

 edm::Handle<edm::View<pat::MET> > mets_jerup;
 evt.getByToken(srcUpMETToken_, mets_jerup);
 const pat::MET& inputMET_JERUp = mets_jerup->at(0);
 pat::MET extendedMET_JERUp = inputMET_JERUp;

 bool skipMuons_=true;

 int k=-1;
 for (auto const& name : uncertNames) {
  k=k+1;
  std::unique_ptr<ShiftedCandCollection> p4OutMETUpJets(new ShiftedCandCollection);
  std::unique_ptr<ShiftedCandCollection> p4OutMETDownJets(new ShiftedCandCollection);

  LorentzVector nominalJetP4(0,0,0,0);
  LorentzVector jesUpJetP4(0,0,0,0);
  LorentzVector jesDownJetP4(0,0,0,0);
  LorentzVector NEWMETUP=inputMET.p4();
  LorentzVector NEWMETDOWN=inputMET.p4();

  for (size_t i = 0; i < nJets; ++i) {
   const pat::Jet& jet = jets->at(i);

   LorentzVector JetP4= jet.p4();

   double unc = 0;
   //double unc2=0;
   if (std::fabs(jet.eta()) < 5.2 && JetP4.pt() > 9) {
    JetUncMap[name]->setJetEta(JetP4.eta());
    JetUncMap[name]->setJetPt(JetP4.pt());
    unc = JetUncMap[name]->getUncertainty(true);  //up
    JetUncMap[name]->setJetEta(JetP4.eta());
    JetUncMap[name]->setJetPt(JetP4.pt());
    //unc2 = JetUncMap[name]->getUncertainty(false);   // down
   }

   // Get uncorrected pt
   assert(jet.jecSetsAvailable());

   LorentzVector uncDown = (1-unc)*JetP4;
   LorentzVector uncUp = (1+unc)*JetP4;

   //std::cout << name << ":  uncDown pt: " << uncDown.pt() << " ,uncUp pt: " << uncUp.pt() << std::endl;

   // Double check if we need more cleaning, this is the bare minimum:
   if(JetP4.pt()<15 || fabs(JetP4.eta())>5.2) continue;


   ShiftedCand candUncDown = jet;
   candUncDown.setP4(uncDown);
   ShiftedCand candUncUp = jet;
   candUncUp.setP4(uncUp);

   nominalJetP4+=JetP4;
   jesUpJetP4+=candUncUp.p4();
   jesDownJetP4+=candUncDown.p4();

  }
  NEWMETUP+=transverseVEC(nominalJetP4-jesUpJetP4); 
  NEWMETDOWN+=transverseVEC(nominalJetP4-jesDownJetP4);

  //std::cout<<"jes"+name<<"   "<<inputMET.pt()<<"   "<<NEWMETUP.pt()<<"   "<<NEWMETDOWN.pt()<<std::endl;

  ShiftedCand newCandUP =  extendedMET;
  newCandUP.setP4(NEWMETUP);
  p4OutMETUpJets->push_back(newCandUP);
  PutHandle p4OutMETUpJetsH = evt.put(std::move(p4OutMETUpJets), std::string("p4OutMETUpJetsUncor"+outputNames[k]));
  extendedMET.addUserCand("jes"+outputNames[k]+"+", CandidatePtr(p4OutMETUpJetsH, 0));

  ShiftedCand newCandDOWN =  extendedMET;
  newCandDOWN.setP4(NEWMETDOWN);
  p4OutMETDownJets->push_back(newCandDOWN);
  PutHandle p4OutMETDownJetsH = evt.put(std::move(p4OutMETDownJets), std::string("p4OutMETDownJetsUncor"+outputNames[k]));
  extendedMET.addUserCand("jes"+outputNames[k]+"-", CandidatePtr(p4OutMETDownJetsH, 0));
  //

  } // end cycle over all uncertainties

  std::unique_ptr<ShiftedCandCollection> METUpJets(new ShiftedCandCollection);
  std::unique_ptr<ShiftedCandCollection> METDownJets(new ShiftedCandCollection);

  
  ShiftedCand jerCandUP =  extendedMET_JERUp;
  METUpJets->push_back(jerCandUP);
  PutHandle p4OutMETUpJetsRH = evt.put(std::move(METUpJets), std::string("METJERUp"));
  extendedMET.addUserCand("jer+", CandidatePtr(p4OutMETUpJetsRH, 0));

  ShiftedCand jerCandDOWN =  extendedMET_JERDown;
  METDownJets->push_back(jerCandDOWN);
  PutHandle p4OutMETDownJetsRH = evt.put(std::move(METDownJets), std::string("METJERDown"));
  extendedMET.addUserCand("jer-", CandidatePtr(p4OutMETDownJetsRH, 0));

  LorentzVector nominalJetP4(0,0,0,0);

  // For a ROUGH check of the unclustered -- this is actually incomplete, we should also subtract the muons, electrons (taus?) 
  for (size_t i = 0; i < nJets; ++i) { 
   const pat::Jet& jet = jets->at(i); 
   LorentzVector JetP4= jet.p4();
   if(JetP4.pt()<15 || fabs(JetP4.eta())>5.2) continue;  
   nominalJetP4+=JetP4;
  }   
  LorentzVector METNOJETS=inputMET.p4()+transverseVEC(nominalJetP4);
  LorentzVector NEWMETUP=METNOJETS*1.1-transverseVEC(nominalJetP4);
  LorentzVector NEWMETDOWN=METNOJETS*0.9-transverseVEC(nominalJetP4);
  //std::cout<<"check UES"<<"   "<<inputMET.pt()<<"   "<<NEWMETUP.pt()<<"   "<<NEWMETDOWN.pt()<<std::endl;

  std::unique_ptr<ShiftedCandCollection> p4OutMETUpJets(new ShiftedCandCollection);
  std::unique_ptr<ShiftedCandCollection> p4OutMETDownJets(new ShiftedCandCollection);

  ShiftedCand newCandUP =  extendedMET;
  newCandUP.setP4(NEWMETUP);
  p4OutMETUpJets->push_back(newCandUP);
  PutHandle p4OutMETUpJetsH = evt.put(std::move(p4OutMETUpJets), std::string("p4OutMETUpJetsUncorUESUP"));
  extendedMET.addUserCand("checkUES+", CandidatePtr(p4OutMETUpJetsH, 0));

  ShiftedCand newCandDOWN =  extendedMET;
  newCandDOWN.setP4(NEWMETDOWN);
  p4OutMETDownJets->push_back(newCandDOWN);
  PutHandle p4OutMETDownJetsH = evt.put(std::move(p4OutMETDownJets), std::string("p4OutMETDownJetsUncorUESDOWN"));
  extendedMET.addUserCand("checkUES-", CandidatePtr(p4OutMETDownJetsH, 0));

  outputMET->push_back(extendedMET);

    evt.put(std::move(outputMET));//,"METMETJesSystematics");

 }

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODMETJesSystematicsEmbedder);

