#include "FinalStateAnalysis/TagAndProbe/interface/ScaleFactorsDoubleMu.h"
#include <cmath>
#include <iostream>
#include <assert.h>
using namespace std;

double Corr_Trg_Mu_2012_53X(double mupt, double mueta) {
  if(mupt >= 10 && mupt < 15){
    if (abs(mueta) < 0.8)                           return 0.9818;
    else if (0.8 <= abs(mueta) && abs(mueta) < 1.2) return 0.9713;
    else if (1.2 <= abs(mueta))                     return 0.9675;
  }
  else if(mupt >= 15 && mupt < 20){
    if (abs(mueta) < 0.8)                           return 0.9781;
    else if (0.8 <= abs(mueta) && abs(mueta) < 1.2) return 0.9782;
    else if (1.2 <= abs(mueta) )                    return 0.9587;
  }
  else if(mupt >= 20 && mupt < 25){
    if (abs(mueta) < 0.8)                           return 0.9873;
    else if (0.8 <= abs(mueta) && abs(mueta) < 1.2) return 0.9532;
    else if (1.2 <= abs(mueta) )                    return 0.9605;
  }
  else if(mupt >= 25 && mupt < 30){
    if (abs(mueta) < 0.8)                           return 0.9755;
    else if (0.8 <= abs(mueta) && abs(mueta) < 1.2) return 0.9818;
    else if (1.2 <= abs(mueta) )                    return 0.9632;
  }
  else if(mupt >= 30){
    if (abs(mueta) < 0.8)                           return 0.9956;
    else if (0.8 <= abs(mueta) && abs(mueta) < 1.2) return 0.9644;
    else if (1.2 <= abs(mueta) )                    return 0.9530;
  }
  return 0.;
}

double Trg_DoubleMu_2012(double mupt1, double mueta1, double mupt2, double mueta2) {
    return Corr_Trg_Mu_2012_53X(mupt1, mueta1) * Corr_Trg_Mu_2012_53X(mupt2, mueta2);
}
