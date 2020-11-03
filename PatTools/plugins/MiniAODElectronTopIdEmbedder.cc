/*
 * Embeds the MVA top ID
 * Author: Cecile Caillol, UW-Madison
 */

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
#include "FinalStateAnalysis/PatTools/interface/LeptonMvaHelper.h"

#include <math.h>

// class declaration
class MiniAODElectronTopIdEmbedder : public edm::EDProducer {
  public:
    explicit MiniAODElectronTopIdEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODElectronTopIdEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);

  private:
    edm::EDGetTokenT<pat::ElectronCollection> electronsCollection_;
    edm::EDGetTokenT<pat::JetCollection> jetsCollection_;
    edm::EDGetTokenT<reco::VertexCollection> vtxCollection_;
    edm::EDGetTokenT<double> rhoCollection_;
    //edm::EDGetTokenT<bool> is2016Token_;
    bool is_2016;

    EffectiveAreas electronsEffectiveAreas;
    EffectiveAreas electronsEffectiveAreas_Summer16; // lepton MVA's are using old effective areas
    EffectiveAreas electronsEffectiveAreas_Spring15; 
    LeptonMvaHelper* leptonMvaComputerTOP;

    template< typename T1, typename T2 > bool isSourceCandidatePtrMatch( const T1& lhs, const T2& rhs );
    const pat::Jet* findMatchedJet( const pat::Electron& lepton, const edm::Handle< std::vector< pat::Jet > >& jets, const bool oldMatching );
    double getRelIso03(const pat::Electron& ele, const double rho, const EffectiveAreas& effectiveAreas) const;
    double getRelIso04(const pat::Electron& ele, const double rho, const EffectiveAreas& effectiveAreas) const;
    template< typename T > double getMiniIsolation( const T& lepton, const double rho, const EffectiveAreas& effectiveAreas, const bool onlyCharged ) const;
};

// class member functions
MiniAODElectronTopIdEmbedder::MiniAODElectronTopIdEmbedder(const edm::ParameterSet& pset)
   : electronsEffectiveAreas(pset.getParameter<edm::FileInPath>("electronsEffAreas").fullPath()),
  electronsEffectiveAreas_Summer16(pset.getParameter<edm::FileInPath>("electronsEffAreas_Summer16").fullPath()),
  electronsEffectiveAreas_Spring15(pset.getParameter<edm::FileInPath>("electronsEffAreas_Spring15").fullPath())
{
  electronsCollection_ = consumes<pat::ElectronCollection>(pset.getParameter<edm::InputTag>("src"));
  jetsCollection_ = consumes<pat::JetCollection>(pset.getParameter<edm::InputTag>("jetSrc"));
  vtxCollection_ = consumes<reco::VertexCollection>(pset.getParameter<edm::InputTag>("vtxSrc"));
  rhoCollection_=consumes<double>(pset.getParameter<edm::InputTag>("srcRho"));
  //is2016Token_=consumes<bool>(pset.getParameter<bool>("is2016"));
  is_2016 = pset.getParameter<bool> ("is2016");
  leptonMvaComputerTOP = new LeptonMvaHelper(pset, "TOP", 2018);
  produces<pat::ElectronCollection>();
}

void MiniAODElectronTopIdEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<std::vector<pat::Electron>> electronsCollection;
  evt.getByToken(electronsCollection_ , electronsCollection);

  double rho=0.0;
  edm::Handle<double> rhoCollection;
  if (evt.getByToken(rhoCollection_,rhoCollection))
     rho = *rhoCollection;

  edm::Handle<std::vector<pat::Jet>> jetsCollection;
  evt.getByToken(jetsCollection_ , jetsCollection);

  edm::Handle<std::vector<reco::Vertex>> vtxCollection;
  evt.getByToken(vtxCollection_ , vtxCollection);
  const reco::Vertex& vertex = *vtxCollection->begin();

  const std::vector<pat::Electron> * electrons = electronsCollection.product();

  unsigned int nbElectron =  electrons->size();

  std::unique_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  output->reserve(nbElectron);

  for(unsigned i = 0 ; i < nbElectron; i++){
    pat::Electron electron(electrons->at(i));

    double _lPt=1.0;
    _lPt=electron.pt();
    double _lEta=1.0;
    _lEta=electron.eta();

    double _3dIPSig=1.0;
    _3dIPSig=abs(electron.dB(pat::Electron::PV3D)/electron.edB(pat::Electron::PV3D));
    double _dxy=1.0;
    _dxy=electron.dB(pat::Electron::PV2D);
    double _dz=1.0;
    _dz=electron.dB(pat::Electron::PVDZ);

    double _relIso=1.0;
    _relIso = getRelIso03(electron, rho, electronsEffectiveAreas);
    double _relIso0p4 =1.0;
    _relIso0p4 = getRelIso04(electron, rho, electronsEffectiveAreas);
    double _relIso_Summer16 = 1.0;
    _relIso_Summer16 = getRelIso03(electron, rho, electronsEffectiveAreas_Summer16);
    double _relIso0p4_Summer16 = 1.0;
    _relIso0p4_Summer16 = getRelIso04(electron, rho, electronsEffectiveAreas_Summer16);

    double _miniIso = 1.0;
    _miniIso = getMiniIsolation(electron, rho, electronsEffectiveAreas, false);
    double _miniIsoCharged = 1.0;
    _miniIsoCharged = getMiniIsolation(electron, rho, electronsEffectiveAreas, true);
    double _miniIso_Spring15 = 1.0;
    _miniIso_Spring15 = getMiniIsolation(electron, rho, electronsEffectiveAreas_Spring15, false);

    double _lElectronMvaSummer16GP=1.0;
    _lElectronMvaSummer16GP = electron.userFloat("ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values");
    double _lElectronMvaFall17v1NoIso=1.0;
    _lElectronMvaFall17v1NoIso = electron.userFloat("ElectronMVAEstimatorRun2Fall17NoIsoV1Values");
    double _lElectronMvaFall17NoIso=1.0;
    _lElectronMvaFall17NoIso = electron.userFloat("ElectronMVAEstimatorRun2Fall17NoIsoV2Values");

    // depends on jets
    double _selectedTrackMult=1.0;
    double _ptRel=1.0;
    double _ptRatio=1.0;
    double _ptRatio_Summer16=1.0;
    double _closestJetDeepFlavor=1.0;
    double _closestJetDeepFlavor_b = 0;
    double _closestJetDeepFlavor_bb = 0;
    double _closestJetDeepFlavor_lepb = 0;
    double _closestJetDeepCsv_b = 0;
    double _closestJetDeepCsv_bb = 0;
    double _closestJetDeepCsv = 0;
    bool oldMatching=false;

    const pat::Jet* matchedJetPtr = findMatchedJet( electron, jetsCollection, oldMatching );
    if( matchedJetPtr == nullptr ){
        _ptRatio          = ( oldMatching ? 1. : 1. / (1. + _relIso0p4));
        _ptRatio_Summer16 = ( oldMatching ? 1. : 1. / (1. + _relIso0p4_Summer16));
        _ptRel = 0;
        _selectedTrackMult = 0;
        _closestJetDeepFlavor_b = 0;
        _closestJetDeepFlavor_bb= 0;
        _closestJetDeepFlavor_lepb = 0;
        _closestJetDeepFlavor = 0;
        _closestJetDeepCsv_b = 0;
        _closestJetDeepCsv_bb = 0;
        _closestJetDeepCsv = 0;
    } else {
        const pat::Jet& jet = *matchedJetPtr;

        auto rawJetP4 = jet.correctedP4("Uncorrected");
        auto leptonP4 = electron.p4();

        bool leptonEqualsJet = ( ( rawJetP4 - leptonP4 ).P() < 1e-4 );

        //if lepton and jet vector are equal set _ptRatio, _ptRel and track multipliticy to defaults 
        if( leptonEqualsJet && !oldMatching ){
            _ptRatio = 1;
            _ptRatio_Summer16 = 1;
            _ptRel = 0;
            _selectedTrackMult = 0;
        } else {

            //remove all corrections above L1 from the lepton
            auto L1JetP4 = jet.correctedP4("L1FastJet");
            double L2L3JEC = jet.pt()/L1JetP4.pt();
            auto lepAwareJetP4 = ( L1JetP4 - leptonP4 )*L2L3JEC + leptonP4;

            _ptRatio = electron.pt() / lepAwareJetP4.pt();
            _ptRatio_Summer16 = electron.pt() / lepAwareJetP4.pt();

            //lepton momentum orthogonal to the jet axis
            //magnitude of cross-product between lepton and rest of jet 
            _ptRel = leptonP4.Vect().Cross( (lepAwareJetP4 - leptonP4 ).Vect().Unit() ).R();

            _selectedTrackMult = 0;
            for( const auto daughterPtr : jet.daughterPtrVector() ){
                const pat::PackedCandidate& daughter = *( (const pat::PackedCandidate*) daughterPtr.get() );

                if( daughter.charge() == 0 ) continue;
                if( daughter.fromPV() < 2 ) continue;
                if( reco::deltaR( daughter, electron ) > 0.4 ) continue;
                if( !daughter.hasTrackDetails() ) continue;

                auto daughterTrack = daughter.pseudoTrack();
                if( daughterTrack.pt() <= 1 ) continue;
                if( daughterTrack.hitPattern().numberOfValidHits() < 8 ) continue;
                if( daughterTrack.hitPattern().numberOfValidPixelHits() < 2 ) continue;
                if( daughterTrack.normalizedChi2() >= 5 ) continue;
                if( std::abs( daughterTrack.dz( vertex.position() ) ) >= 17 ) continue;
                if( std::abs( daughterTrack.dxy( vertex.position() ) ) >= 0.2 ) continue;
                ++_selectedTrackMult;
            }

        }

        //DeepCSV of closest jet
        _closestJetDeepCsv_b  = jet.bDiscriminator("pfDeepCSVJetTags:probb");
        _closestJetDeepCsv_bb = jet.bDiscriminator("pfDeepCSVJetTags:probbb");
        _closestJetDeepCsv    = _closestJetDeepCsv_b + _closestJetDeepCsv_bb;
        if( std::isnan( _closestJetDeepCsv ) ) _closestJetDeepCsv = 0.;

        //DeepFlavor b-tag values of closest jet
        _closestJetDeepFlavor_b = jet.bDiscriminator("pfDeepFlavourJetTags:probb");
        _closestJetDeepFlavor_bb = jet.bDiscriminator("pfDeepFlavourJetTags:probbb");
        _closestJetDeepFlavor_lepb = jet.bDiscriminator("pfDeepFlavourJetTags:problepb");
        _closestJetDeepFlavor = _closestJetDeepFlavor_b + _closestJetDeepFlavor_bb + _closestJetDeepFlavor_lepb;
        if( std::isnan( _closestJetDeepFlavor ) ) _closestJetDeepFlavor = 0.;
    }



    double topid=1.0;
    topid=leptonMvaComputerTOP->leptonMvaElectron(_lPt,
            _lEta,
            _selectedTrackMult,
            _miniIsoCharged,
            (is_2016 ? _miniIso_Spring15 : _miniIso) - _miniIsoCharged,
            _ptRel,
            is_2016 ? _ptRatio_Summer16 : _ptRatio,
            _closestJetDeepCsv,
            _closestJetDeepFlavor,
            _3dIPSig,
            _dxy,
            _dz,
	    _relIso,
            //is_2016 ? _relIso_Summer16 : _relIso,
            _lElectronMvaSummer16GP,
            _lElectronMvaFall17v1NoIso,
            _lElectronMvaFall17NoIso
    );

    electron.addUserFloat("electronMVATopID",topid);

    output->push_back(electron);
  }

  evt.put(std::move(output));
}

