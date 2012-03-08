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
#include <vector>

class PileupSummaryInfo;

/// Get the 3D pileup weight using the given data and MC scenarios
/// See the src file for available data and MC tags
double get3DPileupWeight(const std::string& dataTag, const std::string& mcTag,
    const std::vector<PileupSummaryInfo>& puInfo);
