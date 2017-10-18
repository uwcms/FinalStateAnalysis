// Basic (& silly) program to produce a small genlevel ntuple, and a bunch of gen level plots
// Useful for debugging
// FSA independent

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TTree.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Handle.h"

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include <map>
#include <memory>

using namespace edm;
using namespace std;
using namespace reco;

class BasicGenPlotter : public edm::EDFilter {

public:
  BasicGenPlotter (const edm::ParameterSet &);
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  virtual void beginJob();
  virtual void endJob();
private:
  edm::EDGetTokenT<vector<reco::GenParticle> > GenParticleToken_;
  double minPtThreshold_;

  // For Pythia8
  bool skipMPI_;
  bool skipInitialStateShowers_;
  bool skipFinalStateShowers_;
  bool skipBeamRemnant_;
  bool skipIntermediateHadronization_;
  bool skipDecayProcess_;

  TTree* tree;

  std::map<std::string,TH1D*> h1_;
  std::map<std::string,TH2D*> h2_;

  std::vector<Float_t>* pts_;
  std::vector<Float_t>* etas_;
  std::vector<Float_t>* phis_;
  std::vector<Float_t>* masses_;
  std::vector<Int_t>* statuses_;
  std::vector<Long_t>* pdgIds_;
  std::vector<Int_t>* motherStatuses_;
  std::vector<Long_t>* motherPdgIds_;
  std::vector<Int_t>* numberOfDaughters_;

  ULong_t event_;



  double nall;
  double nsel;
};

BasicGenPlotter::BasicGenPlotter( const ParameterSet & cfg ) :
      GenParticleToken_(consumes<vector<reco::GenParticle> >(cfg.getUntrackedParameter<edm::InputTag> ("GenTag", edm::InputTag("genParticles")))),
      minPtThreshold_(cfg.getUntrackedParameter<double> ("MinPtThreshold",1)),
      skipMPI_(cfg.getUntrackedParameter<bool> ("SkipMPI",false)),
      skipInitialStateShowers_(cfg.getUntrackedParameter<bool> ("SkipInitialStateShowers",false)),
      skipFinalStateShowers_(cfg.getUntrackedParameter<bool> ("SkipFinalStateShowers",false)),
      skipBeamRemnant_(cfg.getUntrackedParameter<bool> ("SkipBeamRemnant",false)),
      skipIntermediateHadronization_(cfg.getUntrackedParameter<bool> ("SkipIntermediateHadronization",false)),
      skipDecayProcess_(cfg.getUntrackedParameter<bool> ("SkipDecayProcess",false))
{
}

void BasicGenPlotter::beginJob() {
      nall=0;
      nsel=0;

      edm::Service<TFileService> fs;
      tree = fs->make<TTree>("Ntuple", "Ntuple");
      pts_ = new std::vector<Float_t>();
      etas_ = new std::vector<Float_t>();
      phis_ = new std::vector<Float_t>();
      masses_ = new std::vector<Float_t>();
      pdgIds_ = new std::vector<Long_t>();
      statuses_ = new std::vector<Int_t>();
      motherStatuses_ = new std::vector<Int_t>();
      motherPdgIds_ = new std::vector<Long_t>();
      numberOfDaughters_ = new std::vector<Int_t>();

      tree->Branch("pt", "std::vector<float>", &pts_);
      tree->Branch("eta", "std::vector<float>", &etas_);
      tree->Branch("phi", "std::vector<float>", &phis_);
      tree->Branch("mass", "std::vector<float>", &masses_);
      tree->Branch("status", "std::vector<int>", &statuses_);
      tree->Branch("pdgId", "std::vector<long>", &pdgIds_);
      tree->Branch("motherStatus", "std::vector<int>", &motherStatuses_);
      tree->Branch("motherPdgId", "std::vector<long>", &motherPdgIds_);
      tree->Branch("numberOfDaughters", "std::vector<int>", &numberOfDaughters_);

      tree->Branch("evt", &event_, "evt/l");

}

