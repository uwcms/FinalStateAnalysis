//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODLeptonHZZIsoDecider.cc                                          //
//                                                                          //
//   Embeds lepton relative isolation and isolation decisions as userfloats //
//       (1 for true, 0 for false) for use in other modules, using          //
//       HZZ4l2015 definitions.                                             //
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
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/MuonReco/interface/MuonPFIsolation.h"


typedef reco::Candidate Cand;
typedef edm::Ptr<Cand> CandPtr;
typedef reco::CandidateView CandView;
typedef pat::Electron Elec;
typedef edm::Ptr<pat::Electron> ElecPtr;
typedef edm::View<pat::Electron> ElecView;
typedef pat::Muon Muon;
typedef edm::Ptr<pat::Muon> MuonPtr;
typedef edm::View<pat::Muon> MuonView;


class MiniAODLeptonHZZIsoDecider : public edm::stream::EDProducer<>
{
public:
  explicit MiniAODLeptonHZZIsoDecider(const edm::ParameterSet&);
  ~MiniAODLeptonHZZIsoDecider() {}

private:
  //// Methods
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  // Make collection to output. Heap allocation done here.
  template<typename Lep>
  std::auto_ptr<std::vector<Lep> >
  makeCollection(const edm::Handle<edm::View<Lep> >& lepsIn,
                 const std::vector<CandPtr>& fsrs) const;

  // Actual isolation calculation
  template<typename Lep>
  float relPFIsoFSR(const edm::Ptr<Lep>& lep,
                    const std::vector<CandPtr>& fsrs) const;
  float isoPUCorrection(const ElecPtr& e) const;
  float isoPUCorrection(const MuonPtr& m) const;
  template<typename Lep>
  float isoFSRCorrection(const edm::Ptr<Lep>& lep,
                         const std::vector<CandPtr>& fsr) const;
  bool fsrInIsoCone(const ElecPtr& e,
                    const CandPtr& fsr) const;
  bool fsrInIsoCone(const MuonPtr& m,
                    const CandPtr& fsr) const;
  
  // Isolation variables for e and mu (why isn't this standard???)
  const reco::GsfElectron::PflowIsolationVariables& 
  isolationVariables(const ElecPtr&) const;
  const reco::MuonPFIsolation& 
  isolationVariables(const MuonPtr&) const;

  // Get all FSR photons
  std::vector<CandPtr> getFSR(const edm::Handle<ElecView>& elecs,
                              const edm::Handle<MuonView>& muons) const;
  // Helper for getFSR()
  template<typename Lep>
  void addFSR(const edm::Handle<edm::View<Lep> >& leps,
              std::vector<CandPtr>& addTo) const;
  bool selectFSRLep(const ElecPtr& e) const;
  bool selectFSRLep(const MuonPtr& m) const;

  // Helper to get cut value for e or mu
  const float getIsoCut(const ElecPtr& e) const {return isoCutE;}
  const float getIsoCut(const MuonPtr& m) const {return isoCutM;}

  //// Data
  edm::EDGetTokenT<ElecView> collectionTokenE;
  edm::EDGetTokenT<MuonView> collectionTokenM;

  // UserFloat labels
  const std::string isoValueLabel;
  const std::string isoDecisionLabel;

  // Collections we'll output at the end
  std::auto_ptr<std::vector<Elec> > outE; 
  std::auto_ptr<std::vector<Muon> > outM; 

  //// Electron WPs
  const double isoCutE;
  const std::string rhoLabel;
  const std::string eaLabel; // use this effective area to correct isolation

  // for the case where the effective areas are for the wrong cone size
  const double eaScaleFactor; 

  const double isoConeDRMaxE;
  const double isoConeDRMinE;
  // only worry about isolation veto cone in barrel
  const double isoConeVetoEtaThresholdE;

  //// Muon WPs
  const double isoCutM;
  const double isoConeDRMaxM;
  const double isoConeDRMinM;

  // Consider fsr from leptons passing these selections
  StringCutObjectSelector<Elec> fsrElecSelection;
  StringCutObjectSelector<Muon> fsrMuonSelection;

  // Label of FSR userCand
  const std::string fsrLabel;
};


// Constructors and destructors

