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
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include <DataFormats/PatCandidates/interface/PackedTriggerPrescales.h>
#include <FWCore/Common/interface/TriggerNames.h>
#include "DataFormats/PatCandidates/interface/TriggerPath.h"

#include "DataFormats/Provenance/interface/EventID.h"
#include "FWCore/Framework/interface/Event.h"


#define DEBUG_ 0

// Cache calls to
// smartTrigger(const std::string& trgs, const pat::TriggerEvent& result)
// because it is very expensive!
namespace {
  // Cache variables
  static edm::EventID lastTrigEvent; // last processed event
  static std::map<std::string, SmartTriggerResult> cache;
}

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
  boost::split_regex(tokens, grp, boost::regex("\\|"));
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
      if(DEBUG_) std::cout << __PRETTY_FUNCTION__ << " "<< __LINE__ << " prescales " << i << " "<< j << " "<< prescales[i][j] << std::endl;
    }
    // Make sure all items have the same prescale.  If not, skip this group.
    if (minInGrp != maxInGrp)
      continue;
    // // If the prescale is zero, the trigger is off. Skip it.
    // if (minInGrp == 0)
    //   continue;
    // Otherwise use this one (as it comes first) if it has a LOWER prescale
    // Not LT not LTE
    if (minInGrp < lowest) {
      lowest = minInGrp;
      bestGroup = i;
    }
  }
  if(DEBUG_) std::cout << __PRETTY_FUNCTION__ << " "<< __LINE__ <<  " bestgroup " << bestGroup << std::endl;
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

