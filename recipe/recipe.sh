#!/bin/bash

# Set default values for the options
LIMITS=${LIMITS:-0}
PATPROD=${PATPROD:-0}

set -o errexit
set -o nounset

: ${CMSSW_BASE:?"CMSSW_BASE is not set!  Run cmsenv before recipe.sh"}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`

echo "Detected CMSSW version: $MAJOR_VERSION"

echo "Checking for CERN CVS kerberos ticket"
set +o errexit
HAS_TICKET=`klist 2>&1 | grep CERN.CH`
set -o errexit

if [ -z "$HAS_TICKET" ]; then
  echo "ERROR: You need to kinit yourname@CERN.CH to enable CVS checkouts"
  exit 1
fi

echo "I'm going to install the FinalStateAnalysis with the following options:"
echo " Limit setting (\$LIMITS): $LIMITS"
echo " PAT tuple production (\$PATPROD): $PATPROD"

while true; do
    read -p "Do you wish continue? " yn
    case $yn in
        [Yy]* ) echo "sounds good dude"; break;;
        [Nn]* ) exit 2;;
        * ) echo "Please answer yes or no.";;
    esac
done

if [ "$MAJOR_VERSION" -eq "4" ]; then
  echo "Applying recipe for CMSSW 4_2_8"
  LIMITS=$LIMITS PATPROD=$PATPROD ./recipe_42X.sh
fi

if [ "$MAJOR_VERSION" -eq "5" ]; then
  echo "Applying recipe for CMSSW 5_X_X"
  LIMITS=$LIMITS PATPROD=$PATPROD ./recipe_52X.sh
fi

echo "Applying common recipe"
LIMITS=$LIMITS PATPROD=$PATPROD ./recipe_common.sh

# Note you now need to install virtual env
echo "Now run recipe/install_python.sh to install python"

cd $CMSSW_BASE/src

echo "To compile: scram b -j 4"
