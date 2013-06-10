/*****************************************************************************
 * Since TEfficiency has the bad habit of crashing in the destructor method  *
 * here is a copy that overrides it to make it work.                         *
 * It also provides some new functions useful for plotting.                  *
 * Author: Mauro Verzetti (UZurich)                                          *
 * mverzett@cern.ch                                                          *
 *****************************************************************************/

#include "FinalStateAnalysis/StatTools/interface/TEfficiencyBugFixed.h"
#include "TList.h"
#include "TDirectory.h"
#include "TGraph2DErrors.h"
#include "TH2.h"
#include "TH1D.h"
#include "TBinomialEfficiencyFitter.h"
#include "TF1.h"
#include "TVirtualFitter.h"
#include <iostream>
#include <string>
#include <ctime>

ClassImp(TEfficiencyBugFixed)

Int_t TEfficiencyBugFixed::Fit(TF1* f1,Option_t* opt)
{
  //fits the efficiency using the TBinomialEfficiencyFitter class
  //
  //The resulting fit function is added to the list of associated functions.
  //
  //Options: - "+": previous fitted functions in the list are kept, by default
  //                all functions in the list are deleted
  //         - for more fitting options see TBinomialEfficiencyFitter::Fit
  TString option = opt;
  option.ToLower();

  //replace existing functions in list with same name
  Bool_t bDeleteOld = true;
  if(option.Contains("+")) {
    option.ReplaceAll("+","");
    bDeleteOld = false;
  }
  
  if(fitter_){
    delete fitter_;
  }
  fitter_ = new TBinomialEfficiencyFitter(fPassedHistogram,fTotalHistogram);
   
  Int_t result = fitter_->Fit(f1,option.Data());
  current_fcn_ = f1; //sets the current function to the this one, but DOES NOT OWN IT
   
  return result;
}

TEfficiencyBugFixed::~TEfficiencyBugFixed()
{
  //It might raise memory leak, but we don't care
  if(fitter_){
    delete fitter_;
  }
  
  //DO NOT DELETE THE FUNCTIONS

  /*if(fDirectory)
      fDirectory->Remove(this);
   
   delete fTotalHistogram;
   delete fPassedHistogram;
   delete fPaintGraph;
   delete fPaintHisto;*/
}

TGraphAsymmErrors* TEfficiencyBugFixed::Projection(axis axisMarker)
{
  //Unfortunately the projection of the effeciency is not the sum on each bin
  //But the sum of den and num and THEN you divide them
  TH2* h2pass = dynamic_cast<TH2*> (fPassedHistogram);
  TH2* h2tot  = dynamic_cast<TH2*> (fTotalHistogram) ;
  
  //check if casting went fine
  if (!(h2pass && h2tot)){
    return NULL;
  }

  TH1D *hpass, *htot = NULL;
  if( axisMarker == axis::xaxis ){
    hpass = h2pass->ProjectionX();
    htot  = h2tot->ProjectionX( );
  }
  else if( axisMarker == axis::yaxis ){
    hpass = h2pass->ProjectionY();
    htot  = h2tot->ProjectionY( );
  }
  else{
    return NULL;
  }

  return new TGraphAsymmErrors(hpass, htot);  
}

TGraphErrors* TEfficiencyBugFixed::ProjectFunction(axis axisMarker, TH2* fine_binned_histo)
{
  //Same here for the function, the projection is not the integral rather than the integral weighted
  //by the distribution of the denominator
  // eff(x) = Integral_y( eff(x,y)*TotalHistogram(x,y) ) / Integral_y( TotalHistogram(x,y) )

  //Get the denominator histogram
  TH2* h2tot  = dynamic_cast<TH2*> (fTotalHistogram) ;
  if (!(current_fcn_ && h2tot )){ //&& fitter_
      return NULL;
    }
  if(fine_binned_histo){
    std::cout << "replacing fTotalHistogram with user provided histogram" << std::endl;
    h2tot = fine_binned_histo;
  }

  //create the output graph
  TGraphErrors* ret = new TGraphErrors();

  //axes pointers
  TAxis *x_axis = h2tot->GetXaxis();
  TAxis *y_axis = h2tot->GetYaxis();
  TAxis *pojected_axis = (axisMarker == axis::xaxis) ? y_axis : x_axis;
  TAxis *shown_axis    = (axisMarker == axis::xaxis) ? x_axis : y_axis;

  //nbins
  int binsx = x_axis->GetNbins();
  int binsy = y_axis->GetNbins();

  //fill dummy TGraph
  TGraph2DErrors *fcn_quantized = new TGraph2DErrors();
  int counter = 0;
  for(int ix = 1; ix <= binsx; ix++ ){
    double x = x_axis->GetBinCenter(ix);
    for(int iy = 1; iy <= binsy; iy++ ){
      double y = y_axis->GetBinCenter(iy);
      fcn_quantized->SetPoint(counter, x, y, 0);
      counter++;
    }
  }

  //Get central value for computed function and its deviation
  //fitter_->GetFitter()->GetConfidenceIntervals(fcn_quantized);

  //Get all the graph points (having a struct called point seemed overshooting to the devs eh?
  // double *xs = fcn_quantized->GetX();
  // double *ys = fcn_quantized->GetY();
  // double *zs = fcn_quantized->GetZ();
  // double *ezs = fcn_quantized->GetEZ();

  
  counter = 0;
  for(int shown_bin = 1; shown_bin <= binsx; shown_bin++ ){
    double num = 0;
    double den = 0;
    double scenter = shown_axis->GetBinCenter(shown_bin); //shown bin center
    for(int proj_bin = 1; proj_bin <= binsy; proj_bin++ ){
      double pcenter = pojected_axis->GetBinCenter(proj_bin); //projected bin center
      double fcn_val = (axisMarker == axis::xaxis) ? current_fcn_->Eval(scenter, pcenter) : current_fcn_->Eval(pcenter, scenter);
      double bin_cont= (axisMarker == axis::xaxis) ? h2tot->GetBinContent(shown_bin, proj_bin) : h2tot->GetBinContent(proj_bin, shown_bin);
      num += fcn_val*bin_cont;
      den += bin_cont;
    }
    double val = (den > 0.) ? num/den : 0.;
    ret->SetPoint(counter, scenter, val);
    counter++;
  }
  
  delete fcn_quantized;
  return ret;
}
