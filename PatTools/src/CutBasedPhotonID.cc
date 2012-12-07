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
    typedef edm::VParameterSet VPSet;
    typedef std::vector<double> vdouble;
    typedef std::vector<std::string> vstring;
  }
  
  CutSet::CutSet( const PSet& conf ) {
    id_params setup;
    unsigned themask=0,theveto=0;

    // setup electron veto, masks and veto
    if( conf.existsAs<bool>("ElectronVeto") ) {
      setup.electronVeto = conf.getParameter<bool>("ElectronVeto");
      bool mask = conf.getParameter<bool>("Mask_ElectronVeto");
      bool veto = conf.getParameter<bool>("Veto_ElectronVeto");
      themask += mask*kElectronVeto;
      theveto += veto*kElectronVeto;
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define ElectronVeto requirement!";
    }  
    
    // setup single tower H/E masks and veto
    if( conf.existsAs<vdouble>("SingleTowerHoverE") ) {
      vdouble theParams = conf.getParameter<vdouble>("SingleTowerHoverE");
      setup.singleTowerHoE_min_eb = theParams[0];
      setup.singleTowerHoE_max_eb = theParams[1];
      
      setup.singleTowerHoE_min_ee = theParams[2];
      setup.singleTowerHoE_max_ee = theParams[3];
      
      bool mask = conf.getParameter<bool>("Mask_SingleTowerHoverE");
      bool veto = conf.getParameter<bool>("Veto_SingleTowerHoverE");
      themask += mask*kSingleTowerHoE;
      theveto += veto*kSingleTowerHoE;
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define SingleTowerHoverE requirement!";
    }

    // setup SigmaIEtaIEta masks and veto
    if( conf.existsAs<vdouble>("SigmaIEtaIEta") ) {
      vdouble theParams = conf.getParameter<vdouble>("SigmaIEtaIEta");
      setup.sihih_min_eb = theParams[0];
      setup.sihih_max_eb = theParams[1];
      
      setup.sihih_min_ee = theParams[2];
      setup.sihih_max_ee = theParams[3];
      
      bool mask = conf.getParameter<bool>("Mask_SigmaIEtaIEta");
      bool veto = conf.getParameter<bool>("Veto_SigmaIEtaIEta");
      themask += mask*kSihih;
      theveto += veto*kSihih;
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
      themask += mask*kPFChargedIso;
      theveto += veto*kPFChargedIso;
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
      themask += mask*kPFNeutralIso;
      theveto += veto*kPFNeutralIso;
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define PFNeutralIso requirement!";
    }

    // setup PFPhotonIso masks and veto
    if( conf.existsAs<vdouble>("PFPhotonIso") ) {
      vdouble theParams = conf.getParameter<vdouble>("PFPhotonIso");
      setup.pfPhotonIso_min_eb = theParams[0];
      setup.pfPhotonIso_max_eb = theParams[1];
      
      setup.pfPhotonIso_min_ee = theParams[2];
      setup.pfPhotonIso_max_ee = theParams[3];

      vdouble slopeParams = conf.getParameter<vdouble>("PFPhotonIsoPtSlope");
      setup.pfPhotonIso_pt_slope_eb = slopeParams[0];
      setup.pfPhotonIso_pt_slope_ee = slopeParams[1];
      
      bool mask = conf.getParameter<bool>("Mask_PFPhotonIso");
      bool veto = conf.getParameter<bool>("Veto_PFPhotonIso");
      themask += mask*kPFPhotonIso;
      theveto += veto*kPFPhotonIso;
    } else {
      throw cms::Exception("CutSet::CutSet()") 
	<< "Did not define PFPhotonIso requirement!";
    }
    
    _mask = (_passAll & ~themask);
    _veto = (_passAll & ~theveto);
    _theid = setup;
    
  } // CutSet::CutSet()
  
  bool CutSet::operator() (const pat::Photon& thePho,
			   const unsigned mask) const {
    unsigned eval = 0x0;
    
    // PUT EACH CUT INSIDE { } SO THAT VARIABLES DESCOPE AND 
    // YOU DON'T FUCK UP AND MAKE A BUG
    { 
      // ElectronVeto    
      bool passesVeto = ((bool)thePho.userInt("ConvSafeElectronVeto") 
			 == _theid.electronVeto);
      eval += passesVeto*kElectronVeto;
    }

    {
      //SingleTowerHoverE
      bool passesHoE = false;
      if( fabs(thePho.superCluster()->eta()) < 1.5 ) { // EB
	passesHoE = 
	(thePho.userFloat("SingleTowerHoE") < _theid.singleTowerHoE_max_eb &&
	 thePho.userFloat("SingleTowerHoE") >= _theid.singleTowerHoE_min_eb);
      } else {
	passesHoE = 
	(thePho.userFloat("SingleTowerHoE") < _theid.singleTowerHoE_max_ee &&
	 thePho.userFloat("SingleTowerHoE") >= _theid.singleTowerHoE_min_ee);
      }
      eval += passesHoE*kSingleTowerHoE;
    }

    {
      //SigmaIEtaIEta
      bool passesSihih = false;
      if( fabs(thePho.superCluster()->eta()) < 1.5 ) { // EB
	passesSihih = (thePho.sigmaIetaIeta() < _theid.sihih_max_eb &&
		       thePho.sigmaIetaIeta() >= _theid.sihih_min_eb    );
      } else {
	passesSihih = (thePho.sigmaIetaIeta() < _theid.sihih_max_ee &&
		       thePho.sigmaIetaIeta() >= _theid.sihih_min_ee    );
      }
      eval += passesSihih*kSihih;
    }

    {
      //PFCharged Iso -- depends on kt6PFJetsRho, PhotonEA_pfchg
      bool passesPFChargedIso = false;
      double iso_shift = 0.0, the_min, the_max;

      if( fabs(thePho.superCluster()->eta()) < 1.5 ) {
	iso_shift = _theid.pfChargedIso_pt_slope_eb*thePho.pt();
	the_max   = _theid.pfChargedIso_max_eb;
	the_min   = _theid.pfChargedIso_min_eb;
      } else {
	iso_shift = _theid.pfChargedIso_pt_slope_ee*thePho.pt();
	the_max   = _theid.pfChargedIso_max_ee;
	the_min   = _theid.pfChargedIso_min_ee;
      }
      
      double ea_charged_iso = 
	std::max( thePho.userIsolation(pat::PfChargedHadronIso) - 
		  iso_shift - 
		  (thePho.userFloat("PhotonEA_pfchg")*
		   thePho.userFloat("kt6PFJetsRho")), 0.0 );      
      
      passesPFChargedIso = (ea_charged_iso < the_max &&
			    ea_charged_iso >= the_min    );
      
      eval += passesPFChargedIso*kPFChargedIso;
    }
    
    {
      //PFNeutral Iso -- depends on kt6PFJetsRho, PhotonEA_pfneut
      bool passesPFNeutralIso = false;
      double iso_shift = 0.0, the_min, the_max;

      if( fabs(thePho.superCluster()->eta()) < 1.5 ) {
	iso_shift = _theid.pfNeutralIso_pt_slope_eb*thePho.pt();
	the_max   = _theid.pfNeutralIso_max_eb;
	the_min   = _theid.pfNeutralIso_min_eb;
      } else {
	iso_shift = _theid.pfNeutralIso_pt_slope_ee*thePho.pt();
	the_max   = _theid.pfNeutralIso_max_ee;
	the_min   = _theid.pfNeutralIso_min_ee;
      }
      
      double ea_neutral_iso = 
	std::max( thePho.userIsolation(pat::PfNeutralHadronIso) - 
		  iso_shift - 
		  (thePho.userFloat("PhotonEA_pfneut")*
		   thePho.userFloat("kt6PFJetsRho")), 0.0 );

      passesPFNeutralIso = (ea_neutral_iso < the_max &&
			    ea_neutral_iso >= the_min    );
  
      eval += passesPFNeutralIso*kPFNeutralIso;
    }

    {
      //PFPhoton Iso -- depends on kt6PFJetsRho, PhotonEA_pfpho
      bool passesPFPhotonIso = false;
      double iso_shift = 0.0, the_min, the_max;

      if( fabs(thePho.superCluster()->eta()) < 1.5 ) {
	iso_shift = _theid.pfPhotonIso_pt_slope_eb*thePho.pt();
	the_max   = _theid.pfPhotonIso_max_eb;
	the_min   = _theid.pfPhotonIso_min_eb;
      } else {
	iso_shift = _theid.pfPhotonIso_pt_slope_ee*thePho.pt();
	the_max   = _theid.pfPhotonIso_max_ee;
	the_min   = _theid.pfPhotonIso_min_ee;
      }
      
      double ea_photon_iso = 
	std::max( thePho.userIsolation(pat::PfGammaIso) - 
		  iso_shift - 
		  (thePho.userFloat("PhotonEA_pfpho")*
		   thePho.userFloat("kt6PFJetsRho")), 0.0 );

      passesPFPhotonIso = (ea_photon_iso < the_max &&
			   ea_photon_iso >= the_min    );
      
      eval += passesPFPhotonIso*kPFPhotonIso;
    }
    
    // yeah various bitwise nots are annoying but it makes the 
    // math easier...
    unsigned mask_tot = ~(~_mask + ~(mask));
    unsigned pass     = _passAll & _veto & mask_tot;
    unsigned result   = eval     & mask_tot;
    
    /*
    std::cout << std::hex << mask_tot << ' ' << _mask 
	      << ' ' << mask << std::endl;
    std::cout << std::hex << pass << ' ' << _passAll << ' ' 
	      << _veto << ' ' << mask_tot << std::endl;
    std::cout << std::hex << eval << ' ' << mask_tot << std::endl;
    std::cout << std::hex << result << " == " << pass << std::endl;
    std::cout << std::dec;
    */

    return ( result == pass );
  }
  
  CutBasedPhotonID::CutBasedPhotonID( const PSet& conf ) {
    vstring ids = conf.getParameterNamesForType<PSet>();    
    vstring::const_iterator i = ids.begin();
    vstring::const_iterator e = ids.end();

    for( ; i != e; ++i) {
      //std::cout << "Constructing Photon ID: " << *i << std::endl;
      _passesID.insert(
		       std::make_pair(*i,CutSet(conf.getParameterSet(*i))));
    }
  }

  bool CutBasedPhotonID::operator() (const pat::Photon& pho, 
				     const std::string& thewp) {
    return _passesID[thewp](pho);
  }

}
