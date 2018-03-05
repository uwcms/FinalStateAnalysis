//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODVertexFittingEmbedder.cc                                          //
//                                                                          //
//   Author: Cecile Caillol, U. Wisconsin                                       //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////


// system includes
#include <memory>
#include <vector>
#include <unordered_map>
#include <utility> // contains std::pair

// CMS includes
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"

// FSA includes
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"


class MiniAODVertexFittingEmbedder : public edm::EDProducer {
 public:
  MiniAODVertexFittingEmbedder(const edm::ParameterSet& pset);
  virtual ~MiniAODVertexFittingEmbedder(){}
 private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  // Calculate the matrix element for fs under process hypothesis proc using calculator calc
  const double getVertexFitting(const PATFinalState& fs, int combi, const edm::EventSetup& iSetup) const;

  // Tag of final state collection
  edm::EDGetTokenT<edm::View<PATFinalState> > srcToken_;

};


MiniAODVertexFittingEmbedder::MiniAODVertexFittingEmbedder(const edm::ParameterSet& iConfig) :
  srcToken_(consumes<edm::View<PATFinalState> >(iConfig.exists("src") ?
       iConfig.getParameter<edm::InputTag>("src") :
       edm::InputTag("finalStatemmmm")))
{
  produces<PATFinalStateCollection>();
}


void MiniAODVertexFittingEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) 
{
  std::unique_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStatesIn;
  iEvent.getByToken(srcToken_, finalStatesIn);

  for (size_t iFS = 0; iFS < finalStatesIn->size(); ++iFS) 
    {
      PATFinalState* embedInto = finalStatesIn->ptrAt(iFS)->clone();

      const double cat12 = getVertexFitting(*embedInto,12,iSetup);
      const double cat23 = getVertexFitting(*embedInto,23,iSetup);
      const double cat34 = getVertexFitting(*embedInto,34,iSetup);
      const double cat13 = getVertexFitting(*embedInto,13,iSetup);
      const double cat14 = getVertexFitting(*embedInto,14,iSetup);
      const double cat24 = getVertexFitting(*embedInto,24,iSetup); 
      const double cat123 = getVertexFitting(*embedInto,123,iSetup);
      const double cat124 = getVertexFitting(*embedInto,124,iSetup);
      const double cat134 = getVertexFitting(*embedInto,134,iSetup);
      const double cat234 = getVertexFitting(*embedInto,234,iSetup);
      const double cat1234 = getVertexFitting(*embedInto,1234,iSetup);

      embedInto->addUserFloat("VertexFitting12", double(cat12));
      embedInto->addUserFloat("VertexFitting23", double(cat23));
      embedInto->addUserFloat("VertexFitting34", double(cat34));
      embedInto->addUserFloat("VertexFitting13", double(cat13));
      embedInto->addUserFloat("VertexFitting14", double(cat14));
      embedInto->addUserFloat("VertexFitting24", double(cat24));
      embedInto->addUserFloat("VertexFitting123", double(cat123));
      embedInto->addUserFloat("VertexFitting124", double(cat124));
      embedInto->addUserFloat("VertexFitting134", double(cat134));
      embedInto->addUserFloat("VertexFitting234", double(cat234));
      embedInto->addUserFloat("VertexFitting1234", double(cat1234));

      output->push_back(embedInto); // takes ownership
    }

  iEvent.put(std::move(output));
}


