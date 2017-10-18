/*****************************************************************************
 * Package: RooRarFit                                                        *
 *    File: $Id: RooCruijff.cc,v 1.1 2009/01/22 21:22:01 kukartse Exp $   *
 * Authors:                                                                  *
 *    Karsten Koeneke, Massachusetts Institute of Technology, Cambridge, USA *
 *    Vouter Hulbergen                                                       *
 *                                                                           *
 * Copyright (c) 2006, Massachsetts Institute of Technology, Cambridge, USA  *
 *****************************************************************************/

// This is an implementation for the Cruijff function for RooFit

#include <iostream>
#include <math.h>

#include "FinalStateAnalysis/StatTools/interface/RooCruijff.h"
#include "RooRealVar.h"
#include "RooRealConstant.h"

ClassImp(RooCruijff)

RooCruijff::RooCruijff(const char *name, const char *title,
		       RooAbsReal& _x, RooAbsReal& _m0, 
		       RooAbsReal& _sigmaL, RooAbsReal& _sigmaR,
		       RooAbsReal& _alphaL, RooAbsReal& _alphaR)
  :
  RooAbsPdf(name, title),
  x("x", "x", this, _x),
  m0("m0", "m0", this, _m0),
  sigmaL("sigmaL", "sigmaL", this, _sigmaL),
  sigmaR("sigmaR", "sigmaR", this, _sigmaR),
  alphaL("alphaL", "alphaL", this, _alphaL),
  alphaR("alphaR", "alphaR", this, _alphaR)
{
}

RooCruijff::RooCruijff(const RooCruijff& other, const char* name) :
  RooAbsPdf(other, name), 
  x("x", this, other.x), 
  m0("m0", this, other.m0),
  sigmaL("sigmaL", this, other.sigmaL), 
  sigmaR("sigmaR", this, other.sigmaR), 
  alphaL("alphaL", this, other.alphaL), 
  alphaR("alphaR", this, other.alphaR)
{
}

// Double_t RooCruijff::getValV(const RooArgSet* set) const
// {
//   return evaluate();
// }

Double_t RooCruijff::evaluate() const 
{
  // build the functional form
  double sigma = 0.0;
  double alpha = 0.0;
  double dx = (x - m0);
  if(dx<0){
    sigma = sigmaL;
    alpha = alphaL;
  } else {
    sigma = sigmaR;
    alpha = alphaR;
  }
  double f = 2*sigma*sigma + alpha*dx*dx ;
  return exp(-dx*dx/f) ;
}
