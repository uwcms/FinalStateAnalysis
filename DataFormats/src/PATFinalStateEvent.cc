#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataAlgos/interface/SmartTrigger.h"
#include "FinalStateAnalysis/DataAlgos/interface/PileupWeighting.h"
#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"
#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"

#include "DataFormats/Math/interface/deltaR.h"
//#include "FWCore/Framework/interface/Event.h"

#define FSA_DATA_FORMAT_VERSION 3
#define DEBUG_ 0

namespace {
  int matchedToAnObject(const std::vector<pat::TriggerObjectStandAlone> trgObjects, const edm::TriggerNames names,
      const reco::Candidate& cand, double maxDeltaR, std::string trigName="") {
    bool matched = false;
    for (size_t i = 0; i < trgObjects.size(); ++i) {
      pat::TriggerObjectStandAlone obj = trgObjects.at(i);
      if (reco::deltaR(cand, obj) > maxDeltaR) continue;
      obj.unpackPathNames(names);
      std::vector<std::string> pathNames = obj.pathNames(true); //Cecile
      for (size_t t = 0; t < pathNames.size(); t++) {
          std::string path = pathNames.at(t);
          if(DEBUG_)std::cout << " - - - path name: " << path << " match name " << trigName << std::endl;
          if ((path.substr(0, path.find_last_of("_v"))).compare(trigName.substr(0, trigName.find_last_of("_v")))==0) {
            matched = true;
           return 1;
          }
      }

      // Commenting it as it is not working in CMSSW_9_3_X
      // // Current filter matching relies only on checking for a trigger object
      // // within the desired cone size that contains the desired trigger filter.
      // // There is no requirement place on the HLT object to match pdgID type
      // // with the candidate. If this matching is desired, uncomment, and double
      // // check the below code.
      // std::vector<std::string> filterLabels;
      // obj.unpackFilterLabels(filterLabels);

      // for (size_t i = 0; i < filterLabels.size(); i++) {
      // 	std::string filter = filterLabels.at(i);
      //     if (filter.compare(trigName)==0) {
      //       //std::cout << " - - - filter name: " << filter << " match name " << trigName << std::endl;
      //       //std::cout << "Checking obj with pdgID = " << cand.pdgId() << std::endl;
      //       //std::cout << "Trig Obj pdgId: " << obj.pdgId() << std::endl;
      //       //std::cout << "Trig Obj Type: " << obj.filterIds() << std::endl;
      //       //for (size_t j = 0; j < obj.filterIds().size(); j++) {
      //       //  std::cout << " -- filter ID " << obj.filterIds().at(j) << std::endl;
      //       //  // Match the Candidate PDG ID to the Trigger Object ID: see DataFormats/HLTReco/interface/TriggerTypeDefs.h
      //       //  // Currently many miniAOD files are missing HLT Electron Trigger objects from above .h file.
      //       //  if ( abs( obj.pdgId() ) == 11 && abs( obj.pdgId() ) == 11 ) {
      //       //    std::cout << "  ------ XXX Matching electron!" << std::endl;
      //       //    matched = true;
      //       //    return 1;
      //       //  }
      //       //  if ( abs( obj.pdgId() ) == 13 && abs( obj.pdgId() ) == 13 ) {
      //       //    std::cout << "  ------ XXX Matching muon!" << std::endl;
      //       //    matched = true;
      //       //    return 1;
      //       //  }
      //       //  if ( abs( obj.pdgId() ) == 15 && abs( obj.pdgId() ) == 15 ) {
      //       //    std::cout << "  ------ XXX Matching tau!" << std::endl;
      //       //    matched = true;
      //       //    return 1;
      //       //  }
      //       //}
      //       matched = true;
      //       return 1;
      //     }
      // }
    }
    if (matched)
      return 1;
    else return 0;
  }
}

