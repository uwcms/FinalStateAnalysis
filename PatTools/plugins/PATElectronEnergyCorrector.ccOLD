/**
 * @file PATElectronEnergyCorrector.cc
 * @author D. Austin Belknap
 */

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "Math/GenVector/VectorUtil.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

/**
 * @class PATElectronEnergyCorrector
 * @brief Produces a collection of Energy-Corrected PAT Electrons
 */
class PATElectronEnergyCorrector : public edm::EDProducer
{

    public:
        PATElectronEnergyCorrector(const edm::ParameterSet& pset);
        virtual ~PATElectronEnergyCorrector () {}
        void produce( edm::Event& evt, const edm::EventSetup& es );

    private:
        typedef reco::Candidate::LorentzVector FourVec;
        edm::InputTag _src;
        std::string _tag;
};



PATElectronEnergyCorrector::PATElectronEnergyCorrector( const edm::ParameterSet& pset)
{
    _src = pset.getParameter<edm::InputTag>("src");
    _tag = pset.getParameter<std::string>("corr_type");
    produces<pat::ElectronCollection>();
}



/**
 * Create a new collection of pat::Electrons with the energy-corrected p4 and
 * push the collection to the event.
 */
void PATElectronEnergyCorrector::produce( edm::Event& evt, const edm::EventSetup& es )
{
    std::auto_ptr<pat::ElectronCollection> out(new pat::ElectronCollection);

    edm::Handle<pat::ElectronCollection> electrons;
    evt.getByLabel( _src, electrons );   

    for ( size_t i = 0; i < electrons->size(); ++i )
    {
        pat::Electron original_electron = electrons->at(i);
        pat::Electron corrected_electron = original_electron;

        FourVec corr_p4 = *original_electron.userData<FourVec>( _tag );

        corrected_electron.setP4( corr_p4 );

        out->push_back( corrected_electron );
    }

    evt.put( out );
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronEnergyCorrector);
