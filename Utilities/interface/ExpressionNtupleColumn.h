/*
 * ExpressionNtupleColumn
 *
 * Abstract base class which fills the appropriate branch variable
 *
 * ExpressionNtupleColumnT
 *
 * which handles different branch types, I, F, and D.
 *
 * The user should utilize the factory function:
 * std::auto_ptr<ExpressionNtupleColumn<T> > buildColumn<T>(
 *  const std::string& name, const edm::ParameterSet& pset, TTree* tree);
 *
 * Author: Evan K. Friis, UW Madison
 *         Lindsey Gray, UW Madison (for vector specializations)
 *
 */

#ifndef EXPRESSIONNTUPLECOLUMN_VOU3DWMC
#define EXPRESSIONNTUPLECOLUMN_VOU3DWMC

#include <TTree.h>
#include <TLeaf.h>
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include <TMath.h>
#include <iostream>
#include <sstream>
#include "FWCore/Utilities/interface/TypeWithDict.h"

template<typename ObjType>
class ExpressionNtupleColumn {
public:
    /// Compute the column function and store result in branch variable
  void compute(const ObjType& obj);
protected:
  /// Abstract function which takes the result from the compute and fills the
  /// branch
  virtual void setValue(double value) = 0;
  virtual void setValue(const std::vector<double>& value) = 0;
  ExpressionNtupleColumn(const std::string& name, const std::string& func);
private:
  std::string name_, expression_;
  StringObjectFunction<ObjType> func_;
};

template<typename T>
ExpressionNtupleColumn<T>::ExpressionNtupleColumn(
    const std::string& name, const std::string& func):
name_(name), expression_(func), func_(func, true) {}

template<typename T> void ExpressionNtupleColumn<T>::compute(const T& obj) {
    try{
      this->setValue(func_(obj));
    } catch(cms::Exception& iException) {
      iException << "Caught exception in evaluating branch: "
        << name_ << " with formula: " << expression_;
      throw;
    }
}

//vector specialization for base class
template<typename T>
class ExpressionNtupleColumn<std::vector<const T*> > {
public:
  /// Compute the column function and store result in branch variable
  void compute(const std::vector<const T*>& obj);
protected:
  /// Abstract function which takes the result from the compute and fills the
  /// branch
  virtual void setValue(double value) = 0;
  virtual void setValue(const std::vector<double>& value) = 0;
  ExpressionNtupleColumn(const std::string& name, const std::string& func);
private:
  std::string name_;
  StringObjectFunction<T> func_;
};

template<class T>
ExpressionNtupleColumn<std::vector<const T*> >::ExpressionNtupleColumn(
    const std::string& name, const std::string& func):
  name_(name), func_(func, true) {}

template<class T>
void ExpressionNtupleColumn<std::vector<const T*> >::compute(
    const std::vector<const T*>& obj) {
  std::vector<double> result;
  typename std::vector<const T*>::const_iterator i = obj.begin();
  typename std::vector<const T*>::const_iterator e = obj.end();
  for( ; i != e; ++i ) {
    result.push_back(func_(*(*i)));

  }
  this->setValue(result);
}

namespace {
  namespace {
    typedef std::vector<double> vdouble;
  }
  template<typename T> std::string getTypeCmd();
  template<> std::string getTypeCmd<Float_t>() { return "/F"; }
  template<> std::string getTypeCmd<Int_t>() { return "/I"; }
  template<> std::string getTypeCmd<UInt_t>() { return "/i"; }
  template<> std::string getTypeCmd<Long64_t>() { return "/L"; }
  template<> std::string getTypeCmd<ULong64_t>() { return "/l"; }
  template<> std::string getTypeCmd<Double_t>() { return "/D"; }

