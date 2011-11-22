#!/bin/bash

cd $CMSSW_BASE/src
echo "Checking out extra packages"
addpkg -z -f FinalStateAnalysis/recipe/tags

# Add and patch to way speed up trigger matching
echo "Applying pat trigger matching speedup"
addpkg -z DataFormats/PatCandidates 
patch -N -p0 < FinalStateAnalysis/recipe/patches/V06-04-16_DataFormats_PatCandidates_PassStrByRef.patch

echo "Adding 2D expression histogram feature"
addpkg -z CommonTools/Utils 
patch -N -p0 < FinalStateAnalysis/recipe/patches/V00-04-02_CommonTools_Utils_Add2DHistoFeature.patch

echo "Checking out pat support for new tau discriminators"
addpkg -z PhysicsTools/PatAlgos 
# Add Mike's muon discriminant
cvs co -r 1.46 PhysicsTools/PatAlgos/python/tools/tauTools.py

echo "Now run: scram b -j 4"
