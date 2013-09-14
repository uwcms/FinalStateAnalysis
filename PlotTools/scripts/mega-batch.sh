#!/bin/bash

# Wrapper around <mega> for use on the condor batch system
# Authors: M. Verzetti (Zurich), E. Friis (UW)
# ARGS
# 1 --> analyzer
# 2 --> input files, comma separated
# 3 --> output file name
# 4 --> working directory
# 5 --> TTree path

echo "mega-batch.sh with arguments: $@"

analyzer=$1
inputs=$2
output=$3
workingdir=$4
tree=$5

pushd $CMSSW_BASE
source $CMSSW_BASE/src/UWHiggs/environment.sh
popd
MEGA=$CMSSW_BASE/src/FinalStateAnalysis/PlotTools/scripts/mega

echo 'Initial working directory:'
echo $PWD

sandbox=$PWD

pushd $workingdir
echo "Now in directory $workingdir"
ls

echo time $MEGA $analyzer $inputs $sandbox/$output --tree "$tree" --single-mode 
time $MEGA $analyzer $inputs $sandbox/$output --tree "$tree" --single-mode --verbose
retcode=$?
popd

echo "completed with exit code $retcode"
exit $retcode
