/*
 * Template class for making a selection one single branch
 *
 * Different types of selectors should implement "selectValue"
 */

#ifndef TMEGABRANCHSELECTIONT_HENJDCUZ
#define TMEGABRANCHSELECTIONT_HENJDCUZ

#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelection.h"
#include "TBranchProxy.h"

template<typename T>
class TMegaBranchSelectionT : public TMegaSelection {
  public:
    TMegaBranchSelectionT(){} // Default constructor for I/O

    /// Normal constructor giving branch name and director
    TMegaBranchSelectionT(ROOT::TBranchProxyDirector* director,
        const char* name):branch_(director, name){}

    /// Clone method
    virtual TMegaBranchSelectionT<T>* Clone() const=0;

    virtual ~TMegaBranchSelectionT(){}

    /// Apply the selection to the given branch
    Bool_t Select() {
      // Get the branch value
      T value = branch_;
      return SelectValue(value);
    }

    // The select function is still abstract as we don't know what to
    // compare it to.
    virtual Bool_t SelectValue(const T& value) const =0;

  private:
    ROOT::TImpProxy<T> branch_;
};

#endif /* end of include guard: TMEGABRANCHSELECTIONT_HENJDCUZ */
