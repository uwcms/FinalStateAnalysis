#include "FinalStateAnalysis/PatTools/interface/PATElectronEnergyCorrection.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

#include "EgammaAnalysis/ElectronTools/interface/PatElectronEnergyCalibrator.h"
#include "EGamma/EGammaAnalysisTools/interface/ElectronEnergyRegressionEvaluate.h"

#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"

#include "EgammaAnalysis/ElectronTools/interface/SuperClusterHelper.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include <stdio.h>

namespace pattools { 

  namespace { // hide a bunch of convenient typedefs
    typedef edm::ParameterSet PSet;
    typedef edm::VParameterSet VPSet;
        
    typedef std::auto_ptr<pat::Electron> pelectron;
    typedef std::vector<pelectron> vpelectron;
    typedef pat::ElectronRef eRef;
    
    typedef edm::ESHandle<CaloTopology> topo_hdl;
    typedef edm::ESHandle<CaloGeometry> geom_hdl;

    typedef std::vector<std::string> vstring;
  }

  PATElectronEnergyCorrection::PATElectronEnergyCorrection(const PSet& conf,
							   const bool isAOD,
							   const bool isMC):
    _errPostfix("_error") {
    
    _userP4Prefix = conf.getParameter<std::string>("userP4Prefix");

    _vtxsrc = conf.getParameter<edm::InputTag>("vtxSrc");
    _rhosrc = conf.getParameter<edm::InputTag>("rhoSrc");

    _recHitsEB = conf.getParameter<edm::InputTag>("recHitsEB");
    _recHitsEE = conf.getParameter<edm::InputTag>("recHitsEE");    
    
    // setup regression pool
    VPSet available_regressions = 
      conf.getParameterSetVector("available_regressions");
    
    { // make iterators descope
      VPSet::const_iterator i = available_regressions.begin();
      VPSet::const_iterator e = available_regressions.end();
      
      for( ; i != e; ++i) {
	std::string type     = i->getParameter<std::string>("type");
	std::string fWeights = i->getParameter<std::string>("weightsFile");
	int version          = i->getParameter<int>("version");
	int index            = i->getParameter<int>("index");

	if( index >= 0 ) {
	  _regs[type] = std::make_pair(version,new regCalc());
	  _regs[type].second->initialize(fWeights,
				(regCalc::ElectronEnergyRegressionType)index);
	  if( _regs[type].second->isInitialized() ) 
	    std::cout << type << " is init!" << std::endl;
	}	
	else {
	  _regs[type] = std::make_pair(-1,new regCalc());
	  // compiler yells at me if I try to instantiate to NULL
	  delete _regs[type].second;
	  _regs[type].second = NULL;
	}
	
      }
    }
    
    // setup calibration pool
    VPSet available_calibrations = 
      conf.getParameterSetVector("available_calibrations");  
    // get applied calibrations
    vstring applyCalibrations = 
      conf.getParameter<vstring>("applyCalibrations");
    _dataset = conf.getParameter<std::string>("dataSet");
    
    { // make iterators descope
      VPSet::const_iterator i = available_calibrations.begin();
      VPSet::const_iterator e = available_calibrations.end();

      vstring::const_iterator iapp = applyCalibrations.begin();
      vstring::const_iterator eapp = applyCalibrations.end();

      for( ; i != e; ++i) {
	std::string type     = i->getParameter<std::string>("type");
	std::string regType  = i->getParameter<std::string>("regression");
	int applyCorrections = i->getParameter<int>("applyCorrections");

	if( applyCorrections >= 0 ) {
	  _calibs[type] = 
	    new eCalib(_dataset,isAOD,isMC,true,applyCorrections,false);
	  if( std::find(iapp,eapp,type) != eapp)
	    _apply[type] = regType;
	}	
	else 
	  _calibs[type] = NULL;
      }      
    }    
    
  }
 
  PATElectronEnergyCorrection::~PATElectronEnergyCorrection() {
    calib_map::iterator i = _calibs.begin();
    calib_map::iterator e = _calibs.end();
    for(; i != e; ++i) 
      if(i->second) 
	delete i->second;

    reg_map::iterator ii = _regs.begin();
    reg_map::iterator ee = _regs.end();
    for(; ii != ee; ++ii) 
      if(ii->second.second)
	delete ii->second.second;
  }

  PATElectronEnergyCorrection::value_type
  PATElectronEnergyCorrection::operator() (const eRef& ele) {    
    value_type out = value_type(new value_type::element_type(*ele));

    apply_map::const_iterator app = _apply.begin();
    apply_map::const_iterator end = _apply.end();

    EcalClusterLazyTools clustools(*_event,*_esetup,
				   _recHitsEB,_recHitsEE);

    
    for( ; app != end; ++app ) {
      value_type temp = value_type(new value_type::element_type(*ele));

      reg_map::mapped_type thisReg = _regs[app->second];
      if( thisReg.second ) {
	double en =
	  thisReg.second->calculateRegressionEnergy(temp.get(),clustools,
						    *_esetup,_rho,_nvtx);
	double en_err =
	  thisReg.second->calculateRegressionEnergyUncertainty(temp.get(),
							       clustools,
							       *_esetup,
							       _rho,_nvtx);

	math::XYZTLorentzVector oldP4,newP4;
	// recalculate then propagate the regression energy and errors
	switch( thisReg.first ) {
	case 1: // V1 regression (just ecal energy)	  
	  temp->correctEcalEnergy(en,en_err);
	  break;
	case 2: // V2 regression (including track variables)
	  oldP4 = temp->p4();
	  newP4 = math::XYZTLorentzVector(oldP4.x()*en/oldP4.t(),
					  oldP4.y()*en/oldP4.t(),
					  oldP4.z()*en/oldP4.t(),
					  en);
	  temp->correctEcalEnergy(en,en_err);
	  temp->correctMomentum(newP4,temp->trackMomentumError(),en_err);
	  break;
	default:
	  break;
	}
      }

      pCalib thisCalib = _calibs[app->first];
      if( thisCalib && temp->core()->ecalDrivenSeed() )
	thisCalib->correct(*(temp.get()),*_event,*_esetup);

      out->addUserData<math::XYZTLorentzVector>(_userP4Prefix+
						_dataset+app->first,
				 temp->p4(reco::GsfElectron::P4_COMBINATION));
      out->addUserFloat(_userP4Prefix+
			_dataset+app->first+
			_errPostfix,
			temp->p4Error(reco::GsfElectron::P4_COMBINATION));
      
    }

    return out;
  }  

  void PATElectronEnergyCorrection::setES(const edm::EventSetup& es) { 
    _esetup = &es; 
    
    edm::ESHandle<CaloTopology> topo;
    _esetup->get<CaloTopologyRecord>().get(topo);

    edm::ESHandle<CaloGeometry> geom;
    _esetup->get<CaloGeometryRecord>().get(geom);

    _topo = topo.product();
    _geom = geom.product();
  }

  void PATElectronEnergyCorrection::setEvent(const edm::Event& ev) { 
    _event  = &ev;

    edm::Handle<double> rho;
    _event->getByLabel(_rhosrc,rho);
    _rho = *rho;

    edm::Handle<reco::VertexCollection> vtxs;
    _event->getByLabel(_vtxsrc,vtxs);
    _nvtx = vtxs->size();
  }  
}
