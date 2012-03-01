#!/bin/bash 

# Setup the environment for the FinalStateAnalysis software

echo "Setting up CMSSW runtime environment"
cmsenv

export FSAHOME=$CMSSW_BASE/src/FinalStateAnalysis/
echo "Setting variable FSAHOME=$FSAHOME"
# easier to type
export fsa=$FSAHOME

export vpython=$CMSSW_BASE/src/FinalStateAnalysis/recipe/external/vpython
echo "Activating python virtualenv from $vpython"

export tests=$CMSSW_BASE/test/$SCRAM_ARCH/

cd $vpython
source bin/activate
cd -
