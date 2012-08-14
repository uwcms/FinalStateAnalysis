#ifndef PATFINALSTATEEVENT_MB433KP6
#define PATFINALSTATEEVENT_MB433KP6

/*
 *   A simple container for holding quantities that are defined across the whole
 *   event.
 *
 *   Author: Evan K. Friis, UW Madison
 *
 */

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Common/interface/PtrVector.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/Provenance/interface/EventID.h"

#include "TMatrixD.h"
#include <map>
#include <string>

class PATFinalStateEvent {
  public:

    PATFinalStateEvent();

    // minimal constructor used only for unit tests
    PATFinalStateEvent(
        const edm::Ptr<reco::Vertex>& pv,
        const edm::Ptr<pat::MET>& met
    );

    // This constructor should only be used in the initial production!
    // It automatically sets the version() to the current one.
    PATFinalStateEvent(double rho,
        const edm::Ptr<reco::Vertex>& pv,
        const edm::PtrVector<reco::Vertex>& recoVertices,
        const edm::Ptr<pat::MET>& met,
        const TMatrixD& metCovariance,
        const pat::TriggerEvent& triggerEvent,
        const std::vector<PileupSummaryInfo>& puInfo,
        const lhef::HEPEUP& hepeup, // Les Houches info
        const reco::GenParticleRefProd& genParticles,
        const edm::EventID& evtId,
        const GenEventInfoProduct& genEventInfoProd,
        bool isRealData,
        const std::string& puScenario,
        const edm::RefProd<pat::ElectronCollection>& electronRefProd,
        const edm::RefProd<pat::MuonCollection>& muonRefProd,
        const edm::RefProd<pat::TauCollection>& tauRefProd,
        const edm::RefProd<pat::JetCollection>& jetRefProd,
        const reco::PFCandidateRefProd& pfRefProd,
        const reco::TrackRefProd& tracks,
        const reco::GsfTrackRefProd& gsfTracks
    );

    /// Get PV
    const edm::Ptr<reco::Vertex>& pv() const;
    /// Get all reconstructed vertices
    const edm::PtrVector<reco::Vertex>& recoVertices() const;
    /// Get PU information
    const std::vector<PileupSummaryInfo>& puInfo() const;
    /// Get the Les Houches event information
    const lhef::HEPEUP& lesHouches() const;
    /// Get the GenEventInfo product
    const GenEventInfoProduct& genEventInfo() const;
    /// Get FastJet rho
    double rho() const;
    /// Get trigger information
    const pat::TriggerEvent& trig() const;
    /// Get MET
    const edm::Ptr<pat::MET>& met() const;
    /// Get MET covariance
    const TMatrixD& metCovariance() const;
    /// Get MET significance
    double metSignificance() const;
    /// Get the event ID
    const edm::EventID& evtId() const;

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

    /// Get the PU scenario used to generate this events (if MC)
    const std::string& puTag() const;

    /// The following allow use of the PileupWeighting feature in DataAlgos
    /// For the available tags, see DataAlgos/data/pileup_distributions.py
    /// This version uses the internally stored PU tag
    double puWeight(const std::string& dataTag) const;

    /// The following allow use of the PileupWeighting feature in DataAlgos,
    /// manually specifying which MC tag to use.
    double puWeight(const std::string& dataTag, const std::string& mcTag) const;

    /// Use 3D reweighting, for backwards compatibility.
    double puWeight3D(const std::string& dataTag) const;
    double puWeight3D(const std::string& dataTag, const std::string& mcTag) const;

    /// Get a named event weight
    float weight(const std::string& name) const;
    void addWeight(const std::string& name, float weight);

    /// Get a named event flag
    int flag(const std::string& flag) const;
    void addFlag(const std::string& name, int flag);

    /// Is real data
    bool isRealData() const { return isRealData_; }

    /// Access to object collections in the event
    const pat::ElectronCollection& electrons() const;
    /// Workaround - in the 2012-05-28 tuples, the electrons are set wrong,
    /// so we need to update them on the fly.  FIXME eventually remove this.
    void setElectrons(const edm::RefProd<pat::ElectronCollection>& elecs) {
      electronRefProd_ = elecs;
    }
    const pat::MuonCollection& muons() const;
    const pat::JetCollection& jets() const;
    const pat::TauCollection& taus() const;

    /// Access to particle flow collections
    const reco::PFCandidateCollection& pflow() const;

    /// Get the version of the FinalState data formats API
    /// This allows you to detect which version of the software was used
    /// So that the methods can be update.
    /// The FSA_DATA_FORMAT_VERSION def at the top of the .cc file should be
    /// incremented after each change to the data format.
    char version() const { return fsaDataFormatVersion_; }

  private:
    std::map<std::string, float> weights_;
    std::map<std::string, int> flags_;
    double rho_;
    pat::TriggerEvent triggerEvent_;
    edm::Ptr<reco::Vertex> pv_;
    edm::PtrVector<reco::Vertex> recoVertices_;
    edm::Ptr<pat::MET> met_;
    TMatrixD metCovariance_;
    std::vector<PileupSummaryInfo> puInfo_;
    lhef::HEPEUP lhe_;
    reco::GenParticleRefProd genParticles_;
    edm::EventID evtID_;
    GenEventInfoProduct genEventInfoProduct_;
    bool isRealData_;
    std::string puScenario_;
    char fsaDataFormatVersion_;
    // Pointers to object collections in the event
    edm::RefProd<pat::ElectronCollection> electronRefProd_;
    edm::RefProd<pat::MuonCollection> muonRefProd_;
    edm::RefProd<pat::TauCollection> tauRefProd_;
    edm::RefProd<pat::JetCollection> jetRefProd_;
    reco::PFCandidateRefProd pfRefProd_;
    reco::TrackRefProd tracks_;
    reco::GsfTrackRefProd gsfTracks_;
};

#endif /* end of include guard: PATFINALSTATEEVENT_MB433KP6 */
