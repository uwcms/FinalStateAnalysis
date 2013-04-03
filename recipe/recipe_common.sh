#!/bin/bash
set -o errexit
set -o nounset

pushd $CMSSW_BASE/src

#for standalone version of svfit
 cvs co -r V00-01-04s TauAnalysis/CandidateTools

# for some reason patTuple creation fails due to lack  of plugin PFCandIsolatorFromDeposits
# to fix
cvs co -r V00-03-13 CommonTools/ParticleFlow

# Tags that work in any release

# To install lumiCalc.py
if [ "$LUMI" = "1" ] 
then
  cvs co -r V04-01-09 RecoLuminosity/LumiDB 
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

else
  cat > $CMSSW_BASE/src/FinalStateAnalysis/PatTools/interface/PATProductionFlag.h << EOF 
//#define ENABLE_PAT_PROD
EOF

fi

popd
