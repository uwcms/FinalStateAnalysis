#include "FinalStateAnalysis/PatTools/plugins/MiniAODObjectEmbedFSR.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Lepton.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"

template<typename T, typename U>
void MiniAODObjectEmbedFSR<T,U>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // Read the shallow clones of a candidate and save the SECOND Clone
  edm::Handle<std::vector<T> > srcTemp;
  edm::Handle<std::vector<U> > srcAltTemp;
  edm::Handle<std::vector<pat::Electron> > srcVetoTemp;

  // Get stuff
  iEvent.getByLabel(src_,srcTemp);
  iEvent.getByLabel(srcAlt_,srcAltTemp);
  iEvent.getByLabel(srcVeto_,srcVetoTemp);
  iEvent.getByLabel(srcVtx_,srcVtx);
  iEvent.getByLabel(srcPho_,srcPho);

  // copy into container we're going to put into the event now to avoid const issues
  src->assign(srcTemp->begin(),srcTemp->end());
  srcAlt->assign(srcAltTemp->begin(),srcAltTemp->end());
  srcVeto->assign(srcVetoTemp->begin(),srcVetoTemp->end());
  // for(unsigned int q = 0; q < srcTemp->size(); ++q)
  //   {
  //     T temp = srcTemp->at(q);
  //     src->push_back(temp);
  //   }


  for(std::vector<pat::PFParticle>::const_iterator pho = srcPho->cbegin(); pho != srcPho->cend(); ++pho) 
    {
      // preselection
      if(pho->pt() < ptInner || fabs(pho->eta()) > maxEta) continue;

      // Loop through lepton candidates, keep track of the best one (smallest dPhi)
      typename std::vector<T>::iterator bestCand = findBestLepton(*pho);

      if(bestCand == src->end()) continue; // no close lepton (or it's in the other collection)

      float dR = reco::deltaR(pho->p4(), bestCand->p4());

      if(dR > dROuter) continue;
      float fsrIso = photonRelIso(*pho);
      if(dR > dRInner)
	{
	  if(fsrIso > isoOuter || pho->pt() < ptOuter) continue;
	}
      else
	{
	  if(fsrIso > isoInner || pho->pt() < ptInner) continue;
	}

      // Cluster veto
      if(!passClusterVeto(*pho, *bestCand)) continue;

      embedFSRCand(bestCand, pho);
    }

  iEvent.put(src);
}


template<typename T, typename U>
typename std::vector<T>::iterator MiniAODObjectEmbedFSR<T,U>::findBestLepton(const pat::PFParticle& pho)
{
  // Find closest lepton
  typename std::vector<T>::iterator out;
  float bestDR = 999.;
  for(typename std::vector<T>::iterator lept = src->begin(); lept != src->end(); ++lept)
    {
      float dR = reco::deltaR(pho.p4(), lept->p4());
      if(dR < bestDR && leptonPassID(*lept))
	{
	  out = lept;
	  bestDR = dR;
	}
    }

  // none found
  if(bestDR == 999.) return src->end();

  // If we did find a decent one, make sure there's not a better one from the other lepton collection
  for(typename std::vector<U>::iterator lept = srcAlt->begin(); lept != srcAlt->end(); ++lept)
    {
      float dR = reco::deltaR(pho.p4(), lept->p4());
      if(dR < bestDR && leptonPassID(*lept))
	{
	  // Better lepton in other collection -- never mind!
	  return src->end();
	}
    }

  // If we got this far, we must be ok
  return out;
}

// Relative isolation, summing all types passed in in isoLabels
template<typename T, typename U>
float MiniAODObjectEmbedFSR<T,U>::photonRelIso(const pat::PFParticle& pho) const
{
  float phoIso = 0.;
  for(std::vector<std::string>::const_iterator isoType = isoLabels_.begin();
      isoType != isoLabels_.end(); ++isoType)
    {
      phoIso += pho.userFloat(*isoType);
    }
  phoIso /= pho.pt(); // relative isolation

  return phoIso;
}

template<typename T, typename U>
template<typename leptonType>
bool MiniAODObjectEmbedFSR<T,U>::leptonPassID(leptonType& lept)
{
  if(lept.hasUserInt(std::string("passMiniAODFSREmbedderID")))
    return (lept.userInt("passMiniAODFSREmbedderID") == 1);

  if(!(lept.isElectron() || lept.isMuon()))
    {
      return false;
    }

  bool passID = idHelper(lept);
  
  // store so we don't have to recalculate
  lept.addUserInt("passMiniAODFSREmbedderID", passID ? 1 : 0);
  
  return passID;
}