  template<typename T> T convertVal(double x);
  template<> Double_t convertVal<Double_t>(double x) { return x; }
  template<> Float_t convertVal<Float_t>(double x) { return x; }
  template<> Int_t convertVal<Int_t>(double x) { return TMath::Nint(x); }
  template<> UInt_t convertVal<UInt_t>(double x) { return TMath::Nint(fabs(x)); }
  template<> Long64_t convertVal<Long64_t>(double x) { return lrint(x); }
  template<> ULong64_t convertVal<ULong64_t>(double x) { return lrint(fabs(x)); }
  //vector spec
  template<typename T> std::vector<T> convertVector(const vdouble& x) {
    std::vector<T> result;
    vdouble::const_iterator i = x.begin();
    vdouble::const_iterator e = x.end();
    for( ; i != e; ++i) result.push_back(convertVal<T>(*i));
    return result;
  }
  template<typename T> std::vector<T> convertVal(const vdouble& x) {return convertVector<T>(x);}
  // template<> std::vector<Double_t> convertVal<Double_t>(const vdouble& x) {
  //   return convertVector<Double_t>(x);
  // }
  // template<> std::vector<Float_t> convertVal<Float_t>(const vdouble& x) {
  //   return convertVector<Float_t>(x);
  // }
  // template<> std::vector<Int_t> convertVal<Int_t>(const vdouble& x) {
  //   return convertVector<Int_t>(x);
  // }
  // template<> std::vector<UInt_t> convertVal<UInt_t>(const vdouble& x) {
  //   return convertVector<UInt_t>(x);
  // }
  // template<> std::vector<Long64_t> convertVal<Long64_t>(const vdouble& x) {
  //   return convertVector<Long64_t>(x);
  // }
  // template<> std::vector<ULong64_t> convertVal<ULong64_t>(const vdouble& x) {
  //   return convertVector<ULong64_t>(x);
  // }
  // template<> std::vector<Double_t> convertVal<Double_t>(const vdouble& x) {
  //   std::vector<Double_t> result;
  //   vdouble::const_iterator i = x.begin();
  //   vdouble::const_iterator e = x.end();
  //   for( ; i != e; ++i) result.push_back(*i);
  //   return result;
  // }
  // template<> std::vector<Float_t> convertVal<Float_t>(const vdouble& x) {
  //   std::vector<Float_t> result;
  //   vdouble::const_iterator i = x.begin();
  //   vdouble::const_iterator e = x.end();
  //   for( ; i != e; ++i) result.push_back(*i);
  //   return result;
  // }
  // template<> std::vector<Int_t> convertVal<Int_t>(const vdouble& x) {
  //   std::vector<Int_t> result;
  //   vdouble::const_iterator i = x.begin();
  //   vdouble::const_iterator e = x.end();
  //   for( ; i != e; ++i) result.push_back(TMath::Nint(*i));
  //   return result;
  // }
}

// Explicit typed (float, double, etc) ntuple column
template<typename ObjType, typename ColType>
class ExpressionNtupleColumnT : public ExpressionNtupleColumn<ObjType> {
  public:

  static ExpressionNtupleColumnT* makeExpression(const std::string& name,
						 const std::string& func,
						 TTree* tree) {
    try{
      return new ExpressionNtupleColumnT(name, func, tree);
    } catch(cms::Exception& iException) {
      iException << "Caught exception in building branch: "
        << name << " with formula: " << func;
      throw;
    }
  }

  protected:
    /// Abstract function
    ExpressionNtupleColumnT(const std::string& name, const std::string& func,
			    TTree* tree);

    void setValue(double value);
    void setValue(const std::vector<double>&) {}
  private:
    boost::shared_ptr<ColType> branch_;
};

// Explicit typed (float, double, etc) ntuple column
template<typename ObjType, typename ColType>
ExpressionNtupleColumnT<ObjType, ColType>::ExpressionNtupleColumnT(
    const std::string& name, const std::string& func, TTree* tree):
  ExpressionNtupleColumn<ObjType>(name, func) {
    branch_.reset(new ColType);
    std::string branchCmd = name + getTypeCmd<ColType>();
    tree->Branch(name.c_str(), branch_.get(), branchCmd.c_str());
}

template<typename ObjType, typename ColType>
void ExpressionNtupleColumnT<ObjType, ColType>::setValue(double value) {
  *branch_ = convertVal<ColType>(value);
}

