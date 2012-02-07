#include "FinalStateAnalysis/StatTools/interface/HorizontalMorphing.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "HiggsAnalysis/CombinedLimit/src/th1fmorph.cc"
#include <assert.h>

// Adapted from version 1.7 at http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/RWolf/MitLimits/Higgs2Tau/interface/?pathrev=MAIN

HorizontalMorphing::HorizontalMorphing(const edm::ParameterSet& cfg):
  inputFile_lowerBound_(0),
  inputFile_upperBound_(0),
  lowerBound_ (cfg.getParameter<double>("lowerBound" )),
  upperBound_ (cfg.getParameter<double>("upperBound" )),
  lowerAccept_(cfg.getParameter<double>("lowerAccept")),
  upperAccept_(cfg.getParameter<double>("upperAccept")),
  histName_   (cfg.getParameter<std::string>("histName"))
{
  std::cout << "<horizontalMorphing>:" << std::endl;
  std::cout << " histName = " << histName_ << std::endl;
  std::cout << " lowerBound = " << lowerBound_ << ", upperBound = " << upperBound_ << std::endl;
  if ( cfg.exists("inputFile") ) {
    inputFileName_lowerBound_ = cfg.getParameter<std::string>("inputFile");
    inputFileName_upperBound_ = inputFileName_lowerBound_;
    outputFileName_ = ( cfg.exists("outputFile") ) ?
      cfg.getParameter<std::string>("outputFile") : "";
  } else {
    inputFileName_lowerBound_ = cfg.getParameter<std::string>("inputFile_lowerBound");
    inputFileName_upperBound_ = cfg.getParameter<std::string>("inputFile_upperBound");
    outputFileName_ = cfg.getParameter<std::string>("outputFile");
  }
  if ( outputFileName_ != "" && outputFileName_ != inputFileName_lowerBound_ && outputFileName_ != inputFileName_upperBound_ )
    inputFile_lowerBound_ = new TFile(inputFileName_lowerBound_.c_str(), "READ");
  else if ( outputFileName_ == inputFileName_lowerBound_ && outputFileName_ == inputFileName_upperBound_ )
    inputFile_lowerBound_ = new TFile(inputFileName_lowerBound_.c_str(), "UPDATE");
  else
    throw cms::Exception("HorizontalMorphing")
      << "Must specify outputFile in case separate inputFiles are used for lower and upper bounds !!\n";
  if ( !inputFile_lowerBound_ )
    throw cms::Exception("HorizontalMorphing")
      << "Failed to open inputFile = " << inputFileName_lowerBound_ << " !!\n";
  if ( inputFileName_upperBound_ != inputFileName_lowerBound_ )
    inputFile_upperBound_ = new TFile(inputFileName_upperBound_.c_str(), "READ");
  else
    inputFile_upperBound_ = inputFile_lowerBound_;
  if ( !inputFile_upperBound_ )
    throw cms::Exception("HorizontalMorphing")
      << "Failed to open inputFile = " << inputFileName_upperBound_ << " !!\n";
  path_ = cfg.getParameter<std::string>("directory");
  histName_output_ = ( cfg.exists("histName_output") ) ?
    cfg.getParameter<std::string>("histName_output") : "";
  std::vector<edm::ParameterSet> buffer = cfg.getParameter<std::vector<edm::ParameterSet> >("points");
  for(std::vector<edm::ParameterSet>::const_iterator point = buffer.begin(); point != buffer.end(); ++point){
    double mass = point->getParameter<double>("mass");
    double norm = point->getParameter<double>("norm");
    std::cout << " requested mass-point = " << mass << ": norm = " << norm << std::endl;
    points_[mass] = norm;
  }
  std::cout << "writing output to file = " << outputFileName_ << std::endl;
}

HorizontalMorphing::~HorizontalMorphing()
{
  delete inputFile_lowerBound_;
  if ( inputFile_upperBound_ != inputFile_lowerBound_ ) delete inputFile_upperBound_;
}