MiniAODLeptonHZZIsoDecider::MiniAODLeptonHZZIsoDecider(const edm::ParameterSet& iConfig):
  collectionTokenE(consumes<ElecView>(iConfig.exists("srcE") ? 
                                      iConfig.getParameter<edm::InputTag>("srcE") :
                                      edm::InputTag("slimmedElectrons"))),
  collectionTokenM(consumes<MuonView>(iConfig.exists("srcMu") ? 
                                      iConfig.getParameter<edm::InputTag>("srcMu") :
                                      edm::InputTag("slimmedMuons"))),
  isoValueLabel(iConfig.exists("isoValueLabel") ?
                iConfig.getParameter<std::string>("isoValueLabel") :
                std::string("HZZ4lIso")),
  isoDecisionLabel(iConfig.exists("isoDecisionLabel") ?
                   iConfig.getParameter<std::string>("isoDecisionLabel") :
                   std::string("HZZ4lIsoPass")),
  isoCutE(iConfig.exists("isoCutE") ? iConfig.getParameter<double>("isoCutE") : 0.5),
  rhoLabel(iConfig.exists("rhoLabel") ?
	   iConfig.getParameter<std::string>("rhoLabel") :
	   std::string("rho_fastjet")),
  eaLabel(iConfig.exists("eaLabel") ?
	  iConfig.getParameter<std::string>("eaLabel") :
	  std::string("EffectiveArea")),
  eaScaleFactor(iConfig.exists("eaScaleFactor") ? 
                iConfig.getParameter<double>("eaScaleFactor") : 1.),
  isoConeDRMaxE(iConfig.exists("isoConeDRMaxE") ? 
                iConfig.getParameter<double>("isoConeDRMaxE") : 0.4),
  isoConeDRMinE(iConfig.exists("isoConeDRMinE") ? 
                iConfig.getParameter<double>("isoConeDRMinE") : 0.08),
  isoConeVetoEtaThresholdE(iConfig.exists("isoConeVetoEtaThresholdE") ? 
                           iConfig.getParameter<double>("isoConeVetoEtaThreshold") : 
                           1.479),
  isoCutM(iConfig.exists("isoCutMu") ? iConfig.getParameter<double>("isoCutMu") : 0.4),
  isoConeDRMaxM(iConfig.exists("isoConeDRMaxMu") ? 
                iConfig.getParameter<double>("isoConeDRMaxMu") : 0.4),
  isoConeDRMinM(iConfig.exists("isoConeDRMinMu") ? 
                iConfig.getParameter<double>("isoConeDRMinMu") : 0.01),
  fsrElecSelection(iConfig.exists("fsrElecSelection") ?
                   iConfig.getParameter<std::string>("fsrElecSelection") :
                   ""),
  fsrMuonSelection(iConfig.exists("fsrMuonSelection") ?
                   iConfig.getParameter<std::string>("fsrMuonSelection") :
                   ""),
  fsrLabel(iConfig.exists("fsrLabel") ?
           iConfig.getParameter<std::string>("fsrLabel") :
           std::string("dretFSRCand"))
{
  produces<std::vector<Elec> >("electrons");
  produces<std::vector<Muon> >("muons");
}


void MiniAODLeptonHZZIsoDecider::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle<ElecView> elecsIn;
  edm::Handle<MuonView> muonsIn;

  iEvent.getByToken(collectionTokenE, elecsIn);
  iEvent.getByToken(collectionTokenM, muonsIn);

  std::vector<CandPtr> fsr = getFSR(elecsIn, muonsIn);

  outE = makeCollection(elecsIn, fsr);
  outM = makeCollection(muonsIn, fsr);

  iEvent.put(outE, "electrons");
  iEvent.put(outM, "muons");
}
    

template<typename Lep>
std::auto_ptr<std::vector<Lep> >
MiniAODLeptonHZZIsoDecider::makeCollection(const edm::Handle<edm::View<Lep> >& lepsIn,
                                           const std::vector<CandPtr>& fsrs) const
{
  std::auto_ptr<std::vector<Lep> > out = 
    std::auto_ptr<std::vector<Lep> >(new std::vector<Lep>);

  for(size_t iLep = 0; iLep < lepsIn->size(); ++iLep)
    {
      const edm::Ptr<Lep> lep = lepsIn->ptrAt(iLep);

      out->push_back(*lep); // copy lepton to save correctly in event

      // Something about the HZZ electron energy corrections causes
      // some electrons to have pt of 0; do this to avoid an infinity
      float iso = 9999.;
      bool decision  = false;
      if(out->back().pt() > 0.)
        {
          iso = relPFIsoFSR(lep, fsrs);
          decision = (iso < getIsoCut(lep));
        }
      out->back().addUserFloat(isoValueLabel, iso);
      out->back().addUserFloat(isoDecisionLabel, float(decision)); // 1 for true, 0 for false

    }

  return out;
}