void unpackTrigger(std::vector<pat::TriggerObjectStandAlone> trig, const edm::TriggerNames& names) {
  for (pat::TriggerObjectStandAlone obj : trig) {
    obj.unpackPathNames(names);
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
    const std::vector<edm::Ptr<reco::Vertex>>& recoVertices,
    const edm::Ptr<pat::MET>& met,
    const TMatrixD& metCovariance,
    const std::vector<pat::MET> MVAMETs,
    const double metSig,
    const math::Error<2>::type metCov,
    const pat::TriggerEvent triggerEvent,
    const edm::RefProd<std::vector<pat::TriggerObjectStandAlone>>& triggerObjects,
    const edm::TriggerNames& names,
    const pat::PackedTriggerPrescales& triggerPrescale,
    const edm::TriggerResults& triggerResults,
    const BXVector<l1t::Tau>& l1extraIsoTaus,
    const std::vector<PileupSummaryInfo>& puInfo,
    const lhef::HEPEUP& hepeup,
    const reco::GenParticleRefProd& genParticles,
    const std::vector<reco::GenJet> genHadronicTaus,
    const std::vector<reco::GenJet> genElectronicTaus,
    const std::vector<reco::GenJet> genMuonicTaus,
    const HTXS::HiggsClassification htxsRivetInfo,
    const edm::EventID& evtId,
    //const edm::Event& evt,
    const GenEventInfoProduct& genEventInfo,
    const GenFilterInfo& generatorFilter,
    bool isRealData,
    bool isEmbeddedSample,
    const std::string& puScenario,
    const edm::RefProd<pat::ElectronCollection>& electronRefProd,
    const edm::RefProd<pat::MuonCollection>& muonRefProd,
    const edm::RefProd<pat::TauCollection>& tauRefProd,
    const edm::RefProd<pat::JetCollection>& jetRefProd,
    const edm::RefProd<pat::PhotonCollection>& phoRefProd,
    const reco::PFCandidateRefProd& pfRefProd,
    const edm::RefProd<pat::PackedCandidateCollection>& packedPFRefProd,
    const reco::TrackRefProd& tracks,
    const reco::GsfTrackRefProd& gsfTracks,
    const std::map<std::string, edm::Ptr<pat::MET> >& mets,
    std::vector<float> lheweights,
    int npNLO,
    std::map<std::string, bool> filterFlagsMap
    ):
  rho_(rho),
  triggerEvent_(triggerEvent),
  triggerObjects_(triggerObjects),
  names_(names),
  triggerPrescale_(triggerPrescale),
  triggerResults_(triggerResults),
  l1extraIsoTaus_(l1extraIsoTaus),
  pv_(pv),
  recoVertices_(recoVertices),
  met_(met),
  metCovariance_(metCovariance),
  MVAMETs_(MVAMETs),
  metSig_(metSig),
  metCov_(metCov),
  puInfo_(puInfo),
  lhe_(hepeup),
  genParticles_(genParticles),
  genHadronicTaus_(genHadronicTaus),
  genElectronicTaus_(genElectronicTaus),
  genMuonicTaus_(genMuonicTaus),
  htxsRivetInfo_(htxsRivetInfo),
  evtID_(evtId),
  //evt_(evt),
  genEventInfoProduct_(genEventInfo),
  generatorFilter_(generatorFilter),
  isRealData_(isRealData),
  isEmbeddedSample_(isEmbeddedSample),
  puScenario_(puScenario),
  fsaDataFormatVersion_(FSA_DATA_FORMAT_VERSION),
  electronRefProd_(electronRefProd),
  muonRefProd_(muonRefProd),
  tauRefProd_(tauRefProd),
  jetRefProd_(jetRefProd),
  phoRefProd_(phoRefProd),
  pfRefProd_(pfRefProd),
  packedPFRefProd_(packedPFRefProd),
  tracks_(tracks),
  gsfTracks_(gsfTracks),
  mets_(mets),
  lheweights_(lheweights),
  npNLO_(npNLO),
  filterFlagsMap_(filterFlagsMap)
{ }

const edm::Ptr<reco::Vertex>& PATFinalStateEvent::pv() const { return pv_; }

const std::vector<edm::Ptr<reco::Vertex>>& PATFinalStateEvent::recoVertices() const {
  return recoVertices_;
}

int PATFinalStateEvent::numberVertices() const {
  return recoVertices().size();
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

const GenFilterInfo& PATFinalStateEvent::generatorFilter() const {
  return generatorFilter_;
}

double PATFinalStateEvent::rho() const { return rho_; }

std::vector<float> PATFinalStateEvent::lheweights() const {
  if (lheweights_.size() == 0) {
    std::vector<float> rtn;
    for (int i = 0; i < 200; i++) {
      rtn.push_back( 0. );
    }
    return rtn;
  }
  return lheweights_;}

int  PATFinalStateEvent::npNLO() const{
   return npNLO_;
}

const pat::TriggerEvent& PATFinalStateEvent::trig() const {
  return triggerEvent_; }

const std::vector<pat::TriggerObjectStandAlone>& PATFinalStateEvent::trigStandAlone() const {
   return *triggerObjects_; }

const edm::TriggerNames& PATFinalStateEvent::names() const {
  return names_; }

const pat::PackedTriggerPrescales& PATFinalStateEvent::trigPrescale() const {
  return triggerPrescale_; }

const edm::TriggerResults& PATFinalStateEvent::trigResults() const {
  return triggerResults_; }

const BXVector<l1t::Tau>& PATFinalStateEvent::l1extraIsoTaus() const {
  return l1extraIsoTaus_; }

const edm::Ptr<pat::MET>& PATFinalStateEvent::met() const {
  return met_;
}

const std::vector<pat::MET> PATFinalStateEvent::MVAMETs() const {
  //std::cout << "newMvaMets, len: " << MVAMETs_.size() <<std::endl;
  return MVAMETs_;
}

const double PATFinalStateEvent::metSig() const {
  return metSig_;
}

const double PATFinalStateEvent::metCov(size_t i) const {
  if (i == 0) return metCov_(0,0);
  if (i == 1) return metCov_(1,0);
  if (i == 2) return metCov_(1,0); // (0,1) not filled, use (1,0)
  if (i == 3) return metCov_(1,1);
  return -999;
}

const edm::Ptr<pat::MET> PATFinalStateEvent::met(
    const std::string& type) const 
{
  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit != mets_.end() && findit->second.isNonnull())
    return findit->second;
  return edm::Ptr<pat::MET>();
}

const TMatrixD& PATFinalStateEvent::metCovariance() const {
  return metCovariance_;
}

double PATFinalStateEvent::metSignificance() const {
  return fshelpers::xySignficance(met_->momentum(), metCovariance_);
}

const reco::Candidate::LorentzVector PATFinalStateEvent::met4vector(
								    const std::string& type, 
								    const std::string& metTag, 
								    const int applyPhiCorr) const 
{

  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit == mets_.end() || findit->second.isNull())
    return reco::Candidate::LorentzVector();

  reco::Candidate::LorentzVector metP4;

  if(type=="mvamet"){  
     metP4=met(type)->p4();
  } 
  else if ( met(type)->hasUserCand(metTag) ){ 
       metP4=met(type)->userCand(metTag)->p4();
  }
  else{
      if(metTag == "jres+")
        metP4 = met(type)->shiftedP4(pat::MET::JetResUp);
      else if(metTag == "jres-")
        metP4 = met(type)->shiftedP4(pat::MET::JetResDown);
      else if(metTag == "jes+")
        metP4 = met(type)->shiftedP4(pat::MET::JetEnUp);
      else if(metTag == "jes-")
        metP4 = met(type)->shiftedP4(pat::MET::JetEnDown);
      else if(metTag == "mes+")
        metP4 = met(type)->shiftedP4(pat::MET::MuonEnUp);
      else if(metTag == "mes-")
        metP4 = met(type)->shiftedP4(pat::MET::MuonEnDown);
      else if(metTag == "ees+")
        metP4 = met(type)->shiftedP4(pat::MET::ElectronEnUp);
      else if(metTag == "ees-")
        metP4 = met(type)->shiftedP4(pat::MET::ElectronEnDown);
      else if(metTag == "tes+")
        metP4 = met(type)->shiftedP4(pat::MET::TauEnUp);
      else if(metTag == "tes-")
        metP4 = met(type)->shiftedP4(pat::MET::TauEnDown);
      else if(metTag == "ues+")
        metP4 = met(type)->shiftedP4(pat::MET::UnclusteredEnUp);
      else if(metTag == "ues-")
        metP4 = met(type)->shiftedP4(pat::MET::UnclusteredEnDown);
      else if(metTag == "pes+")
        metP4 = met(type)->shiftedP4(pat::MET::PhotonEnUp);
      else if(metTag == "pes-")
        metP4 = met(type)->shiftedP4(pat::MET::PhotonEnDown);
      else if(metTag == "raw")
        metP4 = met(type)->uncorP4();
      else
        metP4 = met(type)->p4();
  } 

  return metP4;
  // TODO
  //if (applyPhiCorr == 1)
  //  return fshelpers::metPhiCorrection(metp4, recoVertices_.size(), !isRealData_);
}

