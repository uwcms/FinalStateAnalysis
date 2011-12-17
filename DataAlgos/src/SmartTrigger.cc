#include "FinalStateAnalysis/DataAlgos/interface/SmartTrigger.h"

#include <string>
#include <vector>

#include <boost/regex.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/erase.hpp>
#include <boost/algorithm/string/regex.hpp>

#include "FWCore/Utilities/interface/RegexMatch.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"

typedef std::vector<std::string> vstring;

// Internal functions
namespace {

vstring getGroups(const std::string& trgGrps) {
  vstring tokens;
  std::string clean = boost::algorithm::erase_all_copy(trgGrps, " ");
  boost::split(tokens, clean, boost::is_any_of(","));
  return tokens;
}

vstring getPaths(const std::string& grp) {
  vstring tokens;
  boost::split_regex(tokens, grp, boost::regex(" OR "));
  return tokens;
}

// Get the index of the item matching [glob] in [paths].
size_t
getFullName(const std::string& glob, const vstring& paths) {
  boost::regex regexp(glob);
  size_t result = paths.size();
  for (size_t i = 0; i < paths.size(); ++i) {
    if (boost::regex_match(paths[i], regexp)) {
      // Make sure only one path matches our glob.
      if (result != paths.size())
        throw;
      else
        result = i;
    }
  }
  return result;
}

unsigned int
getPrescale(const std::string& path, const pat::TriggerEvent& trgResult) {
  return 999;
}

unsigned int
getPrescale(const std::string& path, const LumiSummary& trgResult) {
  return 999;
}

typedef std::vector<unsigned int>  VInt;
typedef std::vector<VInt> VVInt;
typedef std::vector<vstring> VVString;

// Choose which group to use, given the prescales
unsigned int
chooseGroup(const VVInt& prescales) {
  // Find the lowest prescale
  unsigned int lowest = std::numeric_limits<unsigned int>::max();
  unsigned int bestGroup = prescales.size();

  for (size_t i = 0; i < prescales.size(); ++i) {
    // Now check if this group is consistent
    unsigned int minInGrp = std::numeric_limits<unsigned int>::max();
    unsigned int maxInGrp = 0;
    for (size_t j = 0; j < prescales[i].size(); ++j) {
      if (prescales[i][j] < minInGrp)
        minInGrp = prescales[i][j];
      if (prescales[i][j] > maxInGrp)
        maxInGrp = prescales[i][j];
    }
    // Make sure all items have the same prescale.  If not, skip this group.
    if (minInGrp != maxInGrp)
      continue;
    // If the prescale is zero, the trigger is off. Skip it.
    if (minInGrp == 0)
      continue;
    // Otherwise use this one (as it comes first) if it has a LOWER prescale
    // Not LT not LTE
    if (minInGrp < lowest) {
      lowest = minInGrp;
      bestGroup = i;
    }
  }
  return bestGroup;
}

} // End internal functions

// Get the list of regexp matching trigger paths from the pat::TriggerEvent
std::vector<const pat::TriggerPath*> matchingTriggerPaths(
    const pat::TriggerEvent& result,
    const std::string& pattern, bool ez) {
  std::vector<const pat::TriggerPath*> output;
  try {
    boost::regex matcher(ez ? edm::glob2reg(pattern) : pattern);
    const pat::TriggerPathCollection* paths = result.paths();
    for (size_t i = 0; i < paths->size(); ++i) {
      if (boost::regex_match(paths->at(i).name(), matcher)) {
        output.push_back(&paths->at(i));
      }
    }
  } catch (std::exception& e) {
    edm::LogError("PathRegexParse") << "Caught exception when parsing"
      << " trigger path regex expression: [" << pattern << "]" << std::endl;
    throw;
  }
  return output;
}

std::vector<const pat::TriggerFilter*>
matchingTriggerFilters(const pat::TriggerEvent& result,
    const std::string& pattern, bool ez) {
  std::vector<const pat::TriggerFilter*> output;
  boost::regex matcher(ez ? edm::glob2reg(pattern) : pattern);
  const pat::TriggerFilterCollection* filters = result.filters();
  for (size_t i = 0; i < filters->size(); ++i) {
    if (boost::regex_match(filters->at(i).label(), matcher))
      output.push_back(&filters->at(i));
  }
  return output;
}

