//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODElectronHZZIDDecider.cc                                         //
//                                                                          //
//   Embeds electron ID and siolation decisions as userfloats               //
//       (1 for true, 0for false), for use in other modules using           //
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
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"


class MiniAODElectronHZZIDDecider : public edm::stream::EDProducer<>
{
public:
  explicit MiniAODElectronHZZIDDecider(const edm::ParameterSet&);
  ~MiniAODElectronHZZIDDecider() {}

private:
  // Methods
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  bool passKinematics(const edm::Ptr<pat::Electron>& elec) const;
  bool passVertex(const edm::Ptr<pat::Electron>& elec,
                  const reco::Vertex& vtx) const;
  bool passBDT(const edm::Ptr<pat::Electron>& elec) const;
  bool passMissingHits(const edm::Ptr<pat::Electron>& elec) const;
  float PFRelIsoRhoNoFSR(const edm::Ptr<pat::Electron>& elec) const;

  // Data
  const edm::EDGetTokenT<edm::View<pat::Electron> > electronCollectionToken_;
  const std::string idLabel_; // label for the decision userfloat
  const std::string isoLabel_;
  const edm::EDGetTokenT<reco::VertexCollection> vtxSrc_; // primary vertex (for veto PV and SIP cuts)

  const double ptCut;
  const double etaCut;
  const double sipCut;
  const double pvDXYCut;
  const double pvDZCut;
  const double idPtThr;
  const double idEtaThrLow;
  const double idEtaThrHigh;
  const double idCutLowPtLowEta;
  const double idCutLowPtMedEta;
  const double idCutLowPtHighEta;
  const double idCutHighPtLowEta;
  const double idCutHighPtMedEta;
  const double idCutHighPtHighEta;
  const std::string bdtLabel;
  const int missingHitsCut;
  const double isoCut;
  const std::string rhoLabel;
  const std::string eaLabel; // use this effective area to correct isolation
  const bool checkMVAID;
  
  StringCutObjectSelector<pat::Electron> selector;
};


// Constructors and destructors

MiniAODElectronHZZIDDecider::MiniAODElectronHZZIDDecider(const edm::ParameterSet& iConfig):
  electronCollectionToken_(consumes<edm::View<pat::Electron> >(iConfig.exists("src") ? 
                                                               iConfig.getParameter<edm::InputTag>("src") :
                                                               edm::InputTag("slimmedElectrons"))),
  idLabel_(iConfig.exists("idLabel") ?
	   iConfig.getParameter<std::string>("idLabel") :
	   std::string("HZZ4lIDPass")),
  isoLabel_(iConfig.exists("isoLabel") ?
	   iConfig.getParameter<std::string>("isoLabel") :
	   std::string("HZZ4lIsoPass")),
  vtxSrc_(consumes<reco::VertexCollection>(iConfig.exists("vtxSrc") ? 
                                           iConfig.getParameter<edm::InputTag>("vtxSrc") : 
                                           edm::InputTag("selectedPrimaryVertex"))),
  ptCut(iConfig.exists("ptCut") ? iConfig.getParameter<double>("ptCut") : 7.),
  etaCut(iConfig.exists("etaCut") ? iConfig.getParameter<double>("etaCut") : 2.5),
  sipCut(iConfig.exists("sipCut") ? iConfig.getParameter<double>("sipCut") : 4.),
  pvDXYCut(iConfig.exists("pvDXYCut") ? iConfig.getParameter<double>("pvDXYCut") : 0.5),
  pvDZCut(iConfig.exists("pvDZCut") ? iConfig.getParameter<double>("pvDZCut") : 1.),
  idPtThr(iConfig.exists("idPtThr") ? iConfig.getParameter<double>("idPtThr") : 10.),
  idEtaThrLow(iConfig.exists("idEtaThrLow") ? iConfig.getParameter<double>("idEtaThrLow") : 0.8),
  idEtaThrHigh(iConfig.exists("idEtaThrHigh") ? iConfig.getParameter<double>("idEtaThrHigh") : 1.479),
  idCutLowPtLowEta(iConfig.exists("idCutLowPtLowEta") ? iConfig.getParameter<double>("idCutLowPtLowEta") : -0.586),
  idCutLowPtMedEta(iConfig.exists("idCutLowPtMedEta") ? iConfig.getParameter<double>("idCutLowPtMedEta") : -0.712),
  idCutLowPtHighEta(iConfig.exists("idCutLowPtHighEta") ? iConfig.getParameter<double>("idCutLowPtHighEta") : -0.662),
  idCutHighPtLowEta(iConfig.exists("idCutHighPtLowEta") ? iConfig.getParameter<double>("idCutHighPtLowEta") : 0.652),
  idCutHighPtMedEta(iConfig.exists("idCutHighPtMedEta") ? iConfig.getParameter<double>("idCutHighPtMedEta") : 0.701),
  idCutHighPtHighEta(iConfig.exists("idCutHighPtHighEta") ? iConfig.getParameter<double>("idCutHighPtHighEta") : 0.350),
  bdtLabel(iConfig.exists("bdtLabel") ? iConfig.getParameter<std::string>("bdtLabel") : "BDTIDNonTrig"),
  missingHitsCut(iConfig.exists("missingHitsCut") ? iConfig.getParameter<int>("missingHitsCut") : 1),
  isoCut(iConfig.exists("isoCut") ? iConfig.getParameter<double>("isoCut") : 0.5),
  rhoLabel(iConfig.exists("rhoLabel") ?
	   iConfig.getParameter<std::string>("rhoLabel") :
	   std::string("rhoCSA14")),
  eaLabel(iConfig.exists("eaLabel") ?
	  iConfig.getParameter<std::string>("eaLabel") :
	  std::string("EffectiveArea_HZZ4l2015")),
  checkMVAID(bdtLabel != ""),
  selector(iConfig.exists("selection") ?
	    iConfig.getParameter<std::string>("selection") :
	    "")
{
  produces<std::vector<pat::Electron> >();
}


