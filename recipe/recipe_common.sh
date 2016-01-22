#!/bin/bash
set -o errexit
set -o nounset

pushd $CMSSW_BASE/src

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`

#for standalone version of svfit
#git clone git@github.com:veelken/SVfit_standalone.git TauAnalysis/SVfitStandalone
#pushd $CMSSW_BASE/src/TauAnalysis/SVfitStandalone
#git checkout svFit_2015Mar28
#popd

# Add and patch to way speed up trigger matching
# Don't crash if patch already applied.
#set +o errexit
#echo "Applying pat trigger matching speedup"
#git cms-addpkg DataFormats/PatCandidates
#git apply FinalStateAnalysis/recipe/patches/DataFormats_PatCandidates_TriggerEvent.cc.patch
#set -o errexit


popd
