#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

class MiniAODMETUesSystEmbedder : public edm::EDProducer {
 public:
  typedef reco::LeafCandidate ShiftedCand;
  typedef std::vector<ShiftedCand> ShiftedCandCollection;
  typedef reco::CandidatePtr CandidatePtr;
  typedef reco::Candidate::LorentzVector LorentzVector;

  MiniAODMETUesSystEmbedder(const edm::ParameterSet& pset);
  virtual ~MiniAODMETUesSystEmbedder(){}
  void produce(edm::Event& evt, const edm::EventSetup& es);
 private:
  typedef edm::OrphanHandle<ShiftedCandCollection> PutHandle;
  edm::EDGetTokenT<edm::View<pat::MET> > srcMETToken_;
  edm::EDGetTokenT<edm::View<reco::Candidate> > srcPFUnclustered_;

  std::string label_;
  std::string fName_;
};

// Get the transverse component of the vector
reco::Candidate::LorentzVector
transverseVectorOnly(const reco::Candidate::LorentzVector& input) {
 math::PtEtaPhiMLorentzVector outputV(input.pt(), 0, input.phi(), 0);
 reco::Candidate::LorentzVector outputT(outputV);
 return outputT;
}



MiniAODMETUesSystEmbedder::MiniAODMETUesSystEmbedder(const edm::ParameterSet& pset) {
 srcMETToken_ = consumes<edm::View<pat::MET> >(pset.getUntrackedParameter<edm::InputTag>("srcMET",edm::InputTag("slimmedMETs")));
 srcPFUnclustered_ = consumes<edm::View<reco::Candidate> >(pset.getUntrackedParameter<edm::InputTag>("srcPF",edm::InputTag("pfCandsForUnclusteredUnc"))); 

 produces<pat::METCollection>();//"METMETJesSystematics");

  produces<ShiftedCandCollection>("p4OutMETUesUP");
  produces<ShiftedCandCollection>("p4OutMETUesDOWN");
  produces<ShiftedCandCollection>("p4OutMETUesHCALUP");
  produces<ShiftedCandCollection>("p4OutMETUesHCALDOWN");
  produces<ShiftedCandCollection>("p4OutMETUesHFUP");
  produces<ShiftedCandCollection>("p4OutMETUesHFDOWN");
  produces<ShiftedCandCollection>("p4OutMETUesCHARGEDUP");
  produces<ShiftedCandCollection>("p4OutMETUesCHARGEDDOWN");
  produces<ShiftedCandCollection>("p4OutMETUesECALUP");
  produces<ShiftedCandCollection>("p4OutMETUesECALDOWN");

}

void MiniAODMETUesSystEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {

  edm::Handle<edm::View<reco::Candidate>> candidateParticles;
  evt.getByToken(srcPFUnclustered_, candidateParticles);

  std::auto_ptr<pat::METCollection> outputMET(new pat::METCollection);

 edm::Handle<edm::View<pat::MET> > mets;
 evt.getByToken(srcMETToken_, mets);
 assert(mets->size() == 1);
 const pat::MET& inputMET = mets->at(0);
 pat::MET extendedMET = inputMET;

  LorentzVector NEWMETUP=extendedMET.p4();
  LorentzVector NEWMETDOWN=extendedMET.p4();

  LorentzVector NEWMETUPHCAL=extendedMET.p4();
  LorentzVector NEWMETDOWNHCAL=extendedMET.p4();

  LorentzVector NEWMETUPHF=extendedMET.p4();
  LorentzVector NEWMETDOWNHF=extendedMET.p4();

  LorentzVector NEWMETUPECAL=extendedMET.p4();
  LorentzVector NEWMETDOWNECAL=extendedMET.p4();

  LorentzVector NEWMETUPCHARGED=extendedMET.p4();
  LorentzVector NEWMETDOWNCHARGED=extendedMET.p4();


  for(edm::View<reco::Candidate>::const_iterator originalParticle = candidateParticles->begin();
      originalParticle != candidateParticles->end(); ++originalParticle ) {

    double uncertainty = 0.1;
    double uncertaintyHCAL=0; 
    double uncertaintyHF=0;
    double uncertaintyECAL=0;
    double uncertaintyCHARGED=0;

    if(originalParticle->pdgId()==130) {
           if(fabs(originalParticle->eta())<1.3){
                        uncertaintyHCAL=TMath::Min(0.25,sqrt(0.64/originalParticle->energy()+0.0025));  // is this min (code) or max (pres?)
           }else{
                        uncertaintyHCAL=TMath::Min(0.30,sqrt(1.0/originalParticle->energy()+0.0016)); 
           } 
         NEWMETUPHCAL-=transverseVectorOnly(originalParticle->p4()*uncertaintyHCAL);
         NEWMETDOWNHCAL-=transverseVectorOnly(originalParticle->p4()*(-1)*uncertaintyHCAL);
     }
    else if( abs(originalParticle->pdgId())==1 || abs(originalParticle->pdgId())==2) {
                        uncertaintyHF=sqrt(1.0/originalParticle->energy()+0.0025); 
         NEWMETUPHF-=transverseVectorOnly(originalParticle->p4()*uncertaintyHF);
         NEWMETDOWNHF-=transverseVectorOnly(originalParticle->p4()*(-1)*uncertaintyHF);
     }
    else if( originalParticle->pdgId()==22) {
                        uncertaintyECAL=sqrt(0.0009/originalParticle->energy()+0.000001);
         NEWMETUPECAL-=transverseVectorOnly(originalParticle->p4()*uncertaintyECAL);
         NEWMETDOWNECAL-=transverseVectorOnly(originalParticle->p4()*(-1)*uncertaintyECAL);
     }
    else if( originalParticle->charge()!=0) {
                        uncertaintyCHARGED=sqrt(  pow(0.00009*originalParticle->pt(),2) + pow(0.0085/sqrt( sin (2*atan(exp(-originalParticle->eta()))) ) ,2)); 
         NEWMETUPCHARGED-=transverseVectorOnly(originalParticle->p4()*uncertaintyCHARGED);
         NEWMETDOWNCHARGED-=transverseVectorOnly(originalParticle->p4()*(-1)*uncertaintyCHARGED);
     }

    NEWMETUP-=transverseVectorOnly(originalParticle->p4()*uncertainty);  
    NEWMETDOWN-=transverseVectorOnly(originalParticle->p4()*(-1)*uncertainty);

  }    

  std::auto_ptr<ShiftedCandCollection> p4OutMETUpUes(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutMETDownUes(new ShiftedCandCollection);

  ShiftedCand newCandUP =  extendedMET;
  newCandUP.setP4(NEWMETUP);
  p4OutMETUpUes->push_back(newCandUP);
  PutHandle p4OutMETUpUesH = evt.put(p4OutMETUpUes, "p4OutMETUesUP");
  extendedMET.addUserCand("metSystUesRunI+", CandidatePtr(p4OutMETUpUesH, 0));

  ShiftedCand newCandDOWN =  extendedMET;
  newCandDOWN.setP4(NEWMETDOWN);
  p4OutMETDownUes->push_back(newCandDOWN);
  PutHandle p4OutMETDownUesH = evt.put(p4OutMETDownUes, "p4OutMETUesDOWN");
  extendedMET.addUserCand("metSystUesRunI-", CandidatePtr(p4OutMETDownUesH, 0));


  std::auto_ptr<ShiftedCandCollection> p4OutMETUpUesHCAL(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutMETDownUesHCAL(new ShiftedCandCollection);

  ShiftedCand newCandUPHCAL =  extendedMET;
  newCandUPHCAL.setP4(NEWMETUPHCAL);
  p4OutMETUpUesHCAL->push_back(newCandUPHCAL);
  PutHandle p4OutMETUpUesHCALH = evt.put(p4OutMETUpUesHCAL, "p4OutMETUesHCALUP");
  extendedMET.addUserCand("metSystUesHCAL+", CandidatePtr(p4OutMETUpUesHCALH, 0));

  ShiftedCand newCandDOWNHCAL =  extendedMET;
  newCandDOWNHCAL.setP4(NEWMETDOWNHCAL);
  p4OutMETDownUesHCAL->push_back(newCandDOWNHCAL);
  PutHandle p4OutMETDownUesHCALH = evt.put(p4OutMETDownUesHCAL, "p4OutMETUesHCALDOWN");
  extendedMET.addUserCand("metSystUesHCAL-", CandidatePtr(p4OutMETDownUesHCALH, 0));


  std::auto_ptr<ShiftedCandCollection> p4OutMETUpUesHF(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutMETDownUesHF(new ShiftedCandCollection);

  ShiftedCand newCandUPHF =  extendedMET;
  newCandUPHF.setP4(NEWMETUPHF);
  p4OutMETUpUesHF->push_back(newCandUPHF);
  PutHandle p4OutMETUpUesHFH = evt.put(p4OutMETUpUesHF, "p4OutMETUesHFUP");
  extendedMET.addUserCand("metSystUesHF+", CandidatePtr(p4OutMETUpUesHFH, 0));

  ShiftedCand newCandDOWNHF =  extendedMET;
  newCandDOWNHF.setP4(NEWMETDOWNHF);
  p4OutMETDownUesHF->push_back(newCandDOWNHF);
  PutHandle p4OutMETDownUesHFH = evt.put(p4OutMETDownUesHF, "p4OutMETUesHFDOWN");
  extendedMET.addUserCand("metSystUesHF-", CandidatePtr(p4OutMETDownUesHFH, 0));


  std::auto_ptr<ShiftedCandCollection> p4OutMETUpUesECAL(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutMETDownUesECAL(new ShiftedCandCollection);

  ShiftedCand newCandUPECAL =  extendedMET;
  newCandUPECAL.setP4(NEWMETUPECAL);
  p4OutMETUpUesECAL->push_back(newCandUPECAL);
  PutHandle p4OutMETUpUesECALH = evt.put(p4OutMETUpUesECAL, "p4OutMETUesECALUP");
  extendedMET.addUserCand("metSystUesECAL+", CandidatePtr(p4OutMETUpUesECALH, 0));

  ShiftedCand newCandDOWNECAL =  extendedMET;
  newCandDOWNECAL.setP4(NEWMETDOWNECAL);
  p4OutMETDownUesECAL->push_back(newCandDOWNECAL);
  PutHandle p4OutMETDownUesECALH = evt.put(p4OutMETDownUesECAL, "p4OutMETUesECALDOWN");
  extendedMET.addUserCand("metSystUesECAL-", CandidatePtr(p4OutMETDownUesECALH, 0));




  std::auto_ptr<ShiftedCandCollection> p4OutMETUpUesCHARGED(new ShiftedCandCollection);
  std::auto_ptr<ShiftedCandCollection> p4OutMETDownUesCHARGED(new ShiftedCandCollection);

  ShiftedCand newCandUPCHARGED =  extendedMET;
  newCandUPCHARGED.setP4(NEWMETUPCHARGED);
  p4OutMETUpUesCHARGED->push_back(newCandUPCHARGED);
  PutHandle p4OutMETUpUesCHARGEDH = evt.put(p4OutMETUpUesCHARGED, "p4OutMETUesCHARGEDUP");
  extendedMET.addUserCand("metSystUesCHARGED+", CandidatePtr(p4OutMETUpUesCHARGEDH, 0));

  ShiftedCand newCandDOWNCHARGED =  extendedMET;
  newCandDOWNCHARGED.setP4(NEWMETDOWNCHARGED);
  p4OutMETDownUesCHARGED->push_back(newCandDOWNCHARGED);
  PutHandle p4OutMETDownUesCHARGEDH = evt.put(p4OutMETDownUesCHARGED, "p4OutMETUesCHARGEDDOWN");
  extendedMET.addUserCand("metSystUesCHARGED-", CandidatePtr(p4OutMETDownUesCHARGEDH, 0));






  outputMET->push_back(extendedMET);

/*
      pat::MET&  test= outputMET->at(0);
      std::cout<<test.pt()<<"  "<<test.userCand("metSystUesRunI-")->p4().pt()<<"  "<<test.userCand("metSystUesRunI+")->p4().pt()<<std::endl;
      std::cout<<test.pt()<<"  "<<test.userCand("metSystUesHCAL-")->p4().pt()<<"  "<<test.userCand("metSystUesHCAL+")->p4().pt()<<std::endl;
      std::cout<<test.pt()<<"  "<<test.userCand("metSystUesHF-")->p4().pt()<<"  "<<test.userCand("metSystUesHF+")->p4().pt()<<std::endl;
      std::cout<<test.pt()<<"  "<<test.userCand("metSystUesECAL-")->p4().pt()<<"  "<<test.userCand("metSystUesECAL+")->p4().pt()<<std::endl;
      std::cout<<test.pt()<<"  "<<test.userCand("metSystUesCHARGED-")->p4().pt()<<"  "<<test.userCand("metSystUesCHARGED+")->p4().pt()<<std::endl;
*/


  evt.put(outputMET);//,"METMETJesSystematics");




 }

#include "FWCore/Framework/interface/MakerMacros.h"
 DEFINE_FWK_MODULE(MiniAODMETUesSystEmbedder);
