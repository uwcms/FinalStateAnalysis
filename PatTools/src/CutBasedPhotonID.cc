#include "FinalStateAnalysis/PatTools/interface/CutBasedPhotonID.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

// Single Tower H/E
 #include "RecoEgamma/EgammaElectronAlgos/interface/ElectronHcalHelper.h"

// Conversation Safe Electron Veto
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

namespace photontools {

  namespace {
    typedef edm::ParameterSet  PSet;
    typedef edm::VParameterSet VPset;
    typedef std::vector<double> vdouble;
  }
  

  CutSet::CutSet( const PSet& conf ) {
    id_params setup;
    unsigned short themask=0,theveto=0;

    // setup electron veto, masks and veto
    if( conf.existsAs<bool>("ElectronVeto") ) {
      setup.electronVeto = conf.getParameter<bool>("ElectronVeto");
      bool mask = conf.getParameter<bool>("Mask_ElectronVeto");
      bool veto = conf.getParameter<bool>("Veto_ElectronVeto");
      themask += mask*(1 << kElectronVeto);
      theveto += veto*(1 << kElectronVeto);
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define ElectronVeto requirement!";
    }  
    
    // setup single tower H/E masks and veto
    if( conf.existsAs<vdouble>("SingleTowerHoverE") ) {
      vdouble theParams = conf.getParameter<double>("SingleTowerHoverE");
      setup.singleTowerHoE_min_eb = theParams[0];
      setup.singleTowerHoE_max_eb = theParams[1];
      
      setup.singleTowerHoE_min_ee = theParams[2];
      setup.singleTowerHoE_max_ee = theParams[3];
      
      bool mask = conf.getParameter<bool>("Mask_SingleTowerHoverE");
      bool veto = conf.getParameter<bool>("Veto_SingleTowerHoverE");
      themask += mask*(1 << kSingleTowerHoE);
      theveto += veto*(1 << kSingleTowerHoE);
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define SingleTowerHoverE requirement!";
    }

    // setup SigmaIEtaIEta masks and veto
    if( conf.existsAs<vdouble>("SigmaIEtaIEta") ) {
      vdouble theParams = conf.getParameter<double>("SigmaIEtaIEta");
      setup.sihih_min_eb = theParams[0];
      setup.sihih_max_eb = theParams[1];
      
      setup.sihih_min_ee = theParams[2];
      setup.sihih_max_ee = theParams[3];
      
      bool mask = conf.getParameter<bool>("Mask_SigmaIEtaIEta");
      bool veto = conf.getParameter<bool>("Veto_SigmaIEtaIEta");
      themask += mask*(1 << kSihih);
      theveto += veto*(1 << kSihih);
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define SigmaIEtaIEta requirement!";
    }

    // setup PFChargedIso masks and veto
    if( conf.existsAs<vdouble>("PFChargedIso") ) {
      vdouble theParams = conf.getParameter<vdouble>("PFChargedIso");
      setup.pfChargedIso_min_eb = theParams[0];
      setup.pfChargedIso_max_eb = theParams[1];
      
      setup.pfChargedIso_min_ee = theParams[2];
      setup.pfChargedIso_max_ee = theParams[3];

      vdouble slopeParams = conf.getParameter<vdouble>("PFChargedIsoPtSlope");
      setup.pfChargedIso_pt_slope_eb = slopeParams[0];
      setup.pfChargedIso_pt_slope_ee = slopeParams[1];
      
      bool mask = conf.getParameter<bool>("Mask_PFChargedIso");
      bool veto = conf.getParameter<bool>("Veto_PFChargedIso");
      themask += mask*(1 << kPFChargedIso);
      theveto += veto*(1 << kPFChargedIso);
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define PFChargedIso requirement!";
    }

    // setup PFNeutralIso masks and veto
    if( conf.existsAs<vdouble>("PFNeutralIso") ) {
      vdouble theParams = conf.getParameter<vdouble>("PFNeutralIso");
      setup.pfNeutralIso_min_eb = theParams[0];
      setup.pfNeutralIso_max_eb = theParams[1];
      
      setup.pfNeutralIso_min_ee = theParams[2];
      setup.pfNeutralIso_max_ee = theParams[3];

      vdouble slopeParams = conf.getParameter<vdouble>("PFNeutralIsoPtSlope");
      setup.pfNeutralIso_pt_slope_eb = slopeParams[0];
      setup.pfNeutralIso_pt_slope_ee = slopeParams[1];
      
      bool mask = conf.getParameter<bool>("Mask_PFNeutralIso");
      bool veto = conf.getParameter<bool>("Veto_PFNeutralIso");
      themask += mask*(1 << kPFNeutralIso);
      theveto += veto*(1 << kPFNeutralIso);
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define PFNeutralIso requirement!";
    }

    // setup PFPhotonIso masks and veto
    if( conf.existsAs<vdouble>("PFPhotonIso") ) {
      vdouble theParams = conf.getParameter<vdouble>("PFPhotonIso");
      setup.pfNeutralIso_min_eb = theParams[0];
      setup.pfNeutralIso_max_eb = theParams[1];
      
      setup.pfNeutralIso_min_ee = theParams[2];
      setup.pfNeutralIso_max_ee = theParams[3];

      vdouble slopeParams = conf.getParameter<vdouble>("PFPhotonIsoPtSlope");
      setup.pfNeutralIso_pt_slope_eb = slopeParams[0];
      setup.pfNeutralIso_pt_slope_ee = slopeParams[1];
      
      bool mask = conf.getParameter<bool>("Mask_PFPhotonIso");
      bool veto = conf.getParameter<bool>("Veto_PFPhotonIso");
      themask += mask*(1 << kPFPhotonIso);
      theveto += veto*(1 << kPFPhotonIso);
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define PFPhotonIso requirement!";
    }
    
    _mask = (_passAll & ~themask);
    _veto = (_passAll & ~theveto);
    _theid = setup;
    
  } // CutSet::CutSet()
  
