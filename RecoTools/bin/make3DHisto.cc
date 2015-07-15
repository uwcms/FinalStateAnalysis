/*
 * Take an input PU histogram distribution and make an output 3D weight file
 *
 * Run on all Cert pileup files:
 *
 * ls Cert_1*root | grep -v 3d.root | sed "s/.root//" | xargs -n 1 -I % make3DHisto --file %.root --path pileup --type data --output %.3d.root
 *
 */

#include <boost/program_options.hpp>
#include <iostream>

#include "TH3D.h"
#include "TH1.h"
#include "TFile.h"
#include "TMath.h"


int main(int argc, char* argv[]) {
  std::string descString(argv[0]);
  descString +=
    "\n The program converts an input histogram file to a 3D weight file.";
  boost::program_options::options_description desc(descString);

  desc.add_options()
    ("help", "show this help message")
    ("file", boost::program_options::value<std::string>(), "input .root file")
    ("path", boost::program_options::value<std::string>(), "path to histogram in file")
    ("output", boost::program_options::value<std::string>(), "output .root file")
    ("type", boost::program_options::value<std::string>(), "data or MC");

  boost::program_options::variables_map vm;
  try {
    store(boost::program_options::command_line_parser(argc,argv).
        options(desc).run(),vm);
    notify(vm);
  } catch(boost::program_options::error const& iException) {
    std::cerr <<"failed to parse command line \n"<<iException.what()<<"\n";
    return 1;
  }
  if(vm.count("help")) {
    std::cout << desc <<std::endl;
    return 0;
  }
  if (!vm.count("file")) {
    std::cerr << "Must specify input file!\n" << desc << std::endl;
    return 1;
  }
  if (!vm.count("path")) {
    std::cerr << "Must specify path to histo!\n" << desc << std::endl;
    return 1;
  }
  if (!vm.count("type")) {
    std::cerr << "Must specify type!\n" << desc << std::endl;
    return 1;
  }
  if (!vm.count("output")) {
    std::cerr << "Must specify output file!\n" << desc << std::endl;
    return 1;
  }

  std::string filepath(vm["file"].as<std::string>());
  std::string path(vm["path"].as<std::string>());
  std::string type(vm["type"].as<std::string>());
  std::string output(vm["output"].as<std::string>());

  std::cout << "Loading input file: " << filepath << std::endl;

  TFile inputFile(filepath.c_str(), "READ");

  TH1* inputHisto = dynamic_cast<TH1*>(inputFile.Get(path.c_str()));

  double outputArray[50][50][50];

  for (int i=0; i<50; i++) {
    for(int j=0; j<50; j++) {
      for(int k=0; k<50; k++) {
        outputArray[i][j][k] = 0.;
      }
    }
  }

  double factorial[50];
  double PowerSer[50];
  double base = 1.;

  factorial[0] = 1.;
  PowerSer[0]=1.;

  for (int i = 1; i<50; ++i) {
    base = base*float(i);
    factorial[i] = base;
  }

  int nbin = inputHisto->GetNbinsX();

  std::cout << "Generating weights over " << nbin << " bins " << std::endl;
  for (int jbin=1;jbin<nbin+1;jbin++) {
    double x =  inputHisto->GetBinCenter(jbin);
    double xweight = inputHisto->GetBinContent(jbin); //use as weight for matrix

    double mean;
    if (type == "MC") {
      //for Summer 11, we have this int feature:
      int xi = int(x);
      // Generate Poisson distribution for each value of the mean
      mean = double(xi);
    } else if (type == "data") {
      mean = x;
    } else {
      std::cerr << "Type must be MC or data!" << std::endl;
      return 2;
    }

    if(mean<0.) {
      std::cerr
        << " Your histogram generates MC luminosity values less than zero!"
        << " value: " << mean
        << " Please Check.  Terminating." << std::endl;
      return 3;
    }

    double Expval;
    if(mean==0.){
      Expval = 1.;
    }
    else {
      Expval = TMath::Exp(-1.*mean);
    }

    double base = 1.;

    for (int i = 1; i<50; ++i) {
      base = base*mean;
      PowerSer[i] = base; // PowerSer is mean^i
    }

    // compute poisson probability for each Nvtx in weight matrix

    for (int i=0; i<50; i++) {
      double probi = PowerSer[i]/factorial[i]*Expval;
      for(int j=0; j<50; j++) {
        double probj = PowerSer[j]/factorial[j]*Expval;
        for(int k=0; k<50; k++) {
          double probk = PowerSer[k]/factorial[k]*Expval;
          // joint probability is product of event weights multiplied by weight of input distribution bin
          outputArray[i][j][k] = outputArray[i][j][k]+probi*probj*probk*xweight;
        }
      }
    }
  }
  TFile * outputFile = new TFile(output.c_str(), "RECREATE");
  outputFile->cd();
  std::cout << "Copying to TH3" << std::endl;
  TH3D* hist = new TH3D("pileup","3D weights",50,-.5,49.5,50,-.5,49.5,50,-.5,49.5 );
  for (int i=0; i<50; i++) {
    for(int j=0; j<50; j++) {
      for(int k=0; k<50; k++) {
        hist->SetBinContent( i+1,j+1,k+1,outputArray[i][j][k] );
      }
    }
  }
  // Scale to original normalization (so we can hadd them)
  std::cout << "Scaling to match original integrated luminosity" << std::endl;

  hist->Scale(inputHisto->Integral()/hist->Integral());

  hist->Write();
  outputFile->Write();
  outputFile->Close();
  return 0;
}
