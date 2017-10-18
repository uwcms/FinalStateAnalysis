
//Ovserloads the lepton with the rho factor


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

// class decleration
//
template <typename T>
class PATRhoOverloader : public edm::EDProducer {

   public:
     explicit PATRhoOverloader (const edm::ParameterSet& iConfig):
       srcToken_(consumes<std::vector<T> >(iConfig.getParameter<edm::InputTag>("src"))),
       srcRhoToken_(consumes<double>(iConfig.getParameter<edm::InputTag>("srcRho")))
       {
         label_ = iConfig.exists("userLabel") ? iConfig.getParameter<std::string>("userLabel") : "rho";
	 produces<std::vector<T> >();
       }

      ~PATRhoOverloader ()
	{

	}

   private:


      virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
	{
	  //Read the shallow clones of a candidate and save the SECOND Clone
	  std::unique_ptr<std::vector<T> > out(new std::vector<T> );
	  edm::Handle<std::vector<T> > src;

	  float rho = 0.0;

	  edm::Handle<double> srcRho;
	  if(iEvent.getByToken(srcRhoToken_,srcRho))
	    rho = *srcRho;


	  if(iEvent.getByToken(srcToken_,src))
	    for(unsigned int i=0;i<src->size();++i) {
	      T obj = src->at(i);
	      obj.addUserFloat(label_, rho );
	      out->push_back(obj);
	    }

	  iEvent.put(std::move(out));
	}

      virtual void endJob() { }

      edm::EDGetTokenT<std::vector<T> > srcToken_;
      edm::EDGetTokenT<double> srcRhoToken_;
      std::string label_;

};
