#include "FinalStateAnalysis/DataAlgos/interface/PileupWeighting.h"

#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"
#include "FWCore/Utilities/interface/Exception.h"

#include <boost/assign/list_of.hpp>
#include <map>
#include <iostream>

#include "TFile.h"
#include "TH1.h"

typedef std::map<std::string, boost::shared_ptr<TH1> > DistMap;

namespace {

// MC and data distributions
static DistMap mcDistributions;
static DistMap dataDistributions;

// Where we store our data
const static edm::FileInPath puInfoFile(
    "FinalStateAnalysis/DataAlgos/data/pileup_distributions.py");

boost::shared_ptr<TH1> loadFromPSet(const std::string& name) {
  boost::shared_ptr<edm::ParameterSet> toplevel =
    make_shared_ptr(edm::readPSetsFrom(puInfoFile.fullPath()));

  edm::ParameterSet steering = toplevel->getParameterSet(
      "pileup_distributions");

  // ROOT file path
  std::string path = "";
  try {
    path = steering.getParameter<edm::FileInPath>(name).fullPath();
  } catch (cms::Exception) {
    std::cerr << "Couldn't get PU distribution corresponding to " << name
      << std::endl;
    std::vector<std::string> available = toplevel->getParameterNames();
    std::cerr << "There are " << available.size() << " available PUs:"
      << std::endl;
    for (size_t i = 0; i < available.size(); ++i) {
      std::cerr << i << ") " << available[i] << std::endl;
    }
    throw;
  }

  TFile file(path.c_str(), "READ");

  TH1* histo = static_cast<TH1*>(file.Get("pileup"));

  if (!histo) {
    throw cms::Exception("MissingPUHisto")
      << "I can't read the [pileup] TH1 from " << path << std::endl;
  }

  boost::shared_ptr<TH1> owned((TH1*)histo->Clone());

  // Make sure it's normalized.
  owned->Scale(1./owned->Integral());
  return owned;
}

double getValue(const boost::shared_ptr<TH1>& histo, double x) {
  int bin = histo->FindBin(x);
  return histo->GetBinContent(bin);
}

} // end anon. namespace

double getPileupWeight(const std::string& dataTag, const std::string& mcTag,
    double nTrueInteractions) {

  DistMap::iterator findMC = mcDistributions.find(mcTag);
  // load it if we haven't yet.
  if (findMC == mcDistributions.end()) {
    mcDistributions.insert(
        std::make_pair(mcTag, loadFromPSet(mcTag))).second;
    findMC = mcDistributions.find(mcTag);
  }

  DistMap::iterator findData = dataDistributions.find(dataTag);
  // load it if we haven't yet.
  if (findData == dataDistributions.end()) {
    dataDistributions.insert(
        std::make_pair(dataTag, loadFromPSet(dataTag))).second;
    findData = dataDistributions.find(dataTag);
  }

  double dataWeight = getValue(findData->second, nTrueInteractions);
  double mcWeight = getValue(findMC->second, nTrueInteractions);

  if (mcWeight == 0)
    return 0;

  return dataWeight/mcWeight;
}