TH1*
HorizontalMorphing::refill(TFile* inputFile, const std::string& histName, const std::string& histName_suffix)
{
  TH1* hin = dynamic_cast<TH1*>(inputFile->Get(histName.data()));
  if ( !hin )
    throw cms::Exception("HorizontalMorphing")
      << "Failed to load histogram = " << histName << " from inputFile = " << inputFile->GetName() << " !!\n";
  TH1* hout = (TH1*)hin->Clone(std::string(histName).append(histName_suffix).data());
  hout->Clear();
  for(int i=0; i<hout->GetNbinsX(); ++i){
    hout->SetBinContent(i+1, hin->GetBinContent(i+1));
    hout->SetBinError  (i+1, 0.);
  }
  return hout;
}

double
HorizontalMorphing::accept(double value){
  if ( upperBound_ == lowerBound_ ) return 0.5*(lowerAccept_+upperAccept_);
  double intercept = (upperAccept_-lowerAccept_)/(upperBound_-lowerBound_);
  return lowerAccept_+intercept*(value-lowerBound_);
}

TString
HorizontalMorphing::getHistName_full(const std::string& path, double value, const std::string& extension)
{
  TString histName_full = path.data();
  if ( histName_full.Length() > 0 && !histName_full.EndsWith("/") ) histName_full.Append("/");
  histName_full.Append(histName_.data());
  TString format_specifier = TString("%2.").Append(TString::Format("%u", digits(value))).Append("f");
  TString value_string = TString::Format(format_specifier.Data(), value);
  histName_full = histName_full.ReplaceAll("$MASS", value_string);
  if ( extension != "" ) histName_full.Append(extension.data());
  return histName_full;
}

TH1*
HorizontalMorphing::interpolate(double value, double norm, const char* extension)
{
  TH1* hout=0;
  if(lowerBound_<=value && value<=upperBound_){
    TString histName_lowerBound = getHistName_full(path_, lowerBound_, extension);
    TH1* lower = refill(inputFile_lowerBound_, histName_lowerBound.Data(), "_lower");
    TString histName_upperBound = getHistName_full(path_, upperBound_, extension);
    TH1* upper = refill(inputFile_upperBound_, histName_upperBound.Data(), "_upper");
    TString histName_morphed;
    if ( histName_output_ != "" ) {
      histName_morphed = histName_output_.data();
    } else {
      histName_morphed = getHistName_full("", value, extension);
    }
    std::cout << " histName_morphed = " << histName_morphed.Data() << std::endl;
    TString histName_morphed_full = path_.data();
    if ( histName_morphed_full.Length() > 0 && !histName_morphed_full.EndsWith("/") ) histName_morphed_full.Append("/");
    histName_morphed_full.Append(histName_morphed.Data());
    if ( outputFileName_ == inputFileName_lowerBound_ && outputFileName_ == inputFileName_upperBound_ ) {
      TH1* morphed = dynamic_cast<TH1*>(inputFile_lowerBound_->Get(histName_morphed_full.Data()));
      if ( morphed ) {
	std::cout << "interpolated hist name: " << morphed->GetName() << " does already exist --> skipping." << std::endl;
	return morphed;
      }
    }
    if      ( value == lowerBound_ ) hout = (TH1*)lower->Clone(histName_morphed.Data());
    else if ( value == upperBound_ ) hout = (TH1*)upper->Clone(histName_morphed.Data());
    else if ( lower == upper       ) hout = (TH1*)lower->Clone(histName_morphed.Data());
    else {
      if(!std::string(extension).empty()){
	//std::cout << "shift" << std::endl;
	if(path_=="emu_vbf" && std::string(extension).find("Up")!=std::string::npos){
	  hout = morph(histName_morphed.Data(), histName_morphed.Data(), lower, upper, value, 1.04*norm*accept(value));
	  std::cout << "interpolated hist name: " << hout->GetName() << " || normalization: " << 1.04*norm*accept(value) << std::endl;
	} else if(path_=="emu_vbf" && std::string(extension).find("Down")!=std::string::npos){
	  hout = morph(histName_morphed.Data(), histName_morphed.Data(), lower, upper, value, 0.96*norm*accept(value));
	  std::cout << "interpolated hist name: " << hout->GetName() << " || normalization: " << 0.96*norm*accept(value) << std::endl;
	} else {
	  hout = morph(histName_morphed.Data(), histName_morphed.Data(), lower, upper, value, norm*accept(value));
	  std::cout << "interpolated hist name: " << hout->GetName() << " || normalization: " << 0.96*norm*accept(value) << std::endl;
	}
      } else {
      //std::cout << "no shift" << std::endl;
	double norm_morph = norm*accept(value);
	if ( norm <= 0. ) {
	  // CV: Compute integral **excluding** underflow and overflow bins.
	  //     Since HiggsAnalysis/CombinedLimit/src/th1fmorph.cc does not support underflow and overflow bins,
	  //     event statistics gets lost otherwise.
	  //double norm_lower = lower->Integral(0, lower->GetNbinsX() + 1);
	  //double norm_upper = upper->Integral(0, upper->GetNbinsX() + 1);
	  double norm_lower = lower->Integral(1, lower->GetNbinsX());
	  double norm_upper = upper->Integral(1, upper->GetNbinsX());
	  double slope = (norm_upper - norm_lower)/(upperBound_ - lowerBound_);
	  norm_morph = norm_lower + slope*(value - lowerBound_);
	}
	hout = morph(histName_morphed.Data(), histName_morphed.Data(), lower, upper, value, norm_morph);
	std::cout << "interpolated hist name: " << hout->GetName() << " || normalization: " << norm_morph << std::endl;
      }
    }
    delete lower;
    delete upper;
  }
  return hout;
}

