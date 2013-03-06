/**
 * @class PATQuadStateBuilderHzzT
 * @file PATQuadStateBuilderHzzT.h
 *
 * @brief Builds ZZ candidates with FSR
 *
 * This template follows the HZZ4L algorithm for construction of ZZ
 * candidates that include final-state radiation (FSR).
 *
 * The first step is to parse the input lepton collectios and form
 * a single collection of unique leptons.
 *
 * Next, map the photons to their closest leptons.
 *
 * @author D. Austin Belknap
 */
#include <vector>
#include <algorithm>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATQuadFinalStateT.h"

template<class FinalState>
class PATQuadFinalStateBuilderHzzT : public edm::EDProducer
{
    public:
        typedef std::vector<FinalState> FinalStateCollection;

        PATQuadFinalStateBuilderT(const edm::ParameterSet& pset);
        virtual ~PATQuadFinalStateBuilderT(){}
        void produce(edm::Event& evt, const edm::EventSetup& es);

    private:
        edm::InputTag leg1Src_;
        edm::InputTag leg2Src_;
        edm::InputTag leg3Src_;
        edm::InputTag leg4Src_;
        edm::InputTag photonSrc_;
        edm::InputTag evtSrc_;
        StringCutObjectSelector<PATFinalState> cut_;
};



/**
 * Class constructor. Parse collections from the EDM framework.
 */
template<class FinalState>
PATQuadFinalStateBuilderT<FinalState>::PATQuadFinalStateBuilderT(
        const edm::ParameterSet& pset):
    cut_(pset.getParameter<std::string>("cut"), true)
{
    leg1Src_   = pset.getParameter<edm::InputTag>("leg1Src");
    leg2Src_   = pset.getParameter<edm::InputTag>("leg2Src");
    leg3Src_   = pset.getParameter<edm::InputTag>("leg3Src");
    leg4Src_   = pset.getParameter<edm::InputTag>("leg4Src");
    photonSrc_ = pset.getParameter<edm::InputTag>("photonSrc");
    evtSrc_    = pset.getParameter<edm::InputTag>("evtSrc");
    produces<FinalStateCollection>();
}



/**
 * Loop over the collections and generate ZZ candidates which are
 * pushed back into the event.
 */
template<class FinalState> void
PATQuadFinalStateBuilderT<FinalState>::produce(
        edm::Event& evt, const edm::EventSetup& es) {

    edm::Handle<edm::View<PATFinalStateEvent> > fsEvent;
    evt.getByLabel(evtSrc_, fsEvent);
    edm::Ptr<PATFinalStateEvent> evtPtr = fsEvent->ptrAt(0);
    assert(evtPtr.isNonnull());

    std::auto_ptr<FinalStateCollection> output(new FinalStateCollection);



    // Get the lepton and photon collections from framework

    edm::Handle<edm::View<typename FinalState::daughter1_type> > leg1s;
    evt.getByLabel( leg1Src_, leg1s );

    edm::Handle<edm::View<typename FinalState::daughter2_type> > leg2s;
    evt.getByLabel( leg2Src_, leg2s );

    edm::Handle<edm::View<typename FinalState::daughter3_type> > leg3s;
    evt.getByLabel( leg3Src_, leg3s );

    edm::Handle<edm::View<typename FinalState::daughter4_type> > leg4s;
    evt.getByLabel( leg4Src_, leg4s );

    edm::Handle<edm::View<typename FinalState::daugher4_type> > photons;
    evt.getByLabel( photonSrc_, photons );



    // Load leptons into a set to ensure no duplicates
    // ToDo: consolidate into a single function

    std::set<reco::CandidatePtr> lepton_set;

    for ( size_t iLeg1 = 0; iLeg1  < leg1s->size(); ++iLeg1 )
    {
        edm::Ptr<typename FinalState::daughter1_type> leg1 = leg1s->ptrAt(iLeg1);
        assert( leg1.isNonnull() );
        lepton_set.insert( reco::Candidate(leg1) );
    }
    for ( size_t iLeg2 = 0; iLeg2  < leg2s->size(); ++iLeg2 )
    {
        edm::Ptr<typename FinalState::daughter2_type> leg2 = leg2s->ptrAt(iLeg2);
        assert( leg2.isNonnull() );
        lepton_set.insert( reco::Candidate(leg2) );
    }
    for ( size_t iLeg3 = 0; iLeg3  < leg3s->size(); ++iLeg3 )
    {
        edm::Ptr<typename FinalState::daughter3_type> leg3 = leg3s->ptrAt(iLeg3);
        assert( leg3.isNonnull() );
        lepton_set.insert( reco::Candidate(leg3) );
    }
    for ( size_t iLeg4 = 0; iLeg4  < leg4s->size(); ++iLeg4 )
    {
        edm::Ptr<typename FinalState::daughter4_type> leg4 = leg4s->ptrAt(iLeg4);
        assert( leg4.isNonnull() );
        lepton_set.insert( reco::Candidate(leg4) );
    }

    // load the lepton set into a vector

    std::vector<reco::CandidatePtr> lepton_list;
    std::copy( lepton_set.begin(), lepton_set.end(), lepton_list.begin() );


    // Map the photons to their nearest lepton

    std::map<reco::CandidatePtr, std::vector<edm::Ptr<pat::Photon> > photonMap;
    for ( size_t i = 0; i < photons->size(); ++i )
    {
        reco::CandiatePtr nearestLepton = lepton_list.at(0);

        for ( size_t j = 1; j < lepton_list.size(); ++j )
        {
        }
    }



    // Create the output candidate object, apply cuts, and push to the event

    FinalState outputCand(leg1, leg2, leg3, leg4, evtPtr);

    if (cut_(outputCand))
        output->push_back(outputCand);

    evt.put(output);
}
