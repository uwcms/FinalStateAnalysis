#include "FinalStateAnalysis/PatTools/interface/PATElectronEACalculator.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "EgammaAnalysis/ElectronTools/interface/ElectronEffectiveArea.h"

namespace pattools {

  namespace {
    typedef ElectronEffectiveArea eea;
    typedef edm::ParameterSet PSet;
    typedef edm::VParameterSet VPSet;
    typedef std::vector<double> vdouble;

    typedef ElectronEffectiveArea::ElectronEffectiveAreaType EATYPE;
    typedef ElectronEffectiveArea::ElectronEffectiveAreaTarget EATARGET;
  }

  PATElectronEACalculator::PATElectronEACalculator(const VPSet& areas){
    VPSet::const_iterator i = areas.begin();
    VPSet::const_iterator e = areas.end();

    for( ; i != e; ++i) {
      std::string name = i->getParameter<std::string>("name");
      int ea_target    = i->getParameter<int>("ea_target");
      int ea_type      = i->getParameter<int>("ea_type");

      ea_info temp;
      temp.ea_target = ea_target;
      temp.ea_type   = ea_type;

      _eamap[name] = temp;
    }
  }

  double PATElectronEACalculator::operator() (const pat::Electron& ele) {
    if( _eatype == "" )
      throw cms::Exception("PATElectronEACalculator::()")
	<< "_eatype not set!\n";

    map_type::mapped_type ea = _eamap[_eatype];

    EATYPE   type   = (EATYPE)ea.ea_type;
    EATARGET target = (EATARGET)ea.ea_target;

    return eea::GetElectronEffectiveArea(type,
					 ele.superCluster()->eta(),
					 target);
  }

}
