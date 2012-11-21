#!/bin/bash
set -o errexit
set -o nounset

pushd $CMSSW_BASE/src

# Tags that work in any release

# To install lumiCalc.py
if [ "$LUMI" = "1" ] 
then
  cvs co -r V04-01-06 RecoLuminosity/LumiDB 
fi

# Add and patch to way speed up trigger matching
# Don't crash if patch already applied.
set +o errexit 
echo "Applying pat trigger matching speedup"
patch -N -p0 < FinalStateAnalysis/recipe/patches/V06-04-16_DataFormats_PatCandidates_PassStrByRef.patch
set -o errexit

#echo "Adding 2D expression histogram feature"
#addpkg -z CommonTools/Utils 
#patch -N -p0 < FinalStateAnalysis/recipe/patches/V00-04-02_CommonTools_Utils_Add2DHistoFeature.patch
#set -o errexit

# Only checkout PAT tuple production dependencies if requested.
if [ "$PATPROD" = "1" ]
then
  # Set the compile time flag which enables PAT modules that have external
  # dependencies. 
  cat > $CMSSW_BASE/src/FinalStateAnalysis/PatTools/interface/PATProductionFlag.h << EOF 
#define ENABLE_PAT_PROD
EOF

  # Add Electron ID MVA - the tags get checked out in 42X/52X/53X specific
  # scripts
  pushd $CMSSW_BASE/src/EGamma/EGammaAnalysisTools/data
  cat download.url | xargs wget
  popd

  # PU Jet ID
  cvs co -r V00-02-09 -d CMGTools/External UserCode/CMG/CMGTools/External

  # MVA MET
  pushd $CMSSW_BASE/src/FinalStateAnalysis/recipe/
  ./recipe_mvamet.sh
  popd

else
  cat > $CMSSW_BASE/src/FinalStateAnalysis/PatTools/interface/PATProductionFlag.h << EOF 
//#define ENABLE_PAT_PROD
EOF

fi

# Get the VBF MVA weight files
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2012#VBF_selection_Matthew
cvs co -r 1.2 UserCode/MitHtt/data/VBFMVA/MuTau/VBFMVA_BDTG.weights.xml

popd
