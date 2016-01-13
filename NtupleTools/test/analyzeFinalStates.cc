#include "FinalStateAnalysis/NtupleTools/interface/PATFinalStateAnalysis.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"

#include "DataFormats/FWLite/interface/ChainEvent.h"
#include "DataFormats/FWLite/interface/LuminosityBlock.h"
#include "DataFormats/FWLite/interface/InputSource.h"
#include "DataFormats/FWLite/interface/OutputFiles.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"

#include <TFile.h>
#include <TSystem.h>

#include "FWCore/Utilities/interface/UnixSignalHandlers.h"

#include <boost/ptr_container/ptr_vector.hpp>

// Dont support fwlite yet

//int main(int argc, char* argv[]) {
//
//  // only allow one argument for this which should be the python cfg file
//  if ( argc < 2 ) {
//    std::cout << "Usage : " << argv[0] << " [parameters.py]" << std::endl;
//    return 0;
//  }
//
//  // load framework libraries
//  gSystem->Load( "libFWCoreFWLite" );
//  AutoLibraryLoader::enable();
//
//  edm::installCustomHandler(SIGINT, edm::ep_sigusr2);
//
//  // Get the python configuration
//  PythonProcessDesc builder(argv[1], argc, argv);
//  edm::ParameterSet cfg = *builder.processDesc()->getProcessPSet();
//
//  /// helper class  for input parameter handling
//  fwlite::InputSource inputHandler(cfg);
//  /// helper class for output file handling
//  fwlite::OutputFiles outputHandler_(cfg);
//  fwlite::TFileService fileService(outputHandler_.file());
//
//  /// Get list of analyses to run
//  typedef std::vector<std::string> vstring;
//  edm::ParameterSet steering = cfg.getParameterSet("steering");
//  vstring toAnalyze = steering.getParameter<vstring>("analyzers");
//
//  // Build our list of analyzers
//  boost::ptr_vector<PATFinalStateAnalysis> analyzers;
//  for (size_t i = 0; i < toAnalyze.size(); ++i) {
//    std::cout << "Initializing final state analyzer: "
//      << toAnalyze[i] << std::endl;
//    TFileDirectory subdir = fileService.mkdir(toAnalyze[i].c_str());
//    edm::ParameterSet anaCfg = cfg.getParameterSet(toAnalyze[i]);
//    anaCfg.addParameter<std::string>("@module_label", toAnalyze[i]);
//    analyzers.push_back(new PATFinalStateAnalysis(anaCfg, subdir));
//    //analyzers.push_back(new PATFinalStateAnalysis(anaCfg, subdir, consumesCollector()));
//  }
//
//  /// Last run processed
//  edm::RunNumber_t lastRun = 0;
//  /// Last run processed
//  edm::LuminosityBlockNumber_t lastLumi = 0;
//
//  unsigned int reportAfter = steering.exists("reportAfter") ?
//    steering.getParameter<unsigned int>("reportAfter") : 1000;
//
//  /// Get the maximum number of events
//  int maxEvents = cfg.exists("maxEvents") ?
//    cfg.getUntrackedParameterSet("maxEvents").getUntrackedParameter<int>(
//        "input") : -1;
//
//  int ievt=0;
//  const vstring& inputFiles = inputHandler.files();
//  // loop the vector of input files
//  fwlite::ChainEvent event( inputFiles );
//
//  // watch for shutdown signal
//  {
//    boost::mutex::scoped_lock sl(boost::mutex);
//
//    for(event.toBegin(); !event.atEnd(); ++event, ++ievt){
//      // Check if we are in a new lumi.  If so we gotta call the appropriate
//      // function in the wrapped class.
//      edm::EventID id = event.id();
//      if (id.luminosityBlock() != lastLumi || id.run() != lastRun) {
//        lastLumi = id.luminosityBlock();
//        lastRun = id.run();
//        // We have started a new lumi block
//        const fwlite::LuminosityBlock& ls = event.getLuminosityBlock();
//        for (size_t i = 0; i < analyzers.size(); ++i) {
//          analyzers[i].beginLuminosityBlock(ls);
//        }
//      }
//
//      // break loop if maximal number of events is reached
//      if(maxEvents>0 ? ievt+1>maxEvents : false) break;
//      // simple event counter
//      if(reportAfter!=0 ? (ievt>0 && ievt%reportAfter==0) : false)
//        std::cout << "  processing event: " << ievt << std::endl;
//      // analyze event
//      for (size_t i = 0; i < analyzers.size(); ++i) {
//        analyzers[i].analyze(event);
//      }
//
//      if (edm::shutdown_flag) {
//        std::cerr << "Signal detected, quitting after " << ievt << " events."
//          << std::endl;
//        break;
//      }
//    }
//
//  }
//  for (size_t i = 0; i < analyzers.size(); ++i) {
//    analyzers[i].endJob();
//  }
//  return 0;
//}

