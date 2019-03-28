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
   "RelativeSample", // New for 2017
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
   "Eta3to5",
   "Eta0to5",
   "Eta0to3",
   "EC2",
   "Closure"
  }; // end uncertNames
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
 srcToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("src"));
 srcMETToken_ = consumes<edm::View<pat::MET> >(pset.getParameter<edm::InputTag>("srcMET"));
 label_ = pset.getParameter<std::string>("corrLabel");
 fName_ = pset.getParameter<std::string>("fName");
 std::cout << "Uncert File: " << fName_ << std::endl;
 produces<pat::METCollection>();//"METMETJesSystematics");

 produces<ShiftedCandCollection>("p4OutMETUpJetsUncorUESUP");
 produces<ShiftedCandCollection>("p4OutMETDownJetsUncorUESDOWN");


 for (auto const& name : uncertNames) {
  produces<ShiftedCandCollection>("p4OutMETUpJetsUncor"+name);
  produces<ShiftedCandCollection>("p4OutMETDownJetsUncor"+name);
  // Create the uncertainty tool for each uncert
  // skip Closure, which is a comparison at the end
  if (name == "Closure" or name=="Eta0to3" or name=="Eta0to5" or name=="Eta3to5" or name=="EC2") continue;
  JetCorrectorParameters const * JetCorPar = new JetCorrectorParameters(fName_, name);
  JetCorParMap[name] = JetCorPar;

  JetCorrectionUncertainty * jecUnc(
    new JetCorrectionUncertainty(*JetCorParMap[name]));
  JetUncMap[name] = jecUnc;
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

 bool skipMuons_=true;


 // For comparing with Total for Closure test
 // assume symmetric uncertainties and ignore Down
 std::vector<double> factorizedTotalUp(nJets, 0.0);
 std::vector<double> factorizedEta0to3Up(nJets, 0.0);
 std::vector<double> factorizedEta0to5Up(nJets, 0.0);
 std::vector<double> factorizedEta3to5Up(nJets, 0.0);
 std::vector<double> factorizedEC2Up(nJets, 0.0);

 for (auto const& name : uncertNames) {
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

   // This is not used right now: 
   // In the MET twiki, this code is referenced when computing the Type1 corrections.
   // For what we are doing it is not working out of the box - we would need to go further and fully uncorrect
   // and propagate the uncertainties?  
   // Assuming just the Change of JES on top of the existing jet pt seems to
   // be enough to get a result close enough to the value already stored in miniAOD for "total", so sticking to that
   // one for now 
//   if ( skipMuons_ ) {
//    const std::vector<reco::CandidatePtr> & cands = jet.daughterPtrVector();
//    for ( std::vector<reco::CandidatePtr>::const_iterator cand = cands.begin();
//      cand != cands.end(); ++cand ) {
//     const reco::PFCandidate *pfcand = dynamic_cast<const reco::PFCandidate *>(cand->get());
//     const reco::Candidate *mu = (pfcand != 0 ? ( pfcand->muonRef().isNonnull() ? pfcand->muonRef().get() : 0) : cand->get());
//     if ( mu != 0 ) {
//      reco::Candidate::LorentzVector muonP4 = (*cand)->p4();
//      //if(muonP4> ??? ) 
//      JetP4 -= muonP4;
//     }
//    }
//   }
   double unc = 0;
   //double unc2=0;
   if (std::fabs(jet.eta()) < 5.2 && JetP4.pt() > 9 && name != "Closure" && !(name == "Eta0to3") && !(name == "EC2") && !(name == "Eta0to5") && !(name == "Eta3to5") && !(name == "ClosureNew")) {
    JetUncMap[name]->setJetEta(JetP4.eta());
    JetUncMap[name]->setJetPt(JetP4.pt());
    unc = JetUncMap[name]->getUncertainty(true);  //up
    JetUncMap[name]->setJetEta(JetP4.eta());
    JetUncMap[name]->setJetPt(JetP4.pt());
    //unc2 = JetUncMap[name]->getUncertainty(false);   // down
   }

   // Save our factorized uncertainties into a cumulative total
   // Apply this uncertainty to loop "Closure" for future
   // comparison (also skim SubTotals)
   if (name != "Total" && name != "Closure" && name != "Eta0to3" && name != "Eta3to5" && name != "Eta0to5" && name != "EC2" && !name.find("SubTotal") ) factorizedTotalUp[i] += unc*unc;

   if (std::abs(jet.eta()) < 5.2 && jet.pt() > 9) {
       // Save our factorized uncertainties into a cumulative total
        // Apply this uncertainty to loop "Closure" for future
        // comparison (also skip SubTotals)
        // ALL factorized uncertainties pass this if statment
        if ( !(name == "Total") && !(name == "Closure") && !(name == "Eta0to3") && !(name == "EC2") && 
              !(name == "Eta0to5") && !(name == "Eta3to5") && !(name == "ClosureNew") ) {
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
        }
        // std::vector is ordered, so Closure comes after all 28 factorized
        // options.  Same for the below Eta regions
        if (name == "Closure") {
          unc = std::sqrt(factorizedTotalUp[i]);
        }
        if (name == "Eta0to3") {
          unc = std::sqrt(factorizedEta0to3Up[i]);
        }
        if (name == "Eta0to5") {
          unc = std::sqrt(factorizedEta0to5Up[i]);
        }
        if (name == "Eta3to5") {
          unc = std::sqrt(factorizedEta3to5Up[i]);
        }
        if (name == "EC2") {
          unc = std::sqrt(factorizedEC2Up[i]);
        }
     } // Shifted jets within absEta and pT


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
  PutHandle p4OutMETUpJetsH = evt.put(std::move(p4OutMETUpJets), std::string("p4OutMETUpJetsUncor"+name));
  extendedMET.addUserCand("jes"+name+"+", CandidatePtr(p4OutMETUpJetsH, 0));

  ShiftedCand newCandDOWN =  extendedMET;
  newCandDOWN.setP4(NEWMETDOWN);
  p4OutMETDownJets->push_back(newCandDOWN);
  PutHandle p4OutMETDownJetsH = evt.put(std::move(p4OutMETDownJets), std::string("p4OutMETDownJetsUncor"+name));
  extendedMET.addUserCand("jes"+name+"-", CandidatePtr(p4OutMETDownJetsH, 0));
  //

  } // end cycle over all uncertainties

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


  //std::cout<<" CENTRAL FROM TOOL: "<<extendedMET.shiftedPt(pat::MET::JetEnUp)<<"   "<<extendedMET.shiftedPt(pat::MET::JetEnDown)<<std::endl;;
  //std::cout<<" UES: "<<extendedMET.shiftedPt(pat::MET::UnclusteredEnUp)<<"   "<<extendedMET.shiftedPt(pat::MET::UnclusteredEnDown)<<std::endl;;

  outputMET->push_back(extendedMET);

  //    pat::MET&  test= outputMET->at(0);
  //    std::cout<<test.pt()<<"  "<<test.userCand("jesTotal+")->p4().pt()<<std::endl;

    evt.put(std::move(outputMET));//,"METMETJesSystematics");




 }

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODMETJesSystematicsEmbedder);

