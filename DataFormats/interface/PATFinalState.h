#ifndef FinalStateAnalysis_DataFormats_PATFinalState_h
#define FinalStateAnalysis_DataFormats_PATFinalState_h

#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateProxy.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"

#include "FinalStateAnalysis/DataAlgos/interface/VBFVariables.h"
#include "FinalStateAnalysis/DataAlgos/interface/VBFSelections.h"

// Forward delcarations
namespace pat {
  class Electron;
  class Muon;
  class Tau;
  class MET;
  class Jet;
}

namespace reco {
  class Vertex;
}

typedef pat::PATObject<reco::LeafCandidate> PATLeafCandidate;

class PATFinalState : public pat::PATObject<reco::LeafCandidate> {
  public:
    typedef reco::Candidate::LorentzVector LorentzVector;

    PATFinalState();

    PATFinalState(
        int charge, const reco::Candidate::LorentzVector& p4,
        const edm::Ptr<PATFinalStateEvent>& evt);

    const edm::Ptr<pat::MET>& met() const;
    const edm::Ptr<reco::Vertex>& vertexObject() const;
    const edm::Ptr<PATFinalStateEvent>& evt() const { return event_; }

    virtual PATFinalState* clone() const = 0;

    /// Get the ith daughter.  Throws an exception if d.n.e.
    const reco::Candidate* daughter(size_t i) const;

    /// Get the ith daughter as a Ptr.  Throws an exception if d.n.e.
    const reco::CandidatePtr daughterPtr(size_t i) const;

    /// Get the number of daughters
    virtual size_t numberOfDaughters() const = 0;
    // Get a list of all the daughters
    std::vector<const reco::Candidate*> daughters() const;
    // Specify some of the systags for the daughters, in a comma separated list.
    std::vector<const reco::Candidate*> daughters(
        const std::string& tags) const;
    std::vector<reco::CandidatePtr> daughterPtrs(const std::string& tags) const;
    // Get all daughters, w/o systematics
    std::vector<reco::CandidatePtr> daughterPtrs() const;

    /// Check if the ith daughter has given user cand
    bool daughterHasUserCand(size_t i, const std::string& tag) const;

    /// Get the ith daughter's user cand (needs concrete type info)
    const reco::CandidatePtr daughterUserCand(size_t i,
        const std::string& tag) const;

    const LorentzVector& daughterUserCandP4(size_t i,
        const std::string& tag) const;

    /// Return the indices of the daughters, ordered by descending pt
    std::vector<size_t> indicesByPt(const std::string& tags="") const;
    /// Get the daughters, ordered by pt
    std::vector<const reco::Candidate*> daughtersByPt(
        const std::string& tags="") const;
    /// Get the ith daughter, ordered by pt
    const reco::Candidate* daughterByPt(size_t i,
        const std::string& tags="") const;
    // Check if the ith candidate has higher pt than the jth
    bool ptOrdered(size_t i, size_t j, const std::string& tags="") const;

    /// Tools for dealing with types
    template<typename T>
    edm::Ptr<T> daughterAs(size_t i) const {
      return edm::Ptr<T>(daughterPtr(i));
    }
    edm::Ptr<pat::Tau> daughterAsTau(size_t i) const;
    edm::Ptr<pat::Muon> daughterAsMuon(size_t i) const;
    edm::Ptr<pat::Electron> daughterAsElectron(size_t i) const;
    edm::Ptr<pat::Jet> daughterAsJet(size_t i) const;

    /// Check if the ith daughter is matched to a given filter.  Returns -1
    /// if filter doesn't exist.
    int matchToHLTFilter(size_t i, const std::string& filter,
        double maxDeltaR = 0.3) const;
    /// Check if the ith daughter is matched to a given path.  Returns -1
    /// if filter doesn't exists.
    int matchToHLTPath(size_t i, const std::string& path,
        double maxDeltaR = 0.3) const;

    // Evaluate a string function on this object (might be slow)
    double eval(const std::string& function) const;
    // Evaluate a string filter on this object (might be slow)
    bool filter(const std::string& cut) const;

    /// Get the total visible P4 (not including MET)
    LorentzVector visP4(const std::string& tags) const;
    /// Version using raw Pts
    LorentzVector visP4() const;

    /// Get the total P4 (including MET)
    LorentzVector totalP4(const std::string& tags,
        const std::string& metTag) const;
    /// Using raw four vectors
    LorentzVector totalP4() const;

    /// Get DeltaPhi between two objects
    double dPhi(int i, const std::string& tagI,
        int j, const std::string& tagJ) const;
    /// Using the raw four vectors
    double dPhi(int i, int j) const;
    /// Return the smallest dPhi between any two daughters
    double smallestDeltaPhi() const;

