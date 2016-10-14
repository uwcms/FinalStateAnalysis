#include "FinalStateAnalysis/DataAlgos/interface/VBFSelections.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

VBFVariables computeVBFInfo(
    const std::vector<const reco::Candidate*>& hardScatter,
    const reco::Candidate::LorentzVector& metp4,
    const std::vector<const reco::Candidate*>& jets) {
  VBFVariables output;

  // number of initial jets
  output.nJets = jets.size();

  // Not enough jets
  if (output.nJets < 2)
    return output;

  //assert(jets[0]->pt() > jets[1]->pt());

  if( jets[0]->pt() > jets[1]->pt() ) {
    output.leadJet = jets[0];
    output.subleadJet = jets[1];
  } else {
    output.leadJet = jets[1];
    output.subleadJet = jets[0];
  } 

  // Get 4vectors of two highest jets
  reco::Candidate::LorentzVector leadJet(output.leadJet->p4());
  reco::Candidate::LorentzVector subleadJet(output.subleadJet->p4());

  const pat::Jet * jet1Pat = dynamic_cast<const pat::Jet*> (jets[0]);
  const pat::Jet * jet2Pat = dynamic_cast<const pat::Jet*> (jets[1]);

  reco::Candidate::LorentzVector leadJet_JESDown(jet1Pat->userCand("jes-")->p4());
  reco::Candidate::LorentzVector leadJet_JESUp(jet1Pat->userCand("jes+")->p4());
  reco::Candidate::LorentzVector subleadJet_JESDown(jet2Pat->userCand("jes-")->p4());
  reco::Candidate::LorentzVector subleadJet_JESUp(jet2Pat->userCand("jes+")->p4());

  reco::Candidate::LorentzVector dijet = leadJet + subleadJet;
  reco::Candidate::LorentzVector dijet_JESDown = leadJet_JESDown + subleadJet_JESDown;
  reco::Candidate::LorentzVector dijet_JESUp = leadJet_JESUp + subleadJet_JESUp;

  reco::Candidate::LorentzVector ditauvis;
  for (size_t i = 0; i < hardScatter.size(); ++i) {
    ditauvis += hardScatter[i]->p4();
  }

  // ditau = hard scatter + MET
  reco::Candidate::LorentzVector ditau = metp4 + ditauvis;

  output.mass = dijet.mass();
  output.deta = std::abs(leadJet.eta() - subleadJet.eta());
  output.dphi = std::abs(reco::deltaPhi(leadJet.phi(), subleadJet.phi()));
  output.pt1 = leadJet.pt();
  output.pt2 = subleadJet.pt();
  output.dijetpt = dijet.pt();
  output.ditaupt = ditau.pt();
  output.hrapidity = ditauvis.Rapidity();
  output.dijetrapidity = dijet.Rapidity();
  output.eta1 = leadJet.eta();
  output.eta2 = subleadJet.eta();

  output.mass_JESDown = dijet_JESDown.mass();
  output.deta_JESDown = std::abs(leadJet_JESDown.eta() - subleadJet_JESDown.eta());
  output.dphi_JESDown = std::abs(reco::deltaPhi(leadJet_JESDown.phi(), subleadJet_JESDown.phi()));
  output.pt1_JESDown = leadJet_JESDown.pt();
  output.pt2_JESDown = subleadJet_JESDown.pt();
  output.dijetpt_JESDown = dijet_JESDown.pt();
  output.dijetrapidity_JESDown = dijet_JESDown.Rapidity();
  output.eta1_JESDown = leadJet_JESDown.eta();
  output.eta2_JESDown = subleadJet_JESDown.eta();

  output.mass_JESUp = dijet_JESUp.mass();
  output.deta_JESUp = std::abs(leadJet_JESUp.eta() - subleadJet_JESUp.eta());
  output.dphi_JESUp = std::abs(reco::deltaPhi(leadJet_JESUp.phi(), subleadJet_JESUp.phi()));
  output.pt1_JESUp = leadJet_JESUp.pt();
  output.pt2_JESUp = subleadJet_JESUp.pt();
  output.dijetpt_JESUp = dijet_JESUp.pt();
  output.dijetrapidity_JESUp = dijet_JESUp.Rapidity();
  output.eta1_JESUp = leadJet_JESUp.eta();
  output.eta2_JESUp = subleadJet_JESUp.eta();

  output.dphihj = std::abs(reco::deltaPhi(dijet.phi(), ditau.phi()));
  output.dphihj_nomet = std::abs(reco::deltaPhi(dijet.phi(),ditauvis.phi()));
  output.c1 = std::min(
      std::abs(ditauvis.eta() - leadJet.eta()),
      std::abs(ditauvis.eta() - subleadJet.eta()));
  output.c2 = ditauvis.pt();
 
  // Figure out the central gap area
  float maxEta = std::max(leadJet.eta(), subleadJet.eta());
  float minEta = std::min(leadJet.eta(), subleadJet.eta());

  float maxEta_JESDown = std::max(leadJet_JESDown.eta(), subleadJet_JESDown.eta());
  float minEta_JESDown = std::min(leadJet_JESDown.eta(), subleadJet_JESDown.eta());

  float maxEta_JESUp = std::max(leadJet_JESUp.eta(), subleadJet_JESUp.eta());
  float minEta_JESUp = std::min(leadJet_JESUp.eta(), subleadJet_JESUp.eta());

  output.jets20 = 0;
  output.jets30 = 0;

  output.jets20_JESDown = 0;
  output.jets30_JESDown = 0;

  output.jets20_JESUp = 0;
  output.jets30_JESUp = 0;

  // Figure out central jet veto counts
  for (size_t k = 2; k < jets.size(); ++k) {
    if(jets.at(k)->eta() > minEta && jets.at(k)->eta() < maxEta) {
      double pt = jets.at(k)->pt();
      if (pt > 20)
        output.jets20++;
      if (pt > 30)
        output.jets30++;
    }
  }

  for (size_t k = 2; k < jets.size(); ++k) {
    if(jets.at(k)->eta() > minEta_JESUp && jets.at(k)->eta() < maxEta_JESUp) {
      double pt = jets.at(k)->pt();
      if (pt > 20)
        output.jets20_JESUp++;
      if (pt > 30)
        output.jets30_JESUp++;
    }
  }

  for (size_t k = 2; k < jets.size(); ++k) {
    if(jets.at(k)->eta() > minEta_JESDown && jets.at(k)->eta() < maxEta_JESDown) {
      double pt = jets.at(k)->pt();
      if (pt > 20)
        output.jets20_JESDown++;
      if (pt > 30)
        output.jets30_JESDown++;
    }
  }

  return  output;
}
