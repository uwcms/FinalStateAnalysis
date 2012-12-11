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
  cvs co -r V00-02-09 -d CMGTools/External UserCode/CMG/CMGTools/External
  cvs co -r V00-02      -d  pharris/MVAMet UserCode/pharris/MVAMet
  cvs co -r CMSSW_4_2_8_patch7 RecoMET/METAlgorithms
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METAlgorithms/interface/PFMETAlgorithmMVA.h
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METAlgorithms/interface/mvaMEtUtilities.h
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METAlgorithms/src/PFMETAlgorithmMVA.cc  
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METAlgorithms/src/mvaMEtUtilities.cc
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METAlgorithms/BuildFile.xml
  cvs co -r CMSSW_4_2_8_patch7 RecoMET/METProducers
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METProducers/interface/PFMETProducerMVA.h
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METProducers/src/PFMETProducerMVA.cc
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METProducers/python/mvaPFMET_cff.py
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METProducers/python/mvaPFMET_cff_leptons.py
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METProducers/BuildFile.xml
  cp /afs/cern.ch/user/b/bianchi/public/SealModule.cc RecoMET/METProducers/src/
  cvs up -r ph_52X_MVAMet_v3 RecoMET/METProducers/python/mvaPFMET_leptons.py
  cvs co -r V00-04-01 CondFormats/EgammaObjects
fi

popd
