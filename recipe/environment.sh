#!/bin/bash 

# Setup the environment for the FinalStateAnalysis software

cmsenv

export FSAHOME=$CMSSW_BASE/src/FinalStateAnalysis/

export vpython=$CMSSW_BASE/src/FinalStateAnalysis/recipe/external/vpython

cd $vpython
source bin/activate
cd -
