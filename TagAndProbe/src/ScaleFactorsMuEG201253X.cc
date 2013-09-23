#include "FinalStateAnalysis/TagAndProbe/interface/ScaleFactorsMuEG201253X.h"
#include <cmath>
#include <iostream>
#include <assert.h>
using namespace std;

Double_t muTrigScale_MuEG_2012_53X(Double_t mupt, Double_t mueta)
{
  if( 10.0 < mupt && mupt <= 15.0 ){
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8)       return 0.9829; //0.9841;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 ) return 0.9745; //0.9742;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 ) return 0.9943; //0.9955;
    else if( 1.6 <= abs(mueta) )                     return 0.9158; //0.9151;
  }							          
  else if( 15.0 < mupt && mupt <= 20.0 ){		          
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )      return 0.9850; //0.9846;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 ) return 0.9852; //0.9834;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 ) return 0.9743; //0.9793;
    else if( 1.6 <= abs(mueta) )                     return 0.9333; //0.9257;
  }							          
  else if( 20.0 < mupt && mupt <= 25.0 ){		          
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )      return 0.9951; //0.9937;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 ) return 0.9610; //0.9594;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 ) return 0.9716; //0.9692;
    else if( 1.6 <= abs(mueta) )                     return 0.9459; //0.9438;
  }							          
  else if( 25.0 < mupt && mupt <= 30.0 ){		          
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )      return 0.9869; //0.9856;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 ) return 0.9779; //0.9818;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 ) return 0.9665; //0.9684;
    else if( 1.6 <= abs(mueta) )                     return 0.9501; //0.9642;
  }							          
  else if( 30.0 < mupt && mupt <= 35.0 ){		          
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )      return 0.9959; //0.9930;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 ) return 0.9881; //0.9800;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 ) return 0.9932; //0.9958;
    else if( 1.6 <= abs(mueta) )                     return 0.9391; //0.9428;
  }							          
  else{							          
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )      return 0.9986; //0.9991;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 ) return 0.9540; //0.9626;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 ) return 0.9549; //0.9611;
    else if( 1.6 <= abs(mueta) )                     return 0.9386; //0.9314;
  }
  return 0.;
}

Double_t eleTrigScale_MuEG_2012_53X(Double_t elept, Double_t eleeta)
{
  if( 10.0 < elept && elept <= 15.0 ){
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.9548; //0.9529;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.9015; //0.8858;
    else if( 1.5 <= abs(eleeta) )                      return 0.9017; //0.9259;
  }							            
  else if( 15.0 < elept && elept <= 20.0 ){		            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.9830; //0.9841;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.9672; //0.9699;
    else if( 1.5 <= abs(eleeta) )                      return 0.9463; //0.9286;
  }							            
  else if( 20.0 < elept && elept <= 25.0 ){		            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.9707; //0.9716;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.9731; //0.9702;
    else if( 1.5 <= abs(eleeta) )                      return 0.9691; //0.9726;
  }							            
  else if( 25.0 < elept && elept <= 30.0 ){		            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.9768; //0.9772;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.9870; //0.9916;
    else if( 1.5 <= abs(eleeta) )                      return 0.9727; //0.9609;
  }							            
  else if( 30.0 < elept && elept <= 35.0 ){		            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 1.0047; //1.0084;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.9891; //0.9900;
    else if( 1.5 <= abs(eleeta) )                      return 0.9858; //0.9817;
  }							            
  else{							            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 1.0063; //1.0069;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 1.0047; //1.0049;
    else if( 1.5 <= abs(eleeta) )                      return 1.0015; //0.9989;
  }
  return 0.;
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
  if( 10.0 < elept && elept <= 15.0 ){	
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.7654;  //  0.7570;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.7693;  //  0.7807;
    else if( 1.5 <= abs(eleeta) )                      return 0.5719;  //  0.6276;
  }							            
  else if( 15.0 < elept && elept <= 20.0 ){		            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.8394;  //  0.8437;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.8457;  //  0.8447;
    else if( 1.5 <= abs(eleeta) )                      return 0.7024;  //  0.7812;
  }							            
  else if( 20.0 < elept && elept <= 25.0 ){		            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.8772;  //  0.8817;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.8530;  //  0.8492;
    else if( 1.5 <= abs(eleeta) )                      return 0.7631;  //  0.8057;
  }							            
  else if( 25.0 < elept && elept <= 30.0 ){		            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.9006;  //  0.9069;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.8874;  //  0.8896;
    else if( 1.5 <= abs(eleeta) )                      return 0.8092;  //  1.0225;
  }							            
  else if( 30.0 < elept && elept <= 35.0){		            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.9261;  //  0.9301;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.9199;  //  0.9230;
    else if( 1.5 <= abs(eleeta) )                      return 0.8469;  //  0.8887;
  }							            
  else{							            
    if( 0.0 <= abs(eleeta) && abs(eleeta) < 0.8 )      return 0.9514;  //  0.9533;
    else if( 0.8 <= abs(eleeta) && abs(eleeta) < 1.5 ) return 0.9445;  //  0.9496;
    else if( 1.5 <= abs(eleeta) )                      return 0.9078;  //  0.9389;
  }
  return  0.;

}

Double_t muIDscale_MuEG_2012_53X(Double_t mupt, Double_t mueta)
{
  if( 10.0 < mupt && mupt <= 15.0 ){
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )       return 0.9771;  // 0.9811;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 )  return 0.9746;  // 0.9689;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 )  return 0.9644;  // 0.9757;
    else if( 1.6 <= abs(mueta) )                      return 0.9891;  // 1.0069;
  }							           
  else if( 15.0 < mupt && mupt <= 20.0 ) {		           
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )       return 0.9548;  // 0.9556;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 )  return 0.9701;  // 0.9635;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 )  return 0.9766;  // 0.9806;
    else if( 1.6 <= abs(mueta) )                      return 0.9892;  // 1.0078;
  }							           
  else if( 20.0 < mupt && mupt <= 25.0 ) {		           
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )       return 0.9648;  // 0.9676;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 )  return 0.9836;  // 0.9785;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 )  return 0.9820;  // 0.9883;
    else if( 1.6 <= abs(mueta) )                      return 0.9909;  // 1.0031;
  }							           
  else if( 25.0 < mupt && mupt <= 30.0 ) {		           
    if ( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )      return 0.9676;  // 0.9691;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 )  return 0.9817;  // 0.9785;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 )  return 0.9886;  // 0.9909;
    else if( 1.6 <= abs(mueta) )                      return 0.9883;  // 0.9991;
  }							           
  else if( 30.0 < mupt && mupt <= 35.0 ) {		           
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )       return 0.9730;  // 0.9746;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 )  return 0.9833;  // 0.9797;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 )  return 0.9910;  // 0.9935;
    else if( 1.6 <= abs(mueta) )                      return 0.9900;  // 0.9987;
  }							           
  else{							           
    if( 0.0 <= abs(mueta) && abs(mueta) < 0.8 )       return 0.9826;  // 0.9841;
    else if( 0.8 <= abs(mueta) && abs(mueta) < 1.2 )  return 0.9841;  // 0.9813;
    else if( 1.2 <= abs(mueta) && abs(mueta) < 1.6 )  return 0.9900;  // 0.9919;
    else if( 1.6 <= abs(mueta) )                      return 0.9886;  // 0.9939;
  }
  return 0.;
}
