/**
 * @class PATQuadStateBuilderHzzT
 * @file PATQuadStateBuilderHzzT.h
 *
 * @brief Builds ZZ candidates with FSR
 *
 * This template follows the HZZ4L algorithm for construction of ZZ
 * candidates that include final-state radiation (FSR).
 *
 * The first step is to parse the input lepton collections and form
 * a single collection of unique leptons.
 *
 * Next, map the photons to their closest leptons.
 *
 * Permute through the list of leptons choosing four.
 * Keep the best arrangement of leptons.
 *
 * Using the photon map, assign FSR photons to the Z candidates
 * (if any)
 *
 * Note that Z1 and Z2 are not necessarily in the proper order
 * upon output.
 *
 * @author D. Austin Belknap
 */
#include <vector>
#include <limits>
#include <algorithm>
#include <typeinfo>
#include <string>

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
#include "DataFormats/PatCandidates/interface/PFParticle.h"
#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "Math/GenVector/VectorUtil.h"

#include "TLorentzVector.h"
#include "ZZMatrixElement/MELA/interface/Mela.h"
#include "ZZMatrixElement/MEMCalculators/interface/MEMCalculators.h"
#include "FinalStateAnalysis/PatTools/interface/HZZ4LAngles.h"


const double ZMASS = 91.188;

// function prototypes
bool comparePt( reco::CandidatePtr A, reco::CandidatePtr B );


template<class FinalState>
class PATQuadFinalStateBuilderHzzT : public edm::EDProducer
{

    public:
        typedef std::vector<FinalState> FinalStateCollection;
        typedef reco::Candidate::LorentzVector FourVec;

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

        MEMs mMEM;

        edm::Ptr<pat::PFParticle> assignPhoton(
                reco::CandidatePtr leg1, reco::CandidatePtr leg2, 
                std::map<reco::CandidatePtr, std::vector<edm::Ptr<pat::PFParticle> > >& photonMap );
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

    mMEM = MEMs(8);
}



/**
 * Loop over the collections and generate ZZ candidates which are
 * pushed back into the event.
 */
