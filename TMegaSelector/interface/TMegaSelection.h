/*
 * Abstract base class for a selection on a TTree.
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#ifndef TMEGASELECTION_M8MSCS4R
#define TMEGASELECTION_M8MSCS4R

#include "Rtypes.h"

class TMegaSelection {
  public:
    TMegaSelection(){}
    virtual ~TMegaSelection(){}
    virtual TMegaSelection* Clone() const=0;

    /// Apply the selection implementation
    virtual Bool_t Select() =0;
};

#endif /* end of include guard: TMEGASELECTION_M8MSCS4R */
