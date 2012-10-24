#!/bin/bash
set -o errexit
set -o nounset

# Tags for 52X

pushd $CMSSW_BASE/src

echo "Checking out PAT tags"
addpkg DataFormats/PatCandidates       V06-05-01
addpkg PhysicsTools/PatAlgos           V08-09-23
addpkg PhysicsTools/PatUtils           V03-09-23
addpkg CommonTools/ParticleFlow        V00-03-16
#20/10/2012 LAG -- PF Isolation for Photons
#https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPFBasedIsolation#Alternate_code_to_calculate_PF_I
addpkg RecoParticleFlow/PFProducer     V15-01-08
addpkg CommonTools/RecoUtils           V00-00-12
cvs up -r 1.4 CommonTools/RecoUtils/BuildFile.xml
addpkg DataFormats/HLTReco             V02-06-05
addpkg JetMETCorrections/Type1MET      V04-06-09
addpkg RecoBTag/SecondaryVertex        V01-08-00
addpkg RecoVertex/AdaptiveVertexFinder V02-02-00

echo "Checking out Tau POG recipe"
cvs co -r V01-04-17 RecoTauTag/RecoTau #equivalent to 04-14
cvs co -r V01-04-03 RecoTauTag/Configuration
cvs co -r V00-04-01 CondFormats/EgammaObjects
cvs up -r 1.53 PhysicsTools/PatAlgos/python/tools/tauTools.py
cvs up -r 1.12 PhysicsTools/PatAlgos/python/producersLayer1/tauProducer_cff.py
cvs up -r 1.15 PhysicsTools/PatAlgos/python/recoLayer0/tauDiscriminators_cff.py

echo "Checking out EGamma POG recipe for electron corrections"
cvs co -r FB_23Oct2012-2 EgammaAnalysis/ElectronTools

set +o errexit
patch -N -p0 < FinalStateAnalysis/recipe/patches/PhysicsToolsPatAlgos_fix_btags_52X.patch
set -o errexit

popd
