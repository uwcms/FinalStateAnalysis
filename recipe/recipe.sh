#!/bin/bash

: ${CMSSW_BASE:?"CMSSW_BASE is not set!  Run cmsenv before recipe.sh"}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`

echo "Detected CMSSW version: $MAJOR_VERSION"

if [ "$MAJOR_VERSION" -eq "4" ]; then
  echo "Applying recipe for CMSSW 4_2_8"
  ./recipe_52X.sh
fi

if [ "$MAJOR_VERSION" -eq "5" ]; then
  echo "Applying recipe for CMSSW 5_2_4"
  ./recipe_52X.sh
fi

echo "Applying common recipe"
./recipe_common.sh

# Note you now need to install virtual env
echo "Now run ./install_python.sh to install python"

echo "To compile: scram b -j 4"