void BasicGenPlotter::endJob() {
     cout<<"********************************************************************"<<endl;
     cout<<"GEN LEVEL FILTERING"<<endl<<endl;
     cout<<"Total Analyzed =   "<<nall<<endl;
     cout<<"LHE Selection  =   "<<nsel<<endl;
     cout<<"********************************************************************"<<endl;




}

bool BasicGenPlotter::filter (Event & ev, const EventSetup &) {
  nall++;

  bool found=true;

  edm::Handle< vector<reco::GenParticle> >pGenPart;
  if(ev.getByToken(GenParticleToken_, pGenPart)){

  pts_->clear();
  etas_->clear();
  phis_->clear();
  masses_->clear();
  statuses_->clear();
  pdgIds_->clear();
  numberOfDaughters_->clear();
  motherStatuses_->clear();
  motherPdgIds_->clear();

  int keep[11] = {36,25,23,24,21,11,12,13,14,15,16};

  cout<<"Reading!"<<endl;
        cout<<"Number || PdgID  || Status || Daugthers  || Mothers "<<endl;
  for( size_t i = 0; i < pGenPart->size(); ++ i ) {
        const reco::GenParticle& genpart = (*pGenPart)[i];
        if(genpart.pt()<minPtThreshold_ && genpart.pt()!=0) continue;  // the "=!0" bit  comes from the A->ZH file, where for whatever reason the first A has 0 pt...
        if(skipMPI_ && genpart.status()>30 && genpart.status()<40) continue;
        if(skipInitialStateShowers_ && genpart.status()>40 && genpart.status()<50) continue;
        if(skipFinalStateShowers_ && genpart.status()>50 && genpart.status()<60) continue;
        if(skipBeamRemnant_ && genpart.status()>60 && genpart.status()<70) continue;
        if(skipIntermediateHadronization_ && genpart.status()>70 && genpart.status()<80) continue;
        if(skipDecayProcess_ && genpart.status()>80 && genpart.status()<90) continue;

        bool skip=true;
        for (int k=0; k<11; k++) { if (abs(genpart.pdgId())==keep[k]) skip=false;}
        if (!skip){
                cout <<"\t\t"<<i<<"   "<<genpart.pdgId()<<"   "<<genpart.status()<<"    "<<genpart.pt()<<"   "<<genpart.numberOfDaughters()<<"   "<<genpart.mass()<<endl;
                pts_->push_back(genpart.pt());
                etas_->push_back(genpart.eta());
                phis_->push_back(genpart.phi());
                masses_->push_back(genpart.mass());
                statuses_->push_back(genpart.status());
                pdgIds_->push_back(genpart.pdgId());
                numberOfDaughters_->push_back(genpart.numberOfDaughters());

                if(genpart.numberOfMothers()>0){
                        const reco::Candidate* higgsmother=genpart.mother(0);
                        cout <<"\t\t mother   "<<higgsmother->pdgId()<<"   "<<higgsmother->status()<<"    "<<higgsmother->pt()<<"    "<<higgsmother->numberOfDaughters()<<endl;
                        motherStatuses_->push_back(higgsmother->status());
                        motherPdgIds_->push_back(higgsmother->pdgId());
                }
                else {
                        motherStatuses_->push_back(0);
                        motherPdgIds_->push_back(0);
                }
                if(genpart.numberOfDaughters()>1 && abs(genpart.pdgId())== (36 || 25 || 23 || 24) ){
                               for (size_t j=0; j<genpart.numberOfDaughters(); j++){
                                      const reco::Candidate* higgsdaughter=genpart.daughter(j);
                                      cout <<"\t\t daughter"<<j<<"   "<<higgsdaughter->pdgId()<<"   "<<higgsdaughter->status()<<"    "<<higgsdaughter->pt()<<"    "<<higgsdaughter->numberOfDaughters()<<endl;
                              }
                 }
        }
  }
  }

  event_=nall;
  tree->Fill();


  if (found) nsel++;
return found;
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(BasicGenPlotter);
