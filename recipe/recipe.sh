#!/bin/bash

cd $CMSSW_BASE/src
echo "Checking out extra packages"
addpkg -Q -f FinalStateAnalysis/recipe/tags

# Add and patch to way speed up trigger matching
echo "Applying pat trigger matching speedup"
addpkg -Q DataFormats/PatCandidates V06-04-16 
patch -N -p0 < FinalStateAnalysis/recipe/patches/V06-04-16_DataFormats_PatCandidates_PassStrByRef.patch

echo "Adding 2D expression histogram feature"
addpkg -Q CommonTools/Utils V00-04-02      
patch -N -p0 < FinalStateAnalysis/recipe/patches/V00-04-02_CommonTools_Utils_Add2DHistoFeature.patch

echo "Fixing problem with nested input T and P directories"
addpkg -Q PhysicsTools/TagAndProbe
patch -N -p0 < FinalStateAnalysis/recipe/patches/V04-00-03_PhysicsTools_TagAndProbe_DirCanContainSlashes.patch

echo "Now run: scram b -j 4"
