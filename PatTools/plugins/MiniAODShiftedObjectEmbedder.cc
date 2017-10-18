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
  std::unique_ptr<std::vector<T> > out = std::unique_ptr<std::vector<T> >(new std::vector<T>);

  edm::Handle<edm::View<T> > src;
  iEvent.getByToken(srcToken_, src);
  edm::Handle<edm::View<T> > shiftSrc;
  iEvent.getByToken(shiftSrcToken_, shiftSrc);

  //if(src->size()!=shiftSrc->size())
  //  std::cout << "Warning: " << label_ << " size missmatch. src: " << src->size() << " shiftSrc: " << shiftSrc->size() << std::endl;

  for (size_t i = 0; i < src->size(); ++i) {
    const T& srcObj = src->at(i);
    //std::cout << label_ << " " << i << " src: pt " << srcObj.pt() << " eta " << srcObj.eta() << " phi " << srcObj.phi() << std::endl;
    T newObj = srcObj;
    if (i<shiftSrc->size()) {
      const edm::Ptr<T> shiftSrcObj = shiftSrc->ptrAt(i);
      //std::cout << label_ << " " << i << " shiftSrc: pt " << shiftSrcObj->pt() << " eta " << shiftSrcObj->eta() << " phi " << shiftSrcObj->phi() << std::endl;
      newObj.addUserCand(label_,shiftSrcObj);
      newObj.addUserFloat(label_+"Pt",shiftSrcObj->pt());
      newObj.addUserFloat(label_+"Eta",shiftSrcObj->eta());
      newObj.addUserFloat(label_+"Phi",shiftSrcObj->phi());
    }
    else {
      //std::cout << label_ << " " << i << " lost. Object ref set to empty candidate." << std::endl;
      const edm::Ptr<T> cand = edm::Ptr<T>();
      newObj.addUserCand(label_,cand);
      newObj.addUserFloat(label_+"Pt",-9.);
      newObj.addUserFloat(label_+"Eta",-9.);
      newObj.addUserFloat(label_+"Phi",-9.);
    }
    out->push_back(newObj);
  }

  //if(shiftSrc->size()>src->size()) {
  //  for (size_t i=src->size(); i<shiftSrc->size(); ++i) {
  //    const edm::Ptr<T> shiftSrcObj = shiftSrc->ptrAt(i);
  //    std::cout << label_ << " " << i << " shiftSrc: pt " << shiftSrcObj->pt() << " eta " << shiftSrcObj->eta() << " phi " << shiftSrcObj->phi() << std::endl;
  //  }
  //}

  iEvent.put(std::move(out));
}

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/MET.h"

typedef MiniAODShiftedObjectEmbedder<pat::Electron> MiniAODShiftedElectronEmbedder;
typedef MiniAODShiftedObjectEmbedder<pat::Muon> MiniAODShiftedMuonEmbedder;
typedef MiniAODShiftedObjectEmbedder<pat::Tau> MiniAODShiftedTauEmbedder;
typedef MiniAODShiftedObjectEmbedder<pat::Jet> MiniAODShiftedJetEmbedder;
typedef MiniAODShiftedObjectEmbedder<pat::Photon> MiniAODShiftedPhotonEmbedder;
typedef MiniAODShiftedObjectEmbedder<pat::MET> MiniAODShiftedMETEmbedder;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODShiftedElectronEmbedder);
DEFINE_FWK_MODULE(MiniAODShiftedMuonEmbedder);
DEFINE_FWK_MODULE(MiniAODShiftedTauEmbedder);
DEFINE_FWK_MODULE(MiniAODShiftedJetEmbedder);
DEFINE_FWK_MODULE(MiniAODShiftedPhotonEmbedder);
DEFINE_FWK_MODULE(MiniAODShiftedMETEmbedder);
