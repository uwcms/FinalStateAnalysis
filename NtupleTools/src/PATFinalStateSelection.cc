#include "FinalStateAnalysis/NtupleTools/interface/PATFinalStateSelection.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/Utilities/interface/CutFlow.h"
#include "FWCore/Utilities/interface/RegexMatch.h"


namespace {
  class CandPtSorter {
    public:
      bool operator()(
          const reco::Candidate* c1, const reco::Candidate* c2) const {
        return c1->pt() > c2->pt();
      }
  };
}

PATFinalStateSelection::PATFinalStateSelection(
    const edm::ParameterSet& pset, TFileDirectory& fs) {
  typedef std::vector<edm::ParameterSet> VPSet;

  VPSet selections = pset.getParameter<VPSet>("selections");

  // Register the most basic selection, which is the existence of the final
  // state.
//  push_back("All");
  push_back("Topology");
  topologyCutId_ = index_type(&bits_, "Topology");

  for (size_t i = 0; i < selections.size(); ++i) {
    edm::ParameterSet& selection = selections[i];
    std::string name = selection.getParameter<std::string>("name");
    // Register the cut in the selector
    push_back(name);
    cuts_.push_back(new FinalStateCut(selection, fs));
  }

  // Load any cuts we want to ignore
  typedef std::vector<std::string> vstring;
  vstring ignore = pset.exists("ignore") ?
    pset.getParameter<vstring>("ignore") : vstring();
  // Turn on all cuts
  bits_.set(true);

  //setIgnoredCuts(ignore);

  // Setup any ignored cuts
  for (size_t i = 0; i < cuts_.size(); ++i) {
    std::string cutName = cuts_[i].name();
    index_type cutIndex(&bits_, cutName);
    cutIndices_.push_back(cutIndex);

    bool isIgnored = false;
    // Check if we are ignoring this cut
    for (size_t iIg = 0; iIg < ignore.size(); ++iIg) {
      const std::string& ignoreCmd = ignore[iIg];
      if (cutName == ignoreCmd) {
        isIgnored = true;
        break;
      }
      // Or if is a regex
      if (edm::is_glob(ignoreCmd)) {
        std::vector<std::string> theName;
        theName.push_back(cutName);
        //std::cout << "Checking: " << cutName << " " << ignoreCmd << " " <<  edm::regexMatch(theName, ignoreCmd).size()<< std::endl;
        if (edm::regexMatch(theName, ignoreCmd).size()) {
          isIgnored = true;
          break;
        }
      }
    }

    if (isIgnored) {
      set(cutIndex, false);
      cuts_[i].setIgnore(true);
      assert(ignoreCut(cutIndex));
    }
  }

  edm::ParameterSet final = pset.getParameterSet("final");

  if (final.exists("sort")) {
    finalSort_.reset(new StringObjectSorter<PATFinalState>(
          final.getParameter<std::string>("sort")));
  }
  take_ = final.getParameter<unsigned int>("take");
  TFileDirectory finaldir = fs.mkdir("final");
  eventView_ = pset.getParameter<bool>("EventView");
  if( eventView_ ){
    finalPlotsEventView_.reset(
                      new ek::HistoFolder<PATFinalStatePtrs> 
		      (final.getParameterSet("plot"),finaldir));    
    
  } else {
    finalPlots_.reset(new ek::HistoFolder<PATFinalState>(
		      final.getParameterSet("plot"), finaldir));
  }

  // Setup the cutflow and link it to the bitset which defines how things pass
  // our cuts.
  cutFlow_.reset(new ek::CutFlow(bits_, "cutFlow", fs));
}

PATFinalStateSelection::~PATFinalStateSelection(){}

bool PATFinalStateSelection::operator()(const PATFinalStatePtrs& input,
    double weight) {
  // Copy the collection to one that we can modify.
  PATFinalStatePtrs passingLocal(input);

//  std::cout << "START" << std::endl;
//  for (size_t i = 0; i < passingLocal.size(); ++i) {
//    std::cout << passingLocal[i]->daughter(2) << std::endl;
//    std::cout << passingLocal[i]->daughter(2)->pt() << std::endl;
//  }
//  std::cout << "END" << std::endl;

  // Set all the cuts to false
  bits_.set(false);

  // If there are any final states to cut
  if (input.size())
    this->passCut(bits_, topologyCutId_);

  for (size_t i = 0; i < cuts_.size(); ++i) {
    // Filter the passing collection collection
    passingLocal = cuts_[i].analyze(passingLocal, weight);
    if (passingLocal.size())
      this->passCut(bits_, cutIndices_[i]);
    else
      break;
  }

  // Fill the cut flow
  cutFlow_->fill(bits_, weight);

  // Check if we want to sort the final selected candidates
  // TODO: fix me.  For some reason this has problems (see Utilities unit tests)
//  if (finalSort_.get()) {
//    std::sort(passingLocal.begin(), passingLocal.end(), *finalSort_);
//  }
  std::sort(passingLocal.begin(), passingLocal.end(), CandPtSorter());

  // Copy only the desired number
  passing_.clear();
  for (size_t i = 0; i < passingLocal.size() && i < take_; ++i) {
    passing_.push_back(passingLocal[i]);
    // only fill the ntuple if we're not doing event view
    if (!eventView_ && finalPlots_.get()) 
      finalPlots_->fill(*passingLocal[i], weight, i);
  }
  // if event view fill fill variable-sized branches
  if ( eventView_ ) finalPlotsEventView_->fill(passingLocal, weight);

  // Check if any pass
  return passing_.size();
}
