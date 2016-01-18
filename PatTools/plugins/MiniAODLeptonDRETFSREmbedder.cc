//////////////////////////////////////////////////////////////////////////////
///                                                                        ///
///    MiniAODLeptonDRETFSREmbedder.cc                                     ///
///                                                                        ///
///    From a collection of photons, a collection of muons, and a          ///
///        collection of electrons: make sure each photon is not in an     ///
///        electron supercluster, and pair it to its closest lepton.       ///
///        For each lepton, embed the photon with the smallest deltaR/eT   ///
///        as a usercand. Cut strings may be supplied for all three types  ///
///        of objects.                                                     ///
///                                                                        ///
///    Author: Nate Woods, U. Wisconsin                                    ///
///                                                                        ///
//////////////////////////////////////////////////////////////////////////////


// system include files
#include <memory>
#include <iostream>
#include <math.h> // pow

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include <DataFormats/PatCandidates/interface/PFParticle.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/PatCandidates/interface/Electron.h>
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"


typedef reco::Candidate Cand;
typedef edm::Ptr<Cand> CandPtr;
typedef reco::CandidateView CandView;
typedef pat::Electron Elec;
typedef edm::Ptr<pat::Electron> ElecPtr;
typedef edm::View<pat::Electron> ElecView;
typedef pat::Muon Muon;
typedef edm::Ptr<pat::Muon> MuonPtr;
typedef edm::View<pat::Muon> MuonView;

class MiniAODLeptonDRETFSREmbedder : public edm::EDProducer
{
public:
  explicit MiniAODLeptonDRETFSREmbedder(const edm::ParameterSet&);
  ~MiniAODLeptonDRETFSREmbedder();

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);
  edm::EDGetTokenT<CandView> photons_;
  edm::EDGetTokenT<ElecView> electrons_;
  edm::EDGetTokenT<MuonView> muons_;

  bool isInSuperCluster(const CandPtr& cand, const std::vector<ElecPtr>& elecs) const;
  
  StringCutObjectSelector<Cand> phoSelection_;
  StringCutObjectSelector<Elec> eSelection_;
  StringCutObjectSelector<Muon> mSelection_;

  std::string fsrLabel_;
  
  const float cut_; // the actual cut on deltaR/eT^n

  const float scVetoDR_;
  const float scVetoDEta_;
  const float scVetoDPhi_;
  const float etPower_;
  const float maxDR_;
};


MiniAODLeptonDRETFSREmbedder::MiniAODLeptonDRETFSREmbedder(const edm::ParameterSet& iConfig):
  photons_(consumes<CandView>(iConfig.getParameter<edm::InputTag>("phoSrc"))),
  electrons_(consumes<ElecView>(iConfig.getParameter<edm::InputTag>("eSrc"))),
  muons_(consumes<MuonView>(iConfig.getParameter<edm::InputTag>("muSrc"))),
  phoSelection_(iConfig.exists("phoSelection") ? 
                iConfig.getParameter<std::string>("phoSelection") :
                ""),
  eSelection_(iConfig.exists("eSelection") ?
	      iConfig.getParameter<std::string>("eSelection") :
	      ""),
  mSelection_(iConfig.exists("muSelection") ? 
	      iConfig.getParameter<std::string>("muSelection") :
	      ""),
  fsrLabel_(iConfig.exists("fsrLabel") ?
            iConfig.getParameter<std::string>("fsrLabel") :
            "dREtFSRCand"),
  cut_(iConfig.exists("cut") ?
       float(iConfig.getParameter<double>("cut")) :
       0.012), // cut on dR/eT^2 as of 21 October 2015
  scVetoDR_(iConfig.exists("scVetoDR") ?
            float(iConfig.getParameter<double>("scVetoDR")) :
            0.15),
  scVetoDEta_(iConfig.exists("scVetoDEta") ?
              float(iConfig.getParameter<double>("scVetoDEta")) :
              0.05),
  scVetoDPhi_(iConfig.exists("scVetoDPhi") ?
              float(iConfig.getParameter<double>("scVetoDPhi")) :
              2.),
  etPower_(iConfig.exists("etPower") ?
	   float(iConfig.getParameter<double>("etPower")) :
	   1.),
  maxDR_(iConfig.exists("maxDR") ?
         float(iConfig.getParameter<double>("maxDR")) :
         0.5)

{
  produces<std::vector<Muon> >();
  produces<std::vector<Elec> >();
}


MiniAODLeptonDRETFSREmbedder::~MiniAODLeptonDRETFSREmbedder()
{
}


void MiniAODLeptonDRETFSREmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::auto_ptr<std::vector<Muon> > mOut( new std::vector<Muon> );
  std::auto_ptr<std::vector<Elec> > eOut( new std::vector<Elec> );
  edm::Handle<CandView> phos;
  iEvent.getByToken(photons_, phos);
  edm::Handle<edm::View<Elec> > elecs;
  iEvent.getByToken(electrons_, elecs);
  edm::Handle<edm::View<Muon> > mus;
  iEvent.getByToken(muons_, mus);

  // get a cleaned electron collection because we need it for the SC veto anyway
  std::vector<ElecPtr> cleanedElectrons;
  for(size_t iE = 0; iE < elecs->size(); ++iE)
    {
      ElecPtr elec = elecs->ptrAt(iE);
      if(eSelection_(*elec))
        cleanedElectrons.push_back(elec);
    }

  // associate photons to their closest leptons
  std::vector<std::vector<CandPtr> > phosByEle = std::vector<std::vector<CandPtr> >(elecs->size());
  std::vector<std::vector<CandPtr> > phosByMu = std::vector<std::vector<CandPtr> >(mus->size());

  for( size_t iPho = 0; iPho != phos->size(); ++iPho )
    {
      CandPtr pho = phos->ptrAt(iPho);
      
      // basic selection
      if (!phoSelection_(*pho))
        continue;

      // supercluster veto
      if(isInSuperCluster(pho, cleanedElectrons))
        continue;

      size_t iBestEle = 9999;
      size_t iBestMu = 9999;
      float dRBestEle = 9999.;
      float dRBestMu = 9999.;

      for(size_t iE = 0; iE < elecs->size(); ++iE)
        {
          float deltaR = reco::deltaR(pho->p4(), elecs->at(iE).p4());

          if(!eSelection_(elecs->at(iE)))
            continue;

          if(deltaR < dRBestEle)
            {
              iBestEle = iE;
              dRBestEle = deltaR;
            }
        }

      for(size_t iM = 0; iM < mus->size(); ++iM)
        {
          float deltaR = reco::deltaR(pho->p4(), mus->at(iM).p4());

          if(!mSelection_(mus->at(iM)))
            continue;

          if(deltaR < dRBestMu)
            {
              iBestMu = iM;
              dRBestMu = deltaR;
            }
        }

      if(elecs->size() && dRBestEle < dRBestMu && dRBestEle < maxDR_)
        phosByEle.at(iBestEle).push_back(pho);
      else if(mus->size() && dRBestMu < maxDR_)
        phosByMu.at(iBestMu).push_back(pho);
    }

  for(size_t iE = 0; iE < elecs->size(); ++iE)
    {
      Elec e = elecs->at(iE);
      
      CandPtr bestPho;
      float dREtBestPho = 9999.;
      
      for(size_t iPho = 0; iPho < phosByEle[iE].size(); ++iPho)
        {
          CandPtr pho = phosByEle[iE][iPho];

          float drEt = reco::deltaR(e.p4(), pho->p4()) / pow(pho->et(), etPower_);

          if(drEt < cut_ && drEt < dREtBestPho)
            {
              dREtBestPho = drEt;
              bestPho = pho;
            }
        }

      if(bestPho.isNonnull())
        {
          e.addUserCand(fsrLabel_, bestPho);
          e.addUserFloat(fsrLabel_+"DREt", dREtBestPho);
        }

      eOut->push_back(e);
    }

  for(size_t iM = 0; iM < mus->size(); ++iM)
    {
      Muon m = mus->at(iM);
      
      CandPtr bestPho;
      float dREtBestPho = 9999.;
      
      for(size_t iPho = 0; iPho < phosByMu[iM].size(); ++iPho)
        {
          CandPtr pho = phosByMu[iM][iPho];

          float drEt = reco::deltaR(m.p4(), pho->p4()) / pow(pho->et(), etPower_);

          if(drEt < cut_ && drEt < dREtBestPho)
            {
              dREtBestPho = drEt;
              bestPho = pho;
            }
        }

      if(bestPho.isNonnull())
        {
          m.addUserCand(fsrLabel_, bestPho);
          m.addUserFloat(fsrLabel_+"DREt", dREtBestPho);
        }

      mOut->push_back(m);
    }

  iEvent.put( eOut );
  iEvent.put( mOut );
}


bool MiniAODLeptonDRETFSREmbedder::isInSuperCluster(const CandPtr& cand, 
                                               const std::vector<ElecPtr>& elecs) const
{
  for(auto elec = elecs.begin(); elec != elecs.end(); ++elec)
    {
      float dR = reco::deltaR(cand->eta(), cand->phi(), (*elec)->superCluster()->eta(), (*elec)->superCluster()->phi());
      if(dR < scVetoDR_)
        return true;

      float dEta = fabs((*elec)->superCluster()->eta() - cand->eta());
      float dPhi = fabs(reco::deltaPhi((*elec)->superCluster()->phi(), cand->phi()));
      if(dEta < scVetoDEta_ && dPhi < scVetoDPhi_)
        return true;
    }

  return false;
}


//define this as a plug-in
DEFINE_FWK_MODULE(MiniAODLeptonDRETFSREmbedder);
