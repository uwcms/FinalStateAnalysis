#include "FinalStateAnalysis/DataAlgos/interface/MVAMet.h"
#include "pharris/MVAMet/interface/MVAMet.h"
#include "pharris/MVAMet/interface/MetUtilities.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

namespace {

// Global instance of MVA
static MVAMet* fMVAMet = NULL;

static const double minJetPt = 0.1;

// Only initialize the MVA when we ask for it so we don't slow down linking.
MVAMet* getMVA() {
  if (fMVAMet == NULL) {
    fMVAMet = new MVAMet(0.1);
    fMVAMet->Initialize(edm::ParameterSet(), // iConfig is never used in pharris/../MVAMet.cc
        TString((getenv("CMSSW_BASE")+std::string("/src/pharris/MVAMet/data/gbrmet_52.root"))),        //U
        TString((getenv("CMSSW_BASE")+std::string("/src/pharris/MVAMet/data/gbrmetphi_52.root"))),     //U Phi
        TString((getenv("CMSSW_BASE")+std::string("/src/pharris/MVAMet/data/gbrmetu1cov_52.root"))),   //U1 Cov
        TString((getenv("CMSSW_BASE")+std::string("/src/pharris/MVAMet/data/gbrmetu2cov_52.root"))) //U2 Cov
        );
  }
  return fMVAMet;
}

} // end anon namespace


// Getting info about the jets
namespace mvametjets {

  // Get the jet infos from a jet collection
  std::vector<MetUtilities::JetInfo> extractJets(const pat::JetCollection& jets,
      double rho) {
    std::vector<MetUtilities::JetInfo> output;
    size_t nJets = jets.size();
    output.reserve(nJets);
    for (size_t i = 0; i < nJets; ++i) {
      const pat::Jet& jet = jets[i];
      double uncorr_pt = jet.userCand("uncorrected")->pt();
      if (uncorr_pt < minJetPt)
        continue;
      if (!jet.userFloat("idLoose"))
        continue;
      double mva = jet.userFloat("philv1Discriminant");
      double lNeuFrac = (jet.neutralEmEnergy()/jet.energy() +
          jet.neutralHadronEnergy()/jet.energy());

      MetUtilities::JetInfo pJetObject;
      pJetObject.p4 = jet.p4();
      pJetObject.mva = mva;
      pJetObject.neutFrac = lNeuFrac;

      // For jets less than 10 GeV apply rho correction ONLY
      if (uncorr_pt < 10) {
        double newPt = std::max(uncorr_pt - jet.jetArea()*rho, 0.0);
        math::PtEtaPhiELorentzVector newP4(jet.p4());
        newP4.SetPt(newPt);
        pJetObject.p4 = newP4;
      }
      output.push_back(pJetObject);
    }
    return output;
  }

  // Caching version from FSA Event
  static edm::EventID lastEvent;
  static std::vector<MetUtilities::JetInfo> lastJets;

}

const std::vector<MetUtilities::JetInfo>& extractJets(
    const pat::JetCollection& jets, double rho, const edm::EventID& evt) {
  if (evt != mvametjets::lastEvent) {
    // update cache
    mvametjets::lastJets = mvametjets::extractJets(jets, rho);
    mvametjets::lastEvent = evt;
  }
  return mvametjets::lastJets;
}

// Information about PFCands in the event
namespace mvametpf {
  // From MVAMetProducer.cc example
  double pfCandDz(const reco::PFCandidate& iPFCand, const reco::Vertex& iPV) {
    double lDz = -999;
    if(iPFCand.trackRef().isNonnull())    lDz = fabs(iPFCand.   trackRef()->dz(iPV.position()));
    if(iPFCand.gsfTrackRef().isNonnull()) lDz = fabs(iPFCand.gsfTrackRef()->dz(iPV.position()));
    return lDz;
  }

  // The output format
  typedef std::vector<std::pair<math::XYZTLorentzVector,double> > PFInfo;

  PFInfo extractPF(const reco::PFCandidateCollection& pf, const reco::Vertex& pv) {
    PFInfo output;
    output.reserve(pf.size());
    for (size_t i = 0; i < pf.size(); ++i) {
      double dz = pfCandDz(pf[i], pv);
      output.push_back(std::make_pair(pf[i].p4(), dz));
    }
    return output;
  }

  // Caching version from FSA Event
  static edm::EventID lastEvent;
  static PFInfo lastPFInfo;
}

const mvametpf::PFInfo& extractPF(const reco::PFCandidateCollection& pf,
    const reco::Vertex& pv, const edm::EventID& evt) {
  if (evt != mvametpf::lastEvent) {
    mvametpf::lastPFInfo = mvametpf::extractPF(pf, pv);
    mvametpf::lastEvent = evt;
  }
  return mvametpf::lastPFInfo;
}

namespace mvametvertices {
  typedef std::vector<math::XYZVector> VertexInfo;

  VertexInfo extractVertices(const edm::PtrVector<reco::Vertex>& vertices) {
    VertexInfo output;
    output.reserve(vertices.size());
    for (size_t i = 0; i < vertices.size(); ++i) {
      const math::XYZPoint& vtxPoint = vertices[i]->position();
      // stupid incompatible vector types
      math::XYZVector vtx(vtxPoint.x(), vtxPoint.y(), vtxPoint.z());
      output.push_back(vtx);
    }
    return output;
  }

  // Caching version from FSA Event
  static edm::EventID lastEvent;
  static VertexInfo lastVertexInfo;
}

const mvametvertices::VertexInfo& extractVertices(
    const edm::PtrVector<reco::Vertex>& vertices,
    const edm::EventID& evt) {
  if (evt != mvametvertices::lastEvent) {
    mvametvertices::lastVertexInfo = mvametvertices::extractVertices(vertices);
    mvametvertices::lastEvent = evt;
  }
  return mvametvertices::lastVertexInfo;
}

// Minimal input-output of MVA MET algorithm
MVAMetResult computeMVAMet(
    const edm::EventID& evt,
    const std::vector<math::XYZTLorentzVector>& hardScatter,
    const reco::PFCandidateCollection& pflow,
    const reco::Vertex& pv,
    const pat::JetCollection& jets,
    const double& rho,
    const edm::PtrVector<reco::Vertex>& vertices) {
  // Initialize inputs - we have to copy these (sigh) since the MVA
  // cleans them
  std::vector<math::XYZTLorentzVector> hardScatterOwned = hardScatter;
  mvametvertices::VertexInfo vertexInfo = extractVertices(vertices, evt);
  mvametpf::PFInfo pfInfo = extractPF(pflow, pv, evt);
  std::vector<MetUtilities::JetInfo> jetInfo = extractJets(jets, rho, evt);
  // Get MVA
  MVAMet* mva = getMVA();
  return mva->GetMet(hardScatterOwned, jetInfo, pfInfo, vertexInfo, false);
}
