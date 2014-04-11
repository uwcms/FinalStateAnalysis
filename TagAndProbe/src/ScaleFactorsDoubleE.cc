#include "FinalStateAnalysis/TagAndProbe/interface/ScaleFactorsDoubleE.h"
#include <cmath>
#include <iostream>
#include <assert.h>
using namespace std;

double Corr_Trg_Ele_2012_53X(double ept, double eeta) { 
  if(ept >= 10 && ept < 15){
    if (abs(eeta) < 0.8)                            return 0.9639;
    else if (0.8 <= abs(eeta) && abs(eeta) < 1.479) return 0.8898;
    else if (1.479 <= abs(eeta) )                   return 0.9228;
  }
  else if(ept >= 15 && ept < 20){
    if (abs(eeta) < 0.8)                            return 0.9762;
    else if (0.8 <= abs(eeta) && abs(eeta) < 1.479) return 0.9647;
    else if (1.479 <= abs(eeta) )                   return 0.9199;
  }
  else if(ept >= 20 && ept < 25){
    if (abs(eeta) < 0.8)                            return 0.9683;
    else if (0.8 <= abs(eeta) && abs(eeta) < 1.479) return 0.9666;
    else if (abs(eeta) >= 1.479 )                   return 0.9679;
  }
  else if(ept >= 25 && ept < 30){
    if (abs(eeta) < 0.8)                            return 0.9756;
    else if (0.8 <= abs(eeta) && abs(eeta) < 1.479) return 0.9896;
    else if (abs(eeta) >= 1.479 )                   return 0.9473;
  }
  else if(ept >= 30){
    if (abs(eeta) < 0.8)   		            return 1.0035;
    else if (abs(eeta) >= 0.8 && abs(eeta) < 1.479) return 0.9977;
    else if (abs(eeta) >= 1.479 )                   return 0.9885;
  }
  return 0.;
}

double Corr_Trg_Ele_2011(double ept, double eeta) {
  if(ept >= 10 && ept < 15){
    if (abs(eeta) < 1.479)  return 0.98;
    else                    return 0.97;
 }
  else if(ept >= 15 && ept < 20){
    if (abs(eeta) < 1.479) return 1.00;
    else                   return 1.05;
  }
  else if(ept >= 20 && ept < 30){
    if (abs(eeta) < 1.479) return 1.001;
    else                   return 1.00;
  }
  else if(ept > 30){
    if (abs(eeta) < 1.479) return 1.003;
    else                   return 1.008;
  }
  return 0.;
}

float Trg_DoubleEle_2011(double ept1, double eeta1, double ept2, double eeta2) {
    return Corr_Trg_Ele_2011(ept1, eeta1) * Corr_Trg_Ele_2011(ept2, eeta2);
}

float Trg_DoubleEle_2012(double ept1, double eeta1, double ept2, double eeta2) {
    return Corr_Trg_Ele_2012_53X(ept1, eeta1) * Corr_Trg_Ele_2012_53X(ept2, eeta2);
}
