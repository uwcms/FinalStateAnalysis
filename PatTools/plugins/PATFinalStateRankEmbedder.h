/*
 * Pat objects originally are sorted by Pt 
 * FSA reorders them so that the highest Pt "fsa" object is the first in the collection
 * This combinatoric approach is good for searches, but not for SMP
 * Incorporating a "rankByPt" variable that gives the position of the object in the collection, by Pt
 * Could be refined, and some care has to be taken if cuts are applied to the collection before being handled in the ntuple
 *
 * Author: M.C., UW Madison
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include <vector>
#include <string>
#include "DataFormats/Candidate/interface/Candidate.h"

template<typename T>
class PATRankEmbedder : public edm::EDProducer {
  typedef std::vector<T> TCollection;
  public:
    virtual ~PATRankEmbedder(){}

    void produce(edm::Event& evt, const edm::EventSetup& es);

    inline bool ptComparator(const reco::Candidate* a , const reco::Candidate* b) {return a->pt() > b->pt(); }
 
    PATRankEmbedder(const edm::ParameterSet& pset) :
    src_ (consumes<edm::View<T> >(pset.getParameter<edm::InputTag>("src"))){
      produces< TCollection >();
    }

  private:
     edm::EDGetTokenT<edm::View<T> > src_;

};

template<typename T>
void PATRankEmbedder< T>::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::unique_ptr<TCollection >output(new TCollection);

  edm::Handle< edm::View<T> > candidates;
  evt.getByToken(src_, candidates);
  output->reserve(candidates->size());


  for (size_t i = 0; i < candidates->size(); i++) {
    T embedInto = *(candidates->ptrAt(i));
    embedInto.addUserFloat("rankByPt",float(i));
    output->push_back(embedInto); // takes ownership
  }
  evt.put(std::move(output));

}