void MiniAODElectronHZZIDDecider::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::auto_ptr<std::vector<pat::Electron> > out = 
    std::auto_ptr<std::vector<pat::Electron> >(new std::vector<pat::Electron>);

  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vtxSrc_,vertices);

  edm::Handle<edm::View<pat::Electron> > electronsIn;
  iEvent.getByToken(electronCollectionToken_, electronsIn);

  for(edm::View<pat::Electron>::const_iterator ei = electronsIn->begin();
      ei != electronsIn->end(); ei++) // loop over electrons
    {
      const edm::Ptr<pat::Electron> eptr(electronsIn, ei - electronsIn->begin());

      out->push_back(*ei); // copy electron to save correctly in event

      bool idResult = selector(*eptr) && (passKinematics(eptr) && passVertex(eptr, vertices->at(0)) && passMissingHits(eptr));
      out->back().addUserFloat(idLabel_, float(idResult)); // 1 for true, 0 for false

      out->back().addUserFloat(idLabel_+"Tight", float(idResult && passBDT(eptr))); // 1 for true, 0 for false
      
      bool isoResult = (PFRelIsoRhoNoFSR(eptr) < isoCut);
      out->back().addUserFloat(isoLabel_, float(isoResult)); // 1 for true, 0 for false
    }

  iEvent.put(out);
}


bool MiniAODElectronHZZIDDecider::passKinematics(const edm::Ptr<pat::Electron>& elec) const
{
  bool result = (elec->pt() > ptCut);
  result = (result && fabs(elec->eta()) < etaCut);
  return result;
}


bool MiniAODElectronHZZIDDecider::passVertex(const edm::Ptr<pat::Electron>& elec,
                                             const reco::Vertex& vtx) const
{
  return (fabs(elec->dB(pat::Electron::PV3D))/elec->edB(pat::Electron::PV3D) < sipCut && 
	  fabs(elec->gsfTrack()->dxy(vtx.position())) < pvDXYCut &&
	  fabs(elec->gsfTrack()->dz(vtx.position())) < pvDZCut);
}


bool MiniAODElectronHZZIDDecider::passBDT(const edm::Ptr<pat::Electron>& elec) const
{
  if(!checkMVAID)
    return true;

  double pt = elec->pt();
  double eta = fabs(elec->superCluster()->eta());

  double bdtCut;
  if(pt < idPtThr)
    {
      if(eta < idEtaThrLow)
	bdtCut = idCutLowPtLowEta;
      else if(eta < idEtaThrHigh)
	bdtCut = idCutLowPtMedEta;
      else
	bdtCut = idCutLowPtHighEta;
    }
  else
    {
      if(eta < idEtaThrLow)
	bdtCut = idCutHighPtLowEta;
      else if(eta < idEtaThrHigh)
	bdtCut = idCutHighPtMedEta;
      else
	bdtCut = idCutHighPtHighEta;
    }

  return (elec->userFloat(bdtLabel) > bdtCut);
}


bool MiniAODElectronHZZIDDecider::passMissingHits(const edm::Ptr<pat::Electron>& elec) const
{
  return (elec->gsfTrack()->hitPattern().numberOfHits(reco::HitPattern::MISSING_INNER_HITS) <= missingHitsCut);
}


float MiniAODElectronHZZIDDecider::PFRelIsoRhoNoFSR(const edm::Ptr<pat::Electron>& elec) const
{
  float chHadIso = elec->chargedHadronIso();
  float nHadIso = elec->neutralHadronIso();
  float phoIso = elec->photonIso();
  float puCorrection = elec->userFloat(rhoLabel) * elec->userFloat(eaLabel);
  
  float neutralIso = nHadIso + phoIso - puCorrection;
  if(neutralIso < 0.)
    neutralIso = 0.;

  return ((chHadIso + neutralIso) / elec->pt());
}


//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODElectronHZZIDDecider);