template< typename T1, typename T2 > bool MiniAODElectronTopIdEmbedder::isSourceCandidatePtrMatch( const T1& lhs, const T2& rhs ){
    for( size_t lhsIndex = 0; lhsIndex < lhs.numberOfSourceCandidatePtrs(); ++lhsIndex ){
        auto lhsSourcePtr = lhs.sourceCandidatePtr( lhsIndex );
        for( size_t rhsIndex = 0; rhsIndex < rhs.numberOfSourceCandidatePtrs(); ++rhsIndex ){
            auto rhsSourcePtr = rhs.sourceCandidatePtr( rhsIndex );
            if( lhsSourcePtr == rhsSourcePtr ){
                return true;
            }
        }
    }
    return false;
}

const pat::Jet* MiniAODElectronTopIdEmbedder::findMatchedJet( const pat::Electron& lepton, const edm::Handle< std::vector< pat::Jet > >& jets, const bool oldMatching ){
    //Look for jet that matches with lepton
    const pat::Jet* matchedJetPtr = nullptr;

    //old matching scheme looks for closest jet in terms of delta R, and required this to be within delta R 0.4 of the lepton
    if( oldMatching ){
        for( auto& jet : *jets ){
            if( jet.pt() <= 5 || fabs( jet.eta() ) >= 3 ) continue;
            if( ( matchedJetPtr == nullptr) || reco::deltaR( jet, lepton ) < reco::deltaR( *matchedJetPtr, lepton ) ){
                matchedJetPtr = &jet;
            }
        }
        if( matchedJetPtr != nullptr && reco::deltaR( lepton, *matchedJetPtr ) > 0.4 ){
            matchedJetPtr = nullptr;
        }
    } else {
        for( auto& jet : *jets ){
            if( isSourceCandidatePtrMatch( lepton, jet ) ){
                //immediately returning guarantees that the leading jet matched to the lepton is returned
                return &jet;
            }
        }
    }
    return matchedJetPtr;
}

