#ifndef ANALYSISCUTHOLDER_1SUHQMG4
#define ANALYSISCUTHOLDER_1SUHQMG4

/*
 * AnalysisCutHolderT<T>
 *
 * Author: Evan K. Friis, UW Madison
 *
 * A class which cuts and plots (collection of) objects of type T.
 *
 * The class takes an edm::ParameterSet configuration and a link
 * to a TFileDirectory into the constructor.
 *
 * The configuration parameters are:
 *  o name: Name of the cut (and subsequent folder)
 *  o description: To be used in TH1 title, etc.
 *
 *  The following parameters are optional.
 *  o cut: The string cut to apply.  Default no cut.
 *  o plot: a cms.PSet that is used to create a HistoFolder<T>.  Default none.
 *  o plotBefore: A HistoFolder that is filled before the cut is applied.
 *  o invert: Invert the cut.  (default false)
 *
 * The class is explicitly not copy-constructible, since it does not own some of
 * the histograms.  Use a ptr_vector for storage.
 */

#include "FinalStateAnalysis/Utilities/interface/HistoFolder.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "TH1F.h"

#include <vector>
#include <memory>
#include <boost/utility.hpp>

template<class T>
class AnalysisCutHolderT : private boost::noncopyable{
  public:
    typedef std::vector<const T*> VectorPtrT;
  typedef std::vector<edm::ParameterSet> VPSet;

    AnalysisCutHolderT(const edm::ParameterSet& pset, TFileDirectory& fs);
    // Simple predicate to check if it passes the cut
    bool filter(const T& object) const;
    // Filter and plot a collection of objects
    VectorPtrT analyze(const VectorPtrT& objects, double weight) const;

    const std::string& name() const { return name_; }
    const std::string& description() const { return description_; }

    // Set the ignore bit for this cut.  If the cut is ignored, all the plots
    // will still be made, but the cut will always pass.
    void setIgnore(bool ignore) { ignored_ = ignore; }

  private:
    typedef StringCutObjectSelector<T> StringCutT;
    typedef ek::HistoFolder<T> HistoFolderT;
    std::string name_;
    std::string description_;

    std::auto_ptr<StringCutT> cut_;
    bool invert_;
    bool ignored_;

    std::auto_ptr<HistoFolderT> folder_;
    std::auto_ptr<HistoFolderT> folderBefore_;
    TH1F* cutHisto_;
};


template<class T>
AnalysisCutHolderT<T>::AnalysisCutHolderT(const edm::ParameterSet& pset,
    TFileDirectory& fs) {
  name_ = pset.getParameter<std::string>("name");
  description_ = pset.exists("description") ?
    pset.getParameter<std::string>("description") : name_;
  ignored_ = false;

  // Make cut subdirectory
  TFileDirectory subdir = fs.mkdir(name_);

  // The cut to apply
  if (pset.exists("cut"))
    cut_.reset(new StringCutT(pset.getParameter<std::string>("cut"), true));

  invert_ = pset.exists("invert") ? pset.getParameter<bool>("invert") : false;

  // Plots to make after cut is applied
  if (pset.exists("plot"))
    folder_.reset(new HistoFolderT(pset, "plot", subdir));

  // Plots to make before cut is applied
  if (pset.exists("before")) {
    TFileDirectory before = subdir.mkdir("before");
    folderBefore_.reset(new HistoFolderT(pset, "before", before));
  }

  // Declare cut monitor histo if we are cutting
  if (cut_.get()) {
    cutHisto_ = subdir.make<TH1F>(
        name_.c_str(), description_.c_str(), 2, -0.5, 1.5);
    cutHisto_->GetXaxis()->SetTitle("Filter result");
    cutHisto_->GetXaxis()->SetBinLabel(1, "Fail");
    cutHisto_->GetXaxis()->SetBinLabel(2, "Pass");
  }
}

template<class T> bool
AnalysisCutHolderT<T>::filter(const T& object) const {
  if (ignored_)
    return true;
  // Get cut result
  bool pass = true;
  if (cut_.get()) {
    pass = (*cut_)(object);
  }
  // Check if we want to invert the cut result
  return pass ^ invert_;
}

template<class T> std::vector<const T*>
AnalysisCutHolderT<T>::analyze(const VectorPtrT& objects, double weight) const {
  VectorPtrT output;
  // Analyze each object in turn
  for (size_t i = 0; i < objects.size(); ++i) {
    const T* object = objects[i];
    assert(object);
    // Make the pre-cut plots, if desired
    if (folderBefore_.get()) {
      folderBefore_->fill(*object, weight, i);
    }
    // Get cut result
    bool pass = filter(*object);
    if (cutHisto_)
      cutHisto_->Fill(pass, weight);
    // Fill after plots
    if (pass && folder_.get()) {
      folder_->fill(*object, weight, output.size());
    }
    if (pass)
      output.push_back(object);
  }
  return output;
}

#endif /* end of include guard: ANALYSISCUTHOLDER_1SUHQMG4 */
