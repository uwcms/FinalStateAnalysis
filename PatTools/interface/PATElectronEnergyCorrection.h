/** \class PATElectronEnergyCorrection
 *
 * Auxiliary class to encapsulate the prescription
 * for applying the regression-based electron energy
 * corrections.
 * Constructed by giving a list of datasets and
 * correction types defined in
 * https://twiki.cern.ch/twiki/bin/view/CMS/EgammaElectronEnergyScale.
 * The user may then apply any one of the given
 * corrections to an input electron.
 *
 * \author Lindsey Gray, UW Madison
 *
 *
 */

#ifndef __PATELECTRONENERGYCORRECTION_H__
#define __PATELECTRONENERGYCORRECTION_H__

#include <map>
#include <string>
#include <vector>
#include <memory>

//forward decls
class ElectronEnergyCalibrator;
class CaloTopology;
class CaloGeometry;
class ElectronEnergyRegressionEvaluate;
#include "DataFormats/PatCandidates/interface/Electron.h"
namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class InputTag;
  template<typename T> class ESHandle;
}


namespace pattools {

  class PATElectronEnergyCorrection {
  public:
    typedef ElectronEnergyRegressionEvaluate regCalc;
    typedef regCalc* pRegCalc;
    typedef ElectronEnergyCalibrator eCalib;
    typedef eCalib* pCalib;
    typedef std::map<std::string,pCalib>      calib_map;
    typedef std::map<std::string,std::pair<int,pRegCalc> > reg_map;
    // calib : regression
    typedef std::map<std::string,std::string> apply_map;
    typedef std::auto_ptr<pat::Electron> value_type;

  private:
    const std::string _errPostfix;

    const CaloTopology* _topo;
    const CaloGeometry* _geom;
    const edm::Event* _event;
    const edm::EventSetup* _esetup;

    edm::InputTag _vtxsrc, _rhosrc;
    std::string _dataset, _userP4Prefix;
    double _smearRatio;
    bool _isSync;

    double _rho;
    int    _nvtx;

    edm::InputTag _recHitsEB,_recHitsEE;
    edm::Handle< EcalRecHitCollection > _recHitCollectionEE;
    edm::Handle< EcalRecHitCollection > _recHitCollectionEB;

    apply_map _apply;
    calib_map _calibs;
    reg_map   _regs;

  public:
    PATElectronEnergyCorrection(const edm::ParameterSet&,
				const bool isAOD,
				const bool isMC);
    ~PATElectronEnergyCorrection();

    value_type operator() (const pat::ElectronRef&);

    void setES(const edm::EventSetup& es);
    void setEvent(const edm::Event& ev);

  };

}

#endif