    /// Get the DeltaR between two daughters
    double dR(int i, const std::string& tagI,
        int j, const std::string& tagJ) const;
    /// Using the raw four vectors
    double dR(int i, int j) const;
    /// Return the smallest dR between any two daughters
    double smallestDeltaR() const;

    /// Get DeltaPhi to the MEt
    double deltaPhiToMEt(int i, const std::string& tag,
        const std::string& metTag) const;
    /// Using the raw four vector
    double deltaPhiToMEt(int i) const;

    /// Get the transverse mass between two objects
    double mt(int i, const std::string& tagI,
        int j, const std::string& tagJ) const;
    /// Using the raw four vector
    double mt(int i, int j) const;
    /// Get MT with MET
    double mtMET(int i, const std::string& tag,
        const std::string& metTag) const;
    double mtMET(int i, const std::string& metTag="") const;

    double ht(const std::string& sysTags) const;
    double ht() const;

    /// Compute the pZeta variable using the ith and jth legs as
    /// the "visible" objects.
    double pZeta(int i=0, int j=1) const;
    /// Visible pZeta.
    double pZetaVis(int i=0, int j=1) const;

    /// Check if the ith and jth daughters are like signed
    bool likeSigned(int i, int j) const;

    /// Check if the ith and jth daughters are like flavored
    bool likeFlavor(int i, int j) const;

    /// Check how far in mass the subcandidate made by the ith and jth objects
    /// is from the Z mass.  If they are same sign, it will return 1000.
    /// = |M_i_j - 91.2|
    double zCompatibility(int i, int j) const;

    /// Get the VBF selection variables.  The jet cuts are applied to the veto
    /// jets using dR of 0.3 away from the members.
    VBFVariables vbfVariables(const std::string& jetCuts) const;

    /// Check if two daughters are ordered in PT.
    /// This is equivalent to (daughter(i).pt > daughter(j).pt)
    /// Useful when ensuring a unique candidate is selected from many
    /// combinations.
    bool orderedInPt(int i, int j) const;

    /// Get a collection of embedded extras
    std::vector<reco::CandidatePtr> extras(
        const std::string& label, const std::string& filter="") const;

    /// Check if a daughter has overlaps subject to a filter
    std::vector<reco::CandidatePtr> filteredOverlaps(
        int i, const std::string& label, const std::string& filter="") const;

    /// Get veto objects at least dR away from any object, passing filter
    std::vector<const reco::Candidate*> vetoMuons(
        double dR=0.1, const std::string& filter="") const;

    std::vector<const reco::Candidate*> vetoElectrons(
        double dR=0.1, const std::string& filter="") const;

    std::vector<const reco::Candidate*> vetoTaus(
        double dR=0.1, const std::string& filter="") const;

    std::vector<const reco::Candidate*> vetoJets(
        double dR=0.1, const std::string& filter="") const;

    /// Get overlap objects at least dR within from the ith object, passing
    /// filter.
    std::vector<const reco::Candidate*> overlapMuons(
        int i, double dR=0.1, const std::string& filter="") const;

    std::vector<const reco::Candidate*> overlapElectrons(
        int i, double dR=0.1, const std::string& filter="") const;

    std::vector<const reco::Candidate*> overlapTaus(
        int i, double dR=0.1, const std::string& filter="") const;

    std::vector<const reco::Candidate*> overlapJets(
        int i, double dR=0.1, const std::string& filter="") const;

    /// Get the total mass, using the SuperCluster for one of the electrons.
    /// For example, if it is an EMT state:
    /// massUsingSuperCluster(0, 2) = tau + super cluster mass
    /// massUsingSuperCluster(0, 1, 2) = tau + mu + super cluster mass
//    double massUsingSuperCluster(int electronIndex, int j,
//        int x=-1, int y=-1, int z=-1) const;

    /// Build a subcandidate
    PATFinalStateProxy subcand(int i, int j,
        int x=-1, int y=-1, int z=-1) const;

    /// Build a subcand using a tag string
    PATFinalStateProxy subcand(const std::string& tags) const;

    /// Build a subcand using a tag string with included (filtered) extras
    PATFinalStateProxy subcand(
        const std::string& tags, const std::string& extras,
        const std::string& filter="") const;

    // Abstract interface to derived classes.  Can return null stuff.
    virtual const reco::Candidate* daughterUnsafe(size_t i) const = 0;
    virtual const reco::CandidatePtr daughterPtrUnsafe(size_t i) const = 0;
    virtual reco::CandidatePtr daughterUserCandUnsafe(size_t i,
        const std::string& tag) const = 0;

    /// Get the specified overlaps for the ith daughter
    virtual const reco::CandidatePtrVector& daughterOverlaps(
        size_t i, const std::string& label) const = 0;

  private:
    edm::Ptr<PATFinalStateEvent> event_;
};

#endif /* end of include guard: FinalStateAnalysis_DataFormats_PATFinalState_h */