template<typename T>
std::auto_ptr<ExpressionNtupleColumn<T> > buildColumn(
    const std::string& name, const edm::ParameterSet& pset, TTree* tree) {

  // The output column
  std::auto_ptr<ExpressionNtupleColumn<T> > output;

  typedef std::vector<std::string> vstring;

  // In the default case (no type specifier) default to float
  if (pset.existsAs<std::string>(name)) {
    output.reset( ExpressionNtupleColumnT<T, Float_t>::makeExpression(name,
          pset.getParameter<std::string>(name), tree));
  } else if (pset.existsAs<vstring>(name)){
    vstring command = pset.getParameter<vstring>(name);
    if (command.size() != 2) {
      throw cms::Exception("BadTypeSpecifier")
        << "The column " << name << " is declared as a cms.vstring, "
        << " but doesnt not have the required format"
        << " cms.vstring('function', 'type')" << std::endl;
    }
    if (command[1] == "I") {
      // Make a integer column
      output.reset( ExpressionNtupleColumnT<T, Int_t>::makeExpression(name,
            command[0], tree));
     } else if (command[1] == "i") {
       // Make an unsigned integer column
       output.reset( ExpressionNtupleColumnT<T, UInt_t>::makeExpression(name,
             command[0], tree));
     } else if (command[1] == "L") {
       // Make a long column
       output.reset( ExpressionNtupleColumnT<T, Long64_t>::makeExpression(name,
             command[0], tree));
     } else if (command[1] == "l") {
       // Make an unsigned long column
       output.reset( ExpressionNtupleColumnT<T, ULong64_t>::makeExpression(name,
             command[0], tree));
    } else if (command[1] == "F" || command[1] == "f") {
      // Make a float column
      output.reset( ExpressionNtupleColumnT<T, Float_t>::makeExpression(name,
            command[0], tree));
    } else if (command[1] == "D" || command[1] == "d") {
      // Make a double column
      output.reset( ExpressionNtupleColumnT<T, Double_t>::makeExpression(name,
            command[0], tree));
    } else {
      throw cms::Exception("BadTypeSpecifier")
        << "The column " << name << " has declared type " << command[1]
        << ", which I don't understand.  Allowed: I, i, L, l, F, and D" << std::endl;
    }
  } else {
      throw cms::Exception("BadColumn")
        << "The column " << name << " is not a cms.vstring or cms.string!"
        << std::endl;
  }
  return output;
}

// template specialization for vectors
template<typename T, typename ColType>
class ExpressionNtupleColumnT<std::vector<const T*>, ColType> :
     public ExpressionNtupleColumn<std::vector<const T*> > {
  public:

  static ExpressionNtupleColumnT*
    makeExpression(const std::string& name,
		   const std::string& func,
		   TTree* tree)
    {
      try{
	return new ExpressionNtupleColumnT(name, func, tree);
      }
      catch(cms::Exception& iException){
        iException << "Caught exception in building branch: "
          << name << " with formula: " << func;
	throw;
      }
    }

 protected:
  /// Abstract function
  ExpressionNtupleColumnT(const std::string& name,
				 const std::string& func,
				 TTree* tree);
  // template specialization for vector inputs
  void setValue(double) {}
  void setValue(const std::vector<double>& value);
 private:
  TLeaf* counter_;
  boost::shared_ptr<ColType> branch_;
  TTree* const myparent_;
  const std::string branchname_;
};

// Explicit typed (float, double, etc) ntuple column
template<typename T, typename ColType>
ExpressionNtupleColumnT<std::vector<const T*>, ColType>::
ExpressionNtupleColumnT(const std::string& name,
			const std::string& func, TTree* tree):
  ExpressionNtupleColumn<std::vector<const T*> >(name, func),
  myparent_(tree),
  branchname_(name) {
  branch_.reset(new ColType[1]);

  std::stringstream idxwrap;
  edm::TypeWithDict t(typeid(T));
  idxwrap << "[N_" << t.name() << "]";

  std::string branchCmd = name + idxwrap.str() + getTypeCmd<ColType>();
  std::string fullName = name;

  tree->Branch(fullName.c_str(), branch_.get(), branchCmd.c_str());
}

namespace {
  template<typename T>
  struct array_deleter{
    void operator () (T* arr) { delete [] arr; }
  };
}

template<typename T, typename ColType>
void ExpressionNtupleColumnT<std::vector<const T*>, ColType>::
setValue(const std::vector<double>& value) {
  // create a new array
  std::vector<ColType> thevals = convertVal<ColType>(value);
  const unsigned arrSize = thevals.size();
  ColType * newValues = new ColType[arrSize];
  // read in the new values
  for( unsigned i = 0; i < arrSize; ++i ) {
    newValues[i] = thevals[i];
  }
  // replace old values
  branch_.reset(newValues,array_deleter<ColType>());
  myparent_->GetBranch(branchname_.c_str())->SetAddress(branch_.get());
}

#endif /* end of include guard: EXPRESSIONNTUPLECOLUMN_VOU3DWMC */