  bool CutSet::operator() (const pat::Photon& thePho,
			   const unsigned short mask) {
    unsigned short eval = 0x0;
    
    // PUT EACH CUT INSIDE { } SO THAT VARIABLES DESCOPE AND 
    // YOU DON'T FUCK UP AND MAKE A BUG
    { 
      // ElectronVeto    
      bool passesVeto = (thePho.getUserInt("ConvSafeElectronVeto") 
			 == _theID.electronVeto);
      eval += passesVeto*(1<<kElectronVeto);
    }

    {
      //SingleTowerHoverE
      bool passesHoE = false;
      if( fabs(thePho.superCluster().eta()) < 1.566 ) { // EB
	passesHoE = 
	(thePho.getUserFloat("SingleTowerHoE") < _theid.singleTowerHoE_max_eb&&
	 thePho.getUserFloat("SingleTowerHoE") > _theid.singleTowerHoE_min_eb);
      } else {
	passesHoE = 
	(thePho.getUserFloat("SingleTowerHoE") < _theid.singleTowerHoE_max_ee&&
	 thePho.getUserFloat("SingleTowerHoE") > _theid.singleTowerHoE_min_ee);
      }
      eval += passesHoE*(1<<kSingleTowerHoE);
    }

    {
      //SigmaIEtaIEta
      bool passesSihih = false;
      if( fabs(thePho.superCluster().eta()) < 1.566 ) { // EB
	passesSihih = (thePho.sigmaIetaIeta() < _theid.sihih_max_eb &&
		       thePho.sigmaIetaIeta() > _theid.sihih_min_eb    );
      } else {
	passesSihih = (thePho.sigmaIetaIeta() < _theid.sihih_max_ee &&
		       thePho.sigmaIetaIeta() > _theid.sihih_min_ee    );
      }
      eval += passesSihih*(1<<kSihih);
    }

    {
      //PFCharged Iso -- depends on kt6PFJetsRho_Photon, PhotonEA_chg
      bool passesPFChargedIso = false;
      double ea_charged_iso = 
	std::max( thePho.userIso(pat::PfChargedIsolation) - 
		  (thePho.userFloat("PhotonEA_chg")*
		   thePho.userFloat("kt6PFJetsRho_Photon")), 0.0 );
      if( fabs(thePho.superCluster().eta()) < 1.566 ) { // EB
	double iso_shift = _theid.pfChargedIso_pt_slope_eb*thePho.pt();
	double the_max   = _theid.pfChargedIso_max_eb + iso_shift; 
	double the_min   = _theid.pfChargedIso_min_eb + iso_shift;
	passesPFChargedIso = (ea_charged_iso < the_max &&
			      ea_charged_iso > the_min    );
      } else {
	double iso_shift = _theid.pfChargedIso_pt_slope_ee*thePho.pt();
	double the_max   = _theid.pfChargedIso_max_ee + iso_shift; 
	double the_min   = _theid.pfChargedIso_min_ee + iso_shift;
	passesPFChargedIso = (thePho.sigmaIetaIeta() < the_max &&
			      thePho.sigmaIetaIeta() > the_min    );
      }
      eval += passesPFChargedIso*(1<<kPFChargedIso);
    }
    
    {
      //PFNeutral Iso -- depends on kt6PFJetsRho_Photon, PhotonEA_neut
      bool passesPFNeutralIso = false;
      double ea_neutral_iso = 
	std::max( thePho.userIso(pat::PfNeutralIsolation) - 
		  (thePho.userFloat("PhotonEA_neut")*
		   thePho.userFloat("kt6PFJetsRho_Photon")), 0.0 );
      if( fabs(thePho.superCluster().eta()) < 1.566 ) { // EB
	double iso_shift = _theid.pfNeutralIso_pt_slope_eb*thePho.pt();
	double the_max   = _theid.pfNeutralIso_max_eb + iso_shift; 
	double the_min   = _theid.pfNeutralIso_min_eb + iso_shift;
	passesPFNeutralIso = (ea_neutral_iso < the_max &&
			      ea_neutral_iso > the_min    );
      } else {
	double iso_shift = _theid.pfNeutralIso_pt_slope_ee*thePho.pt();
	double the_max   = _theid.pfNeutralIso_max_ee + iso_shift; 
	double the_min   = _theid.pfNeutralIso_min_ee + iso_shift;
	passesPFNeutralIso = (ea_neutral_iso < the_max &&
			      ea_neutral_iso > the_min    );
      }
      eval += passesPFNeutralIso*(1<<kPFNeutralIso);
    }

    {
      //PFPhoton Iso -- depends on kt6PFJetsRho_Photon, PhotonEA_pho
      bool passesPFPhotonIso = false;
      double ea_photon_iso = 
	std::max( thePho.userIso(pat::PfPhotonIsolation) - 
		  (thePho.userFloat("PhotonEA_pho")*
		   thePho.userFloat("kt6PFJetsRho_Photon")), 0.0 );
      if( fabs(thePho.superCluster().eta()) < 1.566 ) { // EB
	double iso_shift = _theid.pfPhotonIso_pt_slope_eb*thePho.pt();
	double the_max   = _theid.pfPhotonIso_max_eb + iso_shift; 
	double the_min   = _theid.pfPhotonIso_min_eb + iso_shift;
	passesPFPhotonIso = (ea_photon_iso < the_max &&
			     ea_photon_iso > the_min    );
      } else {
	double iso_shift = _theid.pfPhotonIso_pt_slope_ee*thePho.pt();
	double the_max   = _theid.pfPhotonIso_max_ee + iso_shift; 
	double the_min   = _theid.pfPhotonIso_min_ee + iso_shift;
	passesPFPhotonIso = (ea_photon_iso < the_max &&
			     ea_photon_iso > the_min    );
      }
      eval += passesPFPhotonIso*(1<<kPFPhotonIso);
    }
    
    // yeah various bitwise nots are annoying but it makes the 
    // math easier...
    unsigned mask_tot = ~(~_mask + ~(_passAll&mask))
    unsigned pass     = _passAll & _veto & masktot;
    unsigned result   = eval     & mask_tot;

    return ( result == pass );
  }
}