template<typename T, typename U>
bool MiniAODObjectEmbedFSR<T,U>::idHelper(const pat::Electron& e) const
{
  float pt = e.pt();
  float eta = fabs(e.superCluster()->eta());

  bool passSelection = pt > electronPt &&
    eta < electronMaxEta &&
    fabs(e.dB(pat::Electron::PV3D))/e.edB(pat::Electron::PV3D) < electronSIP && // SIP3D cut
    fabs(e.gsfTrack()->dxy(srcVtx->at(0).position())) < electronPVDXY &&
    fabs(e.gsfTrack()->dz(srcVtx->at(0).position())) < electronPVDZ;
  
  float bdtCut;
  if(e.pt() < electronIDPtThr)
    {
      if(eta < electronIDEtaThrLow)
	bdtCut = electronIDCutLowPtLowEta;
      else if(eta < electronIDEtaThrHigh)
	bdtCut = electronIDCutLowPtMedEta;
      else
	bdtCut = electronIDCutLowPtHighEta;
    }
  else
    {
      if(eta < electronIDEtaThrLow)
	bdtCut = electronIDCutHighPtLowEta;
      else if(eta < electronIDEtaThrHigh)
	bdtCut = electronIDCutHighPtMedEta;
      else
	bdtCut = electronIDCutHighPtHighEta;
    }
  bool passID = e.userFloat(electronIDLabel_) < bdtCut;
  return passID & passSelection;
}

template<typename T, typename U>
bool MiniAODObjectEmbedFSR<T,U>::idHelper(const pat::Muon& m) const
{
  bool passID = (m.isPFMuon()==1 && (m.isGlobalMuon() || m.isTrackerMuon()));
  bool passSelection = m.pt() > muonPt &&
    fabs(m.eta()) < muonMaxEta &&
    fabs(m.dB(pat::Muon::PV3D))/m.edB(pat::Muon::PV3D) < muonSIP && // SIP3D cut
    fabs(m.muonBestTrack()->dxy(srcVtx->at(0).position())) < muonPVDXY &&
    fabs(m.muonBestTrack()->dz(srcVtx->at(0).position())) < muonPVDZ;
  return passID && passSelection;
}

template<typename T, typename U>
bool MiniAODObjectEmbedFSR<T,U>::passClusterVeto(const pat::PFParticle& pho, const reco::Candidate& pairedLep)
{
  for(pat::ElectronCollection::iterator elec = srcVeto->begin(); elec != srcVeto->end(); ++elec)
    {
      bool passDR = reco::deltaR(pho.eta(), pho.phi(), elec->superCluster()->eta(), elec->superCluster()->phi()) < vetoDR;
      bool passDPhi = fabs(reco::deltaPhi(pho.phi(), elec->superCluster()->phi())) < vetoDPhi;
      bool passDEta = fabs(pho.eta() - elec->superCluster()->eta()) < vetoDEta;
      if(! (passDR || (passDEta && passDPhi))) continue;

      if(reco::deltaR(pairedLep.p4(), elec->p4()) < 0.0001) continue; // same object

      if(!leptonPassID(*elec)) continue;

      // Found a vetoing electron
      return false;
    }
  
  // Found no vetoing electrons
  return true;
}

template<typename T, typename U>
int MiniAODObjectEmbedFSR<T,U>::embedFSRCand(typename std::vector<T>::iterator& lept, const std::vector<pat::PFParticle>::const_iterator& pho)
{
  int n, nFSRCands=0; // This is the nth photon; when it's placed there will be nFSRCands=n+1 total
  if(!lept->hasUserInt("nFSRCands"))
    n = 0;
  else
    n = lept->userInt("nFSRCands");

  if(pho->sourceCandidatePtr(0).isNonnull())
    {
      nFSRCands = n+1;
      lept->addUserInt("nFSRCands", nFSRCands);
      
      // The argument to sourceCandidatePtr doesn't appear to matter?
      lept->addUserCand(label_+"Pt"+std::to_string(n), pho->sourceCandidatePtr(0)); 
    }
  return nFSRCands;
}

typedef MiniAODObjectEmbedFSR<pat::Muon, pat::Electron> MiniAODMuonFSREmbedder;
typedef MiniAODObjectEmbedFSR<pat::Electron, pat::Muon> MiniAODElectronFSREmbedder;

DEFINE_FWK_MODULE(MiniAODMuonFSREmbedder);
DEFINE_FWK_MODULE(MiniAODElectronFSREmbedder);
