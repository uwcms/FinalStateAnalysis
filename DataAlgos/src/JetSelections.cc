//#include "FinalStateAnalysis/DataAlgos/interface/JetSelections.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
//#include "DataFormats/RecoCandidate/interface/JetCandidate.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

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
    const pat::Jet * jet1Pat = dynamic_cast<const pat::Jet*> (jets[0]);
    output.push_back( jets[0]->pt() );
    output.push_back( jets[0]->eta() );
    output.push_back( jets[0]->phi() );
    output.push_back( jet1Pat->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") );
    output.push_back( jet1Pat->userFloat("pileupJetId:fullDiscriminant") );
    //output.push_back( jets[0]->SomeConversionThingForJEC );
    output.push_back( -10 );
    for (int i = 0; i < 6; ++i) {
      output.push_back( -10 );
    }
  }
  if (numJets >= 2) {
    for (int i = 0; i < 2; ++i) {
      const pat::Jet * jetPat = dynamic_cast<const pat::Jet*> (jets[i]);
      output.push_back( jets[i]->pt() );
      output.push_back( jets[i]->eta() );
      output.push_back( jets[i]->phi() );
      output.push_back( jetPat->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") );
      output.push_back( jetPat->userFloat("pileupJetId:fullDiscriminant") );
      //output.push_back( jets[i]->SomeConversionThingForJEC );
      output.push_back( -10 );
    }
  }

  return output;
}
