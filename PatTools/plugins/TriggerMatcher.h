/*
 * Embed trigger match information into PAT objects
 *
 * Original author: M. Bachtis
 *
 */

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "Math/GenVector/VectorUtil.h"

#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerRefsCollections.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"

// class decleration
//
template <typename T>
class MyTriggerMatcher : public edm::EDProducer {
  public:
    explicit MyTriggerMatcher (const edm::ParameterSet& iConfig):
      src_(iConfig.getParameter<edm::InputTag>("src")),
      triggerEvent_(iConfig.getParameter<edm::InputTag>("trigEvent")),
      filters_(iConfig.getParameter<std::vector<edm::InputTag> >("filters")),
      pdgId_(iConfig.getParameter<int>("pdgId")) {
        produces<std::vector<T> >();
      }
    ~MyTriggerMatcher () { }

  private:
    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
      using namespace reco;
      using namespace trigger;

      typedef reco::Candidate::LorentzVector LV;

      //Read the shallow clones of a candidate and save the SECOND Clone
      std::unique_ptr<std::vector<T> > out(new std::vector<T> );
      edm::Handle<std::vector<T> > src;

      edm::Handle<TriggerEvent> trigEv;
      iEvent.getByLabel(triggerEvent_,trigEv);

      /*  	  for(unsigned int i=0;i<trigEv->sizeFilters();++i)  */
      /*  	    printf("%s\n",trigEv->filterTag(i).label().c_str());   */

      if(iEvent.getByLabel(src_,src))
        for(unsigned int i=0;i<src->size();++i) {
          T obj = src->at(i);

          //loop the filters
          for(unsigned int i=0;i<filters_.size();++i) {
            size_t INDEX =trigEv->filterIndex(filters_[i]);

            std::vector<LV> trigObjects = getFilterCollection(INDEX,pdgId_,*trigEv);
            bool match = false;

            for(unsigned int j=0;j<trigObjects.size();++j)
              if(deltaR(trigObjects.at(j),obj)<0.5) {
                match=true;
                break;
              }

            // only embed if there are trigger objects
            if (true || trigObjects.size()) {
              if(match)
                obj.addUserFloat(filters_[i].label(),1.0);
              else
                obj.addUserFloat(filters_[i].label(),0.0);
            }
          }

          out->push_back(obj);
        }

      iEvent.put(std::move(out));
    }

    virtual void endJob() { }

    std::vector<reco::Candidate::LorentzVector>
      getFilterCollection(size_t index,int id,const trigger::TriggerEvent& trigEv)
      {
        //Create output Collection
        std::vector<reco::Candidate::LorentzVector>  out;
        //get All the final trigger objects
        const trigger::TriggerObjectCollection& TOC(trigEv.getObjects());
        //filter index
        if(index!=trigEv.sizeFilters())

        {
          const trigger::Keys& KEYS = trigEv.filterKeys(index);
          for(size_t i = 0;i<KEYS.size();++i)
          {
            const trigger::TriggerObject& TO(TOC[KEYS[i]]);
            reco::Candidate::LorentzVector a(TO.px(),TO.py(),TO.pz(),sqrt(TO.px()*TO.px()+TO.py()*TO.py()+TO.pz()*TO.pz()));
            if(abs(TO.id()) == id)
              out.push_back(a);
          }
        }

        return out;
      }

    edm::InputTag src_;
    edm::InputTag triggerEvent_;
    std::vector<edm::InputTag> filters_;
    int pdgId_;
};
