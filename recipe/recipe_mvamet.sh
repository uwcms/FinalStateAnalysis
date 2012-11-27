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
  cvs co -r METPU_5_3_X_v2 JetMETCorrections/METPUSubtraction
  pushd $CMSSW_BASE/src/JetMETCorrections/METPUSubtraction/test/
  ./setup.sh
  popd
  cvs up -r 1.6 PhysicsTools/PatAlgos/plugins/PATMHTProducer.h
  # This is a bug in setup.sh
  cvs up -r METPU_5_3_X_v3 RecoJets/JetProducers
  if [ "$MINOR_VERSION" -eq "2" ]; then
    # Workaround a header file location change
    cvs up -r 1.1 DataFormats/JetReco/interface/PFClusterJet.h
    cvs up -r 1.2 RecoMET/METAlgorithms/src/PFClusterSpecificAlgo.cc
  fi
else
  cvs co -r METPU_4_2_X JetMETCorrections/METPUSubtraction
  pushd $CMSSW_BASE/src/JetMETCorrections/METPUSubtraction/test/
  ./setup42.sh
  popd
  cvs up -r 1.6 PhysicsTools/PatAlgos/plugins/PATMHTProducer.h
  # Get forgotton dependency
  cvs co -r CMSSW_4_4_2 JetMETCorrections/Objects
  cvs co -r CMSSW_4_4_2 CondFormats/JetMETObjects
  pushd $CMSSW_BASE/src
  # Fix link error
  patch -N -p0 < FinalStateAnalysis/recipe/patches/PhysicsToolsPatAlgos_mvamet_buildfile_42X.patch
  popd
fi

popd
