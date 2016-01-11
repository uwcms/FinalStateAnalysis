#!/usr/bin/env bash

# Install dependencies for the FinalStateAnalysis package.
# Usage:
#   OPT1=0 OPT2=1 ./recipe.sh
#
# Some packages are optional.   The options are passed as environment variables 
# to the script (0 or 1) Here are the following options:
# 
#    HZZ: MELA to support the ZZ analysis. Always produced if PATPROD=1
#
# Options which are absolutely required, like PAT data formats, are always 
# installed.
#
# Author: Bucky Badger and friends, UW Madison

# Set default values for the options
HZZ=${HZZ:-0}


set -o errexit
set -o nounset

: ${CMSSW_BASE:?"CMSSW_BASE is not set!  Run cmsenv before recipe.sh"}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`

echo "Detected CMSSW version: $MAJOR_VERSION $MINOR_VERSION"

echo "Store your git ssh password"
eval `ssh-agent -s` 
if ssh-add; then
    echo "ssh agent properly configured"
else
    echo "ssh agent could not retreive your git password!"
    echo "This is probably due to the fact that you did not install either locally or on gitHub the ssh-key access"
    echo "follow the instructions on https://help.github.com/articles/generating-ssh-keys and launch again this command"
    exit 42
fi

if [ -z "FORCERECIPE" ]; then
   while true; do
       read -p "Do you wish continue? " yn
       case $yn in
           [Yy]* ) echo "sounds good dude"; break;;
           [Nn]* ) exit 2;;
           * ) echo "Please answer yes or no.";;
       esac
   done
fi


echo "Applying recipe for CMSSW 7_6_X"
HZZ=$HZZ ./recipe_13TeV.sh

echo "Applying common recipe"
./recipe_common.sh

echo "Kill the ssh-agent"
eval `ssh-agent -k` 


cd $CMSSW_BASE/src
