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
#include "FWCore/Framework/interface/EDProducer.h"
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


class MiniAODElectronHZZIDDecider : public edm::EDProducer
{
public:
  explicit MiniAODElectronHZZIDDecider(const edm::ParameterSet&);
  ~MiniAODElectronHZZIDDecider() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  bool passKinematics(const edm::Ptr<pat::Electron>& elec) const;
  bool passVertex(const edm::Ptr<pat::Electron>& elec) const;
  bool passBDT(const edm::Ptr<pat::Electron>& elec) const;
  bool passMissingHits(const edm::Ptr<pat::Electron>& elec) const;
  float PFRelIsoRhoNoFSR(const edm::Ptr<pat::Electron>& elec) const;

  // Data
  edm::EDGetTokenT<edm::View<pat::Electron> > electronCollectionToken_;
  std::string idLabel_; // label for the decision userfloat
  std::string isoLabel_;
  const edm::InputTag vtxSrc_; // primary vertex (for veto PV and SIP cuts)
  edm::Handle<reco::VertexCollection> vertices;
  std::auto_ptr<std::vector<pat::Electron> > out; // Collection we'll output at the end

  double ptCut;
  double etaCut;
  double sipCut;
  double pvDXYCut;
  double pvDZCut;
  double idPtThr;
  double idEtaThrLow;
  double idEtaThrHigh;
  double idCutLowPtLowEta;
  double idCutLowPtMedEta;
  double idCutLowPtHighEta;
  double idCutHighPtLowEta;
  double idCutHighPtMedEta;
  double idCutHighPtHighEta;
  std::string bdtLabel;
  int missingHitsCut;
  double isoCut;
  std::string rhoLabel;
  std::string eaLabel; // use this effective area to correct isolation

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
  vtxSrc_(iConfig.exists("vtxSrc") ? iConfig.getParameter<edm::InputTag>("vtxSrc") : edm::InputTag("selectedPrimaryVertex")),
  ptCut(iConfig.exists("ptCut") ? iConfig.getParameter<double>("ptCut") : 7.),
  etaCut(iConfig.exists("etaCut") ? iConfig.getParameter<double>("etaCut") : 2.5),
  sipCut(iConfig.exists("sipCut") ? iConfig.getParameter<double>("sipCut") : 4.),
  pvDXYCut(iConfig.exists("pvDXYCut") ? iConfig.getParameter<double>("pvDXYCut") : 0.5),
  pvDZCut(iConfig.exists("pvDZCut") ? iConfig.getParameter<double>("pvDZCut") : 1.),
  idPtThr(iConfig.exists("idPtThr") ? iConfig.getParameter<double>("idPtThr") : 10.),
  idEtaThrLow(iConfig.exists("idEtaThrLow") ? iConfig.getParameter<double>("idEtaThrLow") : 0.8),
  idEtaThrHigh(iConfig.exists("idEtaThrHigh") ? iConfig.getParameter<double>("idEtaThrHigh") : 1.479),
  idCutLowPtLowEta(iConfig.exists("idCutLowPtLowEta") ? iConfig.getParameter<double>("idCutLowPtLowEta") : -0.202),
  idCutLowPtMedEta(iConfig.exists("idCutLowPtMedEta") ? iConfig.getParameter<double>("idCutLowPtMedEta") : -0.444),
  idCutLowPtHighEta(iConfig.exists("idCutLowPtHighEta") ? iConfig.getParameter<double>("idCutLowPtHighEta") : 0.264),
  idCutHighPtLowEta(iConfig.exists("idCutHighPtLowEta") ? iConfig.getParameter<double>("idCutHighPtLowEta") : -0.110),
  idCutHighPtMedEta(iConfig.exists("idCutHighPtMedEta") ? iConfig.getParameter<double>("idCutHighPtMedEta") : -0.284),
  idCutHighPtHighEta(iConfig.exists("idCutHighPtHighEta") ? iConfig.getParameter<double>("idCutHighPtHighEta") : -0.212),
  bdtLabel(iConfig.exists("bdtLabel") ? iConfig.getParameter<std::string>("bdtLabel") : "BDTIDNonTrig"),
  missingHitsCut(iConfig.exists("missingHitsCut") ? iConfig.getParameter<int>("missingHitsCut") : 1),
  isoCut(iConfig.exists("isoCut") ? iConfig.getParameter<double>("isoCut") : 0.5),
  rhoLabel(iConfig.exists("rhoLabel") ?
	   iConfig.getParameter<std::string>("rhoLabel") :
	   std::string("rhoCSA14")),
  eaLabel(iConfig.exists("eaLabel") ?
	  iConfig.getParameter<std::string>("eaLabel") :
	  std::string("EffectiveArea_HZZ4l2015"))
{
  produces<std::vector<pat::Electron> >();
}


void MiniAODElectronHZZIDDecider::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  out = std::auto_ptr<std::vector<pat::Electron> >(new std::vector<pat::Electron>);

  edm::Handle<edm::View<pat::Electron> > electronsIn;
  iEvent.getByLabel(vtxSrc_,vertices);

  iEvent.getByToken(electronCollectionToken_, electronsIn);

  for(edm::View<pat::Electron>::const_iterator ei = electronsIn->begin();
      ei != electronsIn->end(); ei++) // loop over electrons
    {
      const edm::Ptr<pat::Electron> eptr(electronsIn, ei - electronsIn->begin());

      out->push_back(*ei); // copy electron to save correctly in event

      bool idResult = (passKinematics(eptr) && passVertex(eptr) && passMissingHits(eptr));
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


bool MiniAODElectronHZZIDDecider::passVertex(const edm::Ptr<pat::Electron>& elec) const
{
  return (fabs(elec->dB(pat::Electron::PV3D))/elec->edB(pat::Electron::PV3D) < sipCut && 
	  fabs(elec->gsfTrack()->dxy(vertices->at(0).position())) < pvDXYCut &&
	  fabs(elec->gsfTrack()->dz(vertices->at(0).position())) < pvDZCut);
}


bool MiniAODElectronHZZIDDecider::passBDT(const edm::Ptr<pat::Electron>& elec) const
{
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


void MiniAODElectronHZZIDDecider::beginJob()
{}


void MiniAODElectronHZZIDDecider::endJob()
{}


void
MiniAODElectronHZZIDDecider::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODElectronHZZIDDecider);








