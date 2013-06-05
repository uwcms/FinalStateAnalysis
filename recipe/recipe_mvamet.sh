#!/bin/bash

# Install the MVA MET

set -o errexit
set -o nounset

: ${CMSSW_BASE:?"CMSSW_BASE is not set!  Run cmsenv before recipe.sh"}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`

pushd $CMSSW_BASE/src

if [ "$MAJOR_VERSION" -eq "5" ]; then
  # Add MVA MET
  cvs co -r METPU_5_3_X_v9 JetMETCorrections/METPUSubtraction
  pushd $CMSSW_BASE/src/JetMETCorrections/METPUSubtraction/test/
  ./setup.sh
  popd
  cvs up -r 1.6 PhysicsTools/PatAlgos/plugins/PATMHTProducer.h
  pushd $CMSSW_BASE/src
    patch -p0 -N < FinalStateAnalysis/recipe/patches/fixMVAMET_CVSConflicts.patch
  popd
else
  cvs co -r   METPU_4_2_X_v2 JetMETCorrections/METPUSubtraction
  pushd $CMSSW_BASE/src/JetMETCorrections/METPUSubtraction/test/
  ./setup42.sh
  popd
  touch $CMSSW_BASE/src/RecoJets/JetProducers/data/dummy.txt
  # apply patch from Andrew Gilbert
  # https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingMoriond2013#MVA_Met_Sequence_with_predef_AN1
  pushd $CMSSW_BASE/src
    patch -p0 -N < FinalStateAnalysis/recipe/patches/mvamet-jetid-42X.patch
  popd
  addpkg CommonTools/RecoAlgos
  cvs co -r 1.1 CommonTools/RecoAlgos/plugins/PFJetSelector.cc

fi

popd
