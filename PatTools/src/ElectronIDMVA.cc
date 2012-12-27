// Check if PAT tuple production is enabled - we can skip otherwise.
#include "FinalStateAnalysis/PatTools/interface/PATProductionFlag.h"
#ifdef ENABLE_PAT_PROD

#include <TFile.h>
#include "../interface/ElectronIDMVA.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "RecoTauTag/RecoTau/interface/TMVAZipReader.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/IPTools/interface/IPTools.h"

// This is some nonsense so this will work out of the box w/ the 42X and 52X
// versions of TMVAZipReader.
namespace reco { namespace details { int dummy; }}


using namespace reco;
using namespace reco::details;

//--------------------------------------------------------------------------------------------------
ElectronIDMVA::ElectronIDMVA() :
fMethodname("BDTG method"),
fIsInitialized(kFALSE)
{
  // Constructor.
  for(UInt_t i=0; i<6; ++i) {
    fTMVAReader[i] = 0;
  }
}



//--------------------------------------------------------------------------------------------------
ElectronIDMVA::~ElectronIDMVA()
{
  for(UInt_t i=0; i<6; ++i) {
    if (fTMVAReader[i]) delete fTMVAReader[i];
  }
}

//--------------------------------------------------------------------------------------------------
void ElectronIDMVA::Initialize( std::string methodName,
                                std::string Subdet0Pt10To20Weights ,
                                std::string Subdet1Pt10To20Weights ,
                                std::string Subdet2Pt10To20Weights,
                                std::string Subdet0Pt20ToInfWeights,
                                std::string Subdet1Pt20ToInfWeights,
                                std::string Subdet2Pt20ToInfWeights,
                                ElectronIDMVA::MVAType type) {

  fIsInitialized = kTRUE;
  fMVAType = type;

  fMethodname = methodName;

  std::cout << "Initializing type " << fMVAType << "MVA" << std::endl;

  for(UInt_t i=0; i<6; ++i) {
    if (fTMVAReader[i]) delete fTMVAReader[i];

    fTMVAReader[i] = new TMVA::Reader( "!Color:Silent:Error" );
    fTMVAReader[i]->SetVerbose(kTRUE);

    switch(type) {
    case kBaseline:
      fTMVAReader[i]->AddVariable( "SigmaIEtaIEta",         &fMVAVar_EleSigmaIEtaIEta         );
      fTMVAReader[i]->AddVariable( "DEtaIn",                &fMVAVar_EleDEtaIn                );
      fTMVAReader[i]->AddVariable( "DPhiIn",                &fMVAVar_EleDPhiIn                );
      fTMVAReader[i]->AddVariable( "FBrem",                 &fMVAVar_EleFBrem                 );
      fTMVAReader[i]->AddVariable( "SigmaIPhiIPhi",         &fMVAVar_EleSigmaIPhiIPhi         );
      fTMVAReader[i]->AddVariable( "NBrem",                 &fMVAVar_EleNBrem                 );
      fTMVAReader[i]->AddVariable( "OneOverEMinusOneOverP", &fMVAVar_EleOneOverEMinusOneOverP );
      break;
    case kNoIPInfo:
      fTMVAReader[i]->AddVariable( "SigmaIEtaIEta",         &fMVAVar_EleSigmaIEtaIEta         );
      fTMVAReader[i]->AddVariable( "DEtaIn",                &fMVAVar_EleDEtaIn                );
      fTMVAReader[i]->AddVariable( "DPhiIn",                &fMVAVar_EleDPhiIn                );
      fTMVAReader[i]->AddVariable( "FBrem",                 &fMVAVar_EleFBrem                 );
      fTMVAReader[i]->AddVariable( "EOverP",                &fMVAVar_EleEOverP                );
      fTMVAReader[i]->AddVariable( "ESeedClusterOverPout",  &fMVAVar_EleESeedClusterOverPout  );
      fTMVAReader[i]->AddVariable( "SigmaIPhiIPhi",         &fMVAVar_EleSigmaIPhiIPhi         );
      fTMVAReader[i]->AddVariable( "NBrem",                 &fMVAVar_EleNBrem                 );
      fTMVAReader[i]->AddVariable( "OneOverEMinusOneOverP", &fMVAVar_EleOneOverEMinusOneOverP );
      fTMVAReader[i]->AddVariable( "ESeedClusterOverPIn",   &fMVAVar_EleESeedClusterOverPIn   );
      break;
    case kWithIPInfo:
      fTMVAReader[i]->AddVariable( "SigmaIEtaIEta",         &fMVAVar_EleSigmaIEtaIEta         );
      fTMVAReader[i]->AddVariable( "DEtaIn",                &fMVAVar_EleDEtaIn                );
      fTMVAReader[i]->AddVariable( "DPhiIn",                &fMVAVar_EleDPhiIn                );
      fTMVAReader[i]->AddVariable( "D0",                    &fMVAVar_EleD0                    );
      fTMVAReader[i]->AddVariable( "FBrem",                 &fMVAVar_EleFBrem                 );
      fTMVAReader[i]->AddVariable( "EOverP",                &fMVAVar_EleEOverP                );
      fTMVAReader[i]->AddVariable( "ESeedClusterOverPout",  &fMVAVar_EleESeedClusterOverPout  );
      fTMVAReader[i]->AddVariable( "SigmaIPhiIPhi",         &fMVAVar_EleSigmaIPhiIPhi         );
      fTMVAReader[i]->AddVariable( "NBrem",                 &fMVAVar_EleNBrem                 );
      fTMVAReader[i]->AddVariable( "OneOverEMinusOneOverP", &fMVAVar_EleOneOverEMinusOneOverP );
      fTMVAReader[i]->AddVariable( "ESeedClusterOverPIn",   &fMVAVar_EleESeedClusterOverPIn   );
      fTMVAReader[i]->AddVariable( "IP3d",                  &fMVAVar_EleIP3d                  );
      fTMVAReader[i]->AddVariable( "IP3dSig",               &fMVAVar_EleIP3dSig               );
      break;
    case kTrig2012:
      // Pure tracking variables
      fTMVAReader[i]->AddVariable("fbrem",           &fMVAVar_EleFBrem);
      fTMVAReader[i]->AddVariable("kfchi2",          &fMVAVar_EleKfChi2);
      fTMVAReader[i]->AddVariable("kfhits",          &fMVAVar_EleKfHits);
      fTMVAReader[i]->AddVariable("gsfchi2",         &fMVAVar_EleGsfChi2);
      // Geometrical matchings
      fTMVAReader[i]->AddVariable("deta",            &fMVAVar_EleDEtaIn);
      fTMVAReader[i]->AddVariable("dphi",            &fMVAVar_EleDPhiIn);
      fTMVAReader[i]->AddVariable("detacalo",        &fMVAVar_EleDEtaCalo);    
      // Pure ECAL -> shower shapes
      fTMVAReader[i]->AddVariable("see",             &fMVAVar_EleSigmaIEtaIEta);
      fTMVAReader[i]->AddVariable("spp",             &fMVAVar_EleSigmaIPhiIPhi);
      fTMVAReader[i]->AddVariable("etawidth",        &fMVAVar_EleEtaWidth);
      fTMVAReader[i]->AddVariable("phiwidth",        &fMVAVar_ElePhiWidth);
      fTMVAReader[i]->AddVariable("e1x5e5x5",        &fMVAVar_EleOneMinusE1x5E5x5);
      fTMVAReader[i]->AddVariable("R9",              &fMVAVar_EleR9);
      // Energy matching
      fTMVAReader[i]->AddVariable("HoE",             &fMVAVar_EleHoverE);
      fTMVAReader[i]->AddVariable("EoP",             &fMVAVar_EleEOverP); 
      fTMVAReader[i]->AddVariable("IoEmIoP",         &fMVAVar_EleOneOverEMinusOneOverP);
      fTMVAReader[i]->AddVariable("eleEoPout",       &fMVAVar_EleEClusterOverPout);
      if(i == 2 || i == 5) 
	fTMVAReader[i]->AddVariable("PreShowerOverRaw",&fMVAVar_ElePreshowerOverRaw);      
      // IP
      fTMVAReader[i]->AddVariable("d0",              &fMVAVar_EleD0);
      fTMVAReader[i]->AddVariable("ip3d",            &fMVAVar_EleIP3d);
      // spectators
      fTMVAReader[i]->AddSpectator("eta",            &fMVAVar_EleEta);
      fTMVAReader[i]->AddSpectator("pt",             &fMVAVar_ElePt);
      break;
    default:
      throw cms::Exception("IDNotAvailable") << "Electron MVA ID: " 
					     << type << " not available." 
					     << std::endl;
    }

    switch(i) {
    case 0: loadTMVAWeights(fTMVAReader[i], fMethodname , Subdet0Pt10To20Weights ); break;
    case 1: loadTMVAWeights(fTMVAReader[i], fMethodname , Subdet1Pt10To20Weights ); break;
    case 2: loadTMVAWeights(fTMVAReader[i], fMethodname , Subdet2Pt10To20Weights ); break;
    case 3: loadTMVAWeights(fTMVAReader[i], fMethodname , Subdet0Pt20ToInfWeights ); break;
    case 4: loadTMVAWeights(fTMVAReader[i], fMethodname , Subdet1Pt20ToInfWeights ); break;
    case 5: loadTMVAWeights(fTMVAReader[i], fMethodname , Subdet2Pt20ToInfWeights ); break;
    default: throw cms::Exception("OutOfBounds") << "Index " << i 
						 << " is out of bounds!" 
						 << std::endl;
    }

  }

  std::cout << "Electron ID MVA Initialization\n";
  std::cout << "MethodName : " << fMethodname << " , type == " << type << std::endl;
  std::cout << "Load weights file : " << Subdet0Pt10To20Weights << std::endl;
  std::cout << "Load weights file : " << Subdet1Pt10To20Weights << std::endl;
  std::cout << "Load weights file : " << Subdet2Pt10To20Weights << std::endl;
  std::cout << "Load weights file : " << Subdet0Pt20ToInfWeights << std::endl;
  std::cout << "Load weights file : " << Subdet1Pt20ToInfWeights << std::endl;
  std::cout << "Load weights file : " << Subdet2Pt20ToInfWeights << std::endl;

}


//--------------------------------------------------------------------------------------------------
Double_t ElectronIDMVA::MVAValue(Double_t ElePt , Double_t EleSCEta,
                                 Double_t EleSigmaIEtaIEta,
                                 Double_t EleDEtaIn,
                                 Double_t EleDPhiIn,
                                 Double_t EleHoverE,
                                 Double_t EleD0,
                                 Double_t EleFBrem,
                                 Double_t EleEOverP,
                                 Double_t EleESeedClusterOverPout,
                                 Double_t EleSigmaIPhiIPhi,
                                 Double_t EleNBrem,
                                 Double_t EleOneOverEMinusOneOverP,
                                 Double_t EleESeedClusterOverPIn,
                                 Double_t EleIP3d,
                                 Double_t EleIP3dSig,
				 double EleKfChi2,
				 double EleKfHits ,
				 double EleGsfChi2 ,
				 double EleDEtaCalo ,
				 double EleEtaWidth ,
				 double ElePhiWidth ,
				 double EleOneMinusE1x5E5x5 ,
				 double EleR9 ,
				 double ElePreshowerOverRaw ,
				 double EleEClusterOverPout 
  ) {

  if (!fIsInitialized) {
    std::cout << "Error: ElectronIDMVA not properly initialized.\n";
    return -9999;
  }

  Int_t subdet = 0;
  Int_t ptBin = 0;
  switch(fMVAType) {
  case kBaseline:
  case kNoIPInfo:
  case kWithIPInfo:    
    if (fabs(EleSCEta) < 1.0) subdet = 0;
    else if (fabs(EleSCEta) < 1.479) subdet = 1;
    else subdet = 2;  
    if (ElePt > 20.0) ptBin = 1;
    break;
  case kTrig2012:
    ptBin = int(ElePt > 20.0);
    subdet = ( int(fabs(EleSCEta) >= 1.479) +
	       int(fabs(EleSCEta) >= 0.8) );
    break;    
  }  

  //set all input variables
  fMVAVar_EleSigmaIEtaIEta = EleSigmaIEtaIEta;
  fMVAVar_EleDEtaIn = EleDEtaIn;
  fMVAVar_EleDPhiIn = EleDPhiIn;
  fMVAVar_EleHoverE = EleHoverE;
  fMVAVar_EleD0 = EleD0;
  fMVAVar_EleFBrem = EleFBrem;
  fMVAVar_EleEOverP = EleEOverP;
  fMVAVar_EleESeedClusterOverPout = EleESeedClusterOverPout;
  fMVAVar_EleSigmaIPhiIPhi = EleSigmaIPhiIPhi;
  fMVAVar_EleNBrem = EleNBrem;
  fMVAVar_EleOneOverEMinusOneOverP = EleOneOverEMinusOneOverP;
  fMVAVar_EleESeedClusterOverPIn = EleESeedClusterOverPIn;
  fMVAVar_EleIP3d = EleIP3d;
  fMVAVar_EleIP3dSig = EleIP3dSig;
  fMVAVar_EleKfChi2 = EleKfChi2;
  fMVAVar_EleKfHits = EleKfHits;
  fMVAVar_EleGsfChi2 = EleGsfChi2;
  fMVAVar_EleDEtaCalo = EleDEtaCalo;
  fMVAVar_EleEtaWidth = EleEtaWidth;
  fMVAVar_ElePhiWidth = ElePhiWidth;
  fMVAVar_EleOneMinusE1x5E5x5 = EleOneMinusE1x5E5x5;
  fMVAVar_EleR9 = EleR9;
  fMVAVar_ElePreshowerOverRaw = ElePreshowerOverRaw;
  fMVAVar_EleEClusterOverPout = EleEClusterOverPout;
  fMVAVar_EleEta = EleSCEta;
  fMVAVar_ElePt = ElePt;
  

  Double_t mva = -9999;
  TMVA::Reader *reader = 0;
  Int_t MVABin = subdet + 3*ptBin;
  /*
  if (subdet == 0 && ptBin == 0) MVABin = 0;
  if (subdet == 1 && ptBin == 0) MVABin = 1;
  if (subdet == 2 && ptBin == 0) MVABin = 2;
  if (subdet == 0 && ptBin == 1) MVABin = 3;
  if (subdet == 1 && ptBin == 1) MVABin = 4;
  if (subdet == 2 && ptBin == 1) MVABin = 5;
  */
  assert(MVABin >= 0 && MVABin <= 5 && "MVABin out of range!");
  reader = fTMVAReader[MVABin];

  mva = reader->EvaluateMVA( fMethodname );

  return mva;
}



