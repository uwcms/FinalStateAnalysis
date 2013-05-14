#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataAlgos/interface/SmartTrigger.h"
#include "FinalStateAnalysis/DataAlgos/interface/PileupWeighting.h"
#include "FinalStateAnalysis/DataAlgos/interface/PileupWeighting3D.h"
#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"
#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"

#include "DataFormats/Math/interface/deltaR.h"

#define FSA_DATA_FORMAT_VERSION 3

namespace {
  int matchedToAnObject(const pat::TriggerObjectRefVector& trgObjects,
      const reco::Candidate& cand, double maxDeltaR) {
    bool matched = false;
    for (size_t i = 0; i < trgObjects.size(); ++i) {
      if (reco::deltaR(cand, *trgObjects.at(i)) < maxDeltaR) {
        matched = true;
        break;
      }
    }
    if (matched)
      return 1;
    else return 0;
  }
}

PATFinalStateEvent::PATFinalStateEvent() {}

// testing CTOR
PATFinalStateEvent::PATFinalStateEvent(
    const edm::Ptr<reco::Vertex>& pv,
    const edm::Ptr<pat::MET>& met):
  pv_(pv),
  met_(met) { }

PATFinalStateEvent::PATFinalStateEvent(
    double rho,
    const edm::Ptr<reco::Vertex>& pv,
    const edm::PtrVector<reco::Vertex>& recoVertices,
    const edm::Ptr<pat::MET>& met,
    const TMatrixD& metCovariance,
    const pat::TriggerEvent& triggerEvent,
    const std::vector<PileupSummaryInfo>& puInfo,
    const lhef::HEPEUP& hepeup,
    const reco::GenParticleRefProd& genParticles,
    const edm::EventID& evtId,
    const GenEventInfoProduct& genEventInfo,
    bool isRealData,
    const std::string& puScenario,
    const edm::RefProd<pat::ElectronCollection>& electronRefProd,
    const edm::RefProd<pat::MuonCollection>& muonRefProd,
    const edm::RefProd<pat::TauCollection>& tauRefProd,
    const edm::RefProd<pat::JetCollection>& jetRefProd,
    const edm::RefProd<pat::PhotonCollection>& phoRefProd,
    const reco::PFCandidateRefProd& pfRefProd,
    const reco::TrackRefProd& tracks,
    const reco::GsfTrackRefProd& gsfTracks,
    const std::map<std::string, edm::Ptr<pat::MET> >& mets
    ):
  rho_(rho),
  triggerEvent_(triggerEvent),
  pv_(pv),
  recoVertices_(recoVertices),
  met_(met),
  metCovariance_(metCovariance),
  puInfo_(puInfo),
  lhe_(hepeup),
  genParticles_(genParticles),
  evtID_(evtId),
  genEventInfoProduct_(genEventInfo),
  isRealData_(isRealData),
  puScenario_(puScenario),
  fsaDataFormatVersion_(FSA_DATA_FORMAT_VERSION),
  electronRefProd_(electronRefProd),
  muonRefProd_(muonRefProd),
  tauRefProd_(tauRefProd),
  jetRefProd_(jetRefProd),
  phoRefProd_(phoRefProd),
  pfRefProd_(pfRefProd),
  tracks_(tracks),
  gsfTracks_(gsfTracks),
  mets_(mets)
{ }

const edm::Ptr<reco::Vertex>& PATFinalStateEvent::pv() const { return pv_; }

const edm::PtrVector<reco::Vertex>& PATFinalStateEvent::recoVertices() const {
  return recoVertices_;
}

const std::vector<PileupSummaryInfo>& PATFinalStateEvent::puInfo() const {
  return puInfo_;
}

const lhef::HEPEUP& PATFinalStateEvent::lesHouches() const {
  return lhe_;
}

const GenEventInfoProduct& PATFinalStateEvent::genEventInfo() const {
  return genEventInfoProduct_;
}

double PATFinalStateEvent::rho() const { return rho_; }

const pat::TriggerEvent& PATFinalStateEvent::trig() const {
  return triggerEvent_; }

const edm::Ptr<pat::MET>& PATFinalStateEvent::met() const {
  return met_;
}

const TMatrixD& PATFinalStateEvent::metCovariance() const {
  return metCovariance_;
}

double PATFinalStateEvent::metSignificance() const {
  return fshelpers::xySignficance(met_->momentum(), metCovariance_);
}

const edm::Ptr<pat::MET> PATFinalStateEvent::met(
    const std::string& type) const {
  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit != mets_.end())
    return findit->second;
  return edm::Ptr<pat::MET>();
}

const reco::Candidate::LorentzVector PATFinalStateEvent::met4vector(
    const std::string& type, 
    const std::string& tag, 
    const int applyPhiCorr) const {
  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit == mets_.end())
    return reco::Candidate::LorentzVector();

  const reco::Candidate::LorentzVector& metp4 = (tag == "") ? met(type)->p4() : met(type)->userCand(tag)->p4();
  if (applyPhiCorr == 1)
    return fshelpers::metPhiCorrection(metp4, recoVertices_.size(), !isRealData_);

  return metp4;
}