double MiniAODElectronTopIdEmbedder::getRelIso03(const pat::Electron& ele, const double rho, const EffectiveAreas& effectiveAreas) const{
    double puCorr = rho*effectiveAreas.getEffectiveArea( ele.superCluster()->eta() );
    double absIso = ele.pfIsolationVariables().sumChargedHadronPt + std::max(0., ele.pfIsolationVariables().sumNeutralHadronEt + ele.pfIsolationVariables().sumPhotonEt - puCorr);
    return absIso/ele.pt();
}


double MiniAODElectronTopIdEmbedder::getRelIso04(const pat::Electron& ele, const double rho, const EffectiveAreas& effectiveAreas) const{

    //take into account that area is larger in 0.4 cone 
    double puCorr = rho*effectiveAreas.getEffectiveArea( ele.superCluster()->eta() ) * ( 16./9. );
    double absIso = ele.chargedHadronIso() + std::max( 0., ele.neutralHadronIso() + ele.photonIso() - puCorr );
    return absIso/ele.pt();
}

template< typename T > double MiniAODElectronTopIdEmbedder::getMiniIsolation( const T& lepton, const double rho, const EffectiveAreas& effectiveAreas, const bool onlyCharged ) const{
    auto iso = lepton.miniPFIsolation();
    double absIso;
    if( onlyCharged ){
        absIso = iso.chargedHadronIso();
    } else {
        double cone_size = 10.0 / std::min( std::max( lepton.pt(), 50. ), 200. );
        double effective_area = effectiveAreas.getEffectiveArea( lepton.eta() );
        effective_area *= ( cone_size*cone_size )/ ( 0.3*0.3 );
        double pu_corr = effective_area*rho;
        absIso = iso.chargedHadronIso() + std::max( iso.neutralHadronIso() + iso.photonIso() - pu_corr, 0. );
    }
    return ( absIso / lepton.pt() );
}



// define plugin
DEFINE_FWK_MODULE(MiniAODElectronTopIdEmbedder);
