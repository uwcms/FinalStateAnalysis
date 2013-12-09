/**
 * @file PATMuonRochesterCorrector.cc
 * @author D. Austin Belknap
 */

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "Math/GenVector/VectorUtil.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

/**
 * @class PATMuonRochesterCorrector
 * @brief Produces a collection of Rochester-Corrected PAT Muons
 */
class PATMuonRochesterCorrector : public edm::EDProducer
{

    public:
        PATMuonRochesterCorrector(const edm::ParameterSet& pset);
        virtual ~PATMuonRochesterCorrector () {}
        void produce( edm::Event& evt, const edm::EventSetup& es );

    private:
        typedef reco::Candidate::LorentzVector FourVec;
        edm::InputTag _src;
        std::string _tag;
};



PATMuonRochesterCorrector::PATMuonRochesterCorrector( const edm::ParameterSet& pset)
{
    _src = pset.getParameter<edm::InputTag>("src");
    _tag = pset.getParameter<std::string>("corr_type");
    produces<pat::MuonCollection>();
}



/**
 * Create a new collection of pat::Muons with the Rochester-corrected p4 and
 * push the collection to the event.
 */
void PATMuonRochesterCorrector::produce( edm::Event& evt, const edm::EventSetup& es )
{
    std::auto_ptr<pat::MuonCollection> out(new pat::MuonCollection);

    edm::Handle<pat::MuonCollection> muons;
    evt.getByLabel( _src, muons );   

    for ( size_t i = 0; i < muons->size(); ++i )
    {
        pat::Muon original_muon = muons->at(i);
        pat::Muon corrected_muon = original_muon;

        FourVec corr_p4 = *original_muon.userData<FourVec>( _tag );

        corrected_muon.setP4( corr_p4 );

        out->push_back( corrected_muon );
    }

    evt.put( out );
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonRochesterCorrector);