//--------------------------------------------------------------------------------------------------
Double_t ElectronIDMVA::MVAValue(const reco::GsfElectron *ele, const reco::Vertex vertex,
                                 EcalClusterLazyTools myEcalCluster,
                                 const TransientTrackBuilder *transientTrackBuilder) {

  if (!fIsInitialized) {
    std::cout << "Error: ElectronIDMVA not properly initialized.\n";
    return -9999;
  }

  //initialize
  fMVAVar_EleSigmaIEtaIEta = -9999.0;
  fMVAVar_EleDEtaIn = -9999.0;
  fMVAVar_EleDPhiIn = -9999.0;
  fMVAVar_EleHoverE = -9999.0;
  fMVAVar_EleD0 = -9999.0;
  fMVAVar_EleFBrem = -9999.0;
  fMVAVar_EleEOverP = -9999.0;
  fMVAVar_EleESeedClusterOverPout = -9999.0;
  fMVAVar_EleSigmaIPhiIPhi = -9999.0;
  fMVAVar_EleNBrem = -9999.0;
  fMVAVar_EleOneOverEMinusOneOverP = -9999.0;
  fMVAVar_EleESeedClusterOverPIn = -9999.0;
  fMVAVar_EleIP3d = -9999.0;
  fMVAVar_EleIP3dSig = -9999.0;

  Int_t subdet = 0;
  Int_t ptBin = 0;

  switch(fMVAType) {
  case kBaseline:
  case kNoIPInfo:
  case kWithIPInfo:    
    if (fabs(ele->superCluster()->eta()) < 1.0) subdet = 0;
    else if (fabs(ele->superCluster()->eta()) < 1.479) subdet = 1;
    else subdet = 2;  
    if (ele->pt() > 20.0) ptBin = 1;
    break;
  case kTrig2012:
    ptBin = int(ele->pt() > 20.0);
    subdet = ( int(fabs(ele->superCluster()->eta()) >= 1.479) +
	       int(fabs(ele->superCluster()->eta()) >= 0.8) );
    break;    
  }

  //set all input variables
  fMVAVar_EleSigmaIEtaIEta = ele->sigmaIetaIeta() ;
  fMVAVar_EleDEtaIn = ele->deltaEtaSuperClusterTrackAtVtx();
  fMVAVar_EleDPhiIn = ele->deltaPhiSuperClusterTrackAtVtx();
  fMVAVar_EleDEtaCalo = ele->deltaEtaSeedClusterTrackAtCalo();
  fMVAVar_EleOneMinusE1x5E5x5  =  (ele->e5x5()) !=0. ? 1.-(ele->e1x5()/ele->e5x5()) : -1. ;
  fMVAVar_EleHoverE = ele->hcalOverEcal();
  fMVAVar_EleEtaWidth = ele->superCluster()->etaWidth();
  fMVAVar_ElePhiWidth = ele->superCluster()->phiWidth();


  fMVAVar_EleFBrem = ele->fbrem();
  fMVAVar_EleEOverP = ele->eSuperClusterOverP();
  fMVAVar_EleESeedClusterOverPout = ele->eSeedClusterOverPout();
  fMVAVar_EleEClusterOverPout = ele->eEleClusterOverPout();

  reco::TrackRef ctfr = ele->closestCtfTrackRef();
  bool validKF(ctfr.isNonnull() && ctfr.isAvailable());

  fMVAVar_EleKfChi2 =  (validKF) ? ctfr->normalizedChi2() : 0 ;
  fMVAVar_EleKfHits =  (validKF) ? ctfr->hitPattern().trackerLayersWithMeasurement() : -1. ; 
  fMVAVar_EleGsfChi2 =  ele->gsfTrack()->normalizedChi2();  
  fMVAVar_EleR9 =  myEcalCluster.e3x3(*(ele->superCluster()->seed())) / ele->superCluster()->rawEnergy();
  fMVAVar_ElePreshowerOverRaw =  ele->superCluster()->preshowerEnergy() / ele->superCluster()->rawEnergy();

  //temporary fix for weird electrons with Sigma iPhi iPhi == Nan
  //these occur at the sub-percent level
  std::vector<float> vCov = myEcalCluster.localCovariances(*(ele->superCluster()->seed())) ;
  if (!isnan(vCov[2])) fMVAVar_EleSigmaIPhiIPhi = sqrt (vCov[2]);
  else fMVAVar_EleSigmaIPhiIPhi = (fMVAType < 3 ? ele->sigmaIetaIeta() : 0.0);

  fMVAVar_EleNBrem = ele->basicClustersSize() - 1;
  fMVAVar_EleOneOverEMinusOneOverP = (1.0/(ele->superCluster()->energy())) - 1.0 / ele->gsfTrack()->p();
  fMVAVar_EleESeedClusterOverPIn = ele->superCluster()->seed()->energy() / ele->trackMomentumAtVtx().R();

  fMVAVar_EleEta = ele->superCluster()->eta();
  fMVAVar_ElePt  = ele->pt();

  //d0
  if (ele->gsfTrack().isNonnull()) {
    fMVAVar_EleD0 = (-1.0)*ele->gsfTrack()->dxy(vertex.position());
  } else if (ele->closestCtfTrackRef().isNonnull()) {
    fMVAVar_EleD0 = (-1.0)*ele->closestCtfTrackRef()->dxy(vertex.position());
  } else {
    fMVAVar_EleD0 = -9999.0;
  }

  //default values for IP3D
  fMVAVar_EleIP3d = -999.0;
  fMVAVar_EleIP3dSig = 0.0;
  if (ele->gsfTrack().isNonnull()) {
    const double gsfsign   = ( (-ele->gsfTrack()->dxy(vertex.position()))   >=0 ) ? 1. : -1.;

    const reco::TransientTrack &tt = transientTrackBuilder->build(ele->gsfTrack());
    const std::pair<bool,Measurement1D> &ip3dpv =  IPTools::absoluteImpactParameter3D(tt,vertex);
    if (ip3dpv.first) {
      double ip3d = gsfsign*ip3dpv.second.value();
      double ip3derr = ip3dpv.second.error();
      fMVAVar_EleIP3d = ip3d;
      fMVAVar_EleIP3dSig = ip3d/ip3derr;
    }
  }

  Double_t mva = -9999;
  TMVA::Reader *reader = 0;
  Int_t MVABin = subdet + 3*ptBin;
  /*
  if (subdet == 0 && ptBin == 0) MVABin = 0;
  if (subdet == 1 && ptBin == 0) MVABin = 1;
  if (subdet == 2 && ptBin == 0) MVABin = 2;
  if (subdet == 0 && ptBin == 1) MVABin = 3;
  if (subdet == 1 && ptBin == 1) MVABin = 4;
  if (subdet == 2 && ptBin == 1) MVABin = 5;
  */
  assert(MVABin >= 0 && MVABin <= 5 && "MVABin out of range!");
  reader = fTMVAReader[MVABin];

  mva = reader->EvaluateMVA( fMethodname );

//   ***************************************************
//   For DEBUGGING
//   std::cout << "********************************\n";
//   std::cout << "Electron MVA\n";
//   std::cout << ele->pt() << " " << ele->eta() << " " << ele->phi() << " : " << ele->superCluster()->eta() << " : " << MVABin << std::endl;
//   std::cout << fMVAVar_EleSigmaIEtaIEta << "\n"
//        << fMVAVar_EleDEtaIn << "\n"
//        << fMVAVar_EleDPhiIn << "\n"
//        << fMVAVar_EleHoverE << "\n"
//        << fMVAVar_EleD0 << "\n"
//        << fMVAVar_EleFBrem << "\n"
//        << fMVAVar_EleEOverP << "\n"
//        << fMVAVar_EleESeedClusterOverPout << "\n"
//        << fMVAVar_EleSigmaIPhiIPhi << "\n"
//        << fMVAVar_EleNBrem << "\n"
//        << fMVAVar_EleOneOverEMinusOneOverP << "\n"
//        << fMVAVar_EleESeedClusterOverPIn << "\n"
//        << fMVAVar_EleIP3d << "\n"
//        << fMVAVar_EleIP3dSig << "\n"
//        << std::endl;
//   std::cout << "MVA: " << mva << std::endl;
//   std::cout << "********************************\n";

  return mva;
}


