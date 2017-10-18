#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "CommonTools/Utils/interface/PtComparator.h"

#include "RecoTauTag/RecoTau/interface/RecoTauQualityCuts.h"

#include "FinalStateAnalysis/PatTools/interface/ParticlePFIsolationExtractor.h"

#include <string>

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "RecoTauTag/RecoTau/interface/RecoTauCommonUtilities.h"

#include "JetMETCorrections/Objects/interface/JetCorrector.h"

#include "DataFormats/Common/interface/RefToBase.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/Math/interface/deltaR.h"

#include <TMath.h>


class PATTauPreselectionEmbedder : public edm::EDFilter
{
 public:

  explicit PATTauPreselectionEmbedder(const edm::ParameterSet&);
  virtual ~PATTauPreselectionEmbedder();

  bool filter(edm::Event&, const edm::EventSetup&);

private:

  edm::InputTag src_;

  double minJetPt_;
  double maxJetEta_;

  reco::tau::RecoTauQualityCuts* trackQualityCuts_;
  double minLeadTrackPt_;
  double maxDzLeadTrack_;
  double maxLeadTrackPFElectronMVA_;
  bool applyECALcrackVeto_;

  double minDeltaRtoNearestMuon_;
  StringCutObjectSelector<pat::Muon>* muonSelection_;
  edm::InputTag srcMuon_;

  ek::ParticlePFIsolationExtractor<pat::Tau>* pfIsolationExtractor_;
  double maxPFIsoPt_;
  edm::InputTag srcPFIsoCandidates_;
  edm::InputTag srcBeamSpot_;
  edm::InputTag srcVertex_;
  edm::InputTag srcRhoFastJet_;

  // special flag to add userFloats to all pat::Taus
  // without applying any selection cuts
  bool produceAll_;

  // utility to sort (PF)tau-jet candidates in order of decreasing Pt
  // (taken from PhysicsTools/PatAlgos/plugins/PATTauProducer.h)
  GreaterByPt<pat::Tau> pfTauPtComparator_;

  int verbosity_;
};


typedef std::vector<pat::Tau> PATTauCollection;

PATTauPreselectionEmbedder::PATTauPreselectionEmbedder(const edm::ParameterSet& cfg)
  : trackQualityCuts_(0),
    muonSelection_(0),
    pfIsolationExtractor_(0),
    verbosity_(0)
{
  src_ = cfg.getParameter<edm::InputTag>("src");

  minJetPt_ = cfg.getParameter<double>("minJetPt");
  maxJetEta_ = cfg.getParameter<double>("maxJetEta");

  trackQualityCuts_ = new reco::tau::RecoTauQualityCuts(cfg.getParameter<edm::ParameterSet>("trackQualityCuts"));
  minLeadTrackPt_ = cfg.getParameter<double>("minLeadTrackPt");
  maxDzLeadTrack_ = cfg.getParameter<double>("maxDzLeadTrack");
  maxLeadTrackPFElectronMVA_ = cfg.getParameter<double>("maxLeadTrackPFElectronMVA");
  applyECALcrackVeto_ = cfg.getParameter<bool>("applyECALcrackVeto");

  minDeltaRtoNearestMuon_ = cfg.getParameter<double>("minDeltaRtoNearestMuon");
  if ( cfg.exists("muonSelection") ) {
    muonSelection_ = new StringCutObjectSelector<pat::Muon>(cfg.getParameter<std::string>("muonSelection"));
  }
  srcMuon_ = cfg.getParameter<edm::InputTag>("srcMuon");

  pfIsolationExtractor_ = new ek::ParticlePFIsolationExtractor<pat::Tau>(cfg.getParameter<edm::ParameterSet>("pfIsolation"));
  maxPFIsoPt_ = cfg.getParameter<double>("maxPFIsoPt");
  srcPFIsoCandidates_ = cfg.getParameter<edm::InputTag>("srcPFIsoCandidates");
  srcBeamSpot_   = cfg.getParameter<edm::InputTag>("srcBeamSpot");
  srcVertex_     = cfg.getParameter<edm::InputTag>("srcVertex");
  if ( cfg.exists("srcRhoFastJet") ) {
    srcRhoFastJet_ = cfg.getParameter<edm::InputTag>("srcRhoFastJet");
  }

  produces<PATTauCollection>();
}

PATTauPreselectionEmbedder::~PATTauPreselectionEmbedder()
{
  delete muonSelection_;
  delete trackQualityCuts_;
  delete pfIsolationExtractor_;
}

