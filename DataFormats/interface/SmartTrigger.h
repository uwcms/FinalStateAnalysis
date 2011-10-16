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
}
class LumiSummary;

struct SmartTriggerResult {
  unsigned int group;
  unsigned int prescale;
  bool passed;
};

/// Get the result for a single event using the pat::TriggerEvent
SmartTriggerResult smartTrigger(
    const std::string& trgs, const pat::TriggerEvent& trgResult);

/// Get the result for a whole lumi section.
SmartTriggerResult smartTrigger(
    const std::string& trgs, const LumiSummary& lumiSummary);

/// Expose main method for testing.  Not for general use.
SmartTriggerResult makeDecision(
    const std::vector<std::vector<unsigned int> >& prescales,
    const std::vector<std::vector<unsigned int> >& results);


#endif /* end of include guard: SMARTTRIGGER_ZE9BQMEK */
