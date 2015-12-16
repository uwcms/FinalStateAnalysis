//#include "FinalStateAnalysis/DataAlgos/interface/JetSelections.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

//JetVariables computeJetInfo(
std::vector<double> computeJetInfo(
    const std::vector<const reco::Candidate*>& hardScatter,
    const reco::Candidate::LorentzVector& metp4,
    const std::vector<const reco::Candidate*>& jets) {
  //JetVariables output;
  std::vector<double> output;

  //for (auto var : output) {
  //  var = -10;
  //}
  int numJets = jets.size();
  if (numJets == 0) {
    for (int i = 0; i < 12; ++i) {
      output.push_back( -10 );
    }
  }
  if (numJets == 1) {
    output.push_back( jets[0]->pt() );
    output.push_back( jets[0]->eta() );
    output.push_back( jets[0]->phi() );
    //output.push_back( jets[0]->userCand("patJet").bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") );
    //output.push_back( jets[0]->userCand("patJet").userFloat("pileupJetId:fullDiscriminant") );
    //output.push_back( jets[0]->SomeConversionThingForJEC );
    output.push_back( -10 );
    output.push_back( -10 );
    output.push_back( -10 );
    for (int i = 0; i < 6; ++i) {
      output.push_back( -10 );
    }
  }
  if (numJets >= 2) {
    for (int i = 0; i < 2; ++i) {
      output.push_back( jets[i]->pt() );
      output.push_back( jets[i]->eta() );
      output.push_back( jets[i]->phi() );
      //output.push_back( jets[i]->userCand("patJet").bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") );
      //output.push_back( jets[i]->userCand("patJet").userFloat("pileupJetId:fullDiscriminant") );
      //output.push_back( jets[i]->SomeConversionThingForJEC );
      output.push_back( -10 );
      output.push_back( -10 );
      output.push_back( -10 );
    }
  }
//  if( jets[0]->pt() > jets[1]->pt() ) {
//    output.leadJet = jets[0];
//    output.subleadJet = jets[1];
//  } else {
//    output.leadJet = jets[1];
//    output.subleadJet = jets[0];
//  } 
//
//  // Get 4vectors of two highest jets
//  reco::Candidate::LorentzVector leadJet(output.leadJet->p4());
//  reco::Candidate::LorentzVector subleadJet(output.subleadJet->p4());
//
//  output.pt1 = leadJet.pt();
//  output.pt2 = subleadJet.pt();
//  output.eta1 = leadJet.eta();
//  output.eta2 = subleadJet.eta();

  return output;
}
