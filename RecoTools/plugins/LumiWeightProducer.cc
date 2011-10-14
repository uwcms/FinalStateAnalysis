/*
 * =============================================================================
 *
 *    LumiWeightProducer
 *
 *    Author:  Evan Friis, UW Madison (evan.friis@cern.ch)
 *
 *    Put MC-to-Data PU correction weights into the edm::Event.
 *
 *    The module uses the PhysicsTools/Utilities/interface/LumiReWeighting.h
 *    functionality.  The input to the module is expected N_PU distributions in
 *    monte carlo and data.  The distributions can be passed in the python
 *    as either a vector of doubles or a .root file.
 *
 *    The module takes two parameters, [monteCarlo] and [data].  The
 *    parameter can either be a cms.vdouble (descbing the distribution) or
 *    a cms.PSet(...) which has a [filename] and [pathToHist] arguments.
 *
 *    Example (using a .root file for data and hardcoded weights for MC):
 *
 *    process.lumiWeights = cms.EDProducer(
 *       "LumiWeightProducer",
 *       monteCarlo = cms.vdouble(0.104109, 0.0703573, ..., 0.000219377),
 *       data = cms.PSet(
 *          fileName = cms.FileInPath("Path/To/data/2011_lumi2.root"),
 *          pathToHist = cms.string("pileup"),
 *       )
 *    )
 *
 *    You can optionally add the bool parameter [autoPad], which if true will
 *    extend a shorter set of weights with zeros so the two weight dist. have the
 *    same range.
 *
 *    The module produces three doubles, which can be accessed via a
 *    edm::Handle<double> using the three InputTags:
 *
 *       cms.InputTag("lumiWeights") # in time PU
 *       cms.InputTag("lumiWeights", "bx3") # averaged with OOT PU
 *       cms.InputTag("lumiWeights", "oot") # OOT workaround for early Summer11
 *
 *    More information at:
 *
 *    https://twiki.cern.ch/twiki/bin/view/CMS/PileupMCReweightingUtilities
 *
 * =============================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"

#include <memory.h>

// Helper functions (implemented at bottom of this file)
namespace {
  std::vector<float> readTH1(const TH1*);
  std::vector<float> parseCfg(const edm::ParameterSet&, const std::string&);
}

class LumiWeightProducer : public edm::EDProducer {
  public:
    LumiWeightProducer(const edm::ParameterSet& pset);
    virtual ~LumiWeightProducer(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    std::auto_ptr<edm::LumiReWeighting> weighter_;
};

LumiWeightProducer::LumiWeightProducer(const edm::ParameterSet& pset) {

  // The distributions in MC and data
  std::vector<float> mcDist = parseCfg(pset, "monteCarlo");
  std::vector<float> dataDist = parseCfg(pset, "data");

  // Check if we want to pad with zeros
  bool autoPad = (pset.exists("autoPad") ?
      pset.getParameter<bool>("autoPad") : false);
  if (autoPad) {
    size_t longest = std::max(mcDist.size(), dataDist.size());
    while (mcDist.size() < longest) {
      mcDist.push_back(0.0);
    }
    while (dataDist.size() < longest) {
      dataDist.push_back(0.0);
    }
  }

  if (mcDist.size() != dataDist.size()) {
    throw cms::Exception("InconsistentWeights") <<
      "The MC (" << mcDist.size() << ") and data (" << dataDist.size()
      << ") distributions aren't the same size!" << std::endl;
  }

  weighter_.reset(new edm::LumiReWeighting(mcDist, dataDist));

  produces<double>();
  produces<double>("oot");
  produces<double>("3bx");
}

void LumiWeightProducer::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<double> intime(new double);
  std::auto_ptr<double> oot(new double);
  std::auto_ptr<double> bx3(new double);

  // Only apply weights in MC
  if (!evt.isRealData()) {
    *intime = weighter_->weight(evt);
    *oot = weighter_->weightOOT(evt);
    *bx3 = weighter_->weight3BX(evt);
  } else {
    *intime = 1.0;
    *oot = 1.0;
    *bx3 = 1.0;
  }

  evt.put(intime);
  evt.put(oot, "oot");
  evt.put(bx3, "3bx");
}

namespace {
  // Convert a TH1F to a vector of doubles.  Assumes constant bin size of 1 PU
  // interaction.
  std::vector<float> readTH1(const TH1* histo) {
    std::vector<float> output;
    if (!histo) {
      throw cms::Exception("MissingWeightHistogram")
        << "The TH1* passed to the readTH1(...) function is null.."
        << std::endl;
    }
    for (int i = 0; i < histo->GetNbinsX(); ++i) {
      output.push_back(histo->GetBinContent(i+1));
    }
    return output;
  }

  // Logic to extract the config (either .root file or hardcoded weights)
  std::vector<float> parseCfg(const edm::ParameterSet& pset,
      const std::string& paramName) {
    std::vector<float> output;
    // .root histogram file mode
    if (pset.existsAs<edm::ParameterSet>(paramName)) {
      edm::ParameterSet fileCfg = pset.getParameterSet(paramName);
      std::string path =
        fileCfg.getParameter<edm::FileInPath>("fileName").fullPath();
      std::auto_ptr<TFile> file(new TFile(path.c_str(), "READ"));

      if (!file.get()) {
        throw cms::Exception("MissingWeightTFile")
          << "The " << paramName << " .root file @ "
          << path << " does not exist!" << std::endl;
      }
      const TH1* histo = dynamic_cast<const TH1*>(file->Get(
          fileCfg.getParameter<std::string>("pathToHist").c_str()));
      output = readTH1(histo);
    } else {
      // Stupid mismatch in float precision...
      std::vector<double> outputD =
        pset.getParameter<std::vector<double> >(paramName);
      // Copy the doubles into the output float vector
      std::copy(outputD.begin(), outputD.end(), std::back_inserter(output));
    }

    return output;
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(LumiWeightProducer);