template<class FinalState> void
PATQuadFinalStateBuilderHzzT<FinalState>::produce(
        edm::Event& evt, const edm::EventSetup& es)
{
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

    edm::Handle<edm::View<pat::PFParticle> > photons;
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

    // there must be at least 4 leptons in the event, otherwise ignore the event
    if ( lepton_set.size() < 4 )
    {
        evt.put( output );
        return;
    }

    // load the lepton set into a vector

    std::vector<reco::CandidatePtr> lepton_list (lepton_set.size());
    std::copy( lepton_set.begin(), lepton_set.end(), lepton_list.begin() );





    // -------------------------------------------------
    //
    // Assign photons to their closest lepton
    //
    // -------------------------------------------------

    std::map<reco::CandidatePtr, std::vector<edm::Ptr<pat::PFParticle> > > photonMap;
    for ( size_t i = 0; i < photons->size(); ++i )
    {
        edm::Ptr<pat::PFParticle> current_photon = photons->ptrAt(i);

        reco::CandidatePtr nearest_lepton;
        double nearest_dR =  std::numeric_limits<double>::infinity(); // set dR to infty

        for ( size_t j = 0; j < lepton_list.size(); ++j )
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

        // The PF isolation is computed using a cone of 0.3, a threshold of 0.2 GeV on charged
        // hadrons and 0.5 GeV on neutral hadrons and photons
        double isoChHad = current_photon->userFloat("fsrPhotonPFIsoChHad03pt02") + current_photon->userFloat("fsrPhotonPFIsoChHadPU03pt02");
        double isoNeHad = current_photon->userFloat("fsrPhotonPFIsoNHad03");
        double isoPhot  = current_photon->userFloat("fsrPhotonPFIsoPhoton03");

        double photonPfRelIso = ( isoChHad + isoNeHad + isoPhot )/current_photon->pt();

        bool photon_pass1 = nearest_dR < 0.07 && current_photon->pt() > 2;
        bool photon_pass2 = nearest_dR < 0.5 && current_photon->pt() > 4 && photonPfRelIso < 1.0;

        if ( photon_pass1 || photon_pass2 )
            photonMap[nearest_lepton].push_back( current_photon );
    }




    // -------------------------------------------------
    //
    // The core candidate-building algorithm begins here
    //
    // -------------------------------------------------
    
    // leptons must be sorted before permuting
    std::sort( lepton_list.begin(), lepton_list.end(), comparePt );
    
    double best_zmass = 0;
    double best_pt1   = 0;
    double best_pt2   = 0;

    reco::CandidatePtr leg1;
    reco::CandidatePtr leg2;
    reco::CandidatePtr leg3;
    reco::CandidatePtr leg4;

    bool found_event = false;

    do
    {
        reco::CandidatePtr lepton1 = lepton_list.at(0);
        reco::CandidatePtr lepton2 = lepton_list.at(1);
        reco::CandidatePtr lepton3 = lepton_list.at(2);
        reco::CandidatePtr lepton4 = lepton_list.at(3);

        bool OSSF_pass     = lepton1->pdgId() == -lepton2->pdgId() && lepton3->pdgId() == -lepton4->pdgId();
        bool pt_order_pass = lepton1->pt() > lepton2->pt() && lepton3->pt() > lepton4->pt();

        if ( !(OSSF_pass && pt_order_pass) )
            continue;

        FourVec z1 = lepton1->p4() + lepton2->p4();
        FourVec z2 = lepton3->p4() + lepton4->p4();

        // Z1 should be closer to nominal Z mass than Z2
        if ( fabs(z1.M() - ZMASS) > fabs(z2.M() - ZMASS) )
            continue;

        // is Z1 mass the closest to nominal of all tried, and is Z2 made of the highest pt leptons?
        // if yes, then keep 'em!
        if ( fabs(z1.M() - ZMASS) <= fabs(best_zmass - ZMASS) && lepton3->pt() >= best_pt1 && lepton4->pt() >= best_pt2 )
        {
            found_event = true;

            leg1 = lepton1;
            leg2 = lepton2;
            leg3 = lepton3;
            leg4 = lepton4;

            best_zmass = z1.M();
            best_pt1 = lepton3->pt();
            best_pt2 = lepton4->pt();
        }
    }
    while ( std::next_permutation(lepton_list.begin(), lepton_list.end(), comparePt) );

    // if no events pass the ZZ selection, toss the event
    if ( !found_event )
    {
        evt.put( output );
        return;
    }


    // -------------------------------------------------
    //
    // Assign FSR photons to Z candidates
    // Correct lepton iso if necessary
    //
    // -------------------------------------------------
    
    float lepIsoCone = 0.4;
    
    edm::Ptr<pat::PFParticle> photon1 = assignPhoton( leg1, leg2, photonMap );
    edm::Ptr<pat::PFParticle> photon2 = assignPhoton( leg3, leg4, photonMap );

    float leg1_fsrIsoCorr = 0.0;
    float leg2_fsrIsoCorr = 0.0;
    float leg3_fsrIsoCorr = 0.0;
    float leg4_fsrIsoCorr = 0.0;

    if ( !photon1.isNull() )
    {
        float dR1 = ROOT::Math::VectorUtil::DeltaR( leg1->p4(), photon1->p4() );
        float dR2 = ROOT::Math::VectorUtil::DeltaR( leg2->p4(), photon1->p4() );

        if ( dR1 < dR2 && dR1 < lepIsoCone )
            leg1_fsrIsoCorr = photon1->pt();
        else if ( dR2 < dR1 && dR2 < lepIsoCone )
            leg2_fsrIsoCorr = photon1->pt();
    }

    if ( !photon2.isNull() )
    {
        float dR3 = ROOT::Math::VectorUtil::DeltaR( leg3->p4(), photon2->p4() );
        float dR4 = ROOT::Math::VectorUtil::DeltaR( leg4->p4(), photon2->p4() );

        if ( dR3 < dR4 && dR3 < lepIsoCone )
            leg3_fsrIsoCorr = photon2->pt();
        else if ( dR4 < dR3 && dR4 < lepIsoCone )
            leg4_fsrIsoCorr = photon2->pt();
    }



    // -------------------------------------------------
    //
    // Create the output candidate object, apply cuts, and push to the event
    // Also, take care of the special case of 2e2mu
    //
    // -------------------------------------------------
    
    std::string final_state_type = typeid(FinalState).name();
    std::string eemm_type        = "18PATQuadFinalStateTIN3pat8ElectronES1_NS0_4MuonES2_E"; // 0_o

    edm::Ptr<typename FinalState::daughter1_type> leg1_out; 
    edm::Ptr<typename FinalState::daughter2_type> leg2_out; 
    edm::Ptr<typename FinalState::daughter3_type> leg3_out; 
    edm::Ptr<typename FinalState::daughter4_type> leg4_out;

    // for 2e2mu make sure that you have, in fact, 2e2mu (or 2mu2e)
    if ( final_state_type == eemm_type && abs(leg1->pdgId()) == abs(leg3->pdgId()) )
    {
        evt.put( output );
        return;
    }


    // make sure the legs are arranged to match the FinalState datatype
    // i.e. electrons go first for 2e2mu
    bool revOrder = false;
    if ( final_state_type == eemm_type && abs(leg1->pdgId()) == 13 && abs(leg3->pdgId()) == 11 )
    {
        leg1_out = edm::Ptr<typename FinalState::daughter1_type> ( leg3 ); 
        leg2_out = edm::Ptr<typename FinalState::daughter2_type> ( leg4 ); 
        leg3_out = edm::Ptr<typename FinalState::daughter3_type> ( leg1 ); 
        leg4_out = edm::Ptr<typename FinalState::daughter4_type> ( leg2 );
        revOrder = true;
    }
    else
    {
        leg1_out = edm::Ptr<typename FinalState::daughter1_type> ( leg1 ); 
        leg2_out = edm::Ptr<typename FinalState::daughter2_type> ( leg2 ); 
        leg3_out = edm::Ptr<typename FinalState::daughter3_type> ( leg3 ); 
        leg4_out = edm::Ptr<typename FinalState::daughter4_type> ( leg4 ); 
    }

    // Load the legs into the output candidate and push to the event
    FinalState outputCand( leg1_out, leg2_out, leg3_out, leg4_out, evtPtr );

    // attach FSR photons to quad candidate
    if ( photon1.isNonnull() )
        outputCand.addUserCand("fsrPhoton01", photon1);
    if ( photon2.isNonnull() )
        outputCand.addUserCand("fsrPhoton23", photon2);
    
    // attach FSR isolation corrections
    outputCand.addUserFloat("leg0fsrIsoCorr", leg1_fsrIsoCorr);
    outputCand.addUserFloat("leg1fsrIsoCorr", leg2_fsrIsoCorr);
    outputCand.addUserFloat("leg2fsrIsoCorr", leg3_fsrIsoCorr);
    outputCand.addUserFloat("leg3fsrIsoCorr", leg4_fsrIsoCorr);


    // ------------------------------------------------
    // Grab gen-level leptons
    // Correct lepton ordering for 2e2mu if necessary
    // ------------------------------------------------
    const reco::GenParticle *leg1_gen;
    const reco::GenParticle *leg2_gen;
    const reco::GenParticle *leg3_gen;
    const reco::GenParticle *leg4_gen;

    if (revOrder)
    {
        leg1_gen = leg3_out->genLepton();
        leg2_gen = leg4_out->genLepton();
        leg3_gen = leg1_out->genLepton();
        leg4_gen = leg2_out->genLepton();
    }
    else
    {
        leg1_gen = leg1_out->genLepton();
        leg2_gen = leg2_out->genLepton();
        leg3_gen = leg3_out->genLepton();
        leg4_gen = leg4_out->genLepton();
    }



    // ----------------------
    // Add KDs and Angles
    // ----------------------
    std::vector<TLorentzVector> partP(4);
    std::vector<int> partId(4);

    partP.at(0) = TLorentzVector(leg1->px(), leg1->py(), leg1->pz(), leg1->p4().E());
    partP.at(1) = TLorentzVector(leg2->px(), leg2->py(), leg2->pz(), leg2->p4().E());
    partP.at(2) = TLorentzVector(leg3->px(), leg3->py(), leg3->pz(), leg3->p4().E());
    partP.at(3) = TLorentzVector(leg4->px(), leg4->py(), leg4->pz(), leg4->p4().E());

    partId.at(0) = leg1->pdgId();
    partId.at(1) = leg2->pdgId();
    partId.at(2) = leg3->pdgId();
    partId.at(3) = leg4->pdgId();

    mMEM.computeMEs( partP, partId );

    // Compute KD
    double KD         = -1;
    double ME_ggHiggs = -1;
    double ME_qqZZ    = -1;
    mMEM.computeKD(MEMNames::kSMHiggs, MEMNames::kJHUGen, MEMNames::kqqZZ, MEMNames::kMCFM, &MEMs::probRatio, KD, ME_ggHiggs, ME_qqZZ);

    // Compute X -> 4l kinematic angles (Uses Matt Snowball's code)
    // http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/UFL/PAT/Analysis_5X/HZZAnalysis/UFHZZ4LAna/interface/HZZ4LAngles.h
    double costhetastar  = -99;
    double costheta1     = -99;
    double costheta2     = -99;
    double Phi           = -99;
    double Phi1          = -99;
    HZZ4LAngles angles;
    angles.computeAngles(
            partP.at(0) + partP.at(1) + partP.at(2) + partP.at(3),  // H.p4
            partP.at(0) + partP.at(1),                              // Z1.p4
            partP.at(0),                                            // l1.p4
            partP.at(1),                                            // l2.p4
            partP.at(2) + partP.at(3),                              // Z2.p4
			partP.at(2),                                            // l3.p4
            partP.at(3),                                            // l4.p4
            costheta1, costheta2, Phi, costhetastar, Phi1);
    
    outputCand.addUserFloat("KD", KD);
    outputCand.addUserFloat("costheta1", costheta1);
    outputCand.addUserFloat("costheta2", costheta2);
    outputCand.addUserFloat("costhetastar", costhetastar);
    outputCand.addUserFloat("Phi", Phi);
    outputCand.addUserFloat("Phi1", Phi1);


    // Add Gen angles
    double costhetastar_gen  = -99;
    double costheta1_gen     = -99;
    double costheta2_gen     = -99;
    double Phi_gen           = -99;
    double Phi1_gen          = -99;

    if ( leg1_gen != NULL && leg2_gen != NULL && leg3_gen != NULL && leg4_gen != NULL )
    {
        std::vector<TLorentzVector> partP_gen(4);

        partP_gen.at(0) = TLorentzVector(leg1_gen->px(), leg1_gen->py(), leg1_gen->pz(), leg1_gen->p4().E());
        partP_gen.at(1) = TLorentzVector(leg2_gen->px(), leg2_gen->py(), leg2_gen->pz(), leg2_gen->p4().E());
        partP_gen.at(2) = TLorentzVector(leg3_gen->px(), leg3_gen->py(), leg3_gen->pz(), leg3_gen->p4().E());
        partP_gen.at(3) = TLorentzVector(leg4_gen->px(), leg4_gen->py(), leg4_gen->pz(), leg4_gen->p4().E());

        HZZ4LAngles angles_gen;
        angles_gen.computeAngles(
                partP_gen.at(0) + partP_gen.at(1) + partP_gen.at(2) + partP_gen.at(3),  // H.p4
                partP_gen.at(0) + partP_gen.at(1),                                      // Z1.p4
                partP_gen.at(0),                                                        // l1.p4
                partP_gen.at(1),                                                        // l2.p4
                partP_gen.at(2) + partP_gen.at(3),                                      // Z2.p4
	    		partP_gen.at(2),                                                        // l3.p4
                partP_gen.at(3),                                                        // l4.p4
                costheta1_gen, costheta2_gen, Phi_gen, costhetastar_gen, Phi1_gen);
    }
    
    outputCand.addUserFloat("costheta1_gen", costheta1_gen);
    outputCand.addUserFloat("costheta2_gen", costheta2_gen);
    outputCand.addUserFloat("costhetastar_gen", costhetastar_gen);
    outputCand.addUserFloat("Phi_gen", Phi_gen);
    outputCand.addUserFloat("Phi1_gen", Phi1_gen);
    

    // -------------------------
    // Output candidate to event
    // -------------------------
    if ( cut_(outputCand) )
        output->push_back( outputCand );

    evt.put( output );
}



