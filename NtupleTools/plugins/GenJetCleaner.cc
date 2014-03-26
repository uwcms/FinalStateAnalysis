#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <TH1D.h>
#include <TH2D.h>

class GenJetCleaner : public edm::EDProducer {

public:
  GenJetCleaner (const edm::ParameterSet &);
private:

  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void beginJob();
  virtual void endJob();

   std::map<std::string,TH1D*> h1_;
   std::map<std::string,TH2D*> h2_;

  edm::InputTag src_;
  double ptMin_, etaMax_;
};
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"

#include "Math/GenVector/VectorUtil.h"

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <map>
#include <memory>

using namespace edm;
using namespace std;
using namespace reco;


GenJetCleaner::GenJetCleaner( const ParameterSet & cfg ) :
      src_(cfg.getUntrackedParameter<edm::InputTag>("src", edm::InputTag("ak5GenJets"))),
      ptMin_(cfg.getUntrackedParameter<double>("ptMin",30)),
      etaMax_(cfg.getUntrackedParameter<double>("etaMax",5))	
  {
    produces<reco::GenJetCollection>();
  }

void GenJetCleaner::beginJob() {
     edm::Service<TFileService> fs;
      h1_["Jets"]                    =fs->make<TH1D>("Jets","",20,0.,20.);
      h1_["CleanJets"]                    =fs->make<TH1D>("CleanJets","",20,0.,20.);
      h2_["Jets_LHENUP"]   =fs->make<TH2D>("Jets_LHENUP","",20,0,20,10,0,10);

}

void GenJetCleaner::endJob() {
}

void GenJetCleaner::produce (Event & iEvent, const EventSetup &) {

     edm::Handle<LHEEventProduct> lheeventinfo;
     if(!iEvent.getByLabel("source", lheeventinfo)){
            std::cout<< ">>> LHE info not found!!"<<std::endl;
     }

     double NUP=lheeventinfo->hepeup().NUP;


      std::auto_ptr<reco::GenJetCollection > out(new reco::GenJetCollection);
      Handle<reco::GenJetCollection > cands;

      edm::Handle< vector<reco::GenParticle> >pGenPart;

      if(!iEvent.getByLabel("genParticles", pGenPart)) std::cout<<"Hey!!!"<<std::endl;
      if (!iEvent.getByLabel(src_,cands)) std::cout<<"Hey!!!"<<std::endl;

      double nJets=0, nJetsClean=0;
        for(unsigned int  i=0;i!=cands->size();++i){
          reco::GenJet jet = cands->at(i);
	  if(jet.pt()<ptMin_ || abs(jet.eta())>etaMax_) continue;
	  nJets++;
	  bool skip=false;
                for( size_t i = 0; i < pGenPart->size(); ++ i ) {
                const reco::GenParticle& genpart = (*pGenPart)[i];
                        if(genpart.status()!=3) continue;
			if(abs(genpart.pdgId())==11|| abs(genpart.pdgId())==15  || abs(genpart.pdgId())==13 ){
                                double deltaR=ROOT::Math::VectorUtil::DeltaR(jet.p4(),genpart.p4());
	//			cout<<deltaR<<"   "<<jet.phi()<<"   "<<genpart.phi()<<endl;
                                if (deltaR<0.5) skip=true;
                        }
		}
          if (skip==false) {out->push_back(jet); nJetsClean++;}
        }
//      if(nJets>0) std::cout<<nJets<<"  "<<nJetsClean<<std::endl;
      iEvent.put(out);

      h1_["Jets"]->Fill(nJets); h1_["CleanJets"]->Fill(nJetsClean);	
      h2_["Jets_LHENUP"]->Fill(nJetsClean,NUP);	
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(GenJetCleaner);