std::vector<int> matchingTriggerPaths(
    const edm::TriggerNames& names,
    const edm::TriggerResults trgResults,
    const std::string& pattern, bool ez) {
  std::vector<int> output;
  if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
  try {
    boost::regex matcher(ez ? edm::glob2reg(pattern) : pattern);
    for (unsigned int i=0, n=trgResults.size(); i<n; ++i) {
      if(DEBUG_) {
	if (boost::regex_match(names.triggerName(i), matcher)) std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " "<< i << " name "<< names.triggerName(i) << ", pattern "<< pattern << ", matcher " << matcher << " " << boost::regex_match(names.triggerName(i), matcher) << std::endl;
      }
      if (boost::regex_match(names.triggerName(i), matcher)) {
	if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << i<< std::endl;
        output.push_back(i);
      }
    }
  } catch (std::exception& e) {
    edm::LogError("PathRegexParse") << "Caught exception when parsing"
      << " trigger path regex expression: [" << pattern << "]" << std::endl;
    throw;
  }
  if(DEBUG_)  std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " output size " << output.size() << std::endl; 
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

std::vector<const pat::TriggerFilter*>
matchingTriggerFilters(const std::vector<pat::TriggerObjectStandAlone>& trgObject, const edm::TriggerNames& names,
		       const std::string& pattern, bool ez) {
  std::vector<const pat::TriggerFilter*> output;
  boost::regex matcher(ez ? edm::glob2reg(pattern) : pattern);
  //std::vector< std::string > trgnames;
  const std::vector<std::string> labels;
  for (pat::TriggerObjectStandAlone obj : trgObject) {
    obj.unpackPathNames(names);
    for (unsigned int il = 0 ; il<names.size(); il++){
      if (boost::regex_match(names.triggerName(il), matcher)) {
	pat::TriggerFilter* filter = new pat::TriggerFilter(names.triggerName(il));
        output.push_back(filter);
      }	
    }
  }
  return output;
}
SmartTriggerResult makeDecision(
    const VVString& paths, const VVInt& prescales, const VVInt& results) {
  if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;

  unsigned int prescale = 0;
  bool passed = false;
  unsigned int group = chooseGroup(prescales);
  if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " group " << group << " prescale size " << prescales.size() <<  std::endl;
  vstring chosenPaths;
  if (group < prescales.size()) {
    // We know by construction the prescales are the same in the whole group
    prescale = prescales[group][0];
    if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " prescale " << prescale <<  std::endl;
    for (size_t i = 0; i < results[group].size(); ++i) {
      if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " path " << paths[group][i] << ", result " << i << " " << results[group][i] <<  std::endl;
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
  for (size_t i = 0; i < output.paths.size(); ++i) {
    if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " "<< __LINE__ << " " << output.paths[i] <<  ", passed? "  << bool(output.passed) << std::endl;
    
  }
  return output;

}

// Non-cached version
SmartTriggerResult smartTrigger(const std::string& trgs,
    const pat::TriggerEvent& result, bool ez) {
  // Tokenize the trigger groups
  //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
  vstring groups = getGroups(trgs);
  VVInt prescales;
  VVInt results;
  VVString pathGroups;
  for (size_t i = 0; i < groups.size(); ++i) {
    //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
    // Get the paths in this group
    VInt groupPrescale;
    VInt groupResult;
    vstring paths = getPaths(groups[i]);
    // The real names of the matched paths.
    vstring realpaths;
    for (size_t p = 0; p < paths.size(); ++p) {
      //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
      const std::string& path = paths[p];
      // Get all the triggers that match this path pattern.  There should be
      // only one.  The point of the smart trigger is that each path type is a
      // separate group.
      std::vector<const pat::TriggerPath*> matching =
        matchingTriggerPaths(result, path, ez);
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
      if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
      
      const pat::TriggerPath* trgPath = matching.size() ? matching[0] : NULL;
      int thePrescale = (trgPath != NULL) ? trgPath->prescale() : 0;
      int theResult = (trgPath != NULL) ? trgPath->wasAccept() : -1;
      realpaths.push_back((trgPath != NULL) ? trgPath->name() : "error");
      groupPrescale.push_back(thePrescale);
      groupResult.push_back(theResult);
      if (trgPath != NULL) std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " trgPath "<< trgPath->name() << " theResult "<< theResult << std::endl;

    }
    pathGroups.push_back(realpaths);
    prescales.push_back(groupPrescale);
    results.push_back(groupResult);
    if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;

  }
  if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
    
  SmartTriggerResult output = makeDecision(pathGroups, prescales, results);
  if(DEBUG_) std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;


  return output;
}

SmartTriggerResult smartTrigger(const std::string& trgs,
    const edm::TriggerNames& names, const pat::PackedTriggerPrescales& trgPrescales, 
    const edm::TriggerResults& trgResults, bool ez) {
  // Tokenize the trigger groups
  if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
  vstring groups = getGroups(trgs);
  VVInt prescales;
  VVInt results;
  VVString pathGroups;
  // for (size_t itr =0 ; itr<trgResults.size() ; itr++ ){
  //   if ( trgResults.at(itr).accept() ) std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " path   " << names.triggerNames()[itr] << ", results" << trgResults.at(itr).accept() <<  std::endl ;
  // }
  for (size_t i = 0; i < groups.size(); ++i) {
    //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
    // Get the paths in this group
    VInt groupPrescale;
    VInt groupResult;
    vstring paths = getPaths(groups[i]);
    // The real names of the matched paths.
    vstring realpaths;
    for (size_t p = 0; p < paths.size(); ++p) {
      const std::string& path = paths[p];
      //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " path "<< path << std::endl;
      // Get all the triggers that match this path pattern.  There should be
      // only one.  The point of the smart trigger is that each path type is a
      // separate group.
      std::vector<int> matching = matchingTriggerPaths(names, trgResults, path, ez);
      if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl ;

      if (matching.size() > 1) {
        std::stringstream err;
        err << "Error: more than one"
          << " paths match pattern: " << path << ", taking first!" << std::endl
          << " Matches: " << std::endl;
        for (size_t i = 0; i < matching.size(); ++i) {
          err << i << ": " << names.triggerName(matching[i]) << std::endl;
        }
        edm::LogError("SmartTriggerMultiMatchHLT") << err.str();
      }
      //if (matching.size()!=0) std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " matching "<< matching[0] << " trgResults "<<trgResults.size()<< std::endl;
      // for (unsigned int itr = 0 ; itr<trgResults.size(); itr++){
      // 	std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " "<< itr <<" " << names.triggerName(itr) <<  " passed " << trgResults.at(itr).accept()<< std::endl;
      //      }
      //if (matching.size()!=0) std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " path " << path << " accepted " << trgResults.at(matching[0]).accept() << std::endl ;

      realpaths.push_back(matching.size() ? names.triggerName(matching[0]) : "error");
      groupPrescale.push_back(matching.size() ? trgPrescales.getPrescaleForIndex(matching[0]) : 0);
      groupResult.push_back(matching.size() ? trgResults.at(matching[0]).accept() : -1);
      if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
      if(DEBUG_){
	if (matching.size()) std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << matching[0] << " trgPath "<<  names.triggerName(matching[0])<< " theResult "<< trgResults.at(matching[0]).accept() << std::endl;
      }
    }
    if(DEBUG_)std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
    pathGroups.push_back(realpaths);
    prescales.push_back(groupPrescale);
    results.push_back(groupResult);
  }
  SmartTriggerResult output = makeDecision(pathGroups, prescales, results);
  if(DEBUG_){
    for (size_t i=0; i<  output.paths.size(); i++){
      std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " path " <<output.paths[i]<< ", passed? " << output.passed<<   std::endl;
    }
  }
  return output;
}

// Cached version
const SmartTriggerResult& smartTrigger(const std::string& trgs,
    const pat::TriggerEvent& result, const edm::EventID& evt, bool ez) {
  // Check if we have cached the result.
  //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
  if (evt != lastTrigEvent) {
    // new event, clear the cache
    cache.clear();
  } else {
    // If we already have computed these triggers for this event, return it.
    // std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
    std::map<std::string, SmartTriggerResult>::iterator findit = cache.find(trgs);
    if (findit != cache.end())
      return findit->second;
  }

  // If we are here, we just computed the new value bu need to update the cache
  lastTrigEvent = evt;
  cache[trgs] = smartTrigger(trgs, result, ez);
  return cache[trgs];
}

const SmartTriggerResult& smartTrigger(const std::string& trgs,
    const edm::TriggerNames& names, const pat::PackedTriggerPrescales& trgPrescales, 
    const edm::TriggerResults& trgResults, const edm::EventID& evt, bool ez) {
  // Check if we have cached the result.
  //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << std::endl;
  if (evt != lastTrigEvent) {
    // new event, clear the cache
    cache.clear();
  } else {
    // If we already have computed these triggers for this event, return it.
    //std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << trgs<< std::endl;
    std::map<std::string, SmartTriggerResult>::iterator findit = cache.find(trgs);
    if (findit != cache.end())
      return findit->second;
  }

  // If we are here, we just computed the new value bu need to update the cache
  lastTrigEvent = evt;
  cache[trgs] = smartTrigger(trgs, names, trgPrescales, trgResults, ez);
  return cache[trgs];
}