TH1*
HorizontalMorphing::morph(const std::string& histName, const std::string& histTitle, TH1* lower, TH1* upper, double value, double norm)
{
  if ( dynamic_cast<TH1F*>(lower) && dynamic_cast<TH1F*>(upper) ) {
    TH1F* lower_th1f = dynamic_cast<TH1F*>(lower);
    TH1F* upper_th1f = dynamic_cast<TH1F*>(upper);
    return th1fmorph(histName.data(), histTitle.data(), lower_th1f, upper_th1f, lowerBound_, upperBound_, value, norm);
  } else if ( dynamic_cast<TH1D*>(lower) && dynamic_cast<TH1D*>(upper) ) {
    TH1D* lower_th1d = dynamic_cast<TH1D*>(lower);
    TH1D* upper_th1d = dynamic_cast<TH1D*>(upper);
    return th1fmorph(histName.data(), histTitle.data(), lower_th1d, upper_th1d, lowerBound_, upperBound_, value, norm);
  } else throw cms::Exception("HorizontalMorphing")
      << "Invalid histogram types " << lower->ClassName() << " and " << upper->ClassName() << " !!\n";
}

void
HorizontalMorphing::process(){
  for(std::map<double, double>::const_iterator point = points_.begin(); point != points_.end(); ++point){
    TH1* hout = interpolate(point->first, point->second);
    if ( outputFileName_ != inputFileName_lowerBound_ && outputFileName_ != inputFileName_upperBound_ ) {
      assert(outputFileName_ != "");
      TFile* outputFile = new TFile(outputFileName_.c_str(), "RECREATE");
      outputFile->cd();
      if ( path_ != "" ) {
	TDirectory* directory = outputFile->mkdir(path_.c_str());
	directory->cd();
      }
      hout->Write();
      delete outputFile;
    } else if ( inputFile_lowerBound_ == inputFile_upperBound_ ){
      if ( path_ != "" ) inputFile_lowerBound_->cd(path_.c_str());
      hout->Write();
    } else assert(0);
  }
  /*
  for(std::map<double, double>::const_iterator point = points_.begin(); point != points_.end(); ++point){
    TH1* hout = interpolate(point->first, point->second, "_CMS_scale_jUp");
    file_->cd(path_.c_str());
    hout->Write();
  }
  for(std::map<double, double>::const_iterator point = points_.begin(); point != points_.end(); ++point){
    TH1* hout = interpolate(point->first, point->second, "_CMS_scale_jDown");
    file_->cd(path_.c_str());
    hout->Write();
  }
  */
}
