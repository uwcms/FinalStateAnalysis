#ifndef PATFINALSTATEEVENT_MB433KP6
#define PATFINALSTATEEVENT_MB433KP6

/*
 *   A simple container for holder quantities that are defined across the whole
 *   event.
 *
 *   Author: Evan K. Friis, UW Madison
 *
 *   In the future:
 *      > Move MET and PV to here exclusively?
 */

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Common/interface/PtrVector.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/Provenance/interface/EventID.h"

#include <map>
#include <string>

class PATFinalStateEvent {
  public:
    PATFinalStateEvent();

    PATFinalStateEvent(double rho,
        const edm::Ptr<reco::Vertex>& pv,
        const edm::PtrVector<reco::Vertex>& recoVertices,
        const edm::Ptr<pat::MET>& met,
        const pat::TriggerEvent& triggerEvent,
        const std::vector<PileupSummaryInfo>& puInfo,
        const edm::EventID& evtId);


    /// Get PV
    const edm::Ptr<reco::Vertex>& pv() const;
    /// Get all reconstructed vertices
    const edm::PtrVector<reco::Vertex>& recoVertices() const;
    /// Get PU information
    const std::vector<PileupSummaryInfo>& puInfo() const;
    /// Get FastJet rho
    double rho() const;
    /// Get trigger information
    const pat::TriggerEvent& trig() const;
    /// Get MET
    const edm::Ptr<pat::MET>& met() const;
    /// Get the event ID
    const edm::EventID& id() const;

    /// Get the list of trigger paths matching a given pattern.  If [ez] is
    // true, use the friendly '*' syntax.  Otherwise use boost::regexp.
    std::vector<const pat::TriggerPath*> matchingTriggerPaths(
        const std::string& pattern, bool ez=false) const;

    /// Get the list of trigger filters matching a given pattern.  If [ez] is
    // true, use the friendly '*' syntax.  Otherwise use boost::regexp.
    std::vector<const pat::TriggerFilter*> matchingTriggerFilters(
        const std::string& pattern, bool ez=false) const;

    /// The following functions use the "SmartTrigger" functionality.
    /// They can be passed a comma separated list of paths:
    ///   hltResult("HLT_Mu15_v.*,HLT_Mu30_v.*")
    /// And the first path with the lowest prescale will be chosen.

    /// Get the result of the chosen path.  Returns -1 if it doesn't exist
    int hltResult(const std::string& pattern) const;

    /// Get the prescale of a given path.  Returns -1 if it doesn't exist
    int hltPrescale(const std::string& pattern) const;

    /// Get the group of a given path.  Returns -1 if it doesn't exist
    int hltGroup(const std::string& pattern) const;

    /// Determine if a candidate is matched to an HLT filter
    int matchedToFilter(const reco::Candidate& cand, const std::string& filter,
        double maxDeltaR = 0.3) const;

    /// Determine if a candidate is matched to an HLT path
    int matchedToPath(const reco::Candidate& cand, const std::string& pattern,
        double maxDeltaR = 0.3) const;

    /// Get a named event weight
    float weight(const std::string& name) const;
    void addWeight(const std::string& name, float weight);

    /// Get a named event flag
    int flag(const std::string& flag) const;
    void addFlag(const std::string& name, int flag);

  private:
    std::map<std::string, float> weights_;
    std::map<std::string, int> flags_;
    double rho_;
    pat::TriggerEvent triggerEvent_;
    edm::Ptr<reco::Vertex> pv_;
    edm::PtrVector<reco::Vertex> recoVertices_;
    edm::Ptr<pat::MET> met_;
    std::vector<PileupSummaryInfo> puInfo_;
    edm::EventID evtID_;
};

#endif /* end of include guard: PATFINALSTATEEVENT_MB433KP6 */
