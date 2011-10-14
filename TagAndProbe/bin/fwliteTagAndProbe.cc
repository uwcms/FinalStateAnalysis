#include "FinalStateAnalysis/TagAndProbe/interface/AnalyzeTagAndProbe.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"
#include "PhysicsTools/UtilAlgos/interface/FWLiteAnalyzerWrapper.h"

typedef fwlite::AnalyzerWrapper<AnalyzeTagAndProbe> WrappedFWLiteAnalyzer;

int main(int argc, char* argv[])
{
  // load framework libraries
  gSystem->Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();

  // only allow one argument for this simple example which should be the
  // the python cfg file
  if ( argc < 2 ) {
    std::cout << "Usage : " << argv[0] << " [parameters.py]" << std::endl;
    return 0;
  }

  // get the python configuration
  PythonProcessDesc builder(argv[1], argc, argv);
  edm::ParameterSet cfg = *builder.processDesc()->getProcessPSet();

  WrappedFWLiteAnalyzer ana(cfg, std::string("myAnalyzer"), std::string("ohyeah"));

  ana.beginJob();
  ana.analyze();
  ana.endJob();
  return 0;
}

