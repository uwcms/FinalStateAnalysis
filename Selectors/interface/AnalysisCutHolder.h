#ifndef ANALYSISCUTHOLDER_1SUHQMG4
#define ANALYSISCUTHOLDER_1SUHQMG4

#include "FinalStateAnalysis/Utilities/interface/HistoFolder.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

template<class T>
class AnalysisCutHolder {
  public:
    typedef std::vector<const T*> VectorPtrT;
    AnalysisCutHolder(const edm::ParameterSet& pset, TFileDirectory& fs);
    bool analyze(const T& object, double weight) const;
    std::auto_ptr<VectorPtrT> analyze(
        const VectorPtrT& objects, double weight) const;

  private:
    typedef StringCutObjectSelector<T> StringCutT;
    typedef ek::HistoFolder<T> HistoFolderT;
    std::string name_;
    std::string description_;
    std::auto_ptr<StringCutT> cut_;
    std::auto_ptr<HistoFolderT> folder_;
    std::auto_ptr<HistoFolderT> folderBefore_;
    TH1F* cutHisto_;
};

template<class T>
AnalysisCutHolder<T>::AnalysisCutHolder(const edm::ParameterSet& pset,
    TFileDirectory& fs) {
  name_ = pset.getParameter<std::string>("name");
  description_ = pset.exists("description") ?
    pset.getParameter<std::string>("description") : name_;

  // Make cut subdirectory
  TFileDirectory subdir = fs.mkdir(name_);

  // The cut to apply
  if (pset.exists("cut"))
    cut_.reset(new StringCutT(pset.getParameter<std::string>("cut"), true));

  // Plots to make after cut is applied
  if (pset.exists("plot"))
    folder_.reset(
        new HistoFolderT(pset.getParameter<std::string>("plot"), subdir));

  // Plots to make before cut is applied
  if (pset.exists("plotBefore"))
    folderBefore_.reset(
        new HistoFolderT(pset.getParameter<std::string>("plotBefore"), subdir));

  // Declare cut monitor histo if we are cutting
  if (cut_.get()) {
    cutHisto_ = subdir.make<TH1F>(name_, description_, 2, -0.5, 1.5);
    cutHisto_->GetXaxis()->SetTitle("Filter result");
  }
}

template<class T> bool
AnalysisCutHolder<T>::analyze(const T& object, double weight) const {
  // Make the pre-cut plots, if desired
  if (folderBefore_.get()) {
    folderBefore_->fill(object, weight);
  }
  // Get cut result
  bool pass = true;
  if (cut_.get()) {
    pass = (*cut_)(object);
    cutHisto_->Fill(pass);
  }
  // Fill after plots
  if (pass) {
    folder_->fill(object, weight);
  }
  return pass;
}

template<class T> std::auto_ptr<VectorPtrT>
AnalysisCutHolder<T>::analyze(const VectorPtrT& objects, double weight) const {
  std::auto_ptr<VectorPtrT> output(new VectorPtrT);
  // Analyze each object in turn
  for (size_t i = 0; i < objects.size(); ++i) {
    const T* object = objects[i];
    assert(object);
    bool passes = analyze(*object);
    if (passes)
      output->push_back(object);
  }
}


#endif /* end of include guard: ANALYSISCUTHOLDER_1SUHQMG4 */
