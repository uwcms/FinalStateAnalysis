/*
 * =====================================================================================
 *
 *       Filename:  PATMuonMVAEmbedder.cc
 *
 *    Description:  Embeds all these nonsense MVAs into the muons
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "Muon/MuonAnalysisTools/interface/MuonMVAEstimator.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class PATMuonMVAEmbedder : public edm::EDProducer {
  public:
    PATMuonMVAEmbedder(const edm::ParameterSet& pset);
    virtual ~PATMuonMVAEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag pfSrc_;
    edm::InputTag vertexSrc_;
    edm::InputTag rhoSrc_;
    MuonMVAEstimator fMuonIsoMVA;
    MuonMVAEstimator fMuonIDMVA;
    MuonMVAEstimator fMuonIsoRingsRadMVA;
};

namespace {
std::string getFullPath(const std::string& fileInPath) {
  return edm::FileInPath(fileInPath).fullPath();
}

// Convert a list of paths to the full path
void updatePaths(std::vector<std::string>& paths) {
  for (size_t i = 0; i < paths.size(); ++i) {
    paths[i] = getFullPath(paths[i]);
  }
}
}

PATMuonMVAEmbedder::PATMuonMVAEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  pfSrc_ = pset.getParameter<edm::InputTag>("pfSrc");
  rhoSrc_ = pset.getParameter<edm::InputTag>("rhoSrc");
  vertexSrc_ = pset.getParameter<edm::InputTag>("vertexSrc");

  produces<pat::MuonCollection>();

  // Rings isolation
  std::vector<std::string> muoniso_weightfiles;
  muoniso_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-BarrelPt5To10_V0_BDTG.weights.xml");
  muoniso_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-EndcapPt5To10_V0_BDTG.weights.xml");
  muoniso_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-BarrelPt10ToInf_V0_BDTG.weights.xml");
  muoniso_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-EndcapPt10ToInf_V0_BDTG.weights.xml");
  muoniso_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-Tracker_V0_BDTG.weights.xml");
  muoniso_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-Global_V0_BDTG.weights.xml");
  updatePaths(muoniso_weightfiles);
  fMuonIsoMVA.initialize("MuonIso_BDTG_IsoRings",
      MuonMVAEstimator::kIsoRings,
      kTRUE,
      muoniso_weightfiles);
  //fMuonIsoMVA->SetPrintMVADebug(kTRUE);

  // ID
  std::vector<std::string> muonid_weightfiles;
  muonid_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIDMVA_sixie-BarrelPt5To10_V0_BDTG.weights.xml");
  muonid_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIDMVA_sixie-EndcapPt5To10_V0_BDTG.weights.xml");
  muonid_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIDMVA_sixie-BarrelPt10ToInf_V0_BDTG.weights.xml");
  muonid_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIDMVA_sixie-EndcapPt10ToInf_V0_BDTG.weights.xml");
  muonid_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIDMVA_sixie-Tracker_V0_BDTG.weights.xml");
  muonid_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIDMVA_sixie-Global_V0_BDTG.weights.xml");
  updatePaths(muonid_weightfiles);
  fMuonIDMVA.initialize("MuonID_BDTG",
                   MuonMVAEstimator::kID,
                   kTRUE,
                   muonid_weightfiles);

  // Radial + Rings ISO
  std::vector<std::string> muonisoRingsRad_weightfiles;

  muonisoRingsRad_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-BarrelPt5To10_V1_BDTG.weights.xml");
  muonisoRingsRad_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-EndcapPt5To10_V1_BDTG.weights.xml");
  muonisoRingsRad_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-BarrelPt10ToInf_V1_BDTG.weights.xml");
  muonisoRingsRad_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-EndcapPt10ToInf_V1_BDTG.weights.xml");
  muonisoRingsRad_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-Tracker_V1_BDTG.weights.xml");
  muonisoRingsRad_weightfiles.push_back("Muon/MuonAnalysisTools/data/MuonIsoMVA_sixie-Global_V1_BDTG.weights.xml");
  updatePaths(muonisoRingsRad_weightfiles);
  fMuonIsoRingsRadMVA.initialize("MuonIso_BDTG_IsoRingsRad",
                   MuonMVAEstimator::kIsoRingsRadial,
                   kTRUE,
                   muonisoRingsRad_weightfiles);
  //fMuonIsoRingsRadMVA->SetPrintMVADebug(kTRUE);
}

void PATMuonMVAEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::MuonCollection> output(new pat::MuonCollection);

  edm::Handle<edm::View<pat::Muon> > muons;
  evt.getByLabel(src_, muons);
  output->reserve(muons->size());

  edm::Handle<reco::VertexCollection> hVertex;
  evt.getByLabel(vertexSrc_, hVertex);
  const reco::VertexCollection *pvCol = hVertex.product();

  edm::Handle<double> hRho;
  evt.getByLabel(rhoSrc_, hRho);
  double Rho = *hRho;

  edm::Handle<reco::PFCandidateCollection> hPfCandProduct;
  evt.getByLabel(pfSrc_, hPfCandProduct);
  const reco::PFCandidateCollection &inPfCands = *(hPfCandProduct.product());

  // Just leave these blank.
  reco::GsfElectronCollection IdentifiedElectrons;
  reco::MuonCollection IdentifiedMuons;

  for (size_t i = 0; i < muons->size(); ++i) {
    pat::Muon muon = muons->at(i); // make a local copy

    // So I can copy paste from the twiki
    pat::Muon* iM = &muon;

    double isomva = fMuonIsoMVA.mvaValue( *iM, pvCol->at(0),
        inPfCands, Rho,
        MuonEffectiveArea::kMuEAFall11MC,
        IdentifiedElectrons, IdentifiedMuons);

    double idmva = fMuonIDMVA.mvaValue( *iM, pvCol->at(0),
        inPfCands, Rho,
        MuonEffectiveArea::kMuEAFall11MC,
        IdentifiedElectrons, IdentifiedMuons);

    double isoringsradmva = fMuonIsoRingsRadMVA.mvaValue( *iM, pvCol->at(0),
        inPfCands, Rho,
        MuonEffectiveArea::kMuEAFall11MC,
        IdentifiedElectrons, IdentifiedMuons);

    muon.addUserFloat("isomva", isomva);
    muon.addUserFloat("idmva", idmva);
    muon.addUserFloat("isoringsradmva", isoringsradmva);
    output->push_back(muon);
  }

  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuonMVAEmbedder);
