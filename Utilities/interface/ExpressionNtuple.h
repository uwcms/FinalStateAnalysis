/*
 * Tool to build a TTree of floats of from StringObjectFunctions
 *
 * Author: Evan K. Friis, UC Davis
 *
 */

#ifndef EXPRESSIONNTUPLE_XZ7TV8E1
#define EXPRESSIONNTUPLE_XZ7TV8E1

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"

#include "TTree.h"

template<class T>
class ExpressionNtuple {
  public:
    ExpressionNtuple(const edm::ParameterSet& pset);
    ~ExpressionNtuple();

    // Setup the tree in the given TFile
    void initialize(TFileDirectory& fs);
    // Fill the tree with an element with given index.
    void fill(const T& element, int idx = -1);
    // Get access to the internal tree
    TTree* tree() const { return tree_; }
  private:
    struct Column {
      Column(const std::string& n, const std::string& f):
        name(n),func(f, true) {
        branch.reset(new Float_t);
      }
      std::string name;
      StringObjectFunction<T> func;
      boost::shared_ptr<Float_t> branch;
    };
    TTree* tree_;
    boost::shared_ptr<Int_t> idxBranch_;
    std::vector<Column> columns_;
};


template<class T>
ExpressionNtuple<T>::ExpressionNtuple(const edm::ParameterSet& pset) {
  tree_ = NULL;
  typedef std::vector<std::string> vstring;
  vstring columnNames = pset.getParameterNames();
  std::set<std::string> enteredAlready;
  for (size_t i = 0; i < columnNames.size(); ++i) {
    const std::string& colName = columnNames[i];
    if (enteredAlready.count(colName)) {
      throw cms::Exception("DuplicatedBranch")
        << " The ntuple branch with name " << colName
        << " has already been registered!" << std::endl;
    }
    enteredAlready.insert(colName);
    // Build the function object
    Column newCol(colName, pset.getParameter<std::string>(colName));
    columns_.push_back(newCol);
  }
  idxBranch_.reset(new Int_t);
}

template<class T> ExpressionNtuple<T>::~ExpressionNtuple() {}

template<class T> void ExpressionNtuple<T>::initialize(TFileDirectory& fs) {
  tree_ = fs.make<TTree>("Ntuple", "Expression Ntuple");
  // Build branches
  for (size_t i = 0; i < columns_.size(); ++i) {
    const Column& col = columns_[i];
    std::string branchCmd = col.name + "/F";
    tree_->Branch(col.name.c_str(), col.branch.get(), branchCmd.c_str());
  }
  tree_->Branch("idx", idxBranch_.get(), "idx/I");
}

template<class T> void ExpressionNtuple<T>::fill(const T& element, int idx) {
  for (size_t i = 0; i < columns_.size(); ++i) {
    Column& col = columns_[i];
    const StringObjectFunction<T>& func = col.func;
    *(col.branch) = func(element);
  }
  *idxBranch_ = idx;
  tree_->Fill();
}

#endif /* end of include guard: EXPRESSIONNTUPLE_XZ7TV8E1 */
