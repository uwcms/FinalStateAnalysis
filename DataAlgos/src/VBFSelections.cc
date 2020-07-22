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
    const std::vector<const reco::Candidate*>& jets,
    const std::string& sysTag) {
  VBFVariables output;

  // number of initial jets
  output.nJets = jets.size();

  // Not enough jets
  if (output.nJets < 2)
    return output;

  assert(jets[0]->pt() > jets[1]->pt() || (jets[0]->pt() == jets[1]->pt() && jets[0]->eta() != jets[1]->eta()) );

  reco::Candidate::LorentzVector leadJet;
  reco::Candidate::LorentzVector subleadJet;
  const pat::Jet * firstJet = dynamic_cast<const pat::Jet*> (jets[0]);
  const pat::Jet * secondJet = dynamic_cast<const pat::Jet*> (jets[1]);
  //Get jets corresponding to systematics tag
  if (sysTag.empty()){
    leadJet = firstJet->p4();
    subleadJet = secondJet->p4();
  }
  else{
    leadJet = firstJet->userCand(sysTag)->p4();
    subleadJet = secondJet->userCand(sysTag)->p4();
  }

  reco::Candidate::LorentzVector dijet = leadJet + subleadJet;
  output.mass = dijet.mass();

  /*reco::Candidate::LorentzVector ditauvis;
  for (size_t i = 0; i < hardScatter.size(); ++i) {
    ditauvis += hardScatter[i]->p4();
  }

  // ditau = hard scatter + MET
  reco::Candidate::LorentzVector ditau = metp4 + ditauvis;

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

  output.dphihj = std::abs(reco::deltaPhi(dijet.phi(), ditau.phi()));
  output.dphihj_nomet = std::abs(reco::deltaPhi(dijet.phi(),ditauvis.phi()));
  output.c1 = std::min(
      std::abs(ditauvis.eta() - leadJet.eta()),
      std::abs(ditauvis.eta() - subleadJet.eta()));
  output.c2 = ditauvis.pt();
 
  // Figure out the central gap area
  float maxEta = std::max(leadJet.eta(), subleadJet.eta());
  float minEta = std::min(leadJet.eta(), subleadJet.eta());

  output.jets20 = 0;
  output.jets30 = 0;

  // Figure out central jet veto counts
  for (size_t k = 2; k < jets.size(); ++k) {
    if(jets.at(k)->eta() > minEta && jets.at(k)->eta() < maxEta) {
      //double pt = jets.at(k)->pt();
       const pat::Jet * centralJet = dynamic_cast<const pat::Jet*> (jets[k]);
       double pt;
       if (sysTag.empty()){
         pt = centralJet->pt();
       }
       else{
         pt = centralJet->userCand(sysTag)->pt();
       }
      if (pt > 20)
        output.jets20++;
      if (pt > 30)
        output.jets30++;
    }
  }*/

  return  output;
}
