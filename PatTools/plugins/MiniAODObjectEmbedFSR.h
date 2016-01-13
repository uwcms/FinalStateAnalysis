
// MiniAODObjectEmbedFSR 
// Defines class MiniAODObjectEmbedFSR, which gives rise to MiniAODElectronFSREmbedder and MiniAODMuonFSREmbedder

// Original author: Nate Woods, U. Wisconsin

// Overloads the lepton with FSR info

// Because the FSR algorithm is ridiculous, this must be done in a ridiculous way. 
//     A userInt is embedded with the number of matched photons. For each photon, a userCand
//     is added with a key like "FSRCand1" (zero-indexed, so this is the key of the 2nd photon).
//     You can change "FSRCand" to something else by passing in a parameter "userLabel".
//     Almost all the selection is done here, including a bunch of hard cuts that totally
//     defeat the ntuple way of doing things (because we don't really have a choice,
//     unless somebody comes up with something really clever). However, we don't just
//     set the FSR-corrected pt, eta, phi, etc. for the lepton now, because we can't do
//     the improves-Z-mass cut here, and because there will ultimately be only one FSR
//     photon accepted per Z.

// Template has two types because we have to have a type for the leptons we're considering
//     and a type for the other leptons, because I can't think of a better way to do it.
//     See the comment by the declaration of const edm::InputTag srcAlt_ below.



// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/PatCandidates/interface/PFParticle.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include <DataFormats/GsfTrackReco/interface/GsfTrack.h>


// class declaration
//
template <typename T, typename U>
class MiniAODObjectEmbedFSR : public edm::EDProducer {

 public:
  explicit MiniAODObjectEmbedFSR(const edm::ParameterSet& iConfig) : 
    srcToken_(consumes<std::vector<T> >(iConfig.getParameter<edm::InputTag>("src"))),
    srcAltToken_(consumes<std::vector<U> >(iConfig.getParameter<edm::InputTag>("srcAlt"))),
    srcPhoToken_(consumes<std::vector<pat::PFParticle> >(iConfig.exists("srcPho") ? iConfig.getParameter<edm::InputTag>("srcPho") : edm::InputTag("boodtedFsrPhotons"))),
    srcVetoToken_(consumes<std::vector<pat::Electron> >(iConfig.exists("srcVeto") ? iConfig.getParameter<edm::InputTag>("srcVeto") : edm::InputTag("slimmedElectrons"))),
    srcVtxToken_(consumes<reco::VertexCollection>(iConfig.exists("srcVtx") ? iConfig.getParameter<edm::InputTag>("srcVtx") : edm::InputTag("selectedPrimaryVertex"))),
    label_(iConfig.exists("userLabel") ? iConfig.getParameter<std::string>("userLabel") : "FSRCand"),
    isoLabels_(iConfig.getParameter<std::vector<std::string> >("isoLabels")),
    dRInner(iConfig.exists("dRInner") ? iConfig.getParameter<double>("dRInner") : 0.07),
    dROuter(iConfig.exists("dROuter") ? iConfig.getParameter<double>("dROuter") : 0.5),
    isoInner(iConfig.exists("isoInner") ? iConfig.getParameter<double>("isoInner") : 9999.9),
    isoOuter(iConfig.exists("isoOuter") ? iConfig.getParameter<double>("isoOuter") : 1.0),
    ptInner(iConfig.exists("ptInner") ? iConfig.getParameter<double>("ptInner") : 2.),
    ptOuter(iConfig.exists("ptOuter") ? iConfig.getParameter<double>("ptOuter") : 4.),
    maxEta(iConfig.exists("maxEta") ? iConfig.getParameter<double>("maxEta") : 2.4),
    vetoDR(iConfig.exists("vetoDR") ? iConfig.getParameter<double>("vetoDR") : 0.15),
    vetoDPhi(iConfig.exists("vetoDPhi") ? iConfig.getParameter<double>("vetoDPhi") : 2.),
    vetoDEta(iConfig.exists("vetoDEta") ? iConfig.getParameter<double>("vetoDEta") : 0.05),
    idDecisionLabel_(iConfig.exists("idDecisionLabel") ? iConfig.getParameter<std::string>("idDecisionLabel") : "HZZ4lTightIDPass")
      {
	produces<std::vector<T> >();
      }

