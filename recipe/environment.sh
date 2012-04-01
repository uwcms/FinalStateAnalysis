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

# Define shortcuts for the relevant global tags 
export datagt=GR_R_42_V24::All
export mcgt=START42_V17::All

# Define some shortcuts to HDFS and scratch areas
export hdfs=/hdfs/store/user/$LOGNAME/
export scratch=/scratch/$LOGNAME/

export VIRTUAL_ENV_DISABLE_PROMPT=1
cd $vpython
source bin/activate
cd -
