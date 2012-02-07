#ifndef HorizontalMorphing_h
#define HorizontalMorphing_h

#include <map>
#include <string>
#include <fstream>
#include <iomanip>
#include <iostream>

#include <TH1.h>
#include <TFile.h>
#include <TROOT.h>
#include <TString.h>
#include <TSystem.h>
#include <Rtypes.h>

#include <TAxis.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TAttLine.h>
#include <TPaveText.h>

#include "FWCore/ParameterSet/interface/ParameterSet.h"


/**
   \class   HorizontalMorphing HorizontalMorphing.h "MitLimits/Higgs2TauLimits/interface/HorizontalMorphing.h"

   \author  Roger Wolf (MIT)

   Adapted from version 1.8 of http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/RWolf/MitLimits/Higgs2Tau/interface/?pathrev=MAIN
   by Evan Friis

   \brief   Helper class to facilitate horizontal template morphing

   This is a helper class to facilitate horizontal template morphing for Higgs2Tau analyses. It is expected to
   be called within a standalone executable or loaded to interactive root. The cfg file is expected to be of
   type:

   vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
   horizontalMorphing = cms.PSet(
    ## definde verbosity level
    inputFile  = cms.string("testFile.root"),
    ## input file
    directory  = cms.string("emu_X"),
    ##
    histName   = cms.string("Higgs_gf_sm_$MASS"),
    ##
    upperBound = cms.double(105),
    ##
    upperAccept= cms.double(0.15),
    ##
    lowerBound = cms.double(100),
    ##
    lowerAccept= cms.double(0.2),
    ## vector of event classes (bins)
    points = cms.VPSet(
        cms.PSet(mass = cms.double(101), norm = cms.double(1.)),
       ,cms.PSet(mass = cms.double(102), norm = cms.double(1.)),
       ,cms.PSet(mass = cms.double(103), norm = cms.double(1.)),
       ,cms.PSet(mass = cms.double(104), norm = cms.double(1.)),
        )
    )
   vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
*/

class HorizontalMorphing {
 public:
  /// default constructor
  HorizontalMorphing(const edm::ParameterSet& cfg);
  /// default destructor
  ~HorizontalMorphing();
  /// return the lower bound for the interpolation
  double lowerBound() const {return lowerBound_;};
  /// return the upper bound for the interpolation
  double upperBound() const {return upperBound_;};
  /// apply the interpolation
  TH1* interpolate(double value, double norm, const char* extension="");
  TH1* morph(const std::string&, const std::string&, TH1*, TH1*, double, double);
  /// do the interpolation for all intermediate values that are given in the
  /// python input file
  void process();

 private:
  /// refill histograms to make sure that they do not contain errors (in case
  /// these histograms are about to be used for further plotting)
  TH1* refill(TFile*, const std::string&, const std::string&);
  /// determine the number of digits after the '.' to get the histogram name
  /// right for the interpolated histogram. This only works for interpolations
  /// down to a 1/10th of a GeV
  unsigned int digits(double value, unsigned int digit=0){ return (value-(int)value==0) ? digit : digits(10*value, ++digit); }
  ///
  TString getHistName_full(const std::string& path, double value, const std::string& extension);
  /// return interpolated acceptance
  double accept(double value);

 private:
  /// input file; the same file is being extended with the new interpolated
  /// histograms
  std::string inputFileName_lowerBound_;
  std::string inputFileName_upperBound_;
  TFile* inputFile_lowerBound_;
  TFile* inputFile_upperBound_;
  std::string outputFileName_;
  /// mass points in the python config file, the index corresponds to the
  /// mass point, the value to the normalization for the given mass point
  std::map<double, double> points_;
  /// lower bound for the interpolation
  double lowerBound_;
  /// upper bound for the interpolation
  double upperBound_;
  /// acceptance lower bound for the interpolation
  double lowerAccept_;
  /// acceptance of upper bound for the interpolation
  double upperAccept_;
  /// path to the reference histograms to be horizontally morphed, w/o slash;
  /// this will be extended within the program
  std::string path_;
  /// name of the reference histograms to be horizontally morphed; expects a
  /// string of type Higgs_gf_sm_$MASS[_$UNCERT], where $MASS will be replaced
  /// by the interpolated mass value, _$UNCERT may be an additional extension
  /// to the histogram in question to apply the morphing to an arbitrary number
  /// of shape uncertainty histograms
  std::string histName_;
  std::string histName_output_;
};

#endif