double PATFinalStateEvent::metShift(const std::string& type, const std::string& var, const std::string& tag) const
{

  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit == mets_.end() || findit->second.isNull())   
        return 0.0;
  
  if (var=="pt") {
        return met4vector(type,tag).pt();
  }
  else if (var=="phi") {
        return met4vector(type,tag).phi();
  }
  else return 0;

/*
  std::map<std::string, edm::Ptr<pat::MET> >::const_iterator findit =
    mets_.find(type);
  if (findit == mets_.end() || findit->second.isNull())
    return 0.0;
  if (var=="pt") {
    if(tag == "jres+"){
      if(met(type)->hasUserCand("jresUpMET")) {
        //std::cout << "jresUp - precomputed: " << met(type)->shiftedPt(pat::MET::JetResUp) << ", mettools: " << met(type)->userCand("jresUpMET")->pt() << std::endl;
        return met(type)->userCand("jresUpMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::JetResUp);
    }
    else if(tag == "jres-"){
      if(met(type)->hasUserCand("jresUpMET")) {
        //std::cout << "jresDown - precomputed: " << met(type)->shiftedPt(pat::MET::JetResDown) << ", mettools: " << met(type)->userCand("jresDownMET")->pt() << std::endl;
        return met(type)->userCand("jresUpMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::JetResDown);
    }
    else if(tag == "jes+"){
      if(met(type)->hasUserCand("jesUpMET")) {
        //std::cout << "jesUp - precomputed: " << met(type)->shiftedPt(pat::MET::JetEnUp) << ", mettools: " << met(type)->userCand("jesUpMET")->pt() << std::endl;
        return met(type)->userCand("jesUpMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::JetEnUp);
    }
    else if(tag == "jes-"){
      if(met(type)->hasUserCand("jesDownMET")) {
        //std::cout << "jesDown - precomputed: " << met(type)->shiftedPt(pat::MET::JetEnDown) << ", mettools: " << met(type)->userCand("jesDownMET")->pt() << std::endl;
        return met(type)->userCand("jesDownMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::JetEnDown);
    }
    else if(tag == "mes+"){
      if(met(type)->hasUserCand("mesUpMET")) {
        //std::cout << "mesUp - precomputed: " << met(type)->shiftedPt(pat::MET::MuonEnUp) << ", mettools: " << met(type)->userCand("mesUpMET")->pt() << std::endl;
        return met(type)->userCand("mesUpMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::MuonEnUp);
    }
    else if(tag == "mes-"){
      if(met(type)->hasUserCand("mesDownMET")) {
        //std::cout << "mesDown - precomputed: " << met(type)->shiftedPt(pat::MET::MuonEnDown) << ", mettools: " << met(type)->userCand("mesDownMET")->pt() << std::endl;
        return met(type)->userCand("mesDownMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::MuonEnDown);
    }
    else if(tag == "ees+"){
      if(met(type)->hasUserCand("eesUpMET")) {
        //std::cout << "eesUp - precomputed: " << met(type)->shiftedPt(pat::MET::ElectronEnUp) << ", mettools: " << met(type)->userCand("eesUpMET")->pt() << std::endl;
        return met(type)->userCand("eesUpMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::ElectronEnUp);
    }
    else if(tag == "ees-"){
      if(met(type)->hasUserCand("eesDownMET")) {
        //std::cout << "eesDown - precomputed: " << met(type)->shiftedPt(pat::MET::ElectronEnDown) << ", mettools: " << met(type)->userCand("eesDownMET")->pt() << std::endl;
        return met(type)->userCand("eesDownMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::ElectronEnDown);
    }
    else if(tag == "tes+"){
      if(met(type)->hasUserCand("tesUpMET")) {
        //std::cout << "tesUp - precomputed: " << met(type)->shiftedPt(pat::MET::TauEnUp) << ", mettools: " << met(type)->userCand("tesUpMET")->pt() << std::endl;
        return met(type)->userCand("tesUpMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::TauEnUp);
    }
    else if(tag == "tes-"){
      if(met(type)->hasUserCand("tesDownMET")) {
        //std::cout << "tesDown - precomputed: " << met(type)->shiftedPt(pat::MET::TauEnDown) << ", mettools: " << met(type)->userCand("tesDownMET")->pt() << std::endl;
        return met(type)->userCand("tesDownMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::TauEnDown);
    }
    else if(tag == "ues+"){
      if(met(type)->hasUserCand("uesUpMET")) {
        //std::cout << "uesUp - precomputed: " << met(type)->shiftedPt(pat::MET::UnclusteredEnUp) << ", mettools: " << met(type)->userCand("uesUpMET")->pt() << std::endl;
        return met(type)->userCand("uesUpMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::UnclusteredEnUp);
    }
    else if(tag == "ues-"){
      if(met(type)->hasUserCand("uesDownMET")) {
        //std::cout << "uesDown - precomputed: " << met(type)->shiftedPt(pat::MET::UnclusteredEnDown) << ", mettools: " << met(type)->userCand("uesDownMET")->pt() << std::endl;
        return met(type)->userCand("uesDownMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::UnclusteredEnDown);
    }
    else if(tag == "pes+"){
      if(met(type)->hasUserCand("pesUpMET")) {
        //std::cout << "pesUp - precomputed: " << met(type)->shiftedPt(pat::MET::PhotonEnUp) << ", mettools: " << met(type)->userCand("pesUpMET")->pt() << std::endl;
        return met(type)->userCand("pesUpMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::PhotonEnUp);
    }
    else if(tag == "pes-"){
      if(met(type)->hasUserCand("pesDownMET")) {
        //std::cout << "pesDown - precomputed: " << met(type)->shiftedPt(pat::MET::PhotonEnDown) << ", mettools: " << met(type)->userCand("pesDownMET")->pt() << std::endl;
        return met(type)->userCand("pesDownMET")->pt();
      }
      return met(type)->shiftedPt(pat::MET::PhotonEnDown);
    }
    else{
      return met(type)->pt();
    }
  }
  else if (var=="phi") {
    if(tag == "jres+"){
      if(met(type)->hasUserCand("jresUpMET"))
        return met(type)->userCand("jresUpMET")->phi();
      return met(type)->shiftedPhi(pat::MET::JetResUp);
    }
    else if(tag == "jres-"){
      if(met(type)->hasUserCand("jresUpMET"))
        return met(type)->userCand("jresUpMET")->phi();
      return met(type)->shiftedPhi(pat::MET::JetResDown);
    }
    else if(tag == "jes+"){
      if(met(type)->hasUserCand("jesUpMET"))
        return met(type)->userCand("jesUpMET")->phi();
      return met(type)->shiftedPhi(pat::MET::JetEnUp);
    }
    else if(tag == "jes-"){
      if(met(type)->hasUserCand("jesDownMET"))
        return met(type)->userCand("jesDownMET")->phi();
      return met(type)->shiftedPhi(pat::MET::JetEnDown);
    }
    else if(tag == "mes+"){
      if(met(type)->hasUserCand("mesUpMET"))
        return met(type)->userCand("mesUpMET")->phi();
      return met(type)->shiftedPhi(pat::MET::MuonEnUp);
    }
    else if(tag == "mes-"){
      if(met(type)->hasUserCand("mesDownMET"))
        return met(type)->userCand("mesDownMET")->phi();
      return met(type)->shiftedPhi(pat::MET::MuonEnDown);
    }
    else if(tag == "ees+"){
      if(met(type)->hasUserCand("eesUpMET"))
        return met(type)->userCand("eesUpMET")->phi();
      return met(type)->shiftedPhi(pat::MET::ElectronEnUp);
    }
    else if(tag == "ees-"){
      if(met(type)->hasUserCand("eesDownMET"))
        return met(type)->userCand("eesDownMET")->phi();
      return met(type)->shiftedPhi(pat::MET::ElectronEnDown);
    }
    else if(tag == "tes+"){
      if(met(type)->hasUserCand("tesUpMET"))
        return met(type)->userCand("tesUpMET")->phi();
      return met(type)->shiftedPhi(pat::MET::TauEnUp);
    }
    else if(tag == "tes-"){
      if(met(type)->hasUserCand("tesDownMET"))
        return met(type)->userCand("tesDownMET")->phi();
      return met(type)->shiftedPhi(pat::MET::TauEnDown);
    }
    else if(tag == "ues+"){
      if(met(type)->hasUserCand("uesUpMET"))
        return met(type)->userCand("uesUpMET")->phi();
      return met(type)->shiftedPhi(pat::MET::UnclusteredEnUp);
    }
    else if(tag == "ues-"){
      if(met(type)->hasUserCand("uesDownMET"))
        return met(type)->userCand("uesDownMET")->phi();
      return met(type)->shiftedPhi(pat::MET::UnclusteredEnDown);
    }
    else if(tag == "pes+"){
      if(met(type)->hasUserCand("pesUpMET"))
        return met(type)->userCand("pesUpMET")->phi();
      return met(type)->shiftedPhi(pat::MET::PhotonEnUp);
    }
    else if(tag == "pes-"){
      if(met(type)->hasUserCand("pesDownMET"))
        return met(type)->userCand("pesDownMET")->phi();
      return met(type)->shiftedPhi(pat::MET::PhotonEnDown);
    }
    else{
      return met(type)->phi();
    }
  }
  else
    return 0.;
  */
 
}

