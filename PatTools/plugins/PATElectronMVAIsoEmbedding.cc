/*
 * =====================================================================================
 *
 *       Filename:  PATElectronMVAIsoEmbedding.cc
 *
 *    Description:  Embed Iso MVA for electrons
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

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"

#include "EGamma/EGammaAnalysisTools/interface/EGammaMvaEleEstimator.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

class PATElectronMVAIsoEmbedding : public edm::EDProducer {
  public:
    PATElectronMVAIsoEmbedding(const edm::ParameterSet& pset);
    virtual ~PATElectronMVAIsoEmbedding(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag ebRecHits_;
    edm::InputTag eeRecHits_;
    edm::InputTag pfSrc_;
    edm::InputTag vertexSrc_;
    edm::InputTag rhoSrc_;

    ElectronEffectiveArea::ElectronEffectiveAreaTarget target_;
    EGammaMvaEleEstimator fElectronIsoMVA;
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

PATElectronMVAIsoEmbedding::PATElectronMVAIsoEmbedding(const edm::ParameterSet& pset) {
  using namespace std;

  src_ = pset.getParameter<edm::InputTag>("src");
  ebRecHits_ = pset.getParameter<edm::InputTag>("ebRecHits");
  eeRecHits_ = pset.getParameter<edm::InputTag>("eeRecHits");
  pfSrc_ = pset.getParameter<edm::InputTag>("pfSrc");
  rhoSrc_ = pset.getParameter<edm::InputTag>("rhoSrc");
  vertexSrc_ = pset.getParameter<edm::InputTag>("vertexSrc");

  vector<string> eleiso_weightfiles;
  eleiso_weightfiles.push_back("UserCode/sixie/EGamma/EGammaAnalysisTools/data/ElectronIso_BDTG_V0_BarrelPt5To10.weights.xml");
  eleiso_weightfiles.push_back("UserCode/sixie/EGamma/EGammaAnalysisTools/data/ElectronIso_BDTG_V0_EndcapPt5To10.weights.xml");
  eleiso_weightfiles.push_back("UserCode/sixie/EGamma/EGammaAnalysisTools/data/ElectronIso_BDTG_V0_EndcapPt10ToInf.weights.xml");
  eleiso_weightfiles.push_back("UserCode/sixie/EGamma/EGammaAnalysisTools/data/ElectronIso_BDTG_V0_EndcapPt10ToInf.weights.xml");
  updatePaths(eleiso_weightfiles);

  std::string target = pset.getParameter<std::string>("target");
  if (target == "2011Data") {
    target_ = ElectronEffectiveArea::kEleEAData2011;
  } else if (target == "2012Data") {
    target_ = ElectronEffectiveArea::kEleEAData2012;
  } else if (target == "Fall11MC") {
    target_ = ElectronEffectiveArea::kEleEAFall11MC;
  } else if (target == "Summer11MC") {
    target_ = ElectronEffectiveArea::kEleEASummer11MC;
  } else {
    throw cms::Exception("UnknownTarget")
      << "Bad eff. area option for electrons: " << target
      << " options are: 2011Data, Fall11MC, Summer11MC" << std::endl;
  }

  fElectronIsoMVA.initialize("EleIso_BDTG_IsoRings",
      EGammaMvaEleEstimator::kIsoRings,
      kTRUE,
      eleiso_weightfiles);

  produces<pat::ElectronCollection>();
}

void PATElectronMVAIsoEmbedding::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<edm::View<pat::Electron> > electrons;
  evt.getByLabel(src_, electrons);

  edm::ESHandle<TransientTrackBuilder> ttrackBuilder;
  es.get<TransientTrackRecord>().get(
      "TransientTrackBuilder", ttrackBuilder);

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

  EcalClusterLazyTools lazyTools(evt, es, ebRecHits_, eeRecHits_);

  std::auto_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  output->reserve(electrons->size());

  for (size_t i = 0; i < electrons->size(); ++i) {
    // Make our own copy
    pat::Electron ele(electrons->at(i));
    double isomva = fElectronIsoMVA.mvaValue(
        ele, pvCol->at(0),
        *ttrackBuilder,
        lazyTools,
        inPfCands, Rho,
        target_,
        IdentifiedElectrons, IdentifiedMuons);
    ele.addUserFloat("isomva", isomva);
    output->push_back(ele);
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronMVAIsoEmbedding);
