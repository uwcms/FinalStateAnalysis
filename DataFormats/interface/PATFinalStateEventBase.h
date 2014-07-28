#ifndef PATFINALSTATEEVENTBASE
#define PATFINALSTATEEVENTBASE

/*
 *   The base class for FinalStateEvent and FinalStateEventMini classes
 *
 *   Author: Devin N. Taylor, UW Madison
 *
 */

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventBaseFwd.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Common/interface/PtrVector.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenFilterInfo.h"
#include "DataFormats/Provenance/interface/EventID.h"

#include "TMatrixD.h"
#include <map>
#include <string>

class PATFinalStateEventBase {
  public:
    /// Get PV
    virtual const edm::Ptr<reco::Vertex>& pv() const = 0;
    /// Get all reconstructed vertices
    virtual const edm::PtrVector<reco::Vertex>& recoVertices() const = 0;
    /// Get PU information
    virtual const std::vector<PileupSummaryInfo>& puInfo() const = 0;
    /// Get the Les Houches event information
    virtual const lhef::HEPEUP& lesHouches() const = 0;
    /// Get the GenEventInfo product
    virtual const GenEventInfoProduct& genEventInfo() const = 0;
    /// Get weight for embedded samples
    virtual const GenFilterInfo& generatorFilter() const = 0;
    /// Get FastJet rho
    virtual double rho() const = 0;
    /// Get trigger information
    //virtual const pat::TriggerEvent& trig() const = 0;

    /*  These methods will be deprecated! */
    /// Get PFMET
    virtual const edm::Ptr<pat::MET>& met() const = 0;
    /// Get MET covariance
    virtual const TMatrixD& metCovariance() const = 0;
    /// Get MET significance
    virtual double metSignificance() const = 0;

    // Get a given type of MET
    virtual const edm::Ptr<pat::MET> met(const std::string& type) const = 0;
    // Get 4-vector of the MET
    virtual const reco::Candidate::LorentzVector met4vector(const std::string& type, const std::string& tag="", const int applyPhiCorr=0) const = 0;

    /// Get the event ID
    virtual const edm::EventID& evtId() const = 0;

    /// The following functions use the "SmartTrigger" functionality.
    /// They can be passed a comma separated list of paths:
    ///   hltResult("HLT_Mu15_v.*,HLT_Mu30_v.*")
    /// And the first path with the lowest prescale will be chosen.

    /// Get the result of the chosen path.  Returns -1 if it doesn't exist
    virtual int hltResult(const std::string& pattern) const = 0;

    /// Get the prescale of a given path.  Returns -1 if it doesn't exist
    virtual int hltPrescale(const std::string& pattern) const = 0;

    /// Get the group of a given path.  Returns -1 if it doesn't exist
    virtual int hltGroup(const std::string& pattern) const = 0;

    /// Determine if a candidate is matched to an HLT filter
    virtual int matchedToFilter(const reco::Candidate& cand, const std::string& filter,
        double maxDeltaR = 0.3) const = 0;

    /// Determine if a candidate is matched to an HLT path
    virtual int matchedToPath(const reco::Candidate& cand, const std::string& pattern,
        double maxDeltaR = 0.3) const = 0;

    //Finds a decay in MC
    virtual const bool findDecay(const int pdgIdMother, const int pdgIdDaughter) const = 0;

    /// Get the PU scenario used to generate this events (if MC)
    virtual const std::string& puTag() const = 0;

    /// The following allow use of the PileupWeighting feature in DataAlgos
    /// For the available tags, see DataAlgos/data/pileup_distributions.py
    /// This version uses the internally stored PU tag
    virtual double puWeight(const std::string& dataTag) const = 0;

    /// The following allow use of the PileupWeighting feature in DataAlgos,
    /// manually specifying which MC tag to use.
    virtual double puWeight(const std::string& dataTag, const std::string& mcTag) const = 0;

    /// Use 3D reweighting, for backwards compatibility.
    virtual double puWeight3D(const std::string& dataTag) const = 0;
    virtual double puWeight3D(const std::string& dataTag, const std::string& mcTag) const = 0;

    /// Get a named event weight
    virtual float weight(const std::string& name) const = 0;
    virtual void addWeight(const std::string& name, float weight) = 0;

    /// Get a named event flag
    virtual int flag(const std::string& flag) const = 0;
    virtual void addFlag(const std::string& name, int flag) = 0;

    /// Is real data
    virtual bool isRealData() const = 0;

    /// Access to object collections in the event
    virtual const pat::ElectronCollection& electrons() const = 0;
    virtual const pat::MuonCollection& muons() const = 0;
    virtual const pat::JetCollection& jets() const = 0;
    virtual const pat::TauCollection& taus() const = 0;
    virtual const pat::PhotonCollection& photons() const = 0;

    /// Access to particle flow collections
    //virtual const reco::PFCandidateCollection& pflow() const = 0;

    //Access to GenParticleRefProd
    //virtual const reco::GenParticleRefProd genParticleRefProd() const = 0;

    /// Get the version of the FinalState data formats API
    /// This allows you to detect which version of the software was used
    /// So that the methods can be update.
    /// The FSA_DATA_FORMAT_VERSION def at the top of the .cc file should be
    /// incremented after each change to the data format.
    virtual char version() const = 0;
    virtual float jetVariables(const reco::CandidatePtr jet, const std::string& myvar) const = 0;
};

#endif /* end of include guard: PATFINALSTATEEVENTBASE */
