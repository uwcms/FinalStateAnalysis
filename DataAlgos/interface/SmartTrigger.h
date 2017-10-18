#ifndef SMARTTRIGGER_ZE9BQMEK
#define SMARTTRIGGER_ZE9BQMEK

/*
 * Choose the trigger to use from a list in a smart way.
 *
 * Author: Evan K. Friis, UW Madison
 *
 * The SmartTrigger is passed a comma separated list of TriggerGroups.
 *
 *      example: "A|B, B_v*, C_v*"
 *
 * If [ez] is true, use the friendly '*' syntax.  Otherwise use boost::regexp.
 *
 * This example has three trigger groups,
 *
 * 1) A OR B
 * 2) B
 * 3) C
 *
 *
 * The SmartTrigger would first check group 1 (A || B) to see if A and B had
 * the same prescale. If not, it considers the combo trigger untractable and
 * marks it as invalid.
 *
 * The SmartTrigger then takes the Trigger with the lowest prescale in the list,
 * with preference given to the triggers listed earlier.
 *
 * The SmartTrigger returns a SmartTriggerResult object giving the group index,
 * result, and prescale of the chosen trigger.  If none of the groups are found,
 * it will return index = NGroups
 *
 */

#include <string>
#include <vector>
// Fwd Declarations
namespace pat {
  class TriggerEvent;
  class TriggerPath;
  class TriggerFilter;
  class TriggerObjectStandAlone;
  class PackedTriggerPrescales;
}
namespace edm {
  class EventID;
  class TriggerResults;
  class TriggerNames;
}

struct SmartTriggerResult {
  unsigned int group;
  unsigned int prescale;
  std::vector<std::string> paths;
  bool passed;
};

/// Get the result for a single event using the pat::TriggerEvent
SmartTriggerResult smartTrigger(
    const std::string& trgs, const pat::TriggerEvent& trgResult,
    bool ez=false);

/// Get the result for a single event using the pat::TriggerObjectStandAlone
SmartTriggerResult smartTrigger(
    const std::string& trgs, const edm::TriggerNames& names, 
    const pat::PackedTriggerPrescales& trgPrescales,
    const edm::TriggerResults& trgResults,
    bool ez=false);

/// This version caches the results across events to speed things up.
const SmartTriggerResult& smartTrigger(
    const std::string& trgs, const pat::TriggerEvent& trgResult,
    const edm::EventID& event, bool ez=false);

/// Get the result for a single event using the pat::TriggerObjectStandAlone
const SmartTriggerResult& smartTrigger(
    const std::string& trgs, const edm::TriggerNames& names,
    const pat::PackedTriggerPrescales& trgPrescales,
    const edm::TriggerResults& trgResults,
    const edm::EventID& event, bool ez=false);

/// Get the list of trigger paths matching a given pattern.  If [ez] is
// true, use the friendly '*' syntax.  Otherwise use boost::regexp.
std::vector<const pat::TriggerPath*> matchingTriggerPaths(
    const pat::TriggerEvent& result,
    const std::string& pattern, bool ez=false);

std::vector<int> matchingTriggerPaths(
    const edm::TriggerNames& names,
    const pat::PackedTriggerPrescales& trgPrescales,
    const edm::TriggerResults& trgResults,
    const std::string& pattern, bool ez=false);

/// Get the list of trigger filters matching a given pattern.
std::vector<const pat::TriggerFilter*> matchingTriggerFilters(
    const pat::TriggerEvent& result,
    const std::string& pattern, bool ez=false);

std::vector<const pat::TriggerFilter*> matchingTriggerFilters(
    const std::vector<pat::TriggerObjectStandAlone>& trgObject, const edm::TriggerNames& names,
    const std::string& pattern, bool ez=false);

/* std::vector<const pat::TriggerFilter*> matchingTriggerFilters( */
/*     const std::vector<pat::TriggerObjectStandAlone>& trgObject, const edm::TriggerNames& names, const edm::Event& evt,const edm::TriggerResults& trgResults, */
/*     const std::string& pattern, bool ez=false); */

/// Expose decision making method for testing.  Not for general use.
SmartTriggerResult makeDecision(
    const std::vector<std::vector<std::string> >& paths,
    const std::vector<std::vector<unsigned int> >& prescales,
    const std::vector<std::vector<unsigned int> >& results);


#endif /* end of include guard: SMARTTRIGGER_ZE9BQMEK */
