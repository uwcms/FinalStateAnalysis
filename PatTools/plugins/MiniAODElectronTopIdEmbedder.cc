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

  /*edm::Handle<bool> is2016Handle;
  evt.getByToken(is2016Token_, is2016Handle);
  bool is_2016 = *is2016Handle;*/

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

    double _relIso_Summer16=1.0;
    double puCorr = rho*electronsEffectiveAreas_Summer16.getEffectiveArea(electron.superCluster()->eta());
    double absIso = electron.pfIsolationVariables().sumChargedHadronPt + std::max(0., electron.pfIsolationVariables().sumNeutralHadronEt + electron.pfIsolationVariables().sumPhotonEt - puCorr);
    _relIso_Summer16=absIso/electron.pt();

    double _relIso=1.0;
    puCorr = rho*electronsEffectiveAreas.getEffectiveArea(electron.superCluster()->eta());
    absIso = electron.pfIsolationVariables().sumChargedHadronPt + std::max(0., electron.pfIsolationVariables().sumNeutralHadronEt + electron.pfIsolationVariables().sumPhotonEt - puCorr);
    _relIso=absIso/electron.pt();

    double _relIso0p4 = 1.0;
    puCorr = rho*electronsEffectiveAreas.getEffectiveArea(electron.superCluster()->eta()) * ( 16./9. );
    absIso = electron.chargedHadronIso() + std::max( 0., electron.neutralHadronIso() + electron.photonIso() - puCorr );
    _relIso0p4 = absIso/electron.pt();

    double _relIso0p4_Summer16 = 1.0;
    puCorr = rho*electronsEffectiveAreas_Summer16.getEffectiveArea(electron.superCluster()->eta()) * ( 16./9. );
    absIso = electron.chargedHadronIso() + std::max( 0., electron.neutralHadronIso() + electron.photonIso() - puCorr );
    _relIso0p4_Summer16 = absIso/electron.pt();

    double _miniIso_Spring15=1.0;
    auto iso = electron.miniPFIsolation();
    double cone_size = 10.0 / std::min( std::max( electron.pt(), 50. ), 200. );
    double effective_area = electronsEffectiveAreas_Spring15.getEffectiveArea( electron.superCluster()->eta());
    effective_area *= ( cone_size*cone_size )/ ( 0.3*0.3 );
    double pu_corr = effective_area*rho;
    absIso = iso.chargedHadronIso() + std::max( iso.neutralHadronIso() + iso.photonIso() - pu_corr, 0. ); 
    _miniIso_Spring15= ( absIso / electron.pt() );

    double _miniIso=1.0;
    iso = electron.miniPFIsolation();
    effective_area = electronsEffectiveAreas.getEffectiveArea(electron.superCluster()->eta());
    effective_area *= ( cone_size*cone_size )/ ( 0.3*0.3 );
    pu_corr = effective_area*rho;
    absIso = iso.chargedHadronIso() + std::max( iso.neutralHadronIso() + iso.photonIso() - pu_corr, 0. );
    _miniIso= ( absIso / electron.pt() );

    double _miniIsoCharged=1.0;
    iso = electron.miniPFIsolation();
    absIso = iso.chargedHadronIso();
    _miniIsoCharged= ( absIso / electron.pt() );

    double _lElectronMvaSummer16GP=1.0;
    _lElectronMvaSummer16GP = electron.userFloat("ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values");
    double _lElectronMvaFall17v1NoIso=1.0;
    _lElectronMvaFall17v1NoIso = electron.userFloat("ElectronMVAEstimatorRun2Fall17NoIsoV1Values");
    double _lElectronMvaFall17NoIso=1.0;
    _lElectronMvaFall17NoIso = electron.userFloat("ElectronMVAEstimatorRun2Fall17NoIsoV2Values");

    // depends on jets
    int _selectedTrackMult=1.0;
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
            is_2016 ? _relIso_Summer16 : _relIso,
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


// define plugin
DEFINE_FWK_MODULE(MiniAODElectronTopIdEmbedder);
