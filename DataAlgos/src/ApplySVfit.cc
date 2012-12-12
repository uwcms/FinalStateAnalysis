///////////
// imp of class SVfitCaller and member funtion getSVfitMass
// based on standalone SVfit instructions
// https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#SVFit_Christian_Lorenzo_Aram_Rog
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////


#include "DataFormats/Provenance/interface/EventID.h"
#include "FinalStateAnalysis/DataAlgos/interface/ApplySVfit.h"
#include "TauAnalysis/CandidateTools/interface/NSVfitStandaloneAlgorithm.h"
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include <iostream>
#include <iomanip>
#include <map>
#include <stdio.h>
#include <string>


namespace ApplySVfit {

  // cash a string containg 4-vecs and pdgIDs mapped to SVfit mass

  static std::map<std::string, double> SVFitCache;
  static edm::EventID lastSVfitEvent; // last processed event


  SVfitCaller::SVfitCaller(){}

  SVfitCaller::~SVfitCaller(){}

  double SVfitCaller::getSVfitMass( std::vector<MeasuredTauLepton> measuredTauLeptons,
      Vector measuredMET ,
      const TMatrixD& covMET ,
      unsigned int verbosity,
      const edm::EventID event_x
      ){


    ////////////
    // temp printouts

    std::cout<<" mlep1 "<<measuredTauLeptons[0].p4()<<std::endl;
    std::cout<<" mlep1 "<<measuredTauLeptons[0].decayType()<<std::endl;
    std::cout<<" mlep2 "<<measuredTauLeptons[1].p4()<<std::endl;
    std::cout<<" mlep2 "<<measuredTauLeptons[1].decayType()<<std::endl;
    std::cout<<" *** "<<event_x.event()<<std::endl;

    ///



    //////////////
    // clear the map if the event is new

    if(event_x != lastSVfitEvent)  SVFitCache.clear();

    double mass = -999;


    /////////////////////////////
    // form the string defining the current event
    // format is event#, decayType(0),decayType(1), tau_0(pt,eta,phi), tau_1(pt,eta,phi)
    // where 0 has the higher pt of the pair

    char hold_arguments_to_SVfit_char[1000];
    int order_i= 0;
    int order_j= 1;

    if(measuredTauLeptons[1].p4().pt()>measuredTauLeptons[0].p4().pt()) {order_i = 1; order_j = 0;}

    sprintf(hold_arguments_to_SVfit_char,"held_%i_%i_%i_%i_%i_%f_%f_%f_%f_%f_%f",event_x.run(),event_x.luminosityBlock(),
        event_x.event(),measuredTauLeptons[order_i].decayType(),measuredTauLeptons[order_j].decayType(),
        measuredTauLeptons[order_i].p4().pt(), measuredTauLeptons[order_i].p4().eta(),measuredTauLeptons[order_i].p4().phi(),
        measuredTauLeptons[order_j].p4().pt(), measuredTauLeptons[order_j].p4().eta(),measuredTauLeptons[order_j].p4().phi());

    std::string hold_arguments_to_SVfit = hold_arguments_to_SVfit_char;


    std::map <std::string, double>::iterator it;

    ///////////
    // loop over previously cached entries
    // and check for a string match
    // if a string match is found, set mass to the it->second

    /* temp output */  std::cout<<" currently testing "<<hold_arguments_to_SVfit<<std::endl;

    for (it = SVFitCache.begin(); it != SVFitCache.end(); ++it) {

      /* temp output */  std::cout<<it->first<<" "<<it->second<<std::endl;

      if(hold_arguments_to_SVfit.compare(it->first) == 0) {
        mass = it->second; std::cout<<" MATCH FOUND --> "<<mass<<" "<<std::endl; break;}

    } // SVFitCache iteration

    /////////////////////
    // if no match found
    // call SVfit as usual, and cache the result

    if(mass == -999){

      NSVfitStandaloneAlgorithm algo(measuredTauLeptons,measuredMET,covMET,verbosity);
      algo.addLogM(false);
      algo.integrate();
      mass = algo.getMass(); // mass uncertainty not implemented yet
      std::cout<<" Computed SVfit Mass as "<<mass<<std::endl;

      // cache it
      SVFitCache[hold_arguments_to_SVfit] = mass;

    } // new computation & cache


    //////////
    // reset the last event
    // and return

    lastSVfitEvent = event_x;
    return mass;


  } // getSVfitMass
} // namespace ApplySVfit

