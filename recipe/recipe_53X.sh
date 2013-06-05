#!/bin/bash
set -o errexit
set -o nounset

# Tags for 52X

pushd $CMSSW_BASE/src

echo "Checking out PAT dataformats"
addpkg DataFormats/PatCandidates   V06-05-06-10
addpkg PhysicsTools/PatAlgos       V08-09-58
addpkg PhysicsTools/PatUtils       V03-09-28

if [ "$LIMITS" = "1" ]
then
  # For limit tool
  cvs co -r V02-02-03 HiggsAnalysis/CombinedLimit
  cvs co -r V00-02-06 HiggsAnalysis/HiggsToTauTau
fi

if [ "$PATPROD" = "1" ]
then

  echo "Checking out tuple production tags"
  addpkg DataFormats/CaloRecHit      V02-05-11
  addpkg DataFormats/StdDictionaries V00-02-14
  addpkg RecoMET/METProducers        V03-03-12-02
  
  # Stuff from Lindsey
  addpkg CommonTools/RecoUtils           V00-00-12
  cvs up -r 1.4 CommonTools/RecoUtils/BuildFile.xml
  addpkg DataFormats/HLTReco             V02-06-05
  addpkg JetMETCorrections/Type1MET      V04-06-09
  addpkg RecoBTag/SecondaryVertex        V01-08-00
  addpkg RecoVertex/AdaptiveVertexFinder V02-02-00  

  echo "Downloading Quark Gluon Jet ID"
  cvs co -r v1-2-3 -d QuarkGluonTagger/EightTeV UserCode/tomc/QuarkGluonTagger/EightTeV
  
  # MVA MET + PU Jet ID
  # This must go *before* the Tau POG checkout as it fucks with it.
  pushd $CMSSW_BASE/src/FinalStateAnalysis/recipe/
  ./recipe_mvamet.sh
  popd

  echo "Checking out Tau POG recipe"
  cvs co -r V01-04-25 RecoTauTag/RecoTau 
  cvs co -r V01-04-13 RecoTauTag/Configuration
  cvs co -r V00-04-00 CondFormats/EgammaObjects

  echo "Checking out EGamma POG recipe for electron corrections"
  cvs co -r V09-00-01 RecoEgamma/EgammaTools
  cvs co -r FB_4Jun2013 EgammaAnalysis/ElectronTools

  # revert some deleted files in the 4June tag
  cvs co -r 1.16 EgammaAnalysis/ElectronTools/src/PatElectronEnergyCalibrator.cc
  cvs co -r 1.6 EgammaAnalysis/ElectronTools/interface/PatElectronEnergyCalibrator.h

  #Get weight files
  pushd $CMSSW_BASE/src/EgammaAnalysis/ElectronTools/data
  cat download.url | xargs wget
  popd
  #apply some pathces to make everythin work
  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/PATObject.h.patch
  set -o errexit
  
  echo "Applying Marias b-tag patch"
  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/PhysicsToolsPatAlgos_fix_btags_52X.patch
  set -o errexit
  
fi

popd
