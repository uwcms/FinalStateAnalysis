/*
 * Generate missing dictionaries for RooFit iterators to support PyROOT
 *
 * See: http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=11376
 */
#include <list>
#include "RooAbsData.h"

#ifdef __CINT__
#pragma link C++ class std::list<RooAbsData*>::iterator;
#endif
