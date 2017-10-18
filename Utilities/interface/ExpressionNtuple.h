/*
 * Tool to build a TTree of columns of from StringObjectFunctions.
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#ifndef EXPRESSIONNTUPLE_XZ7TV8E1
#define EXPRESSIONNTUPLE_XZ7TV8E1

#include "boost/utility.hpp"
 #include <boost/ptr_container/ptr_vector.hpp>

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "TTree.h"
#include "FWCore/Utilities/interface/TypeWithDict.h"

#include "FinalStateAnalysis/Utilities/interface/ExpressionNtupleColumn.h"

#include <sstream>

template<class T>
class ExpressionNtuple : private boost::noncopyable {
  public:
    ExpressionNtuple(const edm::ParameterSet& pset);
    ~ExpressionNtuple();

    // Setup the tree in the given TFile
    void initialize(TFileDirectory& fs);
    // Fill the tree with an element with given index.
    // If do_commit is true, the held TTree is filled at the end
    // of the fill() function
    void fill(const T& element, int idx = -1, bool do_commit=true);
    // Fill the held TTree based on the current branches
    void commit() { tree_->Fill(); }
    // Get access to the internal tree
    TTree* tree() const { return tree_; }
  private:
    TTree* tree_;
    std::vector<std::string> columnNames_;
    edm::ParameterSet pset_;
    boost::ptr_vector<ExpressionNtupleColumn<T> > columns_;
    boost::shared_ptr<Int_t> idxBranch_;
};

template<class T>
ExpressionNtuple<T>::ExpressionNtuple(const edm::ParameterSet& pset):
  pset_(pset) {
  tree_ = NULL;
  typedef std::vector<std::string> vstring;
  // Double check no column already exists
  columnNames_ = pset.getParameterNames();
  std::set<std::string> enteredAlready;
  for (size_t i = 0; i < columnNames_.size(); ++i) {
    const std::string& colName = columnNames_[i];
    if (enteredAlready.count(colName)) {
      throw cms::Exception("DuplicatedBranch")
        << " The ntuple branch with name " << colName
        << " has already been registered!" << std::endl;
    }
    enteredAlready.insert(colName);
  }
  idxBranch_.reset(new Int_t);
}

template<class T> ExpressionNtuple<T>::~ExpressionNtuple() {}

template<class T> void ExpressionNtuple<T>::initialize(TFileDirectory& fs) {
  tree_ = fs.make<TTree>("Ntuple", "Expression Ntuple");
  // Build branches
  for (size_t i = 0; i < columnNames_.size(); ++i) 
    columns_.push_back(buildColumn<T>(columnNames_[i], pset_, tree_));
  // A special branch so we know which subrow we are on.
  tree_->Branch("idx", idxBranch_.get(), "idx/I");
}

template<class T> void ExpressionNtuple<T>::fill(const T& element, 
						 int idx,
						 bool do_commit) {
  for (size_t i = 0; i < columns_.size(); ++i) {
    // Compute the function and load the value into the column.
    columns_[i].compute(element);
  }
  *idxBranch_ = idx;
  if( do_commit )
    commit();
}
 
// vector template specialization
template<class T>
class ExpressionNtuple<std::vector<const T*> > : private boost::noncopyable {
 public:
  ExpressionNtuple(const edm::ParameterSet& pset);
  ~ExpressionNtuple();
  
  // Setup the tree in the given TFile
  void initialize(TFileDirectory& fs);
  // Fill the tree with an element with given index.
  void fill(const std::vector<const T*>& element, int idx = -1, 
	    bool do_commit=true);
  // Fill the held TTree based on the current branches
    void commit() { tree_->Fill(); }
  // Get access to the internal tree
  TTree* tree() const { return tree_; }
 private:
  TTree* tree_;
  std::vector<std::string> columnNames_;
  edm::ParameterSet pset_;
  boost::ptr_vector<ExpressionNtupleColumn<std::vector<const T*> > > columns_;
  boost::shared_ptr<Int_t> idxBranch_;  
};

template<class T>
ExpressionNtuple<std::vector<const T*> >::
ExpressionNtuple(const edm::ParameterSet& pset):
  pset_(pset) {
  tree_ = NULL;
  typedef std::vector<std::string> vstring;
  // Double check no column already exists
  columnNames_ = pset.getParameterNames();
  std::set<std::string> enteredAlready;
  for (size_t i = 0; i < columnNames_.size(); ++i) {
    const std::string& colName = columnNames_[i];
    if (enteredAlready.count(colName)) {
      throw cms::Exception("DuplicatedBranch")
        << " The ntuple branch with name " << colName
        << " has already been registered!" << std::endl;
    }
    enteredAlready.insert(colName);
  }
  idxBranch_.reset(new Int_t(1));
}

template<class T> 
ExpressionNtuple<std::vector<const T*> >::~ExpressionNtuple() {}

template<class T> 
void ExpressionNtuple<std::vector<const T*> >::initialize(TFileDirectory& fs) {
  tree_ = fs.make<TTree>("Ntuple", "Expression Ntuple");
  // build the index branch
  std::stringstream name, leaf;
  edm::TypeWithDict t(typeid(T));
  name << "N_"  << t.name();
  leaf << name.str() << "/I";
  
  // In this specialization the idx is allows us to have
  // variable length leaves
  tree_->Branch(name.str().c_str(), idxBranch_.get(), leaf.str().c_str());
  // Build branches
  for (size_t i = 0; i < columnNames_.size(); ++i)
    columns_.push_back(buildColumn<std::vector<const T*> >(columnNames_[i], 
							   pset_, tree_));
}

template<class T> 
void ExpressionNtuple<std::vector<const T*> >::
fill(const std::vector<const T*> & element, int idx, bool do_commit) {
  for (size_t i = 0; i < columns_.size(); ++i) {
    // Compute the function and load the value into the column.
    columns_[i].compute(element);
  }
  *idxBranch_ = element.size();
  if( do_commit && element.size() )
    commit();
}

#endif /* end of include guard: EXPRESSIONNTUPLE_XZ7TV8E1 */