bool PATTauPreselectionEmbedder::filter(edm::Event& evt, const edm::EventSetup& es)
{
  if ( verbosity_ ) {
    std::cout << "<PATTauPreselectionEmbedder::filter>:" << std::endl;
    std::cout << " src = " << src_.label() << std::endl;
  }

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByLabel(srcVertex_, vertices);
  reco::VertexRef theVertex;
  if ( vertices->size() >= 1 ) theVertex = reco::VertexRef(vertices, 0);

  edm::Handle<reco::PFCandidateCollection> pfIsoCandidates;
  evt.getByLabel(srcPFIsoCandidates_, pfIsoCandidates);

  edm::Handle<reco::BeamSpot> beamSpot;
  evt.getByLabel(srcBeamSpot_, beamSpot);

  double rhoFastJet = -1.;
  if ( srcRhoFastJet_.label() != "" ) {
    edm::Handle<double> rhoFastJetHandle;
    evt.getByLabel(srcRhoFastJet_, rhoFastJetHandle);
    if ( rhoFastJetHandle.isValid() ) rhoFastJet = (*rhoFastJetHandle);
  }

  typedef std::vector<pat::Muon> PATMuonCollection;
  edm::Handle<PATMuonCollection> muons;
  evt.getByLabel(srcMuon_, muons);

  edm::Handle<PATTauCollection> pfTaus_input;
  evt.getByLabel(src_, pfTaus_input);

  std::unique_ptr<PATTauCollection> pfTaus_output(new PATTauCollection());

  for ( PATTauCollection::const_iterator pfTau_input = pfTaus_input->begin();
	pfTau_input != pfTaus_input->end(); ++pfTau_input ) {

    reco::PFJetRef pfJet = pfTau_input->pfJetRef();
    pat::Tau pfTau_output(*pfTau_input);

//--- select PFChargedHadrons passing track quality cuts
//    applied in PFTau reconstruction
    trackQualityCuts_->setPV(theVertex);
    std::vector<reco::PFCandidatePtr> pfChargedJetConstituents = reco::tau::pfChargedCands(*pfJet);
    std::vector<reco::PFCandidatePtr> selPFChargedHadrons;
    for ( std::vector<reco::PFCandidatePtr>::const_iterator pfChargedJetConstituent = pfChargedJetConstituents.begin();
	  pfChargedJetConstituent != pfChargedJetConstituents.end(); ++pfChargedJetConstituent ) {
      if ( trackQualityCuts_->filterCand(**pfChargedJetConstituent) ) selPFChargedHadrons.push_back(*pfChargedJetConstituent);
    }

//--- find highest Pt "leading" PFChargedHadron
    const reco::PFCandidate* leadPFChargedHadron = 0;
    reco::PFCandidatePtr leadPFChargedHadronPtr;
    for ( std::vector<reco::PFCandidatePtr>::const_iterator selPFChargedHadron = selPFChargedHadrons.begin();
	  selPFChargedHadron != selPFChargedHadrons.end(); ++selPFChargedHadron ) {
      if ( leadPFChargedHadron == 0 || (*selPFChargedHadron)->pt() > leadPFChargedHadron->pt() ) {
	leadPFChargedHadron = selPFChargedHadron->get();
        leadPFChargedHadronPtr = *selPFChargedHadron;
      }
    }
    pfTau_output.addUserCand("leadPFCH", leadPFChargedHadronPtr);

    if ( verbosity_ ) {
      std::cout << " leadPFChargedHadron: ";
      if ( leadPFChargedHadron ) std::cout << "Pt = " << leadPFChargedHadron->pt() << ","
					   << " eta = " << leadPFChargedHadron->eta() << ", phi = " << leadPFChargedHadron->phi();
      else std::cout << " None";
      std::cout << std::endl;
    }

    bool passesAll = true;

//--- require at least one PFChargedHadron passing quality cuts
//   (corresponding to "leading track finding" applied in PFTau reconstruction,
//    but without dR < 0.1 matching between leading track and jet-axis applied)
    pfTau_output.addUserInt("ps_ldTrk",
        (leadPFChargedHadron != NULL) ? 1 : 0);

    double leadTrkPt = (leadPFChargedHadron != NULL) ?
      leadPFChargedHadron->pt() : -1;
    int leadTrkQ = (leadPFChargedHadron != NULL) ?
      leadPFChargedHadron->charge() : 0;

    pfTau_output.addUserFloat("ps_ldTrkPt", leadTrkPt);
    pfTau_output.addUserInt("ps_ldTrkQ", leadTrkQ);

//--- require "leading" (highest Pt) PFChargedHadron to pass Pt cut
//   (corresponding to "leading track Pt cut" applied in PFTau reconstruction,
//    but without dR < 0.1 matching between leading track and jet-axis applied)
    if (!(leadTrkPt > minLeadTrackPt_) )
      passesAll = false;

//--- require that (PF)Tau-jet candidate passes loose isolation criteria
    reco::VertexCollection theVertexCollection;
    theVertexCollection.push_back(*theVertex);
    double loosePFIsoPt = -1.;
    if ( leadPFChargedHadron )
      loosePFIsoPt = (*pfIsolationExtractor_)(*pfTau_input, leadPFChargedHadron->momentum(),
					      *pfIsoCandidates, &theVertexCollection, beamSpot.product(), rhoFastJet);
    if ( verbosity_ ) std::cout << " loosePFIsoPt = " << loosePFIsoPt << std::endl;

    pfTau_output.addUserFloat("ps_lsPFIsoPt", loosePFIsoPt);

    if (loosePFIsoPt > maxPFIsoPt_ )
      passesAll = false;

//--- require "leading" PFChargedHadron to pass cut on (anti-)PFElectron MVA output
//   (corresponding to discriminatorAgainstElectrons(Loose) applied in PFTau reconstruction)
    double PFElectronMVA = -1.;
    if ( leadPFChargedHadron ) {
      if ( verbosity_ ) std::cout << " PFElectronMVA = " << leadPFChargedHadron->mva_e_pi() << std::endl;
      PFElectronMVA = leadPFChargedHadron->mva_e_pi();
    }
    bool isElectron = !(PFElectronMVA < maxLeadTrackPFElectronMVA_);
    pfTau_output.addUserFloat("ps_elMVA", PFElectronMVA);
    if (isElectron)
      passesAll = false;

//--- require "leading" PFChargedHadron not to overlap with reconstructed muon
//   (corresponding to discriminatorAgainstMuons applied in PFTau reconstruction;
//    whether the cut against muons is looser or tighter can be controlled
//    via the 'muonSelection' configuration parameter)
    const pat::Muon* nearestMuon = 0;
    double dRnearestMuon = 1.e+3;
    if ( leadPFChargedHadron ) {
      for ( PATMuonCollection::const_iterator muon = muons->begin();
	    muon != muons->end(); ++muon ) {
	if ( muonSelection_ == 0 || (*muonSelection_)(*muon) ) {
	  double dR = deltaR(leadPFChargedHadron->p4(), muon->p4());
	  if ( dR < dRnearestMuon ) {
	    nearestMuon = &(*muon);
	    dRnearestMuon = dR;
	  }
	}
      }
    }
    bool isMuon = (dRnearestMuon < minDeltaRtoNearestMuon_);
    pfTau_output.addUserFloat("ps_drMuon", dRnearestMuon);
    if ( verbosity_ ) {
      if ( nearestMuon && dRnearestMuon < minDeltaRtoNearestMuon_ ) {
	std::cout << " muon: Pt = " << nearestMuon->pt() << ","
		  << " eta = " << nearestMuon->eta() << ", phi = " << nearestMuon->phi()
		  << " --> dR = " << dRnearestMuon << std::endl;
	std::cout << "(isGlobalMuon = " << nearestMuon->isGlobalMuon() << ","
		  << " isTrackerMuon = " << nearestMuon->isTrackerMuon() << ","
		  << " isStandAloneMuon = " << nearestMuon->isStandAloneMuon() << ")" << std::endl;
      }
      std::cout << " isMuon = " << isMuon << std::endl;
    }
    if (isMuon)
      passesAll = false;

    // Fuck the JEC for this tool
    std::vector<std::string> correctionTypes;
    correctionTypes.push_back("nom");

    for (size_t iCorr = 0; iCorr < correctionTypes.size(); ++iCorr) {

      bool systematicPassResult = passesAll;

      const std::string& corrType = correctionTypes[iCorr];
      reco::Candidate::LorentzVector p4PFJetCorrected =
        pfTau_input->userCand("patJet")->p4();

      bool isECALcrack = (TMath::Abs(p4PFJetCorrected.eta()) > 1.442 &&
          TMath::Abs(p4PFJetCorrected.eta()) < 1.560);

      pfTau_output.addUserInt("ps_crk_" + corrType, isECALcrack);
      if (applyECALcrackVeto_ && isECALcrack)
        systematicPassResult = false;

      //--- check that (PF)tau-jet candidate passes Pt and eta selection
      bool passesKin = (p4PFJetCorrected.pt() > minJetPt_
            && TMath::Abs(p4PFJetCorrected.eta()) < maxJetEta_);
      pfTau_output.addUserInt("ps_kin_" + corrType, passesKin);
      if (!passesKin) {
        systematicPassResult = false;
      }
      // Final result for this systematic
      pfTau_output.addUserInt("ps_sel_" + corrType, systematicPassResult);
    }
//--- all cuts passed
//   --> create selected (PF)tau-jet candidate

//--- store number of tracks passing quality criteria
    pfTau_output.addUserFloat("numTracks", selPFChargedHadrons.size());

    pfTaus_output->push_back(pfTau_output);
  }

//--- sort (PF)tau-jet candidates in order of decreasing Pt
  std::sort(pfTaus_output->begin(), pfTaus_output->end(), pfTauPtComparator_);

  size_t numPFTaus_output = pfTaus_output->size();
  if ( verbosity_ ) std::cout << " numPFTaus_output = " << numPFTaus_output << std::endl;

  evt.put(std::move(pfTaus_output));

  return true;
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATTauPreselectionEmbedder);
