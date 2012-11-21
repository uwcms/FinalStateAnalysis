#!/bin/bash
set -o errexit
set -o nounset

# Tags for 52X

pushd $CMSSW_BASE/src

echo "Checking out PAT tags"
addpkg DataFormats/PatCandidates V06-05-06-03

if [ "$PATPROD" = "1" ]
then
  addpkg PhysicsTools/PatAlgos     V08-09-42
  #24/10/2012 LAG -- PF Isolation for Photons
  #latest PAT recipe
  addpkg RecoParticleFlow/PFProducer     V15-02-06

  echo "Checking out Tau POG recipe"
  cvs co -r V01-04-17 RecoTauTag/RecoTau #equivalent to 04-14
  cvs co -r V01-04-03 RecoTauTag/Configuration
  cvs co -r V00-04-01 CondFormats/EgammaObjects
  cvs up -r 1.53 PhysicsTools/PatAlgos/python/tools/tauTools.py
  cvs up -r 1.12 PhysicsTools/PatAlgos/python/producersLayer1/tauProducer_cff.py
  cvs up -r 1.15 PhysicsTools/PatAlgos/python/recoLayer0/tauDiscriminators_cff.py

  echo "Checking out EGamma POG recipe for electron corrections"
  addpkg RecoEgamma/EgammaTools V08-11-10-02
  cvs co -r V00-00-30 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
  cvs co -r HCP2012_V03-02 EgammaAnalysis/ElectronTools

  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/PhysicsToolsPatAlgos_fix_btags_52X.patch
  set -o errexit
fi

popd