const double MiniAODVertexFittingEmbedder::getVertexFitting(const PATFinalState& fs, int combination, const edm::EventSetup& iSetup) const
{
  if(fs.numberOfDaughters() < 2)
    return -1;
  if (combination>100 && fs.numberOfDaughters() < 3)
    return -1;
  if (combination>1000 && fs.numberOfDaughters() < 4)
    return -1;

  double fv_tC = -1;
  double fv_dOF = -1;
  //double fv_nC = -1;
  double fv_Prob = -1;

  if (combination==12 && fs.numberOfDaughters() >= 2 && abs(fs.daughter(0)->pdgId()) == 13 && abs(fs.daughter(1)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
     if (fs.daughterAsMuon(0)->innerTrack().isNonnull() and fs.daughterAsMuon(1)->innerTrack().isNonnull()){
        reco::TrackRef trk1 = fs.daughterAsMuon(0)->innerTrack();
        reco::TrackRef trk2 = fs.daughterAsMuon(1)->innerTrack();
        t_trks.push_back(theB->build(trk1));
        t_trks.push_back(theB->build(trk2));
        KalmanVertexFitter kvf;
        TransientVertex fv = kvf.vertex(t_trks);
        if(fv.isValid()){
          fv_tC = fv.totalChiSquared();
          fv_dOF = fv.degreesOfFreedom();
          fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
        }
     }
  }
  else if (combination==12 && fs.numberOfDaughters() >= 2 && abs(fs.daughter(0)->pdgId()) == 11 && abs(fs.daughter(1)->pdgId()) == 11){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
     if (fs.daughterAsElectron(0)->closestCtfTrackRef().isNonnull() and fs.daughterAsElectron(1)->closestCtfTrackRef().isNonnull()){
        reco::TrackRef trk1 = fs.daughterAsElectron(0)->closestCtfTrackRef();
        reco::TrackRef trk2 = fs.daughterAsElectron(1)->closestCtfTrackRef();
        t_trks.push_back(theB->build(trk1));
        t_trks.push_back(theB->build(trk2));
        KalmanVertexFitter kvf;
        TransientVertex fv = kvf.vertex(t_trks);
        if(fv.isValid()){
          fv_tC = fv.totalChiSquared();
          fv_dOF = fv.degreesOfFreedom();
          fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
        }
     }
  }

  else if (combination==13 && fs.numberOfDaughters() >= 3 && abs(fs.daughter(0)->pdgId()) == 13 && abs(fs.daughter(2)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(0)->innerTrack().isNonnull() and fs.daughterAsMuon(2)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(0)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(2)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       //fv_nC = fv_tC/fv_dOF;
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==23 && fs.numberOfDaughters() >= 3 && abs(fs.daughter(1)->pdgId()) == 13 && abs(fs.daughter(2)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(1)->innerTrack().isNonnull() and fs.daughterAsMuon(2)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(1)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(2)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       //fv_nC = fv_tC/fv_dOF;
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==14 && fs.numberOfDaughters() >= 4 && abs(fs.daughter(0)->pdgId()) == 13 && abs(fs.daughter(3)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(0)->innerTrack().isNonnull() and fs.daughterAsMuon(3)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(0)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(3)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       //fv_nC = fv_tC/fv_dOF;
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==24 && fs.numberOfDaughters() >= 4 && abs(fs.daughter(1)->pdgId()) == 13 && abs(fs.daughter(3)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(1)->innerTrack().isNonnull() and fs.daughterAsMuon(3)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(1)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(3)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       //fv_nC = fv_tC/fv_dOF;
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==34 && fs.numberOfDaughters() >= 4 && abs(fs.daughter(2)->pdgId()) == 13 && abs(fs.daughter(3)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(2)->innerTrack().isNonnull() and fs.daughterAsMuon(3)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(2)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(3)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       //fv_nC = fv_tC/fv_dOF;
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==123 && fs.numberOfDaughters() >= 3 && abs(fs.daughter(0)->pdgId()) == 13 && abs(fs.daughter(1)->pdgId()) == 13 && abs(fs.daughter(2)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(0)->innerTrack().isNonnull() and fs.daughterAsMuon(1)->innerTrack().isNonnull() and fs.daughterAsMuon(2)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(0)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(1)->innerTrack();
     reco::TrackRef trk3 = fs.daughterAsMuon(2)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     t_trks.push_back(theB->build(trk3));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       //fv_nC = fv_tC/fv_dOF;
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==234 && fs.numberOfDaughters() >= 4 && abs(fs.daughter(1)->pdgId()) == 13 && abs(fs.daughter(2)->pdgId()) == 13 && abs(fs.daughter(3)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(1)->innerTrack().isNonnull() and fs.daughterAsMuon(2)->innerTrack().isNonnull() and fs.daughterAsMuon(3)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(1)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(2)->innerTrack();
     reco::TrackRef trk3 = fs.daughterAsMuon(3)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     t_trks.push_back(theB->build(trk3));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       //fv_nC = fv_tC/fv_dOF;
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==124 && fs.numberOfDaughters() >= 4 && abs(fs.daughter(0)->pdgId()) == 13 && abs(fs.daughter(1)->pdgId()) == 13 && abs(fs.daughter(3)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(0)->innerTrack().isNonnull() and fs.daughterAsMuon(1)->innerTrack().isNonnull() and fs.daughterAsMuon(3)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(0)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(1)->innerTrack();
     reco::TrackRef trk3 = fs.daughterAsMuon(3)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     t_trks.push_back(theB->build(trk3));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       //fv_nC = fv_tC/fv_dOF;
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==134 && fs.numberOfDaughters() >= 4 && abs(fs.daughter(0)->pdgId()) == 13 && abs(fs.daughter(2)->pdgId()) == 13 && abs(fs.daughter(3)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(0)->innerTrack().isNonnull() and fs.daughterAsMuon(2)->innerTrack().isNonnull() and fs.daughterAsMuon(3)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(0)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(2)->innerTrack();
     reco::TrackRef trk3 = fs.daughterAsMuon(3)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     t_trks.push_back(theB->build(trk3));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       //fv_nC = fv_tC/fv_dOF;
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==1234 && fs.numberOfDaughters() >= 4 && abs(fs.daughter(0)->pdgId()) == 13 && abs(fs.daughter(1)->pdgId()) == 13 && abs(fs.daughter(2)->pdgId()) == 13 && abs(fs.daughter(3)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(0)->innerTrack().isNonnull() and fs.daughterAsMuon(1)->innerTrack().isNonnull() and fs.daughterAsMuon(2)->innerTrack().isNonnull() and fs.daughterAsMuon(3)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(0)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(1)->innerTrack();
     reco::TrackRef trk3 = fs.daughterAsMuon(2)->innerTrack();
     reco::TrackRef trk4 = fs.daughterAsMuon(3)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     t_trks.push_back(theB->build(trk3));
     t_trks.push_back(theB->build(trk4));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

  else if (combination==1234 && fs.numberOfDaughters() >= 4 && abs(fs.daughter(0)->pdgId()) == 11 && abs(fs.daughter(1)->pdgId()) == 11 && abs(fs.daughter(2)->pdgId()) == 13 && abs(fs.daughter(3)->pdgId()) == 13){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsElectron(0)->closestCtfTrackRef().isNonnull() and fs.daughterAsElectron(1)->closestCtfTrackRef().isNonnull() and fs.daughterAsMuon(2)->innerTrack().isNonnull() and fs.daughterAsMuon(3)->innerTrack().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsElectron(0)->closestCtfTrackRef();
     reco::TrackRef trk2 = fs.daughterAsElectron(1)->closestCtfTrackRef();
     reco::TrackRef trk3 = fs.daughterAsMuon(2)->innerTrack();
     reco::TrackRef trk4 = fs.daughterAsMuon(3)->innerTrack();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     t_trks.push_back(theB->build(trk3));
     t_trks.push_back(theB->build(trk4));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }

    else if (combination==1234 && fs.numberOfDaughters() >= 4 && abs(fs.daughter(0)->pdgId()) == 13 && abs(fs.daughter(1)->pdgId()) == 13 && abs(fs.daughter(2)->pdgId()) == 11 && abs(fs.daughter(3)->pdgId()) == 11){
     std::vector<reco::TransientTrack> t_trks;
     edm::ESHandle<TransientTrackBuilder> theB;
     iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);
if (fs.daughterAsMuon(0)->innerTrack().isNonnull() and fs.daughterAsMuon(1)->innerTrack().isNonnull() and fs.daughterAsElectron(2)->closestCtfTrackRef().isNonnull() and fs.daughterAsElectron(3)->closestCtfTrackRef().isNonnull()){
     reco::TrackRef trk1 = fs.daughterAsMuon(0)->innerTrack();
     reco::TrackRef trk2 = fs.daughterAsMuon(1)->innerTrack();
     reco::TrackRef trk3 = fs.daughterAsElectron(2)->closestCtfTrackRef();
     reco::TrackRef trk4 = fs.daughterAsElectron(3)->closestCtfTrackRef();
     t_trks.push_back(theB->build(trk1));
     t_trks.push_back(theB->build(trk2));
     t_trks.push_back(theB->build(trk3));
     t_trks.push_back(theB->build(trk4));
     KalmanVertexFitter kvf;
     TransientVertex fv = kvf.vertex(t_trks);
     if(fv.isValid()){
       fv_tC = fv.totalChiSquared();
       fv_dOF = fv.degreesOfFreedom();
       fv_Prob = TMath::Prob(fv_tC,(int)fv_dOF);
     }
     }
  }



  return fv_Prob;

}

/*
// helper functions for use in getVertexFitting()
// each assumes that the earlier categories have already been checked
const bool MiniAODVertexFittingEmbedder::isVBFTagged(const PATFinalState& fs) const
{
  // at least 2 jets
  if(fs.evt()->jets().size() < 2)
    return false;

  // at most one B-tagged jet
  uint nBTags = 0;
  for(size_t j = 0; j < fs.evt()->jets().size(); ++j)
    {
      if(isHZZBTagged(fs.evt()->jets().at(j)))
        {
          nBTags++;
          if(nBTags > 1)
            return false;
        }
    }
  
  // Fisher discriminant > 0.5
  float D_jet = 0.18 * fabs(fs.evt()->jets().at(0).eta() - fs.evt()->jets().at(1).eta()) +
    0.000192 * fs.dijetMass(0,1);
  if(D_jet < 0.5)
    return false;

  // exactly 4 leptons
  if(fs.vetoMuons(0.05, tightLepCut_).size() != 0 || fs.vetoElectrons(0.05, tightLepCut_).size() != 0)
    return false;

  return true;
}

const bool MiniAODVertexFittingEmbedder::isVHHadronicTagged(const PATFinalState& fs) const
{
  // all possibilities require at least 2 jets
  if(fs.evt()->jets().size() < 2)
    return false;

  // exactly 2 b-tagged jets
  bool twoBs = fs.evt()->jets().size() == 2;
  for(size_t j = 0; j < 2 && twoBs; ++j)
    twoBs &= isHZZBTagged(fs.evt()->jets().at(j));
  
  // OR at least 2 jets with |eta|<2.4, pt>40, 60<m_jj<120; and 4lpT>4lmass
  bool vJets = false;
  if(!twoBs)
    {
      for(size_t ijet = 0; ijet < fs.evt()->jets().size()-1 && !vJets; ++ijet) // safe because of 2 jet requirement
        {
          pat::Jet j1 = fs.evt()->jets().at(ijet);
          if(fabs(j1.eta()) > 2.4 || j1.pt() < 40.)
            continue;

          for(size_t jjet = ijet+1; jjet < fs.evt()->jets().size() && !vJets; ++jjet)
            {
              pat::Jet j2 = fs.evt()->jets().at(jjet);
              if(fabs(j2.eta()) > 2.4 || j2.pt() < 40.)
                continue;

              float mjj = (j1.p4() + j2.p4()).M();
              vJets |= (mjj > 60. && mjj < 120);
            }
        }
    }
  vJets &= (fs.mass() < fs.pt());

  if(! (twoBs || vJets))
    return false;

  // and exactly 4 leptons
  if(fs.vetoMuons(0.05, tightLepCut_).size() != 0 || fs.vetoElectrons(0.05, tightLepCut_).size() != 0)
    return false;

  return true;
}

const bool MiniAODVertexFittingEmbedder::isVHLeptonicTagged(const PATFinalState& fs) const
{
  // no more than 2 jets
  if(fs.evt()->jets().size() > 2)
    return false;
  
  // no B-tagged jets
  for(size_t j = 0; j < fs.evt()->jets().size(); ++j)
    if(isHZZBTagged(fs.evt()->jets().at(j)))
      return false;

  // at least 5 leptons
  return (fs.vetoMuons(0.05, tightLepCut_).size() != 0 || fs.vetoElectrons(0.05, tightLepCut_).size() != 0);
}

const bool MiniAODVertexFittingEmbedder::isTTHTagged(const PATFinalState& fs) const
{
  // at least 3 jets, at least one of which is B tagged
  bool threeJ = (fs.evt()->jets().size() >= 3);
  bool oneB = false;
  if(threeJ)
    {
      for(size_t j = 0; j < fs.evt()->jets().size(); ++j)
	{
	  if(isHZZBTagged(fs.evt()->jets().at(j)))
	    {
	      oneB = true;
	      break;
	    }
	}
    }
  
  if(threeJ && oneB)
    return true;

  // OR at least 5 leptons
  return (fs.vetoMuons(0.05, tightLepCut_).size() != 0 || fs.vetoElectrons(0.05, tightLepCut_).size() != 0);
}

const bool MiniAODVertexFittingEmbedder::isHZZ1JetTagged(const PATFinalState& fs) const
{
  // at least 1 jet
  return bool(fs.evt()->jets().size());
}


bool MiniAODVertexFittingEmbedder::isHZZBTagged(const pat::Jet& j) const
{
  return (j.bDiscriminator(bDiscrimLabel_) > bDiscrimCut_);
}

*/

void MiniAODVertexFittingEmbedder::beginJob(){}
void MiniAODVertexFittingEmbedder::endJob(){}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODVertexFittingEmbedder);



