#!/bin/bash

# If FinalStateAnalysis resides somewhere besides $CMSSW_BASE/src, and is
# symlinked into place, scram build will not build the python symlinks
# appropriately.  This script does this manually, and is only necessary if
# FinalStateAnalysis lives in a symlinked directory.

cd ${CMSSW_BASE}/python

for subdir in `ls -d ../src/FinalStateAnalysis/*`
do
  if [ -d "$subdir/python" ]; then
    mkdir -p FinalStateAnalysis
    touch FinalStateAnalysis/__init__.py
    package=`basename $subdir`
    if ! [ -L FinalStateAnalysis/$package ]; then
      echo "\$CMSSW_BASE/python/FinalStateAnalysis/$package => $subdir/python"
      ln -f -s ../$subdir/python FinalStateAnalysis/$package
    fi
  fi
done
