#include "FinalStateAnalysis/TagAndProbe/interface/ScaleFactorsMuEG201253X.h"
#include <cmath>
#include <iostream>
#include <assert.h>
using namespace std;

Double_t muTrigScale_MuEG_2012_53X(Double_t mupt, Double_t mueta)
{
  //if((fabs(mueta) > 2.1) || (mupt < 10)) { cout << "mu kinematics out of range" << endl; assert(0); }
  if(mupt > 30) {
    if(fabs(mueta) < 0.8)        return 0.9956;
    else if(fabs(mueta) < 1.2)   return 0.9644;
    else                         return 0.9530;
  }
  else if(mupt > 25) {
    if(fabs(mueta) < 0.8)        return 0.9755;
    else if(fabs(mueta) < 1.2)   return 0.9818;
    else                         return 0.9632;
  }
  else if(mupt > 20) {
    if(fabs(mueta) < 0.8)        return 0.9873;
    else if(fabs(mueta) < 1.2)   return 0.9532;
    else                         return 0.9605;
  }
  else if(mupt > 15) {
    if(fabs(mueta) < 0.8)        return 0.9781;
    else if(fabs(mueta) < 1.2)   return 0.9782;
    else                         return 0.9587;
  }
  else {
    if(fabs(mueta) < 0.8)        return 0.9818;
    else if(fabs(mueta) < 1.2)   return 0.9713;
    else                         return 0.9675;
  }
}

Double_t eleTrigScale_MuEG_2012_53X(Double_t elept, Double_t eleeta)
{
  //if((fabs(eleeta) > 2.3) || (elept < 10)) { cout << "ele kinematics out of range" << endl; assert(0); }
  if(elept > 30) {
    if(fabs(eleeta) < 0.8)        return 1.0035;
    else if(fabs(eleeta) < 1.479) return 0.9977;
    else                          return 0.9885;
  }
  else if(elept > 25) {
    if(fabs(eleeta) < 0.8)        return 0.9756;
    else if(fabs(eleeta) < 1.479) return 0.9896;
    else                          return 0.9473;
  }
  else if(elept > 20) {
    if(fabs(eleeta) < 0.8)        return 0.9683;
    else if(fabs(eleeta) < 1.479) return 0.9666;
    else                          return 0.9679;
  }
  else if(elept > 15) {
    if(fabs(eleeta) < 0.8)        return 0.9762;
    else if(fabs(eleeta) < 1.479) return 0.9647;
    else                          return 0.9199;
  }
  else {
    if(fabs(eleeta) < 0.8)        return 0.9639;
    else if(fabs(eleeta) < 1.479) return 0.8898;
    else                          return 0.9228;
  }
}

Double_t muTrigEff_MuEG_2012_53X(Double_t mupt, Double_t mueta)
{
  //if((fabs(mueta) > 2.1) || (mupt < 10)) { cout << "mu kinematics out of range" << endl; assert(0); }
  if(mupt > 30) {
    if(fabs(mueta) < 0.8)        return 0.9704;
    else if(fabs(mueta) < 1.2)   return 0.9326;
    else                         return 0.9114;
  }
  else if(mupt > 25) {
    if(fabs(mueta) < 0.8)        return 0.9650;
    else if(fabs(mueta) < 1.2)   return 0.9492;
    else                         return 0.9046;
  }
  else if(mupt > 20) {
    if(fabs(mueta) < 0.8)        return 0.9758;
    else if(fabs(mueta) < 1.2)   return 0.9460;
    else                         return 0.9284;
  }
  else if(mupt > 15) {
    if(fabs(mueta) < 0.8)        return 0.9659;
    else if(fabs(mueta) < 1.2)   return 0.9298;
    else                         return 0.9164;
  }
  else {
    if(fabs(mueta) < 0.8)        return 0.9693;
    else if(fabs(mueta) < 1.2)   return 0.9411;
    else                         return 0.9069;
  }
}

Double_t eleTrigEff_MuEG_2012_53X(Double_t elept, Double_t eleeta)
{
  //if((fabs(eleeta) > 2.3) || (elept < 10)) { cout << "ele kinematics out of range" << endl; assert(0); }
  if(elept > 30) {
    if(fabs(eleeta) < 0.8)        return 0.9643;
    else if(fabs(eleeta) < 1.479) return 0.9778;
    else                          return 0.9737;
  }
  else if(elept > 25) {
    if(fabs(eleeta) < 0.8)        return 0.9394;
    else if(fabs(eleeta) < 1.479) return 0.9674;
    else                          return 0.9286;
  }
  else if(elept > 20) {
    if(fabs(eleeta) < 0.8)        return 0.9200;
    else if(fabs(eleeta) < 1.479) return 0.9515;
    else                          return 0.9323;
  }
  else if(elept > 15) {
    if(fabs(eleeta) < 0.8)        return 0.8874;
    else if(fabs(eleeta) < 1.479) return 0.9177;
    else                          return 0.8500;
  }
  else {
    if(fabs(eleeta) < 0.8)        return 0.7633;
    else if(fabs(eleeta) < 1.479) return 0.7356;
    else                          return 0.7010;
  }
}


Double_t eleIDscale_MuEG_2012_53X(Double_t elept, Double_t eleeta)
{
  if(elept > 20) {
    if(fabs(eleeta) < 0.8)        return 0.9534;
    else if(fabs(eleeta) < 1.479) return 0.9481;
    else                          return 0.9378;
  }
  else if(elept > 15) {
    if(fabs(eleeta) < 0.8)        return 0.8506;
    else if(fabs(eleeta) < 1.479) return 0.8661;
    else                          return 0.7816;
  }
  else {
    if(fabs(eleeta) < 0.8)        return 0.7893;
    else if(fabs(eleeta) < 1.479) return 0.7952;
    else                          return 0.6519;
  }
}

Double_t muIDscale_MuEG_2012_53X(Double_t mupt, Double_t mueta)
{
  if(mupt > 20) {
    if(fabs(mueta) < 0.8)   return 0.9884;
    else if(fabs(mueta) < 1.2)   return 0.9884;
    else                    return 0.9941;
  }
  else if(mupt > 15) {
    if(fabs(mueta) < 0.8)   return 0.9644;
    else if(fabs(mueta) < 1.2)   return 0.9800;
    else                    return 0.9961;
  }
  else {
    if(fabs(mueta) < 0.8)   return 0.9845;
    else if(fabs(mueta) < 1.2)   return 0.9869;
    else                    return 0.9927;
  }
}
