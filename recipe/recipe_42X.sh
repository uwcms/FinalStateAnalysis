#!/bin/bash
set -o errexit
set -o nounset

pushd $CMSSW_BASE/src

# Always need these
addpkg DataFormats/PatCandidates  V06-04-19-05
# PAT RECIPE V08-06-58 IAR 27.Sep.2012
# patch in 44X electrons so regression BS works
cvs up -r 1.44 DataFormats/PatCandidates/interface/Electron.h
cvs up -r 1.33 DataFormats/PatCandidates/src/Electron.cc
addpkg PhysicsTools/PatAlgos V08-06-58
addpkg PhysicsTools/PatUtils V03-09-18
addpkg CommonTools/ParticleFlow B4_2_X_V00-03-05
addpkg PhysicsTools/SelectorUtils V00-03-24
addpkg PhysicsTools/UtilAlgos V08-02-14 
# Remove this junky MHT package, we don't need it and it causes
# link errors with the MVAMET
rm -f PhysicsTools/PatAlgos/plugins/PATMHTProducer*


if [ "$LIMITS" = "1" ]
then
  # For limit tool
  cvs co -r V01-13-02 HiggsAnalysis/CombinedLimit
  cvs co -r V01-13-02 HiggsAnalysis/HiggsToTauTau
fi


if [ "$PATPROD" = "1" ]
then

  #Update to calculate Single Tower H/E in 42X
  #https://twiki.cern.ch/twiki/bin/view/CMS/HoverE2012
  cvs co -r CMSSW_4_2_8_patch7 RecoEgamma/EgammaElectronAlgos
  cvs co -r CMSSW_5_2_2 RecoEgamma/EgammaElectronAlgos/src/ElectronHcalHelper.cc
  cvs co -r CMSSW_5_2_2 RecoEgamma/EgammaElectronAlgos/interface/ElectronHcalHelper.h
  cvs co -r CMSSW_5_2_2 RecoEgamma/EgammaIsolationAlgos

  # For a fix to prevent segfaults on certain MC samples when using
  # the GenParticlePrunder
  cvs co -r V11-03-16 PhysicsTools/HepMCCandAlgos

  echo "Checking out EGamma POG recipe for electron corrections"
  addpkg RecoEgamma/EgammaTools V08-11-10-02
  cvs co -r V00-00-30-BP42X -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
  cvs co -r HCP2012_V04-44X EgammaAnalysis/ElectronTools
  # apply patch so we can configure the passing mask for the PassWP function
  patch -N -p0 < FinalStateAnalysis/recipe/patches/EGammaAnalysisTools_configpatch.patch

  # patch (really an un-patch, but who's counting) electron corrections in 42x IAR 13.Feb.2013
  pushd $CMSSW_BASE/src/FinalStateAnalysis/
  patch -p1 < recipe/patches/electronCorr_42X.patch 
  popd

  echo "Checking out Tau POG recipe"
  addpkg DataFormats/TauReco CMSSW_5_2_4 # yes, this is correct
  addpkg RecoTauTag/TauTagTools CMSSW_5_2_4
  cvs co -r V01-04-23-4XX-00 RecoTauTag/RecoTau
  cvs co -r V01-04-10-4XX RecoTauTag/Configuration
  cvs co -r V00-04-00 CondFormats/EgammaObjects
  cvs up -r 1.52.10.4 PhysicsTools/PatAlgos/python/tools/tauTools.py
  # Apply an optimization - don't build taus w/ pt < 19
  # Don't crash if patch already appliede
  set +o errexit 
  # Make sure we have a clean copy.  
  cvs up -C RecoTauTag/RecoTau
  patch -N -p0 < FinalStateAnalysis/recipe/patches/speedupRecoTauCombBuilder.patch
  # Add Marias patch for negative SSV 
  patch -N -p0 < FinalStateAnalysis/recipe/patches/marias_negativeSSV.patch
  set -o errexit 
fi

popd