const edm::EventID& PATFinalStateEvent::evtId() const {
  return evtID_;
}

// Superseded by the smart trigger
int PATFinalStateEvent::hltResult(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  return result.passed;
}

int PATFinalStateEvent::hltPrescale(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  return result.prescale;
}

int PATFinalStateEvent::hltGroup(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  return result.group;
}

int PATFinalStateEvent::matchedToFilter(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  std::vector<const pat::TriggerFilter*> filters =
    matchingTriggerFilters(trig(), pattern);
  if (!filters.size())
    return -1;
  return matchedToAnObject(
      triggerEvent_.filterObjects(filters[0]->label()), cand, maxDeltaR);
}

int PATFinalStateEvent::matchedToPath(const reco::Candidate& cand,
    const std::string& pattern, double maxDeltaR) const {
  // std::cout << "matcher: " << pattern << std::endl;
  SmartTriggerResult result = smartTrigger(pattern, trig(), evtID_);
  // std::cout << " result: " << result.group << " " << result.prescale << " " << result.passed << std::endl;
  // Loop over all the paths that fired and see if any matched this object.
  if (!result.passed)
    return -1;
  int matchCount = 0;
  for (size_t i = 0; i < result.paths.size(); ++i) {
    bool matched = matchedToAnObject(
      triggerEvent_.pathObjects(result.paths[i]), cand, maxDeltaR);
    // std::cout << " - path: " << result.paths[i] << " matched: " << matched << std::endl;
    if (matched)
      matchCount += 1;
  }
  return matchCount;
}

const std::string& PATFinalStateEvent::puTag() const {
  return puScenario_;
}

double PATFinalStateEvent::puWeight(const std::string& dataTag) const {
  if (isRealData_)
    return 1.;
  return this->puWeight(dataTag, puTag());
}

double PATFinalStateEvent::puWeight(const std::string& dataTag,
    const std::string& mcTag) const {
  if (isRealData_)
    return 1.;
  return getPileupWeight(dataTag, mcTag, puInfo_[1].getTrueNumInteractions());
}

double PATFinalStateEvent::puWeight3D(const std::string& dataTag) const {
  if (isRealData_)
    return 1.;
  return this->puWeight3D(dataTag, puTag());
}

double PATFinalStateEvent::puWeight3D(const std::string& dataTag,
    const std::string& mcTag) const {
  if (isRealData_)
    return 1.;
  return get3DPileupWeight(dataTag, mcTag, puInfo_);
}


float PATFinalStateEvent::weight(const std::string& name) const {
  typedef std::map<std::string, float> WeightMap;
  WeightMap::const_iterator findit = weights_.find(name);
  if (findit != weights_.end())
    return findit->second;
  else
    return -999;
}
void PATFinalStateEvent::addWeight(const std::string& name, float weight) {
  weights_[name] = weight;
}

int PATFinalStateEvent::flag(const std::string& name) const {
  typedef std::map<std::string, int> FlagMap;
  FlagMap::const_iterator findit = flags_.find(name);
  if (findit != flags_.end())
    return findit->second;
  else
    return -999;
}
void PATFinalStateEvent::addFlag(const std::string& name, int flag) {
  flags_[name] = flag;
}

