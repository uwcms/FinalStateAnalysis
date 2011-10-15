#!/bin/bash

cd $CMSSW_BASE/src
echo "Checking out extra packages"
addpkg -f tags

# Add and patch to way speed up trigger matching
echo "Applying pat trigger matching speedup"
addpkg DataFormats/PatCandidates V06-04-16 
patch -p0 < FinalStateAnalysis/recipe/patches/V06-04-16_DataFormats_PatCandidates_PassStrByRef.patch

echo "Adding 2D expression histogram feature"
addpkg CommonTools/Utils V00-04-02      
patch -p0 < FinalStateAnalysis/recipe/patches/V00-04-02_CommonTools_Utils_Add2DHistoFeature.patch
