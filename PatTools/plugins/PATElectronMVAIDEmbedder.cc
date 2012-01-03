/*
 * Embeds MIT MVA Electron ID information into pat::Electrons
 *
 * Author: Evan K. Friis, UW Madison
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FinalStateAnalysis/PatTools/interface/ElectronIDMVA.h"

class PATElectronMVAIDEmbedder : public edm::EDProducer {
  public:
    PATElectronMVAIDEmbedder(const edm::ParameterSet& pset);
    virtual ~PATElectronMVAIDEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    edm::InputTag ebRecHits_;
    edm::InputTag eeRecHits_;
    edm::InputTag srcVertices_;
    std::string userLabel_;
    ElectronIDMVA mva_;
    double maxDB_;
    double maxDZ_;
};

PATElectronMVAIDEmbedder::PATElectronMVAIDEmbedder(const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  ebRecHits_ = pset.getParameter<edm::InputTag>("ebRecHits");
  eeRecHits_ = pset.getParameter<edm::InputTag>("eeRecHits");
  maxDB_ = pset.getParameter<double>("maxDB");
  maxDZ_ = pset.getParameter<double>("maxDZ");
  srcVertices_ = pset.getParameter<edm::InputTag>("srcVertices");

  std::string method_ = pset.getParameter<std::string>("methodName");
  edm::FileInPath Subdet0Pt10To20Weights = pset.getParameter<edm::FileInPath>("Subdet0LowPtWeights");
  edm::FileInPath Subdet1Pt10To20Weights = pset.getParameter<edm::FileInPath>("Subdet1LowPtWeights");
  edm::FileInPath Subdet2Pt10To20Weights = pset.getParameter<edm::FileInPath>("Subdet2LowPtWeights");
  edm::FileInPath Subdet0HighPtWeights = pset.getParameter<edm::FileInPath>("Subdet0HighPtWeights");
  edm::FileInPath Subdet1HighPtWeights = pset.getParameter<edm::FileInPath>("Subdet1HighPtWeights");
  edm::FileInPath Subdet2HighPtWeights = pset.getParameter<edm::FileInPath>("Subdet2HighPtWeights");
  ElectronIDMVA::MVAType mvaType = static_cast<ElectronIDMVA::MVAType>(
      pset.getParameter<unsigned int>("mvaType"));

  mva_.Initialize(
      method_,
      Subdet0Pt10To20Weights.fullPath(),
      Subdet1Pt10To20Weights.fullPath(),
      Subdet2Pt10To20Weights.fullPath(),
      Subdet0HighPtWeights.fullPath(),
      Subdet1HighPtWeights.fullPath(),
      Subdet2HighPtWeights.fullPath(),
      mvaType);

  produces<pat::ElectronCollection>();
}

void PATElectronMVAIDEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<edm::View<pat::Electron> > electrons;
  evt.getByLabel(src_, electrons);

  edm::Handle<reco::BeamSpot> bsHandle;
  evt.getByLabel("offlineBeamSpot", bsHandle);
  const reco::BeamSpot &thebs = *bsHandle.product();

  edm::Handle<reco::VertexCollection> vtxHandle;
  evt.getByLabel(srcVertices_, vtxHandle);

  edm::Handle<reco::ConversionCollection> hConversions;
  evt.getByLabel("allConversions", hConversions);

  std::auto_ptr<pat::ElectronCollection> output(new pat::ElectronCollection);
  output->reserve(electrons->size());

  for (size_t i = 0; i < electrons->size(); ++i) {
    // Make our own copy
    pat::Electron electron(electrons->at(i));

    bool hasConversion = ConversionTools::hasMatchedConversion(
        electron, hConversions, thebs.position());
    electron.addUserFloat("hasConversion", hasConversion);

    const reco::HitPattern& p_inner =
      electron.gsfTrack()->trackerExpectedHitsInner();
    electron.addUserInt("missingHits", p_inner.numberOfHits());


    double dz = 999;
    if (vtxHandle->size())
      dz = electron.gsfTrack()->dz(vtxHandle->at(0).position());
    electron.addUserFloat("idDZ", dz);

    // Compute the mva value
    double mvaV = mva_.MVAValue(
        &electron, evt, es, ebRecHits_, eeRecHits_);
    // Add it as a user float
    electron.addUserFloat("MVA", mvaV);

    float pt = electron.pt();

    // Now apply the actual MIT ID working point
    bool passID = electron.superCluster().isNonnull();
    passID = passID && (!hasConversion);
    passID = passID && (p_inner.numberOfHits() == 0);
    passID = passID && (dz < maxDZ_);
    passID = passID && (electron.dB() < maxDB_);
    if (passID) {
      float eta = fabs(electron.superCluster()->eta());
      if(pt<20 && eta<1 &&mvaV<0.133) passID=false;
      if(pt<20 && eta>1.0 && eta<1.5 &&mvaV<0.465) passID=false;
      if(pt<20 && eta>1.5 && eta<2.5 &&mvaV<0.518) passID=false;

      if(pt>20 && eta<1 &&mvaV<0.942) passID=false;
      if(pt>20 && eta>1.0 && eta<1.5 &&mvaV<0.947) passID=false;
      if(pt>20 && eta>1.5 && eta<2.5 &&mvaV<0.878) passID=false;
    }
    electron.addUserFloat("MITID", passID);

    output->push_back(electron);
  }
  evt.put(output);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATElectronMVAIDEmbedder);
