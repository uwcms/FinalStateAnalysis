///////////
// imp of class SVfitCaller and member funtion getSVfitMass
// based on standalone SVfit instructions 
// https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#SVFit_Christian_Lorenzo_Aram_Rog
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////


#include "FinalStateAnalysis/DataAlgos/interface/ApplySVfit.h"
#include "TauAnalysis/CandidateTools/interface/NSVfitStandaloneAlgorithm.h"
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include <iostream>


namespace ApplySVfit {

	SVfitCaller::SVfitCaller(){}

	SVfitCaller::~SVfitCaller(){}

        double SVfitCaller::getSVfitMass( std::vector<MeasuredTauLepton> measuredTauLeptons,
                                Vector measuredMET , 
                                const TMatrixD& covMET , 
                                unsigned int verbosity
			       ){

   double mass = 0; 

   NSVfitStandaloneAlgorithm algo(measuredTauLeptons,measuredMET,covMET,verbosity);
   algo.addLogM(false);
   algo.integrate();
   mass = algo.getMass(); // mass uncertainty not implemented yet
   std::cout<<" SVfit Mass is "<<mass<<std::endl;

   return mass;	
		     } // getSVfitMass


} // namespace ApplySVfit

