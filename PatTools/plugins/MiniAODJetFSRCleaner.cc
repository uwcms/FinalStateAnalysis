//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODJetFSRCleaner.cc                                                //
//                                                                          //
//   Removes jets close to FSR photons.                                     //
//                                                                          //
//   Author: Nate Woods, U. Wisconsin                                       //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////


// system includes
#include <memory>
#include <vector>
#include <iostream>

// CMS includes
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

typedef reco::Candidate Cand;
typedef edm::Ptr<Cand> CandPtr;
typedef reco::CandidateView CandView;
typedef pat::Electron Elec;
typedef edm::Ptr<pat::Electron> ElecPtr;
typedef edm::View<pat::Electron> ElecView;
typedef pat::Muon Muon;
typedef edm::Ptr<pat::Muon> MuonPtr;
typedef edm::View<pat::Muon> MuonView;
typedef pat::Jet Jet;
typedef edm::Ptr<pat::Jet> JetPtr;
typedef edm::View<pat::Jet> JetView;

class MiniAODJetFSRCleaner : public edm::stream::EDProducer<>
{
public:
  explicit MiniAODJetFSRCleaner(const edm::ParameterSet&);
  ~MiniAODJetFSRCleaner() {}

private:
  //// Methods
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  // Get all FSR photons
  std::vector<CandPtr> getFSR(const edm::Handle<ElecView>& elecs,
                              const edm::Handle<MuonView>& muons) const;
  // Helper for getFSR()
  template<typename Lep>
  void addFSR(const edm::Handle<edm::View<Lep> >& leps,
              std::vector<CandPtr>& addTo) const;
  bool selectFSRLep(const ElecPtr& e) const;
  bool selectFSRLep(const MuonPtr& m) const;
  
  //// Data
  edm::EDGetTokenT<JetView> collectionTokenJ;
  edm::EDGetTokenT<ElecView> collectionTokenE;
  edm::EDGetTokenT<MuonView> collectionTokenM;

  // Consider fsr from leptons passing these selections
  StringCutObjectSelector<Elec> fsrElecSelection;
  StringCutObjectSelector<Muon> fsrMuonSelection;

  // Label of FSR userCand
  const std::string fsrLabel;

  // Size of cleaning cone
  const double coneDR;
};


MiniAODJetFSRCleaner::MiniAODJetFSRCleaner(const edm::ParameterSet& iConfig):
  collectionTokenJ(consumes<JetView>(iConfig.exists("src") ? 
                                      iConfig.getParameter<edm::InputTag>("src") :
                                      edm::InputTag("slimmedJets"))),
  collectionTokenE(consumes<ElecView>(iConfig.exists("srcE") ? 
                                      iConfig.getParameter<edm::InputTag>("srcE") :
                                      edm::InputTag("slimmedElectrons"))),
  collectionTokenM(consumes<MuonView>(iConfig.exists("srcMu") ? 
                                      iConfig.getParameter<edm::InputTag>("srcMu") :
                                      edm::InputTag("slimmedMuons"))),
  fsrElecSelection(iConfig.exists("fsrElecSelection") ?
                   iConfig.getParameter<std::string>("fsrElecSelection") :
                   ""),
  fsrMuonSelection(iConfig.exists("fsrMuonSelection") ?
                   iConfig.getParameter<std::string>("fsrMuonSelection") :
                   ""),
  fsrLabel(iConfig.exists("fsrLabel") ?
           iConfig.getParameter<std::string>("fsrLabel") :
           std::string("dretFSRCand")),
  coneDR(iConfig.exists("deltaR") ?
           iConfig.getParameter<double>("deltaR") :
           0.4)
{
  produces<std::vector<Jet> >();
}


void MiniAODJetFSRCleaner::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<JetView> jetsIn;
  edm::Handle<ElecView> elecsIn;
  edm::Handle<MuonView> muonsIn;

  iEvent.getByToken(collectionTokenJ, jetsIn);
  iEvent.getByToken(collectionTokenE, elecsIn);
  iEvent.getByToken(collectionTokenM, muonsIn);

  std::vector<CandPtr> fsr = getFSR(elecsIn, muonsIn);

  std::unique_ptr<std::vector<Jet> > out = 
    std::unique_ptr<std::vector<Jet> >(new std::vector<Jet>);

  for(size_t iJ = 0; iJ < jetsIn->size(); ++iJ)
    {
      JetPtr jet = jetsIn->ptrAt(iJ);

      bool rejected = false;
      for(size_t iFSR = 0; iFSR < fsr.size(); ++iFSR)
        {
          rejected = reco::deltaR(fsr.at(iFSR)->p4(), jet->p4()) < coneDR;
          if(rejected) break;
        }
      if(!rejected)
        out->push_back(*jet);
    }

  iEvent.put(std::move(out));
}
    

std::vector<CandPtr> 
MiniAODJetFSRCleaner::getFSR(const edm::Handle<ElecView>& elecs,
                             const edm::Handle<MuonView>& muons) const
{
  std::vector<CandPtr> out;

  addFSR(elecs, out);
  addFSR(muons, out);

  return out;
}


template<typename Lep>
void
MiniAODJetFSRCleaner::addFSR(const edm::Handle<edm::View<Lep> >& leps,
                             std::vector<CandPtr>& fsr) const
{
  for(size_t iLep = 0; iLep < leps->size(); ++iLep)
    {
      edm::Ptr<Lep> lep = leps->ptrAt(iLep);
      if(!selectFSRLep(lep)) continue;
      if(lep->hasUserCand(fsrLabel))
        fsr.push_back(lep->userCand(fsrLabel));
    }
}


bool
MiniAODJetFSRCleaner::selectFSRLep(const ElecPtr& e) const
{
  return fsrElecSelection(*e);
}


bool
MiniAODJetFSRCleaner::selectFSRLep(const MuonPtr& m) const
{
  return fsrMuonSelection(*m);
}


//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODJetFSRCleaner);

