// #define _DEBUGFSR_ 1

#include "FinalStateAnalysis/PatTools/plugins/MiniAODObjectEmbedFSR.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Lepton.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "FWCore/Utilities/interface/Exception.h"

template<typename T, typename U>
void MiniAODObjectEmbedFSR<T,U>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // Read the shallow clones of a candidate and save the SECOND Clone
  edm::Handle<std::vector<T> > srcTemp;
  edm::Handle<std::vector<U> > srcAltTemp;
  edm::Handle<std::vector<pat::Electron> > srcVetoTemp;

  // Get stuff
  src = std::unique_ptr<std::vector<T> >(new std::vector<T>);
  iEvent.getByToken(srcToken_,srcTemp);
  src->assign(srcTemp->begin(),srcTemp->end());
  srcAlt = std::unique_ptr<std::vector<U> >(new std::vector<U>);
  iEvent.getByToken(srcAltToken_,srcAltTemp);
  srcAlt->assign(srcAltTemp->begin(),srcAltTemp->end());
  srcVeto = std::unique_ptr<pat::ElectronCollection>(new pat::ElectronCollection);
  iEvent.getByToken(srcVetoToken_,srcVetoTemp);
  srcVeto->assign(srcVetoTemp->begin(),srcVetoTemp->end());
  iEvent.getByToken(srcVtxToken_,srcVtx);
  iEvent.getByToken(srcPhoToken_,srcPho);

  for(std::vector<pat::PFParticle>::const_iterator pho = srcPho->cbegin(); pho != srcPho->cend(); ++pho) 
    {
      // preselection
      if(pho->pt() < ptInner || fabs(pho->eta()) > maxEta) continue;

      // Loop through lepton candidates, keep track of the best one (smallest dR)
      typename std::vector<T>::iterator bestCand = findBestLepton(*pho);

      if(bestCand == src->end()) continue; // no close lepton (or it's in the other collection)

      double dR = reco::deltaR(pho->p4(), bestCand->p4());

      if(dR > dROuter) continue;
      double fsrIso = photonRelIso(*pho);
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

  // count the number of stored photons and place it in the lepton as a userInt
  for(typename std::vector<T>::iterator iLep = src->begin(); iLep != src->end(); ++iLep)
    {
      unsigned int nFSR = 0;

      while(iLep->hasUserCand(label_+std::to_string(nFSR)))
	nFSR++;

      iLep->addUserInt("n"+label_, nFSR);
    }

  iEvent.put(std::move(src));
}


template<typename T, typename U>
typename std::vector<T>::iterator MiniAODObjectEmbedFSR<T,U>::findBestLepton(const pat::PFParticle& pho)
{
  // Find closest lepton
  typename std::vector<T>::iterator out;
  double bestDR = 999.;
  for(typename std::vector<T>::iterator lept = src->begin(); lept != src->end(); ++lept)
    {
      double dR = reco::deltaR(pho.p4(), lept->p4());
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
      double dR = reco::deltaR(pho.p4(), lept->p4());
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
double MiniAODObjectEmbedFSR<T,U>::photonRelIso(const pat::PFParticle& pho) const
{
  double phoIso = 0.;
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
bool MiniAODObjectEmbedFSR<T,U>::leptonPassID(const leptonType& lept) const
{
  return bool(lept.userFloat(idDecisionLabel_));
}

template<typename T, typename U>
template<typename leptonType>
bool MiniAODObjectEmbedFSR<T,U>::leptonPassIDTight(const leptonType& lept) const
{
  return bool(lept.userFloat(idDecisionLabel_+"Tight"));
}

template<typename T, typename U>
bool MiniAODObjectEmbedFSR<T,U>::passClusterVeto(const pat::PFParticle& pho, const reco::Candidate& pairedLep)
{
  for(pat::ElectronCollection::iterator elec = srcVeto->begin(); elec != srcVeto->end(); ++elec)
    {
      if(!leptonPassID(*elec)) continue;

      bool failDR = reco::deltaR(pho.eta(), pho.phi(), elec->superCluster()->eta(), elec->superCluster()->phi()) < vetoDR;
      bool failDPhi = fabs(reco::deltaPhi(pho.phi(), elec->superCluster()->phi())) < vetoDPhi;
      bool failDEta = fabs(pho.eta() - elec->superCluster()->eta()) < vetoDEta;
      if(! (failDR || (failDEta && failDPhi))) continue;

      // Found a vetoing electron
      return false;
    }
  
  // Found no vetoing electrons
  return true;
}

template<typename T, typename U>
int MiniAODObjectEmbedFSR<T,U>::embedFSRCand(typename std::vector<T>::iterator& lept, const std::vector<pat::PFParticle>::const_iterator& pho)
{
  unsigned int n = 0;
  while(lept->hasUserCand(label_+std::to_string(n)))
    n++;

  lept->addUserCand(label_+std::to_string(n), reco::CandidatePtr(srcPho, std::distance(srcPho->begin(), pho)));

  return n;
}

typedef MiniAODObjectEmbedFSR<pat::Muon, pat::Electron> MiniAODMuonFSREmbedder;
typedef MiniAODObjectEmbedFSR<pat::Electron, pat::Muon> MiniAODElectronFSREmbedder;

DEFINE_FWK_MODULE(MiniAODMuonFSREmbedder);
DEFINE_FWK_MODULE(MiniAODElectronFSREmbedder);
