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

class PileupSummaryInfo;
#include <string>

/// Get the pileup weight using the given mode and data and MC scenarios
double getPileupWeight(const std::string& mode,
    const std::string& dataTag, const std::string& mcTag,
    const PileupSummaryInfo& puInfo);
