#!/bin/bash
set -o errexit
set -o nounset

pushd $CMSSW_BASE/src

#for standalone version of svfit
# cvs co -r V00-01-04s TauAnalysis/CandidateTools
git clone https://github.com/cms-analysis/TauAnalysis-CandidateTools.git TauAnalysis/CandidateTools
pushd $CMSSW_BASE/src/TauAnalysis/CandidateTools
git checkout TauAnalysis-CandidateTools-V00-01-04s
pushd $CMSSW_BASE/src

# Tags that work in any release

# To install lumiCalc.py
if [ "$LUMI" = "1" ]
then
git clone https://github.com/cms-sw/RecoLuminosity-LumiDB.git RecoLuminosity/LumiDB
pushd $CMSSW_BASE/src/RecoLuminosity/LumiDB
git checkout V04-02-10
pushd $CMSSW_BASE/src
fi

# Add and patch to way speed up trigger matching
# Don't crash if patch already applied.
set +o errexit
echo "Applying pat trigger matching speedup"
git cms-addpkg DataFormats/PatCandidates
git apply FinalStateAnalysis/recipe/patches/DataFormats_PatCandidates_TriggerEvent.cc.patch
set -o errexit


# Only checkout PAT tuple production dependencies if requested.
if [ "$PATPROD" = "1" ]
then
    #PU Jet ID Weights -- yes this way sucks
    git clone https://github.com/violatingcp/Jets_Short.git
    if [ -d "RecoJets/" ];
    then
      rm -r RecoJets/
    fi
    mv Jets_Short/RecoJets .
    mv Jets_Short/JetMETCorrections/Modules JetMETCorrections/.
    rm -rf Jets_Short
    
    # Set the compile time flag which enables PAT modules that have external
    # dependencies.
    cat > $CMSSW_BASE/src/FinalStateAnalysis/PatTools/interface/PATProductionFlag.h << EOF
#define ENABLE_PAT_PROD
EOF

else
    cat > $CMSSW_BASE/src/FinalStateAnalysis/PatTools/interface/PATProductionFlag.h << EOF
//#define ENABLE_PAT_PROD
EOF

fi

popd
