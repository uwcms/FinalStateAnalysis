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

#include <string>

/// See the data and MC tags must be defined in
/// DataAlgos/data/pileup_distributions.py
double getPileupWeight(const std::string& dataTag, const std::string& mcTag,
    double nTrueInteractions);