template<typename Lep>
float 
MiniAODLeptonHZZIsoDecider::relPFIsoFSR(const edm::Ptr<Lep>& lep,
                                        const std::vector<CandPtr>& fsrs) const
{
  float chHadIso = isolationVariables(lep).sumChargedHadronPt;
  float nHadIso = isolationVariables(lep).sumNeutralHadronEt;
  float phoIso = isolationVariables(lep).sumPhotonEt;
  float puCorrection = isoPUCorrection(lep);

  float fsrCorrection = isoFSRCorrection(lep, fsrs);
  
  float neutralIso = nHadIso + phoIso - puCorrection - fsrCorrection;
  if(neutralIso < 0.)
    neutralIso = 0.;

  return ((chHadIso + neutralIso) / lep->pt());
}


float
MiniAODLeptonHZZIsoDecider::isoPUCorrection(const ElecPtr& e) const
{
  return (e->userFloat(rhoLabel) * 
          e->userFloat(eaLabel) * 
          eaScaleFactor);
}


float
MiniAODLeptonHZZIsoDecider::isoPUCorrection(const MuonPtr& m) const
{
  return 0.5 * isolationVariables(m).sumPUPt;
}


const reco::GsfElectron::PflowIsolationVariables&
MiniAODLeptonHZZIsoDecider::isolationVariables(const ElecPtr& e) const
{
  return e->pfIsolationVariables();
}


const reco::MuonPFIsolation&
MiniAODLeptonHZZIsoDecider::isolationVariables(const MuonPtr& m) const
{
  return m->pfIsolationR03();
}


template<typename Lep>
float
MiniAODLeptonHZZIsoDecider::isoFSRCorrection(const edm::Ptr<Lep>& lep,
                                             const std::vector<CandPtr>& fsrs) const
{
  float corr = 0.;

  for(auto iFSR = fsrs.begin(); iFSR != fsrs.end(); iFSR++)
    {
      if(fsrInIsoCone(lep, *iFSR))
         corr += (*iFSR)->pt();
    }

  return corr;
}


bool
MiniAODLeptonHZZIsoDecider::fsrInIsoCone(const ElecPtr& e,
                                         const CandPtr& fsr) const
{
  // float fsrDR = reco::deltaR(*fsr, *(e->superCluster()));
  float fsrDR = reco::deltaR(fsr->p4(), e->p4());

  bool inCone = (fsrDR < isoConeDRMaxE && 
                 (e->superCluster()->eta() < isoConeVetoEtaThresholdE ||
                  fsrDR > isoConeDRMinE));

  return inCone;
}


bool
MiniAODLeptonHZZIsoDecider::fsrInIsoCone(const MuonPtr& m,
                                         const CandPtr& fsr) const
{
  float fsrDR = reco::deltaR(fsr->p4(), m->p4());

  return (fsrDR < isoConeDRMaxM && fsrDR > isoConeDRMinM);
}


std::vector<CandPtr> 
MiniAODLeptonHZZIsoDecider::getFSR(const edm::Handle<ElecView>& elecs,
                                   const edm::Handle<MuonView>& muons) const
{
  std::vector<CandPtr> out;

  addFSR(elecs, out);
  addFSR(muons, out);

  return out;
}


template<typename Lep>
void
MiniAODLeptonHZZIsoDecider::addFSR(const edm::Handle<edm::View<Lep> >& leps,
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
MiniAODLeptonHZZIsoDecider::selectFSRLep(const ElecPtr& e) const
{
  return fsrElecSelection(*e);
}


bool
MiniAODLeptonHZZIsoDecider::selectFSRLep(const MuonPtr& m) const
{
  return fsrMuonSelection(*m);
}


//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODLeptonHZZIsoDecider);








