#ifndef FinalStateAnalysis_Utilities_Histogrammer_h
#define FinalStateAnalysis_Utilities_Histogrammer_h

#include "CommonTools/Utils/interface/ExpressionHisto.h"
#include "FinalStateAnalysis/Utilities/interface/ExpressionNtuple.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

namespace ek {

template<typename T>
class HistoFolder {
  typedef StringCutObjectSelector<T> Selector;
  typedef boost::shared_ptr<Selector> SelectorPtr;
  typedef ExpressionHisto<T> Histo;
  typedef boost::shared_ptr<Histo> HistoPtr;
  typedef std::vector<edm::ParameterSet> VPSet;
  public:
    // Constructor with subfolders, selections, etc.
    HistoFolder(const edm::ParameterSet& pset, TFileDirectory& fs);
    // Simple constructor using only a VPSet of histograms.
    HistoFolder(const VPSet& psets, TFileDirectory& fs);
    // Simple which takes a mother PSet and the name of the histo folder
    // configuration parameter.  Will automatically deduce which constructor to
    // use.
    HistoFolder(const edm::ParameterSet& motherPset,
		const std::string& parName, 
		TFileDirectory& fs);

    // Fill using the given object and weight.  Optionally you can provide the
    // object index, which will be passed to any ntuples contained in this
    // folder.
    void fill(const T& object, double weight, int idx=-1);
  private:
    // Initialization methods
    void bookHistograms(const edm::ParameterSet& pset, TFileDirectory& fs);
    void bookHistograms(const VPSet& psets, TFileDirectory& fs);
    SelectorPtr selector_;
    std::vector<boost::shared_ptr<HistoFolder<T> > > subfolders_;
    std::vector<HistoPtr> histos_;
    boost::shared_ptr<ExpressionNtuple<T> > ntuple_;
};

template<typename T>
HistoFolder<T>::HistoFolder(const edm::ParameterSet& pset, 
			    TFileDirectory& fs) {
  bookHistograms(pset, fs);
}

template<typename T>
HistoFolder<T>::HistoFolder(const VPSet& psets, TFileDirectory& fs) {
  bookHistograms(psets, fs);
}

template<typename T>
HistoFolder<T>::HistoFolder(const edm::ParameterSet& motherPset,
			    const std::string& parName, 
			    TFileDirectory& fs) {
  assert(motherPset.exists(parName));
  if (motherPset.existsAs<edm::ParameterSet>(parName))
    bookHistograms(motherPset.getParameterSet(parName), fs);
  else
    bookHistograms(motherPset.getParameter<VPSet>(parName), fs);
}

template<typename T> void
HistoFolder<T>::bookHistograms(const edm::ParameterSet& pset,
    TFileDirectory& fs) {
  // Check if this folder has a selection
  if (pset.exists("SELECT")) {
    selector_.reset(new StringCutObjectSelector<T>(
          pset.getParameter<std::string>("SELECT")));
  }

  // Now get all the histograms
  VPSet histos = pset.getParameter<VPSet>("histos");
  bookHistograms(histos, fs);

  // Check if we want to make an ExpressionNtuple
  if (pset.exists("ntuple")) {
    ntuple_.reset(new ExpressionNtuple<T>(pset.getParameterSet("ntuple")));
    ntuple_->initialize(fs);
  }

  // Now find all the subfolders (which are psets)
  typedef std::vector<std::string> vstring;
  vstring subFolderNames = pset.getParameterNamesForType<edm::ParameterSet>();
  // Now build all the subfolders
  for (size_t iFol = 0; iFol < subFolderNames.size(); ++iFol) {
    std::string subFolderName = subFolderNames[iFol];
    if (subFolderName == "ntuple") // skip reserved word
      continue;
    edm::ParameterSet subFolderPSet = pset.getParameterSet(subFolderName);
    TFileDirectory subdir = fs.mkdir(subFolderName);
    boost::shared_ptr<HistoFolder<T> > subfolder(
        new HistoFolder<T>(subFolderPSet, subdir));
    subfolders_.push_back(subfolder);
  }
}


template<typename T> void
HistoFolder<T>::bookHistograms(const VPSet& psets, TFileDirectory& fs) {
  for (size_t iHisto = 0; iHisto < psets.size(); ++iHisto) {
    edm::ParameterSet histoPSet = psets[iHisto];
    // Build the histo
    HistoPtr histo(new Histo(histoPSet));
    // Initialize it
    histo->initialize(fs);
    histos_.push_back(histo);
  }
}

// Recursive filling of histograms
template<typename T>
void HistoFolder<T>::fill(const T& object, double weight, int idx) {
  // Check if we are selecting and if it passes
  if (!selector_.get() || (*selector_)(object)) {
    // Fill this directories histos
    for (size_t iHisto = 0; iHisto < histos_.size(); ++iHisto) {
      histos_.at(iHisto)->fill(object, weight);
    }
    // Fill this directories ntuple, if we are using it.
    if (ntuple_.get())
      ntuple_->fill(object, idx);
    // Descend into subdirectories
    for (size_t iFolder = 0; iFolder < subfolders_.size(); ++iFolder) {
      subfolders_.at(iFolder)->fill(object, weight, idx);
    }
  }
}

// vector specialization
template<typename T>
class HistoFolder<std::vector<const T*> > {
  typedef StringCutObjectSelector<T> Selector;
  typedef boost::shared_ptr<Selector> SelectorPtr;
  typedef ExpressionHisto<T> Histo;
  typedef boost::shared_ptr<Histo> HistoPtr;
  typedef std::vector<edm::ParameterSet> VPSet;
  public:
    // Constructor with subfolders, selections, etc.
    HistoFolder(const edm::ParameterSet& pset, TFileDirectory& fs);
    // Simple constructor using only a VPSet of histograms.
    HistoFolder(const VPSet& psets, TFileDirectory& fs);
    // Simple which takes a mother PSet and the name of the histo folder
    // configuration parameter.  Will automatically deduce which constructor to
    // use.
    HistoFolder(const edm::ParameterSet& motherPset,
		const std::string& parName, 
		TFileDirectory& fs);

    // Fill using the given object and weight.  Optionally you can provide the
    // object index, which will be passed to any ntuples contained in this
    // folder.
    void fill(const std::vector<const T*>& object, double weight, int idx=-1);
  private:
    // Initialization methods
    void bookHistograms(const edm::ParameterSet& pset, TFileDirectory& fs);
    void bookHistograms(const VPSet& psets, TFileDirectory& fs);
    SelectorPtr selector_;
    std::vector<boost::shared_ptr<HistoFolder<std::vector<const T*> > > > 
      subfolders_;
    std::vector<HistoPtr> histos_;
    boost::shared_ptr<ExpressionNtuple<std::vector<const T*> > > 
      ntuple_;
};

template<typename T>
HistoFolder<std::vector<const T*> >::
  HistoFolder(const edm::ParameterSet& pset, 
	      TFileDirectory& fs) {
  bookHistograms(pset, fs);
}

template<typename T>
HistoFolder<std::vector<const T*> >::
  HistoFolder(const VPSet& psets, 
	      TFileDirectory& fs) {
  bookHistograms(psets, fs);
}

template<typename T>
HistoFolder<std::vector<const T*> >::
  HistoFolder(const edm::ParameterSet& motherPset,
	      const std::string& parName, 
	      TFileDirectory& fs) {
  assert(motherPset.exists(parName));
  if (motherPset.existsAs<edm::ParameterSet>(parName))
    bookHistograms(motherPset.getParameterSet(parName), fs);
  else
    bookHistograms(motherPset.getParameter<VPSet>(parName), fs);
}

template<typename T> void
HistoFolder<std::vector<const T*> >::
  bookHistograms(const edm::ParameterSet& pset,
		 TFileDirectory& fs) {
  // Check if this folder has a selection
  if (pset.exists("SELECT")) {
    selector_.reset(new StringCutObjectSelector<T>(
          pset.getParameter<std::string>("SELECT")));
  }

  // Now get all the histograms
  VPSet histos = pset.getParameter<VPSet>("histos");
  bookHistograms(histos, fs);

  // Check if we want to make an ExpressionNtuple
  if (pset.exists("ntuple")) {
    ntuple_.reset(new ExpressionNtuple<std::vector<const T*> >(
                          pset.getParameterSet("ntuple"))
		  );
    ntuple_->initialize(fs);
  }

  // Now find all the subfolders (which are psets)
  typedef std::vector<std::string> vstring;
  vstring subFolderNames = pset.getParameterNamesForType<edm::ParameterSet>();
  // Now build all the subfolders
  for (size_t iFol = 0; iFol < subFolderNames.size(); ++iFol) {
    std::string subFolderName = subFolderNames[iFol];
    if (subFolderName == "ntuple") // skip reserved word
      continue;
    edm::ParameterSet subFolderPSet = pset.getParameterSet(subFolderName);
    TFileDirectory subdir = fs.mkdir(subFolderName);
    boost::shared_ptr<HistoFolder<std::vector<const T*> > > subfolder(
	      new HistoFolder<std::vector<const T*> >(subFolderPSet, subdir));
    subfolders_.push_back(subfolder);
  }
}


template<typename T> void
HistoFolder<std::vector<const T*> >
  ::bookHistograms(const VPSet& psets, 
		   TFileDirectory& fs) {
  for (size_t iHisto = 0; iHisto < psets.size(); ++iHisto) {
    edm::ParameterSet histoPSet = psets[iHisto];
    // Build the histo
    HistoPtr histo(new Histo(histoPSet));
    // Initialize it
    histo->initialize(fs);
    histos_.push_back(histo);
  }
}

// Recursive filling of histograms
template<typename T>
void HistoFolder<std::vector<const T*> >::
  fill(const std::vector<const T*>& objects, 
       double weight, int /*idx*/) {
  
  //loop through the objects
  for( size_t i = 0; i < objects.size(); ++i ) {
    // Check if we are selecting and if it passes
    if (!selector_.get() || (*selector_)(*objects[i])) {
      // Fill this directories histos
      for (size_t iHisto = 0; iHisto < histos_.size(); ++iHisto) {
	histos_.at(iHisto)->fill(*objects[i], weight);
      }      
    }
  }
  // Fill this directories ntuple, if we are using it.
  if (ntuple_.get())
    ntuple_->fill(objects);
  // Descend into subdirectories
  for (size_t iFolder = 0; iFolder < subfolders_.size(); ++iFolder) {
    subfolders_.at(iFolder)->fill(objects, weight);
  }
}

}

#endif
