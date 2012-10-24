#include "FinalStateAnalysis/PatTools/interface/PATElectronEnergyCorrection.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

#include "EgammaAnalysis/ElectronTools/interface/PatElectronEnergyCalibrator.h"
#include "EgammaAnalysis/ElectronTools/interface/SuperClusterHelper.h"

//#include "EGamma/StandAloneCorrections/interface/LeptonScaleCorrections.hh"

#include "FWCore/Framework/interface/ESHandle.h"
#include <stdio.h>

namespace pattools { 

  namespace { // hide a bunch of convenient typedefs
    typedef PATElectronEnergyCorrection::key_type key_type_eec;
    typedef std::vector<key_type_eec> vkey_type_eec;
    typedef std::auto_ptr<pat::Electron> pelectron;
    typedef pat::ElectronRef eRef;
    
    typedef edm::ESHandle<CaloTopology> topo_hdl;
    typedef edm::ESHandle<CaloGeometry> geom_hdl;
  }

  PATElectronEnergyCorrection::PATElectronEnergyCorrection(const vkey_type_eec&
							   init_list,
							   const bool isAOD,
							   const bool isMC) {
    vkey_type_eec::const_iterator i = init_list.begin();
    vkey_type_eec::const_iterator e = init_list.end();    
    for( ; i != e; ++i) {
      _corrs[formIdent(*i)] = new eCalib(i->first,isAOD,
					 isMC,true,
					 i->second,false);
    }
  }
 
  PATElectronEnergyCorrection::~PATElectronEnergyCorrection() {
    map_type::iterator i = _corrs.begin();
    map_type::iterator e = _corrs.end();
    for(; i != e; ++i) delete i->second;
  }

  pelectron 
  PATElectronEnergyCorrection::operator() (const key_type_eec& key,
					   const eRef& ele) {    
    pelectron out(new pelectron::element_type(*ele));

    _corrs[formIdent(key)]->correct(*(out.get()),*_event,*_esetup);

    return out;
  }

  pelectron 
  PATElectronEnergyCorrection::operator() (const std::string& dset,
					   const int corrtype,
					   const eRef& ele) {
    return this->operator()(std::make_pair(dset,corrtype),ele);
  }

  void PATElectronEnergyCorrection::update_topo_geo(topo_hdl topo,
						    geom_hdl geom) {
    topo = topo.product();
    geom = geom.product();
  }

  vkey_type_eec 
  PATElectronEnergyCorrection::corrections() const {
    return vkey_type_eec();
  }

  // ethis is very very slow, but I'm sure 
  // everything else being run is slower...
  std::string 
  PATElectronEnergyCorrection::formIdent(const key_type_eec& key) const {
    char buf[50];
    memset(buf,0,50*sizeof(char));
    sprintf(buf,"%s_%i",key.first.c_str(),key.second);
    return std::string(buf);
  }

}
