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
    const std::vector<const reco::Candidate*>& jets) {
  //JetVariables output;
  std::vector<double> output;

  //for (auto var : output) {
  //  var = -10;
  //}
  int numJets = jets.size();
  if (numJets == 0) {
    for (int i = 0; i < 16; ++i) {
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
    output.push_back( jet1Pat->partonFlavour() );
    if (jet1Pat->hasUserCand("jes+")) {
        output.push_back( jet1Pat->userCand("jes+")->pt() );}
    else output.push_back( -10 );
    if (jet1Pat->hasUserCand("jes-")) {
        output.push_back( jet1Pat->userCand("jes-")->pt() );}
    else output.push_back( -10 );
    for (int i = 0; i < 8; ++i) {
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
      output.push_back( jetPat->partonFlavour() );
      if (jetPat->hasUserCand("jes+")) {
          output.push_back( jetPat->userCand("jes+")->pt() );}
      else output.push_back( -10 );
      if (jetPat->hasUserCand("jes-")) {
          output.push_back( jetPat->userCand("jes-")->pt() );}
      else output.push_back( -10 );
    }
  }

  return output;
}

// BTag Promote/Demote Method
std::vector<int> btagPromoteDemote(
    const std::vector<const reco::Candidate*>& jets) {
  //JetVariables output;
  std::vector<int> output;

  int nbtagsL=0;
  int nbtagsupL=0;
  int nbtagsdownL=0;
  int nbtagsM=0;
  int nbtagsupM=0;
  int nbtagsdownM=0;

  for (size_t i = 0; i < jets.size(); ++i) {
    const pat::Jet * jet = dynamic_cast<const pat::Jet*> (jets[i]);
    float btaggedL = jet->userFloat("btaggedL");
    float btaggedupL = jet->userFloat("btaggedupL");
    float btaggeddownL = jet->userFloat("btaggeddownL");
    float btaggedM = jet->userFloat("btaggedM");
    float btaggedupM = jet->userFloat("btaggedupM");
    float btaggeddownM = jet->userFloat("btaggeddownM");

    if (btaggedL) nbtagsL++;
    if (btaggedupL) nbtagsupL++;
    if (btaggeddownL) nbtagsdownL++;      
    if (btaggedM) nbtagsM++;
    if (btaggedupM) nbtagsupM++;
    if (btaggeddownM) nbtagsdownM++;      

  }

  output.push_back(nbtagsL);
  output.push_back(nbtagsupL);
  output.push_back(nbtagsdownL);
  output.push_back(nbtagsM);
  output.push_back(nbtagsupM);
  output.push_back(nbtagsdownM);

  return output;
}