/**
 * This function takes the two legs of a Z candidate and the photon mapping and assigns
 * either one or zero FSR photons to the Z candidate. A photon is accepted only if brings
 * the Z mass closer to nominal, and 4 < M_llg < 100. If more than one photons pass, pick
 * the one with the highest pT greater than 4 GeV. Otherwise, choose the one with the
 * smallest dR to the leptons.
 *
 * @param leg1,leg2 Legs of the Z-candidate
 * @param photonMap The mapping of leptons to their closest photons
 *
 * @return A single photon candidate or NULL if there isn't one
 */
template<class FinalState> 
edm::Ptr<pat::PFParticle> PATQuadFinalStateBuilderHzzT<FinalState>::assignPhoton(
        reco::CandidatePtr leg1, reco::CandidatePtr leg2, 
        std::map<reco::CandidatePtr, std::vector<edm::Ptr<pat::PFParticle> > >& photonMap )
{
    std::vector<edm::Ptr<pat::PFParticle> > photons;

    for ( size_t i = 0; i < photonMap[leg1].size(); ++i )
    {
        edm::Ptr<pat::PFParticle> photon = photonMap[leg1].at(i);

        FourVec Z     = leg1->p4() + leg2->p4();
        FourVec Z_fsr = Z + photon->p4();

        bool cut1 = 4 < Z_fsr.M() && Z_fsr.M() < 100;
        bool cut2 = fabs(Z_fsr.M() - ZMASS) < fabs(Z.M() - ZMASS);

        if ( cut1 && cut2 )
            photons.push_back( photon );
    }

    for ( size_t i = 0; i < photonMap[leg2].size(); ++i )
    {
        edm::Ptr<pat::PFParticle> photon = photonMap[leg2].at(i);

        FourVec Z     = leg1->p4() + leg2->p4();
        FourVec Z_fsr = Z + photon->p4();

        bool cut1 = 4 < Z_fsr.M() && Z_fsr.M() < 100;
        bool cut2 = fabs(Z_fsr.M() - ZMASS) < fabs(Z.M() - ZMASS);

        if ( cut1 && cut2 )
            photons.push_back( photon );
    }

    // return if one or zero photons are found
    if ( photons.size() == 0 )
    {
        edm::Ptr<pat::PFParticle> out;
        return out;
    }
    else if ( photons.size() == 1 )
        return photons.at(0);

    // pick highest pt photon if above 4 GeV
    bool found = false;
    edm::Ptr<pat::PFParticle> highest_photon;
    double highest_pt = 0;

    for ( size_t i = 0; i < photons.size(); ++i )
    {
        if ( photons.at(i)->pt() > 4 && photons.at(i)->pt() > highest_pt )
        {
            highest_photon = photons.at(i);
            highest_pt     = photons.at(i)->pt();
            found = true;
        }
    }

    if (found)
        return highest_photon;

    // if no photons above 4 GeV, select smallest dR
    edm::Ptr<pat::PFParticle> closest_photon;
    double closest_dR = std::numeric_limits<double>::infinity();

    for ( size_t i = 0; i < photons.size(); ++i )
    {
        edm::Ptr<pat::PFParticle> current_photon = photons.at(i);

        double dR1 = ROOT::Math::VectorUtil::DeltaR( leg1->p4(), current_photon->p4() );
        double dR2 = ROOT::Math::VectorUtil::DeltaR( leg2->p4(), current_photon->p4() );

        if ( dR1 < closest_dR )
        {
            closest_dR = dR1;
            closest_photon = current_photon;
        }
        if ( dR2 < closest_dR )
        {
            closest_dR = dR2;
            closest_photon = current_photon;
        }
    }

    return closest_photon;
}



/**
 * Compares leptons based on their pt.
 * Ensures ordering from greatest to least during sorting.
 *
 * @param A,B Lepton candidates
 * @return True iff A.pt is greater than B.pt
 */
bool comparePt( reco::CandidatePtr A, reco::CandidatePtr B )
{
    return A->pt() > B->pt();
}
