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

#include "DataFormats/Math/interface/deltaR.h"
#include "Math/GenVector/VectorUtil.h"


// function prototype
bool comparePt( reco::CandidatePtr A, reco::CandidatePtr B );


template<class FinalState>
class PATQuadFinalStateBuilderHzzT : public edm::EDProducer
{
    public:
        typedef std::vector<FinalState> FinalStateCollection;

        PATQuadFinalStateBuilderHzzT(const edm::ParameterSet& pset);
        virtual ~PATQuadFinalStateBuilderHzzT(){}
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
PATQuadFinalStateBuilderHzzT<FinalState>::PATQuadFinalStateBuilderHzzT(
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
PATQuadFinalStateBuilderHzzT<FinalState>::produce(
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

    edm::Handle<edm::View<pat::Photon> > photons;
    evt.getByLabel( photonSrc_, photons );



    // Load leptons into a set to ensure no duplicates
    // To-Do: consolidate into a single function

    std::set<reco::CandidatePtr> lepton_set;

    for ( size_t iLeg1 = 0; iLeg1  < leg1s->size(); ++iLeg1 )
    {
        edm::Ptr<typename FinalState::daughter1_type> leg1 = leg1s->ptrAt(iLeg1);
        assert( leg1.isNonnull() );
        lepton_set.insert( reco::CandidatePtr(leg1) );
    }
    for ( size_t iLeg2 = 0; iLeg2  < leg2s->size(); ++iLeg2 )
    {
        edm::Ptr<typename FinalState::daughter2_type> leg2 = leg2s->ptrAt(iLeg2);
        assert( leg2.isNonnull() );
        lepton_set.insert( reco::CandidatePtr(leg2) );
    }
    for ( size_t iLeg3 = 0; iLeg3  < leg3s->size(); ++iLeg3 )
    {
        edm::Ptr<typename FinalState::daughter3_type> leg3 = leg3s->ptrAt(iLeg3);
        assert( leg3.isNonnull() );
        lepton_set.insert( reco::CandidatePtr(leg3) );
    }
    for ( size_t iLeg4 = 0; iLeg4  < leg4s->size(); ++iLeg4 )
    {
        edm::Ptr<typename FinalState::daughter4_type> leg4 = leg4s->ptrAt(iLeg4);
        assert( leg4.isNonnull() );
        lepton_set.insert( reco::CandidatePtr(leg4) );
    }

    // load the lepton set into a vector

    std::vector<reco::CandidatePtr> lepton_list;
    std::copy( lepton_set.begin(), lepton_set.end(), lepton_list.begin() );




    // -------------------------------------------------
    //
    // Assign photons to their closest lepton
    //
    // -------------------------------------------------

    std::map<reco::CandidatePtr, std::vector<edm::Ptr<pat::Photon> > > photonMap;
    for ( size_t i = 0; i < photons->size(); ++i )
    {
        edm::Ptr<pat::Photon> current_photon = photons->ptrAt(i);

        reco::CandidatePtr nearest_lepton = lepton_list.at(0);
        double nearest_dR = ROOT::Math::VectorUtil::DeltaR( nearest_lepton->p4(), current_photon->p4() );

        for ( size_t j = 1; j < lepton_list.size(); ++j )
        {
            reco::CandidatePtr current_lepton = lepton_list.at(j);
            double current_dR = ROOT::Math::VectorUtil::DeltaR( current_lepton->p4(), current_photon->p4() );

            // choose closest lepton
            if ( current_dR < nearest_dR )
            {
                nearest_dR = current_dR;
                nearest_lepton = current_lepton;
            }
        }


        // assign the photon to the lepton. One lepton may have more than one
        // photon attached to it.
        if ( photonMap.count( nearest_lepton ) == 0 )
        {
            std::vector<edm::Ptr<pat::Photon> > phot_vec;
            phot_vec.push_back( current_photon );
            photonMap[nearest_lepton] = phot_vec;
        }
        else if ( photonMap.count( nearest_lepton ) == 1 )
        {
            photonMap[nearest_lepton].push_back( current_photon );
        }
    }



    // -------------------------------------------------
    //
    // The core candidate building algorithm begins here
    //
    // -------------------------------------------------
    
    // leptons must be sorted before permuting
    std::sort( lepton_list.begin(), lepton_list.end(), comparePt );
    
    do
    {
        edm::Ptr<pat::Photon> photon1;
        edm::Ptr<pat::Photon> photon2;

        reco::CandidatePtr lepton1 = lepton_list.at(0);
        reco::CandidatePtr lepton2 = lepton_list.at(1);
        reco::CandidatePtr lepton3 = lepton_list.at(2);
        reco::CandidatePtr lepton4 = lepton_list.at(3);

        bool OSSF_pass     = lepton1->pdgId() == -lepton2->pdgId() && lepton3->pdgId() == -lepton4->pdgId();
        bool pt_order_pass = lepton1->pt() > lepton2->pt() && lepton3->pt() > lepton4->pt();
        
    }
    while ( std::next_permutation(lepton_list.begin(), lepton_list.end(), comparePt) );



    // Create the output candidate object, apply cuts, and push to the event

    /*
    FinalState outputCand( leg1, leg2, leg3, leg4, evtPtr );

    if ( cut_(outputCand) )
        output->push_back( outputCand );

    evt.put( output );
    */
}



/**
 * Compares leptons based on their pt.
 * Ensures ordering from greatest to least during sorting.
 *
 * @param A First lepton
 * @param B Second lepton
 * @return True iff A.pt is greater than B.pt
 */
bool comparePt( reco::CandidatePtr A, reco::CandidatePtr B )
{
    return A->pt() > B->pt();
}
