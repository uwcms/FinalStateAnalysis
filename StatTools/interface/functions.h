#include <math.h>

//namespace FSAStatFcn{
//Like the class but can be implemented in a RooFormulaVar
double RooCruijffFcn( double x, double m0, double sigmaL, double sigmaR, double alphaL, double alphaR){
  // build the functional form
  double sigma = 0.0;
  double alpha = 0.0;
  double dx = (x - m0);
  if( dx < 0 ){
    sigma = sigmaL;
    alpha = alphaL;
  } else {
    sigma = sigmaR;
    alpha = alphaR;
  }
  double f = 2*sigma*sigma + alpha*dx*dx ;
  return exp( -dx*dx / f );
}
//}
