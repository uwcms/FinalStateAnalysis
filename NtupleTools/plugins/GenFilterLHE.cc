#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "TH1D.h"
#include "TH2D.h"

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

class GenFilterLHE : public edm::EDFilter {

public:
  GenFilterLHE (const edm::ParameterSet &);
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  virtual void beginJob();
  virtual void endJob();
private:
  edm::EDGetTokenT<LHEEventProduct> LHEParticleToken_;
  int statusGen_;
  int statusGenMAX_;

   std::map<std::string,TH1D*> h1_;
   std::map<std::string,TH2D*> h2_;


  double nall;
  double nsel;
};

GenFilterLHE::GenFilterLHE( const ParameterSet & cfg ) :
      LHEParticleToken_(consumes<LHEEventProduct>(cfg.getUntrackedParameter<edm::InputTag> ("LHETag", edm::InputTag("source")))),
      statusGen_(cfg.getUntrackedParameter<int>("PartonMultiplicity", 5)),
      statusGenMAX_(cfg.getUntrackedParameter<int>("PartonMultiplicityMAX", 0))
{
}

void GenFilterLHE::beginJob() {
      nall=0;
      nsel=0;

     edm::Service<TFileService> fs;
      h1_["LHE_PARTONMULTIPLICITY"]                    =fs->make<TH1D>("LHE_PARTONMULTIPLICITY","hepeup().NUP",20,0.,20.);
      h2_["LHE_LEADINGPARTON_PT"]   =fs->make<TH2D>("LHE_LEADINGPARTON_PT","",20,0,20,100,0,100);

}

void GenFilterLHE::endJob() {
     cout<<"********************************************************************"<<endl;
     cout<<"GEN LEVEL FILTERING"<<endl<<endl;
     cout<<"Total Analyzed =   "<<nall<<endl;
     cout<<"LHE Selection  =   "<<nsel<<endl;
     cout<<"********************************************************************"<<endl;




}

bool GenFilterLHE::filter (Event & ev, const EventSetup &) {
nall++;

bool found=true;


  edm::Handle<LHEEventProduct> lheeventinfo;
  if(!ev.getByToken(LHEParticleToken_, lheeventinfo)){
            LogDebug("") << ">>> LHE info not found!!";
            return false;
  }

  h1_["LHE_PARTONMULTIPLICITY"]->Fill(lheeventinfo->hepeup().NUP);
        double ptPART=sqrt( lheeventinfo->hepeup().PUP.at(0)[0]*lheeventinfo->hepeup().PUP.at(0)[0] + lheeventinfo->hepeup().PUP.at(0)[1]*lheeventinfo->hepeup().PUP.at(0)[1] );
      h2_["LHE_LEADINGPARTON_PT"]  ->Fill(lheeventinfo->hepeup().NUP, ptPART);

	if(statusGenMAX_==0){
	  if(lheeventinfo->hepeup().NUP!=statusGen_) found=false;
	}
	else{
	  if(lheeventinfo->hepeup().NUP<statusGen_ || lheeventinfo->hepeup().NUP>=statusGenMAX_) found=false;
	}

if (found) nsel++;
return found;
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(GenFilterLHE);
