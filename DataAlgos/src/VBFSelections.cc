#include "FinalStateAnalysis/DataAlgos/interface/VBFSelections.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "TLorentzVector.h"

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

  TLorentzVector leadJet;
  TLorentzVector subleadJet;
  const pat::Jet * firstJet = dynamic_cast<const pat::Jet*> (jets[0]);
  const pat::Jet * secondJet = dynamic_cast<const pat::Jet*> (jets[1]);
  //Get jets corresponding to systematics tag
  leadJet.SetPtEtaPhiM(firstJet->pt(),firstJet->eta(),firstJet->phi(),firstJet->mass());
  subleadJet.SetPtEtaPhiM(secondJet->pt(),secondJet->eta(),secondJet->phi(),secondJet->mass());
  if (!sysTag.empty()){
     leadJet.SetPtEtaPhiM(firstJet->userFloat(sysTag),leadJet.Eta(),leadJet.Phi(),leadJet.M());
     subleadJet.SetPtEtaPhiM(secondJet->userFloat(sysTag),subleadJet.Eta(),subleadJet.Phi(),subleadJet.M());
  }

  TLorentzVector dijet = leadJet + subleadJet;
  output.mass = dijet.M();

  return  output;
}
