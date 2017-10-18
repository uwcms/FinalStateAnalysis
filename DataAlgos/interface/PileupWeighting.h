/*
 * =============================================================================
 *
 *       Filename:  PileupWeighting.h
 *
 *    Description:  Tools for reweighting PAT Final State events
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =============================================================================
 */

#include <boost/shared_ptr.hpp>
#include <memory>
#include <string>

/// See the data and MC tags must be defined in
/// DataAlgos/data/pileup_distributions.py
double getPileupWeight(const std::string& dataTag, const std::string& mcTag,
    double nTrueInteractions);


// Some jerk decided it's really important that we use std::shared_ptr instead
// of boost::shared_ptr, because who needs backwards compatibility? So here's 
// some magic.
// From http://stackoverflow.com/questions/12314967/cohabitation-of-boostshared-ptr-and-stdshared-ptr

template<typename T>
boost::shared_ptr<T> make_shared_ptr(boost::shared_ptr<T> ptr)
{
  return ptr;
}

template<typename T>
boost::shared_ptr<T> make_shared_ptr(std::shared_ptr<T> ptr)
{
  return boost::shared_ptr<T>(ptr.get(), [ptr](T*) mutable {ptr.reset();});
}


