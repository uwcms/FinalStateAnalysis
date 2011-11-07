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

echo "Checking out pat support for new tau discriminators"
addpkg -Q PhysicsTools/PatAlgos 
# For new tau discriminators
cvs up -r 1.43 PhysicsTools/PatAlgos/python/tools/tauTools.py
# Add Mike's muon discriminant
patch -N -p0 < FinalStateAnalysis/recipe/patches/1.43_PhysicsTools_PatAlgos_tauTools.patch
# For bug fixes (mainly where runOnData overwrote the JEC
# http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/PhysicsTools/PatAlgos/python/tools/coreTools.py?revision=1.33.4.2&view=markup
cvs up -r 1.33.4.6 PhysicsTools/PatAlgos/python/tools/coreTools.py

echo "Now run: scram b -j 4"