const pat::ElectronCollection& PATFinalStateEvent::electrons() const {
  if (!electronRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The electron RefProd is null!" << std::endl;
  return *electronRefProd_;
}

const pat::MuonCollection& PATFinalStateEvent::muons() const {
  if (!muonRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The muon RefProd is null!" << std::endl;
  return *muonRefProd_;
}

const pat::TauCollection& PATFinalStateEvent::taus() const {
  if (!tauRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The tau RefProd is null!" << std::endl;
  return *tauRefProd_;
}

const pat::JetCollection& PATFinalStateEvent::jets() const {
  if (!jetRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The jet RefProd is null!" << std::endl;
  return *jetRefProd_;
}

const pat::PhotonCollection& PATFinalStateEvent::photons() const {
  if (!phoRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The photon RefProd is null!" << std::endl;
  return *phoRefProd_;
}

const reco::PFCandidateCollection& PATFinalStateEvent::pflow() const {
  if (!pfRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The PFLOW RefProd is null!" << std::endl;
  return *pfRefProd_;
}

const bool PATFinalStateEvent::findDecay(const int pdgIdMother, const int pdgIdDaughter) const{
  return fshelpers::findDecay(genParticles_, pdgIdMother, pdgIdDaughter);
}
float  PATFinalStateEvent::variables(const reco::Candidate&  jet, const std::string& myvar)const{
  std::map <std::string, float> varMap_; 
  varMap_["eta"] = jet.eta();
  Bool_t useQC = true;
  // if(fabs(jet->eta()) > 2.5 && type == "MLP") useQC = false;		//In MLP: no QC in forward region

 edm::PtrVector<reco::Vertex>::const_iterator  vtxLead = recoVertices_.begin();

  Float_t sum_weight = 0., sum_deta = 0., sum_dphi = 0., sum_deta2 = 0., sum_dphi2 = 0., sum_detadphi = 0., sum_pt = 0.;
  Int_t nChg_QC = 0, nChg_ptCut = 0, nNeutral_ptCut = 0;

  //Loop over the jet constituents
  const pat::Jet *myjet = 0;
  for (pat::JetCollection::const_iterator patjet=jetRefProd_->begin(); patjet!=jetRefProd_->end(); ++patjet){
    if (patjet->pt() == jet.pt() &&patjet->phi() == jet.phi() &&patjet->eta() == jet.eta() ) 
      myjet = &*patjet;
  }
  if (myjet!=0){
    std::vector<reco::PFCandidatePtr> constituents = myjet->getPFConstituents();
    for(unsigned i = 0; i < constituents.size(); ++i){
      reco::PFCandidatePtr part = myjet->getPFConstituent(i);      
      if(!part.isNonnull()) continue;
      
      reco::TrackRef itrk = part->trackRef();;
      
      bool trkForAxis = false;
      if(itrk.isNonnull()){						//Track exists --> charged particle
	if(part->pt() > 1.0) nChg_ptCut++;
	
	//Search for closest vertex to track
	edm::PtrVector<reco::Vertex>::const_iterator  vtxClose = recoVertices_.begin();
	for( edm::PtrVector<reco::Vertex>::const_iterator  vtx = recoVertices_.begin(); vtx != recoVertices_.end(); ++vtx){
	  if(fabs(itrk->dz((*vtx)->position())) < fabs(itrk->dz((*vtxClose)->position()))) vtxClose = vtx;
	}
	
	if(vtxClose == vtxLead){
        Float_t dz = itrk->dz((*vtxClose)->position());
        Float_t dz_sigma = sqrt(pow(itrk->dzError(),2) + pow((*vtxClose)->zError(),2));
	
        if(itrk->quality(reco::TrackBase::qualityByName("highPurity")) && fabs(dz/dz_sigma) < 5.){
          trkForAxis = true;
          Float_t d0 = itrk->dxy((*vtxClose)->position());
          Float_t d0_sigma = sqrt(pow(itrk->d0Error(),2) + pow((*vtxClose)->xError(),2) + pow((*vtxClose)->yError(),2));
          if(fabs(d0/d0_sigma) < 5.) nChg_QC++;
        }
	}
      } else {								//No track --> neutral particle
	if(part->pt() > 1.0) nNeutral_ptCut++;
	trkForAxis = true;
      }
      
      Float_t deta = part->eta() - jet.eta();
      Float_t dphi = 2*atan(tan(((part->phi()- jet.phi()))/2));           
      Float_t partPt = part->pt(); 
      Float_t weight = partPt*partPt;

      if(!useQC || trkForAxis){					//If quality cuts, only use when trkForAxis
	sum_weight += weight;
	sum_pt += partPt;
	sum_deta += deta*weight;                  
	sum_dphi += dphi*weight;                                                                                             
	sum_deta2 += deta*deta*weight;                    
	sum_detadphi += deta*dphi*weight;                               
	sum_dphi2 += dphi*dphi*weight;
      }	
    }
  }
  //Calculate axis and ptD
  Float_t a = 0., b = 0., c = 0.;
  Float_t ave_deta = 0., ave_dphi = 0., ave_deta2 = 0., ave_dphi2 = 0.;
  if(sum_weight > 0){
    varMap_["ptD"] = sqrt(sum_weight)/sum_pt;
    ave_deta = sum_deta/sum_weight;
    ave_dphi = sum_dphi/sum_weight;
    ave_deta2 = sum_deta2/sum_weight;
    ave_dphi2 = sum_dphi2/sum_weight;
    a = ave_deta2 - ave_deta*ave_deta;                          
    b = ave_dphi2 - ave_dphi*ave_dphi;                          
    c = -(sum_detadphi/sum_weight - ave_deta*ave_dphi);                
  } else varMap_["ptD"] = 0;
  Float_t delta = sqrt(fabs((a-b)*(a-b)+4*c*c));
  if(a+b+delta > 0) varMap_["axis1"] = sqrt(0.5*(a+b+delta));
  else varMap_["axis1"] = 0.;
  if(a+b-delta > 0) varMap_["axis2"] = sqrt(0.5*(a+b-delta));
  else varMap_["axis2"] = 0.;
  
  // if(type == "MLP" && useQC) variables["mult"] = nChg_QC;
  // else if(type == "MLP") variables["mult"] = (nChg_ptCut + nNeutral_ptCut);
  // else variables["mult"] = (nChg_QC + nNeutral_ptCut);
  varMap_["mult"] = (nChg_QC + nNeutral_ptCut);
  varMap_["mult_MLP_QC"] = (nChg_QC );
  varMap_["mult_MLP"] = (nChg_ptCut + nNeutral_ptCut );
  float myVarValue =-1;
  for (std::map<std::string, float>::const_iterator it = varMap_.begin(); it != varMap_.end(); ++it){
    if (myvar == it->first)
      myVarValue= it->second; 
  }
  return myVarValue;
}