  ~MiniAODObjectEmbedFSR()
    {

    }

 private:

  // do producer stuff
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob() { }

  // For photon pho, find the closest (deltaR) lepton in src.
  // If none are within dROuter, or there is a better lepton in srcAlt,
  // returns src->end()
  typename std::vector<T>::iterator findBestLepton(const pat::PFParticle& pho);

  // Relative isolation of photon. Sum of all the userFloats whose keys are passed in as isoLabels
  double photonRelIso(const pat::PFParticle& pho) const;

  // Takes a reco::Candidate and tells you whether it passes ID cuts using decision embedded previously
  template<typename leptonType>
  bool leptonPassID(const leptonType& lept) const;
  template<typename leptonType>
  bool leptonPassIDTight(const leptonType& lept) const;

  // Find out if photon passes cluster veto (returns true if it's good).
  // Pass in the lepton the photon is matched to in case it's an electron
  // that's also in the veto collection, so we don't auto-veto.
  bool passClusterVeto(const pat::PFParticle& pho, const reco::Candidate& pairedLep);

  // Embed the FSR photon in a lepton as a userCand, and the number of such cands as userInt("n"+label_)
  // The usercand has a key of the form label_+str(nPho), e.g. FSRCand0 for the pt of the first photon, 
  //     if a new label is not specified
  // nFSRCands is automatically created and incremented, and its new value is returned
  // Leaves the lepton in its collection
  int embedFSRCand(typename std::vector<T>::iterator& lept, const std::vector<pat::PFParticle>::const_iterator& pho);
  

  std::auto_ptr<std::vector<T> > src;
  std::auto_ptr<std::vector<U> > srcAlt;
  std::auto_ptr<pat::ElectronCollection> srcVeto;
  edm::Handle<reco::VertexCollection> srcVtx;
  edm::Handle<std::vector<pat::PFParticle> > srcPho;

  // collection input tags/labels
  const edm::EDGetTokenT<std::vector<T> > srcToken_; // FS leptons
  const edm::EDGetTokenT<std::vector<U> > srcAltToken_; // Dumb hack to deal with the fact that we only consider 
                                       // the closest lepton to a given photoon, so we have to
                                       // worry about both lepton collections at once, but an
                                       // EDProducer can only put one of the collections.
                                       // To put FSR info in electrons, src is for electrons
                                       // and srcAlt_ points to muons, so that we can ignore
                                       // a photon later (and deal with it in the muon producer)
                                       // if there's a closer muon. Or vice versa. 
  const edm::EDGetTokenT<std::vector<pat::PFParticle> > srcPhoToken_; // FSR candidates
  const edm::EDGetTokenT<std::vector<pat::Electron> > srcVetoToken_; // electrons for cluster veto
  const edm::EDGetTokenT<reco::VertexCollection> srcVtxToken_; // primary vertex (for veto PV and SIP cuts)
  const std::string label_; // userFloats names things like <label_>pt1
  const std::vector<std::string> isoLabels_; // keys to userfloats with isolation

  // parameters for FSR algorithm
  const double dRInner; // cuts different for photons very near and just kind of near lepton
  const double dROuter;
  const double isoInner; // iso cut (on photon) within dRInner
  const double isoOuter; // iso cut (on photon) between dRInner and dROuter
  const double ptInner; // pt cut within dRInner
  const double ptOuter; // pt cut between dRInner and dROuter
  const double maxEta; // of photon

  // parameters governing cluster veto
  const double vetoDR; // veto when electron is within dR OR...
  const double vetoDPhi; // ... when it's within dPhi AND dEta
  const double vetoDEta;
  
  // name of the userFloat holding ID decisions
  std::string idDecisionLabel_;

  int nPassPre;
  int nHaveBest;
  int nPassIso;
  int nPassVeto;
};
