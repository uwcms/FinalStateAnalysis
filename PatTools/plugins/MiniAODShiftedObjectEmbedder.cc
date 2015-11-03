/** \class MiniAODShiftedObjectEmbedder
 *
 * Embeds shifted objects into the parent object
 *
 * \author Devin Taylor, UW-Madison
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FinalStateAnalysis/PatTools/interface/PATLeptonTrackVectorExtractor.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include <vector>

template<typename T>
class MiniAODShiftedObjectEmbedder : public edm::EDProducer
{
  public:
    MiniAODShiftedObjectEmbedder(const edm::ParameterSet& pset);
    virtual ~MiniAODShiftedObjectEmbedder(){}
  private:
    // Methods
    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

    // members
    edm::EDGetTokenT<edm::View<T> > srcToken_;
    edm::EDGetTokenT<edm::View<T> > shiftSrcToken_;
    std::string label_;
};

template<typename T>
MiniAODShiftedObjectEmbedder<T>::MiniAODShiftedObjectEmbedder(const edm::ParameterSet& iConfig):
  srcToken_(consumes<edm::View<T> >(iConfig.getParameter<edm::InputTag>("src"))),
  shiftSrcToken_(consumes<edm::View<T> >(iConfig.getParameter<edm::InputTag>("shiftSrc"))),
  label_(iConfig.getParameter<std::string>("label"))
{
  produces<std::vector<T> >();
}

template<typename T>
void MiniAODShiftedObjectEmbedder<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::auto_ptr<std::vector<T> > out = std::auto_ptr<std::vector<T> >(new std::vector<T>);

  edm::Handle<edm::View<T> > src;
  iEvent.getByToken(srcToken_, src);
  edm::Handle<edm::View<T> > shiftSrc;
  iEvent.getByToken(shiftSrcToken_, shiftSrc);

  for (size_t i = 0; i < src->size(); ++i) {
    const T& srcObj = src->at(i);
    const edm::Ptr<T> shiftSrcObj = shiftSrc->ptrAt(i);
    T newObj = srcObj;
    newObj.addUserCand(label_,shiftSrcObj);
    out->push_back(newObj);
  }

  iEvent.put(out);
}

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

typedef MiniAODShiftedObjectEmbedder<pat::Electron> MiniAODShiftedElectronEmbedder;
typedef MiniAODShiftedObjectEmbedder<pat::Muon> MiniAODShiftedMuonEmbedder;
typedef MiniAODShiftedObjectEmbedder<pat::Tau> MiniAODShiftedTauEmbedder;
typedef MiniAODShiftedObjectEmbedder<pat::Jet> MiniAODShiftedJetEmbedder;
typedef MiniAODShiftedObjectEmbedder<pat::Photon> MiniAODShiftedPhotonEmbedder;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODShiftedElectronEmbedder);
DEFINE_FWK_MODULE(MiniAODShiftedMuonEmbedder);
DEFINE_FWK_MODULE(MiniAODShiftedTauEmbedder);
DEFINE_FWK_MODULE(MiniAODShiftedJetEmbedder);
DEFINE_FWK_MODULE(MiniAODShiftedPhotonEmbedder);
