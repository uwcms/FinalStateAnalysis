//--------------------------------------------------------------------------------------------------
// $Id $
//
// ElectronIDMVA
//
// Helper Class for applying MVA electron ID selection
//
// Authors: S.Xie
//--------------------------------------------------------------------------------------------------

#ifndef FSANA_HIGGSANALYSIS_ElectronIDMVA_H
#define FSANA_HIGGSANALYSIS_ElectronIDMVA_H

#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"

class ElectronIDMVA {
  public:
    ElectronIDMVA();
    ~ElectronIDMVA();

    enum MVAType {
      kBaseline = 0,      // SigmaIEtaIEta, DEtaIn, DPhiIn, FBrem, SigmaIPhiIPhi, NBrem,
                          // OneOverEMinusOneOverP
      kNoIPInfo,          // kBaseline + EOverP, ESeedClusterOverPout, ESeedClusterOverPIn
      kWithIPInfo,        // kV2 + d0 , IP3d, IP3dSig
      kTrig2012          // Si's 2012 triggering electron ID MVA with special sauce 
    };

    void   Initialize(std::string methodName,
                      std::string Subdet0Pt10To20Weights ,
                      std::string Subdet1Pt10To20Weights ,
                      std::string Subdet2Pt10To20Weights,
                      std::string Subdet0Pt20ToInfWeights,
                      std::string Subdet1Pt20ToInfWeights,
                      std::string Subdet2Pt20ToInfWeights,
                      ElectronIDMVA::MVAType type );
    Bool_t IsInitialized() const { return fIsInitialized; }
    MVAType getMVAType() const {return fMVAType;}

    double MVAValue(const reco::GsfElectron *ele, const reco::Vertex vertex,
                    EcalClusterLazyTools myEcalCluster,
                    const TransientTrackBuilder *transientTrackBuilder);

    double MVAValue(const reco::GsfElectron *ele,
                    EcalClusterLazyTools myEcalCluster);

    // Build the lazy tools internally
    double MVAValue(
        const reco::GsfElectron *ele,
        const edm::Event& evt,
        const edm::EventSetup& es,
        const edm::InputTag& ebRecHits,
        const edm::InputTag& eeRecHits);

    double MVAValue(double ElePt , double EleSCEta,
                    double EleSigmaIEtaIEta,
                    double EleDEtaIn,
                    double EleDPhiIn,
                    double EleHoverE,
                    double EleD0,
                    double EleFBrem,
                    double EleEOverP,
                    double EleESeedClusterOverPout,
                    double EleSigmaIPhiIPhi,
                    double EleNBrem,
                    double EleOneOverEMinusOneOverP,
                    double EleESeedClusterOverPIn,
                    double EleIP3d,
                    double EleIP3dSig,
		    double EleKfChi2 = -999,
		    double EleKfHits = -999,
		    double EleGsfChi2 = -999,
		    double EleDEtaCalo = -999,
		    double EleEtaWidth = -999,
		    double ElePhiWidth = -999,
		    double EleOneMinusE1x5E5x5 = -999,
		    double EleR9 = -999,
		    double ElePreshowerOverRaw = -999,
		    double EleEClusterOverPout = -999 );



  protected:
    TMVA::Reader             *fTMVAReader[6];
    std::string               fMethodname;
    MVAType                   fMVAType;

    Bool_t                    fIsInitialized;

    Float_t                   fMVAVar_EleSigmaIEtaIEta;
    Float_t                   fMVAVar_EleDEtaIn;
    Float_t                   fMVAVar_EleDPhiIn;
    Float_t                   fMVAVar_EleHoverE;
    Float_t                   fMVAVar_EleD0;
    Float_t                   fMVAVar_EleFBrem;
    Float_t                   fMVAVar_EleEOverP;
    Float_t                   fMVAVar_EleESeedClusterOverPout;
    Float_t                   fMVAVar_EleSigmaIPhiIPhi;
    Float_t                   fMVAVar_EleNBrem;
    Float_t                   fMVAVar_EleOneOverEMinusOneOverP;
    Float_t                   fMVAVar_EleESeedClusterOverPIn;
    Float_t                   fMVAVar_EleIP3d;
    Float_t                   fMVAVar_EleIP3dSig;
    // new for 2012 triggering ID
    Float_t                   fMVAVar_EleKfChi2;
    Float_t                   fMVAVar_EleKfHits;
    Float_t                   fMVAVar_EleGsfChi2;
    Float_t                   fMVAVar_EleDEtaCalo;
    Float_t                   fMVAVar_EleEtaWidth;
    Float_t                   fMVAVar_ElePhiWidth;
    Float_t                   fMVAVar_EleOneMinusE1x5E5x5;
    Float_t                   fMVAVar_EleR9;
    Float_t                   fMVAVar_ElePreshowerOverRaw;
    Float_t                   fMVAVar_EleEta;
    Float_t                   fMVAVar_ElePt;
    Float_t                   fMVAVar_EleEClusterOverPout;
};

#endif
