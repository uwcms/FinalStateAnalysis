#!/bin/bash

: ${CMSSW_BASE:?"CMSSW_BASE is not set!  Run cmsenv before recipe.sh"}

cd $CMSSW_BASE/src
echo "Checking out extra packages"
addpkg -z -f FinalStateAnalysis/recipe/tags

echo "Checking out Tau POG recipe"
addpkg DataFormats/TauReco CMSSW_5_2_4 # yes, this is correct
addpkg RecoTauTag/TauTagTools CMSSW_5_2_4
cvs co -r V01-04-14 RecoTauTag/RecoTau
cvs co -r V01-04-01 RecoTauTag/Configuration
cvs co -r V00-04-01 CondFormats/EgammaObjects
addpkg -z PhysicsTools/PatAlgos 
cvs up -r 1.53 PhysicsTools/PatAlgos/python/tools/tauTools.py

# Add and patch to way speed up trigger matching
echo "Applying pat trigger matching speedup"
addpkg -z DataFormats/PatCandidates 
patch -N -p0 < FinalStateAnalysis/recipe/patches/V06-04-16_DataFormats_PatCandidates_PassStrByRef.patch

echo "Adding 2D expression histogram feature"
addpkg -z CommonTools/Utils 
patch -N -p0 < FinalStateAnalysis/recipe/patches/V00-04-02_CommonTools_Utils_Add2DHistoFeature.patch

# Add support for PU Jet ID
# See https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID
cvs co -r V00-00-09 -d CMGTools/External UserCode/CMG/CMGTools/External

# Add MVA MET
# See https://twiki.cern.ch/twiki/bin/view/CMS/MVAMet
cvs co -r V00-00 -d  pharris/MVAMet UserCode/pharris/MVAMet
cvs co -D "05/02/2012" CondFormats/EgammaObjects
rm pharris/MVAMet/src/GBRTree.cxx
rm pharris/MVAMet/src/GBRForest.cxx
rm pharris/MVAMet/src/PHMetAnalysisLinkDef.h

# Note you now need to install virtual env

# Add Electron ID MVA
cvs co -r V00-00-06 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools

echo "Now run ./install_python.sh to install python"

echo "To compile: scram b -j 4"
