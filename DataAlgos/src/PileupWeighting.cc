#include "FinalStateAnalysis/DataAlgos/interface/PileupWeighting.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "TH1.h"
#include "TH3D.h"
#include "TFile.h"

#include <boost/shared_ptr.hpp>
#include <boost/assign/list_of.hpp>
#include <map>
#include <iostream>

//typedef boost::shared_ptr<TH1> TH1Ptr;
typedef TH1* TH1Ptr;

namespace {

  TH1Ptr loadAndNormHistogram(const edm::FileInPath& path,
      const std::string& name="pileup") {
    TFile file(path.fullPath().c_str(), "READ");
    TH1Ptr output(static_cast<TH1*>(file.Get(name.c_str())->Clone()));
    std::cout << "Loading PU histogram from " << path.relativePath();
    //if (output.get() == NULL) {
    if (output == NULL) {
      throw cms::Exception("BadPileupFile")
        << "The file " << path.fullPath() << " does not contain histogram: "
        << name << std::endl;
    }
    output->SetDirectory(0);
    std::cout << "... histo normalization = " << output->Integral() << std::endl;
    // Normalize
    output->Scale(1.0/output->Integral());
    return output;
  }

  // Build the list of available MC histos
  static std::map<std::string, TH1Ptr> mcHistos = boost::assign::map_list_of
    ("S6", loadAndNormHistogram(edm::FileInPath("FinalStateAnalysis/RecoTools/data/pu/fall11_mc_truth.3d.root")))
    ("S4", loadAndNormHistogram(edm::FileInPath("FinalStateAnalysis/RecoTools/data/pu/summer11_mc_truth.3d.root")));

  // Build the list of available data histos
  static const std::map<std::string, TH1Ptr> dataHistos = boost::assign::map_list_of
    ("2011B", loadAndNormHistogram(edm::FileInPath("FinalStateAnalysis/RecoTools/data/pu/allData_2011B_finebin.3d.root")))
    ("2011A", loadAndNormHistogram(edm::FileInPath("FinalStateAnalysis/RecoTools/data/pu/allData_2011A_finebin.3d.root")))
    ("2011AB", loadAndNormHistogram(edm::FileInPath("FinalStateAnalysis/RecoTools/data/pu/allData_2011AB_finebin.3d.root")));

} // end anon. namespace

double
get3DPileupWeight(const std::string& dataTag, const std::string& mcTag,
    const std::vector<PileupSummaryInfo>& puInfo) {

//  std::cout << "Getting PU weight for " << dataTag << " " << mcTag << std::endl;

  std::map<std::string, TH1Ptr>::const_iterator mcHisto = mcHistos.find(mcTag);
  if (mcHisto == mcHistos.end()) {
    throw cms::Exception("WrongPUTag")
      << "I didn't understand the MC PU tag: " << mcTag << std::endl;
  }

  std::map<std::string, TH1Ptr>::const_iterator dataHisto = dataHistos.find(dataTag);
  if (dataHisto == dataHistos.end()) {
    throw cms::Exception("WrongPUTag")
      << "I didn't understand the data PU tag: " << dataTag << std::endl;
  }

  int npm1=-1;
  int np0=-1;
  int npp1=-1;

  for(std::vector<PileupSummaryInfo>::const_iterator PVI = puInfo.begin();
      PVI != puInfo.end(); ++PVI) {

    int BX = PVI->getBunchCrossing();

    if(BX == -1) {
      npm1 = PVI->getPU_NumInteractions();
    }
    if(BX == 0) {
      np0 = PVI->getPU_NumInteractions();
    }
    if(BX == 1) {
      npp1 = PVI->getPU_NumInteractions();
    }

  }

  npm1 = std::min(npm1,49);
  np0 = std::min(np0,49);
  npp1 = std::min(npp1,49);

//  std::cout << "bins: " << npm1 << " " << np0 << " " << npp1 << std::endl;

  assert(npm1 != -1);
  assert(np0 != -1);
  assert(npp1 != -1);

  assert(mcHisto->second);
  assert(dataHisto->second);

  TH3D* mcHisto3D = dynamic_cast<TH3D*>(mcHisto->second);
  TH3D* dataHisto3D = dynamic_cast<TH3D*>(dataHisto->second);

  assert(mcHisto3D);
  assert(dataHisto3D);

//  std::cout << "MC" << mcHisto3D << std::endl;
//  std::cout << "data" << dataHisto3D << std::endl;

  double mcProb = mcHisto3D->GetBinContent(npm1+1, np0+1, npp1+1);
  double dataProb = dataHisto3D->GetBinContent(npm1+1, np0+1, npp1+1);

  if (mcProb <= 0.) {
    return 0.;
  }

  return dataProb/mcProb;
}