std::vector<LumiSummary::HLT> matchingTriggerPathsLumi(
    const LumiSummary& result, const std::string& pattern, bool ez) {
  std::vector<LumiSummary::HLT> output;
  boost::regex matcher(ez ? edm::glob2reg(pattern) : pattern);
  std::vector<std::string> paths = result.HLTPaths();
  for (size_t i = 0; i < paths.size(); ++i) {
    //std::cout << " path: " << paths->at(i).name() << " " << pattern;
    if (boost::regex_match(paths[i], matcher)) {
      output.push_back(result.hltinfo(i));
      //std::cout << " match!";
    }
    //std::cout << std::endl;
  }
  return output;
}

SmartTriggerResult makeDecision(
    const VVString& paths, const VVInt& prescales, const VVInt& results) {
  unsigned int prescale = 0;
  bool passed = false;
  unsigned int group = chooseGroup(prescales);
  vstring chosenPaths;
  if (group < prescales.size()) {
    // We know by construction the prescales are the same in the whole group
    prescale = prescales[group][0];
    for (size_t i = 0; i < results[group].size(); ++i) {
      if (results[group][i]) {
        passed = true;
        // Push back all the paths that passed
        chosenPaths.push_back(paths[group][i]);
      }
    }
  }
  SmartTriggerResult output;
  output.paths = chosenPaths;
  output.group = group;
  output.prescale = prescale;
  output.passed = passed;
  return output;
}

SmartTriggerResult
smartTrigger(const std::string& trgs, const pat::TriggerEvent& result) {
  // Tokenize the trigger groups
  vstring groups = getGroups(trgs);
  VVInt prescales;
  VVInt results;
  VVString pathGroups;
  for (size_t i = 0; i < groups.size(); ++i) {
    // Get the paths in this group
    VInt groupPrescale;
    VInt groupResult;
    vstring paths = getPaths(groups[i]);
    for (size_t p = 0; p < paths.size(); ++p) {
      const std::string& path = paths[p];
      // Get all the triggers that match this path pattern.  There should be
      // only one.  The point of the smart trigger is that each path type is a
      // separate group.
      std::vector<const pat::TriggerPath*> matching =
        matchingTriggerPaths(result, path);
      if (matching.size() > 1) {
        std::stringstream err;
        err << "Error: more than one"
          << " paths match pattern: " << path << ", taking first!" << std::endl
          << " Matches: " << std::endl;
        for (size_t i = 0; i < matching.size(); ++i) {
          err << i << ": " << matching[i]->name() << std::endl;
        }
        edm::LogError("SmartTriggerMultiMatchHLT") << err.str();
      }
      const pat::TriggerPath* trgPath = matching.size() ? matching[0] : NULL;
      int thePrescale = (trgPath != NULL) ? trgPath->prescale() : 0;
      int theResult = (trgPath != NULL) ? trgPath->wasAccept() : -1;
      groupPrescale.push_back(thePrescale);
      groupResult.push_back(theResult);
    }
    pathGroups.push_back(paths);
    prescales.push_back(groupPrescale);
    results.push_back(groupResult);
  }
  return makeDecision(pathGroups, prescales, results);
}

SmartTriggerResult
smartTrigger(const std::string& trgs, const LumiSummary& result) {
  // Tokenize the trigger groups
  vstring groups = getGroups(trgs);
  VVInt prescales;
  VVInt results;
  VVString pathGroups;
  for (size_t i = 0; i < groups.size(); ++i) {
    // Get the paths in this group
    VInt groupPrescale;
    VInt groupResult;
    vstring paths = getPaths(groups[i]);
    for (size_t p = 0; p < paths.size(); ++p) {
      const std::string& path = paths[p];
      std::vector<LumiSummary::HLT> matching =
        matchingTriggerPathsLumi(result, path, false);
      if (matching.size() > 1) {
        std::stringstream err;
        err << "Error: more than one"
          << " paths match pattern: " << path << ", taking first!" << std::endl
          << " Matches: " << std::endl;
        for (size_t i = 0; i < matching.size(); ++i) {
          err << i << ": " << matching[i].pathname << std::endl;
        }
        edm::LogError("SmartTriggerMultiMatchLumi") << err.str();
      }
      int thePrescale = (matching.size()) ? matching[0].prescale : 0;
      int theResult = (matching.size()) ? matching[0].ratecount : -1;
      groupPrescale.push_back(thePrescale);
      groupResult.push_back(theResult);
    }
    pathGroups.push_back(paths);
    prescales.push_back(groupPrescale);
    results.push_back(groupResult);
  }
  return makeDecision(pathGroups, prescales, results);
}
