/*****************************************************************************
 * Since TEfficiency has the bad habit of crashing in the destructor method  *
 * here is a copy that overrides it to make it work.                         *
 * It also provides some new functions useful for plotting.                  *
 * Author: Mauro Verzetti (UZurich)                                          *
 * mverzett@cern.ch                                                          *
 *****************************************************************************/

#ifndef TEFFICIENCYBUGFIXED_H
#define TEFFICIENCYBUGFIXED_H

#include "TEfficiency.h"
#include "TH2.h"
#include "TF1.h"
#include "TBinomialEfficiencyFitter.h"
#include "TGraphAsymmErrors.h"
#include "TGraphErrors.h"

class TEfficiencyBugFixed : public TEfficiency {
public:
  enum axis{
    xaxis,
    yaxis
  };

  TEfficiencyBugFixed(): 
    TEfficiency(),
    current_fcn_(0),
    fitter_(0)
  {};   
  TEfficiencyBugFixed(const TH1& passed, const TH1& total): 
    TEfficiency(passed, total),
    current_fcn_(0),
    fitter_(0)
  {};
  TEfficiencyBugFixed(const char* name, const char* title, Int_t nbins,
		      const Double_t* xbins): 
    TEfficiency(name, title, nbins, xbins),
    current_fcn_(0),
    fitter_(0)
  {};
  TEfficiencyBugFixed(const char* name, const char* title, Int_t nbins, Double_t xlow,
		      Double_t xup): 
    TEfficiency(name, title, nbins, xlow, xup),
    current_fcn_(0),
    fitter_(0)
  {};
  TEfficiencyBugFixed(const char* name, const char* title, Int_t nbinsx,
		      Double_t xlow, Double_t xup, Int_t nbinsy, Double_t ylow,
		      Double_t yup): 
    TEfficiency(name, title, nbinsx, xlow, xup, nbinsy, ylow, yup),
    current_fcn_(0),
    fitter_(0)
  {};
  TEfficiencyBugFixed(const char* name, const char* title, Int_t nbinsx,
		      const Double_t* xbins, Int_t nbinsy, const Double_t* ybins): 
    TEfficiency( name, title, nbinsx, xbins, nbinsy, ybins),
    current_fcn_(0),
    fitter_(0)
  {};
  TEfficiencyBugFixed(const char* name, const char* title, Int_t nbinsx,
		      Double_t xlow, Double_t xup, Int_t nbinsy, Double_t ylow,
		      Double_t yup, Int_t nbinsz, Double_t zlow, Double_t zup): 
    TEfficiency( name, title, nbinsx, xlow, xup, nbinsy, ylow, yup, nbinsz, zlow, zup),
    current_fcn_(0),
    fitter_(0)
  {};
  TEfficiencyBugFixed(const char* name, const char* title, Int_t nbinsx,
		      const Double_t* xbins, Int_t nbinsy, const Double_t* ybins,
		      Int_t nbinsz, const Double_t* zbins): 
    TEfficiency( name, title, nbinsx, xbins, nbinsy, ybins, nbinsz, zbins),
    current_fcn_(0),
    fitter_(0)
  {};
  //TEfficiencyBugFixed(const TEfficiencyBugFixed& heff);
  ~TEfficiencyBugFixed();
      
  Int_t Fit(TF1* f1,Option_t* opt);
  TGraphAsymmErrors* Projection(axis axisMarker);
  TGraphErrors* ProjectFunction(axis axisMarker, TH2* fine_binned_histo = 0);

  void SetFunction(TF1* f1) {current_fcn_ = f1;}

private:
  ClassDef(TEfficiencyBugFixed, 1)

protected:
  TF1* current_fcn_;
  TBinomialEfficiencyFitter *fitter_;
};


#endif //#ifndef TEFFICIENCYBUGFIXED_H
