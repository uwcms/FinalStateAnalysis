//#include "FinalStateAnalysis/DataAlgos/interface/JetSelections.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
//#include "DataFormats/RecoCandidate/interface/JetCandidate.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

double get_bweight2016(float pt, float eta, int flavor, float deepcsv){
  return 1.0;
}

double get_bweight2017(float pt, float eta, int flavor, float deepcsv){
  return 1.0;
}

double get_bweight2018(float pt, float eta, int flavor, float deepcsv){
  return 1.0;
}

std::vector<double> computeBInfo(
  const std::vector<const reco::Candidate*>& jets) {
  std::vector<double> output;
  double weight2016=1.0;
  double weight2017=1.0;
  double weight2018=1.0;
  for (unsigned int i = 0; i < jets.size(); ++i) {
      const pat::Jet * jetPat = dynamic_cast<const pat::Jet*> (jets[i]);
      weight2016=weight2016*get_bweight2016(jets[i]->pt(),jets[i]->eta(),jetPat->hadronFlavour(),jetPat->bDiscriminator("pfDeepCSVJetTags:probb")+jetPat->bDiscriminator("pfDeepCSVJetTags:probbb"));
      weight2017=weight2017*get_bweight2017(jets[i]->pt(),jets[i]->eta(),jetPat->hadronFlavour(),jetPat->bDiscriminator("pfDeepCSVJetTags:probb")+jetPat->bDiscriminator("pfDeepCSVJetTags:probbb"));
      weight2018=weight2018*get_bweight2018(jets[i]->pt(),jets[i]->eta(),jetPat->hadronFlavour(),jetPat->bDiscriminator("pfDeepCSVJetTags:probb")+jetPat->bDiscriminator("pfDeepCSVJetTags:probbb"));
  }
  output.push_back(weight2016);
  output.push_back(weight2017);
  output.push_back(weight2018);
  return output;
}

//JetVariables computeJetInfo(
std::vector<double> computeJetInfo(
    const std::vector<const reco::Candidate*>& jets) {
  //JetVariables output;
  std::vector<double> output;

  //for (auto var : output) {
  //  var = -9999;
  //}
  int numJets = jets.size();
  if (numJets == 0) {
    for (int i = 0; i < 20; ++i) {
      output.push_back( -9999 );
    }
  }
  if (numJets == 1) {
    const pat::Jet * jet1Pat = dynamic_cast<const pat::Jet*> (jets[0]);
    output.push_back( jets[0]->pt() );
    output.push_back( jets[0]->eta() );
    output.push_back( jets[0]->phi() );
    output.push_back( jet1Pat->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") );
    output.push_back( jet1Pat->userFloat("pileupJetId:fullDiscriminant"));
    //output.push_back( jet1Pat->userFloat("pileupJetIdUpdated:fullDiscriminant"));
    output.push_back( jet1Pat->partonFlavour() );
    output.push_back( jet1Pat->hadronFlavour() );
    output.push_back( jet1Pat->jecFactor("Uncorrected") );
    if (jet1Pat->hasUserCand("jes+")) {
        output.push_back( jet1Pat->userCand("jes+")->pt() );}
    else output.push_back( -9999 );
    if (jet1Pat->hasUserCand("jes-")) {
        output.push_back( jet1Pat->userCand("jes-")->pt() );}
    else output.push_back( -9999 );
    for (int i = 0; i < 10; ++i) {
      output.push_back( -9999 );
    }
  }
  if (numJets >= 2) {
    for (int i = 0; i < 2; ++i) {
      const pat::Jet * jetPat = dynamic_cast<const pat::Jet*> (jets[i]);
      output.push_back( jets[i]->pt() );
      output.push_back( jets[i]->eta() );
      output.push_back( jets[i]->phi() );
      output.push_back( jetPat->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") );
      output.push_back( jetPat->userFloat("pileupJetId:fullDiscriminant"));
      //output.push_back( jetPat->userFloat("pileupJetIdUpdated:fullDiscriminant"));
      output.push_back( jetPat->partonFlavour() );
      output.push_back( jetPat->hadronFlavour() );
      output.push_back( jetPat->jecFactor("Uncorrected") );
      if (jetPat->hasUserCand("jes+")) {
          output.push_back( jetPat->userCand("jes+")->pt() );}
      else output.push_back( -9999 );
      if (jetPat->hasUserCand("jes-")) {
          output.push_back( jetPat->userCand("jes-")->pt() );}
      else output.push_back( -9999 );
    }
  }

  return output;
}

