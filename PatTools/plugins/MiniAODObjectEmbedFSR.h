
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
    src_(iConfig.getParameter<edm::InputTag>("src")),
    srcAlt_(iConfig.getParameter<edm::InputTag>("srcAlt")),
    srcPho_(iConfig.exists("srcPho") ? iConfig.getParameter<edm::InputTag>("srcPho") : edm::InputTag("boodtedFsrPhotons")),
    srcVeto_(iConfig.exists("srcVeto") ? iConfig.getParameter<edm::InputTag>("srcVeto") : edm::InputTag("slimmedElectrons")),
    srcVtx_(iConfig.exists("srcVtx") ? iConfig.getParameter<edm::InputTag>("srcVtx") : edm::InputTag("selectedPrimaryVertex")),
    label_(iConfig.exists("userLabel") ? iConfig.getParameter<std::string>("userLabel") : "FSRCand"),
    isoLabels_(iConfig.getParameter<std::vector<std::string> >("isoLabels")),
    dRInner(iConfig.exists("dRInner") ? iConfig.getParameter<float>("dRInner") : 0.07),
    dROuter(iConfig.exists("dROuter") ? iConfig.getParameter<float>("dROuter") : 0.5),
    isoInner(iConfig.exists("isoInner") ? iConfig.getParameter<float>("isoInner") : 9999.9),
    isoOuter(iConfig.exists("isoOuter") ? iConfig.getParameter<float>("isoOuter") : 1.0),
    ptInner(iConfig.exists("ptInner") ? iConfig.getParameter<float>("ptInner") : 2.),
    ptOuter(iConfig.exists("ptOuter") ? iConfig.getParameter<float>("ptOuter") : 4.),
    maxEta(iConfig.exists("maxEta") ? iConfig.getParameter<float>("maxEta") : 2.4),
    vetoDR(iConfig.exists("vetoDR") ? iConfig.getParameter<float>("vetoDR") : 0.15),
    vetoDPhi(iConfig.exists("vetoDPhi") ? iConfig.getParameter<float>("vetoDPhi") : 2.),
    vetoDEta(iConfig.exists("vetoDEta") ? iConfig.getParameter<float>("vetoDEta") : 0.05),
    electronPt(iConfig.exists("electronPt") ? iConfig.getParameter<float>("electronPt") : 7.),
    electronMaxEta(iConfig.exists("electronMaxEta") ? iConfig.getParameter<float>("electronMaxEta") : 2.5),
    electronSIP(iConfig.exists("electronSIP") ? iConfig.getParameter<float>("electronSIP") : 4.),
    electronPVDXY(iConfig.exists("electronPVDXY") ? iConfig.getParameter<float>("electronPVDXY") : 0.5),
    electronPVDZ(iConfig.exists("electronPVDZ") ? iConfig.getParameter<float>("electronPVDZ") : 1.),
    electronIDPtThr(iConfig.exists("electronIDPtThr") ? iConfig.getParameter<float>("electronIDPtThr") : 10.),
    electronIDEtaThrLow(iConfig.exists("electronIDEtaThrLow") ? iConfig.getParameter<float>("electronIDEtaThrLow") : 0.8),
    electronIDEtaThrHigh(iConfig.exists("electronIDEtaThrHigh") ? iConfig.getParameter<float>("electronIDEtaThrHigh") : 1.479),
    electronIDCutLowPtLowEta(iConfig.exists("electronIDCutLowPtLowEta") ? iConfig.getParameter<float>("electronIDCutLowPtLowEta") : 0.47),
    electronIDCutLowPtMedEta(iConfig.exists("electronIDCutLowPtMedEta") ? iConfig.getParameter<float>("electronIDCutLowPtMedEta") : 0.004),
    electronIDCutLowPtHighEta(iConfig.exists("electronIDCutLowPtHighEta") ? iConfig.getParameter<float>("electronIDCutLowPtHighEta") : 0.295),
    electronIDCutHighPtLowEta(iConfig.exists("electronIDCutHighPtLowEta") ? iConfig.getParameter<float>("electronIDCutHighPtLowEta") : -0.34),
    electronIDCutHighPtMedEta(iConfig.exists("electronIDCutHighPtMedEta") ? iConfig.getParameter<float>("electronIDCutHighPtMedEta") : -0.65),
    electronIDCutHighPtHighEta(iConfig.exists("electronIDCutHighPtHighEta") ? iConfig.getParameter<float>("electronIDCutHighPtHighEta") : 0.6),
    electronIDLabel_(iConfig.exists("electronIDLabel") ? iConfig.getParameter<std::string>("electronIDLabel") : "MVANonTrigCSA14"),
    muonPt(iConfig.exists("muonPt") ? iConfig.getParameter<float>("muonPt") : 5.),
    muonMaxEta(iConfig.exists("muonMaxEta") ? iConfig.getParameter<float>("muonMaxEta") : 2.4),
    muonSIP(iConfig.exists("muonSIP") ? iConfig.getParameter<float>("muonSIP") : 4.),
    muonPVDXY(iConfig.exists("muonPVDXY") ? iConfig.getParameter<float>("muonPVDXY") : 0.5),
    muonPVDZ(iConfig.exists("muonPVDZ") ? iConfig.getParameter<float>("muonPVDZ") : 1.)
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
  float photonRelIso(const pat::PFParticle& pho) const;

  // Takes a reco::Candidate and tells you whether it passes ID cuts. e and mu only.
  // Stores this as a userFloat in the candidate (1 or 0) for reuse (won't persist for
  // any collection except src
  template<typename leptonType>
  bool leptonPassID(leptonType& lept);
  // helper for electrons. Electron cuts as passed in. 
  bool idHelper(const pat::Electron& e) const;
  // helper for muons. Muon cuts: isPFMuon && (isGlobalMuon || isTrackerMuon)
  bool idHelper(const pat::Muon& m) const;

  // Find out if photon passes cluster veto (returns true if it's good).
  // Pass in the lepton the photon is matched to in case it's an electron
  // that's also in the veto collection, so we don't auto-veto.
  bool passClusterVeto(const pat::PFParticle& pho, const reco::Candidate& pairedLep);

  // Embed the FSR photon in a lepton as a userCand, and the number of such cands as userInt("nFSRCands")
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
  const edm::InputTag src_; // FS leptons
  const edm::InputTag srcAlt_; // Dumb hack to deal with the fact that we only consider 
                                       // the closest lepton to a given photoon, so we have to
                                       // worry about both lepton collections at once, but an
                                       // EDProducer can only put one of the collections.
                                       // To put FSR info in electrons, src is for electrons
                                       // and srcAlt_ points to muons, so that we can ignore
                                       // a photon later (and deal with it in the muon producer)
                                       // if there's a closer muon. Or vice versa. 
  const edm::InputTag srcPho_; // FSR candidates
  const edm::InputTag srcVeto_; // electrons for cluster veto
  const edm::InputTag srcVtx_; // primary vertex (for veto PV and SIP cuts)
  const std::string label_; // userFloats names things like <label_>pt1
  const std::vector<std::string> isoLabels_; // keys to userfloats with isolation

  // parameters for FSR algorithm
  const float dRInner; // cuts different for photons very near and just kind of near lepton
  const float dROuter;
  const float isoInner; // iso cut (on photon) within dRInner
  const float isoOuter; // iso cut (on photon) between dRInner and dROuter
  const float ptInner; // pt cut within dRInner
  const float ptOuter; // pt cut between dRInner and dROuter
  const float maxEta; // of photon

  // parameters governing cluster veto
  const float vetoDR; // veto when electron is within dR OR...
  const float vetoDPhi; // ... when it's within dPhi AND dEta
  const float vetoDEta;
  const float electronPt; // This and following select good electrons
  const float electronMaxEta;
  const float electronSIP;
  const float electronPVDXY;
  const float electronPVDZ;
  const float electronIDPtThr; // ID different for high and low pt electrons
  const float electronIDEtaThrLow; // ID different for low, medium, and high eta electrons
  const float electronIDEtaThrHigh;
  const float electronIDCutLowPtLowEta;
  const float electronIDCutLowPtMedEta;
  const float electronIDCutLowPtHighEta;
  const float electronIDCutHighPtLowEta;
  const float electronIDCutHighPtMedEta;
  const float electronIDCutHighPtHighEta;
  const std::string electronIDLabel_; // ID variable to use
  const float muonPt; // This and following select good muons (along with cuts listed under bool muonPassID above)
  const float muonMaxEta;
  const float muonSIP;
  const float muonPVDXY;
  const float muonPVDZ;
};