const edm::EventID& PATFinalStateEvent::evtId() const {
  return evtID_;
}

double PATFinalStateEvent::eventDouble() const {
  ULong64_t eventNum = evtId().event();
  double doub = 0.;
  return doub + eventNum;
}

// Superseded by the smart trigger
int PATFinalStateEvent::hltResult(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, names(), trigPrescale(), trigResults(), evtID_);
  return result.passed;
}

int PATFinalStateEvent::hltPrescale(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, names(), trigPrescale(), trigResults(), evtID_);
  return result.prescale;
}

int PATFinalStateEvent::hltGroup(const std::string& pattern) const {
  SmartTriggerResult result = smartTrigger(pattern, names(), trigPrescale(), trigResults(), evtID_);
  return result.group;
}

int PATFinalStateEvent::matchedToPath(const reco::Candidate& cand,const std::string& pattern, double maxDeltaR) const {
   int match=0;
   for (size_t i = 0; i < trigStandAlone().size(); ++i) {
      pat::TriggerObjectStandAlone obj = trigStandAlone().at(i);
      if (reco::deltaR(cand, obj) > maxDeltaR) continue;
      obj.unpackPathNames(names());
      std::vector<std::string> pathNamesLast = obj.pathNames(false); 
      for (unsigned h = 0, n = pathNamesLast.size(); h < n; ++h) {
	if ((pathNamesLast[h].substr(0, pathNamesLast[h].find_last_of("_v"))).compare(pattern.substr(0, pattern.find_last_of("_v")))==0) {
	       match++;
	}
      }
   }
   return match;
}

int PATFinalStateEvent::matchedToFilter(const reco::Candidate& cand,const std::string& pattern, double maxDeltaR) const {
   int match=0;
   for (size_t i = 0; i < trigStandAlone().size(); ++i) {
      pat::TriggerObjectStandAlone obj = trigStandAlone().at(i);
      if (reco::deltaR(cand, obj) > maxDeltaR) continue;
      obj.unpackPathNames(names());
      std::vector<std::string> pathNamesLast = obj.pathNames(true); 
      for (unsigned h = 0, n = pathNamesLast.size(); h < n; ++h) {
        if ((pathNamesLast[h].substr(0, pathNamesLast[h].find_last_of("_v"))).compare(pattern.substr(0, pattern.find_last_of("_v")))==0) {
           if (obj.hasPathName( pathNamesLast[h], true, true )) 
               match++;
        }
      }
   }
   return match;
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

const pat::PackedCandidateCollection& PATFinalStateEvent::packedPflow() const {
  if (!packedPFRefProd_)
    throw cms::Exception("PATFSAEventNullRefs")
      << "The Packed PFLOW RefProd is null!" << std::endl;
  return *packedPFRefProd_;
}

const bool PATFinalStateEvent::findDecay(const int pdgIdMother, const int pdgIdDaughter) const{
  return fshelpers::findDecay(genParticles_, pdgIdMother, pdgIdDaughter);
}

float PATFinalStateEvent::getGenMass() const{
  if(isRealData_) return -1;
  return fshelpers::genMass(lhe_);
}

float PATFinalStateEvent::genHTT() const{
  if(isRealData_) return -1;
  return fshelpers::genHTT(lhe_);
}

float PATFinalStateEvent::numGenJets() const{
  if(isRealData_) return -1;
  return fshelpers::numGenJets(lhe_);
}

float  PATFinalStateEvent::jetVariables(const reco::CandidatePtr jet, const std::string& myvar) const{
  return fshelpers::jetQGVariables( jet, myvar, recoVertices_);
}

const int PATFinalStateEvent::getFilterFlags( std::string filter ) const{
  if (filterFlagsMap_.find( filter ) != filterFlagsMap_.end())
    return filterFlagsMap_.at( filter );
  else return 0;
}