//--------------------------------------------------------------------------------------------------
Double_t ElectronIDMVA::MVAValue(const reco::GsfElectron *ele,
                                 EcalClusterLazyTools myEcalCluster) {

  if (!fIsInitialized) {
    std::cout << "Error: ElectronIDMVA not properly initialized.\n";
    return -9999;
  }
  if (fMVAType == kWithIPInfo) {
    std::cout << "Error: ElectronIDMVA was initialized with type that requires vertex information. "
              << "It is not compatible with this accessor. \n";
    return -9999;
  }

  //initialize
  fMVAVar_EleSigmaIEtaIEta = -9999.0;
  fMVAVar_EleDEtaIn = -9999.0;
  fMVAVar_EleDPhiIn = -9999.0;
  fMVAVar_EleHoverE = -9999.0;
  fMVAVar_EleFBrem = -9999.0;
  fMVAVar_EleEOverP = -9999.0;
  fMVAVar_EleESeedClusterOverPout = -9999.0;
  fMVAVar_EleSigmaIPhiIPhi = -9999.0;
  fMVAVar_EleNBrem = -9999.0;
  fMVAVar_EleOneOverEMinusOneOverP = -9999.0;
  fMVAVar_EleESeedClusterOverPIn = -9999.0;

  Int_t subdet = 0;
  if (fabs(ele->superCluster()->eta()) < 1.0) subdet = 0;
  else if (fabs(ele->superCluster()->eta()) < 1.479) subdet = 1;
  else subdet = 2;
  Int_t ptBin = 0;
  if (ele->pt() > 20.0) ptBin = 1;

  //set all input variables
  fMVAVar_EleSigmaIEtaIEta = ele->sigmaIetaIeta() ;
  fMVAVar_EleDEtaIn = ele->deltaEtaSuperClusterTrackAtVtx();
  fMVAVar_EleDPhiIn = ele->deltaPhiSuperClusterTrackAtVtx();
  fMVAVar_EleHoverE = ele->hcalOverEcal();

  fMVAVar_EleFBrem = ele->fbrem();
  fMVAVar_EleEOverP = ele->eSuperClusterOverP();
  fMVAVar_EleESeedClusterOverPout = ele->eSeedClusterOverPout();

  //temporary fix for weird electrons with Sigma iPhi iPhi == Nan
  //these occur at the sub-percent level
  std::vector<float> vCov = myEcalCluster.localCovariances(*(ele->superCluster()->seed())) ;
  if (!isnan(vCov[2])) fMVAVar_EleSigmaIPhiIPhi = sqrt (vCov[2]);
  else fMVAVar_EleSigmaIPhiIPhi = ele->sigmaIetaIeta();

  fMVAVar_EleNBrem = ele->basicClustersSize() - 1;
  fMVAVar_EleOneOverEMinusOneOverP = (1.0/(ele->superCluster()->energy())) - 1.0 / ele->gsfTrack()->p();
  fMVAVar_EleESeedClusterOverPIn = ele->superCluster()->seed()->energy() / ele->trackMomentumAtVtx().R();


  Double_t mva = -9999;
  TMVA::Reader *reader = 0;
  Int_t MVABin = -1;
  if (subdet == 0 && ptBin == 0) MVABin = 0;
  if (subdet == 1 && ptBin == 0) MVABin = 1;
  if (subdet == 2 && ptBin == 0) MVABin = 2;
  if (subdet == 0 && ptBin == 1) MVABin = 3;
  if (subdet == 1 && ptBin == 1) MVABin = 4;
  if (subdet == 2 && ptBin == 1) MVABin = 5;
  assert(MVABin >= 0 && MVABin <= 5);
  reader = fTMVAReader[MVABin];

  mva = reader->EvaluateMVA( fMethodname );

//   ***************************************************
//   For DEBUGGING
//   std::cout << "********************************\n";
//   std::cout << "Electron MVA\n";
//   std::cout << ele->pt() << " " << ele->eta() << " " << ele->phi() << " : " << ele->superCluster()->eta() << " : " << MVABin << std::endl;
//   std::cout << fMVAVar_EleSigmaIEtaIEta << "\n"
//        << fMVAVar_EleDEtaIn << "\n"
//        << fMVAVar_EleDPhiIn << "\n"
//        << fMVAVar_EleHoverE << "\n"
//        << fMVAVar_EleFBrem << "\n"
//        << fMVAVar_EleEOverP << "\n"
//        << fMVAVar_EleESeedClusterOverPout << "\n"
//        << fMVAVar_EleSigmaIPhiIPhi << "\n"
//        << fMVAVar_EleNBrem << "\n"
//        << fMVAVar_EleOneOverEMinusOneOverP << "\n"
//        << fMVAVar_EleESeedClusterOverPIn << "\n"
//        << std::endl;
//   std::cout << "MVA: " << mva << std::endl;
//   std::cout << "********************************\n";

  return mva;
}

double ElectronIDMVA::MVAValue(
    const reco::GsfElectron *ele,
    const edm::Event& evt,
    const edm::EventSetup& es,
    const edm::InputTag& ebRecHits,
    const edm::InputTag& eeRecHits) {
  EcalClusterLazyTools clusterTool(evt, es, ebRecHits, eeRecHits);
  return MVAValue(ele, clusterTool);
}

#endif
