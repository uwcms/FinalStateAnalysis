/*****************************************************************************
 * Package: RooRarFit                                                        *
 *    File: $Id: RooCruijff.rdl,v 1.1 2009/01/22 21:22:01 kukartse Exp $   *
 * Authors:                                                                  *
 *    Karsten Koeneke, Massachusetts Institute of Technology, Cambridge, USA *
 *    Wouter Hulsbergen                                                       *
 *                                                                           *
 * Copyright (c) 2006, Massachsetts Institute of Technology, Cambridge, USA  *
 *****************************************************************************/

#ifndef ROO_CRUIJFF
#define ROO_CRUIJFF

#include "RooAbsPdf.h"
#include "RooRealProxy.h"

//using namespace roofit;
class RooRealVar;
class RooAbsReal;

class RooCruijff : public RooAbsPdf {
public:
  RooCruijff():RooAbsPdf(){}

  RooCruijff(const char *name, const char *title, 
	     RooAbsReal& _x,
	     RooAbsReal& _m0, 
	     RooAbsReal& _sigmaL, RooAbsReal& _sigmaR,
	     RooAbsReal& _alphaL, RooAbsReal& _alphaR);
  
  RooCruijff(const RooCruijff& other, const char* name = 0);

  virtual TObject* clone(const char* newname) const { 
    return new RooCruijff(*this,newname); }

  //Double_t getValV(const RooArgSet* set = 0) const;
  inline virtual ~RooCruijff() { }

protected:
  RooRealProxy x;
  RooRealProxy m0;
  RooRealProxy sigmaL;
  RooRealProxy sigmaR;
  RooRealProxy alphaL;
  RooRealProxy alphaR;

  Double_t evaluate() const;

private:
  ClassDef(RooCruijff,1)
};

#endif
