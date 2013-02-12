#!/bin/bash
set -o errexit
set -o nounset

# Tags for 52X

pushd $CMSSW_BASE/src

echo "Checking out PAT dataformats"
addpkg DataFormats/PatCandidates       V06-05-06-06

if [ "$LIMITS" = "1" ]
then
  # For limit tool
  cvs co -r V02-02-03 HiggsAnalysis/CombinedLimit
  cvs co -r V00-02-06 HiggsAnalysis/HiggsToTauTau
fi

if [ "$PATPROD" = "1" ]
then

  echo "Checking out tuple production tags"
  
  addpkg PhysicsTools/PatAlgos           V08-09-52
  addpkg DataFormats/StdDictionaries     V00-02-14
  addpkg PhysicsTools/PatUtils           V03-09-26
  addpkg CommonTools/ParticleFlow        V00-03-16
  addpkg FWCore/GuiBrowsers              V00-00-70
  #24/10/2012 LAG -- PF Isolation for Photons
  addpkg RecoParticleFlow/PFProducer     V15-02-06
  addpkg CommonTools/RecoUtils           V00-00-12
  cvs up -r 1.4 CommonTools/RecoUtils/BuildFile.xml
  addpkg DataFormats/HLTReco             V02-06-05
  addpkg JetMETCorrections/Type1MET      V04-06-09
  addpkg RecoBTag/SecondaryVertex        V01-08-00
  addpkg RecoVertex/AdaptiveVertexFinder V02-02-00  

  # MVA MET + PU Jet ID
  # This must go *before* the Tau POG checkout as it fucks with it.
  pushd $CMSSW_BASE/src/FinalStateAnalysis/recipe/
  ./recipe_mvamet.sh
  popd

  echo "Checking out Tau POG recipe"
  cvs co -r V01-04-23 RecoTauTag/RecoTau #equivalent to 04-14
  cvs co -r V01-04-10 RecoTauTag/Configuration
  cvs co -r V00-04-00 CondFormats/EgammaObjects

  echo "Checking out EGamma POG recipe for electron corrections"
  addpkg RecoEgamma/EgammaTools V08-11-10-02
  cvs co -r V00-00-30-02 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
  cvs up -r 1.4 EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h
  cvs co -r HCP2012_V03-02 EgammaAnalysis/ElectronTools
  
  # apply patch so we can configure the passing mask for the PassWP function
  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/EGammaAnalysisTools_configpatch.patch
  set -o errexit

  #apply patch that lets us use the new MVA ID
  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/EGammaMVAID_updatepatch.patch
  set -o errexit
  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/EGammaMVAID_Estimator.patch
  set -o errexit
  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/EGammaMVAID_buildfile.patch
  set -o errexit

  echo "Applying Marias b-tag patch"
  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/PhysicsToolsPatAlgos_fix_btags_52X.patch
  set -o errexit
  
fi

popd
